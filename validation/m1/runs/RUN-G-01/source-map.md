# RUN-G-01 — Source and Provenance Map

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Commit anchors

- G target erratum: eac2d7561a1b46096e2106e2201da3b7c6dd0788
- G input-freeze commit: this controlled commit adding inputs.md and source-map.md
- E acceptance baseline: 193a2f5614b48007eb4a832acbaf560ec12081c5

## Target and Place context mappings

| Label | Frozen source |
|---|---|
| G-PLACE-P15 | validation/m1/synthetic-case-plan.md P15; validation/m1/corpus-register.csv P15 |
| G-PLACE-P16 | validation/m1/synthetic-case-plan.md P16; validation/m1/corpus-register.csv P16 |
| SYN-G-SAME-LOCUS | frozen P16 wording that P16 represents the same intended locus as P15; approved RUN-G-01 input |

## Source-record provenance

| Label | Meaning |
|---|---|
| SYN-G-P15-RECORD | P15 synthetic source-record assertion |
| SYN-G-P16-RECORD | P16 synthetic source-record assertion |

## Merge and succession provenance

| Label | Meaning |
|---|---|
| SYN-G-MERGE-A | controlled merge action for P15-survivor subcase |
| SYN-G-SUCC-A | controlled succession action for P16-to-P15 subcase |
| SYN-G-MERGE-B | controlled merge action for P16-survivor subcase |
| SYN-G-SUCC-B | controlled succession action for P15-to-P16 subcase |

All Quality values are unknown. All Place, Source Assertion, Resolution Link and Succession entries are SYNTHETIC.

## Historical and isolation references

- Original P08/P09 registration and its defect: validation/m1/errata/SCENARIO-G-TARGET-ERRATUM.md
- Frozen G action and expected outcome: validation/m1/scenario-sheet.md, Scenario G
- E:F6 boundary: validation/m1/reviews/RUN-E-01-disposition.md
- C/F run-local isolation boundary: validation/m1/reviews/RUN-C-01-disposition.md and RUN-F-01-disposition.md

The original scenario sheet is copied unchanged into each checker fixture. The erratum is the effective target authority for this run only.
