from dataclasses import FrozenInstanceError
from math import inf, nan

import pytest

from daen_geocore.ports import PortError, PortFailure, PortSuccess
from daen_geocore.ports.geocoding import (
    DisplayRequirements,
    ExternalProviderReference,
    GeocodeQuery,
    GeocodingProviderFailure,
    GeocodingProviderFailureKind,
    GeoLocation,
    ProviderLookup,
    ProviderResult,
    ReverseGeocodeQuery,
)


def test_location_boundaries_and_finite_values() -> None:
    assert GeoLocation(-90, -180) == GeoLocation(-90, -180)
    assert GeoLocation(90, 180) == GeoLocation(90, 180)
    for value in (nan, inf, -inf):
        with pytest.raises(ValueError):
            GeoLocation(value, 0)
        with pytest.raises(ValueError):
            GeoLocation(0, value)
    with pytest.raises(ValueError):
        GeoLocation(90.1, 0)
    with pytest.raises(ValueError):
        GeoLocation(0, -180.1)


def test_queries_exclude_consumer_and_request_metadata() -> None:
    forward = GeocodeQuery("Example Street 1, Test District", "KH", "km")
    reverse = ReverseGeocodeQuery(GeoLocation(11, 104), "km")
    assert forward.address_text.startswith("Example")
    assert reverse.location == GeoLocation(11, 104)
    assert not hasattr(forward, "consumer_purpose_code")
    assert not hasattr(reverse, "request_id")


def test_provider_values_are_immutable_and_provider_neutral() -> None:
    result = ProviderResult(
        provider_reference=ExternalProviderReference("provider-ref-1"),
        formatted_address="Example Street 1, Test District",
        name="Example Place",
        location=GeoLocation(11, 104),
        precision_class="rooftop",
        partial_match=False,
        display_requirements=DisplayRequirements(True, "Example attribution"),
    )
    with pytest.raises(FrozenInstanceError):
        result.name = "changed"  # type: ignore[misc]
    assert result.provider_reference is not None
    assert result.display_requirements is not None


def test_empty_lookup_is_success() -> None:
    outcome = PortSuccess(ProviderLookup("provider-x", ()))
    assert isinstance(outcome.value, ProviderLookup)
    assert outcome.value.results == ()


def test_failure_kind_set_and_retry_validation() -> None:
    assert {kind.value for kind in GeocodingProviderFailureKind} == {
        "timeout",
        "unavailable",
        "capacity_unavailable",
        "configuration_failure",
        "invalid_response",
    }
    failure = GeocodingProviderFailure(GeocodingProviderFailureKind.TIMEOUT, 5)
    assert failure.retry_after_seconds == 5
    for retry_after in (0, -1, True):
        with pytest.raises(ValueError):
            GeocodingProviderFailure(GeocodingProviderFailureKind.TIMEOUT, retry_after)


def test_fake_provider_forward_reverse_and_failure_are_distinct() -> None:
    class FakeProvider:
        def geocode(self, query: GeocodeQuery):
            assert query.address_text == "Example Street 1, Test District"
            return PortSuccess(ProviderLookup("fake", ()))

        def reverse_geocode(self, query: ReverseGeocodeQuery):
            assert query.location == GeoLocation(11, 104)
            return PortSuccess(GeocodingProviderFailure(GeocodingProviderFailureKind.UNAVAILABLE))

    provider = FakeProvider()
    assert isinstance(
        provider.geocode(GeocodeQuery("Example Street 1, Test District")), PortSuccess
    )
    reverse = provider.reverse_geocode(ReverseGeocodeQuery(GeoLocation(11, 104)))
    assert isinstance(reverse, PortSuccess)
    assert isinstance(reverse.value, GeocodingProviderFailure)
    technical = PortError(PortFailure("adapter_failure"))
    assert isinstance(technical, PortError)
    assert not isinstance(technical, PortSuccess)
