# DAEN Geo Core — Implementation Step 9: Source Assertion Create

`CreateSourceAssertion` is the transport-neutral core for the frozen Source Assertion Create mutation. It targets one exact `PlaceRef`, creates one immutable `SourceAssertionRecord`, and creates the initial `AssertionStandingHead`. It does not expose HTTP, select a current representation, or supersede any existing assertion.

## Contract and boundaries

The command carries idempotency identity, an exact PlaceRef, an open fact purpose, typed value, explicit-or-unknown scope, Source Provenance, Quality, and mutation provenance. It contains no `MutationBasisToken`; Source Assertion Create has no mandatory caller basis. The Extent-kind semantic gate remains outside this core until the body/value-kind contract is materialized; a transport or semantic adapter must reject deferred Extent-kind writes before invoking this operation.

The fixed internal operation key is `source_assertion.create`. The operation first checks committed replay. A valid existing binding returns the exact SourceAssertionRef before EvidenceStore access; a conflicting intent or malformed replay fails closed.

## Recovery and reservation

A request/reference recovery mapping is read before generating technical values. A valid mapping reuses its SourceAssertionRef, initial StateWitness, and recorded UTC time. A missing mapping creates exactly one candidate, one witness, and one Clock value, then records the mapping. Recovery mapping is not commit proof. The exact recovered SourceAssertionRef must pass the READY recovery gate and independent reservation evidence before the authoritative UoW opens. Evidence failure, conflict, or an unready gate fails closed.

## One authoritative UoW

The create decision uses immutable exact Place existence and generated-reference uniqueness; it does not invent a mutable owner read-set. The active mutation UoW rechecks committed idempotency and the exact PlaceRef, then immutably inserts the assertion and initial standing head. It creates one separate Mutation Audit record and one committed replay binding with `PUBLIC_REPLAY_HORIZON` (at least seven days). All four records commit together. No assertion history fact, SelectionRecord, slot head, or Current DAEN Representation is written.

`CommitAccepted` returns `APPLIED`; `CommitNotCommitted` returns explicit `NOT_COMMITTED`; `CommitUnknown` returns explicit `COMMIT_OUTCOME_UNKNOWN`. The operation never retries automatically or mints replacement technical values. A later retry uses committed replay or the same recovery mapping.

Source Provenance remains the assertion's originating provenance. Mutation Provenance remains the audit context; the two opaque payloads are stored separately. No HTTP route, Pydantic DTO, public reference format, production EvidenceStore, generic mutation pipeline, or schema migration is part of Step 9.
