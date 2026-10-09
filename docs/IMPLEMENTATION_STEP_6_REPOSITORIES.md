# Step 6 Repository Adapters

Step 6 adds provider-neutral, module-owned persistence ports and PostgreSQL Core adapters over the frozen Step 5 schema.

## Allowed persistence surface

Production code exposes exactly three repository capabilities: `IdentityRepository`, `AssertionsRepository`, and `RepresentationRepository`. There is no generic CRUD repository and no arbitrary-object save, update, delete, or list-all operation.

## Material records

Ports exchange frozen typed records with opaque encoded payloads, explicit or unknown scope and quality, typed references, history references, state witnesses, found/absent reads, and explicit insert/CAS dispositions. External provider data remains opaque.

## Ownership and transactions

Each adapter owns only its three module tables. Adapters do not query across modules, validate other modules, commit, rollback, retry, or expose SQL rows. A `PostgresUnitOfWork` binds all three adapters to one connection; callers explicitly commit or rollback.

Immutable inserts distinguish `INSERTED`, `ALREADY_PRESENT_SAME`, and `CONFLICTING_EXISTING`. Head creation uses the same rule. Head changes use one conditional SQL `UPDATE` with the expected witness (and expected selection reference for representation), returning `APPLIED` or `PRECONDITION_NOT_MET`.

Step 6 does not change the Step 5 schema and adds no migration. Business mutations, idempotency, API routes, provider integrations, and evidence production remain deferred.
