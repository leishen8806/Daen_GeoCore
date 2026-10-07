# RUN-H-01 — Source and Provenance Map

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Commit anchors

- H target erratum: 6b572bc5ba03f275d25a21f727515128326a7d73
- H input-freeze commit: this controlled commit adding inputs.md and source-map.md
- G acceptance baseline: f46a610f9fa6b695c52ab10e6e20a97fb9d1d49a

## Place context

| Label | Frozen source |
|---|---|
| H-PLACE-P17 | validation/m1/synthetic-case-plan.md P17; validation/m1/corpus-register.csv P17 |
| H-PLACE-P18 | validation/m1/synthetic-case-plan.md P18; validation/m1/corpus-register.csv P18 |

## P17 mappings

| Label | Meaning |
|---|---|
| SYN-H-P17-L1 | Locus A Source Assertion |
| SYN-H-P17-L2-OLD | Mis-conflated Locus B historical Source Assertion |
| SYN-H-P17-B-PLACE | New Locus B Place |
| SYN-H-P17-L2-NEW | Corrected Locus B Source Assertion |
| SYN-H-RES-P17 | Mis-conflation separation Resolution Link |

## P18 mappings

| Label | Meaning |
|---|---|
| SYN-H-P18-HIST | Historical parent Source Assertion |
| SYN-H-P18-DIVISION-PREMISE | Controlled true-division premise |
| SYN-H-P18-A-PLACE | Child A Place |
| SYN-H-P18-A | Child A Source Assertion |
| SYN-H-P18-B-PLACE | Child B Place |
| SYN-H-P18-B | Child B Source Assertion |
| SYN-H-RES-P18-A | Parent-to-child-A Resolution Link |
| SYN-H-RES-P18-B | Parent-to-child-B Resolution Link |
| SYN-H-SUCC-P18-A | Parent-to-child-A Succession |
| SYN-H-SUCC-P18-B | Parent-to-child-B Succession |

All Quality values are unknown and all H entries are SYNTHETIC.

## Protected boundaries

- Historical H targets P10/P11 remain in the original scenario sheet and runbook.
- P17 prior RUN-B unresolved evidence remains unchanged and is not imported.
- P18 remains a future historical J target under the original sheet; H does not pre-decide containment.
- New result handles are local validation identities, not corpus slots or production GeoIDs.
