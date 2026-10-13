# RUN-E-01 — Scenario E Disposition

## Acceptance

- **Project acceptance:** `PASS` for the frozen controlled synthetic shared-Access-Point outcome only.
- **Evidence commit:** `1388f7b33ac96352625b56ce0535c3cc740f2f6c`.
- **Input freeze:** `a966670b5026331c6399c2bed4c67660071223e3`.
- **D acceptance baseline:** `45712b61f2811fe7cf71f086d5a7f38e79a2a287`.
- Exactly one Access Point object is represented and serves `FIX-ID-P07` and `FIX-ID-P08`.
- Both served records resolve to Place rows and the relationship comes from the approved synthetic assertion.
- No Containment relation, coordinate semantics, pickup/drop-off, rider, dispatch or business-policy semantics are modeled.
- PRE rows and Place identity set remain unchanged; D evidence remains unchanged.
- No E rerun is authorized.
- Overall M1 decision remains `NOT MADE`.

This does not claim a real RUPP/Hun Sen Library shared gate, that containment implies access, a production AP namespace or deduplication, AP identity continuity between D and E, AP correction/lifecycle, mechanical validation of served-place relationships, Scenario G behavior, P04 Access Point resolution or overall M1 acceptance.

## Non-blocking findings and dispositions

### RUN-E-01:F1

**Classification:** `VALIDATION MEDIUM ISSUE`, Low. **Blocking:** No.

**Disposition:** Validation notation only. `business_pickup_dropoff=false` MUST NOT become a future schema/API/domain field merely because it appeared in the fixture. The historical ledger is unchanged.

### RUN-E-01:F2

**Classification:** `VALIDATION MEDIUM ISSUE`, Low. **Blocking:** No.

**Disposition:** Subject-label/provenance-label conflation is understandable in this run but is not a preferred future validation convention. The raw run is not rewritten.

### RUN-E-01:F3

**Classification:** `EVIDENCE LIMITATION`, Low. **Blocking:** No.

**Disposition:** E demonstrates one-AP/two-Place representation. It does not independently demonstrate that containment has no bearing on access. No additional E case is created.

### RUN-E-01:F4

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** The complete traceability discrepancy covers `synthetic-case-plan.md`, `corpus-register.csv` and `corpus-evidence.md`. The scenario sheet and runbook remain authoritative; frozen files are not repaired in place.

### RUN-E-01:F5

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** Post-review source-reference erratum: `SYN-E-ACCESS-SHARED` → RUN-E-01 `inputs.md` → frozen at `a966670b5026331c6399c2bed4c67660071223e3`. `45712b61` is the D acceptance baseline, `a966670b` the E input freeze, and `1388f7b3` the E operator evidence. Historical `source-map.md` is unchanged.

### RUN-E-01:F6

**Classification:** `EVIDENCE LIMITATION`, Low, forward-looking. **Blocking:** No.

**Disposition:** Carry forward to the Scenario G precheck. E-local use of `FIX-ID-P08` does not constrain G survivor direction, merge identity, GeoID resolution or AP behavior after merge. G is not pre-decided.

## Decision boundary

This disposition accepts only the frozen controlled Scenario E outcome. It does not mark B1–B11 globally passed and does not make an overall M1 decision.
