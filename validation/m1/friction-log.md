# M1 Model Friction Log

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

Empty log template. Do not populate entries before M1 execution.

## Trigger questions

- What object should this be?
- Is this the same Place?
- Where does this fact belong?
- Which identity should survive?
- Can the current model represent this case?
- Do we need a new concept?

## Approved classification values

- Terminology ambiguity
- Identity ambiguity
- Missing relationship
- Missing lifecycle semantics
- Governance ambiguity
- Implementation question
- Out-of-scope business concept

## Operational observation — Data Maintenance Friction

During M1, reviewers SHOULD record when obtaining or correcting a usable location fact requires:

- field verification;
- specialist judgment;
- repeated manual research;
- multiple user actions.

This is an operational observation, not a Domain Model invariant. It MUST NOT automatically cause `RETURN TO DOMAIN MODEL`.

If field verification appears necessary for routine Place maintenance, record:

`OPERATIONAL WARNING — LOCATION DATA MAINTENANCE COST MAY NOT SCALE`

Do not design future contribution UX in this phase.

## Resolution types

- frozen rule cited
- invented rule
- escalated

## Entry template

### Friction F-___

- **Scenario:**
- **Place/corpus slot:**
- **Question:**
- **Classification:**
- **Resolution type:**
- **Proposed missing wording if an invented rule was required:**
- **Repeated pattern count:**
- **Reviewer notes:**

## Retrospective Review Findings — RUN-A-02

> RETROSPECTIVE REVIEW FINDING — discovered during independent review, not recorded as contemporaneous operator friction.

| Finding | Affected run / evidence | Classification | Project disposition |
|---|---|---|---|
| F1 — Cross-scope supersession is ambiguous and the selection label conflicts with its link | RUN-A-02; `POST-P02-CR`; review sensitivity check | Governance ambiguity | Prospective selection-scope clarification adopted. Historical ambiguity retained. Selection coexistence is not validated by RUN-A-02. |
| F2 — Initial selections marked REAL without a frozen convention | RUN-A-02; `PRE-P01-CR`, `PRE-P02-CR` | Implementation question | Prospective M1 marking convention clarified. Historical marking retained. |
| F3 — P01 initial language scope omitted while described as English | RUN-A-02; `PRE-P01-SA1`, `operator-execution.md` | Terminology ambiguity | Prospective explicit-language convention clarified. Historical omission retained. |
| F4 — Exact source-specific attribution of strings not established | RUN-A-02; `source-map.md` P01-E2/P02-E2 | Implementation question | Evidence limitation accepted for Scenario A narrow scope. No exact external-source verification claim. |
| F5 — Selection attribution is not distinct from assertion provenance | RUN-A-02; selection rows and operator record | Implementation question | Future selections require operator/step attribution distinct from assertion provenance, using existing records. |
| F6 — Checker does not test scope-aware supersession or concept-typed references | RUN-A-02; independent-review sensitivity checks | Implementation question | Checker limitation retained for manual review. No checker enhancement authorized. |
| F7 — Encoding decisions were not logged contemporaneously and RUN-A-01 retrospective pointer was absent | RUN-A-01 and RUN-A-02; disposition and shared log | Governance ambiguity | Retrospective findings and pointers are now recorded. They are not recast as RUN-A-01 observations. |
| F8 — `locus=` is name-derived rather than an independent locator | RUN-A-02; `PRE-P01-PLACE` / `PRE-P02-PLACE` | Implementation question | Evidence limitation accepted for Scenario A narrow scope. No new locator concept added. |

All rows above were discovered at independent review stage. They are not claims about private operator reasoning and do not automatically imply a Domain Model failure.

## INDEPENDENT REVIEW FINDINGS — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-B-01 was accepted for its scoped Scenario B outcome with no confirmed Domain Model friction. The following review findings are retained as non-blocking evidence, reporting or validation-medium limitations only:

| Finding | Disposition |
|---|---|
| `RUN-B-01:F1` repeated P03 assertion | Retain raw evidence; do not treat the repeat as independent corroboration. |
| `RUN-B-01:F2` traceability slip | Additive citation erratum only; frozen inputs and scenario sheet remain unchanged. |
| `RUN-B-01:F3` composite P04 provenance | Accept record-level attribution; do not claim finer original-source attribution. |
| `RUN-B-01:F4` observed-entrance coordinate | Carry forward to Scenario D precheck; frozen D targets remain P05/P06/P07. |
| `RUN-B-01:F5` free-text fixture markers | Validation notation only; not domain states or production semantics. |
| `RUN-B-01:F6` P17 background linkage | Retain `inputs.md` and ledger as one evidence package. |
| `RUN-B-01:F7` explicit `unknown` Quality | Accepted; informative Quality and quality-driven decisions remain untested. |

These are not contemporaneous operator friction and must not be counted as repeated Domain Model friction patterns.

## INDEPENDENT REVIEW FINDINGS — RUN-C-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-C-01 was accepted for its controlled same-scope positive replacement outcome. No confirmed Domain Model failure was found. The six review findings remain non-blocking:

| Finding | Disposition |
|---|---|
| `RUN-C-01:F1` Place-context labels | Retrospective mappings added in the disposition; no new web verification claimed. |
| `RUN-C-01:F2` selector aliases | Retrospective alias index added; not a historical definition claim. |
| `RUN-C-01:F3` commit citation | Correct commit distinction recorded; historical source-map citation unchanged. |
| `RUN-C-01:F4` correction rationale | Retained as prose-only limitation; no Correction workflow or Scenario F execution. |
| `RUN-C-01:F5` scope/effective-state encoding | Retained as validation-medium convention; historical flags unchanged. |
| `RUN-C-01:F6` checker scope | Reference-type, scope and effective-state checks remain manual. |

These are independent-review findings, not contemporaneous operator friction or confirmed Domain Model failures.

## INDEPENDENT REVIEW FINDINGS — RUN-G-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-G-01 was accepted for its controlled synthetic Merge outcome. The five findings remain non-blocking:

| Finding | Classification | Disposition |
|---|---|---|
| `RUN-G-01:F1` same-Place premise not represented as a ledger row | `EVIDENCE LIMITATION`, Low | Frozen in input evidence; no historical ledger row added. |
| `RUN-G-01:F2` retirement not written on Place row | `VALIDATION MEDIUM ISSUE`, Low | Derived from Resolution Link, identities, direction and Succession; no production status field. |
| `RUN-G-01:F3` validation markers are not production mechanisms | `VALIDATION MEDIUM ISSUE`, Low | Markers retained as validation assertions; checker unchanged. |
| `RUN-G-01:F4` alternative-world isolation | `VALIDATION MEDIUM ISSUE`, Low | Subcases MUST NEVER be concatenated into one effective history. |
| `RUN-G-01:F5` traceability references | `REPORTING / TRACEABILITY ISSUE`, Low | Commit distinctions recorded additively; historical source map unchanged. |

The original P08/P09 issue remains separately classified as `VALIDATION PREREGISTRATION / TARGET-SELECTION DEFECT`, not Domain Model friction.

## INDEPENDENT REVIEW FINDINGS — RUN-F-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-F-01 was accepted for its controlled Source Assertion correction outcome with no confirmed Domain Model failure. The five findings remain non-blocking:

| Finding | Classification | Disposition |
|---|---|---|
| `RUN-F-01:F1` input-freeze traceability | `REPORTING / TRACEABILITY ISSUE`, Low | Record E baseline, F input freeze and F evidence commit distinction; historical source-map.md unchanged. |
| `RUN-F-01:F2` duplicate OLD/REVISED relation encoding | `VALIDATION MEDIUM ISSUE`, Low | Retain as disposable notation; supersedes_reference remains the correction carrier; checker unchanged. |
| `RUN-F-01:F3` Correction/Succession terminology boundary | `EVIDENCE LIMITATION`, Low | §19 supports Source Assertion correction; §26 leaves Succession types TBD; no Domain Model failure or amendment. |
| `RUN-F-01:F4` invariant-number shorthand ambiguity | `REPORTING / TRACEABILITY ISSUE`, Low | Additive mapping to M1-B2/B5/B8 and relevant Domain Model correction/history requirement; frozen sheet unchanged. |
| `RUN-F-01:F5` fixture-declared wrong facts | `EVIDENCE LIMITATION`, Low | F tests correction representation, not error detection, source ranking or real-world truth. |

These are independent-review findings, not contemporaneous operator friction or confirmed Domain Model failures.

## INDEPENDENT REVIEW FINDINGS — RUN-E-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-E-01 was accepted for its scoped controlled synthetic shared-Access-Point outcome with no confirmed Domain Model friction. The following findings remain non-blocking validation, evidence or traceability limitations only:

| Finding | Classification | Disposition |
|---|---|---|
| `RUN-E-01:F1` excluded pickup/drop-off term in a negative fixture marker | `VALIDATION MEDIUM ISSUE`, Low | Marker is validation notation only; `business_pickup_dropoff=false` must not become a future schema/API/domain field. |
| `RUN-E-01:F2` subject/provenance label conflation | `VALIDATION MEDIUM ISSUE`, Low | Understandable in this run but not a preferred future convention; raw run retained. |
| `RUN-E-01:F3` P08 containment context | `EVIDENCE LIMITATION`, Low | One-AP/two-Place representation accepted; independence from containment is not established. |
| `RUN-E-01:F4` P05/P06/P07 scenario traceability discrepancy | `REPORTING / TRACEABILITY ISSUE`, Low | Complete note retained; frozen scenario sheet and runbook govern; no frozen-file repair. |
| `RUN-E-01:F5` missing input-freeze SHA in source map | `REPORTING / TRACEABILITY ISSUE`, Low | Post-review mapping records `a966670b5026331c6399c2bed4c67660071223e3`; historical source map unchanged. |
| `RUN-E-01:F6` forward-looking P08/G interaction | `EVIDENCE LIMITATION`, Low, forward-looking | Carry to G precheck; E does not constrain G merge or AP behavior. |

These are independent-review findings, not contemporaneous operator friction or confirmed Domain Model failures.

## INDEPENDENT REVIEW FINDINGS — RUN-D-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-D-01 was accepted for its scoped synthetic Access Point outcome. No observable domain question was identified. The six findings remain non-blocking:

| Finding | Disposition |
|---|---|
| `RUN-D-01:F1` source-reference SHA/path | Corrected mapping recorded retrospectively; original source-map.md unchanged. |
| `RUN-D-01:F2` selector aliases | Retrospective row-key index recorded; no historical alias definition claimed. |
| `RUN-D-01:F3` served-place relationships | Manually checked; checker and encoding unchanged. |
| `RUN-D-01:F4` synthetic access evidence | Accepted as synthetic fixture text; no field research required for D. |
| `RUN-D-01:F5` P04 carry-forward | B:F4 remains unresolved; P04 was not added to D. |
| `RUN-D-01:F6` E overlap | P05/P06 sharing does not execute E's P07 case. |

These are independent-review findings, not contemporaneous operator friction or confirmed Domain Model failures.

## INDEPENDENT REVIEW FINDINGS — RUN-H-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-H-01 was accepted for its controlled synthetic Split outcome. These findings are retained as non-blocking review, validation-medium, evidence or traceability limitations:

| Finding | Classification | Disposition |
|---|---|---|
| `RUN-H-01:F1` cross-subject Source Assertion supersession | `MODEL FRICTION — LOW — SINGLE INSTANCE — NON-BLOCKING` | Accepted for this fixture only; no Domain Model amendment; narrow cross-subject reassociation/supersession TBD deferred to Phase 05/later policy. |
| `RUN-H-01:F2` historical parent status derived from relationships | `VALIDATION MEDIUM ISSUE`, Low | No production parent status field added. |
| `RUN-H-01:F3` one-to-many split notation not mechanically checked | `VALIDATION MEDIUM ISSUE`, Low | No production `split_group`/`result_count` schema added. |
| `RUN-H-01:F4` split premise frozen outside ledger | `EVIDENCE LIMITATION`, Low | Retained; no retrospective premise rows added. |
| `RUN-H-01:F5` 20-to-23 bookkeeping across isolated subcases | `EVIDENCE LIMITATION`, Low | Corrected wording: conceptual capacity only; no materialized 23-Place state. |
| `RUN-H-01:F6` input-freeze and invariant shorthand traceability | `REPORTING / TRACEABILITY ISSUE`, Low | Retrospective references recorded; historical source map unchanged. |
| `RUN-H-01:F7` earlier corpus-plan discrepancy | `REPORTING / TRACEABILITY ISSUE`, Low | Historical discrepancy recorded; historical corpus plan unchanged. |

These are independent-review findings, not contemporaneous operator friction or confirmed global Domain Model failures.

## INDEPENDENT REVIEW FINDINGS — RUN-I-01 — NOT CONTEMPORANEOUS OPERATOR FRICTION

RUN-I-01 was accepted for its controlled closure / historical-reference-withdrawal outcome. The findings remain non-blocking:

| Finding | Classification | Disposition |
|---|---|---|
| `RUN-I-01:F1` self-referential closure Resolution Link | `VALIDATION MEDIUM ISSUE`, Low | Validation notation only; no production Resolution Link design or lifecycle/status field. |
| `RUN-I-01:F2` demolition-to-closure terminology | `MODEL FRICTION`, Low, bounded | Accepted for this fixture; lifecycle states/transitions remain deferred. |
| `RUN-I-01:F3` withdrawal target scope / Reading B | `MODEL FRICTION`, Low-Medium, terminology | Historical-reference withdrawal accepted; Place-GeoID withdrawal remains TBD and must be revisited at final B3 gate. |
| `RUN-I-01:F4` status markers | `VALIDATION MEDIUM ISSUE`, Low | Free-text validation notation only; no production enum. |
| `RUN-I-01:F5` input-freeze/invariant traceability | `REPORTING / TRACEABILITY ISSUE`, Low | Retrospective references recorded; historical source map unchanged. |
| `RUN-I-01:F6` demolition-year attribution | `EVIDENCE LIMITATION`, Low | Memo-level evidence retained without stronger attribution. |
| `RUN-I-01:F7` corpus-role drift | `REPORTING / TRACEABILITY ISSUE`, Low | Historical observations retained; planning files unchanged. |

### Model-friction tally

Confirmed model-friction findings currently include RUN-H-01:F1, RUN-I-01:F2 and RUN-I-01:F3.

`THREE MODEL FRICTION FINDINGS TOTAL, BUT NO REPEATED SAME-PATTERN FRICTION ACROSS THREE DISTINCT PLACES HAS BEEN ESTABLISHED.`

The frozen repeated-friction falsification rule is not triggered merely by count=3. No overall M1 decision is made.
