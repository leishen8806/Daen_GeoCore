# DAEN Geo Core — Phase 05A API Resource Model

## Top-level resources

Exactly three independently addressable resources are frozen for 05A:

1. **Place** — identified by GeoID.
2. **Source Assertion** — future opaque API reference; never GeoID.
3. **Access Point** — future opaque API reference; never GeoID.

Opaque API reference means addressability only; it does not create a new Domain GeoID namespace. Reference format is Phase 05B.

## Concept exposure

| Concept | 05A exposure | Identity/addressability |
|---|---|---|
| Place | top-level resource | GeoID |
| Source Assertion | top-level resource | opaque API reference; not GeoID |
| Access Point | top-level resource | opaque API reference; not GeoID |
| Current DAEN Representation | Place-associated selected view | no independent top-level resource |
| Selected Coordinate | fact/value inside Current Representation | no independent addressability |
| Extent | read-only spatial fact/value, embedded or related | no top-level public resource; independent reference deferred |
| Resolution Link | relationship/history contract | relationship/history record |
| Correction | attributable history/operation record | not top-level |
| Succession | distinct relationship/history concept when present | relationship/history record |
| Containment | directional Place-to-Place relation, read-only | relationship/history record |
| Provenance | attached inspectable metadata | no public Source resource yet |
| Quality | explicit context; `unknown` allowed | no scoring scale |
| Provider reference | assertion/provenance value | never Place identity |
| Unresolved-location assertion subject | Domain-supported | public API exposure deferred |

## Historical resolution

`NO SILENT SUBSTITUTION`: a historical/retired GeoID conceptually returns the requested identity, resolution/new-use context, identity relationships, and applicable survivor/successor identities. A survivor is never silently returned as if it were the requested identity. Lifecycle enum and field form remain deferred.

## Current Representation

A Current DAEN Representation is a Place-associated selected view, not absolute truth. It has represented fact/purpose, selection scope and attribution, supporting Source Assertions, Provenance, and explicit Quality including `unknown`. Relevant competing assertions for the same Place, fact/purpose and scope must remain retrievable, though not necessarily inline. No ranking algorithm is defined.

## Withdrawal T1/T2

T1 affects Place identity/resource: GeoID remains historically resolvable, is not valid for new operational use, and is never reused. T2 affects a Source Assertion/historical reference: it remains retained and traceable and does not automatically withdraw the underlying Place. The effect of T2 withdrawal on a Current DAEN Representation is deliberately deferred.

## Guardrails

05A guarantees same-subject Source Assertion supersession only. Cross-subject relations may be exposed as historical context; no reassociation, effective migration, or cross-subject supersession is promised.

Extent is read-only, embedded/related, with Provenance/Quality context. No independent identity, history/versioning, bare-Extent supersession, role vocabulary, geometry schema, overlap semantics, or mutations are promised.

Containment exposes only `Place contains Place` and the reverse read perspective `Place is contained by Place`; no reciprocal Domain relationship, currentness, temporal fields, transitivity, inheritance, parent policy, or subtype taxonomy is frozen.

Persisted/exposed facts, selections, resolution decisions and material corrections remain attributable. Generic relation/history records use Provenance where required by the model; 05A does not force an identical Quality schema onto every relation.

## Accepted resource-model coherence checks

1. Place uses GeoID; Source Assertion and Access Point do not.
2. Opaque references are not GeoIDs.
3. Current Representation remains Place-associated.
4. Selected Coordinate is not an Access Point.
5. Extent is not a promised top-level resource.
6. Extent history/versioning remains deferred.
7. Resolution Link remains relationship/history data.
8. Correction is not a top-level resource.
9. Succession remains distinct from derived read facets.
10. Containment remains one directional Domain relation with two read perspectives.
11. T1 withdrawal preserves historical Place resolution.
12. T2 withdrawal does not automatically withdraw the Place.
13. Historical resolution does not silently substitute a survivor.
14. Provider references do not become Place identity.

These are resource-model checks only; they define no endpoint layout or reference format.
