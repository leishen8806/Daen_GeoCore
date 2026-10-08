# DAEN Geo Core — Phase 06A Architecture Requirements

## Status

`PHASE 06A ARCHITECTURE REQUIREMENTS & QUALITY ATTRIBUTES = HUMAN FROZEN`

`CD-1 INTERNAL PLACE PROVISIONING CONTRACT = OPEN`

`PHASE 06B FINAL FREEZE = NOT YET AUTHORIZED`

## Initial deployment profile

Singapore first; single-region-first; 24×7 service; planned maintenance 1–2/month for 30–60 minutes; planning RTO <=4 hours; whole-region catastrophe planning RPO <=1 hour; initial infrastructure budget < USD 500/month; managed services preferred; low-cost monitoring/logging SaaS preferred; modular monolith is a hypothesis only; no Kubernetes dependency; Windows and macOS development; one-command local startup. Initial semantics must remain compatible with later multi-region consensus.

## Target profile

Cambodia, Singapore and Malaysia are target regions. All may accept writes in the target architecture, with valid consensus/quorum commit before acknowledgement, no normal independent-region commit then merge, survival of committed ordinary core data through one-region loss, and future multi-cloud reachability. No quorum size, leader model, consensus algorithm or one-region-loss write policy is selected.

## Consistency and atomicity

Requirements include no split-brain commits, intersecting commit sets as required by the selected design, no acknowledgement of uncommitted material mutations, globally coherent idempotency/reference allocation, and read-after-ack freshness for authoritative mutable state. Stale nodes must not present stale material state as current. Stale-basis validation uses authoritative state. Logical atomic visibility is required; one physical transaction is not.

## Recovery and identity durability

Initial catastrophic planning targets RPO <=1 hour and RTO <=4 hours; acknowledged ordinary core data targets approximately zero RPO through normal single-region failure. Daily backups retained 30 days, portability, restore testing, history integrity, idempotency/mutation recovery consistency and reference non-reuse are required. Allocation must remain unique through restore, with durable allocator/reconciliation mechanisms; backup purge/redaction and long-term archival remain TBD.

## Residency

Cross-border replication is supportable but requires legal/compliance activation. Cambodia-only restricted payloads must remain Cambodia-resident; Singapore-first must not accept/store payload already classified as restricted. Classification, policy, schema and law interpretation remain TBD. Architecture needs sufficient granularity for enforcement; if foreign replicas are prohibited, Cambodia-internal failure domains or separately authorized policy are required.

## Scale envelope

Human assumptions only: 100k–1M requests/day; peak 10–100 QPS; 80% reads/20% writes; 1M–10M Places at 12 months; 5–20 assertions per Place; 50M–200M assertions upper scale; APs 30%–100% of Places; 30M–100M Places at three years; Cambodia-first. No byte, TB, ingestion-window or derived-QPS assumptions are frozen.

## Ingestion and CD-1

Internal bulk ingestion is required, outside public Phase 05 mutation API, and may optimize throughput without bypassing Provenance, Quality, history, reference stability or idempotency.

`CD-1 INTERNAL PLACE PROVISIONING CONTRACT = RESOLVED`

Large-scale ingestion needs new Place identities while Phase 05 has no generic Place-create contract. Phase 06 must not invent same-Place, duplicate detection, public POST /places or caller-supplied GeoID semantics. CD-1 is closed by the additive internal provisioning amendment. AP and Containment writes remain separate TBDs.

## Operability and developer experience

No dedicated SRE initially; repeatable deployment; automated backups; health/readiness; rollback; startup validation; secrets out of code/logs; incident runbooks; reproducible environments. Windows/macOS one-command setup, deterministic AI-agent-friendly commands and no production/restricted data locally. Production OS is not frozen.

## Portability and quality

Vendor managed services are allowed only with exportable core data, portable backups, isolated cloud-specific code, an exit path, no Tier-0/Tier-1 semantic dependency on proprietary features, and reachable multi-cloud architecture. Quality must represent explicit `unknown`, remain extensible, avoid invented numeric scales/closed enums, and preserve source-ranking TBD.

## History, spatial, containment and security

Ledger-style means durable replicated material history, append-oriented immutable records where required, auditability and recovery integrity; it does not require blockchain, hash chains, Merkle trees or event sourcing. Spatial capability must not decide Extent geometry/CRS/precision/role. AP remains separable/extensible without frozen module/table/write/lifecycle/backing design. Containment storage must not force tree, DAG, single-parent, currentness, transitivity or inheritance. Security may provide auth, client identity, authorization, redaction, audit and secrets hooks without creating Tenant/Organization/Business concepts. Provider IDs remain external; no provider selected.

## Quality priorities and trade-offs

Tier 0: semantic correctness, historical resolvability, non-destructive integrity. Tier 1: coherent consistency, durability, auditability, recoverability, security/residency capability, provider/cloud independence and multi-region portability. Tier 2: operational simplicity, observability, evolvability, developer experience and cost efficiency. Tier 3: performance and scalability. The USD 500/month constraint may not weaken Tier 0/1. Prefer correctness, durability, history integrity and residency over latency, availability, throughput or convenience; prefer reversible choices.

## Validation coverage

Validate historical reads; merge/split/correction atomicity; stale basis; idempotency replay/conflict; region-loss durability; quorum loss; backup restore; reference non-reuse; AP read; Extent rejection; exact scope equality; read-after-ack freshness; Windows/macOS startup; budget; multi-cloud migration; and residency enforcement. Claude-derived synthetic record-size assumptions are not frozen.

## Open items and gate

CD-1 is CLOSED. CD-2 split-child locating-basis review is RESOLVED. OBS-06-H14-LIFETIME remains OPEN / NON-BLOCKING. Long-term archival, auth/privacy policy, Extent geometry, AP writes/lifecycle, Containment writes/currentness, richer scope equivalence, provider selection and technology selection remain TBD.

`PHASE 06A = HUMAN FROZEN`

`PHASE 06B LOGICAL ARCHITECTURE = HUMAN FROZEN`

CD-1 is CLOSED; CD-2 is RESOLVED; OBS-06-H14-LIFETIME is OPEN / NON-BLOCKING. Phase 06B logical architecture is Human Frozen; Phase 06C remains not yet authorized.
