# M1 Scenarios

This file pre-registers scenarios only. The execution-result and friction-reference fields are intentionally empty. No scenario has been executed.

## Frozen Phase 03 references

Scenario references use the approved [Domain Model](../GEO_CORE_DOMAIN_MODEL.md): Place, GeoID, Source Assertion, Current DAEN Representation, Access Point, Extent, Resolution Link, Provenance, Quality, Correction, Merge, Split, Withdrawal, Closure, Containment and Domain Invariants.

## A — Stable Identity

- **Target slots:** P01, P02
- **Action:** Represent one persistent locus through changed names, scripts or references while retaining one Place identity.
- **Expected outcome:** One Place and one GeoID remain stable; representations and assertions may vary.
- **Phase 03 rule:** Place definition, Place identity boundary, GeoID semantics, invariants 1 and 4.
- **Execution result:**
- **Friction references:**

## B — Multiple Source Assertions

- **Target slots:** P02, P03, P04, P17
- **Action:** Record multiple attributed name, address and coordinate assertions, including conflict.
- **Expected outcome:** Assertions remain attributable; conflict does not silently create or merge Places; Quality is explicit.
- **Phase 03 rule:** Source Assertion, Provenance, Quality, invariant 5 and invariant 10.
- **Execution result:**
- **Friction references:**

## C — Current DAEN Representation Change

- **Target slots:** P04, P14, P16
- **Action:** Change the Current DAEN Representation in response to a correction or stronger evidence.
- **Expected outcome:** Current representation changes without destructive overwrite; prior material state remains traceable.
- **Phase 03 rule:** Current DAEN Representation, Correction, Succession, invariants 4, 8 and 9.
- **Execution result:**
- **Friction references:**

## D — Access Point

- **Target slots:** P05, P06, P07
- **Action:** Represent an Access Point that differs from the Selected Coordinate.
- **Expected outcome:** Access Point remains a separate object and is not inferred solely from the coordinate.
- **Phase 03 rule:** Access Point semantics, Selected Coordinate, invariant 6.
- **Execution result:**
- **Friction references:**

## E — Shared Access Point

- **Target slots:** P07
- **Action:** Represent one Access Point serving multiple Places.
- **Expected outcome:** One shared Access Point is represented once and linked to multiple Places without business pickup or drop-off semantics.
- **Phase 03 rule:** Access Point semantics, invariant 7.
- **Execution result:**
- **Friction references:**

## F — Correction

- **Target slots:** P04, P14, P15
- **Action:** Correct a wrong address, coordinate or provider reference while retaining material history.
- **Expected outcome:** The wrong fact is superseded, attribution remains available and Place identity is not silently changed.
- **Phase 03 rule:** Location Correction, Source Assertion, Succession, invariants 2, 5 and 8.
- **Execution result:**
- **Friction references:**

## G — Merge

- **Target slots:** P08, P09
- **Action:** Test both survivor directions for two records determined to represent the same Place.
- **Expected outcome:** One identity resolves to the survivor, the retired GeoID remains resolvable and no survivor-selection policy is invented.
- **Phase 03 rule:** Merge semantics, Resolution Link, Succession, invariants 1 and 3.
- **Execution result:**
- **Friction references:**

## H — Split

- **Target slots:** P10, P11
- **Action:** Test mis-conflation and true division separately.
- **Expected outcome:** Mis-conflation preserves the true original identity where applicable; true division gives resulting Places new GeoIDs while the historical GeoID remains resolvable.
- **Phase 03 rule:** Split semantics, Resolution Link, Succession, invariants 1 and 3.
- **Execution result:**
- **Friction references:**

## I — Withdrawal / Closure

- **Target slots:** P12, P13
- **Action:** Mark one Place closed and one historical reference withdrawn.
- **Expected outcome:** GeoIDs remain resolvable as closed, withdrawn or historical; resolvable does not mean active or valid for new operational use.
- **Phase 03 rule:** Closure and Withdrawal semantics, invariant 3.
- **Execution result:**
- **Friction references:**

## J — Containment

- **Target slots:** P18, P19
- **Action:** Represent two minimal Place-contains-Place relationships.
- **Expected outcome:** Containment is represented without inventing Area, business hierarchy or a taxonomy beyond the frozen minimal relationship.
- **Phase 03 rule:** Containment, invariant 11 and excluded concepts.
- **Execution result:**
- **Friction references:**
