# Phase 02 Decision Log

This log records the human freeze decisions used to write the Product Constitution. It is a traceability record, not a substitute for the Constitution.

| Decision | Frozen result | Status |
|---|---|---|
| D1 DAEN hierarchy | DAEN is the brand and location-infrastructure umbrella; DAEN Geo Core is the core platform under DAEN | `CONFIRMED` |
| D2 identity scope | Phase 02 requires stable identity capability for Place; other geographic objects may gain independent identity later | `CONFIRMED` |
| D3 identity continuity | Identity is not reassigned to a different Place; historical references remain resolvable after closure or merge; same-Place, split and relocation semantics are deferred | `CONFIRMED` |
| D4 Route | Route remains a reusable capability candidate, not a mandatory core capability | `CANDIDATE` |
| D5 pickup and drop-off | Pickup and drop-off are business semantics and do not enter the Constitution | `CONFIRMED` |
| D6 Access | Access Point is the general concept; Entrance may later be a subtype or semantic | `CONFIRMED` |
| D7 scope admission | 4 MUST tests plus 1 SHOULD reusability test; two existing consumers are not required | `CONFIRMED` |
| D8 history | Preserve non-destructive history, with authorized legal, privacy, security or data-rights exceptions | `CONFIRMED` |
| D9 operational tools | Correction and data-operations tools may be first-party Geo Core components, but are not the complete value definition | `CONFIRMED` |
| D10 brand wording | DAEN and Geo Core are stable project terms; Khmer/Chinese expression and positioning retain their stated status | `CONFIRMED` |
| D11 rationale | Product rationale may precede market validation; M1 must validate real use and willingness to adopt or pay | `CONFIRMED` |
| D12 canonical representation | Geo Core maintains the canonical DAEN representation of known facts; it does not claim perfect physical truth | `CONFIRMED` |

## Phase 03 Human Freeze Decisions

| Decision | Frozen result | Status |
|---|---|---|
| H1 Place | Place is a persistent, referable real-world locus; Place is WHERE and occupant/business is WHO | `CONFIRMED` |
| H2 same Place | Locus continuity governs identity; name, owner, tenant, address or provider change does not automatically create a new Place | `CONFIRMED` |
| H3 Area | Area is not Place; Areas are a future separate concept | `CONFIRMED` |
| H4 GeoID scope | GeoID identifies Place only in Phase 03 | `CONFIRMED` |
| H5 merge | Retire one identity, resolve to survivor, never reassign retired GeoID, preserve historical resolution | `CONFIRMED` |
| H6 split | Mis-conflation and true division use different identity outcomes; children do not silently inherit the old identity in true division | `CONFIRMED` |
| H7 relocation | Place does not move; occupants or businesses move between Places | `CONFIRMED` |
| H8 demolition and rebuild | No default same-Place rule | `TBD` |
| H9 Access Point | First-class object with internal reference; no Place GeoID; one Access Point may serve multiple Places | `CONFIRMED` |
| H10 representation terms | Source Assertion, Current DAEN Representation and Selected Coordinate are the preferred terms | `CONFIRMED` |
| H11 Extent | Extent is a Place spatial fact without independent GeoID; business policy zones are separate | `CONFIRMED` |
| H12 correction | Supersession chain with controlled removal exception; used GeoID is never reusable | `CONFIRMED` |
| H13 containment | Place may contain Place as a minimal relationship | `CONFIRMED` |
| H14 spatial anchoring | A valid Place needs at least one locating basis, but not necessarily a precise coordinate | `CONFIRMED` |
| H15 resolvability | GeoID remains resolvable after closure, merge, split and withdrawal | `CONFIRMED` |
| H16 terminology | Resolution Link and Succession remain; Phase 03 avoids Observation and Canonical Selection | `CONFIRMED` |
| H17 temporal history | Material supersession is retained; arbitrary as-of-time queries remain deferred | `CONFIRMED` |
| H18 business closure | Occupant/business operational status does not become Place lifecycle | `CONFIRMED` |
| H19 provenance scope | Persisted or externally exposed facts and decisions are attributable; ephemeral calculations need not create a permanent graph | `CONFIRMED` |

## Constitution amendment status

`RESOLVED — GeoID resolvability is extended from closure/merge to closure/merge/split/withdrawal.`

The controlled Product Constitution revision is recorded below.

## Constitution Amendment — GeoID Resolvability

**Decision:** GeoID resolvability is extended from closure / merge to closure, merge, split and withdrawal.

**Reason:** Phase 03 Domain Model identified that stable historical identity requires references to remain resolvable across split and withdrawn Place states.

**Status:** `CONFIRMED`

**Source:** `Phase 03 Human Freeze Decision H15`

## Conflict resolution

The earlier source material contained an organization-operations positioning. Phase 01 isolated it from the active Geo Core baseline. This Phase 02 Constitution keeps the location-infrastructure identity and does not import that historical positioning.
