from daen_geocore.domain.provenance import Provenance
from daen_geocore.domain.quality import Quality
from daen_geocore.domain.typed_values import TypedValue, TypeIdentifier


def test_provenance_is_independent_from_quality() -> None:
    provenance = Provenance(source_context="public-source")
    quality = Quality((TypedValue(TypeIdentifier("future.dimension"), "unknown"),))
    assert provenance.source_context == "public-source"
    assert quality.dimensions[0].payload == "unknown"
    assert not isinstance(provenance, Quality)


def test_provenance_is_immutable_and_has_no_mutation_fields() -> None:
    provenance = Provenance(source_context="operator")
    assert provenance == Provenance(source_context="operator")
    assert not hasattr(provenance, "recorded_by")
    assert not hasattr(provenance, "affected_references")
    assert not hasattr(provenance, "resulting_references")


def test_quality_unknown_and_open_dimensions() -> None:
    assert Quality.unknown() == Quality()
    future = Quality((TypedValue(TypeIdentifier("future.dimension"), {"raw": True}),))
    assert future.dimensions[0].payload == {"raw": True}
    assert not hasattr(future, "score")
