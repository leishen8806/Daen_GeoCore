# Phase 02 Decision Log

This log records the human freeze decisions used to write the Product Constitution. It is a traceability record, not a substitute for the Constitution.

| Decision | Frozen result | Status |
|---|---|---|
| D1 DAEN hierarchy | DAEN is the brand and location-infrastructure umbrella; DAEN Geo Core is the core platform under DAEN | `CONFIRMED` |
| D2 identity scope | Phase 02 requires stable identity capability for Place; other geographic objects may gain independent identity later | `CONFIRMED` |
| D3 identity continuity | Identity is not reassigned to a different Place; historical references remain resolvable after closure or merge; same-Place, split and relocation semantics are deferred | `CONFIRMED` |
| D4 Route | Route remains a reusable capability candidate, not a mandatory core capability | `CANDIDATE` |
| D5 pickup and drop-off | Pickup and drop-off are business semantics and do not enter the Constitution | `CONFIRMED` |
| D6 Access | Access Point is the general concept; Entrance may later be a subtype or semantic | `CONFIRMED` |
| D7 scope admission | 4 MUST tests plus 1 SHOULD reusability test; two existing consumers are not required | `CONFIRMED` |
| D8 history | Preserve non-destructive history, with authorized legal, privacy, security or data-rights exceptions | `CONFIRMED` |
| D9 operational tools | Correction and data-operations tools may be first-party Geo Core components, but are not the complete value definition | `CONFIRMED` |
| D10 brand wording | DAEN and Geo Core are stable project terms; Khmer/Chinese expression and positioning retain their stated status | `CONFIRMED` |
| D11 rationale | Product rationale may precede market validation; the original requirement for real use and willingness to adopt or pay is preserved for a future Consumer Validation phase | `SUPERSEDED FOR CURRENT M1 SCOPE` |
| D12 canonical representation | Geo Core maintains the canonical DAEN representation of known facts; it does not claim perfect physical truth | `CONFIRMED` |

## Phase 03 Human Freeze Decisions

| Decision | Frozen result | Status |
|---|---|---|
| H1 Place | Place is a persistent, referable real-world locus; Place is WHERE and occupant/business is WHO | `CONFIRMED` |
| H2 same Place | Locus continuity governs identity; name, owner, tenant, address or provider change does not automatically create a new Place | `CONFIRMED` |
| H3 Area | Area is not Place; Areas are a future separate concept | `CONFIRMED` |
| H4 GeoID scope | GeoID identifies Place only in Phase 03 | `CONFIRMED` |
| H5 merge | Retire one identity, resolve to survivor, never reassign retired GeoID, preserve historical resolution | `CONFIRMED` |
| H6 split | Mis-conflation and true division use different identity outcomes; children do not silently inherit the old identity in true division | `CONFIRMED` |
| H7 relocation | Place does not move; occupants or businesses move between Places | `CONFIRMED` |
| H8 demolition and rebuild | No default same-Place rule | `TBD` |
| H9 Access Point | First-class object with internal reference; no Place GeoID; one Access Point may serve multiple Places | `CONFIRMED` |
| H10 representation terms | Source Assertion, Current DAEN Representation and Selected Coordinate are the preferred terms | `CONFIRMED` |
| H11 Extent | Extent is a Place spatial fact without independent GeoID; business policy zones are separate | `CONFIRMED` |
| H12 correction | Supersession chain with controlled removal exception; used GeoID is never reusable | `CONFIRMED` |
| H13 containment | Place may contain Place as a minimal relationship | `CONFIRMED` |
| H14 spatial anchoring | A valid Place needs at least one locating basis, but not necessarily a precise coordinate | `CONFIRMED` |
| H15 resolvability | GeoID remains resolvable after closure, merge, split and withdrawal | `CONFIRMED` |
| H16 terminology | Resolution Link and Succession remain; Phase 03 avoids Observation and Canonical Selection | `CONFIRMED` |
| H17 temporal history | Material supersession is retained; arbitrary as-of-time queries remain deferred | `CONFIRMED` |
| H18 business closure | Occupant/business operational status does not become Place lifecycle | `CONFIRMED` |
| H19 provenance scope | Persisted or externally exposed facts and decisions are attributable; ephemeral calculations need not create a permanent graph | `CONFIRMED` |

## Constitution amendment status

`RESOLVED — GeoID resolvability is extended from closure/merge to closure/merge/split/withdrawal.`

The controlled Product Constitution revision is recorded below.

## Constitution Amendment — GeoID Resolvability

**Decision:** GeoID resolvability is extended from closure / merge to closure, merge, split and withdrawal.

**Reason:** Phase 03 Domain Model identified that stable historical identity requires references to remain resolvable across split and withdrawn Place states.

**Status:** `CONFIRMED`

**Source:** `Phase 03 Human Freeze Decision H15`

## Phase 04 Human Freeze Decisions

| Decision | Frozen result | Status |
|---|---|---|
| D1 purpose | M1 validates conceptual model coherence and operability only; it makes no market, adoption or production claim | `CONFIRMED` |
| D2 dataset size | 20 initial Places; maximum 23 after split-created Places | `CONFIRMED` |
| D3 reviewer independence | Data Operator and Reviewer are separate roles; if independence is unavailable, record the specified validation limitation and do not block document creation | `CONFIRMED` |
| D4 dataset mix | Target approximately 12 real public Places and 8 clearly marked synthetic cases; no private-home or personal-location data | `CONFIRMED` |
| D5 field verification | Up to 5 public Places may be field-verified; not required for M1 freeze | `CONFIRMED` |
| D6 Access Point cases | At least 3 Places test Access Point != Selected Coordinate | `CONFIRMED` |
| D7 merge and split | Test both merge survivor directions without inventing a survivor policy; test mis-conflation and true division | `CONFIRMED` |
| D8 shared Access Point | At least one Access Point serves multiple Places | `CONFIRMED` |
| D9 containment | At least two containment examples; containment is the first scenario eligible to be cut if the timebox is exceeded | `CONFIRMED` |
| D10 friction log | Model Friction Log is a primary M1 validation instrument | `CONFIRMED` |
| D11 success gate | Use binary invariants B1–B11, scenarios A–J and friction-pattern rules; permit one rerun for documented execution error | `CONFIRMED` |
| D12 execution medium | Execution medium remains TBD and must not introduce a new domain concept | `TBD` |
| D13 surprise cases | Plan 3 surprise cases, preferably selected by the Reviewer | `CONFIRMED` |
| D14 timebox | Target 2 weeks; hard stop 3 weeks after corpus, scenarios and medium are ready | `CONFIRMED` |
| D15 authority | Frozen Phase 03 Domain Model wins over Phase 04 planning text; Phase 04 must not silently reopen Phase 03 | `CONFIRMED` |

## Constitution Amendment — Validation Layer Separation

**Status:** `CONFIRMED`

**Decision:** DAEN Geo Core formally separates Internal Model Validation from Future Consumer Validation. Current M1 is an Internal Geo Core Validation milestone and does not require or claim evidence of customer demand, adoption, real-workflow fit, willingness to adopt or willingness to pay. The original Phase 02 intent to validate real use, adoption and payment is preserved as a requirement for a future Consumer Validation phase.

**Reason:** Combining internal model validation and external market validation in one M1 would either block domain validation indefinitely or force the project to invent an unconfirmed consumer.

**Source:** `Phase 04 Human Constitutional Decision — Validation Layer Separation`

## Phase 04B Human Decisions — Validation Medium

| Decision | Frozen result | Status |
|---|---|---|
| Validation medium | Markdown for human judgment and evidence; CSV for corpus and logically append-only validation state | `CONFIRMED` |
| Disposable checker | A future disposable local checker is approved in principle; source code and runtime remain deferred | `CONFIRMED` |
| Known-bad fixtures | Known-bad Markdown specifications are required before checker implementation | `CONFIRMED` |
| Dedicated area | Validation artifacts live under `validation/m1/` | `CONFIRMED` |
| Synthetic marking | Every future state-ledger entry explicitly marks real/public or synthetic; synthetic assertions attached to real Places remain synthetic at entry level | `CONFIRMED` |
| Opaque local labels | Corpus labels such as P01–P20 are local labels and do not imply GeoID format | `CONFIRMED` |
| Snapshot / void / rerun | Execution errors are handled by void plus rerun; valid ledger history is logically append-only | `CONFIRMED` |
| No-specification rule | Validation fixtures MUST NOT become API, database, schema or architecture precedent | `CONFIRMED` |
| Evidence retention | Human evidence, execution records and friction references are retained for the validation run | `CONFIRMED` |
| Manual authority | Manual Domain Model review has authority over checker output | `CONFIRMED` |

## Phase 04B-2 Human Decisions — Disposable Checker

| Decision | Frozen result | Status |
|---|---|---|
| Checker runtime | Python 3 standard library only | `CONFIRMED` |
| Checker scope | Structural/mechanical validation only; no domain judgment | `CONFIRMED` |
| Self-test evidence | Known-good must pass and every known-bad fixture must trigger its intended rule | `CONFIRMED` |
| Domain ownership | Domain judgment remains human-owned | `CONFIRMED` |

## Phase 04C M1 Corpus Selection — CONFIRMED

| Decision | Frozen result | Status |
|---|---|---|
| Corpus composition | 12 real public Places and 8 explicitly synthetic cases | `CONFIRMED` |
| Approved corpus | P01–P20 are pre-registered exactly as listed in `validation/m1/corpus-register.csv` | `CONFIRMED` |
| Field-verification scope | P04 is the one mandatory real field case; P09, P10 and P11 are optional; P13 remains an unresolved public-source conflict with no M1 field requirement | `CONFIRMED` |
| P20 rationale | Former White Building is selected as the historical Place because public demolition evidence supports lifecycle testing; occupant/business closure is not substituted for Place closure | `CONFIRMED` |
| P09 rationale | Royal Phnom Penh Hospital is selected so P09 and the distinct Calmette coordinate-conflict case P13 remain separate real Places | `CONFIRMED` |
| Execution boundary | A–J expected outcomes, B1–B11, checker rules and frozen scenarios remain unchanged; no results, friction entries or GO decision are created | `CONFIRMED` |

## Phase 04C — Field Verification Scope Reduced

| Decision | Frozen result | Status |
|---|---|---|
| Field verification scope | M1 requires at least one real public Place with field-verified evidence that an Access Point can differ from a general Place reference / Selected Coordinate | `CONFIRMED` |
| Mandatory real field case | P04 — AEON Mall Phnom Penh; minimal public/reference location evidence, observed usable public Access Point, coordinate/map pin if available, and YES/NO/UNCERTAIN difference assessment | `CONFIRMED` |
| Optional field cases | P09, P10 and P11 remain valid public corpus Places; field verification is optional and not required for M1 | `CONFIRMED` |
| Synthetic Access cases | P05/P06 and the frozen synthetic or controlled Access Point cases continue to test model expressiveness without claiming real-world usefulness | `CONFIRMED` |
| P13 | Calmette remains `PUBLIC-SOURCE CONFLICT — UNRESOLVED`; no correct coordinate is forced and no field verification is required for M1 | `CONFIRMED` |
| Operational observation | Data Maintenance Friction may be recorded during M1; it is not a Domain Model invariant and does not automatically cause `RETURN TO DOMAIN MODEL` | `CONFIRMED` |

**Reason:** M1 needs one real-world anchor but must not assume routine location maintenance requires costly manual field verification.

## Phase 04D — Execution Roles

| Decision | Frozen result | Status |
|---|---|---|
| M1 execution roles | Codex is Data Operator; Claude is Independent Reviewer; human owner + ChatGPT are the final decision layer | `CONFIRMED FOR M1 VALIDATION` |

This is an M1 validation separation mechanism and does not establish permanent product governance.

## H20 — Current Representation Selection Scope Clarification

| Decision | Frozen result | Status |
|---|---|---|
| Selection scope and supersession | Representation-level supersession requires the same Place, represented fact or purpose, and explicitly equivalent scope; another language does not by itself invalidate an existing language scope; supporting Source Assertions remain retained | `CONFIRMED PROSPECTIVE CLARIFICATION` |
| RUN-A-02 relationship | This clarification does not repair historical RUN-A-02 evidence and does not expand its narrow Scenario A PASS scope; it is not empirically validated by adding the text | `RECORDED` |

Source: Controlled Scenario A review disposition issued with the RUN-A-02 independent review.

## Phase 04D — Scenario C Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-C-ACCEPT-01 Scenario C acceptance | RUN-C-01 is accepted as `PASS` for the controlled same-Place/fact/purpose/language replacement outcome only; F1–F6 remain non-blocking; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `77a3ec351c0120855b1569e06781813c7d163a34`; review excerpt and disposition are retained under `validation/m1/reviews/`.

## Phase 04D — Scenario D Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-D-ACCEPT-01 Scenario D acceptance | RUN-D-01 is accepted as `PASS` for the controlled Access Point separation outcome only; F1–F6 remain non-blocking; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `281d2f02b945519491376f64aa54afa23b6523a7`; review export and disposition are retained under `validation/m1/reviews/`. P04/F4 and E/F6 follow-ups remain bounded as recorded in the disposition.

## Phase 04D — Scenario B Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-B-ACCEPT-01 Scenario B acceptance | RUN-B-01 is accepted as `PASS` for the frozen Scenario B outcome only; F1–F7 remain recorded as non-blocking limitations; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `b77b87f75a759a62fe64f42ada4d1b0180cd61fc`; review export and disposition are retained under `validation/m1/reviews/`.

## Phase 04D — Scenario E Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-E-ACCEPT-01 Scenario E acceptance | RUN-E-01 is accepted as `PASS` for the frozen controlled synthetic shared-Access-Point outcome only; F1–F6 remain non-blocking; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `1388f7b33ac96352625b56ce0535c3cc740f2f6`; review export and disposition are retained under `validation/m1/reviews/`. The acceptance does not establish real RUPP/Hun Sen Library access, AP identity continuity, AP correction/lifecycle, Scenario G behavior or P04 Access Point resolution.

## Phase 04D — Scenario F Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-F-ACCEPT-01 Scenario F acceptance | RUN-F-01 is accepted as `PASS` for the frozen controlled Source Assertion correction outcome only; F1–F5 remain non-blocking; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `005a25f116e93d331920a0d922fc61cc58b8bbde`; input freeze `8d7ab92a515ad3bed899af35c15cb94227535f5e`; review export and disposition are retained under `validation/m1/reviews/`. This does not establish production correction authority, real-world truth, Current DAEN Representation behavior or general Succession taxonomy.

## Phase 04D — Scenario G Target Erratum

| Decision | Frozen result | Status |
|---|---|---|
| M1-G-ERRATUM-01 | Original G targets P08/P09 are defective for the Merge test; effective execution targets P15/P16 are approved prospectively. Original artifacts remain unchanged. This is a validation-design correction, not a Phase 03 Domain Model amendment. G has not executed or passed. | `CONFIRMED FOR M1 VALIDATION` |

Source: `validation/m1/errata/SCENARIO-G-TARGET-ERRATUM.md`.

## Phase 04D — Scenario G Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-G-ACCEPT-01 | RUN-G-01 is accepted as `PASS` for the controlled synthetic Merge outcome only; P15/P16 effective targets, both isolated survivor directions, explicit Resolution Link/Succession direction, retained history and no survivor policy are supported; F1–F5 remain non-blocking; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `424c15fad6a6f0a3aa58404d2daa1bf1e6bb3459`; input freeze `626556e86441836b00d356ee9cf7f9471b360541`; target erratum `eac2d7561a1b46096e2106e2201da3b7c6dd0788`. The original G erratum remains unchanged.

## Phase 04D — Scenario H Target Erratum

| Decision | Frozen result | Status |
|---|---|---|
| M1-H-ERRATUM-01 | Original H targets P10/P11 are defective for split testing; effective execution targets P17/P18 are approved prospectively. Original artifacts remain unchanged. This is a validation-design correction, not a Phase 03 Domain Model amendment. H has not executed or been accepted. | `CONFIRMED FOR M1 VALIDATION` |

Source: `validation/m1/errata/SCENARIO-H-TARGET-ERRATUM.md`.

## Conflict resolution

The earlier source material contained an organization-operations positioning. Phase 01 isolated it from the active Geo Core baseline. This Phase 02 Constitution keeps the location-infrastructure identity and does not import that historical positioning.

## Phase 04D — Scenario H Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-H-ACCEPT-01 Scenario H acceptance | RUN-H-01 is accepted as `PASS` for the controlled synthetic Split outcome only; P17/P18 effective targets, retained original/history identities, distinct resulting identities and historical resolution are supported; F1–F7 remain non-blocking; overall M1 decision remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `9bc78b883fbe026477634227614134ca2a122944`; input freeze `a0424803269f11805a46f5d2453b0c3fba90c44a`; target erratum `6b572bc5ba03f275d25a21f727515128326a7d73`; review export and disposition are retained under `validation/m1/reviews/`.

## Phase 04D — Scenario I Target Erratum

| Decision | Frozen result | Status |
|---|---|---|
| M1-I-ERRATUM-01 | Historical Scenario I targets P12/P13 conflict with later 04C corpus-role assignment. Effective targets are P20 for physical Place closure and P03 for historical-reference withdrawal. Original artifacts remain unchanged. This is a validation-design correction only and does not amend the Domain Model. Scenario I is not yet accepted. | `CONFIRMED FOR M1 VALIDATION` |

Source: `validation/m1/errata/SCENARIO-I-TARGET-ERRATUM.md`.

## Phase 04D — Scenario I Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-I-ACCEPT-01 Scenario I acceptance | RUN-I-01 is accepted as `PASS` for the controlled closure / historical-reference-withdrawal outcome only; Reading B is consciously accepted, P20 physical closure and P03 historical-reference withdrawal are supported, F1–F7 remain non-blocking, final B3 withdrawal coverage remains for the final gate, and overall M1 remains `NOT MADE` | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `b311f5aff4e3258f591b2d9ec86fc907e9c40cd2`; input freeze `67957e1067066ca7f4947eef5e23e3462fef87f9`; target erratum `13af031692b8f8e57085fc1ccd6c6ab39f2b87d8`; review export and disposition are retained under `validation/m1/reviews/`.

## Phase 04D — Scenario J Target / Fixture Erratum

| Decision | Frozen result | Status |
|---|---|---|
| M1-J-ERRATUM-01 | Historical J targets P18/P19 conflict with later corpus roles and incomplete P19 fixture. Effective positive fixtures are REAL P07→P08 and SYNTHETIC P19→FIX-ID-J-P19-CHILD; P19 occupant proposal is supplemental negative control; P18 is excluded from RUN-J-01. This is a validation-design correction only and does not amend the Domain Model. Scenario J is not yet accepted. | `CONFIRMED FOR M1 VALIDATION` |

Source: `validation/m1/errata/SCENARIO-J-TARGET-ERRATUM.md`.

## Phase 04D — Scenario J Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-J-ACCEPT-01 Scenario J acceptance | RUN-J-01 is accepted as `PASS` for the controlled minimal Containment outcome only; exactly two directional Place-to-Place relationships are accepted, P19 occupant proposal is supplemental negative control only, F1–F5 remain non-blocking, A–J scenario acceptance sequence is complete, and overall M1 remains `NOT MADE` pending Final Gate | `CONFIRMED FOR M1 VALIDATION` |

Evidence: `d1db291e11afd2082ce86bb97e6caedb467ad61c`; input freeze `0e47bdc6b9f7ee8ad447c0bc0c2da91ebca795f0`; target/fixture erratum `532332d00df38b237d214a39e5ee35f32038735f`; review export and disposition are retained under `validation/m1/reviews/`.

## Phase 04D — Reviewer-Selected Surprise Cases

| Decision | Frozen result | Status |
|---|---|---|
| M1-SURPRISE-FREEZE-01 | At baseline `75b3769264e8e35eec1d8cc595ed1b52144df489`, the independent Reviewer selected SURPRISE-01 (P05/P06 Extent overlap), SURPRISE-02 (P07/P08 containment × closure) and SURPRISE-03 (P13 conflicted selection). The cases create zero new Place identities and are frozen before operator execution. | `CONFIRMED FOR M1 VALIDATION` |


## Phase 04D — Bounded Completion Acceptance

| Decision | Frozen result | Status |
|---|---|---|
| M1-BOUNDED-COMPLETION-ACCEPT-01 | P04 real anchor accepted; three Reviewer-selected surprise cases accepted; surprise requirement satisfied; S01/S02/S03 model friction recorded as non-blocking; pattern-equivalence and capacity-accounting decisions recorded separately; overall M1 remains NOT MADE; Final Gate has NOT occurred. | CONFIRMED FOR M1 VALIDATION |
| M1-FRICTION-PATTERN-EQUIVALENCE-01 | Same pattern means a substantially equivalent missing semantic rule or ambiguity requiring substantially the same clarification or repair; broad category or shared TBD root alone is insufficient. Six specific groups currently have maximum repeated count 1. | CONFIRMED |
| M1-VALIDATION-CAPACITY-ACCOUNTING-01 | 20 initial Places / maximum 23 after split-created Places applies to registered corpus and isolated validation-world capacity. H exercises 20→23; J run-local child is not corpus P21; surprise cases create zero Places; P04 AP is not a Place. | CONFIRMED |


## Final Gate Round 1 — B3 Iteration Authorization

| Decision | Frozen result | Status |
|---|---|---|
| M1-FINAL-GATE-ROUND-1-ITERATE-01 | Baseline `69f56525d250d61deca3b67495f2e47ba866794d`; recommendation and Human Final Decision are ITERATE; sole blocker is B3 Place-GeoID withdrawal evidence/scope; no RETURN condition; one bounded synthetic T1 fixture is authorized. | CONFIRMED |


## B3 Withdrawal Target Clarification

| Decision | Frozen result | Status |
|---|---|---|
| M1-WITHDRAWAL-TARGET-CLARIFICATION-01 | Final Gate Round 1 exposed the B3 evidence gap. T1 Place identity/Place record withdrawal and T2 historical reference/Source Assertion withdrawal are distinct. Constitution and invariant 2 are unchanged; no lifecycle taxonomy is defined; one bounded synthetic T1 validation is authorized. | CONFIRMED FOR M1 VALIDATION |


## B3 Withdrawal Iteration Acceptance and Final-Gate Round 2 Scope

| Decision | Frozen result | Status |
|---|---|---|
| M1-B3-WITHDRAWAL-ACCEPT-01 | Authorized T1/T2 clarification accepted; RUN-B3-WITHDRAWAL-01 PASS; B3 PASS; I:F3 resolved prospectively for M1 domain semantics; no new fundamental concept; Final-Gate Round 2 authorized but not yet decided. | CONFIRMED |
| M1-FINAL-GATE-ROUND-2-SCOPE-01 | Round 2 reopens only B3, RUN-I-01:F3 / withdrawal target scope, and whether the bounded clarification creates a new blocking problem. All other Round-1 judgments, limitations, safe-to-defer findings and Phase-05 guardrails are inherited unchanged. | CONFIRMED |


## Final Gate Round 2 — M1 GO

| Decision | Frozen result | Status |
|---|---|---|
| M1-FINAL-GATE-ROUND-2-GO-01 | Round-2 recommendation GO accepted by the Human Final Decision Layer; B1–B11 all PASS; B3 closed after authorized bounded iteration; no falsification criterion triggered; no fundamental new core concept; no business dependency; provenance/Quality sufficiently understandable; M1 Internal Validation complete; Phase 05 API Definition authorized. | CONFIRMED |
| PHASE-04-M1-COMPLETE-01 | Phase 04 M1 Internal Validation is complete. Phase 03 Domain Model is stable enough to proceed to Phase 05 API Definition. This does not mean production ready, market validated, architecture frozen, API designed, or provider selected. | CONFIRMED |


## Phase 05A — Resource Model Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05A-RESOURCE-MODEL-FREEZE-01 | Phase 05A API scope and resource model are Human Frozen. No endpoints, OpenAPI, JSON Schema, database schema, architecture or provider selection is included. | CONFIRMED |
| HF-05A-01 | API Core is Place/GeoID, Source Assertion, Current DAEN Representation, Access Point, historical identity resolution, Provenance and Quality. | CONFIRMED |
| HF-05A-02 | Only Place has a GeoID; Source Assertion and Access Point use future opaque API references. | CONFIRMED |
| HF-05A-03 | Current DAEN Representation is Place-associated, not a top-level resource. | CONFIRMED |
| HF-05A-04 | Selected Coordinate is a selected fact/value, not an Access Point. | CONFIRMED |
| HF-05A-05 | Historical resolution uses NO SILENT SUBSTITUTION. | CONFIRMED |
| HF-05A-06 | T1/T2 withdrawal scope is exposed without deciding T2 effect on Current Representation. | CONFIRMED |
| HF-05A-07 | Same-subject supersession is guaranteed; cross-subject supersession remains deferred. | CONFIRMED |
| HF-05A-08 | Extent and Containment exposure remains read-only and guarded as documented. | CONFIRMED |
| HF-05A-09 | Provenance/Quality remain explicit boundaries; reference formats and endpoint layout are Phase 05B or later. | CONFIRMED |


## Phase 05B — Identifier and Resolution Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05B-IDENTIFIER-RESOLUTION-FREEZE-01 | Phase 05B identifier and resolution contracts are Human Frozen. Endpoints, OpenAPI, JSON Schema, database schema and architecture remain out of scope. | CONFIRMED |
| HF-05B-01 | GeoID is Place-only, DAEN-controlled, stable, immutable, opaque, provider-independent, non-reassignable/non-reusable and historically resolvable. | CONFIRMED |
| HF-05B-02 | PlaceRef is GeoID; SourceAssertionRef, AccessPointRef and SelectionRecordRef are typed opaque references; ResolutionRecordRef, CorrectionRecordRef and ContainmentRecordRef remain deferred. | CONFIRMED |
| HF-05B-03 | Reference types use logical namespaces distinct from serialized prefixes. | CONFIRMED |
| HF-05B-04 | Stable references never silently alias; superseded records remain inspectable. | CONFIRMED |
| HF-05B-05 | Retained relationship/history records preserve originally recorded references. | CONFIRMED |
| HF-05B-06 | Exact Place reads expose identity/resolution context plus optional content. | CONFIRMED |
| HF-05B-07 | Resolution envelope can express recognition, new-use standing, relationships, history and detail availability without frozen JSON fields. | CONFIRMED |
| HF-05B-08 | New-use standing is capability, not lifecycle enum. | CONFIRMED |
| HF-05B-09 | Historical resolution uses NO SILENT SUBSTITUTION and exact GeoID resolution is not search. | CONFIRMED |
| HF-05B-10 | Split, closure and T1/T2 withdrawal semantics follow the frozen bounded contracts. | CONFIRMED |
| HF-05B-11 | Resolution Link, caller-relative view and Succession remain distinct; stored direction/vocabulary remain TBD. | CONFIRMED |
| HF-05B-12 | Recognized historical/restricted identities are not reported as not found merely because they are non-current. | CONFIRMED |
| HF-05B-13 | Provider references are external values only, never DAEN references or GeoIDs. | CONFIRMED |
| HF-05B-14 | I1–I13 and all 15 coherence cases are Human Frozen, subject to protected TBDs. | CONFIRMED |


## Phase 05C — Read Contracts Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05C-READ-CONTRACTS-FREEZE-01 | Phase 05C Source Assertion, Current DAEN Representation, Access Point and Extent read contracts are Human Frozen. No endpoints, OpenAPI, JSON Schema, database schema, mutations or architecture are defined. | CONFIRMED |
| HF-05C-01 | Public Source Assertion subject is PlaceRef only; unresolved-location exposure and AP-as-assertion-subject remain deferred. | CONFIRMED |
| HF-05C-02 | Source Assertion content is open fact/purpose, typed value, scope, Provenance, Quality and history without closed vocabularies. | CONFIRMED |
| HF-05C-03 | Original assertion content is immutable; correction creates a new assertion; superseded differs from withdrawn. | CONFIRMED |
| HF-05C-04 | Same-subject supersession is guaranteed; cross-subject relations are historical/traceability context only. | CONFIRMED |
| HF-05C-05 | Current Representation is Place-associated, selected, traceable and not absolute truth. | CONFIRMED |
| HF-05C-06 | Material Selection Records are immutable and use stable opaque SelectionRecordRef. | CONFIRMED |
| HF-05C-07 | Selected-value traceability is frozen; derivation/normalization algorithms are not. | CONFIRMED |
| HF-05C-08 | Competing evidence is discoverable without ranking or canonical conflict-set logic. | CONFIRMED |
| HF-05C-09 | Access Point reads expose served Places, attributable facts, Provenance and Quality without AP ranking/defaults. | CONFIRMED |
| HF-05C-10 | Access Point attributable location fact is an API read boundary, not a new Domain concept or reference type. | CONFIRMED |
| HF-05C-11 | AP location multiplicity may be zero, one or several; no Place-coordinate fallback. | CONFIRMED |
| HF-05C-12 | AP↔Place is many-to-many capable with explicitly recorded history only. | CONFIRMED |
| HF-05C-13 | Extent is read-only, non-top-level and exposed through assertion/selection values. | CONFIRMED |
| HF-05C-14 | Extent geometry/role/overlap semantics remain deferred; overlap alone implies no relation. | CONFIRMED |
| HF-05C-15 | Provenance remains attached to exposed facts/assertions/selections/AP facts; no public Source resource. | CONFIRMED |
| HF-05C-16 | Quality is explicit where required and `unknown` is valid; no scale or ranking is frozen. | CONFIRMED |
| HF-05C-17 | Absence, unknown, restricted detail and historical identity remain distinct; no fabricated defaults. | CONFIRMED |


## Phase 05D — Mutation and Error Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05D-MUTATION-ERROR-FREEZE-01 | Phase 05D mutation, error, idempotency/concurrency and Provenance/Quality contracts are Human Frozen. Endpoints, OpenAPI, database schema and architecture remain out of scope. | CONFIRMED |
| HF-05D-01 | shared attributable/non-destructive/exact/stale-safe/idempotent rules. | CONFIRMED |
| HF-05D-02 | Source Assertion create and same-subject supersession. | CONFIRMED |
| HF-05D-03 | explicit Correction intent. | CONFIRMED |
| HF-05D-04 | T2 withdrawal semantics. | CONFIRMED |
| HF-05D-05 | Selection add/replace and exact scope. | CONFIRMED |
| HF-05D-06 | merge survivor supplied, not chosen. | CONFIRMED |
| HF-05D-07 | MIS_CONFLATION versus TRUE_DIVISION. | CONFIRMED |
| HF-05D-08 | closure and T1 withdrawal without lifecycle enum. | CONFIRMED |
| HF-05D-09 | domain-specific relationship/history writes only. | CONFIRMED |
| HF-05D-10 | all AP public mutations deferred. | CONFIRMED |
| HF-05D-11 | generic Place creation deferred. | CONFIRMED |
| HF-05D-12 | Extent writes only through assertion/selection. | CONFIRMED |
| HF-05D-13 | mutation Provenance and fact Quality. | CONFIRMED |
| HF-05D-14 | conceptual error classes and ALREADY_HOLDS. | CONFIRMED |
| HF-05D-15 | stale-write protection. | CONFIRMED |
| HF-05D-16 | MutationRequestRef idempotency. | CONFIRMED |
| HF-05D-17 | logical atomicity and result categories. | CONFIRMED |
| HF-05D-18 | no destructive public history delete. | CONFIRMED |
| HF-05D-19 | M1–M18 invariants and 25 coherence cases. | CONFIRMED |
| HF-05D-20 | Phase 05E must preserve unresolved policy. | CONFIRMED |


## Phase 05E — Endpoint Map Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05E-ENDPOINT-MAP-FREEZE-01 | 18-endpoint `/v1` surface frozen: 7 reads and 11 mutations, action routing via `/actions/{verb}`, separate correction, no `/representation`, Idempotency-Key with client-global scope and 7-day minimum replay horizon, MutationBasisToken, and containment read completion. | CONFIRMED |


## Phase 05 Final Gate Round 1

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05-FINAL-GATE-ROUND-1-ITERATE-01 | Baseline `e9342ba376cc2e1639a3eef1953e18067b6ecc2a`; independent recommendation and Human Decision ITERATE; no Domain contradiction; bounded work limited to F1–F5; no endpoint redesign; Phase 06 NOT authorized. | CONFIRMED |


## Phase 05 Final-Gate Round 1 Bounded Completion

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05-FINAL-GATE-R1-BOUNDED-COMPLETION-01 | F1–F5 completed: HTTP status categories recorded; Idempotency-Key reconciled to client-global scope and 7-day minimum; Extent-kind write gate explicit; endpoint basis/idempotency annotations added; exact explicit Selection scope equality recorded. No new endpoints, Domain Model change or OpenAPI. Phase 06 remains NOT authorized; Phase 05 Final Gate requires re-review. | CONFIRMED |


## Phase 05 Final Gate GO

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05-FINAL-GATE-GO-01 | Phase 05 API Definition Final Gate = GO; F1–F5 closed; required conceptual/API-definition deliverables complete; no Domain contradiction; Phase 06 Technical Architecture authorized. OpenAPI, implementation, DB/provider/auth/privacy and market validation are not implied. | CONFIRMED |
| PHASE-05-COMPLETE-01 | Phase 05 API Definition is complete at the conceptual contract and endpoint-mapping level. | CONFIRMED |


## Phase 06 Technical Architecture Entry Gate

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06-TECH-ENTRY-GATE-FREEZE-01 | Phase 06 Entry Gate frozen; no technology, DB or framework selected; no Domain/API TBD resolved; 06A Requirements & Quality Attributes authorized. | CONFIRMED |


## Phase 06A Architecture Requirements Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06A-ARCH-REQUIREMENTS-FREEZE-01 | Phase 06A requirements and quality attributes are Human Frozen; no technology, DB, framework, code, OpenAPI or Domain/API TBD resolution. | CONFIRMED |
| PHASE-06-CD1-INTERNAL-PLACE-PROVISIONING-DEFECT-01 | Internal Place provisioning contract is missing and requires a bounded prior-contract amendment before 06B final ingestion architecture. AP and Containment writes are separate TBDs. | OPEN — BOUNDED PRIOR-CONTRACT AMENDMENT REQUIRED |


## CD-1 Internal Place Provisioning Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-05-POST-GO-CD1-INTERNAL-PLACE-PROVISIONING-01 | Internal-only provisioning of an already-decided NEW PLACE; no public endpoint; Phase 05 GO tag unchanged; permanent internal request/result binding; CD-1 resolved. | CONFIRMED |
| PHASE-06-CD2-SPLIT-CHILD-LOCATING-BASIS-DEFECT-01 | Whether Split-created identities require locating basis in the same logical outcome remains open. | OPEN |
| OBS-06-H14-LIFETIME-01 | Whether H14 is creation-only validity or must remain continuously true after later assertion withdrawal/supersession remains open and non-blocking for 06B. | OPEN / NON-BLOCKING |


## CD-2 Split Child Locating-Basis Human Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06-CD1-LIMITED-REREVIEW-GO-01 | CD-1 limited re-review = GO; internal Place provisioning contract closed. | CONFIRMED |
| PHASE-05-POST-GO-CD2-SPLIT-CHILD-LOCATING-BASIS-01 | H14 at Split-child birth; no parent reassociation or cross-subject supersession; no automatic selection; endpoint surface and Phase 05 tag unchanged; CD-2 resolved. | CONFIRMED |
| OBS-06-H14-LIFETIME-01 | H14 lifetime after birth remains open and non-blocking. | OPEN / NON-BLOCKING |


## Phase 06B Logical Architecture Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06B-LOGICAL-ARCHITECTURE-FREEZE-01 | Modular Monolith pattern, module ownership/dependencies, logical mutation pipeline, Place Bootstrap, read/freshness boundary, audit/residency boundaries, ingestion/jobs and extraction seams are Human Frozen. No technology, DB, cache, queue, runtime, cloud or consensus selected; protected TBDs remain. | CONFIRMED |


## Phase 06B Gate Status Normalization

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06B-GATE-STATUS-NORMALIZATION-01 | Stale Phase 06A header corrected; historical CD-1 OPEN status explicitly marked historical; no architecture or contract semantics changed. | EDITORIAL / NON-SEMANTIC |


## Phase 06B Final Acceptance and Phase 06C Authorization

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06B-LIMITED-CONFORMANCE-GO-01 | Limited conformance re-review at baseline `308c1b9f8ce6710fd643ef7d191c4d0c592bf0fb` = GO; C1-C8 PASS; Logical Mutation Unit conformant; no technology selected; no protected-TBD leak; no Phase 05/API regression. Phase 06B Logical Architecture FINAL ACCEPTED. Phase 06C Persistence / Identity / History / Spatial AUTHORIZED. CD-1 CLOSED; CD-2 RESOLVED; OBS-06-H14-LIFETIME remains OPEN / NON-BLOCKING. | CONFIRMED |


## Phase 06C Persistence / Identity / History / Spatial Freeze

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06C-PERSISTENCE-IDENTITY-HISTORY-SPATIAL-FREEZE-01 | Phase 06C Human Frozen: relational transactional store class, one primary authoritative store initially, reference family/non-reuse corrections, identity/history, selection heads, basis/idempotency persistence support, recovery, residency and spatial readiness requirements. No product selected; 06D not yet authorized pending limited conformance re-review. | CONFIRMED |


## Phase 06C Limited Conformance GO

| Decision | Frozen result | Status |
|---|---|---|
| PHASE-06C-LIMITED-CONFORMANCE-GO-01 | Baseline `2492dc5a9d0ae423ac4a962696a245498f55d563`; C1–C8 PASS; Current Representation persistence and History/Audit persistence conformant; Phase 06C final accepted; no technology/product selection; no protected-TBD leak; Phase 06D authorized. | CONFIRMED |

## PHASE-06D-CONCURRENCY-IDEMPOTENCY-ATOMICITY-FREEZE-01

Status: `CONFIRMED`

Human decision: `PHASE 06D CONCURRENCY / IDEMPOTENCY / ATOMICITY = HUMAN FROZEN`.

This freeze records optimistic concurrency, MutationBasis and recovery-incarnation safety, idempotency execution and replay, local transactional atomicity, non-reuse evidence, recovery/retry behavior, target multi-region guarantees, and declared-read-set protection. It selects no technology or product and does not resolve protected Domain/API TBDs.

## PHASE-06D-LIMITED-CONFORMANCE-R1-ITERATE-01

Status: `CONFIRMED`

Baseline: `ca2347a374ea302ddb0465370d2380f0a82fb91f`.

C3/F4 are the sole defect. C1, C2, C4-C8, Selection Race Error Mapping, Declared Read-Set Protection, Clock/Time Boundary, F1-F3, and F5-F8 are inherited PASS/conformant judgments. This is a bounded repair only; Phase 06E remains NOT authorized.

## PHASE-06D-R1-PROVISIONING-RECOVERY-MAPPING-COMPLETION-01

Status: `CONFIRMED`

Request/reference recovery mappings receive independent durability, including CD-1 provisioning mappings across the primary loss window. The mapping is not commit authority; retries reuse the mapped references. No product was selected.

## PHASE-06D-C3-F4-LIMITED-REREVIEW-GO-01

Status: `CONFIRMED`

Baseline: `1ae66c7ee454b4523d42aa5bc94196e96946ebe6`. C3 PASS, F4 PASS, orphan mapping PASS, fail-closed PASS, and non-reuse/request-mapping separation PASS. All inherited findings remain accepted. Phase 06D is FINAL ACCEPTED and Phase 06E is AUTHORIZED. No product or technology was selected.

## PHASE-06E-SOFTWARE-STACK-FREEZE-01

Status: `CONFIRMED`

`PHASE 06E SOFTWARE STACK = HUMAN FROZEN`. The approved CPython/FastAPI/Uvicorn/Pydantic/PostgreSQL 17/psycopg/SQLAlchemy Core/Alembic/PostgreSQL-backed jobs/no-cache/EvidenceStore/OpenTelemetry/Ruff/Pyright/pytest/Hypothesis/Docker/Compose/GitHub Actions baseline is recorded. Cloud, provider, deployment, evidence region, cost, and infrastructure closure remain explicitly deferred; protected Domain/API TBDs are unchanged.

## PHASE-06E-SOFTWARE-STACK-LIMITED-CONFORMANCE-GO-01

Status: `CONFIRMED`

Baseline: `a6920d9c26261d38530c2add631f8ba35e974fb7`. C1-C6 PASS and software-stack coherence conformant. The software stack is FINAL ACCEPTED; infrastructure/provider/cost remain open, Phase 06F is not authorized, and no protected TBD leaked.

## CD-3 R1 Scope Amendment — Human Frozen

| Decision | Result | Status |
|---|---|---|
| CD3-R1-SCOPE-AMENDMENT-01 | Date: 2026-10-09. R0 reviewed commit `fdbfd0cd572d58104c6e6b7f3224ae3ea4d9f70b` with P0=0, P1=0, P2=11; R1 GO freezes a separate `/gateway/v1` surface with exactly POST geocode, POST reverse-geocode, and GET status. The 06B integration-package exception is bounded; no V1 cache, Domain/provider authority, or automatic persistence is authorized. S1 remains OPEN; Q2 and Q3 remain OPEN; L1/L2/P1/P2/T1/C1 remain open; Phase 06E remains IN PROGRESS; Phase 06F remains NOT AUTHORIZED. | CONFIRMED |

R1 is a documentation/governance scope amendment only. The frozen Phase-05 18-endpoint surface and all existing `/v1` semantics remain unchanged. WP2 defines a separate gateway error contract, and implementation remains gated by R2/R3/R4/R5 and the named dependency/legal decisions.
