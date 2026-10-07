# DAEN Geo Core — Phase 05E Endpoint Map

## Status

`PHASE 05E ENDPOINT MAP = HUMAN FROZEN`

Major path: `/v1`. Action routing uses `/actions/{verb}`. This map contains exactly 18 canonical endpoints: 7 reads and 11 mutations. No aliases are defined.

| Method | Path | Class |
|---|---|---|
| GET | `/v1/places/{placeRef}` | read |
| GET | `/v1/places/{placeRef}/source-assertions` | read |
| GET | `/v1/places/{placeRef}/access-points` | read |
| GET | `/v1/places/{placeRef}/selections` | read |
| GET | `/v1/places/{placeRef}/containment` | read |
| GET | `/v1/source-assertions/{sourceAssertionRef}` | read |
| GET | `/v1/access-points/{accessPointRef}` | read |
| POST | `/v1/source-assertions` | mutation |
| POST | `/v1/source-assertions/{sourceAssertionRef}/actions/supersede` | mutation |
| POST | `/v1/source-assertions/{sourceAssertionRef}/actions/correct` | mutation |
| POST | `/v1/source-assertions/{sourceAssertionRef}/actions/withdraw` | mutation |
| POST | `/v1/places/{placeRef}/selections` | mutation |
| POST | `/v1/places/{placeRef}/selections/{selectionRef}/actions/replace` | mutation |
| POST | `/v1/places/actions/merge` | mutation |
| POST | `/v1/places/{placeRef}/actions/split-mis-conflation` | mutation |
| POST | `/v1/places/{placeRef}/actions/split-true-division` | mutation |
| POST | `/v1/places/{placeRef}/actions/close` | mutation |
| POST | `/v1/places/{placeRef}/actions/withdraw` | mutation |

## Forbidden/deferred routes

No generic Place create; AP writes; containment writes; direct Extent writes; generic relationship, Resolution Link or Succession creation; merge reversal; reopen; un-withdraw; material-history DELETE; search/matching/reverse-geocode/provider lookup.

Phase 05 overall remains `NOT YET FINAL-GATE DECIDED`. This map does not define OpenAPI, JSON Schema, database schema or architecture.
