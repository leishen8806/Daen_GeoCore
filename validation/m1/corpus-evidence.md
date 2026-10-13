# M1 Corpus Evidence — Phase 04C

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

This note records public research used to pre-register the approved corpus. It does not create GeoIDs, select a canonical coordinate, or treat an external provider identifier as DAEN identity. No private or personal information is included.

## P01 — Cambodia Post Central Post Office
- **Public location:** Cambodia Post identifies its Phnom Penh central office through its public location page; public reference material identifies the historic Central Post Office in central Phnom Penh.
- **Reason selected:** Public standalone civic building for stable identity and correction assertions.
- **Scenarios challenged:** A, B, F.
- **Evidence:** [Cambodia Post locations](https://cambodiapost.com.kh/location); [Central Post Office](https://en.wikipedia.org/wiki/Central_Post_Office%2C_Phnom_Penh).
- **Known uncertainty:** Public pages may use different transliterations or map points for the same building.

## P02 — Royal Palace of Cambodia
- **Khmer/public names:** ព្រះបរមរាជវាំង; Royal Palace of Cambodia.
- **Public location:** Bounded royal/public complex in central Phnom Penh.
- **Reason selected:** Public complex with Khmer, English and Chinese public naming and multiple source representations.
- **Scenarios challenged:** A, B, C, J.
- **Evidence:** [Cambodia tourism](https://www.tourismcambodia.org/public/provinces/search/detail/127/royal-palace-1548301051); [Royal Palace site](https://www.royalpalacephnompenh.com/km/); [Chinese public reference](https://zh.wikipedia.org/wiki/%E9%87%91%E8%BE%B9%E7%8E%8B%E5%AE%AB).
- **Known uncertainty:** Complex boundary and public map centroid are not treated as an access point.

## P03 — Raffles Hotel Le Royal Phnom Penh
- **Public location:** Historic hotel in central Phnom Penh, represented by Raffles and Accor.
- **Reason selected:** Hotel with stable public identity and potentially different public address/name representations.
- **Scenarios challenged:** A, B, F, I.
- **Evidence:** [Raffles](https://www.raffles.com/phnom-penh/about/); [Accor](https://all.accor.com/hotel/A5E0/index.en.shtml).
- **Known uncertainty:** Historical operational closure or rebranding is an occupant/business event and MUST NOT be recorded as Place closure.

## P04 — AEON Mall Phnom Penh
- **Public location:** Public shopping mall in Phnom Penh represented by AEON Mall Cambodia and AEON Mall Corporation.
- **Reason selected:** Large commercial Place with multiple entrances and a distinction between map coordinate and usable arrival point.
- **Scenarios challenged:** D, E.
- **Evidence:** [AEON Mall Cambodia](https://www.aeonmallcambodia.com.kh/aeon-mall-phnom-penh-2/); [AEON Mall facility](https://www.aeonmall.com/facility/detail/723/).
- **Known uncertainty:** Sources do not reliably identify the exact usable entrance.
- **FIELD VERIFICATION REQUIRED FOR M1:** one minimal real Access Point anchor for the corpus.

## P07 — Royal University of Phnom Penh Main Campus
- **Public location:** Public university campus in Phnom Penh represented by RUPP’s official site and institutional material.
- **Reason selected:** Campus-scale Place with multiple buildings and boundary/access distinction.
- **Scenarios challenged:** A, B, J.
- **Evidence:** [RUPP](https://www.rupp.edu.kh/); [RUPP institutional guide](https://www.rupp.edu.kh/iro/document/IRO-Guide-2018.pdf).
- **Known uncertainty:** Campus boundary and preferred approach require review.

## P08 — Hun Sen Library, RUPP
- **Public location:** Named library building within the RUPP campus, identified in public RUPP material.
- **Reason selected:** Distinct building physically contained within P07.
- **Scenarios challenged:** A, J.
- **Evidence:** [RUPP](https://www.rupp.edu.kh/); [RUPP tracer-study document](https://www.rupp.edu.kh/iro/document/The%20Findings%20of%20Tracer%20Study2020-STEM.KH.E.Stamped.pdf).
- **Known uncertainty:** Exact footprint and public entrance are not established by the cited documents.

## P09 — Royal Phnom Penh Hospital
- **Public location:** No. 888, Russian Federation Blvd (110), Sangkat Tuek Thla, Khan Sen Sok, Phnom Penh.
- **Reason selected:** Public hospital campus whose usable entrance may differ from a generic map centre; kept separate from P13 Calmette Hospital.
- **Scenarios challenged:** D, F.
- **Evidence:** [official contact page](https://www.royalphnompenhhospital.com/contactus); [public map record](https://mapcarta.com/W379562472); [public hospital network listing](https://www.prudential.com.kh/export/sites/prudential-kh/en/.galleries/pdf/Hospital-Network-18thMarch2022-EN.pdf).
- **Known uncertainty:** Sources confirm the campus and address but not the exact usable emergency or visitor access point.
- **Field verification status:** FIELD VERIFICATION OPTIONAL — NOT REQUIRED FOR M1.

## P10 — Aquation Diamond Island Office Park
- **Public location:** Aquation’s Diamond Island office/retail estate in Phnom Penh, described publicly as a multi-building estate with parking and security.
- **Reason selected:** Large compound where geometric centre is not necessarily a usable gate or building entrance.
- **Scenarios challenged:** D, E, J.
- **Evidence:** [Aquation location](https://www.aquation.asia/location/); [Aquation factsheet](https://www.aquation.asia/media/docs/aquation/factsheets/Aquation-Factsheets-July-2021-ENG.pdf).
- **Known uncertainty:** Sources describe the estate but do not verify a specific gate.
- **Field verification status:** FIELD VERIFICATION OPTIONAL — NOT REQUIRED FOR M1.

## P11 — Royal Group Phnom Penh Special Economic Zone
- **Public location:** Industrial zone on National Road 4 in Phnom Penh, represented by the operator’s zone map and a public SEZ guide.
- **Reason selected:** Large industrial premises with perimeter access and a distinction between geometric centre and usable gate.
- **Scenarios challenged:** D, J.
- **Evidence:** [PPSEZ zone map](https://rgppsez.com.kh/en/our-business/ppsez-zone-map); [public SEZ guide](https://data.vietnam.opendevelopmentmekong.net/dataset/033b89aa-daaf-4ae6-839f-1ea2b93d7cf3/resource/f010d62a-ac28-4774-b9dd-97963727d64b/download/alternative_manufacturing_sezs_guidebook__00.00.2024.pdf); [public entrance context](https://www.sciencespo.fr/coesionet/sites/default/files/GMS%20Capstone%20Report%20May%2017.pdf).
- **Known uncertainty:** Zone is identifiable, but the currently usable gate is not proven by these sources.
- **Field verification status:** FIELD VERIFICATION OPTIONAL — NOT REQUIRED FOR M1.

## P13 — Calmette Hospital coordinate-conflict case
- **Public location:** Calmette Hospital is a public Phnom Penh hospital; official and public map/research sources publish materially different coordinate representations.
- **Reason selected:** Genuine public-source coordinate conflict for attribution and quality handling.
- **Scenarios challenged:** B, C, F.
- **Evidence:** [Calmette official location](https://calmette.gov.kh/calmette-hospital-location/); [OSM-derived map record](https://mapcarta.com/W165927974); [public research-network PDF](https://www.melioidosis.info/download/RC_KHM_CHPP01_Cases_Y2013Y2018_D20191112.pdf).
- **Known uncertainty:** Correct coordinate is intentionally not decided during pre-registration.
- **Field verification status:** PUBLIC-SOURCE CONFLICT — UNRESOLVED. No field verification is required for M1.

## P14 — AEON Mall Cambodia Parking Tower building
- **Public location:** Parking Tower building/premises associated with AEON Mall Cambodia’s Phnom Penh site.
- **Reason selected:** Distinct physical building/premises sharing a public mall address expression; company/head-office identity is not the Place.
- **Scenarios challenged:** B, J.
- **Evidence:** [AEON Mall page](https://www.aeonmallcambodia.com.kh/aeon-mall-phnom-penh-2/); [company profile](https://www.aeonmallcambodia.com.kh/wp-content/uploads/2023/05/230419-2023-ver-AMC-Company-Profile.pdf); [public same-address example](https://www.waze.com/fy/live-map/directions/kh/phnom-penh/pp/smart-shop-phnom-penh-aeon-mall?to=place.ChIJi65O-StRCTERDtc_jqCW3ZA).
- **Known uncertainty:** Sources support shared-address and building distinction but not exact tower footprint.

## P20 — Former White Building, Phnom Penh
- **Public location:** Former Municipal Apartments/White Building on Samdach Sothearos Boulevard; historic building demolished in 2017.
- **Reason selected:** Historical Place with public demolition and changed-site-status evidence, without confusing occupant closure with Place closure.
- **Scenarios challenged:** I, C.
- **Evidence:** [White Building record](https://en.wikipedia.org/wiki/White_Building_%28Phnom_Penh%29); [SCMP demolition report](https://www.scmp.com/magazines/post-magazine/long-reads/article/2106117/last-look-icon-cambodias-golden-age-it-bulldozed); [public architecture catalogue](https://www.raintreecambodia.com/s/Catalogue_Modern-Architecture-Echoes-Reflections_Final_13112024.pdf).
- **Known uncertainty:** Whether later redevelopment is the same Place remains TBD and is not decided here.

## Synthetic cases

P05, P06, P12, P15, P16, P17, P18 and P19 are deliberately synthetic validation fixtures. They carry no public-place claim and must receive entry-level synthetic marking in any future state ledger or assertion.

## Pre-registration boundary

No GeoID, actual result, PASS/FAIL, friction entry, GO/ITERATE/RETURN outcome, canonical coordinate, Access Point handle, merge survivor or demolition/rebuild identity is created by this document.
