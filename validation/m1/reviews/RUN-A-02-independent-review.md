Checks are done. Before I write the review, I'm reading the committed Constitution, which I haven't opened yet.

I'm now writing up the RUN-A-02 review from the evidence I've read and checked.

## RUN-A-02 Independent Review

**Verdict: PASS.** The pre-registered Scenario A outcome holds, and the RUN-A-01 conflation defect is fixed. Four narrower points stay open and need a human ruling (section "Findings"), so I recommend escalation for domain review rather than plain acceptance.

## Exact Commit Reviewed

`7a691dc62541bfeefb66bbb7284bbfafb16fa223`, read as committed content with `git show`.
- Pre-execution rerun-plan commit `7200747` is an ancestor of it.
- Original failed run: `b90a498`.
- Local HEAD happens to equal the evidence commit.
- `git fetch origin` printed nothing.

## Evidence Reviewed and Checks Actually Performed

**Read from the exact commit:**
- All ten RUN-A-02 files: `rerun-plan.md`, `source-map.md`, both state CSVs, `operator-execution.md`, `raw-checker-output.txt`, `reviewer-packet.md`, and the three `checker-fixture/` files.
- `reviews/RUN-A-01-disposition.md`, the Domain Model, `scenario-sheet.md`, `runbook.md`, `manual-review-matrix.md`, `corpus-evidence.md`, `source-assertion-plan.md`, `checker/RULES.md` and `check_m1.py`.
- The Constitution, read last and only for clauses on provenance, scope admission and quality (lines 181, 262, 380–389). It did not change my analysis.

**Checks I performed myself:**
- `git diff` across the commit range for the frozen files and the RUN-A-01 directory.
- `cmp` on committed bytes for every snapshot pair.
- **I ran the checker myself**, on a scratch copy extracted with `git archive` into the scratchpad. Output was `PASS`, exit 0.
- I ran the checker's self-test on that copy. Known-good passed, and each known-bad fixture I saw was detected by its expected rule.
- I ran two mutations on scratch copies: removing the cross-language supersedes link, and giving two entries wrong-type `ref=` targets. The checker passed both.

After all this, `git status` is empty, the branch is `phase/04-m1-execution` and HEAD is `7a691dc`. No repository file was edited.

## Frozen-file and Original-run Integrity

| Check | Result |
|---|---|
| RUN-A-01 directory unchanged `b90a498` → `7a691dc` | **Yes**, empty diff |
| Rerun plan existed before the evidence commit | **Yes.** Committed in `7200747` at 15:45:15, evidence at 15:46:26, and the file is byte-identical in both. |
| Scenario sheet, checker (source, rules, self-test fixtures), Constitution, Domain Model unchanged since `b90a498` | **Yes**, empty diff |
| Scenario A targets and expected outcome unchanged | **Yes.** Run sheet, checker sheet and frozen sheet are byte-identical (SHA-256 `88822666…d5b13`). |
| `corpus-evidence.md` P01 and P02 sections, which the source map cites at `dcd7db6` | **Identical.** The file changed once since then (`e897ea7`, field-verification wording for P04, P09–P11, P13) but not these sections. |
| `runbook.md` | Changed only in `9be78e4`, before `b90a498`, and not since |

## Original-defect Resolution Table

| # | Defect | Status | Evidence |
|---|---|---|---|
| 1 | Place / Source Assertion / Current DAEN Representation separation | **RESOLVED** | Separate entries: Place (`PRE-P01-PLACE`), assertion (`PRE-P01-SA1`, `ref=FIX-ID-P01`), selection (`PRE-P01-CR`, `ref=…-SA1`). Same pattern for P02 and for `POST-*`. |
| 2 | Locus-based identity justification | **RESOLVED**, with an evidence limitation | `reviewer-packet.md` cites the locus rule and the frozen evidence for each Place. Limitation: `locus=` is a name-derived string ("Central Post Office Phnom Penh"), not an independent locator. The frozen memo does not state explicitly that the two P01 names denote one building. |
| 3a | Provenance labels trace | **RESOLVED** | All four labels (`P01-E1/E2`, `P02-E1/E2`) appear in `source-map.md` and map to unchanged memo sections. |
| 3b | Exact claim appears at the cited URL | **INSUFFICIENT EVIDENCE** | See "Provenance and Quality Review". |
| 4 | Explicit Quality and retained uncertainty | **RESOLVED** | `unknown` on every row. Uncertainty is carried in the source-map limitations column (not in the ledger rows). |
| 5 | English/Khmer **assertion** coexistence | **RESOLVED** | `PRE-P02-SA1` (en) kept, `POST-P02-SA2` (km) added, no supersedes on the new assertion. |
| 6 | English/Khmer **selection** coexistence | **UNRESOLVED** | See next section. |
| 7 | REAL/SYNTHETIC marking of selections | **UNRESOLVED** (partly) | `POST-*-CR` marked `SYNTHETIC` is supported. `PRE-*-CR` marked `REAL` is not supported by frozen evidence (below). |
| 8 | Historical rows preserved | **RESOLVED** | The first six lines of the post ledger equal the pre-run file byte-for-byte (`cmp`). Old selection markers were left unchanged, as instructed. |
| 9 | Previous snapshot supplied for VM-I01 | **RESOLVED** | `state-ledger-previous.csv` is byte-identical to `pre-run-state.csv`. `check_append_only` runs when that file exists, and the self-test shows VM-I01 detecting a violation. |
| 10 | Truthful reporting of retrospective vs new friction | **UNRESOLVED** | See "Friction / Reporting Review". |

## P02 Assertion versus Current-selection Coexistence

| Q | Answer |
|---|---|
| **A.** Do the English and Khmer Source Assertions coexist? | **Yes.** `PRE-P02-SA1` and `POST-P02-SA2` both reference `FIX-ID-P02`. Neither supersedes the other. |
| **B.** Do the two current selections coexist? | **Not established.** Both CR entries are retained, but retention is not effectiveness. |
| **C.** Does the supersession link replace the English selection? | **On its face, yes.** `POST-P02-CR` (language=km) carries `supersedes_reference = RUN-A-02:PRE-P02-CR` (language=en). Domain Model §19 and §26 give supersession the meaning "replaced by a later representation". The row's own `selection=coexisting-language-test` label says the opposite. |
| **D.** Is the "coexisting language scopes" claim supported? | **At assertion level, yes. At selection level, not without an interpretation.** The operator's written claims (`rerun-plan.md`, `operator-execution.md` step 5) are about assertions and are accurate. The label on the selection row goes further than its link supports. |
| **E.** Does answering need an unstated interpretation? | **Yes.** |

**The exact ambiguity.** Domain Model §11 defines a representation "for a defined scope". Neither §19 nor §26 says whether supersession applies only within one scope. Two readings are available:
- **Scope-relative:** a km selection cannot replace an en selection, so both are effective and the supersedes link is spurious.
- **Literal:** the km selection replaces the en selection, so only km is effective.

The model does not choose, and I have not invented a rule. The checker passes both encodings: removing the link on a scratch copy also gave `PASS`.

**Why this does not change the verdict.** Under either reading, Place identity is unchanged, both assertions are retained and the representation varied. The expected outcome holds either way. It does matter for Scenarios C and F, which rely on supersession.

## Selection Scope and REAL/SYNTHETIC Review

**Initial selections `PRE-P01-CR` and `PRE-P02-CR` (marked `REAL`):**
- The frozen evidence supports `REAL` only for the underlying name assertions. `source-assertion-plan.md` states it "does not select a Current DAEN Representation".
- A Current DAEN Representation is DAEN's own selection (Domain Model §4.3), not a public source's claim. These two entries are controlled initial selections made for the experiment (`selection=initial`).
- The same kind of operator-created selection is `SYNTHETIC` in the post-run rows, so the marking is inconsistent.
- I do not suggest the public name assertions should become synthetic. The fixture does not make them so.
- No frozen convention defines how to mark a selection, so this is partly a medium gap and partly an execution inconsistency.

**P01 scope:**
- `PRE-P01-SA1` and `PRE-P01-CR` carry no `language`. `POST-P01-SA2` and `POST-P01-CR` carry `language=en`.
- `operator-execution.md` step 4 calls both P01 names "English name assertions", but only the second is encoded as English.
- No frozen convention says what an omitted language means (unspecified, any, or en). I am not supplying a default, so the effective scope of the first P01 selection is **not clear from the frozen conventions**.
- The impact is small because the explicit supersedes link makes `POST-P01-CR` the effective selection, but this is an unreported convention.

## Provenance and Quality Review

**What is supported:**
- Each label maps to a memo section, and the source map's own limitation column is honest. P01-E2 says it "supports representation for this run, not a dated real-world rename event".
- `public-source` is described as a provenance category and not a reliability judgment.
- `unknown` Quality is permitted and explicit.

**Supported by the frozen memo only (not by the cited URL):**
- The exact string "Cambodia Post Central Post Office" attributed to the Cambodia Post locations page (P01-E2).
- The Khmer name attributed to `royalpalacephnompenh.com/km` (P02-E2).
- Why: `source-assertion-plan.md` calls the first one a "research display name", and `corpus-evidence.md` lists names and sources side by side without tying each name to a URL.
- No new research is authorized, so **source-specific attribution is not established**, and I do not claim it is wrong.

**Who or what selected the representation:** the selection entries reuse the source label (`P01-E1`, `P02-E2`) as provenance, and nothing in the ledger rows records who or what made the selection. The run id and `operator-execution.md` (operator "Codex") give run-level attribution only. This is a limitation of the fixture convention, not something I resolve with a governance rule.

## Identity and Business-boundary Review

- **P01 and P02 stayed the same locus.** The Place entries are byte-unchanged and identity strings are stable. No new Place is created. No identity-bearing change is hidden in a representation row.
- **The locus rule is cited and supported** in `reviewer-packet.md`, with the limitation above.
- **Provider independence:** not exercised. No provider/reference assertion exists, and Scenario A allows "names, scripts OR references".
- **No business entity, policy, verdict or occupant identity was needed.** The "Cambodia Post" prefix is a name assertion and does not touch identity.
- **No concept outside the frozen nine was required.**

## Checker Coverage and Limitations

**Checker-supported (structural), re-observed by my own run:**
- M1-M01 identity strings consistent per label (trivially so, since identity is stated once per Place).
- M1-M03 provenance present, M1-M04 Quality present, M1-M05 supersedes references resolve, M1-M06 concept vocabulary, M1-M07 `ref=` targets exist.
- VM-I01 append-only, **actually exercised** this time because the previous snapshot was supplied.
- VM-I02 scenario sheet intact.

**Reviewer-verified comparisons:** all four byte comparisons in the integrity section, plus the six retained pre-run lines.

**Manual semantic judgments (mine):** concept separation, locus continuity, assertion coexistence, selection reading, REAL/SYNTHETIC marking, provenance meaning.

**Not established by a green checker:**
- Language coexistence. The mutation with the link removed also passes.
- Whether `ref=` targets have the right concept type. A mutation that points a selection at another selection and an assertion at a selection also passes.
- Whether a provenance label points to real evidence.
- Correct synthetic marking, and any semantic Scenario A success.

## Friction / Reporting Review

The operator reports no new friction, and the shared Friction Log has zero entries and no pointer to RUN-A-01's retrospective findings. I do not infer what the operator privately thought. The evidence itself contains decisions no one logged:

1. Placing a `supersedes_reference` on a selection whose language scope differs from its target (`POST-P02-CR`).
2. Leaving `language` off the first P01 entries while calling both names English.
3. Marking initial selections `REAL` and later selections `SYNTHETIC`.

Each fits the log's trigger questions ("Can the current model represent this case?", "What object should this be?"). I do not call this an invented rule. I call it unreported encoding decisions.

**Bookkeeping, separate from the domain question:** `RUN-A-01-disposition.md` summarizes the verdict but does not record the retrospective friction (the quiet supersession rule I identified in RUN-A-01). Nothing in the shared log points to it. That is a reporting gap, not a domain failure, and the review pretends no friction was logged during RUN-A-01.

## Findings with Severity and Exact Evidence

| # | Finding | Severity | Class | Evidence |
|---|---|---|---|---|
| F1 | Cross-scope supersession: effective selection state depends on an unstated reading of supersession vs scope; label contradicts link | **Medium** | MODEL FRICTION candidate (Domain Model §11, §19, §26 silent on scope-relativity), plus EXECUTION ERROR (link encoding contradicts the stated intent) | `POST-P02-CR` row; sensitivity run |
| F2 | `PRE-*-CR` marked `REAL`, unsupported by frozen evidence; inconsistent with `POST-*-CR` marked `SYNTHETIC` | **Medium** | EXECUTION ERROR with a VALIDATION MEDIUM ISSUE (no convention for marking selections) | `PRE-P01-CR`, `PRE-P02-CR`; `source-assertion-plan.md` header |
| F3 | First P01 entries have no language, described as English; omitted-language meaning not defined | **Low** | EXECUTION ERROR / unreported convention | `PRE-P01-SA1`, `PRE-P01-CR`; `operator-execution.md` step 4 |
| F4 | Source-specific attribution of exact strings not established | **Low** | EVIDENCE LIMITATION | `source-map.md` P01-E2, P02-E2 |
| F5 | Ledger records no selector attribution; selection rows reuse the source label | **Low** | VALIDATION MEDIUM ISSUE | `POST-*-CR` provenance column |
| F6 | Checker blind spots: scope-aware supersession, concept-typed references | **Low** | VALIDATION MEDIUM ISSUE | Sensitivity runs |
| F7 | Unreported encoding decisions; shared log lacks pointer to retrospective RUN-A-01 findings | **Medium** | REPORTING ISSUE | Friction log; disposition record |
| F8 | `locus=` is a name-derived string; P01 name equivalence rests on the memo | **Low** | EVIDENCE LIMITATION | `PRE-P0x-PLACE` rows |

**Severity basis.** None of these changes whether identity stayed stable. F1 and F7 are the two I would not let pass silently, because C and F will meet the same supersession question.

## Scenario Verdict

`PASS`

**Why PASS and not FAIL:**
- The pre-registered outcome holds. One Place and one fixture identity per target stay stable, and representations and assertions varied.
- The RUN-A-01 defect that drove FAIL (concept collapse) is resolved.
- Every Place and assertion row is retained, the previous snapshot was supplied, and the append-only check ran.
- No required invariant is violated.
- F1 to F8 concern the selection layer, marking conventions and reporting. They do not alter the outcome under either reading of F1.

**What PASS does not claim:** selection coexistence, correct synthetic marking of selections, source-specific attribution, or any Scenario B–J result.

**Why not INEXPRESSIBLE:** the case is expressible. Omitting the supersedes link on `POST-P02-CR` would have expressed it cleanly. F1 is therefore a model-ambiguity candidate for humans to rule on, not a reason to say the scenario cannot be expressed.

## Recommendation

`ESCALATE FOR HUMAN DOMAIN REVIEW`

I recommend escalation because F1 is a Phase 03 clarification question, and F2 and F7 need human dispositions:
1. Whether supersession in Domain Model §19/§26 is scope-relative. I have not decided this.
2. How a controlled selection should be marked REAL or SYNTHETIC.
3. Whether the unreported decisions (F1, F3, F2) belong in the Friction Log, and the pointer to RUN-A-01's retrospective findings.

I do not authorize RUN-A-03 or Scenario B, and I do not decide M1 GO / ITERATE / RETURN. The one authorized rerun is used.

`RUN-A-02 INDEPENDENT REVIEW COMPLETE — WAITING FOR HUMAN DECISION`