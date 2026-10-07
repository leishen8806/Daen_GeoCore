# RUN-J-01 — Source and Provenance Map

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Commit anchors

- I acceptance baseline: `4a88bfb035a950835cb7ea6b0fb18c0326e361d9`
- J target/fixture erratum: `532332d00df38b237d214a39e5ee35f32038735f`
- J input-freeze commit: this controlled commit adding `inputs.md` and `source-map.md`; exact SHA is recorded in the operator evidence and reviewer packet.

## REAL R1

| Label | Meaning | Frozen source | Quality / class |
|---|---|---|---|
| `J-PLACE-P07` | RUPP Main Campus Place | corpus-register P07 + corpus-evidence P07 | unknown / REAL |
| `J-PLACE-P08` | Hun Sen Library Place | corpus-register P08 + corpus-evidence P08 | unknown / REAL |
| `PUB-J-P07-CONTAINS-P08` | P07 contains P08 | Frozen P08 evidence stating it is a distinct building within P07 | unknown / REAL |

## SYNTHETIC R2

| Label | Meaning | Frozen source | Quality / class |
|---|---|---|---|
| `J-PLACE-P19` | Synthetic P19 building Place | corpus-register P19 + synthetic-case-plan P19 | unknown / SYNTHETIC |
| `SYN-J-P19-CHILD-PLACE` | Synthetic child Place input | RUN-J-01 controlled input | unknown / SYNTHETIC |
| `SYN-J-P19-CONTAINS-CHILD` | Synthetic containment relation | RUN-J-01 controlled input | unknown / SYNTHETIC |

## Negative control

| Label | Meaning | Frozen source | Quality / class |
|---|---|---|---|
| `SYN-J-P19-OCCUPANT-PROPOSAL` | Occupant/business incorrectly proposed as Place and rejected | synthetic-case-plan P19 + RUN-J-01 controlled boundary proposition | unknown / SYNTHETIC input only |

R1 uses only generic `relationship=contains` and explicit parent/child direction. No Area, business hierarchy or containment subtype is asserted.
