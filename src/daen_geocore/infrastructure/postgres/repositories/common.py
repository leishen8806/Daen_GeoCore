from typing import Any

from daen_geocore.ports.failures import PortFailure, TechnicalFailureClass
from daen_geocore.ports.persistence.records import (
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityKnown,
    PersistedQualityUnknown,
    PersistedScope,
    PersistedUnknownScope,
)
from daen_geocore.ports.result import PortError


def technical_error(error: BaseException) -> PortError:
    classification = (
        TechnicalFailureClass.TRANSIENT_UNAVAILABLE
        if isinstance(error, (ConnectionError, TimeoutError))
        else TechnicalFailureClass.NON_RETRYABLE_TECHNICAL_FAILURE
    )
    return PortError(
        PortFailure("postgres_repository_failure", classification, type(error).__name__)
    )


def scope_from_row(row: Any) -> PersistedScope:
    if not row["scope_is_explicit"]:
        return PersistedUnknownScope()
    return PersistedExplicitScope(
        row["scope_type_id"],
        OpaqueEncodedPayload(row["scope_encoding"], bytes(row["scope_payload"])),
        None if row["scope_equality_key"] is None else bytes(row["scope_equality_key"]),
    )


def quality_from_row(row: Any) -> PersistedQualityKnown | PersistedQualityUnknown:
    if not row["quality_is_known"]:
        return PersistedQualityUnknown()
    return PersistedQualityKnown(
        OpaqueEncodedPayload(row["quality_encoding"], bytes(row["quality_payload"]))
    )


def metadata_from_row(row: Any) -> OpaqueEncodedPayload | None:
    if row["history_metadata_encoding"] is None:
        return None
    return OpaqueEncodedPayload(
        row["history_metadata_encoding"], bytes(row["history_metadata_payload"])
    )
