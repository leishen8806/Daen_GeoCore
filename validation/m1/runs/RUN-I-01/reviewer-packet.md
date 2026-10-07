# RUN-I-01 — Reviewer Packet

REVIEW PACKET — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Authority and target change

- Approved I target erratum: `validation/m1/errata/SCENARIO-I-TARGET-ERRATUM.md`
- Erratum commit: `13af031692b8f8e57085fc1ccd6c6ab39f2b87d8`
- Input-freeze commit: `67957e1067066ca7f4947eef5e23e3462fef87f9`
- Historical targets: P12/P13
- Effective targets: P20 closure and P03 historical-reference withdrawal
- Original scenario sheet/runbook remain unchanged and show P12/P13.

## Closure fixture

P20 is a REAL historical Place context. PRE has one Place row; POST adds one REAL demolition Source Assertion and one SYNTHETIC closure Resolution Link. The same identity remains historically resolvable, is not valid for new use, is not reassigned and has no successor. The evidence does not decide redevelopment identity.

## Withdrawal fixture

P03 is a REAL Place context. PRE has the Place and one SYNTHETIC historical provider/reference assertion. POST adds one SYNTHETIC reference-withdrawal Resolution Link. The Place identity and lifecycle remain unchanged; the historical reference is retained and traceable but not valid for new use. This is not correction, deletion or replacement.

## Counts and classification

| Subcase | PRE | POST | REAL rows | SYNTHETIC rows added |
|---|---:|---:|---:|---:|
| C — P20 closure | 1 | 3 | Place + demolition assertion | closure action |
| W — P03 withdrawal | 2 | 3 | Place | historical reference + withdrawal action |

## Manual review questions

- Is P20 physical closure clearly separated from business or occupant closure?
- Is P20 historical resolution retained without inventing redevelopment identity?
- Is P03 kept active as a Place while only the synthetic historical reference is withdrawn?
- Is withdrawal distinct from correction, deletion, closure and representation replacement?
- Are `resolvable != active` and `resolvable != valid for new operational use` explicit?
- Are provenance, Quality and REAL/SYNTHETIC boundaries preserved?
- Are C and W isolated rather than combined?

## Checker results

Both raw checker outputs are structural PASS. The checker does not establish physical closure truth, historical resolvability semantics, withdrawal semantics, new-use validity or semantic PASS.

## Prior-run isolation

P03 appeared in earlier run-local evidence; no prior ledger state was imported. P20 had no prior executed lifecycle state. A–H evidence remains untouched.

## Acceptance limits

- P20 closure is evidence-backed physical historical closure only.
- No redevelopment identity judgment is made.
- P03 reference withdrawal is synthetic.
- P03 itself is not closed.
- No production lifecycle enum, resolver/API, reference-selection policy or overall M1 result is created.

## Decision state

Reviewer verdict: ____________________

PASS / FAIL / INEXPRESSIBLE: ____________________

The operator records evidence only. No GO, ITERATE or RETURN decision is made here.
