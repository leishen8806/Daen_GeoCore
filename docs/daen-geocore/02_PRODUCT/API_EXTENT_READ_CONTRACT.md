# DAEN Geo Core — Phase 05C Extent Read Contract

Extent is a read-only spatial fact/value, not a top-level resource in 05C. No ExtentRef, independent GeoID/Place identity, bare-Extent history, direct bare-Extent supersession or write contract is defined. A future independent opaque reference remains possible.

Extent appears through a Source Assertion value or Current Representation selected value. It indicates spatial extent; geometry, CRS, precision, topology and ring rules remain deferred. No closed role enum exists; an optional/open role may be carried through surrounding fact/purpose/scope. Missing role is unknown, not a default footprint/property/campus role.

Asserted Extent changes use Source Assertion supersession; selected Extent changes use Selection Record supersession. Bare Extent versioning is not promised. Overlap alone does not imply same Place, containment, conflict, merge or a new Domain relationship.

Extent inherits Provenance through its host assertion/selection and explicit Quality, with `unknown` valid.
