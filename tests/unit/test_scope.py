from dataclasses import dataclass

from daen_geocore.domain.scope import (
    ExactEqualityKey,
    ExplicitScope,
    UnknownScope,
    exact_scope_equal,
)
from daen_geocore.domain.typed_values import TypeIdentifier


@dataclass(frozen=True)
class Provider:
    def equality_key(self, value: str) -> ExactEqualityKey:
        return ExactEqualityKey(value)


def scope(value: str, type_name: str = "future.scope") -> ExplicitScope:
    return ExplicitScope(TypeIdentifier(type_name), value, Provider())


def test_unknown_scope_never_proves_equality() -> None:
    assert exact_scope_equal(UnknownScope(), scope("x")) is None
    assert exact_scope_equal(UnknownScope(), UnknownScope()) is None


def test_explicit_scope_uses_type_specific_equality_only() -> None:
    assert exact_scope_equal(scope("x"), scope("x")) is True
    assert exact_scope_equal(scope("x"), scope("y")) is False
    assert exact_scope_equal(scope("x", "a"), scope("x", "b")) is False


def test_missing_equality_mechanism_does_not_fallback() -> None:
    left = ExplicitScope(TypeIdentifier("future.scope"), "same")
    right = ExplicitScope(TypeIdentifier("future.scope"), "same")
    assert exact_scope_equal(left, right) is None
