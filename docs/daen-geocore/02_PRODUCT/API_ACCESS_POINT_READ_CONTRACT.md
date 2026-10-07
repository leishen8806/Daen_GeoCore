# DAEN Geo Core — Phase 05C Access Point Read Contract

An Access Point read can express AccessPointRef, served PlaceRefs, zero-or-more attributable location facts, an optional open attributable access descriptor, Provenance, explicit Quality and explicitly recorded history/context. No AP taxonomy, primary/default AP, ordering or pickup/drop-off meaning is defined.

The API boundary term is `Access Point attributable location fact`. It is not declared a public Source Assertion, SourceAssertionRef, Current DAEN Representation, Selected Coordinate or new Domain concept. Each fact belongs to AP context and carries Provenance and Quality; internal backing remains TBD. No new reference type is created.

An Access Point may expose zero, one or several location facts; several may conflict. There is no AP Current Representation, selected coordinate, ranking or primary coordinate. Missing AP location is honest absence/unknown. Place Selected Coordinate is never substituted.

Access Point ↔ Place is many-to-many capable and both directions are discoverable. No primary relation, order, inherited lifecycle standing or silent re-point after Place merge is promised. History is only what is explicitly recorded. AP movement, closure and replacement lifecycle remain unmodeled.
