# RUN-E-01 — Operator Execution Record

> RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity

- **Run ID:** `RUN-E-01`
- **Role:** M1 Data Operator — Codex
- **Frozen target:** P07
- **Supporting served Place:** P08
- **Input-freeze commit:** `a966670b5026331c6399c2bed4c67660071223e3`
- **Starting baseline:** `45712b61f2811fe7cf71f086d5a7f38e79a2a287`
- **E-local AP handle:** `FIX-AP-E-SHARED` — local validation label, not a GeoID.

## Actions performed

1. Materialized P07 and P08 Place context rows.
2. Materialized the `SYN-E-ACCESS-SHARED` Source Assertion.
3. Saved the PRE state with no Access Point object.
4. Appended exactly one Access Point object, `FIX-AP-E-SHARED`, referencing the shared assertion and both Place handles.
5. Did not reuse or mutate `FIX-AP-D-P07` or `FIX-AP-D-SHARED`.
6. Performed no coordinate, selection, containment, correction, merge, split, lifecycle, route or pickup/drop-off operation.

## One-AP / Two-Place relationship

| Access Point | Served Place 1 | Served Place 2 | AP object count |
|---|---|---|---:|
| `FIX-AP-E-SHARED` | `FIX-ID-P07` | `FIX-ID-P08` | 1 |

- Target Place count involved in this relationship: `2`.
- Access Point object count: `1`.
- No duplicate AP row represents the same threshold.
- Shared-service meaning comes from `SYN-E-ACCESS-SHARED`, not containment, proximity, coordinates, public maps or Scenario D evidence.

## Attribution and classification

- `E-PLACE-P07` → REAL P07 context.
- `E-PLACE-P08` → REAL P08 context.
- `SYN-E-ACCESS-SHARED` → SYNTHETIC shared-access assertion and AP object.
- Quality is `unknown` for every evaluated row.
- AP materialization attribution: Codex / `RUN-E-01` / ledger row `RUN-E-01:POST-AP-SHARED`.
- Source Assertion provenance and operator/materialization attribution remain separate.

## Counts and integrity checks

- PRE data records: `3` (header excluded).
- POST data records: `4` (header excluded).
- PRE rows retained unchanged: YES.
- Row keys unique: YES.
- Place identity set unchanged: `FIX-ID-P07`, `FIX-ID-P08`.
- POST Access Point concept rows: exactly `1`.
- Served-place associations: both P07 and P08 retained in the AP row.
- Business pickup/drop-off semantics: absent.

## Checker evidence

- **Runtime:** Python 3.15.0a2
- **Invocation:** `python validation/m1/checker/check_m1.py --fixture validation/m1/runs/RUN-E-01/checker-fixture`
- **Exit code:** `0`
- **Raw output:** `raw-checker-output.txt`, unedited.
- PRE equals checker previous snapshot byte-for-byte.
- POST equals checker ledger byte-for-byte.
- Frozen scenario sheet equals checker scenario copy byte-for-byte.

Checker PASS does not mechanically establish shared served-Place semantics, correct relationship target types, absence of semantically duplicate AP objects, actual physical access or Scenario E semantic PASS. These remain manual-review responsibilities.

## Historical traceability discrepancy

The historical synthetic plan mentions P05/P06 for Scenario E. The frozen scenario sheet authoritatively targets P07. This run therefore uses P07 as target and P08 only as the approved supporting served Place. The historical plan was not edited.

## Friction and limits

No new execution friction was observed. This run does not establish a real RUPP/Hun Sen Library shared gate, containment implying access, a production AP namespace or deduplication rule, D/E AP identity continuity, AP correction/lifecycle, business pickup/drop-off semantics or an overall M1 result. B:F4 / D:F5 regarding P04 remains open and was not tested.

Scenarios A–D and F–J were not executed. Semantic verdict remains undecided.
