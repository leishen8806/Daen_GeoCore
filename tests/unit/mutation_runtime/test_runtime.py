from dataclasses import dataclass

from daen_geocore.application.mutation_runtime import (
    BasisValidation,
    IdempotencyReplayDecider,
    MutationBasisClaims,
    MutationBasisToken,
    MutationBasisValidator,
    ReadSetRevalidator,
    ReadSetValidation,
    RecoveryMappingCoordinator,
    RecoveryMappingOutcome,
    ReferenceReservationCoordinator,
    ReferenceReservationPlan,
    ReplayDecision,
    ReservationOutcome,
)
from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.ports.evidence.store import RequestReferenceRecoveryMapping
from daen_geocore.ports.idempotency import (
    CommittedMutationBinding,
    CommittedMutationResult,
    IdempotencyBindingKey,
)
from daen_geocore.ports.mutation import (
    AssertionOwner,
    AuthoritativeReadSet,
    ObservedOwnerState,
    OwnerAbsent,
    OwnerPresent,
    OwnerStateReader,
    PlaceOwner,
    SelectionSlotOwner,
)
from daen_geocore.ports.persistence.records import (
    AssertionStandingHead,
    RecordAbsent,
    RecordFound,
    SelectionSlotHead,
    SelectionSlotKey,
    StateWitness,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryState
from daen_geocore.ports.result import PortError, PortSuccess
from daen_geocore.ports.technical import (
    EvidenceLookupKey,
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
)

from ...fakes.mutation_runtime import FakeMutationBasisCodec, InMemoryCommittedIdempotencyStore
from ...fakes.ports import FakeRecoveryGate, InMemoryEvidenceStore


@dataclass
class FakeRepos:
    place: StateWitness | None = None
    assertion: StateWitness | None = None
    selection: StateWitness | None = None

    @property
    def identity(self):
        return self

    @property
    def assertions(self):
        return self

    @property
    def representation(self):
        return self

    def get_place_head(self, ref):
        return PortSuccess(
            RecordAbsent()
            if self.place is None
            else RecordFound(type("H", (), {"state_witness": self.place})())
        )

    def get_standing_head(self, ref):
        return PortSuccess(
            RecordAbsent()
            if self.assertion is None
            else RecordFound(AssertionStandingHead(ref, None, self.assertion))
        )

    def get_selection_slot_head(self, slot):
        return PortSuccess(
            RecordAbsent()
            if self.selection is None
            else RecordFound(SelectionSlotHead(slot, SelectionRecordRef("S"), self.selection))
        )


def owners():
    return (
        PlaceOwner(PlaceRef("P")),
        AssertionOwner(SourceAssertionRef("A")),
        SelectionSlotOwner(SelectionSlotKey(PlaceRef("P"), "name", "language", b"km")),
    )


def test_owner_states_and_basis_readset_are_distinct():
    repos = FakeRepos(StateWitness("W"), StateWitness("W"), StateWitness("W"))
    reader = OwnerStateReader()
    observed = tuple(
        ObservedOwnerState(owner, reader.read(owner, repos).value) for owner in owners()
    )
    assert all(isinstance(item.state, OwnerPresent) for item in observed)
    repos.place = repos.assertion = repos.selection = None
    assert all(isinstance(reader.read(owner, repos).value, OwnerAbsent) for owner in owners())
    basis = MutationBasisClaims(RecoveryIncarnation("R1"), observed)
    read_set = AuthoritativeReadSet(observed)
    assert type(basis) is not type(read_set)
    assert not hasattr(read_set, "token")


def test_basis_tamper_recovery_and_owner_validation():
    repos = FakeRepos(StateWitness("W"), None, None)
    gate = FakeRecoveryGate(RecoveryState.READY, RecoveryIncarnation("R1"))
    codec = FakeMutationBasisCodec()
    owner = PlaceOwner(PlaceRef("P"))
    claims = MutationBasisClaims(
        RecoveryIncarnation("R1"), (ObservedOwnerState(owner, OwnerPresent(StateWitness("W"))),)
    )
    token = codec.issue(claims).value
    validator = MutationBasisValidator(codec, gate, OwnerStateReader())
    assert validator.validate(token, repos).value is BasisValidation.VALID
    gate.incarnation = RecoveryIncarnation("R2")
    assert validator.validate(token, repos).value is BasisValidation.RECOVERY_INCARNATION_MISMATCH
    assert (
        validator.validate(MutationBasisToken("tampered"), repos).value
        is BasisValidation.INVALID_TOKEN
    )


def test_readset_revalidation_detects_change_and_absence_to_present():
    repos = FakeRepos(StateWitness("W"), None, None)
    reader = OwnerStateReader()
    owner = PlaceOwner(PlaceRef("P"))
    read_set = AuthoritativeReadSet((ObservedOwnerState(owner, OwnerPresent(StateWitness("W"))),))
    repos.place = StateWitness("W2")
    assert (
        ReadSetRevalidator(reader).revalidate(read_set, repos).value
        is ReadSetValidation.OWNER_STATE_MISMATCH
    )
    absent_set = AuthoritativeReadSet((ObservedOwnerState(owner, OwnerAbsent()),))
    repos.place = StateWitness("W3")
    assert (
        ReadSetRevalidator(reader).revalidate(absent_set, repos).value
        is ReadSetValidation.OWNER_STATE_MISMATCH
    )


def mapping(intent: str, place: str = "P"):
    return RequestReferenceRecoveryMapping(
        OpaqueClientIdentity("C"),
        OpaqueRequestIdentity("R"),
        IntentFingerprint(intent),
        TechnicalOperationKey("op"),
        (PlaceRef(place), SourceAssertionRef("A1")),
        OpaqueReplayMetadata((("x", "1"),)),
    )


def test_reference_reservation_fails_closed_and_reuses_same():
    key = EvidenceLookupKey("reservation")
    plan = ReferenceReservationPlan(key, (PlaceRef("P"),))
    blocked = ReferenceReservationCoordinator(
        FakeRecoveryGate(RecoveryState.BLOCKED, None), InMemoryEvidenceStore()
    )
    assert blocked.reserve(plan).value is ReservationOutcome.BLOCKED
    store = InMemoryEvidenceStore()
    coordinator = ReferenceReservationCoordinator(
        FakeRecoveryGate(RecoveryState.READY, RecoveryIncarnation("R")), store
    )
    assert coordinator.reserve(plan).value is ReservationOutcome.PREPARED
    assert coordinator.reserve(plan).value is ReservationOutcome.PREPARED
    assert (
        coordinator.reserve(ReferenceReservationPlan(key, (PlaceRef("Q"),))).value
        is ReservationOutcome.CONFLICTING_EVIDENCE
    )
    store.available = False
    assert isinstance(
        coordinator.reserve(ReferenceReservationPlan(EvidenceLookupKey("other"), (PlaceRef("Q"),))),
        PortError,
    )


def test_mapping_exact_reuse_and_conflict_without_commit_inference():
    store = InMemoryEvidenceStore()
    coordinator = RecoveryMappingCoordinator(store)
    key = EvidenceLookupKey("mapping")
    first = coordinator.resolve(key, mapping("intent-a")).value
    second = coordinator.resolve(key, mapping("intent-a", "P2")).value
    conflict = coordinator.resolve(key, mapping("intent-b", "P3")).value
    assert first.outcome is RecoveryMappingOutcome.CREATED
    assert second.outcome is RecoveryMappingOutcome.REUSED
    assert second.mapping == first.mapping
    assert conflict.outcome is RecoveryMappingOutcome.CONFLICT
    store.available = False
    assert isinstance(coordinator.resolve(key, mapping("intent-a")), PortError)


def test_idempotency_replay_and_conflict_without_basis_identity():
    key = IdempotencyBindingKey(OpaqueClientIdentity("C"), OpaqueRequestIdentity("R"))
    binding = CommittedMutationBinding(
        key,
        IntentFingerprint("I"),
        TechnicalOperationKey("op"),
        CommittedMutationResult((PlaceRef("P"),)),
    )
    store = InMemoryCommittedIdempotencyStore()
    assert store.create_if_absent(binding).value.value == "created"
    decider = IdempotencyReplayDecider(store)
    assert (
        decider.decide(key, IntentFingerprint("I"), TechnicalOperationKey("op")).value.decision
        is ReplayDecision.REPLAY
    )
    assert (
        decider.decide(key, IntentFingerprint("J"), TechnicalOperationKey("op")).value.decision
        is ReplayDecision.CONFLICT
    )
    assert (
        decider.decide(key, IntentFingerprint("I"), TechnicalOperationKey("other")).value.decision
        is ReplayDecision.CONFLICT
    )
    assert (
        decider.decide(
            IdempotencyBindingKey(OpaqueClientIdentity("C"), OpaqueRequestIdentity("new")),
            IntentFingerprint("I"),
            TechnicalOperationKey("op"),
        ).value.decision
        is ReplayDecision.EXECUTE
    )
    store.available = False
    assert isinstance(
        decider.decide(key, IntentFingerprint("I"), TechnicalOperationKey("op")), PortError
    )
