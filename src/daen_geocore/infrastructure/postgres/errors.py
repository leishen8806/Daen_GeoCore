from __future__ import annotations

from dataclasses import dataclass

from daen_geocore.ports.failures import PortFailure, TechnicalFailureClass
from daen_geocore.ports.persistence.commit import CommitNotCommitted, CommitOutcome, CommitUnknown


class IndeterminateCommitError(RuntimeError):
    """Marker for a commit-boundary failure whose final outcome is unknowable."""


@dataclass(frozen=True, slots=True)
class PostgresInfrastructureError(RuntimeError):
    failure: PortFailure

    def __str__(self) -> str:
        return self.failure.code


def _sqlstate(error: BaseException) -> str | None:
    original = getattr(error, "orig", error)
    return getattr(original, "sqlstate", None) or getattr(original, "pgcode", None)


def translate_begin_failure(error: BaseException) -> PortFailure:
    return PortFailure(
        code="postgres_begin_failed",
        classification=TechnicalFailureClass.TRANSIENT_UNAVAILABLE,
        detail=_sqlstate(error),
    )


def translate_commit_failure(error: BaseException) -> CommitOutcome:
    if isinstance(error, IndeterminateCommitError):
        return CommitUnknown(reason="indeterminate_commit_boundary")
    state = _sqlstate(error)
    if state in {"40001", "40P01"}:
        return CommitNotCommitted(
            failure=PortFailure(
                code="postgres_serialization_failure" if state == "40001" else "postgres_deadlock",
                classification=TechnicalFailureClass.RETRYABLE_TRANSACTION_ABORT,
                detail=state,
            )
        )
    return CommitNotCommitted(
        failure=PortFailure(
            code="postgres_commit_failed",
            classification=TechnicalFailureClass.NON_RETRYABLE_TECHNICAL_FAILURE,
            detail=state,
        )
    )
