import os
import threading
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
from tests.integration.postgres.test_step11_source_assertion_withdrawal import _BarrierGate
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
    candidates = Candidates()
    candidates.calls = 10_000
    operation = ClosePlace(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL or ""),
        Gate(),
        codec,
        candidates,
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


def _run_race(engine, place: PlaceRef, first_kind: str, second_kind: str):
    _seed(engine, place)
    codec = FakeMutationBasisCodec()
    token = _token(codec, place, "w0")
    barrier = threading.Barrier(2)
    results = []

    def worker(kind: str, suffix: str) -> None:
        operation_type = ClosePlace if kind == "close" else WithdrawPlace
        command_type = ClosePlaceCommand if kind == "close" else WithdrawPlaceCommand
        candidates = Candidates()
        candidates.calls = 10_000 if suffix == "a" else 20_000
        operation = operation_type(
            PostgresMutationUnitOfWorkFactory(DATABASE_URL or ""),
            _BarrierGate(barrier),
            codec,
            candidates,
            FakeTransitionClock(),
        )
        results.append(
            operation.execute(
                command_type(
                    _key(f"{kind}-{suffix}"),
                    IntentFingerprint(f"{kind}-v1"),
                    place,
                    token,
                    OpaqueEncodedPayload("mutation", suffix.encode()),
                )
            )
        )

    threads = [
        threading.Thread(target=worker, args=(first_kind, "a")),
        threading.Thread(target=worker, args=(second_kind, "b")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    assert all(not thread.is_alive() for thread in threads)
    return results


def test_postgres_close_close_and_withdraw_withdraw_races_have_one_winner(engine) -> None:
    for index, kind in enumerate(("close", "withdraw")):
        results = _run_race(engine, PlaceRef(f"step13-{kind}-race-{index}"), kind, kind)
        assert (
            sum(
                getattr(getattr(result, "value", None), "outcome", None)
                is PlaceMutationOutcome.APPLIED
                for result in results
            )
            <= 1
        )


def test_postgres_close_withdraw_race_serializes_one_transition(engine) -> None:
    place = PlaceRef("step13-close-withdraw-race")
    results = _run_race(engine, place, "close", "withdraw")
    assert (
        sum(
            getattr(getattr(result, "value", None), "outcome", None) is PlaceMutationOutcome.APPLIED
            for result in results
        )
        <= 1
    )
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
        assert len(facts) == 1, [repr(result) for result in results]
