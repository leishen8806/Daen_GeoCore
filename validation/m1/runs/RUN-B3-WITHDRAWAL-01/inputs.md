# RUN-B3-WITHDRAWAL-01 — Frozen Inputs

Bounded synthetic T1 validation for B3 Place-GeoID withdrawal resolvability.

## Lineage
- Final Gate Round-1 decision: `53659ee`
- Withdrawal target clarification: `1617c245e3c8677d6f453ad0cb809e536b0900b4`
- Pre-iteration baseline: `69f56525d250d61deca3b67495f2e47ba866794d`

All rows are SYNTHETIC with Quality `unknown`. No new Place identity is permitted. This is not a Scenario I rerun.

## PRE rows
1. `FIX-ID-P12` — Place — `locus=SYNTHETIC coarse-located Place; identity=FIX-ID-P12` — provenance `B3-T1-P12-PLACE`.
2. `FIX-ID-P12-SA-LOC` — Source Assertion — `ref=FIX-ID-P12; fact=address; purpose=locating-basis; value=SYNTHETIC COARSE LOCATION P12` — provenance `B3-T1-P12-LOC`.

## POST action
Append exactly one synthetic Resolution Link: `SYN-B3-T1-WITHDRAW-P12`, representing T1 withdrawal of the existing Place identity.

Expected absence: no new Place, Correction, Merge, Current DAEN Representation, replacement, deletion, successor, business semantics or Succession row.
