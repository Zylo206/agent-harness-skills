#!/usr/bin/env python3
"""Batch-run skill cases and compare key expected fields."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def format_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def is_non_empty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, dict):
        return len(value) > 0
    return value is not None


def resolve_path(value: Any, path_expr: str) -> Any:
    if not path_expr:
        return value
    current = value
    for part in path_expr.split("."):
        if not isinstance(current, dict) or part not in current:
            return _MISSING
        current = current[part]
    return current


_MISSING = object()


def compare_expected(
    expected: Any,
    actual: Any,
    root: Any | None = None,
    path: str = "",
) -> list[tuple[str, Any, Any, str]]:
    if root is None:
        root = actual
    mismatches: list[tuple[str, Any, Any, str]] = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [(path or "$", expected, actual, "type")]
        for key, value in expected.items():
            full_path = f"{path}.{key}" if path else key

            if isinstance(value, dict):
                nested_actual = resolve_path(root, full_path)
                if nested_actual is _MISSING:
                    mismatches.append((full_path, value, None, "missing"))
                elif not isinstance(nested_actual, dict):
                    mismatches.append((full_path, value, nested_actual, "type"))
                else:
                    mismatches.extend(compare_expected(value, nested_actual, root, full_path))
                continue

            if key.endswith("_non_empty") and value is True:
                field_path = full_path[: -len("_non_empty")]
                actual_field = resolve_path(root, field_path)
                if actual_field is _MISSING:
                    mismatches.append((field_path, True, None, "missing"))
                elif not is_non_empty(actual_field):
                    mismatches.append((field_path, True, actual_field, "non_empty"))
                continue

            if key.endswith("_min") and isinstance(value, (int, float)):
                field_path = full_path[: -len("_min")]
                actual_field = resolve_path(root, field_path)
                if actual_field is _MISSING:
                    mismatches.append((field_path, value, None, "missing"))
                elif not isinstance(actual_field, (int, float)):
                    mismatches.append((field_path, value, actual_field, "type"))
                elif actual_field < value:
                    mismatches.append((field_path, value, actual_field, "min"))
                continue

            actual_field = resolve_path(root, full_path)
            if actual_field is _MISSING:
                mismatches.append((full_path, value, None, "missing"))
                continue
            if isinstance(value, list):
                if not isinstance(actual_field, list):
                    mismatches.append((full_path, value, actual_field, "type"))
                elif actual_field != value:
                    mismatches.append((full_path, value, actual_field, "value"))
                continue
            if isinstance(value, (str, int, float, bool)) or value is None:
                if actual_field != value:
                    mismatches.append((full_path, value, actual_field, "value"))
                continue
            mismatches.extend(compare_expected(value, actual_field, root, full_path))
        return mismatches

    if isinstance(expected, list):
        if not isinstance(actual, list):
            return [(path or "$", expected, actual, "type")]
        if expected != actual:
            return [(path or "$", expected, actual, "value")]
        return mismatches

    if expected != actual:
        return [(path or "$", expected, actual, "value")]
    return mismatches


def case_stem(case_path: Path) -> str:
    stem = case_path.name
    if stem.endswith(".input.json"):
        return stem[: -len(".input.json")]
    return case_path.stem


def run_case(repo_root: Path, skill_dir: Path, case_path: Path) -> tuple[bool, str]:
    runner = repo_root / "tools" / "skill_runner.py"
    proc = subprocess.run(
        [sys.executable, str(runner), str(skill_dir), str(case_path)],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or f"runner exited with {proc.returncode}"
        return False, message
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return False, f"invalid JSON output from skill_runner: {exc}"
    return True, json.dumps(payload, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a skill bundle benchmark suite.")
    parser.add_argument("skill_dir", help="Path to the skill directory.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    repo_root = skill_dir.parent.parent
    cases_dir = skill_dir / "tests" / "cases"
    expected_dir = skill_dir / "tests" / "expected"

    if not cases_dir.exists():
        eprint(f"error: cases directory not found: {cases_dir}")
        return 1

    case_paths = sorted(cases_dir.glob("*.input.json"))
    if not case_paths:
        eprint(f"warning: no input cases found in {cases_dir}")
        return 0

    passed = 0
    failed = 0

    for case_path in case_paths:
        name = case_stem(case_path)
        expected_path = expected_dir / case_path.name.replace(".input.json", ".expected.json")
        ok, output_or_error = run_case(repo_root, skill_dir, case_path)
        if not ok:
            failed += 1
            print(f"[FAIL] {name}")
            eprint(f"  {output_or_error}")
            continue

        actual = json.loads(output_or_error)
        if not expected_path.exists():
            failed += 1
            print(f"[FAIL] {name}")
            eprint(f"warning: expected file missing: {expected_path}")
            continue

        try:
            expected = load_json(expected_path)
        except Exception as exc:
            failed += 1
            print(f"[FAIL] {name}")
            eprint(f"warning: could not read expected file {expected_path}: {exc}")
            continue

        mismatches = compare_expected(expected, actual)
        if mismatches:
            failed += 1
            print(f"[FAIL] {name}")
            for path, expected_value, actual_value, kind in mismatches:
                if kind == "non_empty":
                    eprint(f"  expected {path} to be non-empty, got {format_value(actual_value)}")
                elif kind == "missing":
                    eprint(f"  expected {path}={format_value(expected_value)}, got <missing>")
                elif kind == "type":
                    eprint(
                        f"  expected {path}={format_value(expected_value)}, got {format_value(actual_value)}"
                    )
                else:
                    eprint(
                        f"  expected {path}={format_value(expected_value)}, got {format_value(actual_value)}"
                    )
            continue

        passed += 1
        print(f"[PASS] {name}")

    total = passed + failed
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
