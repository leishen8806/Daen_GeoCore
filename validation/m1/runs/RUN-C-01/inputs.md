# RUN-C-01 — Approved Scenario C Controlled Inputs

> PRE-EXECUTION INPUT RECORD — VALIDATION EVIDENCE ONLY. NOT A SPECIFICATION.

## Baseline and frozen scope

- **Baseline after Scenario B acceptance:** `e26be48851892a37f222d37569acfe1f3ddc68d2`
- **Branch:** `phase/04-m1-execution`
- **Run:** `RUN-C-01`
- **Role:** M1 Data Operator — Codex
- **Scenario:** C — Current DAEN Representation Change
- **Targets:** `P04`, `P14`, `P16` only
- **Frozen action:** Change the Current DAEN Representation in response to a correction or stronger evidence.
- **Frozen expected outcome:** Current representation changes without destructive overwrite; prior material state remains traceable.

This is a predeclared mock-source spelling-correction test. It does not test source ranking or the full Correction workflow. P04's general-reference coordinate and entrance coordinate remain untouched and are not substituted for one another. P16's duplicate-of-P15 background does not authorize a merge.

## Exact approved synthetic assertion pairs

All six assertions are `SYNTHETIC`, have Quality `unknown`, and come from one mock source per target. The OLD and REVISED values are not independent corroboration.

| Target | Mock origin | OLD assertion | REVISED assertion | Evidence labels |
|---|---|---|---|---|
| P04 | `SYN-C-P04` | `AEON Mall Phnom Pen` | `AEON Mall Phnom Penh` | `SYN-C-P04-OLD`, `SYN-C-P04-REVISED` |
| P14 | `SYN-C-P14` | `AEON Mall Cambodia Parking Twer building` | `AEON Mall Cambodia Parking Tower building` | `SYN-C-P14-OLD`, `SYN-C-P14-REVISED` |
| P16 | `SYN-C-P16` | `SYNTHETIC P15/P16 Test Premies` | `SYNTHETIC P15/P16 Test Premises` | `SYN-C-P16-OLD`, `SYN-C-P16-REVISED` |

For every pair:

- target Place remains unchanged;
- fact = `name`;
- purpose = `display-name`;
- language = `en`;
- OLD fixture instant = `TEST-C0`;
- REVISED fixture instant = `TEST-C1`;
- Quality = `unknown`;
- classification = `SYNTHETIC`;
- initial selection points to OLD;
- replacement selection points to REVISED;
- replacement selection supersedes the prior selection for the same target.

Exact rationale for every pair:

> The OLD display-name spelling is a deliberately introduced transcription error for this fixture. The REVISED spelling is supplied as its correction. Both statements concern the same unchanged premises and the same English display-name purpose. No physical relocation, ownership change, source-trust comparison or scope change occurs.

## Fixture and selection references

| Target handle | OLD assertion | Initial selection | REVISED assertion | Replacement selection |
|---|---|---|---|---|
| `FIX-ID-P04` | `FIX-ID-P04-SA-OLD` | `FIX-ID-P04-SEL-OLD` | `FIX-ID-P04-SA-REVISED` | `FIX-ID-P04-SEL-REVISED` |
| `FIX-ID-P14` | `FIX-ID-P14-SA-OLD` | `FIX-ID-P14-SEL-OLD` | `FIX-ID-P14-SA-REVISED` | `FIX-ID-P14-SEL-REVISED` |
| `FIX-ID-P16` | `FIX-ID-P16-SA-OLD` | `FIX-ID-P16-SEL-OLD` | `FIX-ID-P16-SA-REVISED` | `FIX-ID-P16-SEL-REVISED` |

These handles are validation stand-ins, not production GeoIDs. P04 and P14 remain REAL physical corpus Places; P16 remains a SYNTHETIC corpus case. All controlled initial and replacement selections are `SYNTHETIC` and are explicitly authorized for this experiment, not inferred from public evidence.

## Attribution

- **Assertion provenance:** mock-source labels `SYN-C-P04`, `SYN-C-P14` and `SYN-C-P16`, with `-OLD` and `-REVISED` evidence labels.
- **Selection attribution:** Codex, run `RUN-C-01`, and the exact selection step recorded in `operator-execution.md`.
- Provenance and selector attribution are distinct. Existing CSV fields and Markdown references are sufficient; no new entity, column or parser syntax is introduced.

## Initial and final identity boundary

- **Before:** accepted Place handles are `FIX-ID-P04`, `FIX-ID-P14` and `FIX-ID-P16`; each has one OLD Source Assertion and one controlled initial Current DAEN Representation selection.
- **After:** the accepted Place set and all three Place identities are unchanged. Each target retains OLD and REVISED Source Assertions, retains the historical OLD selection row, and has a same-scope REVISED selection whose supersession target is the OLD selection.
- P16 keeps its intended synthetic locus associated with the duplicate-of-P15 background; P15 is not materialized and no merge is performed.

## H20 and governing clauses

- Domain Model §4.3: Current DAEN Representation is selected from relevant Source Assertions for a defined scope and is not absolute physical truth.
- Domain Model §10: Source Assertions preserve what a source said about a Place.
- Domain Model §11: selections are attributable and retain enough history to explain material changes.
- Domain Model §11.1 / H20: ordinary supersession requires the same Place, same represented fact or purpose, and explicitly equivalent scope; supporting Source Assertions remain retained.
- Domain Model §17: persisted Source Assertions, representations and material corrections must be attributable.
- Domain Model §19: correction/supersession does not silently erase history.
- Domain Model §26: succession supports non-destructive history for representations.
- M1-B4: Current DAEN Representation can change without destructive overwrite.
- M1-B8: wrong facts can be superseded while preserving material history.
- M1-B9: Current DAEN Representations and identity decisions can be traced to source.
- M1-B10: evaluated or selected facts have explicit Quality; `unknown` is valid.

H20 is applied only to these same-scope English display-name selections. No cross-language or general cross-scope migration is tested.

## Required manual checks and limitations

- Selection supersession points to the prior selection, never to a Source Assertion or Place.
- Both selection ends explicitly show `fact=name`, `purpose=display-name`, `language=en`.
- OLD Source Assertions and OLD selection rows remain unchanged and retained.
- The effective value after the run is interpreted from the same-scope supersession relation; this is run interpretation, not a production algorithm.
- No coordinate-role substitution, source ranking, physical correction workflow, P16 merge, provider behavior or new research is included.
- The test does not prove automatic spelling correction or real-world name accuracy.
