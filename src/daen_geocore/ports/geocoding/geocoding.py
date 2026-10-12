"""Provider-neutral geocoding contracts."""

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Protocol

from daen_geocore.ports.result import PortError, PortResult, PortSuccess

_MAX_ADDRESS_TEXT = 512
_MAX_CODE = 64
_MAX_PROVIDER_REFERENCE = 256
_MAX_DISPLAY_TEXT = 512


def _bounded_text(value: str, *, name: str, maximum: int) -> str:
    if type(value) is not str or not value or len(value) > maximum:
        raise ValueError(f"{name} must be a non-empty string of at most {maximum} characters")
    return value


def _optional_code(value: str | None, *, name: str, maximum: int = _MAX_CODE) -> str | None:
    if value is None:
        return None
    if type(value) is not str or not value or len(value) > maximum:
        raise ValueError(f"{name} must be a non-empty string of at most {maximum} characters")
    return value


@dataclass(frozen=True, slots=True)
class GeoLocation:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if type(self.latitude) is bool or not isfinite(self.latitude):
            raise ValueError("latitude must be finite")
        if type(self.longitude) is bool or not isfinite(self.longitude):
            raise ValueError("longitude must be finite")
        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")


@dataclass(frozen=True, slots=True)
class GeocodeQuery:
    address_text: str
    region_code: str | None = None
    language_code: str | None = None

    def __post_init__(self) -> None:
        _bounded_text(self.address_text, name="address_text", maximum=_MAX_ADDRESS_TEXT)
        _optional_code(self.region_code, name="region_code")
        _optional_code(self.language_code, name="language_code", maximum=35)


@dataclass(frozen=True, slots=True)
class ReverseGeocodeQuery:
    location: GeoLocation
    language_code: str | None = None

    def __post_init__(self) -> None:
        _optional_code(self.language_code, name="language_code", maximum=35)


@dataclass(frozen=True, slots=True)
class ExternalProviderReference:
    value: str

    def __post_init__(self) -> None:
        _bounded_text(self.value, name="value", maximum=_MAX_PROVIDER_REFERENCE)


@dataclass(frozen=True, slots=True)
class DisplayRequirements:
    attribution_required: bool
    attribution_text: str | None = None

    def __post_init__(self) -> None:
        if type(self.attribution_required) is not bool:
            raise TypeError("attribution_required must be a bool")
        if self.attribution_text is not None:
            _bounded_text(
                self.attribution_text,
                name="attribution_text",
                maximum=_MAX_DISPLAY_TEXT,
            )


@dataclass(frozen=True, slots=True)
class ProviderResult:
    provider_reference: ExternalProviderReference | None = None
    formatted_address: str | None = None
    name: str | None = None
    location: GeoLocation | None = None
    precision_class: str | None = None
    partial_match: bool | None = None
    display_requirements: DisplayRequirements | None = None

    def __post_init__(self) -> None:
        if self.formatted_address is not None:
            _bounded_text(
                self.formatted_address,
                name="formatted_address",
                maximum=_MAX_DISPLAY_TEXT,
            )
        if self.name is not None:
            _bounded_text(self.name, name="name", maximum=256)
        if self.precision_class is not None:
            _bounded_text(self.precision_class, name="precision_class", maximum=_MAX_CODE)
        if self.partial_match is not None and type(self.partial_match) is not bool:
            raise TypeError("partial_match must be a bool or None")


@dataclass(frozen=True, slots=True)
class ProviderLookup:
    provider_id: str
    results: tuple[ProviderResult, ...]

    def __post_init__(self) -> None:
        _bounded_text(self.provider_id, name="provider_id", maximum=_MAX_CODE)
        if type(self.results) is not tuple:
            raise TypeError("results must be a tuple")
        if not all(type(result) is ProviderResult for result in self.results):
            raise TypeError("results must contain only ProviderResult values")


class GeocodingProviderFailureKind(StrEnum):
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    CAPACITY_UNAVAILABLE = "capacity_unavailable"
    CONFIGURATION_FAILURE = "configuration_failure"
    INVALID_RESPONSE = "invalid_response"


@dataclass(frozen=True, slots=True)
class GeocodingProviderFailure:
    kind: GeocodingProviderFailureKind
    retry_after_seconds: int | None = None

    def __post_init__(self) -> None:
        if type(self.kind) is not GeocodingProviderFailureKind:
            raise TypeError("kind must be a GeocodingProviderFailureKind")
        if self.retry_after_seconds is not None and (
            type(self.retry_after_seconds) is bool or self.retry_after_seconds <= 0
        ):
            raise ValueError("retry_after_seconds must be a positive integer")


ProviderOutcome = ProviderLookup | GeocodingProviderFailure


class GeocodingProvider(Protocol):
    def geocode(self, query: GeocodeQuery) -> PortResult[ProviderOutcome]: ...

    def reverse_geocode(self, query: ReverseGeocodeQuery) -> PortResult[ProviderOutcome]: ...


__all__ = [
    "DisplayRequirements",
    "ExternalProviderReference",
    "GeocodeQuery",
    "GeocodingProvider",
    "GeocodingProviderFailure",
    "GeocodingProviderFailureKind",
    "GeoLocation",
    "ProviderLookup",
    "ProviderResult",
    "ReverseGeocodeQuery",
    "ProviderOutcome",
    "PortError",
    "PortResult",
    "PortSuccess",
]
