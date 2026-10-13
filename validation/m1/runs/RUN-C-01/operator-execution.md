# RUN-C-01 — Operator Execution Record

> RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity

- **Run ID:** `RUN-C-01`
- **Role:** M1 Data Operator — Codex
- **Targets:** P04, P14, P16 only
- **Input freeze:** `32b0708460ede4de3e0601f8570e29bbae5ddd2f`
- **Scenario B acceptance baseline:** `e26be48851892a37f222d37569acfe1f3ddc68d2`
- **Fixture handles:** `FIX-ID-P04`, `FIX-ID-P14`, `FIX-ID-P16` — local validation stand-ins, not GeoIDs.

## Actions performed

1. Materialized only P04/P14/P16 Place context, OLD Source Assertions and controlled initial OLD Current DAEN Representation selections.
2. Preserved the pre-run rows unchanged.
3. Appended each REVISED synthetic name assertion.
4. Appended one REVISED Current DAEN Representation selection per target, with the same Place, `fact=name`, `purpose=display-name`, `language=en` scope as its OLD selection.
5. Set each REVISED selection's `supersedes_reference` to the prior selection row, never to a Source Assertion or Place.
6. Recorded selector attribution as Codex / `RUN-C-01` / exact step label. Assertion provenance remains the approved mock-source label.
7. Did not alter Place identity, locus, coordinates, field evidence or corpus classification. P16 was not merged with or materialized as P15.

## Effective-selection interpretation

| Place | Scope | Initial assertion / selection | Revised assertion / selection | Supersedes | Retained history | Effective value after run |
|---|---|---|---|---|---|---|
| `FIX-ID-P04` | name / display-name / en | `FIX-ID-P04-SA-OLD` / `FIX-ID-P04-SEL-OLD` | `FIX-ID-P04-SA-REVISED` / `FIX-ID-P04-SEL-REVISED` | `RUN-C-01:PRE-P04-SEL-OLD` | OLD assertion and OLD selection retained | `AEON Mall Phnom Penh` |
| `FIX-ID-P14` | name / display-name / en | `FIX-ID-P14-SA-OLD` / `FIX-ID-P14-SEL-OLD` | `FIX-ID-P14-SA-REVISED` / `FIX-ID-P14-SEL-REVISED` | `RUN-C-01:PRE-P14-SEL-OLD` | OLD assertion and OLD selection retained | `AEON Mall Cambodia Parking Tower building` |
| `FIX-ID-P16` | name / display-name / en | `FIX-ID-P16-SA-OLD` / `FIX-ID-P16-SEL-OLD` | `FIX-ID-P16-SA-REVISED` / `FIX-ID-P16-SEL-REVISED` | `RUN-C-01:PRE-P16-SEL-OLD` | OLD assertion and OLD selection retained | `SYNTHETIC P15/P16 Test Premises` |

This table is an interpretation of this controlled run under H20, not a production algorithm. No cross-language or general cross-scope migration was tested.

## Correction rationale

For each target, the OLD display-name spelling is a deliberately introduced transcription error for this fixture. The REVISED spelling is supplied as its correction. Both statements concern the same unchanged premises and the same English display-name purpose. No physical relocation, ownership change, source-trust comparison or scope change occurs.

## Checker and snapshot evidence

- **Runtime:** Python 3.15.0a2
- **Invocation:** `python validation/m1/checker/check_m1.py --fixture validation/m1/runs/RUN-C-01/checker-fixture`
- **Exit code:** `0`
- **Raw output:** `raw-checker-output.txt`, unedited.
- `pre-run-state.csv` equals `checker-fixture/state-ledger-previous.csv` byte-for-byte.
- `post-run-state.csv` equals `checker-fixture/state-ledger.csv` byte-for-byte.
- Frozen `validation/m1/scenario-sheet.md` equals `checker-fixture/scenario-sheet.md` byte-for-byte.
- All PRE rows are retained unchanged; row keys are unique; the accepted Place identity set is unchanged.

The checker confirms structural evidence only. It does not establish concept-typed reference correctness, scope equivalence, real-world factual truth or effective-selection semantics.

## Friction and limits

No new execution friction was observed. This run is limited to controlled synthetic name-correction inputs. It does not test new source verification, coordinate-role substitution, cross-language supersession, source ranking, the full Correction workflow, P16 merge or overall M1.

Scenarios A, B and D–J were not executed. The semantic verdict remains undecided.
