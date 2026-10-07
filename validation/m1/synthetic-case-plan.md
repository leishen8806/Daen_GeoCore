# DAEN Geo Core — M1 Synthetic Case Plan

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

Every fact and event below is explicitly `SYNTHETIC`. These are controlled fixtures, not real places, private homes or personal locations. The plan supplies only the minimum facts needed by the frozen scenarios.

## P05 — Synthetic Mall Unit A

- Mark every assertion/event `SYNTHETIC`.
- Treat P05 as a public-facing unit inside a synthetic mall fixture.
- Give it a synthetic Place identity and a synthetic selected coordinate.
- Use one synthetic public vehicle/pedestrian Access Point distinct from that coordinate.
- Used by the frozen Access Point scenario D and shared Access Point scenario E.

## P06 — Synthetic Mall Unit B

- Mark every assertion/event `SYNTHETIC`.
- Treat P06 as a second synthetic unit in the same synthetic mall fixture.
- Link it to the same synthetic Access Point used by P05.
- Do not add pickup, drop-off or business-policy semantics.
- Used by scenarios D and E.

## P12 — Synthetic coarse-located Place

- Mark every assertion/event `SYNTHETIC`.
- Provide a valid coarse locating basis without a precise coordinate.
- Preserve an explicit historical closure/withdrawal event and a resolution reference.
- Used by scenario I; no active-use claim is created.

## P15 — Synthetic duplicate seed

- Mark every assertion/event `SYNTHETIC`.
- Provide one synthetic Place with an initial address, coordinate and provider/reference assertion.
- Add a later conflicting assertion for controlled correction testing.
- Used by scenario F.

## P16 — Synthetic duplicate of P15

- Mark every assertion/event `SYNTHETIC`.
- Provide a second synthetic record representing the same intended locus as P15.
- Preserve both source records before any later scenario action.
- Used by scenario C as frozen in the scenario sheet.

## P17 — Synthetic mis-conflation

- Mark every assertion/event `SYNTHETIC`.
- Provide two synthetic source assertions that incorrectly conflate distinct Places.
- Preserve the conflict without silently merging the Places.
- Used by scenario B and the frozen split review.

## P18 — Synthetic true division

- Mark every assertion/event `SYNTHETIC`.
- Provide one synthetic historical Place whose later facts describe two resulting Places.
- Do not silently copy the old identity to both results.
- Used by scenarios H and J.

## P19 — Synthetic occupant mistakenly modeled as Place

- Mark every assertion/event `SYNTHETIC`.
- Provide a synthetic building Place and a synthetic occupant/business assertion that is incorrectly proposed as another Place.
- Keep the business boundary explicit for reviewer judgment.
- Used by scenario J; do not add a business hierarchy concept.

No synthetic case creates a production GeoID, API identifier, schema field or new domain concept.
