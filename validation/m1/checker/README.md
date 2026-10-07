# Disposable M1 Checker

> VALIDATION TOOL ONLY.  
> NOT PRODUCTION CODE.  
> NOT AN API CONTRACT.  
> NOT A DATABASE SCHEMA.  
> NOT AN ARCHITECTURE PRECEDENT.  
> MUST NOT BE REUSED AS A PRODUCTION SERVICE OR LIBRARY.

## Runtime

Python 3 standard library only (`python --version` detected Python 3.15.0a2). This runtime choice is disposable validation tooling, not a Phase 06 architecture decision.

## Usage

From the repository root:

```text
python validation/m1/checker/check_m1.py --fixture validation/m1/checker/known-good
python validation/m1/checker/check_m1.py --self-test
```

Exit codes are tool behavior only:

- `0` — no supported mechanical failure found
- `1` — supported validation failure found
- `2` — checker, runtime or input error

## Supported checks

Domain structural checks: M1-M01 through M1-M07.

Validation-medium checks: VM-I01 and VM-I02.

The checker does not execute M1, populate the corpus, make domain judgments, select a provider, or decide GO / ITERATE / RETURN. Manual review remains authoritative.

## Self-test

Self-test runs the synthetic known-good fixture and every executable known-bad fixture. Self-test results validate the checker only; they are not M1 execution results.
