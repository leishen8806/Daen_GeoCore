# RUN-I-01 — Scenario I Disposition

## Acceptance

- **Project acceptance:** `PASS` for the controlled closure / historical-reference-withdrawal outcome only.
- **Evidence:** `b311f5aff4e3258f591b2d9ec86fc907e9c40cd2`.
- **Input freeze:** `67957e1067066ca7f4947eef5e23e3462fef87f9`.
- **Target erratum:** `13af031692b8f8e57085fc1ccd6c6ab39f2b87d8`.
- Effective targets are P20 closure and P03 historical-reference withdrawal.
- Overall M1 remains `NOT MADE`.
- No I rerun is authorized.

## Conscious Reading B

Scenario I withdrawal applies to the historical reference/record. The underlying P03 Place GeoID does not enter a withdrawn state. P03 identity remains unchanged and resolvable. The withdrawn reference remains retained and historically traceable, but is not valid for new operational use.

This follows the frozen action “one historical reference withdrawn”, Domain Model §24 record semantics and historical-reference preservation language.

`RUN-I-01` does not demonstrate resolvability of a Place GeoID whose own lifecycle/status is withdrawn. This must be revisited at the final B1–B11 gate, especially B3.

## Finding dispositions

### RUN-I-01:F1

Accept the self-referential P20 closure Resolution Link as validation notation only. Do not generalize it as production design or add a lifecycle/status field.

### RUN-I-01:F2

Accept bounded demolition-to-closure mapping for this fixture. Section 20 permits demolition as a Geo Core fact; lifecycle states and transitions remain deferred. No Domain Model amendment.

### RUN-I-01:F3

Accept Reading B for this run. Add the narrow TBD `Withdrawal target scope / Place-GeoID versus historical-record withdrawal semantics`, deferred to Phase 05 API Definition / later domain-policy clarification. Do not claim B3 globally passed.

### RUN-I-01:F4

Retain status markers as validation notation only. No production enum.

### RUN-I-01:F5

Record retrospective input-freeze and invariant references. Do not edit historical source-map.md.

### RUN-I-01:F6

Retain P20 demolition year as memo-level evidence without stronger attribution.

### RUN-I-01:F7

Preserve corpus-role drift observations. Do not rewrite historical planning files.

## Non-claims

This disposition does not claim Place-GeoID withdrawal semantics, a production lifecycle/status schema, production resolver/API behavior, general demolition/redevelopment identity policy, business closure semantics or overall M1 acceptance.
