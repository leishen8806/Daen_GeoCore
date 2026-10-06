# M1 Model Friction Log

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

Empty log template. Do not populate entries before M1 execution.

## Trigger questions

- What object should this be?
- Is this the same Place?
- Where does this fact belong?
- Which identity should survive?
- Can the current model represent this case?
- Do we need a new concept?

## Approved classification values

- Terminology ambiguity
- Identity ambiguity
- Missing relationship
- Missing lifecycle semantics
- Governance ambiguity
- Implementation question
- Out-of-scope business concept

## Operational observation — Data Maintenance Friction

During M1, reviewers SHOULD record when obtaining or correcting a usable location fact requires:

- field verification;
- specialist judgment;
- repeated manual research;
- multiple user actions.

This is an operational observation, not a Domain Model invariant. It MUST NOT automatically cause `RETURN TO DOMAIN MODEL`.

If field verification appears necessary for routine Place maintenance, record:

`OPERATIONAL WARNING — LOCATION DATA MAINTENANCE COST MAY NOT SCALE`

Do not design future contribution UX in this phase.

## Resolution types

- frozen rule cited
- invented rule
- escalated

## Entry template

### Friction F-___

- **Scenario:**
- **Place/corpus slot:**
- **Question:**
- **Classification:**
- **Resolution type:**
- **Proposed missing wording if an invented rule was required:**
- **Repeated pattern count:**
- **Reviewer notes:**

## Retrospective Review Findings — RUN-A-02

> RETROSPECTIVE REVIEW FINDING — discovered during independent review, not recorded as contemporaneous operator friction.

| Finding | Affected run / evidence | Classification | Project disposition |
|---|---|---|---|
| F1 — Cross-scope supersession is ambiguous and the selection label conflicts with its link | RUN-A-02; `POST-P02-CR`; review sensitivity check | Governance ambiguity | Prospective selection-scope clarification adopted. Historical ambiguity retained. Selection coexistence is not validated by RUN-A-02. |
| F2 — Initial selections marked REAL without a frozen convention | RUN-A-02; `PRE-P01-CR`, `PRE-P02-CR` | Implementation question | Prospective M1 marking convention clarified. Historical marking retained. |
| F3 — P01 initial language scope omitted while described as English | RUN-A-02; `PRE-P01-SA1`, `operator-execution.md` | Terminology ambiguity | Prospective explicit-language convention clarified. Historical omission retained. |
| F4 — Exact source-specific attribution of strings not established | RUN-A-02; `source-map.md` P01-E2/P02-E2 | Implementation question | Evidence limitation accepted for Scenario A narrow scope. No exact external-source verification claim. |
| F5 — Selection attribution is not distinct from assertion provenance | RUN-A-02; selection rows and operator record | Implementation question | Future selections require operator/step attribution distinct from assertion provenance, using existing records. |
| F6 — Checker does not test scope-aware supersession or concept-typed references | RUN-A-02; independent-review sensitivity checks | Implementation question | Checker limitation retained for manual review. No checker enhancement authorized. |
| F7 — Encoding decisions were not logged contemporaneously and RUN-A-01 retrospective pointer was absent | RUN-A-01 and RUN-A-02; disposition and shared log | Governance ambiguity | Retrospective findings and pointers are now recorded. They are not recast as RUN-A-01 observations. |
| F8 — `locus=` is name-derived rather than an independent locator | RUN-A-02; `PRE-P01-PLACE` / `PRE-P02-PLACE` | Implementation question | Evidence limitation accepted for Scenario A narrow scope. No new locator concept added. |

All rows above were discovered at independent review stage. They are not claims about private operator reasoning and do not automatically imply a Domain Model failure.
