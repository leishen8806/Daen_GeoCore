# RUN-I-01 — Operator Execution Record

RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity and authority

- Run ID: `RUN-I-01`
- Role: M1 Data Operator — Codex
- Historical targets: P12, P13
- Effective targets under approved erratum: P20 closure, P03 withdrawal
- I target erratum commit: `13af031692b8f8e57085fc1ccd6c6ab39f2b87d8`
- I input-freeze commit: `67957e1067066ca7f4947eef5e23e3462fef87f9`
- H acceptance baseline: `afd22cb483d57cd813c17969700b760b55330250`
- Fixture handles and synthetic reference values are validation stand-ins, not production identifiers.

## Closure / withdrawal boundary

Subcase C and Subcase W are isolated and were not combined into one lifecycle.

- P20 is a REAL historical physical Place. The frozen evidence supports demolition in 2017. The closure action is SYNTHETIC validation notation. No successor or redevelopment identity is created.
- P03 is a REAL Place. Only the synthetic historical provider/reference assertion is withdrawn. The Place remains unchanged and is not closed.
- `resolvable != active` and `resolvable != valid for new operational use`.

## Subcase C — P20 closure

| State | Rows | Content |
|---|---:|---|
| PRE | 1 | `FIX-ID-P20` Place |
| POST | 3 | PRE + REAL demolition Source Assertion + SYNTHETIC closure Resolution Link |

The closure link `FIX-RES-I-P20-CLOSED` records `lifecycle=closure`, `resolution=FIX-ID-P20`, `historical_resolvable=true`, `valid_for_new_use=false`, `identity_reassigned=false` and `successor=none`. There are zero Succession rows.

## Subcase W — P03 withdrawal

| State | Rows | Content |
|---|---:|---|
| PRE | 2 | REAL `FIX-ID-P03` Place + SYNTHETIC historical provider/reference Source Assertion |
| POST | 3 | PRE + SYNTHETIC withdrawn-reference Resolution Link |

The withdrawal link `FIX-RES-I-P03-WITHDRAWN-REF` retains the historical reference, points to P03, records `historically_traceable=true`, `valid_for_new_use=false`, `place_identity_unchanged=true`, `place_lifecycle_unchanged=true`, `replacement=none`, `correction=false` and `deletion=false`. There are zero Succession and zero Correction rows.

## Checker evidence

- `closure/raw-checker-output.txt`: exit code 0, `PASS: no supported mechanical failure found`.
- `withdrawal/raw-checker-output.txt`: exit code 0, `PASS: no supported mechanical failure found`.
- Both fixtures contain byte-identical copies of the original scenario sheet, which still lists P12/P13.

## Operator boundaries

No business closure, tenant closure, rebranding, correction, deletion, replacement reference, Current DAEN Representation, successor Place, production lifecycle enum or resolver/API behavior was created. No J execution or semantic Scenario I verdict was made.
