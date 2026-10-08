# DAEN Geo Core — Post-GO Amendment: CD-1 Internal Place Provisioning

## Status

`CD-1 INTERNAL PLACE PROVISIONING CONTRACT = HUMAN FROZEN`

`CD-1 — INTERNAL PLACE PROVISIONING CONTRACT = RESOLVED`

## Governance

Authority is Constitution > Domain Model > Phase 05 frozen public contracts > this bounded Human-frozen internal amendment > Phase 06 architecture. The Phase 05 GO tag and public contracts remain unchanged.

## Internal-only boundary

This transport-neutral contract adds no public endpoint, no `POST /v1/places`, no external generic Place creation and no change to the 18 public endpoints.

## Identity and GeoID

Provisioning executes an already-made `NEW PLACE` decision. The input must attest that decision; the attestation is retained in mutation Provenance. Provisioning never decides same Place, duplicate, matching, confidence, provider mapping or whether a candidate deserves identity.

A successful request creates exactly one Place with a newly DAEN-issued GeoID. The caller cannot provide or choose it. Generation, encoding and allocation remain Phase 06 decisions.

## Bootstrap locating basis

One or more initial Source Assertions are required, with at least one explicitly designated as locating basis. The system enforces designation presence, not semantic adequacy. No coordinate, address, Current Representation, AP, Extent or Containment is required. The designation is internal provisioning/history context, not a new public Source Assertion field.

The outcome is logically atomic: Place, GeoID, initial SourceAssertionRefs, locating-basis designation, attribution and internal request binding become visible together.

## Initial facts and representation

Initial assertions use normal Source Assertion semantics: new Place subject, open fact/purpose, typed value, explicit-or-unknown scope, source Provenance, explicit Quality, immutable content and normal SourceAssertionRef. New Extent payload is forbidden/gated. No Current Representation is created automatically; selections remain separate.

## Request identity and bulk ingestion

Internal provisioning uses the MutationRequestRef semantic pattern without freezing public HTTP form. Same internal client + same request identity + same intent replays the same PlaceRef, assertions and result with no duplicate history. Same identity + different intent conflicts with no effect. The binding is durable and internally resolvable for the lifetime of the resulting Place identity; it is not Domain identity, public lookup or provider mapping. Bulk orchestration provides stable per-item identities.

Different requests are not semantically deduplicated and may create duplicate Places; later confirmed sameness uses existing Merge semantics.

Candidates: EXISTING uses existing PlaceRef and normal mutations; NEW uses internal provisioning; UNRESOLVED creates no identity. Provider records never automatically provision and provider references never become GeoID.

Batch may parallelize or partially succeed, but each Place provisioning outcome is atomic and attributable.

## Boundaries

AP creation/relations, Containment writes and Extent writes are unsupported here. Wrong assertions use existing supersede/correct/T2 withdrawal. Truly spurious Place withdrawal requires separately authorized decision; no automatic withdrawal or destructive delete. No public ProvisioningRecord is created.

Internal audit retains decision attestation, mutation attribution, assertion Provenance, resulting PlaceRef/GeoID, SourceAssertionRefs, locating-basis designation and request/result binding. Acknowledged or externally observable references are permanently bound and never reassigned; gaps are allowed.

## P1–P17 provisioning invariants

P1 already-made NEW PLACE decision; P2 DAEN-issued, never caller-supplied GeoID; P3 one accepted request creates exactly one Place; P4 visibility requires at least one designated locating basis; P5 normal Source Assertion semantics; P6 no automatic Current Representation; P7 same replay creates no duplicate; P8 different requests are not semantically deduplicated; P9 provider data never becomes identity; P10 existing candidates are not provisioned; P11 unresolved candidates are not provisioned; P12 attributable/non-destructive; P13 public surface unchanged; P14 AP/Containment/Extent write TBDs untouched; P15 batch preserves per-item outcomes; P16 request/result binding is durable for the Place lifetime and internally replayable, not public/provider mapping; P17 no caller-supplied GeoID, existing PlaceRef, AP, Containment, Extent or Selection.

## Reviewed coherence cases

1 NEW decision attestation; 2 exactly one Place; 3 caller cannot choose GeoID; 4 initial assertions present; 5 locating-basis designation present; 6 no semantic adequacy inference; 7 logical bootstrap atomicity; 8 normal assertion Provenance/Quality; 9 no automatic selection; 10 replay identity; 11 different request non-deduplication; 12 EXISTING path; 13 UNRESOLVED path; 14 provider boundary; 15 AP/Containment/Extent rejection; 16 batch partial success with per-item outcomes; 17 permanent acknowledged-reference binding; 18 no public endpoint or ProvisioningRecord.

## Open observations

`CD-2 — SPLIT CHILD LOCATING-BASIS CONTRACT GAP = OPEN`

`OBS-06-H14-LIFETIME = OPEN / NON-BLOCKING`

These are not resolved by CD-1.
