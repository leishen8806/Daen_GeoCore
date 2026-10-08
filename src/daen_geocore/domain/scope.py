from dataclasses import dataclass
from typing import Any, Protocol

from .typed_values import TypeIdentifier


@dataclass(frozen=True, slots=True)
class ExactEqualityKey:
    """Opaque in-memory key supplied by a recognized scope type."""

    value: Any


class ExactEqualityProvider(Protocol):
    def equality_key(self, value: Any) -> ExactEqualityKey: ...


class ExactEqualityResolver(Protocol):
    def provider_for(self, type_id: TypeIdentifier) -> ExactEqualityProvider | None: ...


@dataclass(frozen=True, slots=True, eq=False)
class ExplicitScope:
    type_id: TypeIdentifier
    value: Any


@dataclass(frozen=True, slots=True, eq=False)
class UnknownScope:
    """Unknown scope is absence of an established explicit scope."""

    pass


def exact_scope_equal(
    left: ExplicitScope | UnknownScope,
    right: ExplicitScope | UnknownScope,
    resolver: ExactEqualityResolver | None = None,
) -> bool | None:
    """Return True/False when one resolver establishes exact equality, else None."""
    if isinstance(left, UnknownScope) or isinstance(right, UnknownScope):
        return None
    if left.type_id != right.type_id or resolver is None:
        return False if left.type_id != right.type_id else None
    provider = resolver.provider_for(left.type_id)
    if provider is None:
        return None
    return provider.equality_key(left.value) == provider.equality_key(right.value)
