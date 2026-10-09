from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from daen_geocore.ports.mutation.owners import (
    MutationOwner,
    ObservedOwnerState,
    OwnerStateReader,
    RepositoryAwareUnitOfWork,
)
from daen_geocore.ports.recovery.gate import RecoveryGate, RecoveryIncarnation
from daen_geocore.ports.result import PortResult, PortSuccess


@dataclass(frozen=True, slots=True)
class MutationBasisToken:
    value: str | bytes


@dataclass(frozen=True, slots=True)
class MutationBasisClaims:
    recovery_incarnation: RecoveryIncarnation
    observed_owners: tuple[ObservedOwnerState, ...]


@dataclass(frozen=True, slots=True)
class AuthoritativeReadSet:
    observed_owners: tuple[ObservedOwnerState, ...]


@dataclass(frozen=True, slots=True)
class InvalidMutationBasisToken:
    pass


class MutationBasisCodec(Protocol):
    def issue(self, claims: MutationBasisClaims) -> PortResult[MutationBasisToken]: ...

    def verify(
        self, token: MutationBasisToken
    ) -> PortResult[MutationBasisClaims | InvalidMutationBasisToken]: ...


class BasisValidation(StrEnum):
    VALID = "valid"
    RECOVERY_INCARNATION_MISMATCH = "recovery_incarnation_mismatch"
    OWNER_STATE_MISMATCH = "owner_state_mismatch"
    INVALID_TOKEN = "invalid_token"


class ReadSetValidation(StrEnum):
    VALID = "valid"
    OWNER_STATE_MISMATCH = "owner_state_mismatch"


class AuthoritativeReadSetCapture:
    def __init__(self, reader: OwnerStateReader) -> None:
        self._reader = reader

    def capture(
        self, owners: tuple[MutationOwner, ...], uow: RepositoryAwareUnitOfWork
    ) -> PortResult[AuthoritativeReadSet]:
        observed: list[ObservedOwnerState] = []
        for owner in owners:
            result = self._reader.read(owner, uow)
            if not isinstance(result, PortSuccess):
                return result
            observed.append(ObservedOwnerState(owner, result.value))
        return PortSuccess(AuthoritativeReadSet(tuple(observed)))


class MutationBasisValidator:
    def __init__(
        self, codec: MutationBasisCodec, gate: RecoveryGate, reader: OwnerStateReader
    ) -> None:
        self._codec = codec
        self._gate = gate
        self._reader = reader

    def validate(
        self, token: MutationBasisToken, uow: RepositoryAwareUnitOfWork
    ) -> PortResult[BasisValidation]:
        observation = self._gate.observation()
        if not observation.may_authoritative_serve:
            return PortSuccess(BasisValidation.RECOVERY_INCARNATION_MISMATCH)
        decoded = self._codec.verify(token)
        if not isinstance(decoded, PortSuccess):
            return decoded
        if isinstance(decoded.value, InvalidMutationBasisToken):
            return PortSuccess(BasisValidation.INVALID_TOKEN)
        if observation.incarnation != decoded.value.recovery_incarnation:
            return PortSuccess(BasisValidation.RECOVERY_INCARNATION_MISMATCH)
        for expected in decoded.value.observed_owners:
            current = self._reader.read(expected.owner, uow)
            if not isinstance(current, PortSuccess) or current.value != expected.state:
                return (
                    current
                    if not isinstance(current, PortSuccess)
                    else PortSuccess(BasisValidation.OWNER_STATE_MISMATCH)
                )
        return PortSuccess(BasisValidation.VALID)


class ReadSetRevalidator:
    def __init__(self, reader: OwnerStateReader) -> None:
        self._reader = reader

    def revalidate(
        self, read_set: AuthoritativeReadSet, uow: RepositoryAwareUnitOfWork
    ) -> PortResult[ReadSetValidation]:
        for expected in read_set.observed_owners:
            current = self._reader.read(expected.owner, uow)
            if not isinstance(current, PortSuccess):
                return current
            if current.value != expected.state:
                return PortSuccess(ReadSetValidation.OWNER_STATE_MISMATCH)
        return PortSuccess(ReadSetValidation.VALID)
