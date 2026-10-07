# RUN-H-01 — Frozen Split Inputs

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Authority and targets

- Run: RUN-H-01
- H target erratum: 6b572bc5ba03f275d25a21f727515128326a7d73
- Historical H targets: P10, P11
- Effective H targets: P17, P18
- Frozen H action and expected outcome remain those in the original scenario sheet.
- Two isolated subcases: misconflation (P17) and true-division (P18).

The initial corpus remains 20 Places. RUN-H-01 creates exactly three new local synthetic result identities, reaching the maximum conceptual count of 23. These are not P21/P22/P23 corpus registrations or production GeoID formats.

## Subcase M — P17 mis-conflation

All entries are SYNTHETIC with Quality unknown. Human-approved fixture decision: FIX-ID-P17 legitimately belongs to Locus A; Locus B receives new identity FIX-ID-H-P17-B. This is fixture-specific and is not a general first/oldest/lower-ID rule.

### PRE rows

| Subject | Provenance | Fact | Purpose | Value | Ref |
|---|---|---|---|---|---|
| FIX-ID-P17 | H-PLACE-P17 | Place | locus | SYNTHETIC P17 Locus A | identity=FIX-ID-P17 |
| FIX-ID-P17-SA-L1 | SYN-H-P17-L1 | address | place-address | SYNTHETIC ONLY — P17 Locus A | FIX-ID-P17 |
| FIX-ID-P17-SA-L2-OLD | SYN-H-P17-L2-OLD | address | place-address | SYNTHETIC ONLY — P17 Locus B | FIX-ID-P17 |

The Locus B assertion is intentionally attached to the identity belonging to Locus A. PRE count is 3. No Resolution Link or Succession exists.

### POST rows

Append:

- Place FIX-ID-H-P17-B, provenance SYN-H-P17-B-PLACE, locus SYNTHETIC P17 Locus B, identity FIX-ID-H-P17-B.
- Source Assertion FIX-ID-H-P17-B-SA-L2, provenance SYN-H-P17-L2-NEW, address/place-address, value SYNTHETIC ONLY — P17 Locus B, ref FIX-ID-H-P17-B, supersedes RUN-H-01-M:PRE-P17-SA-L2-OLD.
- Resolution Link FIX-RES-H-MIS-P17-B, provenance SYN-H-RES-P17, relationship=mis-conflation-separation, original_identity=FIX-ID-P17, original_locus=P17-Locus-A, separated_identity=FIX-ID-H-P17-B, separated_locus=P17-Locus-B, original_identity_continues=true, new_identity_created=true, history_preserved=true, ref=FIX-ID-P17.

No Succession row is created because FIX-ID-P17 continues to represent Locus A.

## Subcase T — P18 true division

All entries are SYNTHETIC with Quality unknown. Human-approved fixture decision: FIX-ID-P18 is the historical pre-division identity; children FIX-ID-H-P18-A and FIX-ID-H-P18-B are new identities; neither child inherits FIX-ID-P18; the historical identity remains resolvable.

### Division premise

Provenance: SYN-H-P18-DIVISION-PREMISE. Quality: unknown.

For RUN-H-01 true-division testing, the single historical P18 locus later genuinely divides into two resulting Places, Child A and Child B. The historical identity FIX-ID-P18 must not be inherited by either child. This is a controlled synthetic split premise, not a general split-detection algorithm.

### PRE rows

| Subject | Provenance | Fact | Purpose | Value | Ref |
|---|---|---|---|---|---|
| FIX-ID-P18 | H-PLACE-P18 | Place | locus | SYNTHETIC P18 Historical Unified Premises | identity=FIX-ID-P18 |
| FIX-ID-P18-SA-HIST | SYN-H-P18-HIST | address | place-address | SYNTHETIC ONLY — P18 Historical Unified Premises | FIX-ID-P18 |

PRE count is 2. No child, Resolution Link or Succession exists.

### POST rows

Append child A Place and Source Assertion, child B Place and Source Assertion, two Resolution Links and two Succession rows:

- FIX-ID-H-P18-A / SYN-H-P18-A-PLACE / SYNTHETIC P18 Child A; assertion FIX-ID-H-P18-A-SA / SYN-H-P18-A / SYNTHETIC ONLY — P18 Child A.
- FIX-ID-H-P18-B / SYN-H-P18-B-PLACE / SYNTHETIC P18 Child B; assertion FIX-ID-H-P18-B-SA / SYN-H-P18-B / SYNTHETIC ONLY — P18 Child B.
- FIX-RES-H-DIV-P18-A / SYN-H-RES-P18-A: historical_identity=FIX-ID-P18, child_identity=FIX-ID-H-P18-A, resolution_from=FIX-ID-P18, resolution_to=FIX-ID-H-P18-A, historical_resolvable=true, child_inherits_parent_identity=false, split_group=RUN-H-01-P18-DIVISION, result_count=2, ref=FIX-ID-P18.
- FIX-RES-H-DIV-P18-B / SYN-H-RES-P18-B: symmetric for child B, ref=FIX-ID-P18.
- FIX-SUCC-H-DIV-P18-A / SYN-H-SUCC-P18-A: predecessor=FIX-ID-P18, successor=FIX-ID-H-P18-A, relationship=true-division, history_preserved=true, ref=FIX-RES-H-DIV-P18-A.
- FIX-SUCC-H-DIV-P18-B / SYN-H-SUCC-P18-B: predecessor=FIX-ID-P18, successor=FIX-ID-H-P18-B, relationship=true-division, history_preserved=true, ref=FIX-RES-H-DIV-P18-B.

POST count is 10. The original parent Place row is unchanged.

## Isolation, review and limits

Mis-conflation and true division are isolated alternatives and are never concatenated into one ledger. P17 prior RUN-B evidence and P18 future J scope are not imported. Review must verify no silent identity copying, distinct result handles, retained history, historical resolvability and correct relationship directions.

All H loci and events are synthetic. No real-world split, general split-detection algorithm, production GeoID-generation policy, production lifecycle/status schema or overall M1 result is created. Resolution Link and Succession encodings are validation notation.
