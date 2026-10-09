# CD-3 Map Gateway Scope Amendment

## Status

`CD-3 MAP GATEWAY SCOPE AMENDMENT = HUMAN FROZEN`

Authority: Human + ChatGPT Final Decision Layer

R0 baseline: `fdbfd0cd572d58104c6e6b7f3224ae3ea4d9f70b`

This is a bounded transport/integration amendment. It authorizes no code,
provider persistence, Domain identity semantics, or Phase 06F work.

## Frozen gateway surface

Phase 05 retains exactly 18 canonical `/v1` endpoints. CD-3 authorizes the
separate `/gateway/v1` surface with exactly:

- `POST /gateway/v1/geocode`
- `POST /gateway/v1/reverse-geocode`
- `GET /gateway/v1/status`

These are not added to `API_ENDPOINT_MAP.md`, are not additional Phase-05
endpoints, are not `/v1` aliases, and are not Geo Core Domain mutation
endpoints. Existing `/v1` semantics remain unchanged.

## Frozen statement scope limits

The following frozen statements are scope-limited only by this bounded
exception; their original files are not rewritten:

- `API_SCOPE_AND_NON_SCOPE.md`: provider orchestration and consumer-map UI
  remain non-scope except for this gateway transport/integration capability.
- `API_ENDPOINT_MAP.md`: reverse geocoding and provider lookup remain outside
  the canonical `/v1` map; the three gateway operations remain separate.
- `API_PLACE_RESOLUTION_CONTRACT.md`: exact Place resolution remains exact
  GeoID resolution, not search, provider lookup, reverse geocoding, matching,
  or ambiguity resolution.
- `PHASE_06B_LOGICAL_ARCHITECTURE.md`: the anti-module rule remains in force;
  only the bounded integration packages below are authorized.

The Phase 06B anti-module rule remains in force; the
integration packages `transport/http/gateway`, `application/gateway`,
`ports/geocoding`, and `infrastructure/geocoding/<provider>` own no identity,
matching, resolver, Source Assertion, Current Representation, MutationBasis,
idempotency, EvidenceStore, or selection authority.

## Provider, cache, and telemetry boundaries

Provider address, name, coordinate, and precision/result metadata are transient
answers. They are not automatically Source Assertions, Current Representation,
GeoIDs, identity evidence, locating basis, Resolution Link, or Succession. No
automatic persistence or promotion is authorized.

CD-3 V1 implements **NO cache**. WP8 is research only. Until P2 closes,
telemetry excludes raw addresses, coordinates, formatted provider content,
normalized addresses, and deterministic address/query hashes. Allowed telemetry
is bounded operational metadata only. A hash is not treated as legal
anonymization.

`consumerPurposeCode` is bounded, non-sensitive caller classification with no
arbitrary prose, PII, addresses, names, loan notes, or customer profiles.
Vocabulary remains WP10 input; WP2 must define bounded length, character class,
and validation behavior.

## Gates and open decisions

- `S1 = OPEN`; Human owns it, ChatGPT/Final Decision Layer coordinates, and
  Claude independently reviews it. Closing requires a recorded Phase 06E
  bounded software dependency addendum. WP4 requires R2, S1 CLOSED, and T1
  CLOSED.
- `Q2 = OPEN`; provider Place ID durable linkage is not authorized.
- `Q3 = OPEN`; no automatic geocode-result-to-GeoID, Place creation,
  same-Place/deduplication, or locating-basis decision is authorized.
- `L1`, `L2`, `P1`, `P2`, `T1`, and `C1` remain open as recorded in the TBD
  Register.
- WP2 defines a separate CD-3 Gateway Error Contract. Phase-05 HTTP status
  mappings do not automatically govern `/gateway/v1`.
- R5 is only the CD-3 Launch Gate; it does not close Phase 06E or authorize
  Phase 06F.

`TBD_REGISTER.md` is the authoritative complete protected registry. This
amendment does not close same-Place/dedup, source ranking, selection authority,
survivor/withdrawal policy, H14 lifetime, richer scope equivalence,
temporal/as-of, AP/Containment writes, Extent semantics, auth/privacy,
locating-basis adequacy, T2 Current Representation effect, or
issued-but-lost-reference presentation.
