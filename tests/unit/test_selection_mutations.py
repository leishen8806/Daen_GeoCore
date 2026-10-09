# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportReturnType=false, reportMissingParameterType=false, reportUnusedImport=false, reportPrivateUsage=false

from dataclasses import dataclass

from daen_geocore.application.selection_mutations import (
    ADD_OPERATION,
    REPLACE_OPERATION,
    AddSelection,
    AddSelectionCommand,
    ReplaceSelection,
    ReplaceSelectionCommand,
    SelectionMutationOutcome,
    _decode_mapping,
    _slot,
)
from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.ports.evidence.store import (
    EvidenceLookupKey,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.failures import TechnicalFailureClass
from daen_geocore.ports.idempotency.store import (
    BindingRetention,
    CommittedMutationBinding,
    CommittedMutationResult,
    IdempotencyBindingKey,
)
from daen_geocore.ports.mutation import MutationBasisToken
from daen_geocore.ports.persistence.records import (
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityUnknown,
    PersistedTypedValue,
)
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import InMemoryCommittedIdempotencyStore


def _key(request: str) -> IdempotencyBindingKey:
    return IdempotencyBindingKey(OpaqueClientIdentity("unit"), OpaqueRequestIdentity(request))


def _scope() -> PersistedExplicitScope:
    return PersistedExplicitScope("language", OpaqueEncodedPayload("scope", b"km"), b"km")


def _add(request: str = "r") -> AddSelectionCommand:
    return AddSelectionCommand(
        _key(request),
        EvidenceLookupKey(request),
        IntentFingerprint("intent"),
        PlaceRef("place"),
        "name",
        MutationBasisToken("stale"),
        _scope(),
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"value")),
        (SourceAssertionRef("assertion"),),
        OpaqueEncodedPayload("attr", b"a"),
        OpaqueEncodedPayload("selection", b"p"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation", b"m"),
    )


@dataclass
class _Uow:
    committed_idempotency: object

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def rollback(self) -> None:
        return None


class _Factory:
    def __init__(self, store: object):
        self.store = store

    def create(self):
        return _Uow(self.store)


def _operation(store: object) -> AddSelection:
    return AddSelection(_Factory(store), None, None, None, None, None)  # type: ignore[arg-type]


def test_slot_requires_established_equality_key() -> None:
    assert (
        _slot(
            PlaceRef("p"),
            "name",
            PersistedExplicitScope("language", OpaqueEncodedPayload("s", b"")),
        )
        is None
    )


def test_replay_precedes_malformed_scope_support_and_basis() -> None:
    store = InMemoryCommittedIdempotencyStore()
    command = _add()
    ref = SelectionRecordRef("selection-1")
    store.bindings[command.key] = CommittedMutationBinding(
        command.key,
        command.intent_fingerprint,
        ADD_OPERATION,
        CommittedMutationResult(
            (ref,), OpaqueReplayMetadata((("result_kind", "selection_added"),))
        ),
        BindingRetention.PUBLIC_REPLAY_HORIZON,
    )
    replay = _operation(store).execute(command)
    assert isinstance(replay, PortSuccess)
    assert replay.value.outcome is SelectionMutationOutcome.REPLAY
    assert replay.value.selection_record_ref == ref


def test_replay_shape_rejects_wrong_replace_reference_type() -> None:
    store = InMemoryCommittedIdempotencyStore()
    command = _add("replace")
    replace = ReplaceSelectionCommand(
        command.key,
        command.evidence_lookup_key,
        command.intent_fingerprint,
        command.place_ref,
        SelectionRecordRef("prior"),
        command.fact_purpose,
        command.mutation_basis,
        command.scope,
        command.value,
        command.supporting_assertion_refs,
        command.attribution,
        command.provenance,
        command.quality,
        command.mutation_provenance,
    )
    store.bindings[replace.key] = CommittedMutationBinding(
        replace.key,
        replace.intent_fingerprint,
        REPLACE_OPERATION,
        CommittedMutationResult(
            (replace.prior_selection_record_ref, PlaceRef("wrong")),
            OpaqueReplayMetadata((("result_kind", "selection_replaced"),)),
        ),
        BindingRetention.PUBLIC_REPLAY_HORIZON,
    )
    result = ReplaceSelection(_Factory(store), None, None, None, None, None).execute(replace)  # type: ignore[arg-type]
    assert isinstance(result, PortSuccess)
    assert result.value.outcome is SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA


def test_recovery_metadata_fails_closed_for_duplicate_or_invalid_entries() -> None:
    base = RequestReferenceRecoveryMapping(
        OpaqueClientIdentity("c"),
        OpaqueRequestIdentity("r"),
        IntentFingerprint("i"),
        ADD_OPERATION,
        (SelectionRecordRef("s"),),
        OpaqueReplayMetadata((("state_witness", "w"), ("state_witness", "w2"))),
    )
    assert _decode_mapping(base) is None
    invalid = RequestReferenceRecoveryMapping(
        base.client_identity,
        base.request_identity,
        base.intent_fingerprint,
        base.operation_key,
        (SelectionRecordRef("s"),),
        OpaqueReplayMetadata((("state_witness", ""), ("recorded_at", "2026-10-09T15:00:00"))),
    )
    assert _decode_mapping(invalid) is None


def test_idempotency_port_error_is_not_semantic_conflict() -> None:
    failure = PortError(
        PortFailure("idempotency_down", TechnicalFailureClass.TRANSIENT_UNAVAILABLE)
    )

    class Store:
        def read(self, _key):
            return failure

    result = _operation(Store()).execute(_add("technical"))
    assert isinstance(result, PortError)
