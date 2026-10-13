# RUN-H-01 — Reviewer Packet

REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Authority and scope

- Approved target erratum: `validation/m1/errata/SCENARIO-H-TARGET-ERRATUM.md`
- Erratum commit: `6b572bc5ba03f275d25a21f727515128326a7d73`
- Input freeze: `a0424803269f11805a46f5d2453b0c3fba90c44a`
- Historical targets: P10/P11
- Effective targets: P17/P18
- Original frozen scenario-sheet and runbook remain unchanged; the erratum controls this run only.
- Capacity interpretation: 20 original corpus slots plus 3 resulting fixture identities = 23 local identities/records where applicable.

## Controlled decisions under review

- P17 is a synthetic mis-conflation: P17 Locus A remains `FIX-ID-P17`; Locus B receives new `FIX-ID-H-P17-B`.
- P18 is a synthetic true division: parent `FIX-ID-P18` remains historical/resolvable; children `FIX-ID-H-P18-A` and `FIX-ID-H-P18-B` are new and do not inherit the parent identity.
- M and T are isolated alternative worlds, not sequential mutations.

## Evidence

- `inputs.md`
- `source-map.md`
- `operator-execution.md`
- `misconflation/pre-run-state.csv` and `post-run-state.csv`
- `misconflation/checker-fixture/state-ledger.csv` and `raw-checker-output.txt`
- `true-division/pre-run-state.csv` and `post-run-state.csv`
- `true-division/checker-fixture/state-ledger.csv` and `raw-checker-output.txt`
- byte-identical copied scenario sheets in both checker fixtures

## Relationship checks

| Subcase | Historical/original | Resulting identity or identities | Resolution Link | Succession |
|---|---|---|---|---|
| M mis-conflation | `FIX-ID-P17` / Locus A | `FIX-ID-H-P17-B` / Locus B | `FIX-RES-H-MIS-P17-B` | none |
| T true division | `FIX-ID-P18` | `FIX-ID-H-P18-A`, `FIX-ID-H-P18-B` | `FIX-RES-H-DIV-P18-A/B` | `FIX-SUCC-H-DIV-P18-A/B` |

## Manual review checklist

- Verify each PRE prefix is preserved in POST.
- Verify M retains P17’s original identity and creates a distinct B identity.
- Verify the old B assertion is retained and the new B assertion explicitly supersedes it.
- Verify T preserves the historical parent, creates two distinct children, and marks both historical resolutions.
- Verify each Succession reference points to its matching Resolution Link.
- Verify M and T remain isolated and are not combined into one ledger.
- Treat checker output as structural evidence only.

## Checker outputs

- `misconflation/raw-checker-output.txt`: expected structural PASS.
- `true-division/raw-checker-output.txt`: expected structural PASS.

## Limits and acceptance boundary

All fixtures are synthetic. This run does not establish real-world split detection, production lifecycle behavior, production GeoID encoding or policy, merge behavior, provider trust ranking, legal/privacy handling, or a general same-Place algorithm. The P17 separation choice is fixture-specific. The P18 child relationships are controlled validation results. Resolution Link and Succession encodings are validation notation, not an API or schema decision. No overall M1 result is created.

## Decision state

Reviewer verdict: ____________________

PASS / FAIL / INEXPRESSIBLE: ____________________

The operator records evidence only. No GO, ITERATE or RETURN decision is made here.
