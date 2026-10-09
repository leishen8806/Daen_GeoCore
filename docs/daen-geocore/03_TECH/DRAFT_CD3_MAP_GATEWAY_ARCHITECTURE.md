# DAEN Geo Core — CD-3 Map Gateway Architecture

## Status

- `CD-3 MAP GATEWAY ARCHITECTURE = DRAFT / REVIEW CANDIDATE / NOT FROZEN`
- This document is R0 review material. It is not approved, final, or human frozen.
- Phase 06F remains `NOT YET AUTHORIZED`.

## 1. Architectural stance

The gateway is a replaceable integration adapter around a provider. It owns no
authoritative Geo Core state and adds no Domain identity semantics. It must not
become a Search/Geocoding semantic module, matching engine, resolver, or generic
provider lookup layer.

The existing dependency direction remains:

`Transport → Facade → Application → Domain Owner → Ports → Infrastructure`

The gateway may validate requests, call a provider, normalize a transient
response envelope, emit bounded operational telemetry, and return explicit
provider errors. It may not bypass the mutation pipeline.

## 2. Proposed placement

| Layer | Draft responsibility |
|---|---|
| `transport/http/gateway` | `/gateway/v1` transport DTOs and routes |
| `application/gateway` | geocode, reverse-geocode, and status use cases |
| `ports/geocoding` | provider-neutral request, result, and failure types |
| `infrastructure/geocoding/google` | Google adapter, subject to S1 and legal gates |
| `observability` | bounded request, result, latency, retry, and quota telemetry |

There is **no `gateway_cache` implementation in CD-3 V1**. Phase 06E freezes
`Cache: none initially`; WP8 is research only.

The Domain, mutation runtime, identity history, Source Assertions, Selection,
and existing `/v1` transport do not import a provider SDK or outbound client.

## 3. Provider port

The proposed provider port exposes provider-neutral values for:

- forward geocode request;
- reverse geocode request;
- provider address/name/coordinate answer;
- provider precision/result metadata;
- provider reference as an external value only;
- typed provider failure classes.

Google field names and SDK/HTTP details remain inside the adapter. The port must
not create a Source Assertion, Current Representation, locating basis, GeoID,
Resolution Link, or Succession.

## 4. Google adapter dependency gate

The current project has `httpx` in development dependencies, not production
runtime dependencies. The Google adapter cannot start until:

`S1 — Production outbound HTTP client dependency`

is closed by the Human + Final Decision Layer, either by approving promotion or
addition of a production outbound HTTP client or by approving another runtime
mechanism. This is a bounded 06E software-stack addendum question; it does not
silently alter the frozen 06E stack.

The adapter must use bounded timeouts, bounded retries, circuit state, secret
handling, and explicit provider error mapping. No live provider call belongs in
CI; recorded or stubbed responses are required.

## 5. Data and authority

No new authoritative tables are proposed. Provider responses are transient and
are not automatically persisted. No automatic provider-result-to-GeoID or
provider-result-to-Source-Assertion path is authorized.

Q2 remains OPEN: research must establish whether a provider Place ID fits the
frozen Source Assertion typed-value model before durable linkage is designed.

Q3 remains OPEN: CD-1 is the existing internal provisioning capability, but the
consumer flow from a new address to a valid GeoID and locating basis remains a
decision task. H14 is not resolved here.

## 6. Privacy and telemetry

Customer addresses and coordinates are accepted in request bodies only. They
must not appear in URLs, query strings, logs, traces, metrics labels, or error
details.

Allowed bounded telemetry:

- gateway request ID;
- operation;
- bounded consumer identifier;
- provider identifier;
- result/error class;
- latency;
- retry/circuit state;
- bounded quota telemetry.

Telemetry must not contain raw address, coordinate, formatted provider
address, provider content, normalized address, or deterministic address/query
hash. A hash is not treated as de-identification.

The interface uses `consumerPurposeCode`, a bounded caller code. It must not
carry free-form names, addresses, loan notes, customer profiles, or prose.

## 7. Gateway surface boundary

The proposed `/gateway/v1` surface is separate from the 18 frozen canonical
Phase 05 `/v1` endpoints. It is not part of the frozen API map, does not change
`/v1`, and requires a bounded CD-3 scope amendment before implementation.
Status is `RECOMMENDED / DRAFT pending Human freeze`.

The proposed operations are only:

- `POST /gateway/v1/geocode`;
- `POST /gateway/v1/reverse-geocode`;
- `GET /gateway/v1/status`.

Status exposure/authentication remains OPEN and must be coarse; it must not
expose key state, billing, raw quota-account data, or secret identifiers.

## 8. Failure isolation

Provider outage, quota exhaustion, malformed response, credential failure, or
circuit-open state affects gateway operations only. It must not affect core
reads, mutations, recovery readiness, EvidenceStore, MutationBasis, or
idempotency authority. The gateway returns explicit errors and never substitutes
a guessed or expired provider answer.

## 9. Tests and controls

- unit validation and provider-error mapping;
- provider-port contract tests with synthetic or recorded responses;
- architecture dependency-boundary tests;
- timeout, quota, malformed-response, and circuit-open tests;
- telemetry privacy tests proving restricted payloads do not leak;
- no cache tests in V1 because no cache implementation exists;
- no production or restricted customer data in fixtures.

## 10. Work package architecture boundary

WP0 gates legal, privacy, dependency, and Human decisions. WP1 establishes the
scope amendment. WP2 defines the contract; WP3 defines the provider port; WP4
implements the Google adapter only after S1; WP5 adds application use cases;
WP6 adds transport; WP7 researches Q2/Q3; WP8 researches future cache only;
WP9 hardens privacy/failure/architecture/CI; WP10 collects consumer inputs; and
WP11 records infrastructure, deployment, cost, and dependency addenda.

Claude checkpoints are R0 through R5 and are not development packages.

## 11. Protected architecture boundaries

Do not introduce Resolution Link, Succession, Merge, Split, lifecycle states,
reopen/un-withdraw, generic Place creation, Source Assertion or Selection
mutation, Access Point/Containment writes, schema migration 0003, HTTP changes
to `/v1`, or Phase 06F work in this draft.
