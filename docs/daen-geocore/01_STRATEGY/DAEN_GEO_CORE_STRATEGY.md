# DAEN GEO CORE

## 1. Document Status

- Current phase: Documentation Cleanup
- Status: Baseline Draft
- Not final PRD
- Not final architecture
- Not investment decision

## 2. Project Identity

- Brand candidate: ដែន / DAEN / 域联 — `RECOMMENDED`
- Technology platform: DAEN Geo Core — `RECOMMENDED`
- Working place term: Place — `CONFIRMED`
- Working unique place identity term: GeoID — `CANDIDATE`

GeoID is a working term only. Its encoding, persistence, resolution and lifecycle are `TBD`.

## 3. Strategic Direction

DAEN Geo Core is being considered as a location infrastructure layer for Cambodia. The long-term expression Cambodia Location Network is a strategic direction candidate, not a committed coverage or operating promise.

The current working definition is:

> DAEN Geo Core is a location infrastructure layer for real-world places in Cambodia. It provides upper-layer systems with common place identity, address, coordinates, entrances, geographic areas, distance, route and location correction capabilities.

This definition is a cleaned working boundary. It does not define a product backlog, service-level commitment or technical implementation.

## 4. Core Platform

- DAEN is the brand and infrastructure umbrella — `RECOMMENDED`
- DAEN Geo Core is the core location technology platform — `RECOMMENDED`
- Cambodia Location Infrastructure is the strategic positioning candidate — `CANDIDATE`
- Cambodia Location Network is the long-term strategic expression candidate — `CANDIDATE`
- Connect Every Place. is the mission line candidate — `CANDIDATE`

The relationship is:

DAEN → Cambodia Location Infrastructure → DAEN Geo Core → location infrastructure capabilities

## 5. Capability Direction

The following names appear in the source material as capability candidates. They are not completed products or approved scope:

| Capability candidate | Working meaning | Status |
|---|---|---|
| DAEN ID | Place identity and reference | `CANDIDATE` |
| DAEN Places | Place and POI information | `CANDIDATE` |
| DAEN Access | Entrance and last-mile access point information | `CANDIDATE` |
| DAEN Route | Route capability | `CANDIDATE` |
| DAEN Mobility | Movement-related location capability | `CANDIDATE` |
| DAEN Logistics | Location capability for logistics workflows | `CANDIDATE` |
| DAEN API / Cloud | External location service access | `CANDIDATE` |

The specific users, data sources, quality rules, licensing, operations and acceptance criteria for each capability are `TBD`.

## 6. Product Boundary

### Geo Core is

- Location Infrastructure
- Geo Data Infrastructure
- Location Identity Infrastructure
- Place Data Layer
- Geo Capability Layer
- A location capability layer for upper-layer business systems

### Geo Core is not

- A consumer map application
- A consumer navigation application
- A social map
- A delivery business system
- A logistics dispatch system
- A ride-hailing platform
- A lending or financial decision system
- A business decision engine
- An AI organization or coordination platform
- A workflow system

Geo Core may provide location capabilities to these systems. It does not make their final business decisions.

Geo Core may answer where a place is, which place it is, its address or coordinates, where its entrance is, how far two places are apart, whether a place is inside an area, how to travel from A to B, or whether place data needs correction. Decisions such as loan approval, rider assignment, pricing, dispatch and business approval remain outside Geo Core.

## 7. M1 Principle

The first validation should select one clearly defined place-data or location workflow.

The validation must identify:

- Data source
- Place identity
- Data quality rules
- Output
- Acceptance owner
- A result that can be independently reviewed

The specific M1 business scenario, feature list, domain model, API and delivery date are `TBD`. This phase does not define them.

## 8. Historical Technical Direction

The source material contains the following technical directions. They are retained as historical recommendations, not final architecture decisions:

- Provider Adapter for replaceable external geography providers — `RECOMMENDED`
- PostgreSQL as a possible transactional data store — `RECOMMENDED`
- Modular monolith as an early delivery shape — `RECOMMENDED`
- Avoid complex microservices and Kubernetes during an early MVP — `RECOMMENDED`
- Do not build a nationwide owned basemap — `RECOMMENDED`
- Record data source, precision, licensing and update information — `RECOMMENDED`

Provider choice, database schema, deployment, API shape and integration details are `TBD`.

## 9. Known Unknowns

- M1 business scenario and acceptance result — `TBD`
- First customer and first payer — `TBD`
- Data provider and licensing — `TBD`
- GeoID definition and encoding — `TBD`
- Geo domain model — `TBD`
- API and integration contract — `TBD`
- Service-level expectations — `TBD`
- Data quality thresholds — `TBD`
- Location correction rules — `TBD`
- Coverage, update frequency and operating owner — `TBD`
- Brand, Khmer language, trademark, domain and social-handle verification — `TBD`

## 10. Decision Boundary

This document establishes a clean strategic baseline. It does not authorize domain model design, M1 PRD design, API design, database schema design, technical architecture, provider selection, integration implementation, backend development or frontend development.
