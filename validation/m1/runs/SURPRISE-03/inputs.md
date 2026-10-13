# SURPRISE-03 — Frozen Conflicted Selection Fixture

> REVIEWER-SELECTED SURPRISE CASE — FROZEN BY HUMAN DECISION BEFORE OPERATOR EXECUTION.

- Baseline: `75b3769264e8e35eec1d8cc595ed1b52144df489`.
- Target: P13 Calmette Hospital coordinate-conflict case.
- P13 remains REAL and unresolved; no web access or new coordinate research is used.
- Frozen corpus evidence does not provide exact numeric competing coordinates, so the two values below are opaque evidence handles, not new factual coordinates.

## PRE — 4 rows

- `FIX-ID-P13` Place / REAL / `S03-PLACE-P13` / Quality `unknown`.
- `FIX-ID-P13-SA-COORD-A` Source Assertion / REAL / `S03-P13-COORD-A` / `ref=FIX-ID-P13; fact=coordinate; purpose=place-coordinate; value=FROZEN-P13-CONFLICTING-COORDINATE-A` / Quality `unknown`.
- `FIX-ID-P13-SA-COORD-B` Source Assertion / REAL / `S03-P13-COORD-B` / `ref=FIX-ID-P13; fact=coordinate; purpose=place-coordinate; value=FROZEN-P13-CONFLICTING-COORDINATE-B` / Quality `unknown`.
- `FIX-ID-P13-SA-NAME` Source Assertion / REAL / `S03-P13-NAME` / `ref=FIX-ID-P13; fact=name; purpose=display-name; language=en; value=Calmette Hospital` / Quality `unknown`.

No Current DAEN Representation exists in PRE. Both coordinate assertions remain retained and differ as opaque frozen conflict handles.

## POST — append two rows

1. `FIX-ID-P13-CR-COORD` / Current DAEN Representation / SYNTHETIC / `ref=FIX-ID-P13-SA-COORD-A; current_representation=true; place=FIX-ID-P13; fact=coordinate; purpose=place-coordinate` / Quality `unknown`.
2. `FIX-ID-P13-CR-NAME` / Current DAEN Representation / SYNTHETIC / `ref=FIX-ID-P13-SA-NAME; current_representation=true; place=FIX-ID-P13; fact=name; purpose=display-name; language=en` / Quality `unknown`.

No source ranking, winner/loser, conflict marker, trust score, confidence score or provider preference is added.
