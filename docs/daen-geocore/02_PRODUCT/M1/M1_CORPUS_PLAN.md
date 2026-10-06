# M1 Corpus Plan

## 1. Registration status

This is a pre-registration plan only. Actual Place names remain `TBD` for later human selection. No M1 scenario is executed by this document.

## 2. Corpus size and mix

- Initial slots: **20 Places**
- Maximum after split-created Places: **23 Places**
- Recommended target: approximately **12 real public Places** and **8 synthetic Places/cases**
- Every synthetic item MUST be clearly marked synthetic.
- No private-home or personal-location data.

## 3. Twenty corpus slots

| Slot | Target case | Type target | Primary coverage |
|---|---|---|---|
| P01 | Simple persistent Place | Real | Stable identity |
| P02 | Multilingual / multi-script Place | Real | Representations, Source Assertions |
| P03 | Multiple address expressions | Real | Address assertions |
| P04 | Conflicting coordinate assertions | Real | Selected Coordinate, Quality |
| P05 | Access Point differs from Selected Coordinate | Real | Access Point |
| P06 | Second Access Point for one Place | Real | Multiple access |
| P07 | Shared Access Point with another Place | Real | Shared access |
| P08 | Duplicate candidate for merge direction 1 | Real | Merge |
| P09 | Duplicate candidate for merge direction 2 | Real | Merge |
| P10 | Mis-conflation split source | Real | Split: mis-conflation |
| P11 | True division split source | Real | Split: true division |
| P12 | Closed physical Place | Real | Closure, lifecycle |
| P13 | Withdrawn or restricted historical reference | Real | Withdrawal, resolvability |
| P14 | Corrected address or coordinate | Real | Correction, supersession |
| P15 | Provider/reference change | Real | Provider independence |
| P16 | Current DAEN Representation change | Synthetic | Representation lifecycle |
| P17 | Ambiguous or shared address | Synthetic | Identity ambiguity |
| P18 | Parent Place containing child Place | Synthetic | Containment |
| P19 | Second containment example | Synthetic | Containment |
| P20 | Coarse locating basis without precise coordinate | Synthetic | Spatial anchoring |

Actual names, source references and final real/synthetic assignment are left for human corpus preparation.

## 4. Coverage matrix

| Coverage | Slots |
|---|---|
| Simple Place | P01 |
| Multilingual / multi-script | P02 |
| Multiple address expressions | P03 |
| Conflicting coordinates | P04 |
| Access Point != Selected Coordinate | P05, P06, P07 |
| Shared Access Point | P07 |
| Duplicate / merge | P08, P09 |
| Mis-conflation split | P10 |
| True division split | P11 |
| Withdrawal | P13 |
| Closure | P12 |
| Correction | P14 |
| Provider/reference change | P15 |
| Current DAEN Representation change | P16 |
| Ambiguous/shared address | P17 |
| Containment | P18, P19 |
| Coarse locating basis | P20 |

## 5. Optional field verification

Up to 5 public Places MAY be field-verified. Field verification is optional and is not required for M1 freeze. It must not introduce private-home or personal-location data.

## 6. Surprise cases

Plan 3 surprise cases. The Reviewer SHOULD select them after reviewing the registered corpus, and they must remain within the frozen Phase 03 domain boundary.
