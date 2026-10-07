# RUN-D-01 — Scenario D Disposition

## Acceptance

- **Independent reviewer verdict:** `PASS`.
- **Project acceptance:** `PASS` for the frozen Scenario D outcome only.
- **Reviewed evidence:** `281d2f02b945519491376f64aa54afa23b6523a7`.
- Targets are P05, P06 and P07.
- Two distinct Access Point objects were represented separately from Places, coordinate assertions and selections.
- Access meaning and location came from separately specified synthetic access statements, not numeric difference alone.
- Selected test coordinates differ from the relevant Access Point coordinates.
- Place identities, initial selections and PRE rows remain unchanged.
- All six findings remain non-blocking.
- No D rerun is authorized or needed.
- Overall M1 decision remains `NOT MADE`.

Acceptance does not establish actual physical accessibility or a real RUPP gate, independent real-world source verification, production geometry/precision/coordinate standards, a public AP namespace, the relationship between P04's historical entrance-coordinate assertion and an AP, AP coordinate selection/correction/lifecycle/supersession, mechanical validation of served-place relationships, Scenario E, provider/routing/business behavior, or any overall M1 conclusion.

## Project reasoning note

The reviewer's wording about a fixed rule is preserved unchanged in the export. This acceptance rests on the preregistered access statements and their traceable use in the fixture. The project does not infer from a few coordinate pairs that no possible fixed algorithm could reproduce them. That universal claim is neither required nor established by Scenario D. This is a reasoning clarification, not a new finding, test, Domain Model rule or rerun reason.

## Non-blocking findings

### RUN-D-01:F1

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** Add the corrected source-reference mapping below. Original evidence and source-map.md remain unchanged.

### RUN-D-01:F2

**Classification:** `REPORTING / TRACEABILITY ISSUE`, Low. **Blocking:** No.

**Disposition:** Add the retrospective selector-alias index below. It does not claim the aliases were previously defined.

### RUN-D-01:F3

**Classification:** `VALIDATION MEDIUM ISSUE`, Low. **Blocking:** No.

**Disposition:** Served-place relationships were checked manually. Repeated served-place keys are retained as validation notation; the checker, CSV columns and encoding are not changed.

### RUN-D-01:F4

**Classification:** `EVIDENCE LIMITATION`, Low. **Blocking:** No.

**Disposition:** Access evidence is separately specified synthetic fixture text, not independently verified real-world evidence. No field research is required to close D.

### RUN-D-01:F5

**Classification:** `EVIDENCE LIMITATION`, forward-looking, Low. **Blocking:** No.

**Disposition:** Preserve the unresolved relationship between RUN-B-01's P04 observed-entrance assertion and a future AP. D did not address it because P04 was not a D target. Do not mark the original B:F4 follow-up fully resolved or add P04 automatically.

### RUN-D-01:F6

**Classification:** `EVIDENCE LIMITATION`, Low. **Blocking:** No.

**Disposition:** P05/P06 sharing is approved D fixture context only. It does not complete E's frozen P07 case. Carry this distinction into the E precheck.

## POST-REVIEW TRACEABILITY ADDENDUM

These clarifications are added after independent review. They were not fully present in the original run package. Original evidence remains unchanged.

### F1 — Source-reference erratum

The original mistyped baseline in `source-map.md` is retained as historical evidence. The corrected mappings are:

- `D-PLACE-P06` → `validation/m1/synthetic-case-plan.md`, P06 section, resolved against `df9fb2f6e3bfdfb9cccb66ad6f4d44b5afc2cf28`.
- `D-PLACE-P07` → `validation/m1/corpus-evidence.md`, P07 section, resolved against `df9fb2f6e3bfdfb9cccb66ad6f4d44b5afc2cf28`.
- `D-PLACE-P05` → `validation/m1/synthetic-case-plan.md`, P05 section, same existing context baseline.

The new mock-input mappings are:

- `SYN-D-REF-P05`, `SYN-D-REF-P06`, `SYN-D-REF-P07` → exact coordinate rows in `validation/m1/runs/RUN-D-01/inputs.md`, frozen in `a62bd735df7c1b6b1297ed046a382ce9bdade788`.
- `SYN-D-ACCESS-SHARED` → exact shared access statement in the same input file and commit.
- `SYN-D-ACCESS-P07` → exact hypothetical P07 access statement in the same input file and commit.

Input files are unchanged from `a62bd735df7c1b6b1297ed046a382ce9bdade788` through operator evidence `281d2f02b945519491376f64aa54afa23b6523a7`.

Commit roles remain distinct: `df9fb2f6` is the C acceptance baseline; `a62bd735` is the D input freeze; `281d2f0` is the D operator evidence.

### F2 — Selector-alias index

| Original selector string | Ledger row key | Selection subject | Attribution |
|---|---|---|---|
| `STEP-1-P05` | `RUN-D-01:PRE-P05-SEL` | `FIX-ID-P05-SEL` | Codex / RUN-D-01 / operator-execution.md initialization action |
| `STEP-1-P06` | `RUN-D-01:PRE-P06-SEL` | `FIX-ID-P06-SEL` | Codex / RUN-D-01 / operator-execution.md initialization action |
| `STEP-1-P07` | `RUN-D-01:PRE-P07-SEL` | `FIX-ID-P07-SEL` | Codex / RUN-D-01 / operator-execution.md initialization action |
| AP materialization | `RUN-D-01:POST-AP-SHARED` | `FIX-AP-D-SHARED` | Codex / RUN-D-01 / operator-execution.md AP append action |
| AP materialization | `RUN-D-01:POST-AP-P07` | `FIX-AP-D-P07` | Codex / RUN-D-01 / operator-execution.md AP append action |

This is a post-review index. It does not claim the STEP aliases were previously defined and invents no timestamps.

## Decision boundary

This disposition accepts only the frozen controlled Scenario D outcome. It does not mark B1–B11 globally passed or make an overall M1 decision.
