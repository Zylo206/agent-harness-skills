#!/usr/bin/env python3
"""Run every engineered skill test suite in the repository."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def discover_skills(repo_root: Path) -> list[Path]:
    skills_dir = repo_root / "skills"
    return sorted(path.parent for path in skills_dir.glob("*/skill.yaml"))


def has_cases(skill_dir: Path) -> bool:
    cases_dir = skill_dir / "tests" / "cases"
    return cases_dir.exists() and any(cases_dir.glob("*.input.json"))


def run_skill_tests(repo_root: Path, skill_dir: Path) -> tuple[int, str, str]:
    runner = repo_root / "tools" / "run_skill_tests.py"
    proc = subprocess.run(
        [sys.executable, str(runner), str(skill_dir)],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all skill bundle test suites.")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Override the repository root. Defaults to the parent directory of this script.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else Path(__file__).resolve().parent.parent
    skill_dirs = discover_skills(repo_root)
    if not skill_dirs:
        eprint(f"error: no skills found under {repo_root / 'skills'}")
        return 1

    passed_skills = 0
    failed_skills = 0
    skipped_skills = 0

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        print(f"== {skill_name} ==")
        if not has_cases(skill_dir):
            skipped_skills += 1
            eprint(f"warning: no test cases found for {skill_name}")
            print()
            continue

        code, stdout, stderr = run_skill_tests(repo_root, skill_dir)
        if stdout:
            print(stdout, end="" if stdout.endswith("\n") else "\n")
        if stderr:
            print(stderr, file=sys.stderr, end="" if stderr.endswith("\n") else "\n")
        if code == 0:
            passed_skills += 1
        else:
            failed_skills += 1
        print()

    tested_skills = passed_skills + failed_skills
    print("Summary:")
    print(f"Skills discovered: {len(skill_dirs)}")
    print(f"Skills tested: {tested_skills}")
    print(f"Passed skills: {passed_skills}")
    print(f"Failed skills: {failed_skills}")
    print(f"Skipped skills: {skipped_skills}")
    return 0 if failed_skills == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
