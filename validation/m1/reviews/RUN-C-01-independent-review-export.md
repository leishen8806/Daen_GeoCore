# RUN-C-01 Independent Review Excerpt

Selected original passages from the completed RUN-C-01 independent review. This is an excerpt, not the complete original report.

## RUN-C-01 Independent Review

**Verdict: PASS.** In this controlled test the replacement selection supersedes the old selection within the same explicit scope. Nothing is erased, and the chain from the new selection back to the old value, source label and instant is traceable. Three traceability defects remain and none blocks the outcome. The humans should dispose of them.

## Exact Commit Reviewed

- **Evidence commit:** `77a3ec351c0120855b1569e06781813c7d163a34` (2026-10-06 17:18:33).
- **Input-freeze commit:** `32b0708460ede4de3e0601f8570e29bbae5ddd2f` (17:17:35), an ancestor of the evidence commit.
- **Scenario B acceptance baseline:** `e26be48851892a37f222d37569acfe1f3ddc68d2`, an ancestor of the input commit.
- **The three are distinct commits.** Only `32b0708` is the input freeze.

## Selected Finding Passages

### RUN-C-01:F1

The Place rows' provenance labels `C-PLACE-P04/P14/P16` have no mapping in the run package or frozen evidence. The association is implicit only.

Classification: REPORTING / TRACEABILITY ISSUE, Low.
Blocking: No.

### RUN-C-01:F2

The selector strings carry `STEP-C-*` labels that exist only in the ledger. `operator-execution.md` defines none, although `inputs.md` and `source-map.md` state the exact step is recorded there. Selection attribution is reliable at run, operator and ledger-row level but not at the promised step level.

Classification: REPORTING / TRACEABILITY ISSUE, Medium.
Blocking: No.

### RUN-C-01:F3

`source-map.md` cites `inputs.md` at "baseline `e26be48`". `inputs.md` did not exist at that commit; it was added in `32b0708`.

Classification: REPORTING / TRACEABILITY ISSUE, Low.
Blocking: No.

### RUN-C-01:F4

The correction that triggers the selection change is recorded only in prose (`inputs.md`, `operator-execution.md`). The ledger has no Correction entry, and the REVISED assertion carries no marker that it corrects the OLD one. The relation exists only through the selection chain and `instant=TEST-C0`/`TEST-C1`.

Classification: EVIDENCE LIMITATION, Low.
Blocking: No.

### RUN-C-01:F5

Scope and effective state are not carried by a field. Scope is free text on both ends, and all six selection rows retain `current_representation=true`, so the effective selection is derived only from the supersession relation. This is the approved procedure, not a failure.

Classification: VALIDATION MEDIUM ISSUE, Low.
Blocking: No.

### RUN-C-01:F6

The checker confirms that references exist and resolve to earlier entries. It does not check reference type, scope equality or effective-selection meaning. For this run, correctness of the selection→selection supersession rests entirely on manual verification.

Classification: VALIDATION MEDIUM ISSUE, Low.
Blocking: No.

## Scenario Verdict

**`PASS`**

The frozen outcome is supported within the approved controlled-test scope:
- **Current representation changes.** Each REVISED selection supersedes the prior selection within the same explicit scope, and the three effective values are the REVISED ones.
- **No destructive overwrite.** All nine PRE rows are unchanged and retained. The OLD assertions and OLD selections remain.
- **Prior material state is traceable.** The REVISED selection points to the OLD selection, which points to the OLD assertion, which carries its value, instant and mock-source label.
- **Identity stable.** The three Places are unchanged and nothing was merged.

## Recommendation

`READY FOR HUMAN ACCEPTANCE OF SCENARIO C`

I recommend human acceptance with the six findings recorded as non-blocking. F1 to F3 are traceability corrections the humans should dispose of, and F2 is the one closest to the material change. I do not authorize a rerun, Scenario D, or any overall M1 GO / ITERATE / RETURN.
