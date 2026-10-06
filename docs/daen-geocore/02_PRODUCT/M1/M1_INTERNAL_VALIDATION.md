# M1 Internal Geo Core Validation

## 1. Purpose

M1 validates whether the frozen Phase 03 Domain Model is coherent and operable against a deliberately difficult internal corpus. It validates model friction, not commercial or production value.

## 2. Frozen hypothesis

> If the frozen Phase 03 domain model is coherent, a pre-registered corpus of 15–25 Places containing deliberately difficult and surprise location cases MUST be representable through the frozen Geo Core concepts without violating domain invariants, requiring business semantics, or requiring an unplanned new core domain concept.

For this M1, the initial corpus is 20 Places and the maximum after split scenarios is 23 Places.

The hypothesis is falsified if:

1. a domain invariant is violated by the model;
2. a required scenario cannot be expressed;
3. a fundamental new core concept or business concept is required; or
4. the same identity, relationship or lifecycle friction pattern occurs on 3 or more distinct Places.

## 3. What M1 does and does not prove

M1 validates:

- conceptual model coherence;
- identity continuity and resolvability;
- representation change;
- Source Assertions;
- Access Point modelability;
- Correction, Merge and Split;
- Provenance and Quality;
- absence of business semantics;
- practical domain-model friction.

M1 Internal Validation does not validate customer demand, consumer adoption, willingness to adopt, willingness to pay, real consumer workflow fit, market demand, consumer integration value, production provider independence, scale, performance, SLA or production readiness.

## 4. Actors and independence

- **Data Operator:** prepares and executes the registered corpus and scenarios.
- **Reviewer:** independently reviews the corpus, selects or confirms surprise cases, checks outcomes and classifies friction.

The two roles MUST be separate. The Reviewer SHOULD NOT be the primary author of the Phase 03 Domain Model. If independence cannot be achieved, record:

`VALIDATION LIMITATION — Reviewer independence not fully achieved`

This limitation does not block document creation.

## 5. Workflow

1. Freeze the 20-slot corpus plan and scenarios A–J.
2. Select actual public Places later; mark every synthetic case clearly.
3. Register three surprise cases selected preferably by the Reviewer.
4. Execute each scenario against the frozen concepts without adding concepts or business semantics.
5. Record binary invariant outcomes and any friction in the Model Friction Log.
6. Permit one rerun only when a documented operator, data-entry or execution-medium error caused the apparent failure.
7. Classify the result as GO, ITERATE or RETURN TO DOMAIN MODEL.

## 6. Execution rules

- MUST cite the frozen Phase 03 rule used for each scenario.
- MUST keep scenario outcomes and friction findings separate from the pre-registered expectation.
- MUST NOT invent a merge survivor policy.
- MUST NOT silently reopen Phase 03 decisions.
- MUST NOT introduce a domain concept absent from the Phase 03 model.
- MUST NOT add business entities or business decisions to make a scenario pass.
- SHOULD field-verify up to 5 public Places when practical.
- Execution medium remains `TBD`.

## 7. Binary invariants

- **B1 — No identity reuse:** No GeoID is reassigned or reused.
- **B2 — Identity continuity:** Name, address, coordinate or provider-reference changes MUST NOT silently change Place identity.
- **B3 — Historical resolution:** GeoIDs remain resolvable after merge, closure, split and withdrawal.
- **B4 — Representation change:** Current DAEN Representation can change without destructive overwrite.
- **B5 — Assertion attribution:** Source Assertions remain attributable after change.
- **B6 — Access separation:** Access Point can differ from Selected Coordinate and MUST NOT be inferred solely from it.
- **B7 — Shared access:** A shared Access Point can be represented once and serve multiple Places.
- **B8 — Supersession:** Wrong facts can be superseded while preserving material history.
- **B9 — Traceability:** Current DAEN Representations and identity-resolution decisions can be traced to source.
- **B10 — Explicit quality:** Every fact evaluated or selected as a Current DAEN Representation during M1 has explicit Quality; `unknown` is valid.
- **B11 — No business dependency:** No business entity or business decision is required to complete M1.

## 8. Decision gate

### GO

GO requires B1–B11 to hold after permitted execution-error reruns, scenarios A–J to be expressible, no fundamental new core concept, mainly governance or implementation TBD friction, no repeated identity/relationship/lifecycle model-gap pattern, and understandable Provenance and Quality.

GO means the Phase 03 Domain Model is stable enough to proceed to Phase 05 — API Definition. GO does not mean market validation.

### ITERATE

Use ITERATE when the model mostly works but bounded wording, relationship or lifecycle clarification is required. Only one bounded Phase 03/04 revision cycle is allowed without a new human decision.

### RETURN TO DOMAIN MODEL

Use RETURN TO DOMAIN MODEL when Place definition repeatedly fails, GeoID continuity cannot be maintained, Merge/Split semantics conflict, Access Point cannot be represented coherently, Current DAEN Representation requires false certainty, a fundamental new concept is necessary, or business semantics are required.

## 9. Timebox

- Target: `2 weeks`
- Hard stop: `3 weeks`

The timebox begins only when the corpus, scenarios and execution medium are ready.
