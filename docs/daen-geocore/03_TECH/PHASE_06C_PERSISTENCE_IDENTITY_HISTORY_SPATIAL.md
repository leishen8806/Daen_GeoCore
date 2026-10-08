# DAEN Geo Core — Phase 06C Persistence / Identity / History / Spatial

## Status

`PHASE 06C PERSISTENCE / IDENTITY / HISTORY / SPATIAL = HUMAN FROZEN`

`DATABASE PRODUCT = NOT SELECTED`

`PHASE 06D CONCURRENCY / IDEMPOTENCY / ATOMICITY = NOT YET AUTHORIZED`

## Persistence pattern

Use immutable material records, explicit non-destructive history facts, small synchronously maintained rebuildable heads, and derived rebuildable views. Material/history state wins over a disagreeing head. Event Sourcing is not required as the authoritative model. Authorized removal feasibility remains mandatory.

## Primary store and identity

`PRIMARY AUTHORITATIVE STORE CLASS = RELATIONAL TRANSACTIONAL`

`ONE PRIMARY AUTHORITATIVE STORE INITIALLY`

No database product is selected. Place identity is immutable with explicit identity/history facts and a rebuildable per-Place current head. No lifecycle enum is introduced. Resolution Link and Succession are first-class persisted relationship/history records with exact historical lookup, both-direction indexing capability and no silent substitution. Traversal/projection algorithms and graph technology remain open.

## Reference family and non-reuse

Preferred family for GeoID/PlaceRef, SourceAssertionRef, SelectionRecordRef and AccessPointRef: stateless cryptographically strong random fixed-width references, minimum 120 random bits, 128-bit class preferred. References remain typed, opaque, provider/region/shard independent and semantically meaningless. Textual format, prefix, checksum, width/form, UUID choice and surrogate keys remain deferred.

Random generation is insufficient alone: live uniqueness plus durable accepted-reference non-reuse evidence/reconciliation is required. Acknowledged, committed-visible or externally observed references never become reissuable after restore. Unexposed failed-operation references may be discarded. No central allocator ledger is required.

## Assertions and representation

Source Assertions remain immutable; standing/history is appended through explicit facts; no cross-subject reassociation. SelectionRecord is authoritative and immutable, with a synchronously maintained exact-slot head; Current Representation is derived/assembled from selection state and no asynchronous authoritative projection is required initially. Exact typed scope equality is supported without normalization, aliasing, fallback or richer equivalence.

## MutationBasis and idempotency

Persistence must support authoritative owner witnesses/revisions, conditional writes, insert-if-absent, compare-and-set equivalents, read-set revalidation, selection-slot absence/current witnesses and assertion-standing witnesses. Restore must not let a pre-restore basis validate against a different post-restore state. Mechanism is deferred to 06D.

Public idempotency uses client-global keys with >=7-day replay; internal provisioning binds client/request identity for the resulting Place lifetime. Request identity, intent fingerprint, original result refs and mutation shared fate are durable; cache is never authority.

## Audit and recorded time

Source Provenance, Mutation Audit and Operational Logs remain distinct. Audit is authoritative, recoverable, queryable, non-destructive by default and capable of authorized redaction/removal. No blockchain, Merkle tree, hash chain, event sourcing or physically unredactable store is required. A controlled Clock/Recorded-Time capability is required; wall clock is not identity authority, same-Place authority, total order or consensus time.

## Access Point / Containment / Spatial

AP persistence supports exact AccessPointRef lookup, Place↔AP relations, multi-Place service and neutral attributable facts with Provenance/Quality; no write/lifecycle model is frozen. Containment supports parent/child refs and both-direction lookup without tree, DAG, parent, cycle, transitivity, inheritance, currentness or write semantics.

Spatial readiness must not preclude coordinate facts, source CRS metadata, future geometry, spatial indexing or Cambodia-scale data. Extent geometry, CRS, precision, roles, history, public search, reverse geocoding and routing remain deferred. A disposable spatial spike is required before selecting a spatial product/extension.

## Evolution, partitioning and recovery

Backward-compatible expand/contract migration, readable old records, rebuildable derived indexes/views and rollback-compatible staged deployment are required. No sharding/partition key is selected. Exact lookups, Place-anchored collections, later partitioning and history/archive separation must remain possible.

Daily backups with 30-day retention, frequent/continuous change protection, planning RPO <=1h, RTO <=4h and rehearsed restore tests are required. Recovery validation covers reference non-reuse, provisioning bindings, idempotency, audit/history, removal/redaction resurrection and MutationBasis safety. Restoring an older backup must not resurrect authorized removals.

## Multi-region and residency

Architecture must remain compatible with quorum-backed logical commit, no split-brain, global idempotency/non-reuse, read-after-ack and multi-cloud. Async multi-writer conflict merge, last-write-wins, wall-clock conflicts, per-region uniqueness, encoded public refs and a proprietary global facility as sole correctness mechanism are rejected defaults. No consensus implementation is selected.

Residency must allow Cambodia-only restricted details to be independently controlled for placement, replication, backup, export and redaction while preserving applicable global identity/history. Exact decomposition and metadata granularity remain deferred.

## Capability matrix

Required now: transactional grouping, exact lookup, uniqueness, conditional writes, immutable/history records, append-oriented writes, backup/change recovery, export and operational maturity. Required by 12 months: secondary indexes and bounded pagination for large collections. Target readiness: multi-region evolution and spatial point/geometry. Optional/measured: replicas, spatial indexes and native partitioning. Managed-service availability is a strong selection preference, not a semantic requirement.

## Ownership and atomicity

Same physical store does not mean shared ownership. Modules own writes; cross-module access uses ports. Foreign typed references may be stored without owning foreign state. 06D must validate coherent all-or-nothing visibility, uniqueness at commit, conditional writes, authoritative revalidation, idempotency/audit shared fate, durable commit before acknowledgement, deterministic apply and crash safety. No transaction protocol is selected.

## Protected TBDs

Same-Place/dedup; source ranking; selection authority; survivor policy; withdrawal authority; H14 lifetime; AP writes/lifecycle; Containment writes/currentness; Extent geometry/history; richer scope equivalence; temporal/as-of; provider selection; auth/privacy; locating-basis adequacy and all other protected Domain/API TBDs remain unresolved.

## Gate

`PHASE 06C = HUMAN FROZEN`

A limited conformance re-review is required before 06D.
