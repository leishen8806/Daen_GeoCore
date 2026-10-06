# DAEN GEO CORE DOMAIN MODEL

## 1. Document Status

- Phase: `Phase 03 — Domain Model`
- Status: `BASELINE CANDIDATE`
- Authority: Phase 03 Human Freeze Decisions
- Governing boundary: DAEN Geo Core Product Constitution
- This document is conceptual and does not define database schema, API endpoints or implementation.

## 2. Governing Product Constitution

This model is subordinate to `GEO_CORE_PRODUCT_CONSTITUTION.md`. It preserves the Constitution principles of geography over business logic, stable DAEN-controlled Place identity, provider independence, Access Point separation, correction, provenance, data quality and Current DAEN Representation.

If this model conflicts with the Product Constitution, the conflict must be reported and resolved through a Constitution amendment. It must not be silently resolved in a later implementation.

## 3. Domain Modeling Goals

The model must provide a clear conceptual language for:

- persistent real-world loci;
- stable Place identity;
- source-attributed claims about location facts;
- the current DAEN representation of known facts;
- Access Point and Extent as separate concepts;
- non-destructive correction, merge and split history;
- provenance and quality without claiming perfect physical truth.

It must keep business, occupant and operational semantics outside Geo Core.

## 4. Domain Terminology

### 4.1 Place

A Place is a persistent, referable real-world locus: a physical site or premises that can be referenced independently of its occupant, owner, business name, provider record, address or coordinates — `CONFIRMED`.

`Place = WHERE`; business, organization and tenant describe `WHO` and are not Geo Core Place objects.

### 4.2 Source Assertion

A Source Assertion is a source-attributed statement about a Place or an unresolved real-world location. Examples include name, address, coordinate, Extent and provider-derived assertions — `CONFIRMED`.

The preferred Phase 03 term is Source Assertion. `Observation` is not the primary term.

### 4.3 Current DAEN Representation

The Current DAEN Representation is DAEN's current best-known representation selected from relevant Source Assertions for a defined scope. It is not absolute physical truth — `CONFIRMED`.

### 4.4 Selected Coordinate

Selected Coordinate is the coordinate currently selected for a defined scope. It is not a synonym for Place identity or Access Point — `CONFIRMED`.

### 4.5 Access Point

An Access Point is a first-class domain object representing a real-world point used to access a Place. Entrance may later be a subtype or semantic. Pickup and drop-off are business meanings and are excluded from this domain vocabulary — `CONFIRMED`.

### 4.6 Extent

Extent is a spatial fact describing a Place. It may describe a building footprint, property extent or campus extent. It has no independent GeoID in Phase 03 — `CONFIRMED`.

### 4.7 Area

Area is a future separate geographic concept. Neighborhoods, villages and administrative areas are not Place in this model — `CONFIRMED`; Area identity is `TBD`.

## 5. Core Domain Concepts

The Phase 03 conceptual model contains:

- Place
- GeoID
- Source Assertion
- Current DAEN Representation
- Resolution Link
- Access Point
- Extent
- Correction
- Succession

Cross-cutting concepts:

- Provenance
- Quality

Route remains a reusable capability candidate, not a domain object — `CANDIDATE`.

## 6. Conceptual Relationship Model

```text
Place
├── GeoID
├── Source Assertions
│   ├── Name
│   ├── Address
│   ├── Coordinate
│   ├── Extent
│   └── Provider-derived assertion
├── Current DAEN Representation
├── Access Points
├── Extents
├── Resolution Links
├── Corrections
└── Succession

Cross-cutting: Provenance, Quality
```

This is a conceptual relationship view. It is not a database or API design.

## 7. Place Definition

Place is a locus-based concept. A shopping mall, a shop premises inside the mall, a school campus and a hospital site can each be Places. A tenant company, institution, owner or brand is not automatically a Place.

Place identity is independent of occupant, owner, business name, provider record, address and coordinate. Exact taxonomy and identity boundaries remain subject to the invariants and TBDs below.

## 8. Place Identity Boundary

GeoID identifies Place only in Phase 03 — `CONFIRMED`.

GeoID does not identify Access Point, Area, Extent, Route or other geographic objects in this phase. Future namespaces require separate decisions.

Changes to name, owner, tenant, provider reference or address MUST NOT automatically create a new Place. A different locus normally indicates a different Place. Edge cases require explicit identity policy.

Geo Core does not introduce business identifiers as a business registry.

## 9. GeoID Semantics

GeoID is the stable DAEN-controlled identity term for Place — `CONFIRMED` as scope, `TBD` as design.

Rules:

- A GeoID MUST NOT be reassigned to another Place.
- A previously used GeoID MUST NOT become reusable after removal.
- A retired GeoID remains resolvable subject to authorized removal rules.
- GeoID format, generation, persistence, resolution and lifecycle are deferred.

## 10. Source Assertion Model

Source Assertions preserve what a source said about a Place or unresolved location. They may describe:

- Name
- Address
- Coordinate
- Extent
- Provider-derived location information

Assertions can disagree, become stale or be superseded. They are not automatically the Current DAEN Representation and are not automatically proof of a separate Place.

## 11. Current DAEN Representation

DAEN selects a current best-known representation from relevant Source Assertions for a defined scope. The selection is attributable and must retain enough history to explain material changes.

The representation may include a Selected Coordinate, selected address expression, selected names and selected Extent. The exact structure and selection policy are deferred.

“Canonical Selection” is not the preferred Phase 03 term. Legacy Constitution wording “canonical representation” maps to Current DAEN Representation without changing the frozen meaning.

## 12. Address Semantics

Address is a location expression about a Place. Multiple language forms and address expressions may refer to one Place. Address is not Place identity.

Normalization, administrative hierarchy, language variants and conflict resolution are `TBD`.

## 13. Coordinate Semantics

Coordinates are Source Assertions or selected location facts associated with a Place or Access Point. A coordinate does not by itself establish Place identity.

Selected Coordinate does not automatically represent the practical access point. Precision, confidence, source quality and verification semantics are `TBD`.

## 14. Access Point Semantics

Access Point is a first-class Geo Core object with a stable internal reference that is separate from the Place GeoID namespace.

- One Place MAY be served by multiple Access Points.
- One Access Point MAY serve multiple Places.
- Access Point MUST NOT be inferred solely from Selected Coordinate.
- Entrance MAY later be represented as an Access Point subtype or semantic.
- Pickup, drop-off and rider waiting meanings remain business semantics.

Access Point public identity and namespace are `TBD`.

## 15. Extent Semantics

Extent is a spatial fact about a Place. A Place MAY have different Extents for different roles, such as building footprint, property extent or campus extent.

Extent has no independent GeoID in Phase 03. Delivery zones, pricing zones, attendance zones and service zones are business-policy zones, not Place Extents.

Extent roles and geometry semantics are `TBD`.

## 16. Resolution Link

A Resolution Link records an identity or representation relationship between historical, duplicate, merged, split or withdrawn records. It must identify the relationship in a traceable way.

Resolution Link semantics, direction and allowed relationship types are `TBD`.

## 17. Provenance

Persisted or externally exposed location facts, Source Assertions, identity-resolution decisions, Current DAEN Representations and material corrections MUST be attributable.

This does not require a permanent complete provenance graph for every ephemeral derived calculation. Requirements for derived capability provenance are deferred to API and architecture phases.

## 18. Data Quality

Quality is cross-cutting context for location facts and representations. Geo Core must be able to distinguish known, uncertain, stale, conflicting, incomplete or corrected information in later designs.

Quality dimensions, scales, source trust ranking and conflict resolution are `TBD`.

## 19. Location Correction

Correction replaces or supersedes a material location assertion or representation without silently erasing history.

Normal correction follows a supersession chain:

```text
old Source Assertion or representation
        ↓ superseded
new Source Assertion or representation
```

Correction authority, review process, controlled removal and security rules are `TBD`.

## 20. Place Lifecycle

Place lifecycle concerns the physical or geographic status of the locus, not the operating status of an occupant or business.

Business closure, tenant closure, business hours and institution operating status MUST NOT become Place lifecycle. A sealed access point, demolished building or physically inaccessible site MAY be a Geo Core fact when it describes the locus itself.

Lifecycle states, transitions and evidence are `TBD`.

## 21. Merge Semantics

When two Place records are determined to represent the same real-world Place:

- one identity survives;
- the other GeoID becomes retired;
- the retired GeoID is never reassigned;
- the retired GeoID remains resolvable;
- the resolution explicitly identifies the survivor and merge relationship;
- material history remains attributable;
- merge is non-destructive and governance-reversible.

Survivor selection policy is `TBD`.

## 22. Split Semantics

### 22.1 Mis-conflation

One record incorrectly represented two Places. The original GeoID MAY continue to represent the true original locus, while a new GeoID is created for the other Place.

### 22.2 True division

One historical Place genuinely becomes multiple Places. The original GeoID becomes historical or superseded and the resulting Places receive new GeoIDs. A child MUST NOT silently inherit the old GeoID.

Split evidence and exact resolution semantics are `TBD`.

## 23. Relocation Semantics

A Place does not move. Occupants or businesses move between Places.

For example, a pharmacy moving from an old site to a new site changes the business's Place reference; it does not move the old Place. Geo Core does not create a business registry to manage that relocation.

## 24. Closure and Withdrawal Semantics

GeoID resolvability MUST apply after closure, merge, split and withdrawal. Resolvable does not mean active and does not mean valid for new operational use.

Withdrawal may indicate that a record should not be used for new operations while preserving historical resolution. Authorized legal, privacy, security or data-rights removal MAY follow a controlled process.

The Product Constitution now covers closure, merge, split and withdrawal resolvability through a controlled amendment recorded in the Decision Log and TBD Register.

## 25. Containment

Place MAY contain Place — `CONFIRMED` as a minimal concept.

Containment remains one relationship only. Physical, functional, administrative and commercial containment taxonomies are not created in Phase 03. Multi-parent semantics remain `TBD`.

## 26. Succession

Succession records that a Place identity or representation has been superseded by later identities or representations. It supports non-destructive history for merge, split, withdrawal and material correction.

The exact succession types and lifecycle transitions are `TBD`.

## 27. Domain Invariants

1. A GeoID MUST NOT be reassigned to another Place.
2. A GeoID MUST remain resolvable after closure, merge, split or withdrawal, subject only to authorized legal, privacy, security or data-rights removal.
3. Name, address, coordinate, provider ID and business ID MUST NOT be Place identity.
4. Occupant, owner, business-name or provider changes MUST NOT by themselves change Place identity.
5. Multiple representations MUST NOT automatically create multiple Places.
6. Similar representations MUST NOT automatically prove the same Place.
7. Corrections MUST NOT silently erase material history.
8. Current DAEN Representation MUST NOT be presented as absolute truth.
9. Access Point MUST NOT be inferred solely from Selected Coordinate.
10. Pickup and drop-off MUST NOT become Geo Core domain semantics.
11. Merge and split MUST remain attributable and non-destructive.
12. Business closure MUST NOT become Place lifecycle.
13. Provider taxonomy MUST NOT define DAEN Place taxonomy.

## 28. Explicitly Excluded Concepts

The following do not enter the Phase 03 Geo Core domain model:

- Area, neighborhood, village and administrative area
- Street and intersection
- Business, branch, owner, organization and tenant
- Pickup, drop-off and rider waiting point
- Route object
- Delivery, pricing, attendance and service zones
- Business operating status
- Business registry identifiers

## 29. Deferred Decisions

- GeoID format and generation algorithm
- Area model and identity
- Street and network concepts
- Access Point public identity or namespace
- Independent Extent identity
- Containment taxonomy and multi-parent containment
- Demolition and rebuild identity policy
- Merge survivor selection
- Correction authority and legal/privacy removal workflow
- Data Quality dimensions and numeric scales
- Source trust ranking and source conflict resolution
- Temporal state-as-of queries
- Route capability and provider mapping policy
- Provider taxonomy handling
- API, database and architecture
- M1 scenario and acceptance result

All are `TBD` and must be resolved in their assigned later phase.

## 30. Constitution Amendment Record

`RESOLVED — Extend GeoID resolvability from closure/merge to split/withdrawal.`

The Product Constitution was amended through the controlled revision recorded in `DECISION_LOG.md` and `TBD_REGISTER.md`.

## 31. Phase 04 Entry Gate

Phase 04 — M1 PRD may begin only after this conceptual model passes human review and the Constitution amendment is included in the reviewed baseline.

Phase 04 may define one validated M1 scenario and its acceptance criteria. It must not silently resolve the remaining TBDs or turn Route into a mandatory capability.
