# DAEN Geo Core — Phase 05D Idempotency and Concurrency Contract

All material public mutations require an opaque caller-originated MutationRequestRef. It is request identity only, not GeoID, resource identity, Domain identity or business identity.

Identical request identity plus identical semantic intent returns the same semantic result and created refs without duplicate history. Same request identity plus different intent is a request-identity conflict with no effect. Logical uniqueness scope is requesting client identity + Idempotency-Key globally across all Phase 05 material mutation endpoints. Minimum guaranteed replay horizon is 7 days from first accepted request; implementations may retain longer.

A material mutation must not silently overwrite newer conflicting state. Conceptual expected prior state/mutation basis is required for replacement, retirement, supersession and identity-history changes. ETag, version, revision, CAS, locks, transactions, storage and serialization remain deferred.

A single logical domain mutation becomes externally visible as one coherent semantic outcome, including assertion supersession, selection replacement, merge, split, closure and withdrawal. AP mutation atomicity is not defined because AP writes are deferred.

Every successful result may express affected refs, newly created refs, resulting history/relations, resulting Current Representation where applicable, attribution and MutationRequestRef. Ordinary destructive deletion of material Place, Source Assertion, Selection Record or resolution/history is not a public contract.


## Transport and replay

Every material public mutation requires HTTP header `Idempotency-Key`, carrying MutationRequestRef semantics. It is request identity only, never GeoID, resource, Domain or business identity; no external standards dependency is claimed. Same client/key plus same intent replays the original result and refs without duplicate history. Same client/key plus different intent returns HTTP 409 with no effect. Outside the 7-day guarantee, replay memory is not assured; an identical Source Assertion create may then create a new assertion, visibly and non-destructively. Basis-protected mutations retain stale-state and ALREADY_HOLDS protection independently. Storage, encoding and expiry mechanisms remain deferred.
