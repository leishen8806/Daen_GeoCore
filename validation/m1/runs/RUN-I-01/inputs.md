# RUN-I-01 — Frozen Closure / Withdrawal Inputs

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Authority and targets

- Historical frozen Scenario I targets: P12, P13.
- Effective targets under approved erratum: P20 closure, P03 historical-reference withdrawal.
- Target erratum commit: `13af031692b8f8e57085fc1ccd6c6ab39f2b87d8`.
- H acceptance baseline: `afd22cb483d57cd813c17969700b760b55330250`.
- The original scenario sheet and runbook remain unchanged and still show P12/P13.

## Semantic boundary

`resolvable != active` and `resolvable != valid for new operational use`.

Closure and withdrawal are isolated operations:

- Subcase C: P20 is a REAL historical physical Place. Demolition is physical Place evidence, not business closure. No successor or redevelopment identity is created.
- Subcase W: P03 is a REAL Place. Only a SYNTHETIC historical provider/reference assertion is withdrawn. The Place remains unchanged and is not closed.

Do not use hotel operational closure, rebranding, tenant closure or operating hours as Place lifecycle evidence. Do not correct, delete or replace the withdrawn reference.

## Subcase C — P20 physical closure

### PRE, exactly one row

- `FIX-ID-P20` / Place / `I-PLACE-P20` / REAL / Quality `unknown` / `locus=Former White Building Phnom Penh; identity=FIX-ID-P20`

### POST append, exactly two rows

1. `FIX-ID-P20-SA-DEMOLITION` / Source Assertion / `PUB-I-P20-DEMOLITION` / REAL / `ref=FIX-ID-P20; fact=physical-status; purpose=place-lifecycle-evidence; value=demolished in 2017`
2. `FIX-RES-I-P20-CLOSED` / Resolution Link / `SYN-I-CLOSE-P20` / SYNTHETIC / `ref=FIX-ID-P20; lifecycle=closure; relationship=closure; resolution=FIX-ID-P20; historical_identity=FIX-ID-P20; physical_status=demolished; historical_resolvable=true; valid_for_new_use=false; identity_reassigned=false; successor=none`

No Succession, Current DAEN Representation or replacement Place row.

## Subcase W — P03 historical-reference withdrawal

### PRE, exactly two rows

1. `FIX-ID-P03` / Place / `I-PLACE-P03` / REAL / Quality `unknown` / `locus=Raffles Hotel Le Royal Phnom Penh; identity=FIX-ID-P03`
2. `FIX-ID-P03-SA-REF-HIST` / Source Assertion / `SYN-I-P03-REF-HIST` / SYNTHETIC / `ref=FIX-ID-P03; fact=provider-reference; purpose=external-location-reference; value=SYN-I-P03-HISTORICAL-REFERENCE-001`

### POST append, exactly one row

- `FIX-RES-I-P03-WITHDRAWN-REF` / Resolution Link / `SYN-I-WITHDRAW-P03` / SYNTHETIC / `ref=FIX-ID-P03-SA-REF-HIST; relationship=reference-withdrawal; withdrawn_subject=FIX-ID-P03-SA-REF-HIST; target_place=FIX-ID-P03; resolution_to=FIX-ID-P03; historically_traceable=true; valid_for_new_use=false; place_identity_unchanged=true; place_lifecycle_unchanged=true; replacement=none; correction=false; deletion=false`

No new Source Assertion, Current DAEN Representation, Succession or Correction row.

## Provenance and quality

P20 Place and demolition assertion are REAL. P20 closure action is SYNTHETIC. P03 Place is REAL. P03 provider/reference fixture and withdrawal action are SYNTHETIC. Every row carries Quality `unknown`.

## Isolation and review questions

- Do not import P03 prior-run ledger state.
- P20 has no prior executed lifecycle state.
- Keep C and W separate; never combine them into one lifecycle.
- Review physical closure versus business closure; withdrawal versus correction/deletion/closure; historical resolution versus active/new-use validity.

## Acceptance limits

No production lifecycle enum, resolver/API semantics, reference-selection policy, successor identity, redevelopment identity or overall M1 result is created.
