"""Disposable structural checker for the DAEN Geo Core M1 fixture medium.

VALIDATION TOOL ONLY.
NOT PRODUCTION CODE.
NOT AN API CONTRACT.
NOT A DATABASE SCHEMA.
NOT AN ARCHITECTURE PRECEDENT.
MUST NOT BE REUSED AS A PRODUCTION SERVICE OR LIBRARY.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

LEDGER_FIELDS = [
    "run_id", "step_id", "local_subject_label", "frozen_concept_involved",
    "free_text_statement", "provenance_reference", "quality_statement",
    "synthetic_flag", "supersedes_reference",
]
CONCEPTS = {
    "Place", "GeoID", "Source Assertion", "Current DAEN Representation",
    "Resolution Link", "Access Point", "Extent", "Correction", "Succession",
    "Provenance", "Quality", "Coordinate", "Address", "Containment",
}
LIFECYCLE_RE = re.compile(r"\blifecycle=([a-z_-]+)")
IDENTITY_RE = re.compile(r"\bidentity=([^;]+)")
RESOLUTION_RE = re.compile(r"\bresolution=([^;]+)")
REF_RE = re.compile(r"\bref=([^;]+)")


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(row for row in handle if not row.startswith("#"))
        if reader.fieldnames != LEDGER_FIELDS:
            raise ValueError("CHECKER ERROR: unexpected state-ledger header")
        return list(reader)


def row_key(row: dict[str, str]) -> str:
    return f"{row['run_id']}:{row['step_id']}"


def check_ledger(root: Path) -> list[tuple[str, str, str]]:
    rows = load_rows(root / "state-ledger.csv")
    failures: list[tuple[str, str, str]] = []
    subjects: dict[str, set[str]] = {}
    keys = {row_key(row) for row in rows}
    subject_labels = {row["local_subject_label"] for row in rows if row["local_subject_label"]}
    for row in rows:
        key = row_key(row)
        subject = row["local_subject_label"]
        identity = IDENTITY_RE.search(row["free_text_statement"])
        if identity:
            subjects.setdefault(subject, set()).add(identity.group(1).strip())
        lifecycle = LIFECYCLE_RE.search(row["free_text_statement"])
        if lifecycle and lifecycle.group(1) in {"merge", "split", "closure", "withdrawal"} and not RESOLUTION_RE.search(row["free_text_statement"]):
            failures.append(("M1-M02", "DOMAIN STRUCTURAL FAILURE", key))
        if row["provenance_reference"].strip() == "":
            failures.append(("M1-M03", "DOMAIN STRUCTURAL FAILURE", key))
        if "current_representation=true" in row["free_text_statement"] and row["quality_statement"].strip() == "":
            failures.append(("M1-M04", "DOMAIN STRUCTURAL FAILURE", key))
        if row["supersedes_reference"].strip() and row["supersedes_reference"] not in keys:
            failures.append(("M1-M05", "DOMAIN STRUCTURAL FAILURE", key))
        if row["frozen_concept_involved"] not in CONCEPTS:
            failures.append(("M1-M06", "DOMAIN STRUCTURAL FAILURE", key))
        for reference in REF_RE.findall(row["free_text_statement"]):
            if reference.strip() not in subject_labels:
                failures.append(("M1-M07", "DOMAIN STRUCTURAL FAILURE", key))
    for subject, identities in subjects.items():
        if len(identities) > 1:
            failures.append(("M1-M01", "DOMAIN STRUCTURAL FAILURE", subject))
    return failures


def check_append_only(root: Path) -> list[tuple[str, str, str]]:
    previous = root / "state-ledger-previous.csv"
    if not previous.exists():
        return []
    old_rows = {row_key(row): row for row in load_rows(previous)}
    new_rows = {row_key(row): row for row in load_rows(root / "state-ledger.csv")}
    return [("VM-I01", "VALIDATION MEDIUM FAILURE", old_key)
            for old_key, old_row in old_rows.items()
            if old_key not in new_rows or new_rows[old_key] != old_row]


def check_scenario_sheet(root: Path, required: bool = True) -> list[tuple[str, str, str]]:
    path = root / "scenario-sheet.md"
    if not path.exists():
        return [("VM-I02", "VALIDATION MEDIUM FAILURE", "scenario-sheet.md")] if required else []
    text = path.read_text(encoding="utf-8")
    failures = []
    for letter in "ABCDEFGHIJ":
        if not re.search(rf"^## {letter} —", text, re.MULTILINE):
            failures.append(("VM-I02", "VALIDATION MEDIUM FAILURE", letter))
    if text.count("- **Expected outcome:**") != 10:
        failures.append(("VM-I02", "VALIDATION MEDIUM FAILURE", "expected outcomes"))
    if re.search(r"- \*\*Actual result:\*\*[ \t]*\S", text) or re.search(r"- \*\*PASS / FAIL / INEXPRESSIBLE:\*\*[ \t]*\S", text):
        failures.append(("VM-I02", "VALIDATION MEDIUM FAILURE", "pre-execution result fields"))
    return failures


def run_fixture(root: Path, require_scenarios: bool = True) -> list[tuple[str, str, str]]:
    try:
        return check_ledger(root) + check_append_only(root) + check_scenario_sheet(root, require_scenarios)
    except (OSError, ValueError, KeyError) as exc:
        return [("CHECKER ERROR", "CHECKER ERROR", str(exc))]


def print_failures(failures: list[tuple[str, str, str]]) -> None:
    for rule, category, detail in failures:
        print(f"{category}: {rule}: {detail}")
    if failures:
        print("MANUAL REVIEW REQUIRED: structural output does not decide domain meaning")


def self_test(root: Path) -> int:
    good_failures = run_fixture(root / "known-good")
    print(f"known-good: {'PASS' if not good_failures else 'FAIL'}")
    print_failures(good_failures)
    failed = bool(good_failures)
    for fixture in sorted((root / "known-bad").iterdir()):
        if not fixture.is_dir():
            continue
        expected = (fixture / "expected-rule.txt").read_text(encoding="utf-8").strip()
        failures = run_fixture(fixture, require_scenarios=False)
        detected = {rule for rule, _, _ in failures}
        result = "PASS" if expected in detected else "FAIL"
        print(f"{fixture.name}: expected={expected} detected={','.join(sorted(detected)) or 'none'} result={result}")
        print_failures(failures)
        failed |= result == "FAIL"
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Disposable M1 structural checker")
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test(Path(__file__).parent)
    if not args.fixture:
        parser.error("provide --fixture or --self-test")
    failures = run_fixture(args.fixture)
    if failures:
        print_failures(failures)
        return 1
    print("PASS: no supported mechanical failure found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
