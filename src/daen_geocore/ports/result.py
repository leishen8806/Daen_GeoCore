from dataclasses import dataclass
from typing import TypeVar

from daen_geocore.ports.failures import PortFailure

ValueT = TypeVar("ValueT")


@dataclass(frozen=True, slots=True)
class PortSuccess[ValueT]:
    value: ValueT


@dataclass(frozen=True, slots=True)
class PortError:
    failure: PortFailure


type PortResult[ValueT] = PortSuccess[ValueT] | PortError
