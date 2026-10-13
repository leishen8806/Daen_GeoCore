# RUN-A-02 — Operator Execution Record

> RAW OPERATOR EVIDENCE — NOT A SPECIFICATION.

## Run identity

- **Run ID:** `RUN-A-02`
- **Role:** M1 Data Operator — Codex
- **Targets:** P01, P02 only
- **Original run:** RUN-A-01; review disposition for `b90a498c819b1f1c00e820b8031edc58223d739d`
- **Fixture handles:** `FIX-ID-P01`, `FIX-ID-P02` — local validation stand-ins, not GeoIDs.

## Scope

This is a scenario-local run. Only the minimum state for P01/P02 was materialized. The frozen corpus still contains P01–P20; the other 18 slots were not initialized or executed here. This follows the earlier minimum-state execution instruction while the broader initial-state plan describes full M1 setup. This is a procedure clarification, not a model defect.

## Frozen Scenario A

The unchanged frozen scenario is Stable Identity for P01/P02. Its expected outcome is not copied into or modified in the frozen scenario sheet.

## Corrected encoding actions

1. Created separate Place rows for P01 and P02 with stable local fixture identity and locus statements.
2. Created separate REAL Source Assertion rows for each frozen public name representation.
3. Created separate Current DAEN Representation rows with explicit scope and assertion references.
4. P01 retained both English name assertions; the controlled selection test points to the second assertion without claiming a historical rename.
5. P02 retained English and Khmer assertions as coexisting language scopes; the Khmer assertion does not supersede English.
6. Controlled selection changes are marked `SYNTHETIC`; public source assertions remain `REAL`.
7. All pre-run rows remain unchanged in the post-run ledger.

## Friction

No new RUN-A-02 friction entry was observed. Existing checker limitations are recorded in the reviewer packet; they are not semantic results.

## Checker and snapshot evidence

- **Runtime:** Python 3.15.0a2
- **Invocation:** `python validation/m1/checker/check_m1.py --fixture validation/m1/runs/RUN-A-02/checker-fixture`
- **Exit code:** `0`
- **Raw output:** `raw-checker-output.txt` containing `PASS: no supported mechanical failure found`
- **Pre-run snapshot SHA-256:** `D328B5DB03296EC2330D915C8F536AD765F89159EAD4726C35BF4412909155B2`
- **Checker previous snapshot SHA-256:** `D328B5DB03296EC2330D915C8F536AD765F89159EAD4726C35BF4412909155B2`
- **Post-run snapshot SHA-256:** `23D2085F8BC0E6EA98B8C0BA91E80C11E7FE26FE7DC67B0BEFEDDEC4851F7E13`
- **Checker state-ledger SHA-256:** `23D2085F8BC0E6EA98B8C0BA91E80C11E7FE26FE7DC67B0BEFEDDEC4851F7E13`
- **Checker scenario-sheet SHA-256:** `888226663678F662DFB07846DAC49D9C56699E4EF78ABB3521B1995C3EAD5B13`
- **Frozen scenario-sheet SHA-256:** `888226663678F662DFB07846DAC49D9C56699E4EF78ABB3521B1995C3EAD5B13`

The two snapshot pairs and the scenario-sheet pair are byte-identical. The checker input was the run-local `checker-fixture/` directory, not the central M1 ledger.

## Boundary

- Scenario A only.
- Scenarios B–J: NOT EXECUTED.
- Semantic verdict: reserved for Independent Reviewer.
