# Prompt for ChatGPT — CD-3 Map Gateway Work Assignment

## Status

`R1 SCOPE AMENDMENT RECORDED / IMPLEMENTATION PACKAGES REMAIN GATED`

R0 was FINAL ACCEPTED and R1 is HUMAN FROZEN. Only the bounded scope amendment
is frozen; implementation packages remain gated and this is not a Phase 06F
authorization.

## Summary

CD-3 proposes a separate `/gateway/v1` integration surface for geocode,
reverse-geocode, and coarse status. It does not alter the 18 frozen Phase 05
`/v1` endpoints or introduce Geo Core identity semantics. Provider answers are
transient and are not automatically Source Assertions, Current Representation,
locating basis, or GeoIDs.

Implementation project state:

- Repository: `E:\Daen_GeoCore`
- GitHub: `leishen8806/Daen_GeoCore`
- Accepted implementation baseline before CD-3: `72897e0dc1770fa439005960fc906cee0ac95062`
- CD-3 working branch: `feature/cd3-map-gateway`
- `phase/06-technical-architecture` is architecture history, not the active implementation branch.
- Step 13 is FINAL ACCEPTED; Steps 2–13 exist.
- Merge/Split, remaining reads, and core HTTP work remain separate later work.

## Gate Order

1. R0 verified these drafts against frozen references at `fdbfd0c`.
2. R1 freezes the bounded `/gateway/v1` scope amendment recorded separately.
3. WP0 and WP10 collect legal, privacy, dependency, and consumer inputs.
4. After R1, WP2 contract and WP3 provider-neutral port proceed to R2.
5. After R2, WP5 may proceed using a fake/stub provider and WP9 may begin incrementally.
6. WP4 proceeds separately only after R2, S1 CLOSED, and T1 CLOSED; R3 reviews WP4.
7. WP6 follows accepted WP2 + WP5; R4 reviews gateway application/transport implementation.
8. WP9 final hardening completes after WP6; WP11 continues in parallel and required launch/deployment/cost items close before R5.

Documentation review, Q2/Q3 research, WP8 cache research, and consumer
clarification may proceed in parallel after R0. After R1, WP2/WP3 may proceed;
WP5/WP9 wait for R2; WP4 waits for R2, S1 CLOSED, and T1 CLOSED. No step
authorizes Phase 06F.

## Work Packages

| ID | Goal | Owner | Scope amendment first? |
|---|---|---|---|
| WP0 | L1, L2, P1, P2, S1, T1, C1 gates | Human / ChatGPT / Claude review | Yes for implementation |
| WP1 | Product + architecture scope amendment | Human + ChatGPT | Yes |
| WP2 | Contract-first `/gateway/v1` OpenAPI and error mapping | Codex / Claude | R1 |
| WP3 | Provider-neutral port/value types | Codex / Claude | R1 |
| WP4 | Google adapter with bounded failure controls | Codex / Claude | R2 + S1 + T1 |
| WP5 | Gateway use cases, bounded telemetry, rate-limit hook | Codex / Claude | R2 |
| WP6 | Gateway HTTP transport | Codex / Claude | R2 |
| WP7 | Q2 provider Place ID and Q3 address-to-GeoID research | ChatGPT / Human | No code |
| WP8 | Future Cache Decision Package; no V1 cache code | ChatGPT / Human | Legal + R1 |
| WP9 | Privacy, failure-isolation, architecture, and CI hardening | Codex / Claude | R2 |
| WP10 | Microfinance and Dr.life+ consumer inputs | Human / ChatGPT | No code |
| WP11 | Infrastructure, deployment, cost, and dependency addendum | Human / ChatGPT | 06E gate |

Required WP10 inputs are daily and peak volume/QPS, raw-address retention
need/system/duration, platform, map scenarios, DAU, calls/day, and whether a
selected location must resolve to GeoID. Do not invent values.

### S1 ownership

Accountable owner: **Human**. Coordinator: **ChatGPT / Final Decision Layer**.
Independent reviewer: **Claude**. S1 closes only when a Phase 06E bounded
software dependency addendum is recorded. Legal and Compliance may be
consulted but are not S1 owners.

## Sequencing

Core implementation may continue independently. CD-3 must not alter frozen
`/v1`, delay core mutations/reads, require Merge/Split, or resolve protected
TBDs. WP5 may use a fake/stub provider after R2. WP4 waits separately for R2,
S1, and T1. WP6 follows accepted WP2 and WP5. The first release remains
exactly three gateway operations.

## Codex Prompts

Each prompt below is a separate bounded step. Before every step Codex MUST
verify: cwd `E:\Daen_GeoCore`; remote `git@github.com:leishen8806/Daen_GeoCore.git`;
the requested branch; exact supplied baseline; clean tree except explicitly
authorized files; required DAEN markers; and that this is not another project.
If any check fails, stop with `STOPPED — WRONG OR UNVERIFIED PROJECT`. Use
synthetic data only, never credentials or customer addresses.

### Codex WP2 — Contract

Baseline: the accepted CD-3 scope-amendment commit supplied by the Human after
R1. Read the two CD-3 drafts, `API_ENDPOINT_MAP.md`, `API_ERROR_CONTRACT.md`,
`API_SCOPE_AND_NON_SCOPE.md`, and Phase 06B/06E. Produce only the draft
OpenAPI/contract artifact for the three `/gateway/v1` operations. Keep
`consumerPurposeCode` bounded, no cache fields, no query hashes, no provider
content persistence, and no `/v1` changes. Add synthetic contract tests only.
Run format/lint/type/tests and stop if any frozen file or source boundary is
changed. Commit: `docs: define CD-3 gateway contract`.

### Codex WP3 — Provider Port

Baseline: the reviewed WP2 commit. Re-run identity checks. Read the CD-3
architecture draft and Phase 06B/06E. Add only provider-neutral port/value
types and unit tests; no Google SDK, outbound client, cache, persistence,
GeoID, Source Assertion, or HTTP route. Run strict checks. Commit:
`feat: add CD-3 provider port`.

### Codex WP4 — Google Adapter

Baseline: the reviewed WP3 commit and closed S1. Re-run identity checks. Read
the dependency decision and provider-port contract. Add only the Google adapter
with an approved production HTTP dependency, bounded timeouts/retries/circuit
behavior, secret indirection, explicit errors, and synthetic/recorded tests.
No live calls, cache, persistence, GeoID linkage, or `/v1` changes. Stop if S1
is not closed. Commit: `feat: add CD-3 Google gateway adapter`.

### Codex WP5 — Gateway Application

Baseline: insert the future exact commit for the accepted R2 contract/port
state here when this prompt is issued; do not use a WP4 baseline. Add only
geocode/reverse/status application use cases, bounded telemetry and rate-limit
hooks. Use a fake/stub `GeocodingProvider`; WP5 has no Google adapter
dependency, no production provider credentials, and no S1 dependency of its
own. Never log addresses, coordinates, provider content, normalized values, or
hashes. Do not persist provider answers. Commit:
`feat: add CD-3 gateway application`.

### Codex WP6 — Gateway Transport

Baseline: insert the future exact commit for the accepted WP2 contract and
WP5 application surface here when this prompt is issued; do not require WP4.
Add only `/gateway/v1` transport routes and DTO mapping for the three
operations. Do not touch frozen `/v1`, Domain,
mutation, migration, or provider semantics. Commit:
`feat: expose CD-3 gateway transport`.

### Codex WP9 — Hardening

Baseline: reviewed WP6 commit. Add only architecture-boundary, privacy-leak,
failure-isolation, dependency, and CI tests. Confirm no cache implementation,
query hash, unrestricted purpose field, or forbidden route. Commit:
`test: harden CD-3 gateway boundaries`.

## Review Gates

- **R0** — exact three-draft conformance review at the current branch commit.
- **R1** — Human scope-amendment review for `/gateway/v1`; no code yet.
- **R2** — contract and provider-port review at named commits.
- **R3** — Google adapter review, including S1 evidence and privacy controls.
- **R4** — gateway implementation review, limited to approved surface.
- **R5** — launch gate covering legal, privacy, cost, CI, and rollback evidence.

Claude returns PASS or ITERATE at each exact commit. No review authorizes
Phase 06F or silently resolves a protected TBD.

## Risks and Stop Conditions

- Google terms may prohibit proposed retention or lending use: stop WP4/WP5.
- Privacy or cross-border approval may fail: stop provider calls.
- S1 may not approve a production HTTP dependency: stop WP4.
- Quota, cost, vendor lock-in, secret exposure, or accidental provider-content
  retention: stop and return to the relevant gate.
- Any proposed cache, query hash, free-form purpose, `/v1` modification,
  GeoID creation, or Domain semantic expansion: stop immediately.

## Open Questions

- L1: What Google contract terms govern caching, storage, and lending use?
- L2: May a business-confirmed provider result be retained as its own fact?
- P1: Is third-party/cross-border address processing approved?
- P2: What telemetry policy is approved?
- S1: Which production outbound HTTP mechanism is approved?
- T1: Is Google the first provider adapter?
- C1: How is provider cost included in the open 06E infrastructure gate?
- Q2: Can provider Place ID fit the frozen Source Assertion value model?
- Q3: What exact consumer flow obtains a GeoID for a new address?
- What authentication/exposure model is approved for status?

## R1 Clarifications

WP2 must define a separate `CD-3 Gateway Error Contract`; the Phase-05 HTTP
status mapping does not automatically govern `/gateway/v1`. R1 freezes no
provider Place ID linkage, no new-address-to-GeoID flow, no automatic Place
creation, no matching/deduplication, and no locating-basis decision.

The complete protected registry is `TBD_REGISTER.md`; this prompt only repeats
directly relevant examples. R1 also records that Step 13 was accepted by the
Human + ChatGPT Final Decision Layer at baseline
`72897e0dc1770fa439005960fc906cee0ac95062`; that acceptance record is external
to repository governance files at the R1 baseline.

R5 is only the CD-3 Launch Gate. It does not close Phase 06E or authorize 06F.

## Recommendation

Proceed with WP0, WP7, WP8 research, WP10, and the named R2/R3/R4/R5 gates.
Keep each implementation package blocked until its explicit gate is accepted.

CD-3 R1 SCOPE AMENDMENT RECORDED — IMPLEMENTATION PACKAGES REMAIN GATED
