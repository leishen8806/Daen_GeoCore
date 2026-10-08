from dataclasses import dataclass
from typing import Literal, Protocol

from daen_geocore.ports.failures import PortFailure


@dataclass(frozen=True, slots=True)
class CommitAccepted:
    status: Literal["committed"] = "committed"


@dataclass(frozen=True, slots=True)
class CommitNotCommitted:
    failure: PortFailure | None = None
    status: Literal["definitely_not_committed"] = "definitely_not_committed"


@dataclass(frozen=True, slots=True)
class CommitUnknown:
    status: Literal["outcome_unknown"] = "outcome_unknown"
    reason: str | None = None


type CommitOutcome = CommitAccepted | CommitNotCommitted | CommitUnknown


class CommitPort(Protocol):
    """Explicit logical commit boundary without storage API leakage."""

    def commit(self) -> CommitOutcome: ...

    def rollback(self) -> None: ...
