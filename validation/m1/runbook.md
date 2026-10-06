# DAEN Geo Core — Phase 04D-0 M1 Execution Runbook

> VALIDATION RUNBOOK — NOT A PRODUCT SPECIFICATION, NOT AN API, NOT A DATABASE DESIGN.

## Roles

### Data Operator — Codex

- Register Source Assertions and manipulate validation fixtures.
- Execute scenario actions only after this preparation is reviewed.
- Record actual results and friction immediately during execution.
- Never decide unresolved domain policy.

### Independent Reviewer — Claude

Later, the Reviewer will compare actual and expected outcomes, review same-Place judgments, merge/split semantics, friction and invented rules, perform manual B1–B11 review, and recommend PASS / FAIL / INEXPRESSIBLE per scenario.

### Final Decision Layer

The human owner and ChatGPT review approve amendments and decide GO / ITERATE / RETURN.

AI execution/review separation is an M1 independence mechanism. It is not external customer validation.

## Local identifiers

Run labels use `RUN-<scenario>-<sequence>`, for example `RUN-A-01` and `RUN-B-01`. They are local M1 evidence labels only; they are not API identifiers, database IDs or production event IDs.

Fixture identity handles use `FIX-ID-P01`, `FIX-ID-P02`, and so on. These are non-production stand-ins for conceptual DAEN-controlled Place identity. They are not actual or proposed GeoID format and do not resolve the GeoID-format TBD.

## Frozen execution order

Execute only after readiness review, in this order:

| Order | Scenario | Frozen target slots | Frozen expected outcome | Invariant references |
|---:|---|---|---|---|
| 1 | A — Stable Identity | P01, P02 | One Place and one GeoID remain stable; representations and assertions may vary | 1, 4 |
| 2 | B — Multiple Source Assertions | P02, P03, P04, P17 | Assertions remain attributable; conflict does not silently create or merge Places; Quality is explicit | 5, 10 |
| 3 | C — Current DAEN Representation Change | P04, P14, P16 | Current representation changes without destructive overwrite; prior material state remains traceable | 4, 8, 9 |
| 4 | D — Access Point | P05, P06, P07 | Access Point remains separate and is not inferred solely from coordinate | 6 |
| 5 | E — Shared Access Point | P07 | One shared Access Point links to multiple Places without pickup/drop-off semantics | 7 |
| 6 | F — Correction | P04, P14, P15 | Wrong fact is superseded, attribution remains, identity is not silently changed | 2, 5, 8 |
| 7 | G — Merge | P08, P09 | One identity resolves to survivor; retired GeoID remains resolvable; no survivor policy invented | 1, 3 |
| 8 | H — Split | P10, P11 | Mis-conflation and true division retain the frozen distinct outcomes | 1, 3 |
| 9 | I — Withdrawal / Closure | P12, P13 | GeoIDs remain resolvable as closed, withdrawn or historical; resolvable does not mean active | 3 |
| 10 | J — Containment | P18, P19 | Minimal Place-contains-Place relationships without Area, business hierarchy or new taxonomy | 11 |

The scenario-sheet wording and expected outcomes are authoritative and are not rewritten here.

Execution note: `RUN-A` target conflict resolved before execution. Authoritative targets are `P01, P02` because both the frozen `scenario-sheet.md` and this frozen runbook define Scenario A as P01/P02. No scenario amendment was approved.

## Scenario-sheet immutability

`validation/m1/scenario-sheet.md` is the frozen PRE-REGISTRATION artifact. During execution, expected outcomes and pre-registered scenario definitions MUST NOT change. Actual execution results MUST NOT be written back into the frozen expected-outcome definitions; they belong in execution records, run evidence, result summary and Reviewer notes. This is an execution-medium rule, not a Domain Model decision, and preserves VM-I02.

## Preparation boundaries

- No scenario A–J has been executed.
- No actual result, PASS / FAIL / INEXPRESSIBLE, Friction Log finding or GO / ITERATE / RETURN decision is written during preparation.
- P04 field evidence is referenced without reinterpretation.
- P13 remains `PUBLIC-SOURCE CONFLICT — UNRESOLVED`.
- Surprise cases are reserved for the independent Reviewer.

## M1 Execution Readiness

- [x] validation harness baseline frozen
- [x] corpus baseline frozen
- [x] field-verification rule frozen
- [x] P04 field evidence frozen
- [x] checker self-test PASS
- [x] runbook frozen
- [x] synthetic case plan frozen
- [x] source assertion plan frozen
- [x] initial-state plan frozen
- [x] execution checklist frozen
- [x] manual review matrix frozen
- [x] Operator / Reviewer separation documented
- [x] surprise cases reserved for Reviewer
- [x] working tree clean after readiness commit

This checklist is not complete until the preparation documents are reviewed and a later readiness commit is approved.

## M1 Fixture Conventions — Prospective

- Public Source Assertions supported by frozen evidence may remain `REAL`, with their evidence limitations.
- Fixture-created initial selections are `SYNTHETIC`.
- Controlled later selection operations are `SYNTHETIC`.
- A synthetic operation on a real Place does not make the physical Place or its supported public assertions synthetic.
- When language is relevant, name-selection scope MUST be explicit. An omitted language is unspecified; it is not automatically English or all languages. Historical runs are not retroactively changed.
- Source provenance and operator/step selection attribution are distinct. Existing run/step references and Markdown execution records are sufficient; no new entity, column or parser rule is introduced.
- Evidence supported by a frozen research memo is distinct from evidence confirmed in an exact original source. The former MUST NOT be promoted into the latter.

These are M1 evidence conventions, not a production event taxonomy.
