# RUN-F-01 — Scenario F Disposition

## Acceptance

- **Independent verdict:** `PASS`.
- **Project acceptance:** `PASS` for the frozen Scenario F outcome only.
- **Evidence:** `005a25f116e93d331920a0d922fc61cc58b8bbde`.
- **Input freeze:** `8d7ab92a515ad3bed899af35c15cb94227535f5e`.
- **Scenario E acceptance baseline:** `193a2f5614b48007eb4a832acbaf560ec12081c5`.
- Three wrong fixture Source Assertions were superseded.
- OLD assertions remain retained and REVISED assertions remain attributable.
- Three Correction action records exist.
- Place identities remain unchanged and no destructive overwrite occurred.
- No Current DAEN Representation or separate Succession object was required for this run.
- No F rerun is authorized.
- Overall M1 decision remains `NOT MADE`.

This does not establish production correction authority, real-world truth of revised values, real AEON address correction, P04 entrance/Access Point resolution, Current DAEN Representation behavior after correction, general Succession taxonomy, merge/split/lifecycle behavior or overall M1 acceptance.

## Non-blocking findings

### RUN-F-01:F1

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** Add the retrospective input-freeze reference: `8d7ab92a515ad3bed899af35c15cb94227535f5e`. Distinguish `193a2f5` as E acceptance baseline, `8d7ab92` as F input freeze and `005a25f` as F operator evidence. Historical source-map.md remains unchanged.

### RUN-F-01:F2

**Classification:** `VALIDATION MEDIUM ISSUE`, Low. **Blocking:** No.

**Disposition:** The actual correction is carried by the Source Assertion supersedes_reference chain. Correction rows additionally provide a typed Correction marker, correction-action provenance and fixture-only governance marker. The duplicated OLD/REVISED encoding is not a production schema decision. The checker is unchanged.

### RUN-F-01:F3

**Classification:** `EVIDENCE LIMITATION`, Low. **Blocking:** No.

**Disposition:** Domain Model §19 explicitly supports Source Assertion supersession as normal correction. §26 describes Succession for a Place identity or representation and leaves exact types TBD. RUN-F-01 therefore does not require a separate Succession row, but whether Source Assertion supersession counts as Succession terminology remains unresolved. No Domain Model amendment is made.

### RUN-F-01:F4

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** The frozen shorthand invariants 2, 5 and 8 is mapped additively for this run to M1-B2 identity continuity, M1-B5 assertion attribution, M1-B8 supersession, plus the relevant Domain Model correction/history invariant. The frozen scenario sheet is not rewritten.

### RUN-F-01:F5

**Classification:** `EVIDENCE LIMITATION`, Low. **Blocking:** No.

**Disposition:** The facts are wrong by controlled fixture declaration. F validates correction representation, supersession, retention, attribution and identity preservation, not error detection, source-trust ranking, correction-authority decisions or real-world factual truth. The P04 synthetic address is not AEON's real address evidence.

## Carry-forward

- B:F4 / D:F5: P04 observed-entrance coordinate versus Access Point remains open.
- C findings are not imported into F.
- F3 remains the Correction/Succession terminology boundary.
- F2 remains the duplicate relation-encoding medium limitation.

## Decision boundary

This disposition accepts only the frozen controlled Scenario F outcome. It does not mark B1–B11 globally passed and does not make an overall M1 decision.
