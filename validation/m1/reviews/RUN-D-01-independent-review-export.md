# RUN-D-01 Independent Review Export

Exported sections of the completed RUN-D-01 independent review. This is not the complete original review transcript.

## 1. Exact Commit Reviewed

I reviewed the expected commits. There is no discrepancy.

- **Evidence commit:** `281d2f02b945519491376f64aa54afa23b6523a7` (2026-10-07 09:34:33).
- **Input-freeze commit:** `a62bd735df7c1b6b1297ed046a382ce9bdade788` (09:32:22), an ancestor of the evidence commit.
- **Scenario C acceptance baseline:** `df9fb2f6e3bfdfb9cccb66ad6f4d44b5afc2cf28`, an ancestor of the input commit.
- The three are distinct commits. I read committed content from the evidence commit, not a moving HEAD.
- Starting state: branch `phase/04-m1-execution`, HEAD `281d2f0`, clean working tree.

## 2. Scenario Verdict and Acceptance Limits

**`PASS`**

The approved D outcome is faithfully supported within this controlled synthetic test:

- **Access Point remains a separate object.** Two rows have the concept `Access Point`. They are distinct from Place rows, coordinate assertions, selections and the access assertions they reference, and they use a separate handle namespace.
- **It is not inferred solely from the coordinate.** The access function and location were separately specified before the AP existed, are retained in PRE, and are reproduced in POST. The access coordinates are not reproducible from the selected coordinates by one fixed rule.
- **The Access Point differs from the Selected Coordinate**, for all three Places.
- **Nothing else moved.** Place identities, selections and PRE rows are unchanged, and no excluded operation occurred.

**Acceptance limits.** Accepting Scenario D means only this. It does not establish:

- Physical or real-world accessibility, a real RUPP gate, or independent real-world evidence. All new D facts are synthetic.
- Scenario E. The overlap is noted but E's frozen target is untested.
- Production geometry, a coordinate reference system, precision or distance thresholds, or a public AP namespace.
- How a real observed-entrance coordinate assertion (as in P04) maps to an AP.
- Selection of an AP coordinate as a Current DAEN Representation, and AP correction, lifecycle or supersession.
- Any mechanical validation of AP relationships. They were checked manually.
- Provider behavior, routing, pickup/drop-off, or business semantics.
- Any overall M1 result.

## 3. Complete Findings Table

No new execution friction was reported, and I found no observable decision that is a domain question.

| ID | Finding | Evidence | Governing requirement | Classification and severity | Effect on frozen D outcome | Blocking? |
|---|---|---|---|---|---|---|
| **RUN-D-01:F1** | Two `source-map.md` rows (`D-PLACE-P06`, `D-PLACE-P07`) carry a 39-character baseline SHA that omits "a" (`…66d6f4…` for `…66ad6f4…`), which is not a valid Git object. The `SYN-D-*` rows say the input-freeze commit is "recorded after creation" and never name `a62bd73`. The correct baseline is unambiguous elsewhere, and `operator-execution.md` names the input commit. | `source-map.md` "Existing Place context" table (P06 and P07 rows) and "Approved mock inputs" table | Domain Model §17; M1-B9 | **REPORTING / TRACEABILITY ISSUE**, Low | None. The cited source texts are unchanged and identifiable. | **No** |
| **RUN-D-01:F2** | Selector aliases `STEP-1-P05/P06/P07` are not defined in `operator-execution.md`. Attribution is supported at operator, run and ledger-row level through the row keys listed in the attribution section, not at an alias level. | `PRE-P05-SEL`, `PRE-P06-SEL`, `PRE-P07-SEL`; `operator-execution.md` "Attribution and classification" | Domain Model §11, §17 | **REPORTING / TRACEABILITY ISSUE**, Low | None. Each selection is identifiable by its row, and the Access Point rows are attributed through the same section. | **No** |
| **RUN-D-01:F3** | The served-place relationship is encoded in free text and is not validated by any checker. The PRE access assertions use slot names (`served_places=P05\|P06`, `served_place=P07`) with no `ref=` to a Place. The POST AP rows use repeated `served_place=FIX-ID-…` keys. A naive key-value parse would drop one of the two shared-AP associations. I resolved both manually and the sets match. | `PRE-AP-SHARED-SA`, `PRE-AP-P07-SA`, `POST-AP-SHARED`, `POST-AP-P07` | Domain Model §14 (one AP MAY serve multiple Places) | **VALIDATION MEDIUM ISSUE**, Low | None. The relationships are understandable in the approved medium and verified. | **No** |
| **RUN-D-01:F4** | "Independent" access evidence is separately specified synthetic fixture text, authored in the same frozen input record as the coordinates. It is not independent real-world verification. The AP rows repeat the assertions' coordinates and types and add no new information beyond them. | `inputs.md` "Exact access statements"; `POST-AP-*` rows | Domain Model §14, M1-B6 | **EVIDENCE LIMITATION**, Low (accepted synthetic-data limitation) | None. The test was approved on this basis. | **No** |
| **RUN-D-01:F5** | **Carry-forward from B:F4, partly addressed.** In this run the Place-reference coordinates (`purpose=place-reference`) stay separate from the access assertions and AP objects, and no entrance-role coordinate assertion is attached to a Place. How P04's earlier `role=observed-entrance` coordinate assertion in RUN-B-01 relates to any Access Point is **not addressed**, because P04 is supporting context only and no AP was created for it. | `PRE-P0x-REF` rows; `RUN-B-01-disposition.md` F4 | Domain Model §13, §14 | **EVIDENCE LIMITATION**, forward-looking, Low | None for D. | **No** |
| **RUN-D-01:F6** | **Scenario E overlap.** The shared AP across P05 and P06 is approved fixture context. E's frozen target slot is P07 only, and the P07 AP here serves only P07. D therefore does not execute E as frozen. | `POST-AP-SHARED`; frozen Scenario E entry and runbook row 5 | M1-B7 | **EVIDENCE LIMITATION**, Low | None. D's outcome does not depend on E. | **No** |

## 4. Recommendation

`READY FOR HUMAN ACCEPTANCE OF SCENARIO D`

I recommend human acceptance with the six findings recorded as non-blocking. F1 and F2 are traceability corrections for the humans to dispose of, and F5 and F6 are worth carrying forward. I do not authorize a rerun or Scenario E, and I do not issue any overall M1 GO / ITERATE / RETURN.
