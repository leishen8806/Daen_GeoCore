from dataclasses import dataclass
from typing import Protocol

from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
from daen_geocore.ports.persistence.records import (
    RecordAbsent,
    SelectionSlotHead,
    SelectionSlotKey,
    StateWitness,
)
from daen_geocore.ports.persistence.repositories import (
    AssertionsRepository,
    IdentityRepository,
    RepresentationRepository,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess


@dataclass(frozen=True, slots=True)
class PlaceOwner:
    place_ref: PlaceRef


@dataclass(frozen=True, slots=True)
class AssertionOwner:
    source_assertion_ref: SourceAssertionRef


@dataclass(frozen=True, slots=True)
class SelectionSlotOwner:
    slot: SelectionSlotKey


type MutationOwner = PlaceOwner | AssertionOwner | SelectionSlotOwner


@dataclass(frozen=True, slots=True)
class OwnerPresent:
    witness: StateWitness


@dataclass(frozen=True, slots=True)
class OwnerAbsent:
    pass


type OwnerState = OwnerPresent | OwnerAbsent


@dataclass(frozen=True, slots=True)
class ObservedOwnerState:
    owner: MutationOwner
    state: OwnerState


class RepositoryAwareUnitOfWork(Protocol):
    identity: IdentityRepository
    assertions: AssertionsRepository
    representation: RepresentationRepository


class OwnerStateReader:
    def read(self, owner: MutationOwner, uow: RepositoryAwareUnitOfWork) -> PortResult[OwnerState]:
        if isinstance(owner, PlaceOwner):
            result = uow.identity.get_place_head(owner.place_ref)
        elif isinstance(owner, AssertionOwner):
            result = uow.assertions.get_standing_head(owner.source_assertion_ref)
        else:
            result = uow.representation.get_selection_slot_head(owner.slot)
        if isinstance(result, PortError):
            return result
        if isinstance(result.value, RecordAbsent):
            return PortSuccess(OwnerAbsent())
        return PortSuccess(OwnerPresent(result.value.record.state_witness))


def owner_state_from_slot_head(head: SelectionSlotHead | None) -> OwnerState:
    return OwnerAbsent() if head is None else OwnerPresent(head.state_witness)
