# DAEN Geo Core — Post-GO Amendment: CD-2 Split Child Locating Basis

## Status

`CD-2 SPLIT CHILD LOCATING-BASIS CONTRACT = HUMAN FROZEN`

`CD-2 — SPLIT CHILD LOCATING-BASIS CONTRACT GAP = RESOLVED`

## Governance and scope

This bounded post-GO amendment applies only to the existing Split actions: mis-conflation and true-division. It adds no endpoint, changes no route or identity outcome, and does not move the Phase 05 GO tag.

## H14 at child birth

Every new Place created by Split becomes externally visible only with at least one designated locating basis. This applies at birth/first visibility only and does not resolve H14 lifetime semantics.

Mis-conflation A→B requires A unchanged, new B, at least one new Source Assertion about B, at least one B locating basis and the split history. True division A→B,C requires A historical outcome, all children, at least one new child assertion and designated basis for each child, plus split history. Each child satisfies the rule independently; no primary child ordering is introduced.

## Child assertions and reassociation

Child bootstrap assertions are new immutable Source Assertions with child subject, normal fact/value/scope, Provenance and explicit Quality. Parent assertions remain on the parent; they are not migrated, reassociated or cross-subject superseded. Child assertions carry no supersession relation to parent assertions, though they may cite shared evidence/context.

The locating-basis designation is mutation/history context. Presence is enforced; adequacy, precision, address/coordinate requirements and confidence thresholds are not decided.

## Atomicity and idempotency

The complete Split outcome is logically atomic: parent outcome, all child identities, each child bootstrap assertion/designation and split relationships become visible coherently. If any child lacks the bootstrap rule, no partial child set becomes visible and the parent is not partially changed. No physical transaction shape is frozen.

Existing Idempotency-Key and MutationBasisToken semantics apply. Within the replay guarantee, identical replay returns the same child/assertion refs and relationships without duplicates. Outside the replay horizon, authoritative state and stale-basis protection prevent a second successful semantic Split. No new idempotency concept is created.

## Failure and deferred boundaries

Existing 400/422 taxonomy applies; this amendment does not refine that distinction. Extent/AP/Containment writes remain untouched and new Extent payloads remain gated. Misattributed parent evidence is not migrated or hidden. No automatic Current Representation is created.

## Unified Place-bootstrap rule

Every newly created DAEN Place identity becomes visible only with at least one designated locating basis. Covered paths are CD-1 internal provisioning and CD-2 Split child creation. This is not generic public Place creation.

## S1–S11

S1 birth basis required; S2 presence enforced, adequacy open; S3 child evidence uses new child assertions; S4 parent assertions never silently reassociated; S5 each true-division child independently satisfies; S6 no automatic Current Representation; S7 replay returns same refs and stale-state prevents duplicate after horizon; S8 endpoint surface unchanged; S9 Extent/AP/Containment TBDs untouched; S10 H14 lifetime open; S11 child assertions have no parent supersession.

## Reviewed coherence cases

Sixteen cases are supported. Case 16, later T2 withdrawal removing a child’s only locating assertion, is correctly deferred to H14 lifetime semantics. No CD-2 contract gap remains.
