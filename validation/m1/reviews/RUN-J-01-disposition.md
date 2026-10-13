# RUN-J-01 — Scenario J Disposition

## Acceptance

- **Project acceptance:** `PASS` for the controlled minimal Containment outcome only.
- **Evidence:** `d1db291e11afd2082ce86bb97e6caedb467ad61c`.
- **Input freeze:** `0e47bdc6b9f7ee8ad447c0bc0c2da91ebca795f0`.
- **Target/fixture erratum:** `532332d00df38b237d214a39e5ee35f32038735f`.
- **I acceptance baseline:** `4a88bfb035a950835cb7ea6b0fb18c0326e361d9`.
- No J rerun is authorized.
- Overall M1 remains `NOT MADE`.

## Supported relationships

### R1 — REAL

`FIX-ID-P07 contains FIX-ID-P08`.

Both endpoints are Places, the relationship is directional, P07 and P08 differ, and the relation is supported at frozen REAL corpus-memo level. No Access Point, business hierarchy or Area is imported.

### R2 — SYNTHETIC

`FIX-ID-P19 contains FIX-ID-J-P19-CHILD`.

Both endpoints are SYNTHETIC Places, the child is run-local, the relationship is directional and no containment subtype is created.

### Supplemental negative control

The P19 occupant/business proposal receives no Place identity, no Containment relation and no business hierarchy. It does not count as a positive relationship.

## Finding dispositions

### RUN-J-01:F1

Evidence limitation only. Do not upgrade P07→P08 to exact claim-to-source attribution.

### RUN-J-01:F2

Validation-medium limitation only. Parent/child/direction/relationship remain free-text manual checks; no production Containment schema.

### RUN-J-01:F3

Evidence limitation only. The negative control is verified by absence; no rejected-business entity is added.

### RUN-J-01:F4

Evidence limitation only. Controlled synthetic locus text is retained without invented address or coordinate.

### RUN-J-01:F5

Traceability limitation only. Historical role and invariant shorthand discrepancies remain preserved.

## Acceptance limits

No multi-parent, recursive, transitive or inheritance semantics; no containment taxonomy; no Area model; no production schema/API; no interaction with Access Point, lifecycle, merge or split; no overall M1 result.
