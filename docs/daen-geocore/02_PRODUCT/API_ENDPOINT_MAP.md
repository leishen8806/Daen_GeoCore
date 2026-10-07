# DAEN Geo Core — Phase 05E Endpoint Map

## Status

`PHASE 05E ENDPOINT MAP = HUMAN FROZEN`

Major path: `/v1`. Action routing uses `/actions/{verb}`. This map contains exactly 18 canonical endpoints: 7 reads and 11 mutations. No aliases are defined.

| Method / operation | Idempotency-Key | MutationBasisToken | Expected success |
|---|---|---|---|
| GET `/v1/places/{placeRef}` | No | n/a | 200 |
| GET `/v1/places/{placeRef}/source-assertions` | No | n/a | 200 |
| GET `/v1/places/{placeRef}/access-points` | No | n/a | 200 |
| GET `/v1/places/{placeRef}/selections` | No | n/a | 200 |
| GET `/v1/places/{placeRef}/containment` | No | n/a | 200 |
| GET `/v1/source-assertions/{sourceAssertionRef}` | No | n/a | 200 |
| GET `/v1/access-points/{accessPointRef}` | No | n/a | 200 |
| POST `/v1/source-assertions` (create) | Yes | No | 201 |
| POST `/v1/source-assertions/{sourceAssertionRef}/actions/supersede` | Yes | Yes | 201 |
| POST `/v1/source-assertions/{sourceAssertionRef}/actions/correct` | Yes | Yes | 201 |
| POST `/v1/source-assertions/{sourceAssertionRef}/actions/withdraw` (T2) | Yes | No mandatory basis | 200 |
| POST `/v1/places/{placeRef}/selections` (add) | Yes | Yes | 201 |
| POST `/v1/places/{placeRef}/selections/{selectionRef}/actions/replace` | Yes | Yes | 201 |
| POST `/v1/places/actions/merge` | Yes | Yes | 200 |
| POST `/v1/places/{placeRef}/actions/split-mis-conflation` | Yes | Yes | 201 |
| POST `/v1/places/{placeRef}/actions/split-true-division` | Yes | Yes | 201 |
| POST `/v1/places/{placeRef}/actions/close` | Yes | Yes | 200 |
| POST `/v1/places/{placeRef}/actions/withdraw` (T1) | Yes | Yes | 200 |

## Forbidden/deferred routes

No generic Place create; AP writes; containment writes; direct Extent writes; generic relationship, Resolution Link or Succession creation; merge reversal; reopen; un-withdraw; material-history DELETE; search/matching/reverse-geocode/provider lookup.

Every material POST mutation requires `Idempotency-Key`. `/actions/` is an HTTP routing literal only and imposes no Domain or reference-token semantics; no token restriction or reserved value is defined. `/v1` freezes major-version path placement only, not compatibility, deprecation, sunset or negotiation policy. GeoID and opaque references carry no API-version semantics.

Phase 05 overall remains `NOT YET FINAL-GATE DECIDED`. This map does not define OpenAPI, JSON Schema, database schema or architecture.
