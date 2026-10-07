# DAEN Geo Core — Phase 05D Error Contract

Conceptual mutation failure classes are: wrong reference type/uninterpretable reference; unknown reference; incomplete or uninterpretable intent; invariant violation attempt; semantic precondition failure; stale basis/semantic conflict; unsupported/deferred operation; and MutationRequestRef conflict. HTTP status-category mapping is frozen below; error-body schema remains deferred.

`ALREADY HOLDS` is a successful semantic no-op when the desired outcome already exists; no new history is added and existing result refs are returned. An identical replay with the same MutationRequestRef returns the original mutation result and is distinct from ALREADY HOLDS.

A material mutation must not silently overwrite a conflicting newer material state. Replace, retire, supersede and identity-history changes require a conceptual expected prior state or mutation basis.

Semantic outcomes APPLIED, ALREADY_HOLDS and NOT_APPLIED are conceptual categories, not wire enums. No generic Operation resource is required.


## HTTP status-category mapping

### Success

- `200 OK`: applied action with no new addressable resource, `ALREADY_HOLDS`, recognized historical Place reads and normal exact reads.
- `201 Created`: mutation creates one or more new addressable resources.
- Identical Idempotency-Key replay returns the original status and semantic result.

### Request and semantic failures

- `400 Bad Request`: structurally uninterpretable/incomplete request or detectable reference-type mismatch.
- `404 Not Found`: unknown exact path resource or unmapped route. The eventual error body must distinguish unknown-resource-reference from route-not-found.
- `405 Method Not Allowed`: unsupported method on a mapped route.
- `409 Conflict`: stale basis/newer state or MutationRequestRef/Idempotency-Key reuse for different intent. These conflict classes remain distinguishable in the eventual body.
- `422 Unprocessable Content`: understood mutation violating an invariant/precondition, unknown semantic body reference, or correctly mapped deferred capability such as an Extent-kind write.

No 3xx identity redirects, no 300 for multiple split successors, no 410 merely for historical/closed/withdrawn identity, and no 501 for deferred capabilities. Restricted details do not become 404/410 merely because details are unavailable; 403 and privacy mechanics remain deferred.

Conceptual outcomes remain APPLIED, ALREADY_HOLDS and NOT_APPLIED; they are not required wire enums.
