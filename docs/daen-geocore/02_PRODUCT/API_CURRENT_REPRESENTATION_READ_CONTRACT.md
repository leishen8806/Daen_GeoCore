# DAEN Geo Core — Phase 05C Current DAEN Representation Read Contract

A Current DAEN Representation is a Place-associated selected view, never absolute truth. Each selected fact can express PlaceRef, fact/purpose, scope, selected value, one-or-more supporting SourceAssertionRefs, SelectionRecordRef, selection attribution, Provenance and explicit Quality.

SelectionRecordRef is a stable opaque history reference, not GeoID, not a top-level resource and not a new Domain identity. A material Selection Record is immutable; a new material selection creates a new reference. Standalone retrieval remains deferred.

Traceability is frozen, derivation is not. A selected value need not be byte-for-byte equal to an assertion value. Normalization, composition and derivation algorithms are not defined. Supporting assertions must remain identifiable.

Relevant retained potentially competing evidence remains discoverable. Unknown scope is not wildcard or proof of equivalence. Superseded and withdrawn evidence remains discoverable. No canonical competing-set, source-ranking or selection-authority algorithm is frozen.

Selected Coordinate is never an Access Point. Current Representation may expose Provenance and Quality, with `unknown` valid.


## Mutation basis capability

Reads relevant to Selection add and replace must be able to expose an opaque MutationBasisToken, including the observed empty-current-selection basis where applicable.
