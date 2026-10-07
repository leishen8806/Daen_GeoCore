# RUN-J-01 — Operator Execution Record

RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Authority and scope

- Run ID: `RUN-J-01`
- Role: M1 Data Operator — Codex
- Historical targets: P18, P19
- Effective fixtures: R1 P07→P08 and R2 P19→`FIX-ID-J-P19-CHILD`
- J target/fixture erratum: `532332d00df38b237d214a39e5ee35f32038735f`
- J input-freeze: `0e47bdc6b9f7ee8ad447c0bc0c2da91ebca795f0`
- I acceptance baseline: `4a88bfb035a950835cb7ea6b0fb18c0326e361d9`

## Containment boundary

Both subcases use only generic `relationship=contains` with explicit `parent` and `child`. No reciprocal row was created. No Area, business hierarchy, commercial hierarchy, containment subtype or multi-parent semantics were introduced.

## R1 — REAL P07 contains P08

| State | Rows | Content |
|---|---:|---|
| PRE | 2 | REAL P07 Place + REAL P08 Place |
| POST | 3 | PRE + REAL `FIX-CONT-J-P07-P08` Containment |

The relation states `parent=FIX-ID-P07; child=FIX-ID-P08`. P07 and P08 are distinct Place identities. No Access Point or organization relation was imported.

## R2 — SYNTHETIC P19 contains synthetic child

| State | Rows | Content |
|---|---:|---|
| PRE | 2 | SYNTHETIC P19 Place + SYNTHETIC J-local child Place |
| POST | 3 | PRE + SYNTHETIC `FIX-CONT-J-P19-CHILD` Containment |

The relation states `parent=FIX-ID-P19; child=FIX-ID-J-P19-CHILD`. The child is not a corpus slot or production GeoID.

## P19 negative business-boundary control

`SYN-J-P19-OCCUPANT-PROPOSAL` exists only in frozen input evidence. No occupant Place row, Containment row or business-hierarchy representation was created.

## Checker evidence

- `real-campus/raw-checker-output.txt`: exit code 0, `PASS: no supported mechanical failure found`.
- `synthetic-building/raw-checker-output.txt`: exit code 0, `PASS: no supported mechanical failure found`.
- Both checker fixtures contain byte-identical copies of the original scenario sheet, which still shows P18/P19.

## Operator boundaries

No P18 H state was imported. No prior P07/P08 D/E/G state or P19 ledger state was imported. No J semantic verdict, overall M1 decision, production schema/API, Area, business hierarchy or containment taxonomy was created.
