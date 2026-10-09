# Software Implementation Step 13 — Place Closure and T1 Withdrawal

Step 13 adds two transport-neutral, operation-specific application services:

- `ClosePlace` (`place.close`) appends `place.closed`.
- `WithdrawPlace` (`place.withdraw`) appends `place.withdrawn_from_new_use`.

Both commands target an exact `PlaceRef` and require a current `PlaceOwner`
`MutationBasisToken`. A committed binding is checked before any Place, basis,
history, recovery, clock, or generator work. Replays return the original
`APPLIED` or `ALREADY_HOLDS` result without revalidating the supplied basis.

Fresh work uses an authoritative transaction: exact Place and PlaceHead reads,
basis validation, operation-specific history inspection, a one-fact immutable
history append, read-set revalidation, Place-head compare-and-swap, Mutation
Audit, and committed binding. The history/head/audit/binding writes share one
commit. `ALREADY_HOLDS` writes only audit and binding; it does not generate a
fact or change the head witness.

Closure and T1 withdrawal are separate facts and may coexist on one retained
Place. Neither operation creates a successor, Resolution Link, new PlaceRef,
lifecycle enum, Source Assertion mutation, Selection mutation, EvidenceStore
record, HTTP endpoint, or schema migration.

The implementation is intentionally transport-neutral. PostgreSQL coverage
uses the existing Step 6–12 persistence ports and the existing two migrations.
