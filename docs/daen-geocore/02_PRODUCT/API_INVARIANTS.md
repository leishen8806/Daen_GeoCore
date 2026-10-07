# DAEN Geo Core — Consolidated API Invariants

## I1–I13 Identifier and resolution

I1 Only Place uses GeoID. I2 GeoID is never silently substituted. I3 Historical GeoIDs remain resolvable. I4 GeoID is never reassigned or reused. I5 Opaque API references do not create Domain GeoID identity. I6 DAEN references are type-scoped. I7 Stable references never silently alias. I8 Exact GeoID resolution is not search/matching. I9 Multiple successors are not identity ambiguity. I10 Provider references are not DAEN references. I11 Every exact Place read exposes identity/resolution context. I12 Recognized identity is not reported not-found merely due to historical/non-current/restricted context. I13 Retained relationship/history records preserve originally recorded references; later reassociation is explicit and non-destructive.

## R1–R15 Read contracts

R1 SourceAssertionRef denotes the original assertion. R2 Original asserted content is not destructively edited. R3 Current Representation is not absolute truth. R4 Selected facts trace to supporting assertions and a material Selection Record. R5 Retained competing evidence remains discoverable. R6 Selected Coordinate is never an Access Point. R7 AP never falls back to Place Selected Coordinate. R8 AP↔Place is many-to-many capable. R9 Extent gains no independent Place identity or GeoID. R10 Extent overlap alone implies no relation. R11 Missing data is absence/unknown, never fabricated defaults. R12 Reads preserve material history. R13 Material Selection Record is immutable. R14 Unknown scope is not wildcard/equivalence. R15 Cross-subject assertion relations are historical/traceability context only.

## M1–M18 Mutation

M1 history non-destructive. M2 no reassignment/reuse/aliasing. M3 correction creates a new assertion. M4 same-subject supersession preserves subject and fact/purpose. M5 replacement creates a new SelectionRecordRef. M6 replacement requires same Place/fact-purpose/explicit scope. M7 merge does not rewrite retired GeoID references. M8 true-division children do not inherit parent GeoID. M9 T1 preserves resolution and not-valid-for-new-use. M10 T2 does not automatically alter Place or Current Representation. M11 every material mutation is attributable. M12 newer conflicts are not silently overwritten. M13 idempotent retry has no duplicate effects. M14 logical multi-record mutation is coherent. M15 no ordinary destructive history deletion. M16 exact references only. M17 supersession is explicit. M18 deferred operations are never approximated by another mutation.

## E1–E12 Endpoint and transport boundary

E1 Endpoint mapping does not expand scope. E2 Historical reads never redirect/substitute. E3 Immutable records have no PUT/PATCH mutation. E4 Destructive history DELETE is absent. E5 Deferred operations have no public endpoint. E6 Every material mutation requires MutationRequestRef. E7 Stale-protected mutations carry valid MutationBasisToken. E8 Exact-reference API never matches/searches. E9 One semantic operation has one canonical endpoint. E10 Provider refs never occupy DAEN-ref parameters. E11 404 meanings remain distinguishable in eventual error body. E12 URL action mapping imposes no semantic structure on opaque refs.

Phase 05 overall remains `NOT YET FINAL-GATE DECIDED`.
