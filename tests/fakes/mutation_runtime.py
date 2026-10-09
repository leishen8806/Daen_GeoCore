from dataclasses import dataclass, field

from daen_geocore.ports.failures import TechnicalFailureClass
from daen_geocore.ports.idempotency.store import (
    CommittedBindingAbsent,
    CommittedBindingFound,
    CommittedIdempotencyStore,
    CommittedMutationBinding,
    IdempotencyBindingKey,
    IdempotencyCreateDisposition,
)
from daen_geocore.ports.mutation.basis import (
    InvalidMutationBasisToken,
    MutationBasisClaims,
    MutationBasisCodec,
    MutationBasisToken,
)
from daen_geocore.ports.result import PortError, PortFailure, PortResult, PortSuccess


class FakeMutationBasisCodec(MutationBasisCodec):
    def __init__(self) -> None:
        self._claims: dict[str, MutationBasisClaims] = {}

    def issue(self, claims: MutationBasisClaims) -> PortResult[MutationBasisToken]:
        token = MutationBasisToken(f"fake-{len(self._claims) + 1}")
        self._claims[token.value] = claims
        return PortSuccess(token)

    def verify(
        self, token: MutationBasisToken
    ) -> PortResult[MutationBasisClaims | InvalidMutationBasisToken]:
        claims = self._claims.get(
            token.value if isinstance(token.value, str) else token.value.decode()
        )
        return PortSuccess(claims if claims is not None else InvalidMutationBasisToken())


@dataclass
class InMemoryCommittedIdempotencyStore(CommittedIdempotencyStore):
    available: bool = True
    bindings: dict[IdempotencyBindingKey, CommittedMutationBinding] = field(default_factory=dict)

    def _unavailable(self) -> PortError:
        return PortError(
            PortFailure("idempotency_unavailable", TechnicalFailureClass.TRANSIENT_UNAVAILABLE)
        )

    def read(self, key: IdempotencyBindingKey):
        if not self.available:
            return self._unavailable()
        binding = self.bindings.get(key)
        return PortSuccess(
            CommittedBindingAbsent() if binding is None else CommittedBindingFound(binding)
        )

    def create_if_absent(self, binding: CommittedMutationBinding):
        if not self.available:
            return self._unavailable()
        existing = self.bindings.get(binding.key)
        if existing is None:
            self.bindings[binding.key] = binding
            return PortSuccess(IdempotencyCreateDisposition.CREATED)
        return PortSuccess(
            IdempotencyCreateDisposition.ALREADY_PRESENT_SAME
            if existing == binding
            else IdempotencyCreateDisposition.CONFLICTING_EXISTING
        )
