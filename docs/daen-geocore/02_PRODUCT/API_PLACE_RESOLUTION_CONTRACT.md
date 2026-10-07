# DAEN Geo Core — Phase 05B Place Resolution Contract

## Exact Place read

One conceptual exact-identity contract combines an identity/resolution facet with an optional Place content facet. Every exact Place read exposes the identity facet; a resolution-only projection is allowed. Endpoint form and JSON fields are deferred.

## Resolution envelope capability

The contract can express the requested PlaceRef, recognized versus unknown identity, new-use standing knowledge, identity relationships, history pointers, detail availability and the requested Place's own content. No lifecycle enum or field names are frozen.

## New-use standing

The capability distinguishes: explicitly usable for new use; explicitly not usable for new use; and not asserted/unknown. These are not lifecycle states. T1 withdrawal must communicate not-valid-for-new-use. Merge, closure and split do not imply ACTIVE/CLOSED/MERGED/WITHDRAWN status values.

## No silent substitution

Resolving historical Place A preserves A as the requested identity. For merge A→B, A's identity/resolution context is returned and B is exposed as a related survivor; B is never returned as if it were A.

Exact GeoID resolution is not search: names, addresses, coordinates, reverse geocoding, provider IDs, fuzzy matching and duplicate detection are excluded. Exact resolution does not return identity-match ambiguity.

## Split, closure and withdrawal

- Mis-conflation: A may continue; B is a new Place; A is not automatically retired; assertion reassociation remains TBD.
- True division: A remains historically resolvable; B/C use new GeoIDs; children do not inherit A; multiple successors are not ambiguity and have no ranking or primary successor.
- Closure: GeoID remains resolvable; no successor, Succession or validation self-link is required; demolition-to-closure remains TBD.
- T1 withdrawal: Place is the target; same GeoID remains resolvable, is not valid for new use and is never reused/reassigned; no successor is required.
- T2 withdrawal: Source Assertion keeps SourceAssertionRef and remains retained/traceable; the Place identity does not automatically change. Its effect on Current DAEN Representation is deferred.

Stored Resolution Link direction/vocabulary, caller-relative resolution views and Succession remain distinct. Succession exists only when a later identity/representation exists.

## Outcome boundary

Supported outcomes include recognized identity; recognized identity with historical/non-new-use context; unknown identity; and recognized identity with restricted/unavailable details. Historical, closed, withdrawn or retired identities must not become `not found` merely because they are not current. Unknown exact GeoID is the conceptual not-found case. Restricted-detail mechanics remain deferred. Multiple successors are not ambiguity.

Provider references are external values only and are never accepted as DAEN references or GeoID.

## Human-frozen API invariants

I1 Only Place uses GeoID.
I2 GeoID is never silently substituted.
I3 Historical GeoIDs remain resolvable.
I4 GeoID is never reassigned or reused.
I5 Opaque API references do not create Domain GeoID identity.
I6 DAEN references are type-scoped.
I7 Stable references never silently alias.
I8 Exact GeoID resolution is not search/matching.
I9 Multiple successors are not identity ambiguity.
I10 Provider references are not DAEN references.
I11 Every exact Place read exposes identity/resolution context.
I12 Recognized identity is not reported not-found merely due to historical/non-current/restricted context.
I13 Retained relationship/history records preserve originally recorded references; later reassociation must be explicit and non-destructive.

## Coherence cases

All 15 Phase 05B coherence cases are supported subject to this Human Freeze: typed identity; opaque references; no aliasing; exact read identity facet; historical resolution; merge; split; closure; T1; T2; multiple successors; provider-reference separation; relationship preservation; unknown versus historical identity; and restricted-detail distinction.

## Protected TBDs

GeoID encoding; serialized reference forms; canonical textual normalization; Resolution Link stored direction/type vocabulary; lifecycle taxonomy; demolition-to-closure; withdrawal authority/removal workflow; Access Point lifecycle; cross-subject assertion reassociation; selection authority; provider mapping; error codes/object; HTTP; database; cache; and version mechanics remain TBD.
