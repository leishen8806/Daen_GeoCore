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
| Execution medium | Resolved in Phase 04B-1 | Markdown + CSV fixture medium; checker runtime remains TBD |
| Synthetic-mark recording mechanism | Resolved in Phase 04B-1 | Every future state-ledger entry carries an explicit real/public or synthetic mark |
| Actual corpus Place selection | Resolved in Phase 04C | Exact P01–P20 corpus is pre-registered; no GeoIDs or execution results are created |
| Scenario D evaluation of frozen P04 field evidence | PENDING M1 EXECUTION | P04 field evidence already exists and is frozen; M1 must evaluate it against the Access Point model |
| P13 correct coordinate | Later validation and governance | Public sources conflict; pre-registration does not select the correct coordinate |
| GeoID format | Later domain and architecture work | M1 validates semantics, not identifier encoding |
| Access Point handle | Later domain and API design | M1 validates modelability, not handle format |
| Merge survivor policy | Later governance policy | M1 tests both survivor directions without selecting a policy |
| Correction authority | Later governance policy | M1 tests correction semantics, not authority assignment |
| Quality scales | Later quality policy | `unknown` is valid for M1; numeric scales are not frozen |
| Source trust ranking | Later governance policy | M1 tests attribution, not a ranking system |
| Numeric tolerances | Later validation design | No numeric tolerance is justified by the frozen M1 definition |
| Checker runtime | Resolved in Phase 04B-2 | Python 3 standard library only; checker remains disposable |

## Phase 04D Scenario A review additions

| Item | Status / deferred to | Reason |
|---|---|---|
| Representation selection scope wording | Resolved prospectively in Phase 04D | Same-Place, represented fact/purpose and explicitly equivalent scope are required for ordinary selection supersession |
| Cross-scope migration policy | Later representation policy | General migration across language or other scopes is not defined |
| Selection scope encoding | Later validation medium / architecture | Scope representation and algorithms remain deferred |
| Selection attribution convention | M1 convention recorded; exact production model deferred | Operator/step attribution must remain distinct from assertion provenance; no new entity or column is introduced |
| Scenario C/F supersession behavior | Scenario C controlled same-scope positive replacement accepted; Scenario F remains unexecuted | Cross-scope behavior, production algorithms and full correction workflow remain deferred |
| Exact source-specific attribution for RUN-A-02 strings | Evidence limitation retained | Frozen memo support does not establish exact claim-to-URL attribution |

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

| Source Assertion subject reassociation / cross-subject supersession semantics | Phase 05 API Definition / later domain-policy clarification | RUN-H-01:F1 demonstrates one accepted fixture interpretation, but general cross-subject supersession semantics are not frozen. This is a narrow TBD, not a production requirement already decided. |

| Withdrawal target scope / Place-GeoID versus historical-record withdrawal semantics | Phase 05 API Definition / later domain-policy clarification | RESOLVED FOR M1 DOMAIN SEMANTICS: T1 Place identity/record withdrawal and T2 historical reference/Source Assertion withdrawal are distinct. Lifecycle taxonomy, authority/removal workflow and API representation remain TBD. |


## Phase 05 API Definition Carry-Forward Guardrails

The following remain unresolved and MUST NOT be silently frozen as settled domain policy by API Definition:

- cross-subject Source Assertion reassociation / supersession;
- lifecycle taxonomy;
- demolition/rebuild identity policy;
- demolition → closure mapping;
- withdrawal authority;
- legal/privacy/security removal workflow;
- Extent history representation;
- containment currentness;
- selection authority / conflict rationale;
- merge survivor selection;
- Quality scales;
- source trust/ranking;
- temporal/as-of semantics;
- GeoID encoding;
- resolver implementation.

Withdrawal T1/T2 target scope is `RESOLVED FOR M1 DOMAIN SEMANTICS`; API representation remains unresolved.


## Phase 05A API-Exposure Decisions

Phase 05A freezes resource boundaries only. The following remain unresolved: Extent history; containment currentness; cross-subject supersession; selection authority; withdrawal authority; lifecycle taxonomy; reference format. API Definition MUST NOT silently freeze these as settled domain policy.


## Phase 05B Protected TBDs

GeoID encoding; serialized reference forms; canonical textual normalization; Resolution Link stored direction/type vocabulary; lifecycle taxonomy; demolition-to-closure; withdrawal authority/removal workflow; Access Point lifecycle; cross-subject assertion reassociation; selection authority; provider mapping; error codes/object; HTTP; database; cache; and version mechanics remain unresolved.


## Phase 05C Protected TBDs

Access Point as Source Assertion subject; AP location-fact backing/reference; AP Current Representation/ranking; AP lifecycle; assertion-kind and value-type vocabularies; scope encoding; selected-value derivation; selection authority; conflict resolution; Extent geometry/CRS/role/reference; public Source resource; Quality scale; source ranking; temporal/as-of semantics; expansion/filter/pagination; endpoint layout; mutations/idempotency/versioning remain unresolved.


## Phase 05D Protected TBDs

Generic Place creation; all AP public mutations; Containment write; AP backing/reference/correction/removal/lifecycle; merge reversal; un-withdrawal; reopening; authorization/approval; same-Place and survivor algorithms; GeoID generation; lifecycle enum; richer scope equivalence; selection authority; selected-value derivation; Extent geometry/write; HTTP/error codes; persistence; ETag/version implementation; transaction/locking; MutationRequestRef serialization; API version mechanics remain unresolved.


## Phase 05E Protected TBDs

Auth/privacy mechanics; OpenAPI field schemas; pagination/filter syntax; GeoID/reference encoding; MutationBasisToken transport; idempotency storage; database/transactions/cache; and all previously protected Domain TBDs remain unresolved.


## Phase 05 Final-Gate Round 1 Bounded Completion

Resolved at Phase 05 contract level: HTTP status-category mapping; Idempotency-Key transport role; client-global idempotency scope; 7-day minimum replay guarantee; endpoint per-operation basis/idempotency requirements; and exact explicit scope equality for Selection mutation.

Still unresolved: error-body JSON schema; authorization/privacy HTTP behavior; GeoID/reference encoding; MutationBasisToken transport; idempotency storage; scope encoding; richer scope equivalence; Extent geometry payload; and all existing Domain TBDs.


## Phase 05 Final-Gate Status

`PHASE 05 API DEFINITION = COMPLETE / GO`

Resolved at Phase 05: resource/API exposure boundary; typed-reference semantics; exact Place resolution; Source Assertion read/write semantics; Current Representation read/selection semantics; Access Point read-only public semantics; Extent read boundary and write gate; Correction intent; minimal Containment read contract; Provenance/Quality boundary; mutation/error semantics; idempotency/concurrency semantics; MutationBasisToken semantics; HTTP status categories; and 18 canonical endpoints.

All still-protected TBDs remain carried forward without semantic change.


## Phase 06 Technical Architecture Guardrails

Phase 06 may design around but must not decide protected Domain/API items: cross-subject reassociation; lifecycle taxonomy; demolition/rebuild and demolition→closure; withdrawal authority/removal; Extent semantics; containment currentness/multi-parent; selection authority; selected-value derivation; source ranking; Quality scale; merge survivor policy; same-Place algorithm; generic Place creation; AP write/lifecycle/subject semantics; temporal/as-of; richer scope equivalence; merge reversal/reopen/un-withdraw; auth/privacy semantics.

06A Human Freeze additionally requires explicit expected workload, expected growth, availability expectations, deployment region/data-residency constraints, budget/operational constraints, and team stack/operations capability. These assumptions must not be invented by the architecture agent.


## Phase 06A Frozen Requirements and CD-1 — Historical Status at 06A Freeze

Historical snapshot only. Superseded by the later CD-1 and CD-2 resolution records below. Current Phase 06 status is recorded in the Phase 06B Logical Architecture Status section.

`CD-1 — INTERNAL PLACE PROVISIONING CONTRACT MISSING` remains OPEN and blocks Phase 06B final freeze for ingestion architecture. Phase 06A also preserves unresolved long-term archival, auth/privacy policy, Extent geometry, AP writes/lifecycle, Containment writes/currentness, richer scope equivalence, provider selection and technology selection.

06A Human Freeze requires explicit workload, growth, availability, deployment region/data residency, budget/operations and team capability assumptions before 06A can reach Human Freeze; these must not be invented.


## CD-1 Resolution and Carry-Forward

Resolved: internal provisioning of an already-decided NEW PLACE.

Still deferred: public generic Place creation; same-Place/dedup/matching; identity authority/governance; all AP, Containment and Extent writes; CD-2 Split-child locating basis; and OBS-06-H14 lifetime interpretation.


## CD-2 Resolution and Phase 06B Gate

Resolved: CD-1 internal already-decided Place provisioning; CD-2 locating basis at birth for Split-created Places.

Still open: H14 lifetime after birth; same-Place/dedup; cross-subject supersession; locating-basis adequacy; identity/split authority; AP/Containment/Extent writes; and all other protected TBDs.


## Phase 06B Logical Architecture Status

`PHASE 06B = HUMAN FROZEN`

`CD-1 = CLOSED`

`CD-2 = RESOLVED`

`OBS-06-H14-LIFETIME = OPEN / NON-BLOCKING`

`PHASE 06C = NOT YET AUTHORIZED` Historical defect records remain unchanged.
