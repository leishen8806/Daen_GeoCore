# RUN-E-01 Independent Review Export

This file preserves the supplied export of the completed independent review. It is not a new review and does not alter the raw operator evidence.

## Review anchors

- Evidence commit: `1388f7b33ac96352625b56ce0535c3cc740f2f6c`
- Input-freeze commit: `a966670b5026331c6399c2bed4c67660071223e3`
- D acceptance baseline: `45712b61f2811fe7cf71f086d5a7f38e79a2a287`
- Verdict: `PASS`
- Recommendation: `READY FOR HUMAN ACCEPTANCE OF SCENARIO E`

## Findings

### RUN-E-01:F1

The AP row carries `business_pickup_dropoff=false`. It is a negative validation marker and models no pickup, drop-off, rider or dispatch semantics, but it imports the excluded concept's name into an Access Point row. It must not be carried forward as a field.

Classification: `VALIDATION MEDIUM ISSUE`, Low

Blocking: No

### RUN-E-01:F2

The Source Assertion's subject label and its provenance label are the same string, `SYN-E-ACCESS-SHARED`. The AP row's `ref=` and its provenance also use it. It resolves unambiguously, but ledger subject and source label are conflated.

Classification: `VALIDATION MEDIUM ISSUE`, Low

Blocking: No

### RUN-E-01:F3

P08 is, per frozen corpus evidence, physically contained within P07. The shared relationship is supplied by the synthetic statement, which disclaims containment, proximity and coordinates, and no Containment row exists. For a container/contained pair, independence from containment rests on that statement and absent rows, not on a case where containment could not explain the relationship.

Classification: `EVIDENCE LIMITATION`, Low

Blocking: No

### RUN-E-01:F4

The historical discrepancy is wider than `inputs.md` names.

Besides `synthetic-case-plan.md` saying P05/P06 are used by E:

- `corpus-register.csv` lists P05/P06 for `D; E`;
- `corpus-register.csv` lists P07 without E;
- `corpus-evidence.md` lists P07 scenarios without E.

The frozen scenario sheet and runbook target P07 and govern.

Classification: `REPORTING / TRACEABILITY ISSUE`, Low

Blocking: No

### RUN-E-01:F5

`source-map.md` says the input-freeze commit is "recorded after creation" for `SYN-E-ACCESS-SHARED` and never names the SHA.

`operator-execution.md` and `reviewer-packet.md` identify:

`a966670b5026331c6399c2bed4c67660071223e3`

Classification: `REPORTING / TRACEABILITY ISSUE`, Low

Blocking: No

### RUN-E-01:F6

Forward-looking: P08 is the frozen target of Scenario G. E uses `FIX-ID-P08` only inside its own run ledger.

Any later interaction between an Access Point and a Place affected by Scenario G merge behavior remains untested.

No AP identity continuity between D and E is claimed.

Classification: `EVIDENCE LIMITATION`, Low, forward-looking

Blocking: No

## Carry-forward items

- D:F3 served-place encoding/manual validation remains applicable.
- D:F6 is addressed by E's execution of the P07 shared case.
- D:F5 / B:F4 regarding P04 observed-entrance versus Access Point remains open.
