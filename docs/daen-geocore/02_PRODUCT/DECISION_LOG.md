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

## Conflict resolution

The earlier source material contained an organization-operations positioning. Phase 01 isolated it from the active Geo Core baseline. This Phase 02 Constitution keeps the location-infrastructure identity and does not import that historical positioning.
