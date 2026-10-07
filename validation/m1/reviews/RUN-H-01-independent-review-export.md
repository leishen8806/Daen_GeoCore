# RUN-H-01 Independent Review Export

This file is an archival excerpt of the completed independent review. It is not a new review.

## Review anchors

- Evidence: `9bc78b883fbe026477634227614134ca2a122944`
- Input freeze: `a0424803269f11805a46f5d2453b0c3fba90c44a`
- Target erratum: `6b572bc5ba03f275d25a21f727515128326a7d73`
- G acceptance baseline: `f46a610f9fa6b695c52ab10e6e20a97fb9d1d49a`
- Verdict: `PASS`
- Recommendation: `READY FOR HUMAN ACCEPTANCE OF SCENARIO H`

## Findings

### RUN-H-01:F1

Cross-subject Source Assertion supersession: the new Locus-B assertion references `FIX-ID-H-P17-B` but supersedes the historical Locus-B assertion that referenced `FIX-ID-P17`.

Classification: `MODEL FRICTION`, Low, single instance. Blocking: No. Effect: None on the frozen H outcome. This interpretation is accepted for RUN-H-01 only and MUST NOT silently be generalized.

### RUN-H-01:F2

P18 historical/superseded parent state is derived from Resolution Links and Succession rather than marked directly on the parent Place row.

Classification: `VALIDATION MEDIUM ISSUE`, Low. Blocking: No.

### RUN-H-01:F3

One-to-many true-division semantics use two Resolution Links sharing the historical parent, `split_group` and `result_count=2`, plus two Succession rows. These semantic fields are free-text validation notation and are not mechanically checked.

Classification: `VALIDATION MEDIUM ISSUE`, Low. Blocking: No.

### RUN-H-01:F4

Split premises are frozen in inputs rather than ledger rows. The P18 division premise label is mapped but unused by ledger rows; the P17 true-original-locus choice appears in the Resolution Link.

Classification: `EVIDENCE LIMITATION`, Low. Blocking: No.

### RUN-H-01:F5

The 20-to-23 statement is bookkeeping across isolated split subcases, not a materialized 23-Place runtime state. Three new result identities equal 23 minus 20, but no single ledger contains 23 Places.

Classification: `EVIDENCE LIMITATION`, Low. Blocking: No.

### RUN-H-01:F6

Traceability: `source-map.md` does not name the exact H input-freeze SHA; frozen “invariants 1 and 3” shorthand is ambiguous between Domain Model numbering and M1 B-numbering.

Classification: `REPORTING / TRACEABILITY ISSUE`, Low. Blocking: No.

### RUN-H-01:F7

Historical-document discrepancy: the earlier `M1_CORPUS_PLAN.md` assigns P10/P11 to split, P17 to ambiguous/shared address and P18 to containment, while later 04C corpus artifacts assign P17/P18 to H. The H erratum leaves the historical file unchanged.

Classification: `REPORTING / TRACEABILITY ISSUE`, Low. Blocking: No.
