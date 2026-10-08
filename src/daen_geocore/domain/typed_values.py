from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True, slots=True)
class TypeIdentifier:
    """Open, opaque identifier for a typed value vocabulary."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("type identifier must be a string")


PayloadT = TypeVar("PayloadT")


@dataclass(frozen=True, slots=True)
class TypedValue[PayloadT]:
    """Open typed value carrier; type and payload are preserved unchanged."""

    type_id: TypeIdentifier
    payload: PayloadT
