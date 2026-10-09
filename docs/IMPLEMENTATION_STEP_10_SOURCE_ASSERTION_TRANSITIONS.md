# DAEN Geo Core — Implementation Step 10: Source Assertion Transitions

Step 10 implements two distinct transport-neutral operations:
`SupersedeSourceAssertion` and `CorrectSourceAssertion`.

Both require a caller `MutationBasisToken` containing an `AssertionOwner`
claim for the exact target with `OwnerPresent`. The target assertion supplies
the immutable PlaceRef and fact/purpose; callers provide only the replacement
value, scope, source provenance and quality. Scope equivalence is never
inferred. Extent-kind validation remains outside this core.

Committed replay is checked before basis validation or evidence access. A
fresh request reads the exact target and standing head, validates the mandatory
basis against the current owner state, and only then inspects retained
supersession history. A stale caller basis therefore returns `STALE_BASIS` even
when the target is already superseded; a fresh current basis returns
`TARGET_ALREADY_SUPERSEDED` without recovery or evidence side effects. Only
then does the operation obtain recovery material. A valid mapping preserves
the new SourceAssertionRef, all witnesses, history references and recorded time
without regeneration. Only the new SourceAssertionRef is reserved as a stable
reference.

The authoritative SERIALIZABLE transaction rechecks replay, target, head and
basis, captures a separate authoritative read-set, inserts the new assertion
and head, appends supersession history (and explicit correction history for
Correct), revalidates the read-set, and CAS-updates the old standing head.
Mutation audit and committed replay binding are written in the same unit of
work. Supersede and Correct use separate operation keys and replay result
kinds. Concurrent attempts are serialized by the authoritative read-set and
old-head CAS, permitting one standing transition winner and no second
supersession branch. Neither changes Current Representation or Selection
records.

Commit unknown is returned explicitly; a later retry uses committed replay or
the same recovery mapping. No HTTP route, generic mutation framework,
production EvidenceStore, schema migration or CorrectionRecordRef is part of
Step 10. Later work includes withdrawal, Selection and Place identity
mutations, production evidence adapters, HTTP API, and remaining
infrastructure closure.
