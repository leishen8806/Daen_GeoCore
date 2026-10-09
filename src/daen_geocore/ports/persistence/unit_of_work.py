from typing import Protocol, Self

from daen_geocore.ports.persistence.commit import CommitOutcome
from daen_geocore.ports.persistence.repositories import (
    AssertionsRepository,
    IdentityRepository,
    RepresentationRepository,
)


class UnitOfWork(Protocol):
    """Explicit NEW → ACTIVE → COMMITTED/ROLLED_BACK → CLOSED lifecycle."""

    def __enter__(self) -> Self: ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...

    def begin(self) -> None: ...

    def commit(self) -> CommitOutcome: ...

    def rollback(self) -> None: ...

    @property
    def identity(self) -> IdentityRepository: ...

    @property
    def assertions(self) -> AssertionsRepository: ...

    @property
    def representation(self) -> RepresentationRepository: ...
