from pathlib import Path

SOURCE = Path("src/daen_geocore/application/place_identity_mutations.py").read_text()


def test_step13_has_only_two_operation_keys_and_no_transport_or_evidence_store() -> None:
    assert 'TechnicalOperationKey("place.close")' in SOURCE
    assert 'TechnicalOperationKey("place.withdraw")' in SOURCE
    assert "EvidenceStore" not in SOURCE
    assert "RequestReferenceRecoveryMapping" not in SOURCE
    assert "ReferenceReservationCoordinator" not in SOURCE
    assert "PlaceStatus" not in SOURCE
    assert "PlaceLifecycleState" not in SOURCE
    assert "/v1/" not in SOURCE


def test_step13_does_not_add_a_migration() -> None:
    revisions = sorted(Path("alembic/versions").glob("*.py"))
    assert [path.name for path in revisions] == [
        "0001_authoritative_persistence.py",
        "0002_correctness_persistence.py",
    ]
