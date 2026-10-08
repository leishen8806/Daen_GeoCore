from typing import Protocol, Self

from daen_geocore.ports.persistence.commit import CommitOutcome


class UnitOfWork(Protocol):
    """Explicit NEW → ACTIVE → COMMITTED/ROLLED_BACK → CLOSED lifecycle."""

    def __enter__(self) -> Self: ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...

    def begin(self) -> None: ...

    def commit(self) -> CommitOutcome: ...

    def rollback(self) -> None: ...
