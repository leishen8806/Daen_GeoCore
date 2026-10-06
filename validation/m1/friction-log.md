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
