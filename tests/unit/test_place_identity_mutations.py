from dataclasses import dataclass, field
from datetime import UTC, datetime

from daen_geocore.application.place_identity_mutations import (
    CLOSE_FACT_TYPE,
    WITHDRAW_FACT_TYPE,
    ClosePlace,
    ClosePlaceCommand,
    PlaceMutationOutcome,
    WithdrawPlace,
    WithdrawPlaceCommand,
)
from daen_geocore.domain.references import PlaceRef
from daen_geocore.ports.audit.store import MutationAuditRecord
from daen_geocore.ports.clock import Clock
from daen_geocore.ports.idempotency.store import (
    CommittedBindingAbsent,
    CommittedBindingFound,
    CommittedIdempotencyStore,
    IdempotencyBindingKey,
    IdempotencyCreateDisposition,
)
from daen_geocore.ports.mutation import (
    MutationBasisClaims,
    MutationBasisToken,
    ObservedOwnerState,
    OwnerPresent,
    PlaceOwner,
)
from daen_geocore.ports.persistence.commit import CommitAccepted
from daen_geocore.ports.persistence.records import (
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PlaceHead,
    PlaceHistoryFact,
    PlaceHistoryFactRef,
    PlaceIdentityRecord,
    RecordAbsent,
    RecordFound,
    StateWitness,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryObservation, RecoveryState
from daen_geocore.ports.result import PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import FakeMutationBasisCodec

NOW = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)


class Gate:
    def __init__(
        self, ready: bool = True, incarnation: str = "r1", validated_incarnation: str | None = None
    ) -> None:
        self.ready = ready
        self.incarnation = incarnation
        self.validated_incarnation = validated_incarnation or incarnation

    def observation(self):
        return RecoveryObservation(
            RecoveryState.READY if self.ready else RecoveryState.BLOCKED,
            RecoveryIncarnation(self.incarnation) if self.ready else None,
        )

    def validate_before_authoritative_serving(self):
        return PortSuccess(RecoveryIncarnation(self.validated_incarnation))


class ClockStub(Clock):
    def now(self):
        return NOW


class Generator:
    def __init__(self) -> None:
        self.n = 0

    def new_place_history_fact_ref(self):
        self.n += 1
        return PlaceHistoryFactRef(f"history-{self.n}")

    def new_state_witness(self):
        self.n += 1
        return StateWitness(f"witness-{self.n}")


@dataclass
class Identity:
    places: dict[PlaceRef, PlaceIdentityRecord] = field(default_factory=dict)
    heads: dict[PlaceRef, PlaceHead] = field(default_factory=dict)
    history: dict[PlaceRef, list[PlaceHistoryFact]] = field(default_factory=dict)

    def get_place(self, ref):
        return PortSuccess(RecordFound(self.places[ref]) if ref in self.places else RecordAbsent())

    def get_place_head(self, ref):
        return PortSuccess(RecordFound(self.heads[ref]) if ref in self.heads else RecordAbsent())

    def list_place_history(self, ref):
        return PortSuccess(tuple(self.history.get(ref, ())))

    def append_place_history_if_absent(self, fact):
        items = self.history.setdefault(fact.place_ref, [])
        existing = next(
            (item for item in items if item.history_fact_ref == fact.history_fact_ref), None
        )
        if existing is not None:
            return PortSuccess(
                InsertDisposition.ALREADY_PRESENT_SAME
                if existing == fact
                else InsertDisposition.CONFLICTING_EXISTING
            )
        items.append(fact)
        return PortSuccess(InsertDisposition.INSERTED)

    def compare_and_swap_place_head(self, ref, expected, latest, witness):
        current = self.heads.get(ref)
        if current is None or current.state_witness != expected:
            return PortSuccess(ConditionalWriteDisposition.PRECONDITION_NOT_MET)
        self.heads[ref] = PlaceHead(ref, latest, witness)
        return PortSuccess(ConditionalWriteDisposition.APPLIED)


@dataclass
class Audit:
    records: dict[IdempotencyBindingKey, MutationAuditRecord] = field(default_factory=dict)

    def append_if_absent(self, record):
        if record.key in self.records:
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        self.records[record.key] = record
        return PortSuccess(InsertDisposition.INSERTED)


@dataclass
class Uow:
    identity: Identity
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: Audit
    assertions: object = field(default_factory=object)
    representation: object = field(default_factory=object)

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def commit(self):
        return CommitAccepted()

    def rollback(self):
        return None


class Factory:
    def __init__(self, identity, committed, audit):
        self.identity, self.committed, self.audit = identity, committed, audit

    def create(self):
        return Uow(self.identity, self.committed, self.audit)


def _key(name: str) -> IdempotencyBindingKey:
    return IdempotencyBindingKey(OpaqueClientIdentity("client"), OpaqueRequestIdentity(name))


def _setup():
    place = PlaceRef("place-1")
    identity = Identity(
        {place: PlaceIdentityRecord(place, NOW)},
        {place: PlaceHead(place, None, StateWitness("w0"))},
    )
    committed = InMemoryCommittedStore()
    audit = Audit()
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(PlaceOwner(place), OwnerPresent(StateWitness("w0"))),),
        )
    ).value
    return place, identity, committed, audit, codec, token


class InMemoryCommittedStore(CommittedIdempotencyStore):
    def __init__(self):
        self.bindings = {}

    def read(self, key):
        value = self.bindings.get(key)
        return PortSuccess(
            CommittedBindingAbsent() if value is None else CommittedBindingFound(value)
        )

    def create_if_absent(self, binding):
        current = self.bindings.get(binding.key)
        if current is None:
            self.bindings[binding.key] = binding
            return PortSuccess(IdempotencyCreateDisposition.CREATED)
        return PortSuccess(
            IdempotencyCreateDisposition.ALREADY_PRESENT_SAME
            if current == binding
            else IdempotencyCreateDisposition.CONFLICTING_EXISTING
        )


def _command(place, token, name="close", intent=None):
    common = dict(
        key=_key(name),
        intent_fingerprint=IntentFingerprint(intent or name),
        place_ref=place,
        mutation_basis=token,
        mutation_provenance=OpaqueEncodedPayload("actor", b"operator"),
    )
    return (
        ClosePlaceCommand(**common) if name.startswith("close") else WithdrawPlaceCommand(**common)
    )


def _operation(kind, factory, gate, codec, generator):
    cls = ClosePlace if kind == "close" else WithdrawPlace
    return cls(factory, gate, codec, generator, ClockStub())


def test_close_and_withdraw_are_distinct_and_replay_preserves_outcome():
    place, identity, committed, audit, codec, token = _setup()
    factory = Factory(identity, committed, audit)
    generator = Generator()
    close = _operation("close", factory, Gate(), codec, generator)
    close_command = _command(place, token, "close-1")
    first = close.execute(close_command)
    assert isinstance(first, PortSuccess)
    assert first.value.outcome is PlaceMutationOutcome.APPLIED
    assert identity.history[place][0].fact_type == CLOSE_FACT_TYPE
    replay = close.execute(close_command)
    assert replay.value.outcome is PlaceMutationOutcome.REPLAY
    assert replay.value.replayed_outcome is PlaceMutationOutcome.APPLIED

    fresh = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    PlaceOwner(place), OwnerPresent(identity.heads[place].state_witness)
                ),
            ),
        )
    ).value
    withdraw = _operation("withdraw", factory, Gate(), codec, generator)
    second = withdraw.execute(_command(place, fresh, "withdraw-1"))
    assert second.value.outcome is PlaceMutationOutcome.APPLIED
    assert {fact.fact_type for fact in identity.history[place]} == {
        CLOSE_FACT_TYPE,
        WITHDRAW_FACT_TYPE,
    }
    assert len(audit.records) == 2


def test_already_holds_is_distinct_from_replay_and_stale_basis_wins():
    place, identity, committed, audit, codec, token = _setup()
    factory = Factory(identity, committed, audit)
    close = _operation("close", factory, Gate(), codec, Generator())
    first = close.execute(_command(place, token, "close-1"))
    assert first.value.outcome is PlaceMutationOutcome.APPLIED
    stale = close.execute(_command(place, token, "close-2"))
    assert stale.value.outcome is PlaceMutationOutcome.STALE_BASIS
    fresh_token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    PlaceOwner(place), OwnerPresent(identity.heads[place].state_witness)
                ),
            ),
        )
    ).value
    duplicate = close.execute(_command(place, fresh_token, "close-3"))
    assert duplicate.value.outcome is PlaceMutationOutcome.ALREADY_HOLDS
    assert len(identity.history[place]) == 1
    assert len(audit.records) == 2


def test_invalid_basis_and_missing_target_are_fail_closed():
    place, identity, committed, audit, codec, token = _setup()
    factory = Factory(identity, committed, audit)
    close = _operation("close", factory, Gate(), codec, Generator())
    invalid = close.execute(_command(place, MutationBasisToken("bad"), "bad"))
    assert invalid.value.outcome is PlaceMutationOutcome.INVALID_BASIS
    missing = close.execute(_command(PlaceRef("missing"), token, "missing"))
    assert missing.value.outcome is PlaceMutationOutcome.TARGET_PLACE_NOT_FOUND


def test_missing_head_and_recovery_incarnation_mismatch_are_distinct():
    place, identity, committed, audit, codec, token = _setup()
    identity.heads.clear()
    factory = Factory(identity, committed, audit)
    close = _operation("close", factory, Gate(), codec, Generator())
    assert (
        close.execute(_command(place, token, "head-missing")).value.outcome
        is PlaceMutationOutcome.TARGET_PLACE_HEAD_MISSING
    )

    place, identity, committed, audit, codec, token = _setup()
    mismatch = _operation(
        "close",
        Factory(identity, committed, audit),
        Gate(validated_incarnation="r2"),
        codec,
        Generator(),
    )
    assert (
        mismatch.execute(_command(place, token, "incarnation")).value.outcome
        is PlaceMutationOutcome.RECOVERY_INCARNATION_MISMATCH
    )


def test_recovery_gate_blocks_fresh_work_but_not_committed_replay():
    place, identity, committed, audit, codec, token = _setup()
    factory = Factory(identity, committed, audit)
    close = _operation("close", factory, Gate(), codec, Generator())
    command = _command(place, token, "close-1")
    assert close.execute(command).value.outcome is PlaceMutationOutcome.APPLIED
    blocked = _operation("close", factory, Gate(False), codec, Generator()).execute(command)
    assert blocked.value.outcome is PlaceMutationOutcome.REPLAY


def test_withdraw_already_holds_and_replay_are_distinct():
    place, identity, committed, audit, codec, token = _setup()
    factory = Factory(identity, committed, audit)
    generator = Generator()
    operation = _operation("withdraw", factory, Gate(), codec, generator)
    command = _command(place, token, "withdraw-1")
    assert operation.execute(command).value.outcome is PlaceMutationOutcome.APPLIED
    assert operation.execute(command).value.outcome is PlaceMutationOutcome.REPLAY
    fresh = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    PlaceOwner(place), OwnerPresent(identity.heads[place].state_witness)
                ),
            ),
        )
    ).value
    duplicate = operation.execute(_command(place, fresh, "withdraw-2"))
    assert duplicate.value.outcome is PlaceMutationOutcome.ALREADY_HOLDS
    assert len(identity.history[place]) == 1
