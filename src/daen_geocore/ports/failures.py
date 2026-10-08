from dataclasses import dataclass
from enum import StrEnum


class TechnicalFailureClass(StrEnum):
    RETRYABLE_TRANSACTION_ABORT = "retryable_transaction_abort"
    TRANSIENT_UNAVAILABLE = "transient_unavailable"
    NON_RETRYABLE_TECHNICAL_FAILURE = "non_retryable_technical_failure"


@dataclass(frozen=True, slots=True)
class PortFailure:
    """Neutral technical failure; semantic conflicts are outside ports."""

    code: str
    classification: TechnicalFailureClass = TechnicalFailureClass.NON_RETRYABLE_TECHNICAL_FAILURE
    detail: str | None = None
