# DAEN Geo Core — M1 Initial State Plan

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

Before `RUN-A-01`, the operator will confirm the following planned initial state. This document is a plan only; it does not populate `state-ledger.csv`.

## Required initial state

- All 20 corpus slots P01–P20 exist with their frozen REAL/SYNTHETIC classifications.
- Local fixture handles are planned as `FIX-ID-P01` through `FIX-ID-P20`; these are not GeoIDs.
- Source Assertions are registered from the frozen source assertion plan.
- Every synthetic assertion or event is marked `SYNTHETIC` at entry level.
- P04 field evidence is referenced as `P04-FIELD-AP01`.
- P13 has multiple conflicting Source Assertions and remains `PUBLIC-SOURCE CONFLICT — UNRESOLVED`.
- P04 does not receive a Current DAEN Representation selection from the field evidence alone.

## Explicitly absent before execution

- No scenario mutation is applied.
- No correction is applied.
- No merge is applied.
- No split is applied.
- No withdrawal or closure mutation is applied.
- No actual result, friction finding or decision outcome is populated.

The first executable run is `RUN-A-01` after independent readiness review.
