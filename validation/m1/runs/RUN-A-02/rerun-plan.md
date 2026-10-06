# RUN-A-02 — Authorized Scenario A Rerun Plan

> PRE-EXECUTION RERUN PLAN — NOT A SPECIFICATION.

- **Original run:** RUN-A-01, reviewed commit `b90a498c819b1f1c00e820b8031edc58223d739d`.
- **Targets:** P01 and P02 only.
- **Expected outcome:** Unchanged frozen Scenario A outcome: one Place and one fixture identity remain stable while representations and Source Assertions may vary.
- **Initialization scope:** Scenario-local minimum state for P01/P02. The earlier run instruction requested this minimum state while the broader initial-state plan describes full M1 preparation; this is an execution-procedure clarification, not a model defect.
- **Representation changes:** P01 uses two existing name representations from frozen evidence; P02 keeps English and adds the supported Khmer representation. No historical rename, correction, merge, split, closure or Access Point event is introduced.
- **Concept separation:** Place identity, Source Assertion and Current DAEN Representation are separate ledger entries using the existing fixture conventions. No new columns or parser syntax are introduced.
- **Source references:** Every non-empty provenance label maps to the run-local source map and frozen repository evidence.
- **Language and synthetic marking:** P01/P02 public claims remain `REAL`; controlled selection changes are marked `SYNTHETIC` where represented as experimental operations. Language coexistence does not supersede the English assertion.
- **Checker command:** `python validation/m1/checker/check_m1.py --fixture validation/m1/runs/RUN-A-02/checker-fixture`; previous snapshot input is `state-ledger-previous.csv`.
- **Manual review:** Reviewer must inspect locus-based identity, assertion retention, selection scope, provenance meaning, Quality meaning and checker limitations.

No scenario result exists yet. No semantic verdict is assigned by this plan.
