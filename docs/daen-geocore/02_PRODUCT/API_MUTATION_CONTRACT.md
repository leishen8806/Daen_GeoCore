# DAEN Geo Core — Phase 05D Mutation Contract

## Status
`PHASE 05D MUTATION AND ERROR CONTRACTS = HUMAN FROZEN`

## Shared rules
Material mutations are attributable, non-destructive, stable-reference preserving, exact-target, stale-safe, idempotent and logically coherent. Authorization and implementation mechanisms are not defined.

## Source Assertions
Create targets an exact PlaceRef and carries open fact/purpose, typed value, explicit-or-unknown scope, originating source Provenance and explicit Quality. It creates a new SourceAssertionRef and never implicitly supersedes. Same-subject/same-fact-purpose supersession is explicit, creates a new assertion, retains the old assertion and records history. Scope compatibility is not inferred; cross-subject supersession remains deferred. Correction is explicit intent layered on supersession and is not synonymous with every supersession.

## Withdrawal and selection
T2 targets SourceAssertionRef, retains the assertion, records withdrawal history and does not change Place identity or automatically affect Current Representation. No un-withdrawal contract. Add Selection and Replace Selection each create immutable SelectionRecordRef with PlaceRef, fact/purpose, scope, selected value, supporting assertion refs, attribution, Provenance and Quality. Supporting assertions belong to the same Place; T2-withdrawn assertions cannot support a new selection. Replace requires same Place, fact/purpose and explicit contract-recognized scope; unknown scope is not equivalence.

## Domain-specific Place mutations
Merge accepts exact participants and an explicitly supplied survivor, without choosing survivor policy or silently migrating assertions, AP relations, containment or provider references. Split explicitly distinguishes MIS_CONFLATION and TRUE_DIVISION; child identities are new and do not inherit the parent. Closure preserves resolvability without requiring successor or lifecycle enum. T1 withdrawal targets PlaceRef, preserves GeoID resolution, marks it not valid for new use, and requires no successor.

Resolution Link is created only by domain-specific operations; Succession is optional when a later identity exists. Generic relationship mutation and Containment write are deferred.

## Deferred writes
All public Access Point mutations, generic Place creation, direct Extent mutation, geometry writes, and business workflows are deferred. Split child creation is the only frozen domain-specific Place-creation outcome.
