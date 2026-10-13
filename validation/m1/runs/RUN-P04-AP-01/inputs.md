# RUN-P04-AP-01 — Frozen P04 Real Access Point Anchor

> SUPPLEMENTAL BOUNDED EVALUATION — NOT A SCENARIO D RERUN.

- Human freeze baseline: `75b3769264e8e35eec1d8cc595ed1b52144df489`.
- Reviewer-selected bounded completion work; frozen before operator execution.
- Source: `validation/m1/field-evidence/P04.md`.

## PRE — exactly two rows

1. `FIX-ID-P04` / Place / REAL / `P04-ANCHOR-PLACE` / Quality `unknown`.
2. `FIX-ID-P04-SA-REF-COORD` / Source Assertion / REAL / `P04-FIELD-REFERENCE` / `ref=FIX-ID-P04; fact=coordinate; purpose=general-place-reference; value=11.5479358,104.9325711` / Quality `unknown`.

The reference coordinate is not called the Selected Coordinate.

## POST — append exactly one Access Point

`FIX-AP-P04-FIELD-01` / Access Point / REAL / `P04-FIELD-AP01` / Quality `unknown` / `ref=FIX-ID-P04; served_place=FIX-ID-P04; coordinate=11.548290,104.931271; access=vehicle-and-pedestrian; publicly_usable=true; differs_from_general_reference=true`.

This is the observed AEON Phnom Penh public entrance. No pickup/drop-off semantics, Current DAEN Representation or correction is created. Operator records evidence only; reviewer decides whether the real anchor is satisfied.
