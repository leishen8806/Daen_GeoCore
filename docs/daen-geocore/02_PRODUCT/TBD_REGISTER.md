# Phase 02 TBD Register

These items are intentionally unresolved. They must not be silently decided in a later PRD, model, API or implementation document.

| Item | Deferred to | Reason |
|---|---|---|
| Meaning of “same Place” | Phase 03 Domain Model | Identity continuity intent is frozen; equivalence semantics are not |
| GeoID encoding and generation | Phase 03 Domain Model / Phase 06 Architecture | Avoid premature identity implementation |
| Split, relocation, rebuild and reopening semantics | Phase 03 Domain Model | Lifecycle meaning is unresolved |
| Place taxonomy and identity boundaries | Phase 03 Domain Model | Minimum Place definition is sufficient for Phase 02 |
| Address normalization and administrative structure | Phase 03 Domain Model | No field or schema design in this phase |
| Access Point taxonomy | Phase 03 Domain Model | Entrance and other access meanings require explicit boundaries |
| Boundary and geofence representation | Phase 03 Domain Model | No geometry or storage design in this phase |
| Route entry criteria and implementation | Phase 04 M1 / Phase 06 Architecture | Route is a candidate capability |
| Location Correction authority and workflow | Later product and domain design | Constitution freezes the principle only |
| Provider selection and integration | Phase 06 Architecture / later evaluation | No provider is selected |
| API and SDK contracts | Phase 05 API | Contract principle is frozen; endpoints are not |
| M1 business scenario and acceptance result | Phase 04 M1 PRD | No feature list is defined in Phase 02 |
| First customer and payer | Future Consumer Validation Phase | No market evidence in the current baseline |
| Data licensing, coverage and update operation | M1 validation / later operations design | Source and governance evidence is missing |
| Quality thresholds and confidence semantics | Phase 03 Domain Model / M1 validation | Principle is frozen; measurements are not |
| Service-level expectations | Later product and technical design | No operating commitment is established |
| Trademark, language, domain and account verification | Brand Strategy | Not a Product Constitution decision |

## Phase 03 additions

| Item | Deferred to | Reason |
|---|---|---|
| Meaning of same Place | Later identity policy | Locus continuity is frozen; equivalence algorithm is not |
| GeoID format and generation algorithm | Later model and architecture | Scope is frozen; encoding is not |
| Area model and identity | Later geographic concept decision | Area is not Place |
| Street and network objects | Later domain model | Not needed for the Phase 03 minimum model |
| Access Point public identity or namespace | Later domain and API design | Internal reference is sufficient for this phase |
| Independent Extent identity | Later domain model | Extent has no Phase 03 GeoID |
| Containment taxonomy | Later domain model | Only minimal Place contains Place is frozen |
| Multi-parent containment | Later domain model | Relationship complexity is deferred |
| Demolition and rebuild identity policy | Later identity policy | No default same-Place rule |
| Merge survivor selection | Later governance policy | Survivor choice is not frozen |
| Correction authority | Later product and domain design | Principle is frozen; authority is not |
| Legal/privacy removal workflow | Later governance and technical design | Controlled exception is allowed, details are not |
| Data Quality dimensions and numeric scales | Later model and validation | Quality is cross-cutting but unquantified |
| Source trust ranking and conflict resolution | Later governance | No ranking is frozen |
| Temporal state-as-of queries | Phase 05 API / Phase 06 architecture | Supersession is retained; query contract is deferred |
| Route capability | Later product and architecture review | Route remains `CANDIDATE` |
| Provider mapping policy and provider taxonomy | Later architecture | Provider independence is frozen, mapping is not |
| API, database and architecture | Later phases | Explicitly excluded from Phase 03 |
| M1 scenario and acceptance | Phase 04 M1 PRD | No M1 feature list is defined |

## Phase 04 M1 additions

| Item | Deferred to | Reason |
|---|---|---|
| Execution medium | Later controlled execution decision | Phase 04 must not select technology or implementation medium |
| Synthetic-mark recording mechanism | M1 execution preparation | Synthetic cases must be clearly marked; recording mechanism is not frozen |
| Actual corpus Place selection | M1 corpus preparation | Humans select actual public Places later; this definition uses slots only |
| GeoID format | Later domain and architecture work | M1 validates semantics, not identifier encoding |
| Access Point handle | Later domain and API design | M1 validates modelability, not handle format |
| Merge survivor policy | Later governance policy | M1 tests both survivor directions without selecting a policy |
| Correction authority | Later governance policy | M1 tests correction semantics, not authority assignment |
| Quality scales | Later quality policy | `unknown` is valid for M1; numeric scales are not frozen |
| Source trust ranking | Later governance policy | M1 tests attribution, not a ranking system |
| Numeric tolerances | Later validation design | No numeric tolerance is justified by the frozen M1 definition |

## Future Consumer Validation Phase

Status: `Future Consumer Validation Phase — TBD`

This future phase must eventually define:

- confirmed real consumer;
- real location-dependent workflow;
- location-data context;
- external integration boundary;
- adoption evidence;
- operational-value evidence;
- willingness-to-adopt evidence;
- willingness-to-pay evidence where relevant;
- GO / ITERATE / STOP criteria.

No phase number or design is assigned here.

## Constitution amendment dependency

`RESOLVED — GeoID resolvability is extended from closure/merge to split/withdrawal.`

The controlled Product Constitution revision is recorded in `GEO_CORE_PRODUCT_CONSTITUTION.md` and confirmed in `DECISION_LOG.md`.

Each unresolved item remains `TBD` until the relevant phase produces evidence and a reviewable decision.
