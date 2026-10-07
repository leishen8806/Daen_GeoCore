# DAEN Geo Core — Phase 05 API Definition Entry Gate

## Status

`AUTHORIZED`

## Entry authority

- M1 Final Gate Round 2 = GO
- Human Final Decision = GO
- Phase 04 M1 = COMPLETE

## Phase 05 purpose

Define external/internal API contracts necessary to expose the validated Geo Core model without silently resolving deferred domain policy.

## Frozen API-design inputs

Place / GeoID identity boundary; Source Assertion; Current DAEN Representation; Selected Coordinate; Resolution Link; Access Point; Extent; Correction; Succession; minimal Containment; Provenance; Quality; Merge / Split semantics; Closure / Withdrawal T1/T2 target scope; non-destructive history; business-boundary exclusions.

## API Definition MUST NOT yet assume

Final GeoID encoding; final database schema; source ranking; Quality scoring algorithm; merge survivor algorithm; lifecycle enum; relationship-currentness model; temporal/as-of contract; provider selection; business entities; route object; Area model; production resolver implementation.

## Contract-first rule

Begin from resources/domain nouns; stable identifiers/references; read contracts; resolution behavior; mutation contracts; Provenance/Quality exposure; errors/ambiguity representation; lifecycle boundaries; versioning/idempotency; only then endpoint layout. Do not begin with REST URL naming.

## Required Phase 05 first deliverables

1. API Scope & Non-Scope
2. Resource Model
3. Identifier / Reference Contract
4. Place Resolution Contract
5. Source Assertion Contract
6. Current Representation Contract
7. Access Point Contract
8. Extent Contract
9. Correction Contract
10. Merge / Split / Withdrawal Resolution Contract
11. Containment Contract
12. Provenance / Quality Contract
13. Error / Ambiguity Model
14. Mutation / Idempotency Contract
15. API Invariants
16. Endpoint mapping LAST

## Entry gate

`PHASE 05 API DEFINITION MAY BEGIN`

No architecture or implementation is authorized by this document.
