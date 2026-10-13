# RUN-F-01 — Source and Provenance Map

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Commit anchors

- E acceptance baseline: `193a2f5614b48007eb4a832acbaf560ec12081c5`
- F input-freeze commit: recorded by the Git commit that adds this file and `inputs.md`
- F operator evidence: recorded after execution; not known at input-freeze time

## Frozen wording and context

| Label | Source | Context |
|---|---|---|
| Scenario F | `validation/m1/scenario-sheet.md`, Scenario F | Frozen action and expected outcome |
| F-PLACE-P04 | `validation/m1/corpus-evidence.md`, P04; `validation/m1/field-evidence/P04.md` | Real P04 Place context; field evidence is not corrected by this run |
| F-PLACE-P14 | `validation/m1/corpus-evidence.md`, P14 | Real Parking Tower premises, not company identity |
| F-PLACE-P15 | `validation/m1/synthetic-case-plan.md`, P15 | Synthetic duplicate seed context |
| C/F boundary | `validation/m1/reviews/RUN-C-01-disposition.md` | C's representation replacement is not F's Source Assertion correction |
| D:F5 / B:F4 | `validation/m1/reviews/RUN-D-01-disposition.md` | P04 entrance versus Access Point remains open |

## Ledger provenance mappings

| Ledger provenance | Meaning | Input mapping |
|---|---|---|
| `SYN-F-P04-ADDR-OLD` | P04 OLD Source Assertion provenance | `inputs.md`, P04 OLD address row |
| `SYN-F-P04-ADDR-REVISED` | P04 REVISED Source Assertion provenance | `inputs.md`, P04 REVISED address row |
| `SYN-F-P14-PROVIDER-OLD` | P14 OLD Source Assertion provenance | `inputs.md`, P14 OLD provider-reference row |
| `SYN-F-P14-PROVIDER-REVISED` | P14 REVISED Source Assertion provenance | `inputs.md`, P14 REVISED provider-reference row |
| `SYN-F-P15-ADDR` | P15 initial address provenance | `inputs.md`, P15 initial address row |
| `SYN-F-P15-COORD-OLD` | P15 OLD Source Assertion provenance | `inputs.md`, P15 OLD coordinate row |
| `SYN-F-P15-PROVIDER` | P15 initial provider-reference provenance | `inputs.md`, P15 initial provider row |
| `SYN-F-P15-COORD-REVISED` | P15 REVISED Source Assertion provenance | `inputs.md`, P15 REVISED coordinate row |

## Correction-action provenance mappings

| Ledger provenance | Meaning | Correction target |
|---|---|---|
| `SYN-F-CORR-P04` | Human/project-approved controlled M1 fixture action | `FIX-CORR-F-P04` |
| `SYN-F-CORR-P14` | Human/project-approved controlled M1 fixture action | `FIX-CORR-F-P14` |
| `SYN-F-CORR-P15` | Human/project-approved controlled M1 fixture action | `FIX-CORR-F-P15` |

Correction-action provenance is not a production correction-authority model. Operator attribution is recorded separately as Codex / RUN-F-01 / actual ledger row key; no undefined STEP aliases are introduced.

## Scope protections

- Source Assertion correction only; no Current DAEN Representation rows.
- No separate Succession row.
- P04 reference coordinate and observed entrance coordinate retain their different roles.
- All synthetic augmentation is marked `SYNTHETIC` at entry level.
- `unknown` is the explicit Quality value for every fixture assertion and correction action.
