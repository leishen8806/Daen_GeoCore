# RUN-B-01 — Reviewer Packet

> REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Frozen authority

- Input record: `inputs.md` (commit `f61516e`)
- Frozen Scenario B: `validation/m1/scenario-sheet.md`
- Expected outcome unchanged: assertions remain attributable; conflict does not silently create or merge Places; Quality is explicit.
- Relevant Domain Model: §4.2 Source Assertion, §10 Source Assertion Model, §17 Provenance, §18 Data Quality; DM-5 and DM-6.
- Relevant M1 checks: B5 Assertion attribution, B10 Explicit quality, B11 No business dependency.

## Coverage

- P02: English and Khmer name assertions with explicit language context.
- P03: supported frozen name assertion only; no invented address or coordinate.
- P04: frozen address plus general-reference and observed-entrance coordinate roles; no Access Point object.
- P17: two synthetic exclusive claims over the same raw record/time/role, retained unresolved.

## Evidence references

- `pre-run-state.csv`
- `post-run-state.csv`
- `source-map.md`
- `operator-execution.md`
- `checker-fixture/state-ledger.csv`
- `checker-fixture/state-ledger-previous.csv`
- `checker-fixture/scenario-sheet.md`
- `raw-checker-output.txt`

## Reviewer checks requested

1. Verify every assertion is attributable and has explicit Quality.
2. Verify REAL/SYNTHETIC classification and source-map limitations.
3. Distinguish P04 coordinate roles from an Access Point operation.
4. Confirm P17's two claims are a genuine unresolved conflict under §4.2 without a new Place, mapping, merge or split.
5. Confirm the accepted Place identity set is unchanged before and after.
6. Confirm no selection, correction, lifecycle or source-ranking action occurred.
7. Review the checker result only as structural evidence and apply the manual semantic review independently.

## Decision state

The operator records evidence only. Independent review and any later scenario decision remain open.
