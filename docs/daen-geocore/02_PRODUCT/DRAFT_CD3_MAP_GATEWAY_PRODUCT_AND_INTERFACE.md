# DAEN Geo Core — CD-3 Map Gateway Product and Interface

## Status

- `CD-3 R1 SCOPE = HUMAN FROZEN / IMPLEMENTATION NOT YET AUTHORIZED`
- Only the bounded R1 scope amendment is frozen; WP2+ implementation details remain gated.
- The amendment changes no Constitution, Domain Model, or frozen Phase-05/06 semantics.

## 1. Purpose and product position

CD-3 is a proposed transport/integration gateway for two internal needs:

- microfinance address-to-coordinate and coordinate-to-address conversion;
- Dr.life+ map use.

The gateway is a replaceable provider adapter. Google is the proposed first
adapter, subject to the gates below. Provider answers are transient answers;
they are not automatically Source Assertions, Current Representation, identity
evidence, locating-basis decisions, or GeoIDs.

Business facts, loan notes, customer profiles, and credit decisions remain in
the consuming business systems. Geo Core does not become a lending system.

## 2. Frozen boundaries that this draft must respect

Phase 05 has exactly 18 frozen canonical `/v1` endpoints. R1 authorizes a
separate gateway surface:

`/gateway/v1`

This surface is not added to the Phase 05 endpoint map, is not a 19th/20th/21st
Phase-05 endpoint, is not an alias of `/v1`, and is not a Geo Core Domain
mutation endpoint. It does not change `/v1` semantics and is transport/
integration capability, not new Geo Core identity semantics.

The gateway must not require Merge, Split, Resolution Link, Succession, or
protected TBD resolution. Core implementation may continue independently.

## 3. Draft V1 gateway operations

Only these operations are proposed for the first release:

- `POST /gateway/v1/geocode`
- `POST /gateway/v1/reverse-geocode`
- `GET /gateway/v1/status`

Autocomplete, Place Details, routing, distance, directions, search, matching,
deduplication, tiles proxy, generic provider lookup, and any GeoID creation
endpoint are deferred candidates and are not in this draft V1 scope.

### 3.1 Geocode request and response sketch

```json
{
  "address": {"text": "synthetic address"},
  "regionCode": "KH",
  "languageCode": "km",
  "consumerPurposeCode": "bounded-code"
}
```

The response may expose a request ID, provider identifier, transient provider
results, provider address/name/coordinate, provider precision metadata, and
display requirements. Exact wire fields remain open for WP2.

`ZERO_RESULTS` is an empty result response. The gateway never invents a
coordinate or address.

Reverse geocode accepts finite latitude/longitude in the request body. Personal
location data is never placed in a URL or query string.

`GET /gateway/v1/status` is recommended as an authenticated/internal or
authorized-consumer coarse status endpoint. Exact authentication and exposure
remain OPEN. It must not expose API key state, billing details, raw quota
account data, or secret identifiers.

## 4. Consumer purpose

The field is `consumerPurposeCode`, not unrestricted caller prose. It must be a
bounded agreed code or constrained token suitable for audit and usage
classification. It must not contain names, addresses, loan notes, customer
profiles, or arbitrary text. The exact vocabulary remains OPEN until WP10.

## 5. Retention and telemetry

CD-3 V1 contains **NO cache implementation**. Phase 06E freezes `Cache: none
initially`. WP8 is only a Future Cache Decision Package that may research legal
allowance, retention windows, purge requirements, and an architecture
amendment. It must not build cache code, cache fields, a cache adapter, or a
purge job in V1.

Provider content, formatted addresses, coordinates, names, and raw customer
addresses are not retained by the gateway by default. A later legal and Human
decision is required before any durable retention.

Logs, traces, and metrics may contain only bounded non-sensitive metadata:

- gateway request ID;
- operation;
- bounded consumer identifier;
- provider identifier;
- result/error class;
- latency;
- retry/circuit state;
- bounded quota telemetry.

They must not contain raw addresses, coordinates, formatted provider content,
normalized addresses, or deterministic address/query hashes. No hash is treated
as making location data non-sensitive.

## 6. Provider authority and open gaps

Provider-returned address, coordinate, name, and provider precision metadata are
transient gateway answers. They are not automatically persisted, promoted to
Source Assertions, selected as Current Representation, used as a locating
basis, turned into a GeoID, Resolution Link, or Succession.

### Q2 — provider Place ID

`Q2 = OPEN`. WP7 must research the Domain Model, Source Assertion contracts,
and open typed-value model before any durable provider-reference linkage. A
provider Place ID is not a DAEN reference and no new endpoint is authorized.

### Q3 — new address to GeoID

`Q3 = OPEN`. CD-1 is the existing internal provisioning capability. A valid
Place birth requires a locating basis. The exact consumer/gateway flow remains
a decision task. No automatic geocode-result-to-GeoID behavior is authorized.

## 7. Frozen statement scope limits

R1 records bounded exceptions to the Phase-05 non-scope for provider
orchestration and consumer-map integration only through this separate gateway
surface. The exact Place resolution contract remains exact GeoID resolution,
not search, provider lookup, reverse geocoding, matching, or ambiguity
resolution. The Phase 06B anti-module rule is unchanged: the authorized
integration packages own no identity, matching, resolver, Source Assertion,
Current Representation, MutationBasis, idempotency, EvidenceStore, or
selection authority.

## 8. Gates and inputs

| ID | Gate / input | Owner | Status |
|---|---|---|---|
| L1 | Google terms for caching, storage, and lending use | Legal | OPEN |
| L2 | Business-confirmed provider result retention | Legal | OPEN |
| P1 | Third-party/cross-border processing of customer addresses | Compliance | OPEN |
| P2 | Telemetry/logging policy | Compliance + Human | OPEN |
| S1 | Production outbound HTTP client dependency | Human + Final Decision Layer | OPEN |
| T1 | Google as first gateway provider adapter | Final Decision Layer | OPEN |
| C1 | Provider cost in the 06E infrastructure/budget gate | Final Decision Layer | OPEN |

WP4 Google adapter implementation cannot start until S1 is closed and the
relevant legal, privacy, scope, and review gates are accepted.

Microfinance inputs required in WP10: forward daily volume and peak QPS,
reverse daily volume and peak QPS, whether original addresses must be retained,
retention system, and retention duration. Dr.life+ inputs: platform, map
scenarios, expected DAU, map calls/day, and whether selected locations must
eventually resolve to DAEN GeoID. Missing numbers remain OPEN.

## 9. Work packages

Exactly twelve packages are proposed:

| ID | Package |
|---|---|
| WP0 | Legal / compliance / Human gates |
| WP1 | CD-3 product and architecture scope amendment |
| WP2 | `/gateway/v1` contract-first OpenAPI |
| WP3 | Provider-neutral `GeocodingProvider` port/value types |
| WP4 | Google adapter, only after S1 and relevant gates |
| WP5 | Gateway application use cases, observability, rate-limit hook |
| WP6 | Gateway HTTP transport |
| WP7 | Provider Place ID and new-address-to-GeoID research |
| WP8 | Future Cache Decision Package; no V1 cache code |
| WP9 | Privacy, failure-isolation, architecture, and CI hardening |
| WP10 | Consumer clarification |
| WP11 | Infrastructure, deployment, cost, and dependency addendum |

Claude review gates are recorded separately and are not work packages.

## 10. Review gates

- `R0 — CD-3 Draft Conformance Review`
- `R1 — Scope Amendment Review`
- `R2 — Contract + Port Review`
- `R3 — Google Adapter Review`
- `R4 — Gateway Implementation Review`
- `R5 — Launch Gate`

No gate authorizes Phase 06F. Each gate requires a named commit and returns
PASS or ITERATE.

## 11. Sequencing recommendation

Immediately after R0, WP0, WP7, WP8 research, and WP10 may proceed. After R1,
WP2 and WP3 may proceed. After R2, WP5 may use a fake/stub provider and WP9 may
begin incrementally. WP4 requires R2, S1 CLOSED, and T1 CLOSED; it uses only
synthetic or recorded fixtures during implementation. WP6 requires accepted
WP2 and WP5. WP9 completes after WP6, while WP11 runs in parallel and closes
deployment/cost items before R5.

CD-3 must not alter frozen `/v1`, delay core mutations or reads, require
Merge/Split, or resolve protected TBDs.

## 12. Gateway error contract and launch boundary

WP2 will define a separate `CD-3 Gateway Error Contract`. The frozen
Phase-05 `API_ERROR_CONTRACT.md` remains unchanged and its HTTP mappings do
not automatically govern `/gateway/v1`. Proposed 429/502/503/504, provider
timeout, quota, and credential failures must be specified in WP2 and reviewed
at R2.

R5 is only the `CD-3 Launch Gate`; it does not close Phase 06E, authorize
Phase 06F, decide unrelated infrastructure, or resolve protected TBDs.

## 13. Protected items

TBD_REGISTER.md is the authoritative complete protected registry. Relevant
examples that remain unresolved include provider selection outside T1, same-
Place/deduplication, source ranking, selection authority, survivor and
withdrawal policy, H14 lifetime, richer scope equivalence, temporal/as-of,
Access Point/Containment writes, Extent semantics, auth/privacy, locating-basis
adequacy, T2 Current Representation effect, and issued-but-lost reference
presentation.
