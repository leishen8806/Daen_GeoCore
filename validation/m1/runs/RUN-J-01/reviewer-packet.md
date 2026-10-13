# RUN-J-01 — Reviewer Packet

REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Authority and effective fixtures

- J target/fixture erratum: `validation/m1/errata/SCENARIO-J-TARGET-ERRATUM.md`
- Erratum commit: `532332d00df38b237d214a39e5ee35f32038735f`
- Input-freeze commit: `0e47bdc6b9f7ee8ad447c0bc0c2da91ebca795f0`
- Historical targets: P18/P19
- Effective fixtures: R1 P07→P08 and R2 P19→synthetic child
- P19 occupant proposal is supplemental negative control only.

## Relationship evidence

| Fixture | Parent | Child | Class | PRE | POST |
|---|---|---|---|---:|---:|
| R1 real-campus | `FIX-ID-P07` | `FIX-ID-P08` | REAL | 2 | 3 |
| R2 synthetic-building | `FIX-ID-P19` | `FIX-ID-J-P19-CHILD` | SYNTHETIC | 2 | 3 |

## Manual review questions

- Are both endpoints Places?
- Is each relation explicitly directed parent→child?
- Are parent and child distinct?
- Is generic `relationship=contains` used without subtype taxonomy?
- Is P07→P08 geographic containment rather than Access Point, ownership or organization hierarchy?
- Is the P19 occupant proposal rejected by absence of Place and Containment rows?
- Is Area absent?
- Are P18 H ledgers, P07/P08 D/E/G state and P19 prior state isolated?
- Are REAL/SYNTHETIC and provenance boundaries preserved?

## Checker results

Both checker outputs are structural PASS. The checker does not understand parent/child direction, Area avoidance, business-boundary rejection or containment subtype absence.

## Acceptance limits

- Only two minimal Place-to-Place relationships are represented.
- No general containment taxonomy, recursive semantics or multi-parent behavior is tested.
- No business hierarchy or ownership relation is created.
- R1 relies on frozen public corpus evidence; R2 is synthetic.
- P19 negative control is supplemental and does not count as a positive relationship.
- No production schema/API or overall M1 result is created.

## Decision state

Reviewer verdict: ____________________

PASS / FAIL / INEXPRESSIBLE: ____________________

The operator records evidence only. No GO, ITERATE or RETURN decision is made here.
