# SURPRISE-02 — Frozen Containment × Closure Fixture

> REVIEWER-SELECTED SURPRISE CASE — FROZEN BY HUMAN DECISION BEFORE OPERATOR EXECUTION.

- Baseline: `75b3769264e8e35eec1d8cc595ed1b52144df489`.
- Targets: P07, P08.
- P07/P08 state is recreated in isolation; prior D/E/J ledgers are not imported.

## PRE — 3 rows

- `FIX-ID-P07` Place / REAL / `S02-P07-PLACE` / Quality `unknown`.
- `FIX-ID-P08` Place / REAL / `S02-P08-PLACE` / Quality `unknown`.
- `FIX-CONT-S02-P07-P08` Containment / REAL / `S02-P07-CONTAINS-P08` / `ref=FIX-ID-P07; relationship=contains; parent=FIX-ID-P07; child=FIX-ID-P08` / Quality `unknown`.

## POST — append one row

`FIX-RES-S02-P07-CLOSED` / Resolution Link / SYNTHETIC / `SYN-S02-CLOSE-P07` / `ref=FIX-ID-P07; lifecycle=closure; relationship=closure; resolution=FIX-ID-P07; historical_resolvable=true; valid_for_new_use=false; successor=none` / Quality `unknown`.

Do not close, withdraw, relocate or replace P08. Do not delete or inverse the containment row. Do not add relationship-currentness or lifecycle fields.
