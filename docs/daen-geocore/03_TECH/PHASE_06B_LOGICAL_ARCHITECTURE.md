# DAEN Geo Core — Phase 06B Logical Architecture

## Status

`PHASE 06B LOGICAL ARCHITECTURE = HUMAN FROZEN`

## Pattern

`Modular Monolith`: one deployable application with strict ownership boundaries and future extraction seams. Physical deployment topology and technologies are not frozen.

## Module map and ownership

Authoritative domain modules: identity; assertions; representation; access (read-only); containment (read-only). Application/orchestration: operations; query; ingestion; jobs. Cross-cutting: mutation; audit; policy; contracts; observability ports. Quality and Extent are not standalone modules.

`identity` owns Place identity, GeoID existence, new-use standing, merge/split/closure/T1 history, Resolution Link, Succession where present and historical exact resolution. Identity and resolver are one authority and do not decide same-Place, survivor policy, governance or business status.

`assertions` owns immutable Source Assertions, create/supersede/correct/T2 withdrawal, history, Source Provenance and Quality. No cross-subject reassociation.

`representation` owns SelectionRecord, exact slots, add/replace and Current Representation derivation. Dependency is representation → assertions → identity; no reverse dependency, ranking or selection authority.

`access` and `containment` are thin read-authority modules with no sanctioned write interface. Extent is a fact/value inside existing records with no Extent module/service.

## Bootstrap and mutation

Place Bootstrap is an internal capability inside operations for CD-1 provisioning and CD-2 Split children. It stages allocation, identity, assertions, locating basis and coherent commit, without public route, identity decision or deduplication.

Logical mutation process: DECIDE/STAGE → REVALIDATE authoritative read-set → ONE LOGICAL COMMIT DECISION → VISIBLE. This is logical atomic visibility, not one SQL transaction, database, 2PC or consensus mechanism.

Reference allocation is a shared capability with stable, non-reused, restore-safe, multi-region-safe semantics; no physical allocator or issued-reference ledger is selected. Idempotency supports public client-global keys and internal provisioning bindings. MutationBasisToken is opaque and validated against authoritative state; cache/projection is never authority.

## Read architecture

`query` composes only facets required by frozen API contracts and owns no authoritative state. Place reads do not automatically inline AP or Containment. Derived data must be same-event visible, sufficiently fresh against authority, or fail/fallback safely. Resolution may later use traversal, projection/index or hybrid; projections are rebuildable and cannot substitute the requested identity.

## Audit, policy and residency

Source Provenance, mutation Audit and operational Logs remain separate. `audit` is the authoritative mutation-attribution boundary and non-destructive by default while preserving authorized removal feasibility. No Actor/Tenant/Organization entity is introduced.

`policy` provides authentication/client-identity, authorization, residency, redaction, audit and secrets hooks. Enforcement must cover writes, reads, jobs, replication/export, backups and telemetry at sufficient granularity for Cambodia-only restricted detail. Policy schema/classification/legal semantics remain TBD.

## Dependency rules

Transport → Facade → Application → Domain Owner → Ports. Infrastructure implements Ports. No cross-module persistence access, module-owned writes only, jobs/ingestion call facades, no domain dependency on HTTP/cloud/database/broker, no shared mutable domain models, and acyclic domain reads.

## Authoritative / derived / operational

Authoritative: Place identity/history, Source Assertions/history, SelectionRecords, AP records, Containment relations, material idempotency bindings and mutation audit. Derived: Current Representation, projections and MutationBasis state. Cached: infrastructure caches only. Operational: ingestion staging and job state. Reference allocation is authoritative semantic responsibility without frozen physical ledger.

## Ingestion, jobs and extraction

Operations coordinates provisioning and Split use cases; jobs owns scheduling/retry/failure state and calls facades; ingestion maps EXISTING to normal mutation, NEW to CD-1 and UNRESOLVED to no identity, with per-item retry and no batch atomicity. Explicit ownership interfaces and no shared mutable stores preserve future extraction; commit-coupled modules may extract together or with coordination preserving logical atomicity.

## Multi-region readiness

Future quorum-backed commits cover only authoritative state participating in a mutation. Boundaries must preserve multi-region writes, global uniqueness/non-reuse, idempotency, read freshness and multi-cloud execution. No consensus mechanism is selected.

## Anti-modules

Do not introduce standalone Quality, Extent, Provider, Tenant/Organization/Business, SamePlace/Matching/Dedup, Identity Decision Engine, Blockchain, Generic Relationship, Separate Resolver, Search/Geocoding or Event Bus semantic modules without authorized scope change.

## Protected TBDs

Same-Place/dedup; source ranking; selection authority; survivor policy; withdrawal authority; H14 lifetime; AP writes/lifecycle; containment writes/currentness; Extent geometry/history; richer scope equivalence; temporal/as-of; provider selection; auth/privacy; locating-basis adequacy remain protected.

## Logical ADR candidates

Modular monolith; module ownership/dependencies; identity/resolution; assertions/representation; Place Bootstrap; logical mutation unit; idempotency ownership; read/freshness boundary; audit; residency; ingestion/jobs. No technology ADRs are created.

`PHASE 06B = HUMAN FROZEN`

`PHASE 06C PERSISTENCE / IDENTITY / HISTORY / SPATIAL = NOT YET AUTHORIZED`
