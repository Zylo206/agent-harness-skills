#!/usr/bin/env python3
"""Minimal structured-context-compressor runtime."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TECH_KEYWORDS = (
    "json",
    "schema",
    "runtime",
    "python",
    "test",
    "tests",
    "conversation",
    "context",
    "snapshot",
    "handoff",
    "resume",
    "skill",
    "bundle",
)

COMPLETION_KEYWORDS = (
    "已完成",
    "implemented",
    "added",
    "created",
    "updated",
)

CONSTRAINT_KEYWORDS = (
    "不要",
    "不需要",
    "必须",
    "保持",
    "只",
    "不改",
    "do not",
    "must",
    "only",
    "keep",
)

NEGATIVE_CONSTRAINT_KEYWORDS = (
    "不要",
    "不需要",
    "不改",
    "do not",
    "must not",
    "don't",
    "no ",
    "avoid",
    "forbid",
)


def load_input(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"input file not found: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to read input file: {path}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in input file: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("input JSON must be an object")
    return data


def normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str):
            stripped = item.strip()
            if stripped:
                result.append(stripped)
    return result


def normalize_clause_list(value: Any) -> list[str]:
    items = normalize_string_list(value)
    result: list[str] = []
    for item in items:
        result.extend(sentence_candidates(item) or [item])
    return dedupe(result)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in values:
        key = item.strip()
        if key and key.lower() not in seen:
            seen.add(key.lower())
            result.append(key)
    return result


def first_user_message(conversation: list[Any]) -> str:
    for message in conversation:
        if isinstance(message, dict) and str(message.get("role", "")).lower() == "user":
            content = message.get("content", "")
            if isinstance(content, str) and content.strip():
                return content.strip()
    for message in conversation:
        if isinstance(message, dict):
            content = message.get("content", "")
            if isinstance(content, str) and content.strip():
                return content.strip()
    return ""


def sentence_candidates(text: str) -> list[str]:
    parts = re.split(r"[。！？\n]+", text)
    return [part.strip() for part in parts if part.strip()]


def extract_keyword_lines(text: str, keywords: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    matches: list[str] = []
    for sentence in sentence_candidates(text):
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in keywords):
            matches.append(sentence)
    if not matches and any(keyword in lowered for keyword in keywords):
        stripped = text.strip()
        if stripped:
            matches.append(stripped)
    return matches


def looks_like_negative_constraint(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in NEGATIVE_CONSTRAINT_KEYWORDS)


def extract_user_constraints(conversation: list[Any]) -> list[str]:
    found: list[str] = []
    for message in conversation:
        if not isinstance(message, dict):
            continue
        role = str(message.get("role", "")).lower()
        if role not in {"user", "system"}:
            continue
        content = message.get("content", "")
        if not isinstance(content, str) or not content.strip():
            continue
        if any(keyword.lower() in content.lower() for keyword in CONSTRAINT_KEYWORDS):
            found.extend(extract_keyword_lines(content, CONSTRAINT_KEYWORDS))
    return dedupe(found)


def extract_completed_work(conversation: list[Any]) -> list[str]:
    found: list[str] = []
    for message in conversation:
        if not isinstance(message, dict):
            continue
        if str(message.get("role", "")).lower() != "assistant":
            continue
        content = message.get("content", "")
        if not isinstance(content, str) or not content.strip():
            continue
        if any(keyword.lower() in content.lower() for keyword in COMPLETION_KEYWORDS):
            found.extend(extract_keyword_lines(content, COMPLETION_KEYWORDS))
    return dedupe(found)


def extract_technical_context(conversation: list[Any]) -> list[str]:
    found: list[str] = []
    for message in conversation:
        if not isinstance(message, dict):
            continue
        content = message.get("content", "")
        if not isinstance(content, str) or not content.strip():
            continue
        for keyword in TECH_KEYWORDS:
            if keyword in content.lower():
                found.append(keyword)
    return dedupe(found)


def format_artifact(artifact: dict[str, Any]) -> str:
    path = str(artifact.get("path", "")).strip()
    kind = str(artifact.get("type", "")).strip()
    summary = str(artifact.get("summary", "")).strip()
    pieces = [piece for piece in [path, kind] if piece]
    prefix = " / ".join(pieces)
    if summary and prefix:
        return f"{prefix}: {summary}"
    if summary:
        return summary
    return prefix


def build_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    conversation = payload.get("conversation")
    if not isinstance(conversation, list) or not conversation:
        raise ValueError("conversation is required and must be a non-empty array")

    task_goal = str(payload.get("task_goal", "") or "").strip()
    changed_files = normalize_string_list(payload.get("changed_files"))
    failed_attempts = normalize_string_list(payload.get("failed_attempts"))
    user_constraints = normalize_clause_list(payload.get("user_constraints"))
    pending_tasks = normalize_string_list(payload.get("pending_tasks"))
    current_state_input = str(payload.get("current_state", "") or "").strip()
    artifacts_value = payload.get("artifacts")
    artifacts: list[str] = []
    if isinstance(artifacts_value, list):
        for artifact in artifacts_value:
            if isinstance(artifact, dict):
                formatted = format_artifact(artifact)
                if formatted:
                    artifacts.append(formatted)

    primary_request = task_goal or first_user_message(conversation)

    extracted_constraints = extract_user_constraints(conversation)
    user_constraints = dedupe(user_constraints + extracted_constraints)

    if not failed_attempts:
        for message in conversation:
            if not isinstance(message, dict):
                continue
            content = message.get("content", "")
            if not isinstance(content, str) or not content.strip():
                continue
            if any(keyword in content.lower() for keyword in ("failed", "error", "exception", "失败")):
                failed_attempts.extend(extract_keyword_lines(content, ("failed", "error", "exception", "失败")))
    failed_attempts = dedupe(failed_attempts)

    do_not_repeat_sources: list[str] = []
    do_not_repeat_sources.extend(failed_attempts)
    for constraint in user_constraints:
        if looks_like_negative_constraint(constraint) or "only" in constraint.lower():
            do_not_repeat_sources.append(constraint)
        elif any(keyword in constraint.lower() for keyword in ("modify source", "change other skill", "other skill")):
            do_not_repeat_sources.append(constraint)
    do_not_repeat = dedupe(do_not_repeat_sources)

    technical_context = extract_technical_context(conversation)
    files_and_artifacts = dedupe(changed_files + artifacts)
    completed_work = extract_completed_work(conversation)

    if current_state_input:
        current_state = current_state_input
    elif pending_tasks:
        current_state = "Work remains in progress with pending tasks identified."
    elif failed_attempts:
        current_state = "Snapshot is ready, but prior failed attempts should not be repeated."
    else:
        current_state = "Snapshot generated from the provided conversation."

    if pending_tasks:
        next_step = pending_tasks[0]
    else:
        next_step = "Review the snapshot and continue from the current_state."

    return {
        "primary_request": primary_request,
        "user_constraints": user_constraints,
        "technical_context": technical_context,
        "files_and_artifacts": files_and_artifacts,
        "completed_work": completed_work,
        "failed_attempts": failed_attempts,
        "do_not_repeat": do_not_repeat,
        "pending_tasks": pending_tasks,
        "current_state": current_state,
        "next_step": next_step,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the structured-context-compressor runtime.")
    parser.add_argument("input_path", help="Path to the input JSON file.")
    args = parser.parse_args()

    try:
        payload = load_input(Path(args.input_path))
        snapshot = build_snapshot(payload)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"error: unexpected runtime failure: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
