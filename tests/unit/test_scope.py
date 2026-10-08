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


@dataclass(frozen=True)
class Resolver:
    provider: Provider | None = Provider()

    def provider_for(self, type_id: TypeIdentifier) -> Provider | None:
        return self.provider if type_id == TypeIdentifier("future.scope") else None


def scope(value: str, type_name: str = "future.scope") -> ExplicitScope:
    return ExplicitScope(TypeIdentifier(type_name), value)


def test_unknown_scope_never_proves_equality() -> None:
    assert UnknownScope() != UnknownScope()
    assert exact_scope_equal(UnknownScope(), scope("x"), Resolver()) is None
    assert exact_scope_equal(UnknownScope(), UnknownScope(), Resolver()) is None


def test_explicit_scope_uses_one_external_type_provider() -> None:
    resolver = Resolver()
    assert scope("x") != scope("x")
    assert exact_scope_equal(scope("x"), scope("x"), resolver) is True
    assert exact_scope_equal(scope("x"), scope("y"), resolver) is False
    assert exact_scope_equal(scope("x", "a"), scope("x", "b"), resolver) is False


def test_missing_equality_mechanism_does_not_fallback() -> None:
    left = ExplicitScope(TypeIdentifier("future.scope"), "same")
    right = ExplicitScope(TypeIdentifier("future.scope"), "same")
    assert exact_scope_equal(left, right, Resolver(provider=None)) is None
    assert exact_scope_equal(left, right, None) is None
