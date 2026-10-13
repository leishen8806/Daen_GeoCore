# RUN-D-01 — Source Map

> OPERATOR EVIDENCE — SOURCE MAPPING ONLY. NOT A PRODUCTION PROVENANCE MODEL.

## Existing Place context

| Provenance label | Source | Statement supported | Limitation |
|---|---|---|---|
| `D-PLACE-P05` | `validation/m1/synthetic-case-plan.md`, P05 section, baseline `df9fb2f6e3bfdfb9cccb66ad6f4d44b5afc2cf28` | Synthetic Mall Unit A context, distinct synthetic coordinate and access concept | Synthetic fixture only; no real-world claim. |
| `D-PLACE-P06` | `validation/m1/synthetic-case-plan.md`, P06 section, baseline `df9fb2f6e3bfdfb9cccb66d6f4d44b5afc2cf28` | Synthetic Mall Unit B context and shared-access relationship | Synthetic fixture only; no real-world claim. |
| `D-PLACE-P07` | `validation/m1/corpus-evidence.md`, P07 section, baseline `df9fb2f6e3bfdfb9cccb66d6f4d44b5afc2cf28` | Royal University of Phnom Penh campus is a public REAL Place | Campus boundary and preferred approach remain uncertain; no real gate is asserted here. |

## Approved mock inputs

| Provenance label | Source | Statement supported | Limitation |
|---|---|---|---|
| `SYN-D-REF-P05` | This run's `inputs.md`, P05 coordinate row; input-freeze commit recorded after creation | Place-reference coordinate `0.010000, 0.010000` | Synthetic test value only. |
| `SYN-D-REF-P06` | This run's `inputs.md`, P06 coordinate row; input-freeze commit recorded after creation | Place-reference coordinate `0.010000, 0.012000` | Synthetic test value only. |
| `SYN-D-REF-P07` | This run's `inputs.md`, P07 coordinate row; input-freeze commit recorded after creation | Place-reference coordinate `0.020000, 0.020000` | Synthetic augmentation for a REAL Place; not a RUPP measurement. |
| `SYN-D-ACCESS-SHARED` | This run's `inputs.md`, exact shared access statement; input-freeze commit recorded after creation | One common public pedestrian/vehicle threshold at `0.009000, 0.011000` serves P05 and P06 | Fictional mock access record; not independent real-world verification. |
| `SYN-D-ACCESS-P07` | This run's `inputs.md`, exact P07 access statement; input-freeze commit recorded after creation | One hypothetical public pedestrian threshold at `0.019000, 0.020500` serves P07 | Explicitly not a claim about an actual RUPP gate or accessibility. |

All labels used in the run map to this table. Every new assertion, selection and Access Point object is `SYNTHETIC` with Quality `unknown`.
