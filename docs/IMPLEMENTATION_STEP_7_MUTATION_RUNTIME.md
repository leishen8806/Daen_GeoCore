# Step 7 Mutation Runtime Foundations

Step 7 provides provider-neutral correctness primitives only. No business mutation, production cryptography, reference generator, database adapter, migration, HTTP route, or generic mutation framework is included.

## Basis and read-set

`MutationBasisToken` is opaque. `MutationBasisClaims` contains caller-observed owner states and a `RecoveryIncarnation`; `AuthoritativeReadSet` is a separate type captured from the current active UoW. Basis validation checks a READY gate, exact incarnation, and exact present/absent owner states. Invalid tokens, recovery changes, and witness changes fail closed.

Owner locators are explicit for Place, Source Assertion, and Selection Slot. Owner readers only inspect whether a module-owned head exists and its exact witness. Commit-time revalidation reads those owners again through the same repository-bound UoW.

## Recovery and references

Reference reservation accepts caller-supplied typed candidates only after READY recovery state and durable reservation evidence report created or same. Gate failure, unavailable evidence, and conflicting evidence never produce prepared references. Reservation evidence prevents reuse; it is not Domain truth or commit proof.

Request/reference recovery mappings are separate evidence. Same client/request/intent/operation reuses the exact stored mapping; different intent conflicts. A mapping does not imply that the mutation committed.

## Committed idempotency

`CommittedIdempotencyStore` is a purpose-specific capability, not a repository. `CommittedMutationBinding` is the authority for committed replay and stores immutable typed references and replay metadata. The replay decider returns execute, exact replay, or conflict. MutationBasisToken is not part of the binding key or intent identity. No `IN_PROGRESS` semantic result exists.

The public replay horizon and CD-1 lifetime remain architectural requirements; Step 7 adds no expiry scheduler or persistence implementation.

## Boundaries and deferred work

Deterministic fakes and tests cover tampering, recovery-incarnation changes, present/absent transitions, read-set revalidation, fail-closed reference reservation, mapping reuse/conflict, and idempotency replay. Step 5 schema, the single production migration, Step 6 repository ownership, API routes, business operations, production crypto, and provider adapters remain unchanged or deferred.
