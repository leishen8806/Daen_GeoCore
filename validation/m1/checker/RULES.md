# Disposable M1 Checker Rules

> VALIDATION TOOL ONLY.  
> NOT PRODUCTION CODE.  
> NOT AN API CONTRACT.  
> NOT A DATABASE SCHEMA.  
> NOT AN ARCHITECTURE PRECEDENT.  
> MUST NOT BE REUSED AS A PRODUCTION SERVICE OR LIBRARY.

The checker inspects structural evidence only. Its output is validation-tool evidence, not a Product Constitution or Domain Model judgment.

## A. Domain-related mechanical checks

| Rule | Structural check | Output |
|---|---|---|
| M1-M01 | A local subject label has incompatible `identity=` values | `DOMAIN STRUCTURAL FAILURE` |
| M1-M02 | A lifecycle event lacks a structural resolution or terminal status reference | `DOMAIN STRUCTURAL FAILURE` |
| M1-M03 | A ledger entry requiring attribution has no provenance reference | `DOMAIN STRUCTURAL FAILURE` |
| M1-M04 | A fact marked `current_representation=true` has no explicit Quality value; `unknown` is valid | `DOMAIN STRUCTURAL FAILURE` |
| M1-M05 | A supersedes reference is missing or does not resolve to an earlier ledger entry | `DOMAIN STRUCTURAL FAILURE` |
| M1-M06 | A frozen-concept reference is outside the approved Phase 03 vocabulary | `DOMAIN STRUCTURAL FAILURE` |
| M1-M07 | A `ref=` or structural subject reference points to no existing local subject | `DOMAIN STRUCTURAL FAILURE` |

The checker does not decide whether any identity, lifecycle, merge, split, access or correction judgment is semantically correct.

## B. Validation-medium integrity checks

| Rule | Structural check | Output |
|---|---|---|
| VM-I01 | A prior ledger snapshot has a missing or modified entry instead of a superseding entry | `VALIDATION MEDIUM FAILURE` |
| VM-I02 | Scenario headings A–J, pre-registered expected outcomes, or blank pre-execution result fields are missing/changed | `VALIDATION MEDIUM FAILURE` |

CSV is not physically immutable. VM-I01 checks the logical append-only convention only when a prior snapshot is supplied.

## C. Human-only / partially manual checks

The checker MUST report `MANUAL REVIEW REQUIRED` rather than decide:

- same Place;
- merge correctness or survivor choice;
- mis-conflation versus true division;
- Access Point physical correctness or duplication;
- business-semantic leakage;
- whether a new core concept is necessary;
- whether a Current DAEN Representation is better;
- whether provenance is meaningful or trustworthy;
- whether Quality is reasonable;
- GO / ITERATE / RETURN.

Manual Domain Model review has authority over checker output.
