# DAEN Geo Core — Phase 06 Technical Architecture Entry Gate

## Status

`PHASE 06 TECHNICAL ARCHITECTURE ENTRY GATE = HUMAN FROZEN`

`PHASE 06A ARCHITECTURE REQUIREMENTS & QUALITY ATTRIBUTES = AUTHORIZED`

## Authority

Constitution > Domain Model > M1 controlled clarifications > Phase 05 frozen API contracts > Phase 06 ADRs. An ADR cannot override a frozen contract. Contract ambiguity is escalated for bounded amendment; architecture does not repair contracts silently.

## Purpose and boundary

Phase 06 defines how frozen Geo Core Domain/API contracts are implemented. It may define mechanisms but may not create Product, Domain or API semantics for convenience. No technology, database, framework, table, code, OpenAPI or architecture decision is selected by this Entry Gate.

## Architecture decision inventory

Planning categories only: read-consistency model; logical atomic visibility; authorized-removal feasibility; identity/reference allocation; recovery/backup; history mechanism; Current Representation computation/materialization/cache; resolution traversal/projection/index; MutationBasisToken implementation; Idempotency-Key persistence/fingerprint/expiry; concurrency and stale-write control; logical atomicity; persistence capability; spatial capability; AP extensibility; Provenance normalization; Quality storage; containment storage; security/auth/client identity; provider adapters; service topology; runtime/framework; deployment/regions; observability; performance/scalability; cost/operational simplicity; read-consistency model validation; ADR governance.

These categories include read-consistency, authorized-removal feasibility, open typed-value representation, requesting-client identity hook, recorded-time/clock source, and ADR governance as explicit planning questions.

## Atomicity correction

Phase 05 requires one coherent externally visible semantic outcome per logical mutation. This is logical atomic visibility, not necessarily one physical database/service commit. Callers must never observe a half-applied mutation.

## Frozen architecture constraints

- Place-only GeoID.
- Historical identity resolvability.
- Stable non-aliased references.
- Immutable material assertions and selections.
- Non-destructive history.
- Logical atomic visibility.
- Stale-write rejection.
- Idempotency-Key semantics.
- Exact-reference/no-search boundary.
- No destructive public history delete.
- AP public read-only boundary.
- Extent mutation gate.
- Minimal containment.
- Provider independence.

No mechanism is frozen.

## Identity and recovery

Allocation must remain unique through backup/restore and never cause GeoID/API reference reuse. Future authorized legal/privacy/security removal must remain feasible without defining that policy. Backup purge/redaction policy is not defined.

## Representation and resolution

Architecture may evaluate computed, materialized, partially materialized or cached Current Representation, retaining authoritative history, supporters, competing evidence and rebuildability. T2 withdrawal does not automatically modify Current Representation. Resolution may use traversal, projection/index or hybrid; projections are not Domain authority and cannot substitute the requested identity.

## MutationBasisToken and idempotency

MutationBasisToken remains opaque, non-identity, state-invalidating and authoritatively validated at write time. Idempotency-Key remains client-global for material public mutations with a seven-day minimum replay guarantee. Phase 06 may decide persistence, fingerprinting, expiry, in-flight coordination and crash consistency.

## Persistence, spatial and AP boundaries

Domain concept, API resource and database table are distinct. Event sourcing is not required. Spatial capability may be prepared without deciding Extent geometry, CRS, precision or roles. AP semantics remain separable/extensible; no dedicated AP module/table or write/lifecycle/backing model is frozen.

Originating-source and mutation Provenance remain distinct. Quality must represent explicit `unknown`, remain extensible, avoid an invented numeric scale/ranking, and not prohibit a future approved dimension. Containment storage must not force tree, DAG, single parent, currentness, transitivity or inheritance.

## Security, provider and topology boundary

Phase 06 may design authentication, client identity, authorization hooks, redaction, audit and secrets handling without creating Tenant, Organization or Business concepts. Provider adapters may be designed but no provider is selected. Candidate topologies are modular monolith, bounded services, distributed/event-driven and hybrid; none is selected. Any distributed design must preserve logical atomic visibility and coherent reads.

## Capability classes

Relational transactional, spatial, document, event, graph, key-value/cache and object/archive are capability classes only. No product is selected and no datastore is required merely because a Domain relation exists.

## Quality priorities

Tier 0: semantic correctness, historical resolvability, non-destructive integrity.
Tier 1: coherent consistency, auditability, recoverability, security boundary, provider independence.
Tier 2: operational simplicity, observability, evolvability.
Tier 3: performance, scalability.
No SLA, QPS or latency numbers are frozen.

## Protected TBD matrix

Phase 06 may design around, but must not decide: cross-subject reassociation; lifecycle taxonomy; demolition/rebuild and demolition→closure; withdrawal authority/removal; Extent semantics; containment currentness/multi-parent; selection authority; selected-value derivation; source ranking; Quality scale; merge survivor policy; same-Place algorithm; generic Place creation; AP write/lifecycle/subject semantics; temporal/as-of; richer scope equivalence; merge reversal/reopen/un-withdraw; and auth/privacy semantics.

## Phase 06 subphases

06A Requirements & Quality Attributes; 06B Logical Architecture; 06C Persistence / Identity / History / Spatial; 06D Concurrency / Idempotency / Atomicity; 06E Runtime / Technology / Deployment / Observability; 06F Architecture Final Gate.

A concrete product may be selected after its required capabilities/constraints are frozen. Primary datastore may be selected in late 06C, concurrency capability validated in 06D, and framework/runtime/deployment mainly in 06E.

## ADR program

ADR-001 Authority and contract precedence; ADR-002 logical atomic visibility; ADR-003 consistency; ADR-004 history mechanism; ADR-005 identity/reference allocation; ADR-006 recovery; ADR-007 Current Representation; ADR-008 resolution projection; ADR-009 MutationBasisToken; ADR-010 idempotency; ADR-011 stale-write concurrency; ADR-012 persistence capabilities; ADR-013 spatial capability; ADR-014 AP extensibility; ADR-015 Provenance; ADR-016 Quality; ADR-017 containment storage; ADR-018 security/client identity; ADR-019 provider boundary/topology; ADR-020 observability/deployment. Planning inventory only; no ADR outcome files are created here.

## Architecture validation plan

1 identity uniqueness through restore; 2 historical resolution; 3 no-aliasing; 4 assertion immutability; 5 selection history; 6 logical atomicity; 7 stale-write rejection; 8 idempotent replay; 9 conflicting idempotency intent; 10 Current Representation rebuild; 11 competing evidence discovery; 12 exact resolution no-search; 13 T1/T2 separation; 14 Extent write gate; 15 AP read-only boundary; 16 containment non-tree flexibility; 17 Provenance separation; 18 explicit unknown Quality; 19 provider independence; 20 restricted-detail handling; 21 observability/recovery evidence. These validate architecture against frozen contracts and create no Domain semantics.

## 06A operating-assumption gate

06A may start immediately but may not reach Human Freeze until expected workload, expected growth, availability expectations, deployment region/data-residency constraints, budget/operational constraints, and team stack/operations capability are explicitly recorded. Architecture must not invent them.

## OpenAPI boundary

OpenAPI and JSON Schema are wire artifacts derived from frozen API semantics. They may not invent semantics and are not a Phase 06 Entry blocker.

## Phase 01 proposals

Phase 01 strategy/proposal documents are non-authoritative context only. Tenant, organization, Agent runtime, worker/queue and Office modules are not imported into Geo Core merely because they appear there.
