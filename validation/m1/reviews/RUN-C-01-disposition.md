# RUN-C-01 — Scenario C Disposition

## Acceptance

- **Independent verdict:** `PASS`.
- **Project acceptance:** `PASS` for Scenario C's frozen outcome only.
- **Reviewed evidence commit:** `77a3ec351c0120855b1569e06781813c7d163a34`.
- Controlled positive replacement of English display-name selections within the same Place/fact/purpose/language scope is supported.
- OLD assertions and OLD selections remain retained.
- Prior material state remains traceable.
- Place identities remain unchanged.
- No C rerun is authorized or needed.
- Overall M1 decision remains `NOT MADE`.

Not established: cross-language coexistence or migration; rejection of invalid cross-scope replacement; general current-state computation; real-world name accuracy or automatic spelling correction; source ranking; full Correction workflow; Access Point or coordinate behavior; provider behavior; P15/P16 merge; or any D–J result.

## Non-blocking findings

### RUN-C-01:F1

**Review finding:** Place-context provenance labels `C-PLACE-P04/P14/P16` were implicitly associated only.

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** Add the retrospective Place-context mapping in the traceability addendum below.

### RUN-C-01:F2

**Review finding:** `STEP-C-*` selector aliases were not defined in `operator-execution.md`.

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Medium. **Blocking:** No.

**Disposition:** Add the retrospective selector alias index below. It does not claim the aliases were previously defined.

### RUN-C-01:F3

**Review finding:** `source-map.md` cited `inputs.md` at baseline `e26be48`, although `inputs.md` was added in `32b0708`.

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** Record the correct commit distinction below. Do not repair the historical citation inside `source-map.md`.

### RUN-C-01:F4

**Review finding:** The mock correction rationale exists in prose; no Correction ledger entry or correction marker was created.

**Classification:** `EVIDENCE LIMITATION`, Low. **Blocking:** No.

**Disposition:** Retain the limitation. Do not create a Correction workflow or execute Scenario F.

### RUN-C-01:F5

**Review finding:** Scope and effective state are free-text/relationship-derived properties of the validation medium.

**Classification:** `VALIDATION MEDIUM ISSUE`, Low. **Blocking:** No.

**Disposition:** Keep the disposable validation-medium convention. Do not alter historical flags.

### RUN-C-01:F6

**Review finding:** The checker does not validate reference type, scope equality or effective-selection meaning.

**Classification:** `VALIDATION MEDIUM ISSUE`, Low. **Blocking:** No.

**Disposition:** Keep these checks assigned to manual review. Do not enhance the checker.

## POST-REVIEW TRACEABILITY ADDENDUM

These mappings are added after review. They did not exist completely in the original run package.

### F1 — Place-context labels

- `C-PLACE-P04` → `validation/m1/corpus-evidence.md`, P04 section, committed at full baseline `e26be48851892a37f222d37569acfe1f3ddc68d2`.
- `C-PLACE-P14` → `validation/m1/corpus-evidence.md`, P14 section, committed at full baseline `e26be48851892a37f222d37569acfe1f3ddc68d2`. The subject is the Parking Tower premises, not the company.
- `C-PLACE-P16` → `validation/m1/synthetic-case-plan.md`, P16 section, committed at full baseline `e26be48851892a37f222d37569acfe1f3ddc68d2`. The duplicate-of-P15 background is preserved without a merge.

No new web verification is claimed.

### F2 — Selector aliases

| Existing selector string | Ledger row key | Selection subject | Attribution |
|---|---|---|---|
| `STEP-C-P04-OLD` | `RUN-C-01:PRE-P04-SEL-OLD` | `FIX-ID-P04-SEL-OLD` | Codex / RUN-C-01 / `operator-execution.md` step 1 and OLD selection action |
| `STEP-C-P04-REVISED` | `RUN-C-01:POST-P04-SEL-REVISED` | `FIX-ID-P04-SEL-REVISED` | Codex / RUN-C-01 / `operator-execution.md` steps 3–6 |
| `STEP-C-P14-OLD` | `RUN-C-01:PRE-P14-SEL-OLD` | `FIX-ID-P14-SEL-OLD` | Codex / RUN-C-01 / `operator-execution.md` step 1 and OLD selection action |
| `STEP-C-P14-REVISED` | `RUN-C-01:POST-P14-SEL-REVISED` | `FIX-ID-P14-SEL-REVISED` | Codex / RUN-C-01 / `operator-execution.md` steps 3–6 |
| `STEP-C-P16-OLD` | `RUN-C-01:PRE-P16-SEL-OLD` | `FIX-ID-P16-SEL-OLD` | Codex / RUN-C-01 / `operator-execution.md` step 1 and OLD selection action |
| `STEP-C-P16-REVISED` | `RUN-C-01:POST-P16-SEL-REVISED` | `FIX-ID-P16-SEL-REVISED` | Codex / RUN-C-01 / `operator-execution.md` steps 3–6 |

This is a retrospective alias index, not a claim that the aliases were previously defined. No action timestamps are invented.

### F3 — Commit citation

- `e26be48851892a37f222d37569acfe1f3ddc68d2` = B acceptance baseline.
- `32b0708460ede4de3e0601f8570e29bbae5ddd2f` = C input-freeze commit.
- `77a3ec351c0120855b1569e06781813c7d163a34` = C operator evidence.

The C input files are unchanged between `32b0708` and `77a3ec3`.

## Decision boundary

This disposition accepts only the controlled same-scope positive replacement. It does not mark B1–B11 globally passed and does not make an overall M1 decision.
