# RUN-E-01 — Approved Shared-Access Fixture

> PRE-EXECUTION INPUT RECORD — VALIDATION EVIDENCE ONLY. NOT A SPECIFICATION.

## Baseline and frozen scope

- **Baseline:** `45712b61f2811fe7cf71f086d5a7f38e79a2a287` (Scenario D acceptance)
- **Branch:** `phase/04-m1-execution`
- **Run:** `RUN-E-01`
- **Role:** M1 Data Operator — Codex
- **Scenario:** E — Shared Access Point
- **Frozen target slot:** P07
- **Action:** Represent one Access Point serving multiple Places.
- **Expected outcome:** One shared Access Point is represented once and linked to multiple Places without business pickup/drop-off semantics.

P08 is an approved supporting served Place required to exercise the multi-Place relationship. It is not a new E target, corpus slot or scenario substitution.

## Place handles and boundary

- `FIX-ID-P07` → P07, Royal University of Phnom Penh Main Campus, REAL.
- `FIX-ID-P08` → P08, Hun Sen Library, RUPP, REAL.
- `FIX-AP-E-SHARED` → one E-local Access Point object, SYNTHETIC.
- Do not reuse, mutate or extend `FIX-AP-D-P07` or `FIX-AP-D-SHARED`.
- Do not materialize containment, infer access from proximity, or create a second AP object.

P07 and P08 correspond to existing REAL corpus Places. The shared-access relationship is explicitly SYNTHETIC and does not claim that the real places share an entrance.

## Exact approved shared-access statement

### SYN-E-ACCESS-SHARED

“Within the RUN-E-01 controlled fixture, one shared pedestrian access threshold serves both P07 (RUPP Main Campus) and P08 (Hun Sen Library premises). The shared-service relationship is supplied explicitly by this synthetic fixture statement. It is not inferred from containment, proximity, coordinates, public maps, or Scenario D evidence.”

- **Classification:** `SYNTHETIC`
- **Quality:** `unknown`
- **Coordinate:** none; Scenario E does not test coordinate semantics.

## Historical traceability note

TRACEABILITY NOTE — The historical `synthetic-case-plan.md` mentions P05/P06 for Scenario E, but the authoritative frozen scenario sheet targets P07. RUN-E-01 therefore uses P07 as the target and P08 only as the approved supporting served Place.

The historical plan is not edited. This is a pre-execution traceability discrepancy, not a runtime model finding.

## PRE / POST plan

### PRE

Materialize exactly:

1. P07 Place context;
2. P08 Place context;
3. the `SYN-E-ACCESS-SHARED` Source Assertion.

No E Access Point object exists in PRE. No Current DAEN Representation, Selected Coordinate, Correction, Succession, Merge, Split, Containment, lifecycle, route or pickup/drop-off operation is created.

### POST

Retain every PRE row unchanged and append exactly one Access Point object row, `FIX-AP-E-SHARED`, referencing `SYN-E-ACCESS-SHARED` and visibly associating both `FIX-ID-P07` and `FIX-ID-P08`.

## Attribution and review boundaries

- Source Assertion provenance: `SYN-E-ACCESS-SHARED`.
- Place-context provenance: `E-PLACE-P07` and `E-PLACE-P08`.
- AP materialization attribution: Codex, run `RUN-E-01`, exact ledger row key recorded in `operator-execution.md`.
- Provenance and operator/materialization attribution remain separate.
- The review table is evidence only, not a schema proposal.

Manual review must confirm one AP object serves two Places, the relationship is supplied by the synthetic assertion, no duplicate AP exists, no business semantics appear, and D evidence remains unchanged.

Acceptance limits: no real RUPP/Hun Sen Library shared gate, no containment-implies-access claim, no production AP namespace or deduplication rule, no D/E AP identity continuity, no AP correction/lifecycle, no pickup/drop-off semantics and no overall M1 result.
