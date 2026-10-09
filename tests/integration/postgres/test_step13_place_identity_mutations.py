import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import create_engine, select

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
from daen_geocore.infrastructure.postgres.mutation_factory import PostgresMutationUnitOfWorkFactory
from daen_geocore.infrastructure.postgres.schema import (
    identity_place,
    identity_place_head,
    identity_place_history,
    mutation_audit,
    mutation_committed_binding,
)
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.mutation import (
    MutationBasisClaims,
    ObservedOwnerState,
    OwnerPresent,
    PlaceOwner,
)
from daen_geocore.ports.persistence.records import OpaqueEncodedPayload, StateWitness
from daen_geocore.ports.recovery.gate import RecoveryIncarnation
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import FakeMutationBasisCodec
from tests.unit.test_source_assertion_transition import Candidates, FakeTransitionClock, Gate

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


def _key(request: str) -> IdempotencyBindingKey:
    return IdempotencyBindingKey(OpaqueClientIdentity("step13"), OpaqueRequestIdentity(request))


def _seed(engine, place: PlaceRef) -> None:
    with engine.begin() as connection:
        connection.execute(identity_place.insert().values(place_ref=place.token, recorded_at=NOW))
        connection.execute(
            identity_place_head.insert().values(
                place_ref=place.token, latest_history_fact_ref=None, state_witness="w0"
            )
        )


def _token(codec, place: PlaceRef, witness: str):
    return codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(PlaceOwner(place), OwnerPresent(StateWitness(witness))),),
        )
    ).value


def test_postgres_close_withdraw_and_replay(engine) -> None:
    place = PlaceRef("step13-place")
    _seed(engine, place)
    codec = FakeMutationBasisCodec()
    generator = Candidates()
    factory = PostgresMutationUnitOfWorkFactory(DATABASE_URL or "")
    close = ClosePlace(factory, Gate(), codec, generator, FakeTransitionClock())
    close_command = ClosePlaceCommand(
        _key("close"),
        IntentFingerprint("close-v1"),
        place,
        _token(codec, place, "w0"),
        OpaqueEncodedPayload("mutation", b"operator"),
    )
    first = close.execute(close_command)
    assert first.value.outcome is PlaceMutationOutcome.APPLIED
    replay = close.execute(close_command)
    assert replay.value.outcome is PlaceMutationOutcome.REPLAY
    assert replay.value.replayed_outcome is PlaceMutationOutcome.APPLIED

    with engine.connect() as connection:
        head = (
            connection.execute(
                select(identity_place_head).where(identity_place_head.c.place_ref == place.token)
            )
            .mappings()
            .one()
        )
    withdraw = WithdrawPlace(factory, Gate(), codec, generator, FakeTransitionClock())
    withdrawal = withdraw.execute(
        WithdrawPlaceCommand(
            _key("withdraw"),
            IntentFingerprint("withdraw-v1"),
            place,
            _token(codec, place, head["state_witness"]),
            OpaqueEncodedPayload("mutation", b"operator"),
        )
    )
    assert withdrawal.value.outcome is PlaceMutationOutcome.APPLIED
    with engine.connect() as connection:
        facts = (
            connection.execute(
                select(identity_place_history.c.fact_type).where(
                    identity_place_history.c.place_ref == place.token
                )
            )
            .scalars()
            .all()
        )
        assert set(facts) == {CLOSE_FACT_TYPE, WITHDRAW_FACT_TYPE}
        assert len(connection.execute(select(mutation_audit)).mappings().all()) == 2
        assert len(connection.execute(select(mutation_committed_binding)).mappings().all()) == 2


def test_postgres_close_rolls_back_history_and_head_on_audit_conflict(engine) -> None:
    place = PlaceRef("step13-rollback-place")
    _seed(engine, place)
    codec = FakeMutationBasisCodec()
    command = ClosePlaceCommand(
        _key("rollback"),
        IntentFingerprint("close-v1"),
        place,
        _token(codec, place, "w0"),
        OpaqueEncodedPayload("mutation", b"operator"),
    )
    with engine.begin() as connection:
        connection.execute(
            mutation_audit.insert().values(
                client_identity=command.key.client_identity.value,
                request_identity=command.key.request_identity.value,
                intent_fingerprint="different-intent",
                operation_key="place.close",
                recorded_at=NOW,
                mutation_provenance_encoding="mutation",
                mutation_provenance_payload=b"prior",
                audit_details_encoding="details",
                audit_details_payload=b"prior",
            )
        )
    operation = ClosePlace(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL or ""),
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    )
    result = operation.execute(command)
    assert result.value.outcome is PlaceMutationOutcome.AUDIT_CONFLICT
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(identity_place_history).where(
                    identity_place_history.c.place_ref == place.token
                )
            )
            .mappings()
            .all()
            == []
        )
        head = (
            connection.execute(
                select(identity_place_head).where(identity_place_head.c.place_ref == place.token)
            )
            .mappings()
            .one()
        )
        assert head["latest_history_fact_ref"] is None
        assert head["state_witness"] == "w0"
