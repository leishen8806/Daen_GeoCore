# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportReturnType=false, reportMissingParameterType=false, reportUnusedImport=false

import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import create_engine, select

from daen_geocore.application.selection_mutations import (
    AddSelection,
    AddSelectionCommand,
    ReplaceSelection,
    ReplaceSelectionCommand,
    SelectionMutationOutcome,
)
from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
from daen_geocore.infrastructure.postgres.mutation_factory import PostgresMutationUnitOfWorkFactory
from daen_geocore.infrastructure.postgres.schema import (
    assertions_source_assertion,
    assertions_standing_head,
    identity_place,
    representation_selection_record,
    representation_selection_slot_head,
    representation_selection_support,
)
from daen_geocore.ports.evidence.store import EvidenceLookupKey
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.mutation import (
    AssertionOwner,
    MutationBasisClaims,
    ObservedOwnerState,
    OwnerAbsent,
    OwnerPresent,
    SelectionSlotOwner,
)
from daen_geocore.ports.persistence.records import (
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityUnknown,
    PersistedTypedValue,
    SelectionSlotKey,
    StateWitness,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import FakeMutationBasisCodec
from tests.unit.test_source_assertion_transition import (
    Candidates,
    Evidence,
    FakeTransitionClock,
    Gate,
)

NOW = datetime(2026, 10, 9, 15, 0, tzinfo=UTC)
DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DAEN_TEST_DATABASE_URL is not configured")


def _config() -> Config:
    config = Config(str(Path("alembic.ini").resolve()))
    config.set_main_option("sqlalchemy.url", DATABASE_URL or "")
    return config


@pytest.fixture(scope="module")
def engine():
    assert DATABASE_URL is not None
    alembic_command.upgrade(_config(), "head")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    yield engine
    alembic_command.downgrade(_config(), "base")
    engine.dispose()


def _scope() -> PersistedExplicitScope:
    return PersistedExplicitScope("language", OpaqueEncodedPayload("scope", b"km"), b"km")


def _seed(engine, place: str, assertion: str) -> None:
    with engine.begin() as connection:
        connection.execute(identity_place.insert().values(place_ref=place, recorded_at=NOW))
        connection.execute(
            assertions_source_assertion.insert().values(
                source_assertion_ref=assertion,
                place_ref=place,
                fact_purpose="name",
                value_type_id="text",
                value_encoding="utf8",
                value_payload=b"source",
                scope_is_explicit=False,
                provenance_encoding="source",
                provenance_payload=b"source",
                quality_is_known=False,
                recorded_at=NOW,
            )
        )
        connection.execute(
            assertions_standing_head.insert().values(
                source_assertion_ref=assertion,
                latest_history_fact_ref=None,
                state_witness="w1",
            )
        )


def _key(request: str) -> IdempotencyBindingKey:
    return IdempotencyBindingKey(OpaqueClientIdentity("step12"), OpaqueRequestIdentity(request))


def test_postgres_selection_add_replace_and_replay(engine) -> None:
    place = PlaceRef("step12-place")
    assertion = SourceAssertionRef("step12-assertion")
    _seed(engine, place.token, assertion.token)
    scope = _scope()
    slot = SelectionSlotKey(place, "name", scope.type_id, scope.equality_key or b"")
    codec = FakeMutationBasisCodec()
    evidence = Evidence()
    add_token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),
                ObservedOwnerState(AssertionOwner(assertion), OwnerPresent(StateWitness("w1"))),
            ),
        )
    ).value
    add = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    )
    command = AddSelectionCommand(
        _key("add"),
        EvidenceLookupKey("step12-add"),
        IntentFingerprint("add-v1"),
        place,
        "name",
        add_token,
        scope,
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"selected")),
        (assertion,),
        OpaqueEncodedPayload("attribution", b"a"),
        OpaqueEncodedPayload("selection", b"p"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation", b"m"),
    )
    first = add.execute(command)
    assert first.value.outcome is SelectionMutationOutcome.APPLIED
    ref = first.value.selection_record_ref
    assert ref is not None
    replay = add.execute(command)
    assert replay.value.outcome is SelectionMutationOutcome.REPLAY
    assert replay.value.selection_record_ref == ref
    with engine.connect() as connection:
        head = (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            )
            .mappings()
            .one()
        )
    replace_token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    SelectionSlotOwner(slot), OwnerPresent(StateWitness(head["state_witness"]))
                ),
                ObservedOwnerState(AssertionOwner(assertion), OwnerPresent(StateWitness("w1"))),
            ),
        )
    ).value
    replace_candidates = Candidates()
    replace_candidates.calls = 1000
    replace = ReplaceSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        replace_candidates,
        FakeTransitionClock(),
    )
    replacement = replace.execute(
        ReplaceSelectionCommand(
            _key("replace"),
            EvidenceLookupKey("step12-replace"),
            IntentFingerprint("replace-v1"),
            place,
            ref,
            "name",
            replace_token,
            scope,
            PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"new")),
            (assertion,),
            OpaqueEncodedPayload("attribution", b"a2"),
            OpaqueEncodedPayload("selection", b"p2"),
            PersistedQualityUnknown(),
            OpaqueEncodedPayload("mutation", b"m2"),
        )
    )
    assert replacement.value.outcome is SelectionMutationOutcome.APPLIED
    assert replacement.value.selection_record_ref != ref
    with engine.connect() as connection:
        assert connection.execute(select(representation_selection_record)).mappings().all()
        assert connection.execute(select(representation_selection_support)).mappings().all()
