# RUN-A-01 — Operator Execution Record

> RAW OPERATOR EVIDENCE — NOT A SPECIFICATION.

## Run identity

- **Run ID:** `RUN-A-01`
- **Role:** M1 Data Operator — Codex
- **Target Places:** P01, P02
- **Fixture handles:** `FIX-ID-P01`, `FIX-ID-P02`
- **Handle disclaimer:** local validation stand-ins only; not actual or proposed GeoID format and not production identifiers.

## Frozen authority

Scenario A is taken unchanged from `validation/m1/scenario-sheet.md`: Stable Identity; targets P01 and P02; expected outcome is that one Place and one fixture identity remain stable while representations and Source Assertions may vary.

## Initial state

Minimum initial state was materialized in `pre-run-state.csv` with one real/public Place fixture row for P01 and P02, explicit provenance, quality and stable local fixture identity handles.

## Operator actions

1. Preserved P01 fixture identity `FIX-ID-P01` while changing the public name representation from `Central Post Office` to `Cambodia Post Central Post Office`.
2. Preserved P02 fixture identity `FIX-ID-P02` while adding the Khmer name representation `ព្រះបរមរាជវាំង` to the English representation.
3. Preserved prior rows and linked each changed row to its predecessor through `supersedes_reference`.
4. Did not perform correction, merge, split, closure, withdrawal or Access Point actions.

## Friction

Zero friction entries recorded during this operator run. No unresolved judgment was silently converted into a rule.

## Boundary

- Scenario executed: A only.
- Scenarios B–J: NOT EXECUTED.
- Semantic verdict: intentionally blank pending Independent Reviewer.
