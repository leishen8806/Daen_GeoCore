# RUN-B-01 — Approved Scenario B Inputs

> PRE-EXECUTION INPUT RECORD — VALIDATION EVIDENCE ONLY. NOT A SPECIFICATION.

## Baseline and scope

- **Reviewed baseline:** `1175e75208e29c4a72ea668b0289cd2fd964afbb` (`1175e75`)
- **Branch:** `phase/04-m1-execution`
- **Run:** `RUN-B-01`
- **Role:** M1 Data Operator — Codex
- **Scenario:** B — Multiple Source Assertions
- **Targets:** `P02`, `P03`, `P04`, `P17` only
- **Execution boundary:** add attributed Source Assertions only. No Current DAEN Representation selection, correction, merge, split, lifecycle event, Access Point object, provider ranking or GeoID assignment.

## Frozen Scenario B wording

From the unchanged `validation/m1/scenario-sheet.md`:

- **Pre-registered action:** Record multiple attributed name, address and coordinate assertions, including conflict.
- **Expected outcome:** Assertions remain attributable; conflict does not silently create or merge Places; Quality is explicit.

Coverage is assessed across Scenario B. Every target need not supply every assertion category individually. P02 and P03 use only supported frozen name evidence; P04 supplies the address and coordinate coverage; P17 supplies the approved synthetic conflict.

## Approved inputs and evidence references

### P02 — REAL

- **Research display name:** Royal Palace of Cambodia
- **Name assertions:** English `Royal Palace of Cambodia`; Khmer `ព្រះបរមរាជវាំង`.
- **Evidence:** `validation/m1/corpus-evidence.md`, P02 section; frozen public references listed there (Cambodia tourism, Royal Palace site, Chinese public reference).
- **Use in this run:** name variation with explicit language context only.
- **Address / coordinate:** none supplied for RUN-B-01. Do not manufacture either.
- **Known limitation:** complex boundary and public map centroid are not treated as an Access Point or exact fact here.

### P03 — REAL

- **Research display name:** Raffles Hotel Le Royal Phnom Penh
- **Name assertion:** supported frozen public name `Raffles Hotel Le Royal Phnom Penh`.
- **Evidence:** `validation/m1/corpus-evidence.md`, P03 section; frozen Raffles and Accor references listed there.
- **Use in this run:** supported name assertion only. Two source links do not automatically create two different name assertions.
- **Address / coordinate:** none supplied for RUN-B-01. Do not manufacture either.
- **Known limitation:** historical operational closure or rebranding is an occupant/business event, not Place closure.

### P04 — REAL

- **Research display name:** AEON Mall Phnom Penh
- **Address assertion:** `#132 Samdach Sothearos Blvd (3), Sangkat Tonle Bassac, Khan Chamkarmon, Phnom Penh, Cambodia`.
- **General public-reference coordinate:** `11.5479358, 104.9325711`.
- **Observed entrance coordinate:** `11.548290, 104.931271`.
- **Evidence:** `validation/m1/field-evidence/P04.md`, Evidence ID `P04-FIELD-AP01`; official AEON source and frozen field evidence.
- **Use in this run:** preserve the general reference coordinate and observed entrance coordinate as role-distinguished coordinate assertions. Different roles are not automatically contradictory.
- **Access Point boundary:** do not create or mutate an Access Point object in Scenario B.
- **Known limitation:** field-evidence notes official-page support is partial for the exact entrance coordinate; no Current DAEN Representation is selected.

### P17 — SYNTHETIC

These are newly approved synthetic test inputs, not historical public facts. Every assertion is marked `SYNTHETIC`.

#### Fixture background

`L1` and `L2` are two distinct, disjoint premises within one fictional test yard. Neither contains the other. They are narrative fixture locus labels only: not GeoIDs, not corpus slots and not new domain object types.

The raw source-record token is `SAMPLE-P17-R`; it is not a canonical DAEN identity. Both statements concern `TEST-T0` and the same role: exclusive association of that raw record with one physical premises.

#### Source A

- **Provenance:** `SYN-P17-SOURCE-A`
- **Name expression:** `SYNTHETIC P17 Facility`
- **Address expression:** `SYNTHETIC ONLY — Test Yard 17, North Plot`
- **Exact association claim:** “At TEST-T0, source record SAMPLE-P17-R describes only premises L1, the North Plot. It does not describe premises L2.”
- **Quality:** `unknown`
- **Classification:** `SYNTHETIC`

#### Source B

- **Provenance:** `SYN-P17-SOURCE-B`
- **Name expression:** `SYNTHETIC P17 Facility`
- **Address expression:** `SYNTHETIC ONLY — Test Yard 17, South Plot`
- **Exact association claim:** “At TEST-T0, source record SAMPLE-P17-R describes only premises L2, the South Plot. It does not describe premises L1.”
- **Quality:** `unknown`
- **Classification:** `SYNTHETIC`

#### Required handling

Preserve both as attributed Source Assertions and keep the association unresolved. Do not declare either source correct, collapse L1/L2, split or merge anything, or create an accepted canonical identity mapping. P17 remains unresolved source evidence under Domain Model §4.2; it does not require a confirmed Place row or an issued fixture identity in this run. Do not add numeric coordinates; P04 supplies coordinate coverage.

## Pre-run and added-assertion assignment

### Pre-run state

Materialize only minimum local fixture context for P02, P03 and P04 using `FIX-ID-P02`, `FIX-ID-P03` and `FIX-ID-P04`. Each is a validation stand-in, not an actual or proposed GeoID. Keep Place rows distinct from Source Assertion rows. P17 has no accepted Place row and no `FIX-ID-P17`.

Pre-run entries are limited to the existing frozen public identity context and supported baseline assertions. No future-scenario mutation, selection, correction or conflict resolution is present.

### Added during RUN-B-01

- P02: Khmer name assertion with `language=km`; no invented address/coordinate.
- P03: supported frozen name assertion only; no invented address/coordinate.
- P04: frozen address plus role-distinguished general-reference and observed-entrance coordinate assertions.
- P17: both approved synthetic Source Assertions, retained unresolved.

All added assertions carry provenance and explicit Quality. `unknown` is valid. Pre-run rows remain byte-for-byte unchanged in the post-run state.

## Expected identity / Place set

- **Before:** accepted Places are `FIX-ID-P02`, `FIX-ID-P03`, `FIX-ID-P04`; no accepted P17 Place identity.
- **After:** the accepted Place set is unchanged: `FIX-ID-P02`, `FIX-ID-P03`, `FIX-ID-P04`; P17 remains unresolved source evidence. Added Source Assertions are not new Places.
- No Current DAEN Representation selection or `current_representation=true` flag is required or permitted.

## Required manual checks

- Every assertion remains attributable to its source and run evidence.
- Name language scopes are explicit where applicable.
- P04 coordinate roles are distinguished and are not treated as an Access Point mutation or automatic contradiction.
- P17 claims share raw record, time and association role but have exclusive, different referents; both remain unresolved.
- No conflict silently creates, merges or splits a Place.
- No source claim is promoted to an accepted DAEN identity mapping.
- REAL/SYNTHETIC markings and `unknown` Quality are explicit.
- No semantic verdict is recorded by the operator.

## Invariant crosswalk and traceability

The frozen scenario sheet's shorthand is preserved, but its reference to “invariants 5 and 10” is disambiguated here:

- `DM-5` / Domain Model invariant 5: multiple representations do not automatically create multiple Places.
- `DM-6` / Domain Model invariant 6: similar representations do not prove the same Place; relevant to keeping unresolved claims unresolved.
- `M1-B5`: Source Assertions remain attributable after change.
- `M1-B10`: every fact evaluated or selected as a Current DAEN Representation during M1 has explicit Quality; `unknown` is valid. Scenario B's explicit Quality wording is operationally checked here even though no Current DAEN Representation is selected.
- `M1-B11`: no business entity or business decision is required to complete M1.
- Domain Model §4.2 defines Source Assertion as a source-attributed statement about a Place or unresolved real-world location; this is the basis for P17 without a confirmed Place row.
- Domain Model §10 defines the Source Assertion model and the assertion categories used here.
- Domain Model §17 requires persisted Source Assertions and material facts to be attributable.
- Domain Model §18 requires Quality to distinguish known, uncertain, stale, conflicting, incomplete or corrected information; quality scales remain TBD and `unknown` is used.
- Domain Model §10 / DM-10 concerns pickup/drop-off semantics in the frozen invariant numbering; it is not a Quality rule. Explicit Quality is M1-B10 and Scenario B wording.

## Evidence limitations

P02/P03 memo support is not exact original-webpage verification. P04 field evidence distinguishes official-page support, general reference point and observed entrance, and does not select a canonical coordinate. P17 is an approved synthetic fixture only. No external research or new field evidence is authorized for this run.

## Checker boundary

The existing checker self-test must pass before execution. Scenario B has no selections, so M1-M04 will not exercise every Source Assertion's Quality. Operator records will include per-assertion provenance and Quality checklists. Checker output is structural evidence only and cannot establish conflict meaning, source truth, REAL/SYNTHETIC correctness or semantic Scenario B success.

