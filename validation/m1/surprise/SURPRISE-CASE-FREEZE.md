# M1 Reviewer-Selected Surprise Case Freeze

> CONTROLLED VALIDATION FREEZE — NOT A SPECIFICATION.

## HF-S1 — Baseline

Authoritative baseline:

`75b3769264e8e35eec1d8cc595ed1b52144df489`

## HF-S2 — Capacity

Surprise Cases create zero new Place identities. They reuse existing corpus identities:

- SURPRISE-01 → P05 / P06
- SURPRISE-02 → P07 / P08
- SURPRISE-03 → P13

P04 may create an Access Point handle. Access Point is not a Place and does not change corpus capacity. No P21/P22/P23 or other corpus slots are created.

## HF-S3 — SURPRISE-01

- Dimension: Identity / Representation / Extent
- Targets: P05, P06
- Question: Does a Place retain identity when its Extent is superseded, and can two distinct Places have overlapping Extents without automatically merging or requiring a new relationship?

## HF-S4 — SURPRISE-02

- Dimension: Containment relationship × Place lifecycle
- Targets: P07, P08
- Question: If a container Place closes, does that automatically alter the contained Place or erase the containment relationship?
- Boundary: No automatic lifecycle propagation is authorized.

## HF-S5 — SURPRISE-03

- Dimension: Provenance / uncertainty / Current DAEN Representation
- Target: P13
- Question: Can a Current DAEN Representation be selected while relevant Source Assertions remain in live conflict, without source ranking, and can a contested selection be distinguished from an uncontested selection using frozen concepts and evidence context alone?
- Boundary: No source-ranking rule is authorized.

## Selection provenance

These three Surprise Cases were selected by the independent Reviewer after A–J execution. They are not retrospective relabeling of ordinary scenarios, P04 repair, B3 repair or post-hoc guaranteed-pass fixtures.
