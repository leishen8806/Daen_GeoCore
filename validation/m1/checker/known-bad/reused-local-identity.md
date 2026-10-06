# Known-Bad: Reused Local Identity

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

- **Defect injected:** The same local subject label is reused for two inconsistent Places without an explicit continuity basis.
- **Mechanical rule expected to detect it:** M-01 inconsistent local identity reuse.
- **Expected checker result:** Error: inconsistent local identity reuse.
