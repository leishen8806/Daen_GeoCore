from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True, slots=True)
class CommitAccepted:
    status: Literal["committed"] = "committed"


@dataclass(frozen=True, slots=True)
class CommitRejected:
    status: Literal["rejected"] = "rejected"
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class CommitUnknown:
    status: Literal["unknown"] = "unknown"
    reason: str | None = None


type CommitOutcome = CommitAccepted | CommitRejected | CommitUnknown


class CommitPort(Protocol):
    """Explicit logical commit boundary without storage API leakage."""

    def commit(self) -> CommitOutcome: ...

    def rollback(self) -> None: ...
