# RUN-D-01 — Approved Scenario D Access Fixtures

> PRE-EXECUTION INPUT RECORD — VALIDATION EVIDENCE ONLY. NOT A SPECIFICATION.

## Baseline and frozen scope

- **Baseline:** `df9fb2f6e3bfdfb9cccb66ad6f4d44b5afc2cf28` (Scenario C acceptance)
- **Branch:** `phase/04-m1-execution`
- **Run:** `RUN-D-01`
- **Role:** M1 Data Operator — Codex
- **Scenario:** D — Access Point
- **Targets:** `P05`, `P06`, `P07`
- **Action:** Represent an Access Point that differs from the Selected Coordinate.
- **Expected outcome:** Access Point remains separate and is not inferred solely from the coordinate.

P04 remains supporting context only. No new public research or field verification is used. The coordinates below are synthetic test pairs, not real-world measurements; they are not geocoded, navigable, publishable or a production geometry/precision model.

## Exact approved synthetic inputs

| Target | Selected test coordinate | Access-evidence test coordinate | Local Access Point handle | Place classification |
|---|---|---|---|---|
| P05 | `0.010000, 0.010000` | `0.009000, 0.011000` | `FIX-AP-D-SHARED` | SYNTHETIC |
| P06 | `0.010000, 0.012000` | `0.009000, 0.011000` | `FIX-AP-D-SHARED` | SYNTHETIC |
| P07 | `0.020000, 0.020000` | `0.019000, 0.020500` | `FIX-AP-D-P07` | REAL physical Place; synthetic augmentation for this run |

Place-reference assertion origins are `SYN-D-REF-P05`, `SYN-D-REF-P06` and `SYN-D-REF-P07`, each with `fact=coordinate` and `purpose=place-reference`. Controlled initial coordinate selections are authorized and are `SYNTHETIC`.

## Exact access statements

### SYN-D-ACCESS-SHARED

“In this fictional mall fixture, one common public pedestrian/vehicle access threshold serves both P05 and P06. Its test coordinate is 0.009000, 0.011000. Its access function and location are supplied by this mock access record, independently of the Place-reference coordinate assertions.”

### SYN-D-ACCESS-P07

“Within the hypothetical P07 augmentation used only by RUN-D-01, one public pedestrian access threshold serves P07. Its test coordinate is 0.019000, 0.020500. Its access function and location are supplied by this mock access record, independently of the Place-reference coordinate assertion. This is not a claim about an actual RUPP gate, its real coordinate or current public accessibility.”

Independent means separately specified fixture evidence. Numeric difference alone is not proof of access; the access meaning comes from the separate mock access statement.

## Place and object boundaries

- `FIX-ID-P05` and `FIX-ID-P06` are synthetic Place handles from the frozen P05/P06 fixture context.
- `FIX-ID-P07` is a validation handle for the REAL RUPP campus context supported by frozen corpus evidence.
- `FIX-AP-D-SHARED` is one synthetic Access Point object serving both P05 and P06.
- `FIX-AP-D-P07` is one synthetic Access Point object serving P07.
- All new coordinate assertions, access statements, controlled selections and Access Point objects are `SYNTHETIC` with Quality `unknown`.
- Handles are local validation labels, not GeoIDs or public namespace proposals.
- No P15/P16 merge, parent mall, new corpus slot, business entity, containment, routing or pickup/drop-off operation is introduced.

## PRE / POST plan

### PRE state

Materialize separate entries for:

1. P05, P06 and P07 Place context;
2. one Place-reference coordinate Source Assertion per target;
3. one controlled initial coordinate selection per target;
4. the two independent access Source Assertions.

The two Access Point objects do not exist in PRE.

### POST state

Retain every PRE row unchanged and append exactly two Access Point object rows: `FIX-AP-D-SHARED` and `FIX-AP-D-P07`. Each object references its access assertion, identifies the served Place or Places, and preserves the supplied access meaning and test coordinate.

Do not replace selected Place-reference coordinates with Access Point coordinates. Do not perform selection supersession, Correction, Merge, Split, lifecycle, containment, routing or pickup/drop-off operations.

## Provenance and Quality

| Label | Meaning | Classification | Quality |
|---|---|---|---|
| `D-PLACE-P05` | Frozen synthetic-case-plan.md P05 context | SYNTHETIC | `unknown` |
| `D-PLACE-P06` | Frozen synthetic-case-plan.md P06 context | SYNTHETIC | `unknown` |
| `D-PLACE-P07` | Frozen corpus-evidence.md P07 campus context | REAL | `unknown` |
| `SYN-D-REF-P05/P06/P07` | Exact approved coordinate input statements | SYNTHETIC | `unknown` |
| `SYN-D-ACCESS-SHARED` | Exact shared access statement | SYNTHETIC | `unknown` |
| `SYN-D-ACCESS-P07` | Exact P07 augmentation access statement | SYNTHETIC | `unknown` |

## Manual-review questions

- Are Access Point objects separate from Place and coordinate assertions?
- Does P05/P06 share exactly one Access Point object?
- Is P07's synthetic augmentation kept distinct from real RUPP evidence?
- Is each AP supported by a separate access statement rather than inferred from numeric difference?
- Are all PRE rows retained and all Place identities and initial selections unchanged?
- Are provenance, Quality and REAL/SYNTHETIC markings explicit?

## Crosswalk

- Domain Model §13: coordinate is a location fact and does not establish Place identity.
- Domain Model §14 and DM-9: Access Point is separate and is not inferred solely from Selected Coordinate.
- Domain Model §17: persisted facts and Source Assertions must be attributable.
- M1-B6: Access Point separation.
- M1-B10: explicit Quality; `unknown` is valid.
