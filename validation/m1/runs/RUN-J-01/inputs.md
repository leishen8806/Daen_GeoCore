# RUN-J-01 — Frozen Containment Inputs

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Authority and effective fixtures

- Historical frozen J targets: P18, P19.
- Historical roles: P18 parent/child containment; P19 second containment example.
- Effective J positive fixtures under approved erratum: R1 P07→P08 and R2 P19→`FIX-ID-J-P19-CHILD`.
- P18 is not used by RUN-J-01.
- J target/fixture erratum commit: `532332d00df38b237d214a39e5ee35f32038735f`.
- I acceptance baseline: `4a88bfb035a950835cb7ea6b0fb18c0326e361d9`.

## Frozen containment rule

Use only generic `relationship=contains` with explicit `parent` and `child`. The direction `parent contains child` does not imply the reciprocal. No Area, administrative hierarchy, business hierarchy, commercial hierarchy, containment subtype taxonomy, multi-parent or recursive semantics are introduced.

## R1 — REAL P07 contains P08

PRE exactly 2 REAL Place rows:

- `FIX-ID-P07` / `J-PLACE-P07` / `locus=Royal University of Phnom Penh Main Campus; identity=FIX-ID-P07` / Quality `unknown`.
- `FIX-ID-P08` / `J-PLACE-P08` / `locus=Hun Sen Library RUPP; identity=FIX-ID-P08` / Quality `unknown`.

POST retains PRE and appends exactly one REAL Containment row:

- `FIX-CONT-J-P07-P08` / `PUB-J-P07-CONTAINS-P08` / `ref=FIX-ID-P07; relationship=contains; parent=FIX-ID-P07; child=FIX-ID-P08` / Quality `unknown`.

## R2 — SYNTHETIC P19 contains synthetic child

PRE exactly 2 SYNTHETIC Place rows:

- `FIX-ID-P19` / `J-PLACE-P19` / `locus=SYNTHETIC P19 Building; identity=FIX-ID-P19` / Quality `unknown`.
- `FIX-ID-J-P19-CHILD` / `SYN-J-P19-CHILD-PLACE` / `locus=SYNTHETIC P19 Child Premises; identity=FIX-ID-J-P19-CHILD` / Quality `unknown`.

POST retains PRE and appends exactly one SYNTHETIC Containment row:

- `FIX-CONT-J-P19-CHILD` / `SYN-J-P19-CONTAINS-CHILD` / `ref=FIX-ID-P19; relationship=contains; parent=FIX-ID-P19; child=FIX-ID-J-P19-CHILD` / Quality `unknown`.

The child is a J-local validation identity, not a corpus slot or production GeoID.

## P19 negative business-boundary control

`SYN-J-P19-OCCUPANT-PROPOSAL`: a synthetic occupant/business associated with `FIX-ID-P19` is proposed as another Place for boundary testing. The proposal is rejected: it receives no Place identity, no Containment row and no business-hierarchy representation in Geo Core.

This is input-level negative-control evidence only and does not count as a positive relationship.

## Acceptance limits and isolation

R1 is REAL based on frozen public corpus evidence. R2 and the negative control are SYNTHETIC. Do not import P07/P08 prior D/E/G state, P19 prior state or H P18 ledgers. No production schema/API, recursive semantics, taxonomy, Area, business hierarchy or overall M1 result is created.
