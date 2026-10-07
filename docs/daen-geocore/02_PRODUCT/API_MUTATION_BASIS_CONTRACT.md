# DAEN Geo Core — MutationBasisToken Contract

`MutationBasisToken` is an opaque concurrency/precondition indicator representing the relevant material state observed by a read. It is not GeoID, a stable resource reference, Domain identity or MutationRequestRef. It may change whenever the relevant state changes. Transport and encoding remain deferred.

Relevant reads must be able to expose a basis where required. Basis-required mutations are assertion supersede, assertion correct, selection add, selection replace, merge, both split forms, closure and T1 withdrawal. Source Assertion create has no mandatory basis; T2 withdrawal has no mandatory basis in Phase 05.

Add Selection basis represents that no current selection exists for the exact Place + fact/purpose + contract-recognized scope. If a selection now exists, the operation is stale/conflicting and is not applied. Add Selection must not create a second current selection for the same exact scope.

A material mutation must not silently overwrite newer conflicting state. ETag, version, revision, CAS, locking and transaction mechanisms are not defined.
