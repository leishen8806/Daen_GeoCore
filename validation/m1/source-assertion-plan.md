# DAEN Geo Core — M1 Source Assertion Plan

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

This plan uses only the evidence frozen in `corpus-evidence.md` and `field-evidence/P04.md`. It registers possible attributed assertions; it does not select a Current DAEN Representation or decide disputed facts.

| Slot | Research display name | Evidence references | Assertion categories available | Known uncertainty | Synthetic augmentation allowed? |
|---|---|---|---|---|---|
| P01 | Cambodia Post Central Post Office | Cambodia Post locations; public Central Post Office reference | Name; Address; Coordinate; Provider/reference assertion | Transliteration and map point may vary | YES, entry-level only |
| P02 | Royal Palace of Cambodia | Cambodia tourism; Royal Palace site; Chinese public reference | Name; Address; Coordinate; Extent; Provider/reference assertion | Complex boundary and centroid | YES, entry-level only |
| P03 | Raffles Hotel Le Royal Phnom Penh | Raffles; Accor | Name; Address; Coordinate; Provider/reference assertion | Operational closure/rebranding is not Place closure | YES, entry-level only |
| P04 | AEON Mall Phnom Penh | AEON official page; P04 field evidence | Name; Address; Coordinate; Extent; Access Point; Provider/reference assertion | Official route does not prove exact entrance coordinate | YES, entry-level only |
| P07 | Royal University of Phnom Penh Main Campus | RUPP site; RUPP institutional guide | Name; Address; Extent; Provider/reference assertion | Campus boundary/access representation | YES, entry-level only |
| P08 | Hun Sen Library, RUPP | RUPP site; RUPP tracer-study document | Name; Address; Coordinate; Provider/reference assertion | Exact building footprint | YES, entry-level only |
| P09 | Royal Phnom Penh Hospital | Official contact page; public map; hospital network listing | Name; Address; Coordinate; Access Point; Provider/reference assertion | Usable entrance not publicly verified; field check optional | YES, entry-level only |
| P10 | Aquation Diamond Island Office Park | Aquation location page; Aquation factsheet | Name; Address; Extent; Access Point; Provider/reference assertion | Exact compound gate not publicly verified; field check optional | YES, entry-level only |
| P11 | Royal Group Phnom Penh Special Economic Zone | PPSEZ zone map; public SEZ guide; public entrance context | Name; Address; Extent; Access Point; Provider/reference assertion | Current usable gate not publicly verified; field check optional | YES, entry-level only |
| P13 | Calmette Hospital coordinate-conflict case | Calmette official location; public map; research PDF | Name; Address; Coordinate; Provider/reference assertion | `PUBLIC-SOURCE CONFLICT — UNRESOLVED`; do not choose coordinate | YES, entry-level only |
| P14 | AEON Mall Cambodia Parking Tower building | AEON mall page; company profile; public same-address example | Name; Address; Extent; Provider/reference assertion | Building/premises distinction and footprint | YES, entry-level only |
| P20 | Former White Building, Phnom Penh | Public historical record; demolition report; architecture catalogue | Name; Address; Coordinate; Provider/reference assertion | Demolition/rebuild identity remains TBD | YES, entry-level only |

Synthetic augmentation means a synthetic assertion may be attached to a real Place for a controlled scenario. It must be marked `SYNTHETIC` at entry level and must not be presented as public fact.
