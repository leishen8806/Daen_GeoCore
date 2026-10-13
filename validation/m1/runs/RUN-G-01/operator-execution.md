# RUN-G-01 — Operator Execution Record

RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity

- Run ID: RUN-G-01
- Role: M1 Data Operator — Codex
- Original registered targets: P08, P09
- Effective targets under approved erratum: P15, P16
- Target erratum commit: eac2d7561a1b46096e2106e2201da3b7c6dd0788
- Input freeze: 626556e86441836b00d356ee9cf7f9471b360541
- Fixture handles are local validation stand-ins, not production GeoID formats.

## Execution method

The same four-row common PRE was copied byte-for-byte into two isolated subcases. The subcases are alternative hypothetical worlds, not sequential events.

| Subcase | Survivor | Retired | Resolution Link | Succession | Retired resolves to | PRE identical |
|---|---|---|---|---|---|---|
| A | FIX-ID-P15 | FIX-ID-P16 | FIX-RES-G-A-P16-TO-P15 | FIX-SUCC-G-A-P16-TO-P15 | FIX-ID-P15 | yes |
| B | FIX-ID-P16 | FIX-ID-P15 | FIX-RES-G-B-P15-TO-P16 | FIX-SUCC-G-B-P15-TO-P16 | FIX-ID-P16 | yes |

## Actions

1. Materialized the controlled synthetic same-locus premise and two source-record assertions.
2. Subcase A appended one Resolution Link and one Succession for P16-to-P15.
3. Subcase B independently appended one Resolution Link and one Succession for P15-to-P16.
4. No subcase changed the four PRE rows, source assertions, or introduced Current DAEN Representation.
5. Both directions use survivor_basis=test-direction-only and survivor_policy=not-defined.

## Manual reference checks

- Each retired and survivor handle exists as a Place identity row.
- Retired and survivor handles differ.
- Resolution direction matches the subcase.
- retired_resolvable=true in both Resolution Link rows.
- Succession predecessor is retired and successor is survivor.
- Each Succession ref resolves to its corresponding Resolution Link.
- No identity is reassigned to a third Place.
- Historical Place and Source Assertion rows remain retained.

## Boundaries

The same-Place premise came from the controlled synthetic fixture and is not a general equivalence algorithm. No survivor policy was selected. E's P08 supporting use has no bearing on G; C's P16 and F's P15 ledgers are run-local and were not mutated; no previous representation, correction or Access Point state was imported.

## Checker and limits

Both checker fixtures use the unchanged original scenario sheet, which still records historical P08/P09 targets. The approved erratum is the effective target authority for RUN-G-01. Checker output is structural evidence only and does not establish same-Place correctness, merge direction, survivor semantics, historical resolvability, Resolution Link meaning, Succession meaning, absence of survivor policy or semantic PASS.

No new runtime friction was observed. No H–J scenario was executed.
