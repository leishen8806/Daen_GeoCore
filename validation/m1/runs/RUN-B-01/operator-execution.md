# RUN-B-01 — Operator Execution Record

> RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity

- **Run ID:** `RUN-B-01`
- **Role:** M1 Data Operator — Codex
- **Targets:** P02, P03, P04, P17 only
- **Input freeze:** `f61516e`
- **Baseline:** `1175e75` / `1175e75208e29c4a72ea668b0289cd2fd964afbb`
- **Fixture handles:** `FIX-ID-P02`, `FIX-ID-P03`, `FIX-ID-P04` — local validation stand-ins, not GeoIDs.

## Actions performed

1. Materialized the minimum pre-run state for P02, P03 and P04. No P17 Place row or `FIX-ID-P17` was created.
2. Preserved the pre-run rows unchanged.
3. Added P02 Khmer name context, P03 supported name evidence, and P04 address/coordinate assertions according to `inputs.md`.
4. Added both approved P17 synthetic Source Assertions. The claims share raw record, test instant and association role but refer exclusively to L1 and L2; they remain unresolved.
5. Created no Current DAEN Representation selections, no `current_representation=true` flags, no Access Point object, no correction, merge, split, lifecycle event or source ranking.

## Per-assertion provenance and Quality checklist

| Assertion group | Provenance present | Quality explicit | Classification | Manual status |
|---|---|---|---|---|
| P02 English / Khmer names | YES | `unknown` | REAL | Pending independent review |
| P03 supported name | YES | `unknown` | REAL | Pending independent review |
| P04 address / general coordinate / observed-entrance coordinate | YES | `unknown` | REAL | Coordinate roles distinguished; pending independent review |
| P17 Source A / Source B | YES | `unknown` | SYNTHETIC | Both retained unresolved; pending independent review |

## Checker invocation

- **Runtime:** Python 3.15.0a2
- **Invocation:** `python validation/m1/checker/check_m1.py --fixture validation/m1/runs/RUN-B-01/checker-fixture`
- **Exit code:** `0`
- **Raw output:** `raw-checker-output.txt` (unedited)
- **Checker-supported checks exercised:** ledger vocabulary, identity consistency, provenance presence, reference resolution, supersession/append-only structure (no prior snapshot mutation), and frozen scenario-sheet integrity.
- **Not exercised by M1-M04:** because no Current DAEN Representation selection exists, M1-M04 did not validate every Source Assertion's Quality. The per-assertion checklist above is operator evidence only.

Checker output is structural evidence. It does not establish source truth, conflict meaning, REAL/SYNTHETIC correctness or a semantic Scenario B result.

## Snapshot evidence

- `pre-run-state.csv` is copied byte-for-byte to `checker-fixture/state-ledger-previous.csv`.
- `post-run-state.csv` is copied byte-for-byte to `checker-fixture/state-ledger.csv`.
- Frozen `validation/m1/scenario-sheet.md` is copied byte-for-byte to `checker-fixture/scenario-sheet.md`.
- Pre-run rows remain unchanged in post-run state; added rows are append-only evidence.

## Friction and boundary

No new execution friction was observed. The earlier input blockers and their approved resolution are recorded in `inputs.md`, not misreported as execution findings. Scenarios A and C–J were not executed. Semantic verdict remains reserved for the Independent Reviewer.
