# RUN-F-01 — Operator Execution Record

RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity

- Run ID: RUN-F-01
- Role: M1 Data Operator — Codex
- Targets: P04, P14, P15 only
- Input freeze: 8d7ab92a515ad3bed899af35c15cb94227535f5e
- Scenario E acceptance baseline: 193a2f5614b48007eb4a832acbaf560ec12081c5
- Fixture handles: FIX-ID-P04, FIX-ID-P14, FIX-ID-P15 — local validation stand-ins, not GeoIDs.

## Scope and actions

1. Materialized only the frozen Place context and Source Assertion inputs.
2. Did not create or select any Current DAEN Representation.
3. Appended one revised Source Assertion for each target.
4. Set each revised assertion supersedes_reference to the exact earlier OLD Source Assertion row.
5. Appended one Correction row for each target using existing ledger fields.
6. Used no separate Succession row.
7. Recorded operator attribution here as Codex / RUN-F-01; no undefined STEP aliases were introduced.
8. Did not alter P04 real coordinate or entrance evidence.

## Manual correction table

| Place | Fact | OLD assertion | REVISED assertion | Revised supersedes | Correction object | Identity unchanged |
|---|---|---|---|---|---|---|
| FIX-ID-P04 | address | FIX-ID-P04-SA-ADDR-OLD | FIX-ID-P04-SA-ADDR-REVISED | RUN-F-01:PRE-P04-SA-ADDR-OLD | FIX-CORR-F-P04 | yes |
| FIX-ID-P14 | provider-reference | FIX-ID-P14-SA-PROVIDER-OLD | FIX-ID-P14-SA-PROVIDER-REVISED | RUN-F-01:PRE-P14-SA-PROVIDER-OLD | FIX-CORR-F-P14 | yes |
| FIX-ID-P15 | coordinate | FIX-ID-P15-SA-COORD-OLD | FIX-ID-P15-SA-COORD-REVISED | RUN-F-01:PRE-P15-SA-COORD-OLD | FIX-CORR-F-P15 | yes |

## State preservation

- OLD values remain retained.
- Revised values are appended.
- Correction records are appended.
- Place identity set before and after is {FIX-ID-P04, FIX-ID-P14, FIX-ID-P15}.
- No Current DAEN Representation row exists.
- No GeoID, Place, merge, split, lifecycle or containment change occurred.
- P04 general Place-reference coordinate and observed entrance coordinate were not treated as a correction pair.

## Provenance and classification

Source Assertion provenance is separate from Correction-action provenance. Source Assertions use the SYN-F labels in source-map.md; correction actions use SYN-F-CORR-P04, SYN-F-CORR-P14 and SYN-F-CORR-P15. P04 and P14 Place context is REAL; P15 Place context and all new fixture assertions/actions are SYNTHETIC; every Quality value is unknown.

## Snapshot and checker evidence

- pre-run-state.csv equals checker-fixture/state-ledger-previous.csv byte-for-byte.
- post-run-state.csv equals checker-fixture/state-ledger.csv byte-for-byte.
- checker-fixture/scenario-sheet.md equals the frozen scenario sheet byte-for-byte.
- PRE contains 8 data rows and POST contains 14 data rows.
- Row keys are unique; there are exactly 3 Correction rows and exactly 3 revised Source Assertion supersession references.
- Every revised supersedes_reference targets its intended OLD Source Assertion row.
- Every Correction ref points to the corresponding revised Source Assertion and every corrects value identifies the intended OLD Source Assertion.

## Checker command

The frozen checker self-test was run before this execution. The scenario checker command and unedited output are recorded in raw-checker-output.txt.

The checker provides structural evidence only. It does not decide Correction semantic correctness, reference target types, OLD versus REVISED roles, identity preservation, factual truth of synthetic values or Scenario F semantic PASS.

## Friction and limits

No new runtime friction was observed. This run tests only controlled synthetic Source Assertion corrections. It does not test Current DAEN Representation behavior, general Succession taxonomy, production correction authority, P04 real address/coordinate truth, P04 entrance resolution, P14 name correction or overall M1.
