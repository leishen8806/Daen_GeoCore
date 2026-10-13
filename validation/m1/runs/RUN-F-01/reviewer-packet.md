# RUN-F-01 — Reviewer Packet

REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Frozen scope

- Input-freeze: 8d7ab92a515ad3bed899af35c15cb94227535f5e
- Scenario E acceptance baseline: 193a2f5614b48007eb4a832acbaf560ec12081c5
- Targets: P04, P14, P15
- Frozen action: correct a wrong address, coordinate or provider reference while retaining material history.
- Frozen expected outcome: wrong fact is superseded, attribution remains available and Place identity is not silently changed.

## Correction pairs

| Place | Fact | OLD | REVISED | Correction |
|---|---|---|---|---|
| FIX-ID-P04 | address | FIX-ID-P04-SA-ADDR-OLD = synthetic Building 41 | FIX-ID-P04-SA-ADDR-REVISED = synthetic Building 14 | FIX-CORR-F-P04 |
| FIX-ID-P14 | provider-reference | FIX-ID-P14-SA-PROVIDER-OLD = SYN-F-P14-PROVIDER-REF-WRONG | FIX-ID-P14-SA-PROVIDER-REVISED = SYN-F-P14-PROVIDER-REF-CORRECT | FIX-CORR-F-P14 |
| FIX-ID-P15 | coordinate | FIX-ID-P15-SA-COORD-OLD = 0.050000, 0.050000 | FIX-ID-P15-SA-COORD-REVISED = 0.051000, 0.049000 | FIX-CORR-F-P15 |

P15 initial triplet also includes the address SYNTHETIC ONLY — P15 Test Premises, Lot 15 and provider reference SYN-F-P15-PROVIDER-REF-0015.

## Review checks

1. Confirm all 8 PRE rows remain unchanged in POST.
2. Confirm 3 revised Source Assertions supersede the intended OLD rows.
3. Confirm 3 Correction rows reference the revised and OLD assertions correctly.
4. Confirm all source and correction-action provenance labels map to inputs.md and source-map.md.
5. Confirm P04/P14 Place context remains REAL and P15 context remains SYNTHETIC; all new assertion/action entries are SYNTHETIC.
6. Confirm Quality is explicit as unknown.
7. Confirm no Current DAEN Representation or separate Succession row exists.
8. Confirm Place identity set is unchanged.
9. Treat checker output as structural evidence only.

## Manual-only checks

Reference target types, OLD/REVISED semantic roles, meaningful provenance, Quality reasonableness, identity preservation and Correction semantic correctness remain reviewer judgments.

## Acceptance limits

- All correction facts are controlled synthetic fixture inputs.
- P04 real address/coordinate truth is not being corrected.
- P04 entrance/general-coordinate issue remains open.
- P14 C-name change is not reused.
- P15 coordinates are synthetic test values.
- Production correction authority remains TBD.
- No Current DAEN Representation behavior is tested.
- No general Succession taxonomy is defined.
- No overall M1 result is created.

## Decision state

The operator records evidence only. No semantic PASS, FAIL or INEXPRESSIBLE verdict is recorded.
