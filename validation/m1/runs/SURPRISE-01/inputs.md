# SURPRISE-01 — Frozen Extent Overlap Fixture

> REVIEWER-SELECTED SURPRISE CASE — FROZEN BY HUMAN DECISION BEFORE OPERATOR EXECUTION.

- Baseline: `75b3769264e8e35eec1d8cc595ed1b52144df489`.
- Targets: P05, P06.
- All rows SYNTHETIC; Quality `unknown`.
- Geometry strings are validation notation only.

## PRE — 4 rows

- `FIX-ID-P05` Place; `ref` not required; identity P05.
- `FIX-EXT-S01-P05-V1` Extent; `ref=FIX-ID-P05; geometry=VALIDATION_RECT_0_0_4_4`.
- `FIX-ID-P06` Place; identity P06.
- `FIX-EXT-S01-P06-V1` Extent; `ref=FIX-ID-P06; geometry=VALIDATION_RECT_6_0_10_4`.

## POST — append one row

`FIX-EXT-S01-P05-V2` / Extent / `SYN-S01-P05-EXT-V2` / `ref=FIX-ID-P05; geometry=VALIDATION_RECT_0_0_8_4` / supersedes `RUN-SURPRISE-01:PRE-P05-EXT-V1`.

No new Place, merge, Resolution Link, Containment, same-Place relation or Area.
