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
from daen_geocore.ports.failures import TechnicalFailureClass
from daen_geocore.ports.idempotency.store import (
    BindingRetention,
    CommittedBindingAbsent,
    CommittedBindingFound,
    CommittedIdempotencyStore,
    CommittedMutationBinding,
    CommittedMutationResult,
    IdempotencyBindingKey,
    IdempotencyCreateDisposition,
)
from daen_geocore.ports.mutation import (
    MutationBasisClaims,
    MutationBasisToken,
    ObservedOwnerState,
    OwnerAbsent,
    OwnerPresent,
    PlaceOwner,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted, CommitUnknown
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
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
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


class BrokenIdentity:
    def __init__(self, identity, method, failure):
        self.identity, self.method, self.failure = identity, method, failure

    def __getattr__(self, name):
        if name == self.method:
            return lambda *_args, **_kwargs: self.failure
        return getattr(self.identity, name)


@dataclass
class Audit:
    records: dict[IdempotencyBindingKey, MutationAuditRecord] = field(default_factory=dict)

    def append_if_absent(self, record):
        if record.key in self.records:
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        self.records[record.key] = record
        return PortSuccess(InsertDisposition.INSERTED)


class BrokenAudit(Audit):
    def append_if_absent(self, _record):
        return PortError(PortFailure("audit_down", TechnicalFailureClass.TRANSIENT_UNAVAILABLE))


@dataclass
class Uow:
    identity: Identity
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: Audit
    assertions: object = field(default_factory=object)
    representation: object = field(default_factory=object)
    commit_outcome: object = field(default_factory=CommitAccepted)

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def commit(self):
        return self.commit_outcome

    def rollback(self):
        return None


class Factory:
    def __init__(self, identity, committed, audit, commit_outcome=None):
        self.identity, self.committed, self.audit, self.commit_outcome = (
            identity,
            committed,
            audit,
            commit_outcome,
        )

    def create(self):
        return Uow(
            self.identity,
            self.committed,
            self.audit,
            commit_outcome=self.commit_outcome or CommitAccepted(),
        )


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


class BrokenBindingStore(InMemoryCommittedStore):
    def create_if_absent(self, _binding):
        return PortError(PortFailure("binding_down", TechnicalFailureClass.TRANSIENT_UNAVAILABLE))


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


def test_committed_replay_is_operation_specific_and_shape_strict():
    place, identity, committed, audit, codec, token = _setup()
    command = _command(place, token, "close-replay")
    committed.bindings[command.key] = CommittedMutationBinding(
        command.key,
        command.intent_fingerprint,
        TechnicalOperationKey("place.close"),
        CommittedMutationResult(
            (place,), OpaqueReplayMetadata((("result_kind", "place_withdrawn"),))
        ),
        BindingRetention.PUBLIC_REPLAY_HORIZON,
    )
    result = _operation(
        "close", Factory(identity, committed, audit), Gate(), codec, Generator()
    ).execute(command)
    assert result.value.outcome is PlaceMutationOutcome.IDEMPOTENCY_CONFLICT


def test_basis_matrix_covers_missing_unrelated_absent_and_stale_owner():
    place, identity, committed, audit, codec, token = _setup()
    factory = Factory(identity, committed, audit)
    operation = _operation("close", factory, Gate(), codec, Generator())
    cases = (
        (),
        (ObservedOwnerState(PlaceOwner(PlaceRef("other")), OwnerPresent(StateWitness("w"))),),
        (ObservedOwnerState(PlaceOwner(place), OwnerAbsent()),),
        (ObservedOwnerState(PlaceOwner(place), OwnerPresent(StateWitness("wrong"))),),
    )
    expected = (
        PlaceMutationOutcome.INSUFFICIENT_BASIS,
        PlaceMutationOutcome.INSUFFICIENT_BASIS,
        PlaceMutationOutcome.INSUFFICIENT_BASIS,
        PlaceMutationOutcome.STALE_BASIS,
    )
    for index, (claims, outcome) in enumerate(zip(cases, expected, strict=True)):
        current = codec.issue(MutationBasisClaims(RecoveryIncarnation("r1"), claims)).value
        result = operation.execute(_command(place, current, f"basis-{index}"))
        assert result.value.outcome is outcome


def test_commit_outcomes_are_exposed_without_retry():
    for commit_outcome, expected in (
        (CommitNotCommitted(), PlaceMutationOutcome.NOT_COMMITTED),
        (CommitUnknown(), PlaceMutationOutcome.COMMIT_OUTCOME_UNKNOWN),
    ):
        place, identity, committed, audit, codec, token = _setup()
        generator = Generator()
        operation = _operation(
            "close", Factory(identity, committed, audit, commit_outcome), Gate(), codec, generator
        )
        result = operation.execute(_command(place, token, f"commit-{expected.value}"))
        assert result.value.outcome is expected
        assert generator.n == 2


def test_idempotency_port_error_is_preserved():
    place, identity, committed, audit, codec, token = _setup()
    failure = PortError(PortFailure("down", TechnicalFailureClass.TRANSIENT_UNAVAILABLE))

    class BrokenStore(InMemoryCommittedStore):
        def read(self, _key):
            return failure

    result = _operation(
        "close", Factory(identity, BrokenStore(), audit), Gate(), codec, Generator()
    ).execute(_command(place, token, "technical-idempotency"))
    assert result is failure


def test_place_ports_and_audit_binding_errors_stay_technical():
    place, identity, committed, audit, codec, token = _setup()
    failure = PortError(PortFailure("port_down", TechnicalFailureClass.TRANSIENT_UNAVAILABLE))

    def run(factory, name):
        return _operation("close", factory, Gate(), codec, Generator()).execute(
            _command(place, token, name)
        )

    assert (
        run(Factory(BrokenIdentity(identity, "get_place", failure), committed, audit), "place")
        is failure
    )
    assert (
        run(Factory(BrokenIdentity(identity, "get_place_head", failure), committed, audit), "head")
        is failure
    )
    assert (
        run(
            Factory(BrokenIdentity(identity, "list_place_history", failure), committed, audit),
            "history",
        )
        is failure
    )
    assert (
        run(
            Factory(
                BrokenIdentity(identity, "append_place_history_if_absent", failure),
                committed,
                audit,
            ),
            "append",
        )
        is failure
    )
    assert (
        run(
            Factory(
                BrokenIdentity(identity, "compare_and_swap_place_head", failure), committed, audit
            ),
            "cas",
        )
        is failure
    )
    audit_error = run(Factory(identity, committed, BrokenAudit()), "audit")
    binding_error = run(Factory(identity, BrokenBindingStore(), audit), "binding")
    assert isinstance(audit_error, PortError) and audit_error.failure.code == "audit_down"
    assert isinstance(binding_error, PortError) and binding_error.failure.code == "binding_down"
