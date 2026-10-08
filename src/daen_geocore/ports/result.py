from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True, slots=True)
class PortFailure:
    """Transport-neutral failure detail for a port operation."""

    code: str
    detail: str | None = None


ValueT = TypeVar("ValueT")


@dataclass(frozen=True, slots=True)
class PortSuccess[ValueT]:
    value: ValueT


@dataclass(frozen=True, slots=True)
class PortError:
    failure: PortFailure


type PortResult[ValueT] = PortSuccess[ValueT] | PortError
