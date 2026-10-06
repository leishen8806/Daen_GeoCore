# M1 Validation Medium

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

M1 is **Internal Geo Core Validation**. This directory supports validation only. It is not market validation, production tooling or reusable architecture.

Fixture layouts MUST NOT be reused as API or database designs. Local fixture labels MUST NOT imply GeoID format. The state ledger is logically append-only: old entries are never edited or deleted during a valid run. Execution errors are handled by void plus rerun. Domain Model judgments remain manual.

No M1 scenario has been executed in this setup step.

## Files

- `scenario-sheet.md` — frozen scenarios with blank result fields
- `corpus-register.csv` — 20 opaque local corpus slots
- `state-ledger.csv` — generic append-only validation ledger header
- `execution-record.md` — blank run record
- `friction-log.md` — blank manual friction log
- `result-summary.md` — blank final report structure
- `checker/RULES.md` — proposed mechanical and manual check boundaries
- `checker/known-bad/` — non-executable known-bad specifications

The future checker is disposable and its runtime remains TBD.
