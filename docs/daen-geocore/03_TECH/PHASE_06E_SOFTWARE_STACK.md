# DAEN Geo Core — Phase 06E Software Stack

## Gate Status

- `PHASE 06E SOFTWARE STACK = HUMAN FROZEN`
- `PHASE 06E INFRASTRUCTURE / DEPLOYMENT / COST = OPEN`
- `PHASE 06E OVERALL = IN PROGRESS`
- `PHASE 06F = NOT YET AUTHORIZED`

This is an internal software sub-gate. It selects no cloud provider, region, VM/container size, managed offering, evidence vendor, consensus product, or monthly infrastructure price, and resolves no protected Domain/API TBD.

## Frozen Software Choices

- Runtime: supported stable **CPython** minor, with exact patch pinned in project/deployment lockfiles; no Python-version-specific application semantics.
- HTTP: **FastAPI** at the transport boundary only; **Uvicorn** ASGI baseline. Domain modules do not import FastAPI.
- Validation: **Pydantic 2** and **pydantic-settings** for transport/configuration. Internal commands, Domain types, and persistence representations remain framework-independent and explicitly mapped.
- Primary database software family: **PostgreSQL 17**; exact patch deployment-pinned. PostgreSQL 18 is a future candidate. This selects software, not cloud, machine class, or HA topology.
- Database access: **psycopg 3** and **SQLAlchemy Core 2.x**; no ORM as Domain/persistence model; explicit transaction boundaries and repository/port mapping. Domain does not depend on either library.
- Migrations: **Alembic**, hand-reviewed, expand/contract, compatibility rollout window, forward-fix default, CI validation. Physical schema is not frozen.
- Jobs: **PostgreSQL-backed** initially; job idempotency, retry safety, duplicate safety, bounded retry, failure visibility. Scheduler and worker may share the application image. No external broker initially.
- Cache: **none initially**. Cache is never authority for identity, representation, MutationBasis, idempotency, or recovery evidence.
- Evidence: `EvidenceStore` infrastructure port with a strongly consistent conditional-create object-store backend class supporting create-if-absent, reliable immediate lookup, exact keys, permanent and expiring records, encryption, portability, and fail-closed integration. No vendor or region selected.
- Evidence lookup: stable opaque deterministic request lookup key; exact lookup, no raw identifier exposure, key-rotation survival, CD-1 lifetime reachability. Exact HMAC/encoding deferred.
- Recovery gate: structural external recovery-lineage gate: external lineage/control state → reconciliation → new Recovery Incarnation → basis validation → readiness. Provider identity is adapter concern.
- Spatial: no extension initially; PostGIS remains a candidate subject to the approved synthetic spike. Extent semantics unchanged.
- Observability: **OpenTelemetry** with OTLP, structured logs, traces, metrics, request/mutation correlation, and no restricted payload in telemetry. Backend SaaS is deferred.
- Logging: structured JSON, Python logging-compatible interface, correlation/trace IDs, mutation/request correlation, no default payload dump, no raw stable refs/client IDs in high-cardinality labels.
- Quality: **Ruff**, **Pyright strict**, **pytest**, **Hypothesis**. Transaction semantics require real PostgreSQL integration tests.
- Test layers: unit, Domain invariant, property, application, API contract, PostgreSQL integration, concurrency, crash/retry, recovery/evidence adapter contract, migration, and end-to-end smoke. Synthetic data only for concurrency/recovery/spatial technology tests.
- Packaging: `pyproject.toml`, reproducible lockfile, hashes where supported, runtime/dev groups, dependency and security scanning.
- Container: OCI/Docker, Linux Debian-slim class, non-root, immutable commit/digest tags, one application image with API and worker entrypoints, no Kubernetes dependency.
- Local development: **Docker Compose** on Windows and macOS, one-command startup equivalent to `docker compose up`, with application/API/worker, PostgreSQL 17, local EvidenceStore-compatible adapter, migrations, and no production/restricted data or credentials.
- CI: **GitHub Actions** running lint, format, strict type, unit/property/API/contract tests, PostgreSQL integration, concurrency, migration validation, container build, dependency/secret/image scans.

## Module and Source Boundaries

`Transport → Application → Domain / Module APIs → Ports → Infrastructure Adapters`

Each module owns write repositories; cross-module direct repository access is forbidden; orchestration coordinates transactions; typed foreign references may cross boundaries; infrastructure implements ports. Domain depends on none of FastAPI, Pydantic DTOs, SQLAlchemy, psycopg, cloud SDKs, evidence SDKs, or telemetry backend SDKs.

Recommended implementation layout (not Domain semantics):

`src/daen_geocore/{transport/http,application/{operations,query,ingestion,jobs},domain/{identity,assertions,representation,access,containment},ports/{persistence,evidence,clock,policy,observability},infrastructure/{postgres,evidence,telemetry,runtime}}`

## Software Stack Summary

| Area | Frozen baseline |
|---|---|
| Runtime | CPython |
| HTTP | FastAPI + Uvicorn |
| Validation | Pydantic 2 + pydantic-settings |
| Database | PostgreSQL 17 |
| Access | psycopg 3 + SQLAlchemy Core 2.x |
| Migrations | Alembic |
| Jobs | PostgreSQL-backed |
| Cache | None |
| Evidence | EvidenceStore port + conditional-create object-store class |
| Spatial | No extension initially |
| Instrumentation | OpenTelemetry |
| Quality | Ruff + Pyright strict |
| Tests | pytest + Hypothesis + PostgreSQL integration |
| Packaging | OCI/Docker |
| Local | Docker Compose |
| CI | GitHub Actions |

## Explicitly Deferred

Cloud/provider and region, managed database, compute sizes, runtime platform, load balancer, network/NAT/endpoints, evidence provider and region, cross-border decision, monthly cost, telemetry/error-monitoring SaaS, PostGIS activation, Multi-AZ, distributed database, consensus product, and infrastructure closure remain open.

All existing protected Domain/API TBDs remain unresolved, including same-Place/dedup, source ranking, selection authority, survivor/withdrawal policy, H14 lifetime, AP/Containment writes, Extent semantics, richer scope equivalence, auth/privacy, locating-basis adequacy, T2 Current Representation effect, and issued-but-lost reference presentation.

## Preserved Architecture Constraints

The stack must preserve the relational transactional primary-store class, one initial primary authoritative store, local transactional commit, independent non-reuse/recovery durability, fail-closed evidence policy, frozen reference/idempotency/recovery semantics, and future multi-region evolution.
