# RUN-H-01 — Operator Execution Record

RAW OPERATOR EVIDENCE — SEMANTIC VERDICT RESERVED FOR INDEPENDENT REVIEW.

## Run identity and authority

- Run ID: `RUN-H-01`
- Role: M1 Data Operator — Codex
- Historical registered targets: P10, P11
- Effective targets under approved target erratum: P17, P18
- Target erratum commit: `6b572bc5ba03f275d25a21f727515128326a7d73`
- Input freeze commit: `a0424803269f11805a46f5d2453b0c3fba90c44a`
- Fixture handles are local validation stand-ins, not production GeoID formats.

## Capacity and isolation

The effective corpus interpretation is the original 20 slots plus three distinct resulting identities: P17 mis-conflation separation adds `FIX-ID-H-P17-B`; P18 true division adds `FIX-ID-H-P18-A` and `FIX-ID-H-P18-B`. The executed local capacity is therefore 23 distinct fixture identities/records where applicable. Mis-conflation (M) and true-division (T) are isolated alternative subcases, not sequential events and not concatenated histories.

## Mis-conflation subcase (M)

P17 Locus A retains `FIX-ID-P17`. The prior P17 Locus B assertion remains in history and is explicitly superseded by a new B-locus assertion attached to `FIX-ID-H-P17-B`.

| Original identity | True original locus | New identity | Separated locus | Original retained | New identity distinct |
|---|---|---|---|---|---|
| FIX-ID-P17 | P17 Locus A | FIX-ID-H-P17-B | P17 Locus B | yes | yes |

| Historical B assertion | New B assertion | Supersedes |
|---|---|---|
| `FIX-ID-P17-SA-L2-OLD` / `SYN-H-P17-L2-OLD` | `FIX-ID-H-P17-B-SA-L2` / `SYN-H-P17-L2-NEW` | `RUN-H-01-M:PRE-P17-SA-L2-OLD` |

A Resolution Link `FIX-RES-H-MIS-P17-B` records separation, original identity continuation, new identity creation and history preservation. No Succession row is created in this subcase.

## True-division subcase (T)

Historical parent `FIX-ID-P18` remains resolvable. Children `FIX-ID-H-P18-A` and `FIX-ID-H-P18-B` are new identities and neither inherits the parent identity.

| Historical parent | Child A | Child B | Parent inherited by child? | Historical resolvable |
|---|---|---|---|---|
| FIX-ID-P18 | FIX-ID-H-P18-A | FIX-ID-H-P18-B | no | yes |

Resolution Links: `FIX-RES-H-DIV-P18-A`, `FIX-RES-H-DIV-P18-B`.
Succession handles: `FIX-SUCC-H-DIV-P18-A`, `FIX-SUCC-H-DIV-P18-B`.

## Operator actions

1. Materialized only the frozen synthetic P17/P18 initial state.
2. Created isolated M and T pre-run snapshots.
3. Applied only the approved split subcase mutations.
4. Preserved prior rows append-only and retained provenance and explicit `unknown` Quality.
5. Ran the unchanged disposable checker separately for both fixtures and saved raw output unedited.
6. Did not alter the frozen scenario sheet, corpus, Domain Model or checker.

## Evidence paths

- `misconflation/pre-run-state.csv`
- `misconflation/post-run-state.csv`
- `misconflation/checker-fixture/state-ledger.csv`
- `misconflation/raw-checker-output.txt`
- `true-division/pre-run-state.csv`
- `true-division/post-run-state.csv`
- `true-division/checker-fixture/state-ledger.csv`
- `true-division/raw-checker-output.txt`

No semantic verdict is recorded. No production GeoID is created or proposed.
