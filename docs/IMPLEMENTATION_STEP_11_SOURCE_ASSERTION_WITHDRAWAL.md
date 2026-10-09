# DAEN Geo Core — Implementation Step 11: Source Assertion Withdrawal

Step 11 implements the transport-neutral T2 operation
`WithdrawSourceAssertion` with operation key
`source_assertion.withdraw`.

T2 targets one exact `SourceAssertionRef`, retains the original assertion,
and appends the open history fact `source_assertion.withdrawn`. It changes the
assertion standing witness through server-side authoritative read-set capture,
revalidation, and compare-and-swap. It does not withdraw Place identity, alter
Current Representation, create Resolution Links, or provide an un-withdrawal
operation.

The command contains only the idempotency key, intent fingerprint, exact
target, and mutation provenance. T2 has no mandatory `MutationBasisToken`,
does not use EvidenceStore, does not create a public stable reference, and
does not use request/reference recovery mapping or stable-reference
reservation. Internal history references, witnesses, and timestamps are
generated only after the authoritative transaction confirms that the target is
present, has a standing head, and is not already withdrawn.

Committed replay is checked before mutable target state, recovery-gate,
history, generator, or clock work. A committed APPLIED result replays as
`REPLAY` with original semantic outcome `APPLIED`. A new request against a
withdrawn target returns `ALREADY_HOLDS`, writes only Mutation Audit and a
committed binding, and leaves history and the standing witness unchanged. An
identical retry then returns `REPLAY` with original semantic outcome
`ALREADY_HOLDS`.

The APPLIED path keeps history, standing-head CAS, Mutation Audit, and the
committed binding in one SERIALIZABLE unit of work. Unknown commit outcome is
reported without hidden retry; a later retry first checks the committed
binding, and if absent re-evaluates the current target state. T2/T2 and
T2/Supersede or T2/Correct races are decided by the authoritative read-set and
standing-head CAS, allowing at most one transition from a shared original
witness and no duplicate withdrawal history.

No HTTP route, schema migration, generic lifecycle enum, generic mutation
framework, Selection mutation, Place mutation, or provider-specific adapter is
part of Step 11. Later work includes Place identity mutations, Selection
mutations, production evidence/provider integration, HTTP API, and remaining
infrastructure closure.
