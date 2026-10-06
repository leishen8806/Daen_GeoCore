# RUN-B-01 Independent Review Export

Exported sections of the previously completed independent review.

This is an export of the review I already completed. It is reproduced from my earlier output, with no new checks and no repository changes.

## 1. Exact Commit Reviewed

I reviewed the expected commit:

- **Evidence commit:** `b77b87f75a759a62fe64f42ada4d1b0180cd61fc` (16:33:37).
- **Input commit:** `f61516e4e84ce099fefbd8e2f374f0b1016887af` (16:32:51), an ancestor of the evidence commit.
- **Baseline:** `1175e75208e29c4a72ea668b0289cd2fd964afbb`, an ancestor of the input commit.
- **Starting and ending state:** branch `phase/04-m1-execution`, HEAD `b77b87f`, working tree clean.

## 2. Scenario Verdict and Acceptance Limits

**`PASS`**

The frozen outcome is supported:

- **Assertions remain attributable.** All 13 rows carry provenance that maps to the source map, and every pre-run row is intact.
- **Conflict does not silently create or merge Places.** The accepted Place set is unchanged and P17 has no Place, identity, link or resolution.
- **Quality is explicit.** All rows state `unknown`, verified by me because the checker did not.

**Acceptance limits.** Accepting Scenario B means only this. It does not establish:

- The conflict is **synthetic**. No conflict between real sources was exercised.
- P04's two coordinates differ by role and were not tested as a conflict.
- Quality is uniformly `unknown`, so Quality was not exercised as an informative property.
- Memo-level support is not exact original-webpage verification.
- The P04 photographs were not inspected.
- Selection, correction, conflict resolution, scope handling under §11.1, Access Point, and provider behavior were not tested.
- This run tests internal representation and retention of conflicting claims, not conflict prevalence, detection or source truth.

## 3. All Seven Findings

The operator reports no new execution friction. I found no observable decision that rises to model friction. I record the items below for transparency, with no inferred thoughts.

| # | Finding | Class | Evidence | Governing requirement | Effect on Scenario B outcome | Blocking? |
|---|---|---|---|---|---|---|
| **F1** | P03 appears twice as an identical assertion. The repeat must not be read as multiple or corroborating sources. | **EVIDENCE LIMITATION** (low) | `PRE-P03-SA1` and `POST-P03-SA2` | `inputs.md` P03 section; `source-map.md` P03-E1 | None. Attribution and Quality are intact, and no corroboration is claimed. | **No** |
| **F2** | **Traceability slip in `inputs.md`.** Its crosswalk says "Domain Model §10 / DM-10 concerns pickup/drop-off semantics". §10 is the Source Assertion Model, and DM-10 is invariant 10 (pickup/drop-off). The same file correctly calls §10 the Source Assertion model in an earlier bullet. | **REPORTING / TRACEABILITY ISSUE** (low) | `inputs.md`, crosswalk section, last bullet | Domain Model §10 and §27 item 10 | None. The correct requirements are identifiable and satisfied: M1-B5, M1-B10 and M1-B11, §4.2, §10, §17, §18, DM-5 and DM-6. `reviewer-packet.md` states them correctly. The scenario sheet's "invariants 5 and 10" shorthand is ambiguous between DM-10 and M1-B10 in the same way. I did not amend either file. | **No** |
| **F3** | One provenance label (`P04-FIELD-AP01`) covers the public address, the public reference coordinate and the verifier's observed coordinate, which come from different sources inside that record. They are distinguished by `role` and by the record itself, not by the label. | **EVIDENCE LIMITATION** (low) | `PRE-P04-SA1/SA2`, `POST-P04-SA3`; `source-map.md` | Domain Model §17 | None. All three are attributable to the frozen record. | **No** |
| **F4** | `role=observed-entrance` is a coordinate assertion on the Place, with the entrance meaning in free text. No Access Point object exists and none was inferred, which satisfies Domain Model §14 and invariant 9. In Scenario D the same real entrance will be represented as an Access Point, and how it relates to this assertion is undecided. | **EVIDENCE LIMITATION**, forward-looking | `POST-P04-SA3` | Domain Model §13, §14 | None for B. I do not call it model friction. | **No** |
| **F5** | Fixture vocabulary was added in free text, with no frozen meaning: `unresolved=true`, `access_point_object=not-created`, the role names, and `claim=`/`referent=` for P17. Unresolved status is established by the absence of any resolution, selection or supersession rows (verified), not by the flag. | **VALIDATION MEDIUM ISSUE** (low) | `POST-P17-SA1/SA2`, `POST-P04-SA3` | `inputs.md` handling instruction for P17 | None | **No** |
| **F6** | The disjointness of L1 and L2 lives only in `inputs.md`. A reader of the ledger alone sees "only L1, not L2" versus "only L2, not L1", which implies L1 ≠ L2, but cannot see that the premises are disjoint. | **EVIDENCE LIMITATION** (low) | `POST-P17-SA1/SA2`; `inputs.md` fixture background | Domain Model §4.2 | None. The run records the frozen background by reference. | **No** |
| **F7** | Quality is `unknown` on every row, including the two P17 rows that are conflicting by construction. Domain Model §18 is about being able to distinguish known, uncertain, stale or conflicting information in later designs. The ledger has no marker for it other than free text. This is permitted: scales are TBD and `unknown` is valid. | **EVIDENCE LIMITATION** (low) | All 13 rows | Domain Model §18; M1-B10 | None. Quality is explicit. It is uninformative. | **No** |

**Not findings (from the original review):**

- The P02 pair is not a conflict, and the run does not call it one.
- No business concept was needed, so M1-B11 holds.
- No concept outside the frozen nine was required.
- The pre-execution input blockers and their approved resolutions stay in `inputs.md`. I did not attribute them to execution.

## 4. Recommendation

`READY FOR HUMAN ACCEPTANCE OF SCENARIO B`

I recommend human acceptance with the seven findings above recorded as non-blocking limitations. F2 is a one-line traceability correction for the humans to dispose of, and F4 is worth carrying forward to Scenario D. I do not authorize a rerun, Scenario C, or any overall M1 GO / ITERATE / RETURN.
