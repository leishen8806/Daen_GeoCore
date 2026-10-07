# DAEN Geo Core — Phase 05D Error Contract

Conceptual mutation failure classes are: wrong reference type/uninterpretable reference; unknown reference; incomplete or uninterpretable intent; invariant violation attempt; semantic precondition failure; stale basis/semantic conflict; unsupported/deferred operation; and MutationRequestRef conflict. HTTP and numeric codes are deferred.

`ALREADY HOLDS` is a successful semantic no-op when the desired outcome already exists; no new history is added and existing result refs are returned. An identical replay with the same MutationRequestRef returns the original mutation result and is distinct from ALREADY HOLDS.

A material mutation must not silently overwrite a conflicting newer material state. Replace, retire, supersede and identity-history changes require a conceptual expected prior state or mutation basis.

Semantic outcomes APPLIED, ALREADY_HOLDS and NOT_APPLIED are conceptual categories, not wire enums. No generic Operation resource is required.
