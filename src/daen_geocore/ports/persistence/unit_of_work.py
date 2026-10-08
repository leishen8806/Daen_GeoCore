from typing import Protocol, Self

from daen_geocore.ports.persistence.commit import CommitPort


class UnitOfWork(Protocol):
    """Application transaction boundary; implementation owns storage details."""

    commit_port: CommitPort

    def __enter__(self) -> Self: ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
