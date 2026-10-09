from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from daen_geocore.application.source_assertion_create import (
    SOURCE_ASSERTION_CREATE_OPERATION,
    CreateSourceAssertion,
    CreateSourceAssertionCommand,
    MutationUnitOfWork,
    SourceAssertionCreateOutcome,
)
from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
from daen_geocore.ports.audit.store import MutationAuditRecord
from daen_geocore.ports.clock import Clock
from daen_geocore.ports.evidence.store import (
    EvidenceAbsent,
    EvidenceCreated,
    EvidenceFound,
    EvidenceLookupKey,
    ReferenceReservationEvidence,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.failures import TechnicalFailureClass
from daen_geocore.ports.idempotency.store import (
    CommittedIdempotencyStore,
    IdempotencyBindingKey,
)
from daen_geocore.ports.persistence.commit import (
    CommitAccepted,
    CommitNotCommitted,
    CommitOutcome,
    CommitUnknown,
)
from daen_geocore.ports.persistence.records import (
    AssertionStandingHead,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedQualityUnknown,
    PersistedTypedValue,
    PersistedUnknownScope,
    PlaceIdentityRecord,
    RecordAbsent,
    RecordFound,
    SourceAssertionRecord,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryObservation, RecoveryState
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess
from daen_geocore.ports.technical import (
    EvidenceLookupKey as TechnicalEvidenceLookupKey,
)
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
)

NOW = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)


@dataclass
class FakeEvidence:
    available: bool = True
    mappings: dict[EvidenceLookupKey, RequestReferenceRecoveryMapping] = field(default_factory=dict)
    reservations: dict[EvidenceLookupKey, ReferenceReservationEvidence] = field(
        default_factory=dict
    )
    mapping_reads: int = 0
    reservation_writes: int = 0

    def read_request_mapping(self, key):
        self.mapping_reads += 1
        if not self.available:
            return PortError(
                PortFailure("evidence_unavailable", TechnicalFailureClass.TRANSIENT_UNAVAILABLE)
            )
        record = self.mappings.get(key)
        return PortSuccess(EvidenceAbsent() if record is None else EvidenceFound(record))

    def create_request_mapping_if_absent(self, key, record):
        if not self.available:
            return PortError(PortFailure("evidence_unavailable"))
        existing = self.mappings.get(key)
        if existing is None:
            self.mappings[key] = record
            return PortSuccess(EvidenceCreated())
        return PortSuccess(EvidenceCreated() if existing == record else object())

    def create_reservation_if_absent(self, key, record):
        self.reservation_writes += 1
        if not self.available:
            return PortError(PortFailure("evidence_unavailable"))
        existing = self.reservations.get(key)
        if existing is None:
            self.reservations[key] = record
            return PortSuccess(EvidenceCreated())
        from daen_geocore.ports.evidence.store import (
            EvidenceAlreadyPresentConflict,
            EvidenceAlreadyPresentSame,
        )

        return PortSuccess(
            EvidenceAlreadyPresentSame() if existing == record else EvidenceAlreadyPresentConflict()
        )

    def read_reservation(self, key):
        record = self.reservations.get(key)
        return PortSuccess(EvidenceAbsent() if record is None else EvidenceFound(record))


@dataclass
class FakeIdentity:
    places: set[PlaceRef] = field(default_factory=set)

    def get_place(self, place_ref):
        return (
            PortSuccess(RecordFound(PlaceIdentityRecord(place_ref, NOW)))
            if place_ref in self.places
            else PortSuccess(RecordAbsent())
        )


@dataclass
class FakeAssertions:
    records: dict[SourceAssertionRef, SourceAssertionRecord] = field(default_factory=dict)
    heads: dict[SourceAssertionRef, AssertionStandingHead] = field(default_factory=dict)

    def insert_assertion_if_absent(self, record):
        existing = self.records.get(record.source_assertion_ref)
        if existing is None:
            self.records[record.source_assertion_ref] = record
            return PortSuccess(InsertDisposition.INSERTED)
        return PortSuccess(
            InsertDisposition.ALREADY_PRESENT_SAME
            if existing == record
            else InsertDisposition.CONFLICTING_EXISTING
        )

    def insert_standing_head_if_absent(self, head):
        existing = self.heads.get(head.source_assertion_ref)
        if existing is None:
            self.heads[head.source_assertion_ref] = head
            return PortSuccess(InsertDisposition.INSERTED)
        return PortSuccess(
            InsertDisposition.ALREADY_PRESENT_SAME
            if existing == head
            else InsertDisposition.CONFLICTING_EXISTING
        )


@dataclass
class FakeAudit:
    records: dict[object, MutationAuditRecord] = field(default_factory=dict)

    def append_if_absent(self, record):
        existing = self.records.get(record.key)
        if existing is None:
            self.records[record.key] = record
            return PortSuccess(InsertDisposition.INSERTED)
        return PortSuccess(
            InsertDisposition.ALREADY_PRESENT_SAME
            if existing == record
            else InsertDisposition.CONFLICTING_EXISTING
        )

    def read(self, key):
        return PortSuccess(self.records.get(key))


class FakeUow(MutationUnitOfWork):
    def __init__(
        self, identity, assertions, committed, audit, outcome: CommitOutcome | None = None
    ):
        self.identity, self.assertions = identity, assertions
        self.committed_idempotency, self.mutation_audit = committed, audit
        self.outcome = CommitAccepted() if outcome is None else outcome
        self.rollback_count = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def commit(self):
        return self.outcome

    def rollback(self):
        self.rollback_count += 1


@dataclass
class FakeFactory:
    identity: FakeIdentity
    assertions: FakeAssertions
    committed: CommittedIdempotencyStore
    audit: FakeAudit
    outcome: CommitOutcome | None = None
    created: list[FakeUow] = field(default_factory=list)

    def create(self):
        uow = FakeUow(self.identity, self.assertions, self.committed, self.audit, self.outcome)
        self.created.append(uow)
        return uow


class FakeCandidates:
    def __init__(self):
        self.count = 0

    def new_source_assertion_ref(self):
        self.count += 1
        return SourceAssertionRef(f"assertion-{self.count}")

    def new_state_witness(self):
        self.count += 1
        from daen_geocore.ports.persistence.records import StateWitness

        return StateWitness(f"witness-{self.count}")


class FakeClock(Clock):
    def __init__(self):
        self.calls = 0

    def now(self):
        self.calls += 1
        return NOW


class FakeGate:
    def observation(self):
        return RecoveryObservation(RecoveryState.READY, RecoveryIncarnation("r1"))


def command(request="request-1", intent="intent-1", place="place-1"):
    return CreateSourceAssertionCommand(
        IdempotencyBindingKey(OpaqueClientIdentity("client"), OpaqueRequestIdentity(request)),
        TechnicalEvidenceLookupKey(f"evidence-{request}"),
        IntentFingerprint(intent),
        PlaceRef(place),
        "address",
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"value")),
        PersistedUnknownScope(),
        OpaqueEncodedPayload("source.v1", b"source"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation.v1", b"mutation"),
    )


def operation(identity=None, evidence=None, factory=None, candidates=None, clock=None):
    identity = identity or FakeIdentity({PlaceRef("place-1")})
    evidence = evidence or FakeEvidence()
    assertions = FakeAssertions()
    from tests.fakes.mutation_runtime import InMemoryCommittedIdempotencyStore

    committed = InMemoryCommittedIdempotencyStore()
    audit = FakeAudit()
    factory = factory or FakeFactory(identity, assertions, committed, audit)
    return (
        CreateSourceAssertion(
            factory, evidence, FakeGate(), candidates or FakeCandidates(), clock or FakeClock()
        ),
        factory,
        evidence,
        assertions,
        committed,
        audit,
    )


def test_create_replay_is_before_evidence_and_unknown_place_has_no_side_effect() -> None:
    op, factory, evidence, assertions, committed, audit = operation()
    first = op.execute(command())
    assert first.value.outcome is SourceAssertionCreateOutcome.APPLIED
    reads, writes = evidence.mapping_reads, evidence.reservation_writes
    replay = op.execute(command())
    assert replay.value.outcome is SourceAssertionCreateOutcome.REPLAY
    assert replay.value.source_assertion_ref == first.value.source_assertion_ref
    assert evidence.mapping_reads == reads and evidence.reservation_writes == writes
    unknown = op.execute(command(request="unknown", place="missing"))
    assert unknown.value.outcome is SourceAssertionCreateOutcome.TARGET_PLACE_NOT_FOUND
    assert len(assertions.records) == 1 and len(audit.records) == 1


def test_recovery_reuses_ref_witness_and_recorded_at_without_clock_or_candidate() -> None:
    candidates = FakeCandidates()
    clock = FakeClock()
    op, _, evidence, assertions, _, _ = operation(candidates=candidates, clock=clock)
    first = op.execute(command())
    second = op.execute(command(request="other"))
    assert first.value.source_assertion_ref != second.value.source_assertion_ref
    assert candidates.count == 4 and clock.calls == 2
    mapping = next(iter(evidence.mappings.values()))
    assert mapping.operation_key == SOURCE_ASSERTION_CREATE_OPERATION
    assert len(assertions.records) == 2


def test_reservation_failure_prevents_authoritative_writes() -> None:
    evidence = FakeEvidence(available=False)
    op, factory, _, assertions, committed, audit = operation(evidence=evidence)
    result = op.execute(command())
    assert isinstance(result, PortError)
    assert len(factory.created) == 1
    assert not assertions.records and not committed.bindings and not audit.records


def test_same_request_different_intent_conflicts_without_new_candidate() -> None:
    op, _, evidence, assertions, _, _ = operation()
    assert op.execute(command()).value.outcome is SourceAssertionCreateOutcome.APPLIED
    writes = evidence.reservation_writes
    result = op.execute(command(intent="different"))
    assert result.value.outcome is SourceAssertionCreateOutcome.IDEMPOTENCY_CONFLICT
    assert evidence.reservation_writes == writes
    assert len(assertions.records) == 1


def test_commit_not_committed_is_explicit() -> None:
    identity = FakeIdentity({PlaceRef("place-1")})
    assertions = FakeAssertions()
    from tests.fakes.mutation_runtime import InMemoryCommittedIdempotencyStore

    factory = FakeFactory(
        identity, assertions, InMemoryCommittedIdempotencyStore(), FakeAudit(), CommitNotCommitted()
    )
    op = CreateSourceAssertion(factory, FakeEvidence(), FakeGate(), FakeCandidates(), FakeClock())
    assert op.execute(command()).value.outcome is SourceAssertionCreateOutcome.NOT_COMMITTED


def test_malformed_recovery_metadata_fails_closed_without_new_candidate() -> None:
    evidence = FakeEvidence()
    cmd = command()
    evidence.mappings[cmd.evidence_lookup_key] = RequestReferenceRecoveryMapping(
        cmd.key.client_identity,
        cmd.key.request_identity,
        cmd.intent_fingerprint,
        SOURCE_ASSERTION_CREATE_OPERATION,
        (SourceAssertionRef("existing"),),
        OpaqueReplayMetadata((("wrong", "metadata"),)),
    )
    candidates = FakeCandidates()
    op, _, _, assertions, _, _ = operation(evidence=evidence, candidates=candidates)
    result = op.execute(cmd)
    assert result.value.outcome is SourceAssertionCreateOutcome.MALFORMED_RECOVERY_METADATA
    assert candidates.count == 0 and not assertions.records


class ConflictingReservationEvidence(FakeEvidence):
    def create_reservation_if_absent(self, key, record):
        from daen_geocore.ports.evidence.store import EvidenceAlreadyPresentConflict

        return PortSuccess(EvidenceAlreadyPresentConflict())


def test_reference_reservation_conflict_fails_closed() -> None:
    op, factory, _, assertions, committed, audit = operation(
        evidence=ConflictingReservationEvidence()
    )
    result = op.execute(command())
    assert result.value.outcome is SourceAssertionCreateOutcome.REFERENCE_EVIDENCE_CONFLICT
    assert (
        len(factory.created) == 1
        and not assertions.records
        and not committed.bindings
        and not audit.records
    )


def test_commit_unknown_is_explicit() -> None:
    factory = None
    identity = FakeIdentity({PlaceRef("place-1")})
    assertions = FakeAssertions()
    from tests.fakes.mutation_runtime import InMemoryCommittedIdempotencyStore

    committed = InMemoryCommittedIdempotencyStore()
    audit = FakeAudit()
    factory = FakeFactory(identity, assertions, committed, audit, CommitUnknown(reason="network"))
    op = CreateSourceAssertion(factory, FakeEvidence(), FakeGate(), FakeCandidates(), FakeClock())
    assert (
        op.execute(command()).value.outcome is SourceAssertionCreateOutcome.COMMIT_OUTCOME_UNKNOWN
    )


def test_explicit_scope_quality_and_provenance_are_preserved_without_selection() -> None:
    from daen_geocore.ports.persistence.records import PersistedExplicitScope, PersistedQualityKnown

    op, _, _, assertions, _, audit = operation()
    source = OpaqueEncodedPayload("source.v2", b"origin")
    mutation = OpaqueEncodedPayload("mutation.v2", b"context")
    result = op.execute(
        replace(
            command(),
            scope=PersistedExplicitScope(
                "language", OpaqueEncodedPayload("scope.v1", b"km"), b"km"
            ),
            quality=PersistedQualityKnown(OpaqueEncodedPayload("quality.v1", b"known")),
            source_provenance=source,
            mutation_provenance=mutation,
        )
    )
    assert result.value.outcome is SourceAssertionCreateOutcome.APPLIED
    record = next(iter(assertions.records.values()))
    audit_record = next(iter(audit.records.values()))
    assert record.provenance == source
    assert audit_record.mutation_provenance == mutation
    assert record.provenance != audit_record.mutation_provenance
