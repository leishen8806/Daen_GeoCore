# RUN-G-01 — Frozen Merge Inputs

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Authority and targets

- Run: RUN-G-01
- Erratum commit: eac2d7561a1b46096e2106e2201da3b7c6dd0788
- Original frozen G registration: P08, P09
- Effective approved targets: P15, P16
- Frozen action remains: test both survivor directions for two records determined to represent the same Place.
- Frozen expected outcome remains: one identity resolves to the survivor, the retired identity remains resolvable and no survivor-selection policy is invented.

The target erratum is the authority for target selection only. The original scenario sheet and runbook remain unchanged historical evidence.

## Same-Place premise

For RUN-G-01, P15 and P16 are treated as two distinct synthetic records representing the same intended synthetic locus. This premise is supplied by the controlled M1 fixture and the frozen P16 same-intended-locus plan. It is not a general equivalence algorithm.

- Provenance: SYN-G-SAME-LOCUS
- Quality: unknown
- P15 and P16: SYNTHETIC

## Common PRE fixture

| Row | Subject | Provenance | Fact | Purpose | Value | Quality | Classification |
|---|---|---|---|---|---|---|---|
| P15 Place | FIX-ID-P15 | G-PLACE-P15 | Place | locus | synthetic P15 intended locus | unknown | SYNTHETIC |
| P15 source | FIX-ID-P15-SA-RECORD | SYN-G-P15-RECORD | provider-reference | external-location-reference | SYN-G-P15-SOURCE-RECORD-001 | unknown | SYNTHETIC |
| P16 Place | FIX-ID-P16 | G-PLACE-P16 | Place | locus | synthetic P15/P16 same intended locus | unknown | SYNTHETIC |
| P16 source | FIX-ID-P16-SA-RECORD | SYN-G-P16-RECORD | provider-reference | external-location-reference | SYN-G-P16-SOURCE-RECORD-002 | unknown | SYNTHETIC |

No merge is pre-applied. No Resolution Link or Succession exists in PRE. No Current DAEN Representation is required.

## Isolated survivor-direction subcases

These are alternative test worlds from byte-equivalent PRE snapshots, not sequential events.

### Subcase A — P15 survives

- Survivor: FIX-ID-P15
- Retired: FIX-ID-P16
- Resolution Link: FIX-RES-G-A-P16-TO-P15
- Succession: FIX-SUCC-G-A-P16-TO-P15
- Merge-action provenance: SYN-G-MERGE-A
- Succession provenance: SYN-G-SUCC-A
- retired_resolvable=true
- survivor_basis=test-direction-only
- survivor_policy=not-defined
- historical requests for FIX-ID-P16 resolve to FIX-ID-P15

### Subcase B — P16 survives

- Survivor: FIX-ID-P16
- Retired: FIX-ID-P15
- Resolution Link: FIX-RES-G-B-P15-TO-P16
- Succession: FIX-SUCC-G-B-P15-TO-P16
- Merge-action provenance: SYN-G-MERGE-B
- Succession provenance: SYN-G-SUCC-B
- retired_resolvable=true
- survivor_basis=test-direction-only
- survivor_policy=not-defined
- historical requests for FIX-ID-P15 resolve to FIX-ID-P16

No lower-ID, age, richness, real/synthetic or source-trust survivor policy is defined. These handles are local validation stand-ins, not production GeoID formats.

## Resolution Link and Succession semantics

Each POST appends exactly one Resolution Link and one Succession row. The Resolution Link records relationship=merge, retired_identity, survivor_identity, resolution_from, resolution_to, retired_resolvable=true, survivor_basis=test-direction-only and survivor_policy=not-defined. The Succession row records predecessor=retired, successor=survivor, relationship=merge and history_preserved=true, and references the corresponding Resolution Link.

## Boundaries and manual review

- E's P08 use is an E-local supporting served Place and has no bearing on G.
- C's P16 evidence and F's P15 evidence are run-local and are not mutated or imported.
- RUN-G-01 initializes its own isolated P15/P16 fixture.
- No Current DAEN Representation, Correction or Access Point state is imported.
- Review must verify same-Place premise, direction, retired resolvability, retained history and absence of survivor policy.

Acceptance limits: synthetic merge fixture only; no real-world merge; no survivor-selection algorithm; no production GeoID encoding; no provider trust ranking; no merge governance workflow; no AP behavior after merge; no overall M1 result.
