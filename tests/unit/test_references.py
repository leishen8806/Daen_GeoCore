from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given
from hypothesis import strategies as st

from daen_geocore.domain.references import (
    PlaceRef,
    SourceAssertionRef,
)


@given(st.text())
def test_opaque_reference_tokens_round_trip(token: str) -> None:
    assert PlaceRef(token).token == token


def test_reference_types_are_immutable_hashable_and_distinct() -> None:
    place = PlaceRef("same")
    assert place == PlaceRef("same")
    assert hash(place) == hash(PlaceRef("same"))
    assert place != SourceAssertionRef("same")
    with pytest.raises(FrozenInstanceError):
        place.token = "changed"  # type: ignore[misc]


def test_reference_tokens_are_not_interpreted() -> None:
    assert PlaceRef("not-a-uuid/prefix/timestamp").token == "not-a-uuid/prefix/timestamp"
    with pytest.raises(TypeError):
        PlaceRef(123)  # type: ignore[arg-type]
