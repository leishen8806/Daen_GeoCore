# RUN-G-01 — Reviewer Packet

REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Authority and scope

- Target erratum: validation/m1/errata/SCENARIO-G-TARGET-ERRATUM.md
- Erratum commit: eac2d7561a1b46096e2106e2201da3b7c6dd0788
- Input freeze: 626556e86441836b00d356ee9cf7f9471b360541
- Original targets: P08/P09
- Effective targets: P15/P16
- Frozen action and expected outcome remain those of Scenario G in the original scenario sheet.

## Same-Place premise

P15 and P16 are two distinct synthetic records representing the same intended synthetic locus, based on the frozen P16 synthetic-case-plan wording and the approved controlled fixture. This is not a general equivalence rule.

## Evidence

- common-pre-state.csv
- subcase-A/pre-run-state.csv and post-run-state.csv
- subcase-B/pre-run-state.csv and post-run-state.csv
- both checker fixtures and raw checker outputs
- operator-execution.md
- inputs.md and source-map.md

## Subcase review table

| Subcase | Survivor | Retired | Resolution Link | Succession | Historical resolution |
|---|---|---|---|---|---|
| A | FIX-ID-P15 | FIX-ID-P16 | FIX-RES-G-A-P16-TO-P15 | FIX-SUCC-G-A-P16-TO-P15 | P16 resolves to P15 |
| B | FIX-ID-P16 | FIX-ID-P15 | FIX-RES-G-B-P15-TO-P16 | FIX-SUCC-G-B-P15-TO-P16 | P15 resolves to P16 |

## Manual checks

Review same-Place premise, Resolution Link direction, retired resolvability, Succession predecessor/successor, retained history, byte-equivalent PRE snapshots and no-survivor-policy encoding. Checker output remains structural only.

## Isolation and acceptance limits

- Both directions are isolated alternatives, not sequential merges.
- No survivor-selection algorithm or policy is tested.
- This is a synthetic merge fixture only; no real-world merge is claimed.
- No production GeoID encoding, provider trust ranking, merge governance or AP-after-merge behavior is tested.
- E P08, C P16 and F P15 evidence remain run-local and are not imported.
- No overall M1 result is created.

## Decision state

The operator records evidence only. PASS, FAIL and INEXPRESSIBLE remain blank for independent review.
