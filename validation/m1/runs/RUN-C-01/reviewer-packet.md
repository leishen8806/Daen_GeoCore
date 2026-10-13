# RUN-C-01 — Reviewer Packet

> REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Frozen expectation

Scenario C — Current DAEN Representation Change; targets P04, P14 and P16.

Expected outcome: Current representation changes without destructive overwrite; prior material state remains traceable.

## Approved controlled inputs

Each target uses one synthetic mock source with an OLD and REVISED English display-name assertion. Both selections use the same Place, `fact=name`, `purpose=display-name`, `language=en` scope and Quality `unknown`. Replacement selections supersede only their prior selections.

Exact inputs and rationale: `inputs.md`.
Source and selector attribution: `source-map.md` and `operator-execution.md`.

## Evidence

- `pre-run-state.csv`
- `post-run-state.csv`
- `operator-execution.md`
- `source-map.md`
- `checker-fixture/state-ledger.csv`
- `checker-fixture/state-ledger-previous.csv`
- `checker-fixture/scenario-sheet.md`
- `raw-checker-output.txt`

## Reviewer checks requested

1. Confirm each replacement selection has the same Place, fact, purpose and language scope as its superseded selection.
2. Confirm supersession targets prior selections, not Source Assertions or Places.
3. Confirm OLD Source Assertions and OLD selection rows remain retained and unchanged.
4. Confirm P04 general-reference and entrance coordinates were untouched and not substituted.
5. Confirm P16 remains a synthetic case without a P15 merge.
6. Distinguish mock-source provenance from Codex/run/step selector attribution.
7. Treat checker output as structural evidence only; review scope and effective-selection meaning manually.

## Acceptance limits

Controlled name-correction inputs only; no new source verification; no coordinate-role substitution; no cross-language supersession; no general source ranking; no full Correction workflow; no P16 merge; no overall M1 decision.

## Decision state

The operator records evidence only. No semantic verdict is recorded.
