# DAEN Geo Core Product Constitution

Status: `BASELINE CANDIDATE`

Phase: `Phase 02 — Product Definition`

Scope: `Product identity, product boundary and product principles only`

Not included:

- Domain Model
- M1 PRD
- API
- Architecture
- Provider selection
- Implementation

本文档是 DAEN Geo Core 后续产品、数据、API 与技术架构设计的最高产品边界约束。后续设计若与本文冲突，应优先修改后续设计，除非 Product Constitution 本身经过正式变更。

本文使用以下决策状态：

- `CONFIRMED`：当前项目已冻结的工作定义或边界。
- `RECOMMENDED`：明确推荐，但仍需后续正式批准或验证。
- `CANDIDATE`：候选方向，不构成当前承诺。
- `TBD`：资料不足，留待后续阶段决策。

规范词含义：`MUST` 表示不可违反；`MUST NOT` 表示明确禁止；`SHOULD` 表示默认遵守，偏离时需要说明原因；`MAY` 表示可选。

## 1. DAEN Identity

### 1.1 Brand and platform hierarchy

- `DAEN` is the project working brand and the location-infrastructure umbrella — `CONFIRMED`.
- `ដែន / DAEN / 域联` is the working brand expression — `RECOMMENDED`; Khmer language and trademark verification remain `TBD`.
- `DAEN Geo Core` is the core location-infrastructure platform under DAEN — `CONFIRMED`.
- `Cambodia Location Infrastructure` is the current positioning — `RECOMMENDED`.
- `Cambodia Location Network` is a long-term expression candidate — `CANDIDATE`.
- `Connect Every Place.` is a mission-line candidate — `CANDIDATE`.

The hierarchy is:

```text
DAEN
│
├── Geo Core
│   └── core location infrastructure
│
└── Future DAEN products and capabilities
    └── only if independently approved
```

DAEN MAY become broader than Geo Core. DAEN expansion MUST NOT automatically expand Geo Core scope.

This document does not decide trademark registration, domain availability or visual identity details. Those remain in Brand Strategy.

## 2. Geo Core Definition

### 2.1 Long definition

DAEN Geo Core is DAEN's core location-infrastructure platform. It establishes stable digital identity and standardized location expression for real-world places, and provides upper-layer systems with common place, address, coordinate, access-point, spatial-boundary, distance, route and location-correction capabilities.

Geo Core manages geographic facts and reusable location capabilities. It does not make final business decisions for upper-layer systems.

### 2.2 Short internal definition

`Geo Core = Location Identity + Location Facts + Location Capabilities` — `RECOMMENDED`.

### 2.3 Canonical representation

Geo Core maintains the canonical DAEN representation of known location facts. It does not claim perfect knowledge of physical reality. Location data MAY be stale, incomplete, conflicting, uncertain or wrong; the product must preserve the ability to express source, quality and correction state in later phases.

## 3. Why Geo Core Exists

The following is product rationale, not market validation — `RECOMMENDED`.

Real-world places can have multiple names, address expressions, external references, coordinate quality levels and access points. A map center may not match the practical access point. Places can move, close, be duplicated or require correction. Multiple systems may otherwise store the same place independently, while an external reference may change when a provider changes.

Geo Core exists to establish a stable, referable, traceable and correctable location-facts layer. Whether a real consumer will adopt or pay for a capability, and which real consumer workflow should be validated first, are external validation questions. They MUST NOT be inferred from M1 Internal Validation and MUST be validated through a later Consumer Validation phase.

M1 Internal Validation provides evidence only about Geo Core model coherence and operability; it MUST NOT be treated as evidence of customer demand, adoption, willingness to pay or real-workflow fit.

## 4. Primary Consumers

Geo Core serves consumer types rather than fixing a single commercial customer profile.

### 4.1 Internal business systems

Examples include OA, Delivery, Logistics, Mobility, FinTech, CRM, ERP and asset or facility systems. These are examples of possible consumers, not confirmed customers or scope.

### 4.2 Developers and internal services

Future internal services MAY consume Geo Core through API, SDK or internal service contracts. The exact contract is `TBD — Deferred to later phase`.

### 4.3 Data operations

Data operations MAY maintain place review, correction, access-point review and external-reference conflict review. These are role types only; screens, workflows and permissions are `TBD — Deferred to later phase`.

## 5. Core Capability Categories

This section freezes capability categories only. It does not define fields, tables, endpoints or implementation.

### 5.1 Location Identity

A Place MUST have the capability to be referred to by a stable DAEN-controlled identity. `GeoID` is the current working term — `CANDIDATE`.

External provider IDs, coordinates, addresses, names and business IDs MUST NOT serve as the canonical Geo Core identity.

GeoID encoding, generation and hierarchy remain `TBD — Deferred to Phase 06 Architecture`. Resolution and identity-continuity semantics are governed by the rules below and the approved Phase 03 Domain Model.

Identity continuity is frozen as intent:

- An identity MUST NOT be reassigned to a different real-world Place.
- Historical references MUST remain resolvable after closure, merge, split and withdrawal.
- A merge MUST preserve resolvability of historical identities and identify the survivor when applicable.
- A split MUST preserve resolvability of the historical identity and, when applicable, identify the resulting Place references.
- Withdrawal MUST remain resolvable as withdrawn or historical.
- Resolvable does not mean active, current, preferred or valid for new operational use.
- Authorized legal, privacy or security removal MAY restrict or remove underlying data through a later controlled process, but MUST NOT make the identifier reusable for another Place.
- The exact meaning of “the same Place”, relocation, rebuilding and reopening remain `TBD — Deferred to Phase 03 Domain Model`.

Other geographic objects MAY gain independent identities later. This document does not require every geographic object to share one identity system.

### 5.2 Place

Place is a referable real-world location whose identity and location facts may be reused independently of one single business workflow — `RECOMMENDED`.

Exact Place taxonomy and identity boundaries are `TBD — Deferred to Phase 03 Domain Model`.

### 5.3 Address

Address is a location expression and standardization capability. Administrative-area structure and normalization rules are `TBD — Deferred to Phase 03 Domain Model`.

### 5.4 Coordinate

Coordinate is a location fact with quality and source context. `Coordinate ≠ Place Identity`.

### 5.5 Access Point

Access Point is a real-world point used to access a Place. A Place representative coordinate MUST NOT be assumed to equal an Access Point.

Access Point MAY later distinguish pedestrian, vehicle, loading, service, parking and emergency access semantics. The exact taxonomy is `TBD — Deferred to Phase 03 Domain Model`.

Business-purpose terms such as pickup point, drop-off point and rider waiting point are not Geo Core concepts. They belong to the consuming business system.

### 5.6 Boundary and Geofence

Boundary or geofence expresses a spatial extent. Geo Core MAY answer whether a point is inside a spatial extent. The resulting attendance, eligibility, pricing or operational decision belongs to the consuming business system.

### 5.7 Distance

Distance provides a location fact or reusable spatial capability between places or coordinates. It does not define delivery price, ride price or dispatch policy.

### 5.8 Route

Route is a reusable location capability candidate — `CANDIDATE`. Geo Core MUST NOT be described as requiring a proprietary routing engine, consumer navigation product or real-time traffic network at this stage. Implementation and entry into M1 are `TBD — Deferred to later phase`.

### 5.9 Location Correction

Location Correction is a first-class Geo Core capability principle. It covers address errors, coordinate errors, duplicate Places, incorrect Access Points, movement, closure and external-reference conflict.

Specific correction authority, review process and lifecycle rules are `TBD — Deferred to Phase 03 Domain Model and later product design`.

### 5.10 Provider Reference

Provider Reference represents an external source of location data or capability. Possible source categories include commercial providers, open datasets, government datasets, internally verified data and user or business corrections. No specific provider is selected in this phase.

## 6. Product Boundary

### 6.1 Geo Core owns

Geo Core owns the canonical DAEN representation and governance of reusable location facts and capabilities, including:

- Location Identity
- Place facts
- Address facts
- Coordinates and their quality context
- Access Points
- Boundaries and spatial relationships
- Distance capability
- Route capability when separately approved
- Data source and provenance
- Location Correction principles and records

Operational and correction tools MAY be first-party components of Geo Core. They are means of operating the location-facts product; Geo Core's core value MUST remain usable independently of a consumer-facing map application.

### 6.2 Business systems own

Business systems own decisions and workflows such as approval, pricing, dispatching, task assignment, credit decisions, attendance policy, delivery fee, driver or rider selection, operational priority and business workflow.

Only information with cross-business location value should enter Geo Core. Business-specific metadata such as delivery instructions, customer notes, lending notes and attendance rules belongs to the business system. If generality and reuse cannot be established, the decision is `TBD — evaluate by generality and reuse`.

## 7. Boundary Examples

| Question | Geo Core | Owner |
|---|---:|---|
| Where is this Place? | Yes | Geo Core |
| What GeoID represents this Place? | Yes | Geo Core |
| What is the Access Point? | Yes | Geo Core |
| Is point X inside boundary Y? | Yes | Geo Core |
| What is the distance from A to B? | Yes | Geo Core |
| What route capability is available from A to B? | Yes / candidate capability | Geo Core |
| Should employee attendance pass? | No | OA |
| Which rider receives an order? | No | Delivery |
| What should delivery fee be? | No | Delivery |
| Should this borrower receive a loan? | No | FinTech |
| Which driver should be matched? | No | Mobility |

### 7.1 OA attendance

Geo Core MAY answer `Current coordinate ∈ Office Geofence?`. OA decides normal attendance, late arrival, early departure or abnormal check-in.

### 7.2 Delivery

Geo Core MAY provide Place references, Access Points, distance and route capability. Delivery decides rider selection, delivery price, dispatch priority and SLA.

### 7.3 Lending and FinTech

Geo Core MAY provide location, address, location-verification facts, distance and boundary facts. FinTech decides credit approval, credit score, loan limit and risk policy.

### 7.4 Mobility

Geo Core MAY provide pickup or destination location facts only as generic Places or Access Points. Mobility decides driver matching, fare, surge and cancellation policy. “Pickup Point” remains a Mobility interpretation, not a Geo Core fact category.

## 8. Product Principles

### P1 — Stable DAEN-Controlled Identity

**Principle:** A Place MUST be referable by a stable DAEN-controlled identity.

**Meaning:** External references, coordinates, addresses, names and business IDs are representations or references, not the canonical identity.

**Implication:** GeoID MUST NOT be reassigned to a different real-world Place; historical references MUST remain resolvable after closure, merge, split and withdrawal. Resolvable does not mean active or valid for new operational use. Authorized legal, privacy or security removal MAY restrict underlying data through a controlled process, but the identifier MUST NOT become reusable.

**Forbidden shortcut:** Using a provider ID or coordinate as the permanent DAEN identity.

### P2 — Provider Independence

**Principle:** A provider is a source of data or capability, not the owner of Geo Core identity.

**Meaning:** Internal identity and business references SHOULD remain independent of one provider's model.

**Implication:** The conceptual relationship is `Provider → Provider Reference / Adapter → Geo Core → GeoID → Business Systems`.

**Forbidden shortcut:** Binding the canonical Place identity to an external provider record.

### P3 — Geography, Not Business Logic

**Principle:** Geo Core manages geographic facts; business systems decide business actions.

**Meaning:** Geo Core answers what the known location facts are, not what a business should do.

**Implication:** Approval, pricing, assignment, dispatch, credit and attendance decisions remain outside Geo Core.

**Forbidden shortcut:** Adding a business decision because it consumes a location fact.

### P4 — Source Traceability

**Principle:** Material location facts MUST be traceable to source and update context.

**Meaning:** The product must be able to represent source, update time, precision or confidence and correction history in later phases.

**Implication:** Provenance and quality are part of the product boundary even though fields are deferred.

**Forbidden shortcut:** Presenting a location fact without any source or quality context.

### P5 — Correctable Reality

**Principle:** Geo Core MUST support correction of changing and incorrect location facts.

**Meaning:** Correction is a core capability principle, not an ad hoc administrative repair.

**Implication:** Address, coordinate, duplicate, Access Point, closure, movement and provider-conflict cases require explicit later semantics.

**Forbidden shortcut:** Treating the first imported value as permanently authoritative.

### P6 — Access Point Matters

**Principle:** A Place representative coordinate MUST NOT be treated as its only practical access point.

**Meaning:** Access Point is the general concept; Entrance MAY later be a subtype or semantic.

**Implication:** Multiple access modes MAY be represented later without turning business-purpose pickup semantics into Geo Core facts.

**Forbidden shortcut:** Reusing the Place center for all arrival and access decisions.

### P7 — Contract-First, Not Map-App-First

**Principle:** Geo Core SHOULD be consumed through stable data and service contracts; a consumer map application is optional.

**Meaning:** Data, API, SDK and operational or correction tools are possible product surfaces; exact contracts are deferred.

**Implication:** A map view MAY assist inspection, but it is not the product definition.

**Forbidden shortcut:** Making a map screen the only way to use or validate Geo Core.

### P8 — Explicit Data Quality

**Principle:** Geo Core MUST NOT treat all location data as equally accurate.

**Meaning:** Precision, confidence, source quality and verification state must be representable in later phases.

**Implication:** Consumers can distinguish known, uncertain and corrected facts when the later model is defined.

**Forbidden shortcut:** Returning coordinates or addresses with implied certainty when quality is unknown.

### P9 — Multiple Representations Do Not Imply Multiple Places

**Principle:** Multiple names, languages, addresses, external references, Access Points or coordinates do not automatically mean multiple Places.

**Meaning:** One reality can have multiple valid representations.

**Implication:** Identity resolution and duplicate handling require explicit Phase 03 semantics.

**Forbidden shortcut:** Creating a new Place solely because a provider, language or address representation differs.

### P10 — Cambodia First, Without Premature Internationalization

**Principle:** Product validation begins with Cambodia while the core concepts remain general enough to avoid artificial country lock-in — `RECOMMENDED`.

**Meaning:** Cambodia is the priority direction; this is not a decision to expand internationally.

**Implication:** Later geographic scope decisions must follow evidence, licensing and operating capacity.

**Forbidden shortcut:** Either hard-coding the concept to one country's administrative assumptions or promising international coverage before validation.

### Principle priority

Internal priority is not equal:

- Tier 0: P3 Geography, Not Business Logic
- Tier 1: P1 Stable Identity; P4 Source Traceability; P5 Correctable Reality
- Tier 2: P2 Provider Independence; P6 Access Point; P8 Explicit Data Quality; P9 Multiple Representations
- Tier 3: P7 Contract-First; P10 Cambodia First

## 9. Explicit Non-Goals

Geo Core is not:

- A consumer map application
- A social map
- A Google Maps clone
- A navigation application
- A delivery platform
- A logistics dispatch platform
- A ride-hailing platform
- An OA system
- A credit engine
- A pricing engine
- A business workflow engine

This phase does not commit to:

- A nationwide proprietary basemap
- A proprietary road network
- A proprietary routing engine
- A real-time traffic network
- Consumer user growth
- Map social features

## 10. Location Fact vs Business Decision

The general rule is:

> If a question describes a location fact, a Place identity or a reusable spatial relationship, it tends toward Geo Core.

> If a question decides what a business should do, for whom, at what price or whether to approve an action, it belongs to the upper-layer business system.

## 11. Data Ownership Principles

### 11.1 Canonical Geo Core identity

DAEN Geo Core controls the canonical DAEN representation of known location facts. It does not claim absolute truth about physical reality.

### 11.2 External provider reference

External provider references belong to their sources and map into Geo Core. They do not control internal identity.

### 11.3 Business-specific metadata

Business-specific metadata belongs to the business system unless it meets the Geo Core Scope Admission Test.

### 11.4 Geo Core Scope Admission Test

A new information type or capability MAY enter Geo Core only when it passes the following test:

1. **MUST 1 — Reality:** It describes a real-world place, location or spatial relationship.
2. **MUST 2 — Consumer-neutral semantics:** Its meaning does not change between OA, Delivery, FinTech, Mobility or another consumer.
3. **MUST 3 — Non-decision:** It describes what reality is; it does not decide what a business should do.
4. **MUST 4 — Governable:** It can have clear provenance, quality and correction semantics.
5. **SHOULD 5 — Reusability:** It should have value for reuse across systems, without requiring two existing consumers as a hard threshold.

If the test cannot be applied, the item is `TBD — evaluate by generality and reuse`.

## 12. Change Governance

Any later requirement that changes the Geo Core definition, changes the Geo Core versus business-system boundary, makes a provider ID the core identity, introduces a business decision, downgrades Location Correction to a temporary mechanism, or treats an Access Point as identical to a Place center MUST first modify this Constitution.

The product boundary MUST NOT be changed silently through a PRD, API, database migration or implementation.

Normal correction MUST preserve non-destructive history for material location changes, except where an authorized legal, privacy, security or data-rights process requires removal.

Operational and correction tools MAY be first-party Geo Core components, but they remain means of operating the product rather than the complete product definition.

## 13. Decision Status

| Topic | Decision | Status |
|---|---|---|
| DAEN brand and umbrella | DAEN is the project working brand and location-infrastructure umbrella | `CONFIRMED` |
| Brand expression | ដែន / DAEN / 域联 | `RECOMMENDED` |
| Positioning | Cambodia Location Infrastructure | `RECOMMENDED` |
| Long-term expression | Cambodia Location Network | `CANDIDATE` |
| Mission line | Connect Every Place. | `CANDIDATE` |
| Core platform | DAEN Geo Core | `CONFIRMED` |
| Place identity | A Place MUST have stable DAEN-controlled identity capability | `CONFIRMED` |
| GeoID | Working term; format and lifecycle deferred | `CANDIDATE` |
| Provider independence | Product principle | `CONFIRMED` |
| Location Correction | Core capability principle | `CONFIRMED` |
| Access Point | Core concept; exact taxonomy deferred | `CONFIRMED` |
| Route | Reusable location capability candidate | `CANDIDATE` |
| Consumer map application | Non-goal | `CONFIRMED` |
| M1 | Deferred to later phase | `TBD` |
| Domain Model | Deferred to Phase 03 | `TBD` |
| API | Deferred to Phase 05 | `TBD` |
| Architecture | Deferred to Phase 06 | `TBD` |

## 14. Phase 03 Entry Gate

Only after this Product Constitution passes human review and is frozen may the project enter `Phase 03 — Domain Model`.

Phase 03 will address GeoID, Place, Address, Coordinate, Access Point, Boundary, Provider Reference, Location Correction, relationships, lifecycle and identity resolution. Those topics are explicitly deferred from this Constitution.
