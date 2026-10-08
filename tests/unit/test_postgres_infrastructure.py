from types import SimpleNamespace

from daen_geocore.infrastructure.postgres.errors import (
    IndeterminateCommitError,
    translate_begin_failure,
    translate_commit_failure,
)
from daen_geocore.ports.failures import TechnicalFailureClass
from daen_geocore.ports.persistence.commit import CommitNotCommitted, CommitUnknown


def test_commit_error_translator_maps_retryable_sqlstates() -> None:
    for state in ("40001", "40P01"):
        outcome = translate_commit_failure(SimpleNamespace(orig=SimpleNamespace(sqlstate=state)))
        assert isinstance(outcome, CommitNotCommitted)
        assert outcome.failure is not None
        assert outcome.failure.classification is TechnicalFailureClass.RETRYABLE_TRANSACTION_ABORT


def test_commit_error_translator_keeps_indeterminate_commit_unknown() -> None:
    outcome = translate_commit_failure(IndeterminateCommitError())
    assert isinstance(outcome, CommitUnknown)


def test_begin_failure_is_transient_and_not_commit_unknown() -> None:
    failure = translate_begin_failure(RuntimeError("connection unavailable"))
    assert failure.classification is TechnicalFailureClass.TRANSIENT_UNAVAILABLE


def test_generic_commit_failure_is_commit_unknown() -> None:
    outcome = translate_commit_failure(RuntimeError("constraint"))
    assert isinstance(outcome, CommitUnknown)
