#!/usr/bin/env python3
"""Run a skill runtime with optional schema validation."""

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
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def load_skill_spec(skill_dir: Path) -> dict[str, Any]:
    skill_path = skill_dir / "skill.yaml"
    if not skill_path.exists():
        raise FileNotFoundError(f"skill.yaml not found: {skill_path}")
    try:
        return json.loads(skill_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"skill.yaml must be JSON-compatible YAML for this runner: {skill_path}: {exc}"
        ) from exc


def validate_schema(schema_path: Path, payload: Any, label: str) -> None:
    try:
        import importlib.util

        if importlib.util.find_spec("jsonschema") is None:
            eprint(f"warning: jsonschema is not installed; skipping {label} validation.")
            return

        from jsonschema import validate
        from jsonschema.exceptions import ValidationError
    except Exception as exc:  # pragma: no cover - soft dependency fallback
        eprint(f"warning: could not load jsonschema; skipping {label} validation ({exc}).")
        return

    schema = load_json(schema_path)
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as exc:
        raise ValueError(f"{label} validation failed: {exc.message}") from exc


def run_runtime(runtime_path: Path, input_path: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(runtime_path), str(input_path)],
        cwd=str(runtime_path.parent.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        if proc.stderr.strip():
            eprint(proc.stderr.rstrip())
        raise RuntimeError(f"runtime exited with code {proc.returncode}")

    stdout = proc.stdout.strip()
    if not stdout:
        raise ValueError("runtime produced no JSON output")
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"runtime output is not valid JSON: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a skill bundle runtime.")
    parser.add_argument("skill_dir", help="Path to the skill directory.")
    parser.add_argument("input_json", help="Path to the input JSON file.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    input_path = Path(args.input_json).expanduser().resolve()

    try:
        skill = load_skill_spec(skill_dir)
        runtime_entry = skill["runtime"]["entry"]
        runtime_path = (skill_dir / runtime_entry).resolve()
        if not runtime_path.exists():
            raise FileNotFoundError(f"runtime entry not found: {runtime_path}")

        input_payload = load_json(input_path)
        validate_schema(skill_dir / "schemas" / "input.schema.json", input_payload, "input")
        output_payload = run_runtime(runtime_path, input_path)
        validate_schema(skill_dir / "schemas" / "output.schema.json", output_payload, "output")
    except (FileNotFoundError, ValueError, RuntimeError, KeyError) as exc:
        eprint(f"error: {exc}")
        return 1

    print(json.dumps(output_payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
