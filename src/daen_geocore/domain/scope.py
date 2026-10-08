from dataclasses import dataclass
from typing import Any, Protocol

from .typed_values import TypeIdentifier


@dataclass(frozen=True, slots=True)
class ExactEqualityKey:
    """Opaque in-memory key supplied by a recognized scope type."""

    value: Any


class ExactEqualityProvider(Protocol):
    def equality_key(self, value: Any) -> ExactEqualityKey: ...


@dataclass(frozen=True, slots=True)
class ExplicitScope:
    type_id: TypeIdentifier
    value: Any
    equality_provider: ExactEqualityProvider | None = None


@dataclass(frozen=True, slots=True)
class UnknownScope:
    """Unknown scope is absence of an established explicit scope."""

    pass


def exact_scope_equal(
    left: ExplicitScope | UnknownScope, right: ExplicitScope | UnknownScope
) -> bool | None:
    """Return True/False when exact equality is established, else None."""
    if isinstance(left, UnknownScope) or isinstance(right, UnknownScope):
        return None
    if left.type_id != right.type_id:
        return False
    if left.equality_provider is None or right.equality_provider is None:
        return None
    left_key = left.equality_provider.equality_key(left.value)
    right_key = right.equality_provider.equality_key(right.value)
    return left_key == right_key
