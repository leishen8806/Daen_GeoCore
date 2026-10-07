# RUN-F-01 — Frozen Correction Inputs

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Run and authority

- Run: `RUN-F-01`
- Scenario: F — Correction
- Scenario E acceptance baseline: `193a2f5614b48007eb4a832acbaf560ec12081c5`
- Frozen Scenario F wording: `validation/m1/scenario-sheet.md`, Scenario F
- Role: M1 Data Operator — Codex
- Operator attribution is recorded in the execution record, separately from assertion provenance.

## Controlled correction scope

RUN-F-01 corrects Source Assertions only. It does not initialize, create, replace or supersede any Current DAEN Representation. Scenario C already tested representation replacement.

No separate `Succession` row is created. The Source Assertion supersession chain is used directly under Domain Model §19. Correction authority and governance remain deferred; these are controlled M1 fixture actions only.

All new F facts and actions are `SYNTHETIC`, including synthetic assertions attached to the real P04 and P14 Places. P15 is a synthetic Place.

## Place context

| Place handle | Corpus slot | Classification | Context label |
|---|---|---|---|
| `FIX-ID-P04` | P04 — AEON Mall Phnom Penh | REAL | `F-PLACE-P04` |
| `FIX-ID-P14` | P14 — AEON Mall Cambodia Parking Tower building | REAL | `F-PLACE-P14` |
| `FIX-ID-P15` | P15 — Synthetic duplicate seed | SYNTHETIC | `F-PLACE-P15` |

## P04 — synthetic address correction

The real P04 Place remains unchanged. The general Place-reference coordinate and observed entrance coordinate are not treated as OLD versus corrected; B:F4 / D:F5 remains open.

| Role | Subject | Provenance | Fact | Purpose | Value | Quality |
|---|---|---|---|---|---|---|
| OLD | `FIX-ID-P04-SA-ADDR-OLD` | `SYN-F-P04-ADDR-OLD` | address | place-address | `SYNTHETIC ONLY — Test Address P04, Building 41` | unknown |
| REVISED | `FIX-ID-P04-SA-ADDR-REVISED` | `SYN-F-P04-ADDR-REVISED` | address | place-address | `SYNTHETIC ONLY — Test Address P04, Building 14` | unknown |

Correction: `FIX-CORR-F-P04`, provenance `SYN-F-CORR-P04`, target `FIX-ID-P04`, fact `address`, OLD `FIX-ID-P04-SA-ADDR-OLD`, REVISED `FIX-ID-P04-SA-ADDR-REVISED`.

Rationale: The OLD address contains a deliberately introduced transposition error for this controlled fixture. The REVISED address corrects that synthetic error for the same unchanged P04 locus. This is not a relocation, new Place, public-source correction or claim about AEON Mall's real address.

## P14 — synthetic provider-reference correction

The real P14 Parking Tower premises remains unchanged. Scenario C's display-name spelling correction is not reused.

| Role | Subject | Provenance | Fact | Purpose | Value | Quality |
|---|---|---|---|---|---|---|
| OLD | `FIX-ID-P14-SA-PROVIDER-OLD` | `SYN-F-P14-PROVIDER-OLD` | provider-reference | external-location-reference | `SYN-F-P14-PROVIDER-REF-WRONG` | unknown |
| REVISED | `FIX-ID-P14-SA-PROVIDER-REVISED` | `SYN-F-P14-PROVIDER-REVISED` | provider-reference | external-location-reference | `SYN-F-P14-PROVIDER-REF-CORRECT` | unknown |

Correction: `FIX-CORR-F-P14`, provenance `SYN-F-CORR-P14`, target `FIX-ID-P14`, fact `provider-reference`, OLD `FIX-ID-P14-SA-PROVIDER-OLD`, REVISED `FIX-ID-P14-SA-PROVIDER-REVISED`.

Rationale: The OLD provider/reference value is deliberately wrong in this controlled fixture. The REVISED provider/reference value corrects the external reference for the same unchanged P14 locus. Provider reference is not Place identity, and this correction does not change the Place.

## P15 — synthetic coordinate correction

All P15 values are synthetic fixture values only; they are not geographic claims or production coordinate standards.

| Role | Subject | Provenance | Fact | Purpose | Value | Quality |
|---|---|---|---|---|---|---|
| Initial | `FIX-ID-P15-SA-ADDR` | `SYN-F-P15-ADDR` | address | place-address | `SYNTHETIC ONLY — P15 Test Premises, Lot 15` | unknown |
| OLD | `FIX-ID-P15-SA-COORD-OLD` | `SYN-F-P15-COORD-OLD` | coordinate | place-reference | `0.050000, 0.050000` | unknown |
| Initial | `FIX-ID-P15-SA-PROVIDER` | `SYN-F-P15-PROVIDER` | provider-reference | external-location-reference | `SYN-F-P15-PROVIDER-REF-0015` | unknown |
| REVISED | `FIX-ID-P15-SA-COORD-REVISED` | `SYN-F-P15-COORD-REVISED` | coordinate | place-reference | `0.051000, 0.049000` | unknown |

Correction: `FIX-CORR-F-P15`, provenance `SYN-F-CORR-P15`, target `FIX-ID-P15`, fact `coordinate`, OLD `FIX-ID-P15-SA-COORD-OLD`, REVISED `FIX-ID-P15-SA-COORD-REVISED`.

Rationale: The OLD coordinate is deliberately wrong in this synthetic fixture. The REVISED coordinate is the approved correction for the same unchanged P15 locus. The differing coordinate does not create a new Place and does not imply merge, split or relocation. The initial address and provider-reference assertions remain unchanged.

## PRE / POST plan

- PRE contains 8 data rows: three Place rows, P04 OLD address, P14 OLD provider reference, and P15's initial address, OLD coordinate and initial provider reference.
- POST appends 3 revised Source Assertions and 3 Correction rows for 14 data rows total.
- No Current DAEN Representation row exists in PRE or POST.
- No separate Succession row exists.
- Every revised Source Assertion carries `supersedes_reference` to the exact OLD Source Assertion ledger row.
- Each Correction row uses existing ledger fields only; `ref=` points to the revised assertion and `corrects=` names the OLD assertion.

## Manual review questions and limits

- Are all OLD assertions retained and all revised assertions attributable?
- Does each revised assertion supersede the intended OLD assertion?
- Does each Correction row identify the intended Place, fact, OLD and REVISED values?
- Is the Place identity set unchanged?
- Are no Current DAEN Representation or Succession semantics introduced?
- P04 real address/coordinate truth is not being corrected; its entrance/general-coordinate issue remains open.
- P14's C-name change is not reused.
- Production correction authority remains TBD.
- No overall M1 result is created.
