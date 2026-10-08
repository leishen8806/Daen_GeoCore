from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True, slots=True)
class PortFailure:
    """Transport-neutral failure detail for a port operation."""

    code: str
    detail: str | None = None


ValueT = TypeVar("ValueT")


@dataclass(frozen=True, slots=True)
class PortResult[ValueT]:
    """Typed success/failure result without HTTP or provider semantics."""

    value: ValueT | None = None
    failure: PortFailure | None = None

    @property
    def succeeded(self) -> bool:
        return self.failure is None
