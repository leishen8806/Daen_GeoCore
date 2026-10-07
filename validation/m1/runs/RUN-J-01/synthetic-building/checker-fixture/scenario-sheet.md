# M1 Scenario Sheet

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

This sheet copies the frozen Phase 04 scenarios. Actual results remain blank. No scenario has been executed.

## A — Stable Identity

- **Scenario ID:** A
- **Name:** Stable Identity
- **Target corpus slots:** P01, P02
- **Pre-registered action:** Represent one persistent locus through changed names, scripts or references while retaining one Place identity.
- **Expected outcome:** One Place and one GeoID remain stable; representations and assertions may vary.
- **Phase 03 rule / invariant reference:** Place definition, Place identity boundary, GeoID semantics, invariants 1 and 4.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## B — Multiple Source Assertions

- **Scenario ID:** B
- **Name:** Multiple Source Assertions
- **Target corpus slots:** P02, P03, P04, P17
- **Pre-registered action:** Record multiple attributed name, address and coordinate assertions, including conflict.
- **Expected outcome:** Assertions remain attributable; conflict does not silently create or merge Places; Quality is explicit.
- **Phase 03 rule / invariant reference:** Source Assertion, Provenance, Quality, invariants 5 and 10.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## C — Current DAEN Representation Change

- **Scenario ID:** C
- **Name:** Current DAEN Representation Change
- **Target corpus slots:** P04, P14, P16
- **Pre-registered action:** Change the Current DAEN Representation in response to a correction or stronger evidence.
- **Expected outcome:** Current representation changes without destructive overwrite; prior material state remains traceable.
- **Phase 03 rule / invariant reference:** Current DAEN Representation, Correction, Succession, invariants 4, 8 and 9.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## D — Access Point

- **Scenario ID:** D
- **Name:** Access Point
- **Target corpus slots:** P05, P06, P07
- **Pre-registered action:** Represent an Access Point that differs from the Selected Coordinate.
- **Expected outcome:** Access Point remains a separate object and is not inferred solely from the coordinate.
- **Phase 03 rule / invariant reference:** Access Point semantics, Selected Coordinate, invariant 6.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## E — Shared Access Point

- **Scenario ID:** E
- **Name:** Shared Access Point
- **Target corpus slots:** P07
- **Pre-registered action:** Represent one Access Point serving multiple Places.
- **Expected outcome:** One shared Access Point is represented once and linked to multiple Places without business pickup or drop-off semantics.
- **Phase 03 rule / invariant reference:** Access Point semantics, invariant 7.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## F — Correction

- **Scenario ID:** F
- **Name:** Correction
- **Target corpus slots:** P04, P14, P15
- **Pre-registered action:** Correct a wrong address, coordinate or provider reference while retaining material history.
- **Expected outcome:** The wrong fact is superseded, attribution remains available and Place identity is not silently changed.
- **Phase 03 rule / invariant reference:** Location Correction, Source Assertion, Succession, invariants 2, 5 and 8.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## G — Merge

- **Scenario ID:** G
- **Name:** Merge
- **Target corpus slots:** P08, P09
- **Pre-registered action:** Test both survivor directions for two records determined to represent the same Place.
- **Expected outcome:** One identity resolves to the survivor, the retired GeoID remains resolvable and no survivor-selection policy is invented.
- **Phase 03 rule / invariant reference:** Merge semantics, Resolution Link, Succession, invariants 1 and 3.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## H — Split

- **Scenario ID:** H
- **Name:** Split
- **Target corpus slots:** P10, P11
- **Pre-registered action:** Test mis-conflation and true division separately.
- **Expected outcome:** Mis-conflation preserves the true original identity where applicable; true division gives resulting Places new GeoIDs while the historical GeoID remains resolvable.
- **Phase 03 rule / invariant reference:** Split semantics, Resolution Link, Succession, invariants 1 and 3.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## I — Withdrawal / Closure

- **Scenario ID:** I
- **Name:** Withdrawal / Closure
- **Target corpus slots:** P12, P13
- **Pre-registered action:** Mark one Place closed and one historical reference withdrawn.
- **Expected outcome:** GeoIDs remain resolvable as closed, withdrawn or historical; resolvable does not mean active or valid for new operational use.
- **Phase 03 rule / invariant reference:** Closure and Withdrawal semantics, invariant 3.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**

## J — Containment

- **Scenario ID:** J
- **Name:** Containment
- **Target corpus slots:** P18, P19
- **Pre-registered action:** Represent two minimal Place-contains-Place relationships.
- **Expected outcome:** Containment is represented without inventing Area, business hierarchy or a taxonomy beyond the frozen minimal relationship.
- **Phase 03 rule / invariant reference:** Containment, invariant 11 and excluded concepts.
- **Actual result:**
- **PASS / FAIL / INEXPRESSIBLE:**
- **Friction references:**
