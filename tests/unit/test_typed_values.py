from hypothesis import given
from hypothesis import strategies as st

from daen_geocore.domain.typed_values import TypedValue, TypeIdentifier


@given(
    st.text(min_size=1),
    st.one_of(st.text(), st.integers(), st.dictionaries(st.text(), st.integers())),
)
def test_unknown_typed_values_are_preserved(type_name: str, payload: object) -> None:
    value = TypedValue(TypeIdentifier(type_name), payload)
    assert value.type_id.value == type_name
    assert value.payload == payload


def test_typed_values_do_not_normalize() -> None:
    assert TypedValue(TypeIdentifier(" future/type "), "  raw ").payload == "  raw "
