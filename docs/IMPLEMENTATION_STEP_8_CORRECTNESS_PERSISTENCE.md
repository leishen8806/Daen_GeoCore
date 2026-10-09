# DAEN Geo Core — Implementation Step 8

## Scope

Step 8 supplies correctness infrastructure only. It does not implement a business mutation, public API, EvidenceStore adapter, or provider integration.

## Reference candidates

`SecureReferenceCandidateGenerator` uses Python `secrets` with an explicit 16-byte (128-bit) entropy class. It generates opaque candidates for typed public references, internal history references, and `StateWitness`. Candidates are not issued or acknowledged by generation alone. The implementation text is not a public DAEN reference-format contract; consumers treat tokens as opaque and no parser is provided.

Issuance remains the later combination of candidate generation, request/reference recovery mapping, independent durable reservation evidence, and authoritative uniqueness. Evidence failure remains fail closed.

## Committed idempotency

`PostgresCommittedIdempotencyStore` is a purpose-specific store bound to the active `PostgresUnitOfWork` connection. It stores immutable bindings, ordered typed result references, and ordered opaque replay metadata. `PUBLIC_REPLAY_HORIZON` is retained as a vocabulary for a horizon of at least seven days; `PLACE_IDENTITY_LIFETIME` is retained for the lifetime of the resulting Place identity. No cleanup or expiration scheduler is implemented. The store never begins, commits, rolls back, updates, deletes, or lists arbitrary records.

The four Step 8 tables are isolated in a correctness metadata group and are created only by Alembic revision `0002_correctness_persistence`. Child rows have no cascade delete and result references have no foreign keys to Domain tables.

## Mutation audit

`MutationAuditRecord` and `MutationAuditStore` are separate from Source Provenance, EvidenceStore, committed replay bindings, and logs. `recorded_at` is supplied as an explicit UTC-aware application value; the database supplies no clock default. The PostgreSQL adapter appends once and distinguishes inserted, exact-existing, and conflicting-existing records.

## EvidenceStore boundary

`ReferenceReservationEvidence` and `RequestReferenceRecoveryMapping` are not persisted in PostgreSQL in Step 8. The production EvidenceStore backend remains deferred to a separately reviewed infrastructure decision.
