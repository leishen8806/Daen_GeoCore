# DAEN Geo Core — Phase 05C Source Assertion Read Contract

## Status

`PHASE 05C READ CONTRACTS = HUMAN FROZEN`

Public Source Assertion subject is `PlaceRef` only. Unresolved-location subjects remain Domain-supported but public exposure is deferred. Access Point is not frozen as a Source Assertion subject; no generic SubjectRef is created. Assertion subject is immutable and cross-subject reassociation remains TBD.

A read can express SourceAssertionRef, PlaceRef, open fact/purpose, typed asserted value, explicit-or-unknown scope, originating source Provenance, explicit Quality and retained history relations. Assertion-kind and value-type vocabularies remain open.

Original subject, fact/purpose, value, scope and originating source context are non-destructively immutable. Correction creates a new assertion. History may record supersession, T2 withdrawal, selection citations and other attributable events. Superseded is not withdrawn. No lifecycle enum is defined.

Same-subject supersession is guaranteed: old assertion remains readable and the new assertion is discoverable. Cross-subject relationships are historical/traceability context only; no effective migration or subject reassignment is promised.

Relevant retained evidence for the same Place/fact/purpose/scope has a retrieval/traversal path. Unknown-scope assertions are not automatically scope-equivalent or silently hidden. Superseded and withdrawn evidence remains discoverable through history. No ranking or conflict-resolution algorithm is frozen.

Provenance is originating source context; Quality is explicit and `unknown` is valid. No public Source resource, closed scope schema, or mutation contract is defined.
