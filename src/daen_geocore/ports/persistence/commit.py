from typing import Protocol

from daen_geocore.ports.result import PortResult


class CommitPort(Protocol):
    """Logical commit boundary without a storage or transaction API leak."""

    def commit(self) -> PortResult[None]: ...

    def rollback(self) -> None: ...
