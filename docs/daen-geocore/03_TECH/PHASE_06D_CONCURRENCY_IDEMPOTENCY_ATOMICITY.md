# DAEN Geo Core — Phase 06D Concurrency, Idempotency and Atomicity

## Status

- PHASE 06D CONCURRENCY / IDEMPOTENCY / ATOMICITY = HUMAN FROZEN
- PHASE 06E RUNTIME / TECHNOLOGY / DEPLOYMENT / OBSERVABILITY = NOT YET AUTHORIZED
- Limited 06D conformance re-review is required before Phase 06E.
- Baseline: `751cafe8311108a9961801678ecf8128c8fda100`

## Scope Boundary

This document freezes architecture capabilities and invariants only. It selects no database, cloud, framework, runtime, queue, cache, consensus product, schema, code, or OpenAPI behavior, and does not resolve protected Domain/API TBDs.

## Concurrency and Mutation Basis

- Use optimistic concurrency across requests.
- Authoritative commit-time revalidation, conditional writes, and uniqueness are final safety controls.
- Semantic conflicts are not silently retried; technical retries are allowed only while semantic intent and caller basis remain valid.
- MutationBasisToken is an opaque integrity-protected commitment to caller-observed authoritative owner witnesses plus the current Recovery Incarnation. Caller basis and server read-set are distinct. It is not identity, a timestamp, a public revision, or a global snapshot ID.
- Each relevant committed transition changes an unrepeatable opaque owner-state witness. A rollbackable sequence alone is insufficient. Absence-sensitive state may use absence plus Recovery Incarnation.
- Stable exact-equality representation is required for contract-recognized typed scope values; normalization, aliasing, language fallback, richer equivalence, and universal serialization remain open.

## Recovery and Serving Gate

A rollback-capable recovery requires:

`RESTORE → NON-REUSE RECONCILIATION → NEW RECOVERY INCARNATION → BASIS-SAFETY VALIDATION → AUTHORITATIVE SERVING`

Recovery Incarnation is fresh and random after backup restore, PITR rollback, or unsafe recovery; intact failover/catch-up preserving committed history does not require a change. It is initialized before serving. Pre-recovery basis tokens become invalid. Failure to establish the gate fails closed. No last-commit comparison algorithm is selected.

The minimal basis/read-set model covers merge, split, closure/T1, supersede/correct, Selection Add/Replace, supporting assertions, assertion creation, and provisioning without broadening frozen caller requirements.

## Merge, Split, Assertion and Selection Concurrency

- Merge/split revalidate all participant witnesses atomically. One conflicting identity mutation may commit; the loser receives frozen stale/conflict semantics. Partial split children are impossible. Any physical lock ordering is deterministic, with encoding deferred.
- One concurrent supersede/correct transition wins. A standing witness prevents branching; T2 racing supersede/correct changes the standing witness. Duplicate desired T2 state may return `ALREADY_HOLDS`; T2 effect on existing Current Representation remains TBD.
- Concurrent Add for one exact slot yields one current slot. Concurrent Replace from one prior selection has one winner. Slot stale conflict uses the existing 409 category. Invalid/withdrawn supporting assertions before commit use the existing 422 category. No new status is added.

## Idempotency

Conceptual states are absent, in-flight/reserved, committed, and public replay memory expired; these names are not wire enums. Correctness authority is the unique committed binding whose binding and mutation share fate. Reservations/leases control liveness only.

For the same client, key, and semantic intent, one execution proceeds; duplicates may wait boundedly, replay a committed result, or be asked to retry with the same key after an unresolved wait. Duplicates never independently commit. No `IN_PROGRESS` semantic error class or exact transport/status behavior is frozen.

Intent fingerprints use the parsed typed semantic command, including operation, targets, and semantic parameters. Insignificant wire serialization differences are not semantic differences. MutationBasisToken is excluded. Fingerprint algorithm and serialization remain deferred.

Committed bindings retain immutable semantic outcome data sufficient to replay the original result: outcome category, success class, created/affected/relationship refs, and required immutable snapshot fields. Replay never derives the result from later mutable heads. Full HTTP bytes are unnecessary.

Public replay is guaranteed for at least 7 days; bindings may expire later and no permanent public conflict tombstone is required. Provisioning bindings last for the resulting Place lifetime. In-flight reservations may expire; a slow executor cannot bypass committed uniqueness and a crash cannot permanently block a key. Exact durations are deferred.

## Atomicity and Commit Pipeline

Initial mechanism class:

`ONE LOCAL TRANSACTIONAL COMMIT ACROSS PARTICIPATING AUTHORITATIVE RECORD SETS`

Authoritative logical mutations do not use saga/compensation for atomicity. Saga/async retry is permitted only for non-authoritative after-commit effects.

Conceptual pipeline:

`client identity/auth hook → typed semantic intent → intent fingerprint → idempotency gate → authoritative reads → domain validation → generate/fix references and recorded values → stage module changes → residency/policy checks → durable non-reuse reservation evidence → commit-time basis/read-set revalidation → uniqueness/conditional enforcement → audit + committed binding → local atomic commit → acknowledgment → after-commit effects`

The code shape and replaceable commit-port abstraction are not frozen.

## Reference Non-Reuse Evidence

Stable references use stateless cryptographically strong random generation, fixed-width typed namespaces, at least 120 random bits, with 128-bit class preferred, plus live uniqueness enforcement. Randomness is not the complete guarantee:

`random generation + live uniqueness + durable accepted-reference non-reuse evidence/reconciliation`

Before commit/acknowledgment, durable Write-Ahead Non-Reuse Reservation Evidence must exist in a failure domain independent of the primary recovery domain. It is conservative recovery/replay evidence, not an allocator, Domain truth, external commit authority, or proof that the mutation committed. Uncommitted reservations may remain permanently unused. Evidence protecting non-reuse must outlive the ordinary payload catastrophic RPO; initial serving remains Singapore-first, with a minimal independent durability control plane. Failure to establish evidence fails closed. No mechanism, vendor, or location product is selected.

Evidence classes remain separate: permanent reservation evidence, and request/reference recovery mapping (public at least 7 days; CD-1 provisioning for resulting Place lifetime). `OBS-06-ISSUED-REFERENCE-DETAIL-LOSS = OPEN / NON-BLOCKING`; the reference remains permanently non-reusable, while API representation remains undecided.

## Target Multi-Region Guarantees

The target architecture freezes only: one logical commit decision, quorum intersection, no split-brain, acknowledgment after durable quorum, idempotency as committed result, fixed generated refs/recorded values before commit, deterministic apply, no wall-clock conflict ordering, fail-closed quorum loss, and catch-up/verification before authoritative serving. No Raft, Paxos, quorum size, leader model, or product is selected.

Initial local transactional commit evolves to quorum-backed logical commit while preserving mutation intent, staged changes, generated refs, audit, idempotency, basis semantics, and acknowledgment only after durable commit decision.

## Reads, Retries and Isolation

After acknowledgment, an authoritative read must not return older relevant identity/selection state; otherwise use the authoritative source or fail safely. Technical transaction retries are bounded and observable, recheck authoritative state, stop on stale basis, and check committed bindings after unknown outcomes. Material mutations require serializable-equivalent protection for their declared authoritative read-set; global serializable isolation is not required.

Bulk ingestion uses per-item atomicity, stable item request identity, backpressure, partial success, no semantic dedup, and upstream conflict reporting. Jobs use job-level idempotency and the normal mutation pipeline. No queue product is selected. Correctness does not depend on synchronized wall clocks.

Authorized removal/redaction is a privileged material mutation with coherent visibility, concurrency safety, recovery-safe removal evidence, and restore-resurrection protection; tombstone, journal, retained-field, and authority details remain open.

## Capability and Synthetic Spike Requirements

A future primary store must demonstrate multi-record atomicity, uniqueness, conditional writes, insert-if-absent, serializable-equivalent declared-read-set protection, durable commit, retry/abort signals, recovery, and replication evolution. `DATABASE PRODUCT = NOT SELECTED`.

Disposable synthetic-data spikes are required for lost-response idempotency, same-key races, slot Add/Replace races, merge/split stale basis, supporting-assertion write skew, crash around commit, restore invalidation, non-reuse evidence outage/reconciliation, cross-module commit, and slow execution after lease expiry. No production or restricted data is used.

## Protected TBDs

Preserved unresolved items: same-Place/dedup; source ranking; selection authority; survivor policy; withdrawal authority; H14 lifetime; AP writes/lifecycle; Containment writes/currentness; Extent geometry/history; richer scope equivalence; temporal/as-of API; provider selection; auth/privacy; locating-basis adequacy; and T2 impact on existing Current Representation.

## C3 / F4 Bounded Repair — Durable Request/Reference Recovery Mapping

For every reference-issuing mutation with request identity semantics, independent write-ahead recovery evidence MUST include a durable Request/Reference Recovery Mapping containing the requesting client identity, request identity, semantic intent fingerprint, operation type, every generated stable typed reference, and the minimal immutable replay/recovery metadata needed to preserve the frozen idempotency outcome. It need not contain the full Domain payload, full HTTP bytes, or mutable current Place state.

For CD-1 Internal Place Provisioning, the mapping includes the resulting PlaceRef and every initial SourceAssertionRef generated by that attempt. It has the same independent failure-domain durability as non-reuse reservation evidence, survives the primary payload recovery-loss window, and fails closed if that durability cannot be established. Public mappings remain available for at least 7 days from the first accepted request; CD-1 mappings remain available for the lifetime of the resulting Place identity.

The mapping is written before authoritative commit. Its existence is reservation and recovery evidence, not Domain truth, commit authority, or proof that the mutation committed. A mapping may remain for an attempt that never commits.

On retry by the same client/request identity: a different fingerprint uses existing conflict semantics; a same-fingerprint committed binding replays the original result; a same-fingerprint mapping without a committed primary binding reuses exactly the mapped references, reconciles or safely reconstructs the mutation, and fails closed if safe reconstruction cannot be established. It MUST never mint replacement references.

For CD-1, the same internal client, request identity, and semantic intent always resolve to the same mapped PlaceRef and initial SourceAssertionRefs for the resulting Place lifetime, including after catastrophic primary loss. The primary committed binding remains authoritative proof of commit; the independent mapping remains recovery/reservation support.

The recovery serving gate must establish integrity and availability of non-reuse evidence, required retained mappings, a new Recovery Incarnation, and MutationBasis safety. It need not copy every mapping into the primary before serving, but affected reference-issuing/replay capability fails closed if safe consultation/reconciliation cannot be established.

### Repaired F4 Behavior

`R -> PlaceRef P + SourceAssertionRefs A1...An` is durably mapped independently; after acknowledged primary loss, retry of the same R finds and reuses P,A1...An, then safely reconstructs/recommits or fails closed. It never creates Q. `F4 = PASS after bounded repair`.
