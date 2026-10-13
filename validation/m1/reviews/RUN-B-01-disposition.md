# RUN-B-01 — Scenario B Disposition

## Acceptance

RUN-B-01 is accepted as `PASS` for the frozen Scenario B outcome only.

Accepted scope:

- Assertions remain attributable within the stated evidence limits.
- Pre-run material history is preserved.
- Conflicting claims did not silently create or merge accepted Places.
- Quality is explicitly recorded as `unknown`; informative Quality was not demonstrated.
- P17 remains unresolved synthetic Source Assertion evidence.

Not established:

- Real-source conflict prevalence or automated detection.
- Conflict resolution, informative Quality or source ranking.
- Exact original-webpage attribution.
- Independent inspection of unavailable P04 photographs.
- Current DAEN Representation selection or H20 scoped-selection behavior.
- Correction, Merge, Split, Access Point model validation or provider behavior.
- Scenarios C–J or overall M1 GO.

No Scenario B rerun is authorized or needed. No Domain Model amendment is authorized by this disposition.

## Finding dispositions

The following preserves the supplied review wording and classifications. Project dispositions are additive and do not repair the frozen evidence.

### RUN-B-01:F1

**Review finding:** P03 appears twice as an identical assertion. The repeat must not be read as multiple or corroborating sources.

**Classification:** `EVIDENCE LIMITATION` (low), non-blocking.

**Project disposition:** Retain the raw evidence. Do not treat the repeated row as independent corroboration.

### RUN-B-01:F2

**Review finding:** Traceability slip in `inputs.md`: the crosswalk conflates Domain Model §10 and DM-10.

**Classification:** `REPORTING / TRACEABILITY ISSUE` (low), non-blocking.

**Project disposition / erratum:** Domain Model §10 is the Source Assertion Model. Domain Model §27 invariant 10 / DM-10 is the pickup/drop-off boundary. M1-B10 is explicit Quality. The frozen `inputs.md` and scenario sheet remain unchanged; this is a citation correction, not a new product rule.

### RUN-B-01:F3

**Review finding:** `P04-FIELD-AP01` covers the public address, public reference coordinate and observed coordinate within one composite record.

**Classification:** `EVIDENCE LIMITATION` (low), non-blocking.

**Project disposition:** Accept composite-record-level attribution for P04. Do not claim independent original-source attribution for each fact.

### RUN-B-01:F4

**Review finding:** `role=observed-entrance` is a coordinate assertion on the Place; the relationship to a future Access Point in Scenario D remains undecided.

**Classification:** `EVIDENCE LIMITATION`, forward-looking, non-blocking.

**Project disposition:** Carry forward to the Scenario D precheck. Frozen D targets remain P05, P06 and P07. This does not authorize adding P04, creating an Access Point or collecting new field evidence. D preparation must determine how approved target-scope coordinate assertions and Access Point evidence relate.

### RUN-B-01:F5

**Review finding:** Free-text fixture vocabulary has no frozen meaning; unresolved status is established by absence of resolution, selection or supersession rows.

**Classification:** `VALIDATION MEDIUM ISSUE` (low), non-blocking.

**Project disposition:** Retain free-text markers as validation notation only. They are not domain states, API fields or production semantics.

### RUN-B-01:F6

**Review finding:** L1/L2 disjointness is in `inputs.md`, not the ledger alone.

**Classification:** `EVIDENCE LIMITATION` (low), non-blocking.

**Project disposition:** Preserve `inputs.md` and the ledger together as the P17 evidence package. Do not claim the ledger alone contains the complete fixture background.

### RUN-B-01:F7

**Review finding:** Quality is `unknown` on every row, including conflicting P17 rows.

**Classification:** `EVIDENCE LIMITATION` (low), non-blocking.

**Project disposition:** Explicit `unknown` Quality is accepted. Informative Quality and quality-driven decisions remain untested. No scale or marker is added to historical rows.

## Bookkeeping erratum

An independent CSV parse of the committed B ledger confirms:

- 1 header row;
- 12 data records;
- 3 Place records;
- 9 Source Assertion records.

The review export's “13 rows” wording includes the header and must not be interpreted as 13 attributed data records. This is separate project bookkeeping and does not alter the exported review or renumber F1–F7.

## Decision boundary

This record accepts only the scoped Scenario B outcome. Overall M1 remains `NOT MADE`.
