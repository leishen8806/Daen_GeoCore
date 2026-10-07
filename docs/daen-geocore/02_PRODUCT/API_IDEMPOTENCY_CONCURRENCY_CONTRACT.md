# DAEN Geo Core — Phase 05D Idempotency and Concurrency Contract

All material public mutations require an opaque caller-originated MutationRequestRef. It is request identity only, not GeoID, resource identity, Domain identity or business identity.

Identical request identity plus identical semantic intent returns the same semantic result and created refs without duplicate history. Same request identity plus different intent is a request-identity conflict with no effect. Retention duration and uniqueness scope are not frozen; Phase 05E cannot finalize a mutation endpoint without defining both logically.

A material mutation must not silently overwrite newer conflicting state. Conceptual expected prior state/mutation basis is required for replacement, retirement, supersession and identity-history changes. ETag, version, revision, CAS, locks, transactions, storage and serialization remain deferred.

A single logical domain mutation becomes externally visible as one coherent semantic outcome, including assertion supersession, selection replacement, merge, split, closure and withdrawal. AP mutation atomicity is not defined because AP writes are deferred.

Every successful result may express affected refs, newly created refs, resulting history/relations, resulting Current Representation where applicable, attribution and MutationRequestRef. Ordinary destructive deletion of material Place, Source Assertion, Selection Record or resolution/history is not a public contract.
