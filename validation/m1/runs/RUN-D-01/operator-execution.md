# RUN-D-01 — Operator Execution Record

> RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity

- **Run ID:** `RUN-D-01`
- **Role:** M1 Data Operator — Codex
- **Targets:** P05, P06, P07 only
- **Scenario D input-freeze commit:** `a62bd735df7c1b6b1297ed046a382ce9bdade788`
- **Starting baseline:** `df9fb2f6e3bfdfb9cccb66ad6f4d44b5afc2cf28`
- **Fixture handles:** `FIX-ID-P05`, `FIX-ID-P06`, `FIX-ID-P07`, `FIX-AP-D-SHARED`, `FIX-AP-D-P07` — local validation labels, not GeoIDs.

## Actions performed

1. Materialized separate Place, Place-reference Source Assertion and controlled initial coordinate selection rows for P05, P06 and P07.
2. Materialized the two independent access Source Assertions without creating Access Point objects in PRE.
3. Preserved every PRE row unchanged.
4. Appended exactly two separate Access Point objects: `FIX-AP-D-SHARED` and `FIX-AP-D-P07`.
5. Kept `FIX-AP-D-SHARED` shared by P05 and P06; kept `FIX-AP-D-P07` serving P07.
6. Performed no selection supersession, correction, merge, split, lifecycle, containment, routing or pickup/drop-off operation.

## Per-target comparison

| Place | Selected coordinate | Independent access assertion | Access Point object | Access coordinate | Served Place relationship |
|---|---|---|---|---|---|
| `FIX-ID-P05` | `0.010000, 0.010000` | `SYN-D-ACCESS-SHARED` | `FIX-AP-D-SHARED` | `0.009000, 0.011000` | Shared with `FIX-ID-P06` |
| `FIX-ID-P06` | `0.010000, 0.012000` | `SYN-D-ACCESS-SHARED` | `FIX-AP-D-SHARED` | `0.009000, 0.011000` | Shared with `FIX-ID-P05` |
| `FIX-ID-P07` | `0.020000, 0.020000` | `SYN-D-ACCESS-P07` | `FIX-AP-D-P07` | `0.019000, 0.020500` | Serves `FIX-ID-P07` |

The access meaning comes from the separately specified mock access statements. It was not inferred from numeric difference between coordinates. P07's augmentation is synthetic and makes no claim about an actual RUPP gate.

## Attribution and classification

- Place context: `D-PLACE-P05`, `D-PLACE-P06`, `D-PLACE-P07` as mapped in `source-map.md`.
- Coordinate assertions and initial selections: `SYN-D-REF-P05`, `SYN-D-REF-P06`, `SYN-D-REF-P07`; all synthetic, Quality `unknown`.
- Access assertions and AP objects: `SYN-D-ACCESS-SHARED`, `SYN-D-ACCESS-P07`; all synthetic, Quality `unknown`.
- P05/P06 Place contexts are SYNTHETIC. P07 physical Place context is REAL; its coordinate augmentation, selection and AP are SYNTHETIC.
- Selection/AP attribution: Codex, `RUN-D-01`, and ledger action rows `PRE-P05-SEL`, `PRE-P06-SEL`, `PRE-P07-SEL`, `POST-AP-SHARED`, `POST-AP-P07`.

## Counts and integrity checks

- PRE data records: 11 (header excluded).
- POST data records: 13 (header excluded).
- PRE rows retained unchanged in POST: YES.
- Row keys unique: YES.
- Accepted Place identities before/after: `FIX-ID-P05`, `FIX-ID-P06`, `FIX-ID-P07` / unchanged.
- Initial selections before/after: `FIX-ID-P05-SEL`, `FIX-ID-P06-SEL`, `FIX-ID-P07-SEL` / unchanged.
- Distinct AP objects after run: 2.
- P05/P06 shared-object check: YES, one `FIX-AP-D-SHARED` row serves both.

## Checker evidence

- **Runtime:** Python 3.15.0a2
- **Invocation:** `python validation/m1/checker/check_m1.py --fixture validation/m1/runs/RUN-D-01/checker-fixture`
- **Exit code:** `0`
- **Raw output:** `raw-checker-output.txt`, unedited.
- Checker ledger equals POST snapshot byte-for-byte.
- Checker previous snapshot equals PRE snapshot byte-for-byte.
- Checker scenario sheet equals frozen scenario sheet byte-for-byte.

The checker does not prove physical accessibility, real-world evidence independence, AP correctness, concept-typed reference correctness, synthetic marking correctness or semantic Scenario D success. Those remain manual-review questions.

## Friction and limits

No new execution friction was observed. This run uses only approved synthetic coordinate/access fixtures. It does not establish a real RUPP gate, new field evidence, Scenario E acceptance, production geometry, coordinate reference system, precision standard or distance threshold.

Scenarios A–C and E–J were not executed. Semantic verdict remains undecided.
