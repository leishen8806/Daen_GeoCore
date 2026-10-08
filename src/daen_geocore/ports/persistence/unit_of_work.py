from typing import Protocol

from daen_geocore.ports.persistence.commit import CommitOutcome


class UnitOfWork(Protocol):
    """Explicit application transaction lifecycle."""

    def begin(self) -> None: ...

    def commit(self) -> CommitOutcome: ...

    def rollback(self) -> None: ...
