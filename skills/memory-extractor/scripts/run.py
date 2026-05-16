#!/usr/bin/env python3
"""Minimal memory-extractor runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


PREFERENCE_HINTS = (
    "我更喜欢",
    "以后都",
    "从现在开始",
    "以后不要",
    "记住",
    "remember that",
    "from now on",
    "i prefer",
    "do not",
    "always",
    "优先",
)
WORKFLOW_HINTS = (
    "prompt",
    "claude code",
    "workflow",
    "format",
    "回答",
    "提示词",
    "可直接复制",
)
PROJECT_HINTS = (
    "我的项目",
    "我正在做",
    "项目叫",
    "技术栈",
    "repository",
    "project",
    "stack",
)
CONSTRAINT_HINTS = (
    "必须使用",
    "不能使用",
    "不要引入",
    "保持兼容",
    "must use",
    "do not introduce",
    "keep compatible",
)
TEMPORARY_HINTS = (
    "现在正在",
    "刚刚",
    "这一步",
    "临时",
    "today",
    "currently",
    "right now",
)
SENSITIVE_HINTS = (
    "medical",
    "diagnosis",
    "religion",
    "political affiliation",
    "exact address",
    "身份证",
    "住址",
    "宗教",
    "政治立场",
    "疾病",
    "诊断",
)
FEEDBACK_HINTS = (
    "feedback",
    "too verbose",
    "too slow",
    "too much",
    "not helpful",
    "improve response",
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


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def canonical_key(memory_type: str, content: str) -> tuple[str, str]:
    return memory_type, normalize_text(content).lower()


def stable_id(memory_type: str, content: str) -> str:
    digest = hashlib.sha1(f"{memory_type}\0{normalize_text(content).lower()}".encode("utf-8")).hexdigest()
    return f"{memory_type}-{digest[:12]}"


def normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str):
            stripped = normalize_text(item)
            if stripped:
                result.append(stripped)
    return result


def normalize_memories(value: Any, current_date: str, default_source: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    result: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, dict):
            continue
        memory_type = str(raw.get("type", "rejected")).strip() or "rejected"
        content = normalize_text(str(raw.get("content", "") or ""))
        if not content:
            continue
        item = {
            "id": str(raw.get("id") or stable_id(memory_type, content)),
            "type": memory_type,
            "content": content,
            "source": str(raw.get("source") or default_source),
            "confidence": float(raw.get("confidence", 0.5) or 0.5),
            "lifespan": str(raw.get("lifespan", "medium_term") or "medium_term"),
            "status": str(raw.get("status", "active") or "active"),
            "tags": normalize_string_list(raw.get("tags")),
            "created_at": raw.get("created_at") if raw.get("created_at") is not None else current_date,
            "updated_at": raw.get("updated_at") if raw.get("updated_at") is not None else current_date,
            "expires_at": raw.get("expires_at"),
            "reason": str(raw.get("reason", "") or ""),
        }
        result.append(item)
    return result


def new_memory_item(
    memory_type: str,
    content: str,
    source: str,
    confidence: float,
    lifespan: str,
    status: str,
    tags: list[str],
    reason: str,
    current_date: str,
    expires_at: Any = None,
) -> dict[str, Any]:
    return {
        "id": stable_id(memory_type, content),
        "type": memory_type,
        "content": normalize_text(content),
        "source": source,
        "confidence": round(max(0.0, min(1.0, confidence)), 3),
        "lifespan": lifespan,
        "status": status,
        "tags": tags,
        "created_at": current_date,
        "updated_at": current_date,
        "expires_at": expires_at,
        "reason": reason,
    }


def contains_any(text: str, needles: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(needle.lower() in lower for needle in needles)


def sentence_candidates(text: str) -> list[str]:
    parts = re.split(r"[。！？!?;\n]+", text)
    return [normalize_text(part) for part in parts if normalize_text(part)]


def extract_from_text(text: str, source: str, policy: dict[str, Any], current_date: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    candidates: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    notes: list[str] = []

    allow_sensitive = bool(policy.get("allow_sensitive_memory", False))
    prefer_long_term = bool(policy.get("prefer_long_term", True))
    reject_temporary = bool(policy.get("reject_temporary_state", True))

    for sentence in sentence_candidates(text) or [normalize_text(text)]:
        if not sentence:
            continue
        lower = sentence.lower()
        if contains_any(lower, SENSITIVE_HINTS) and not allow_sensitive:
            rejected.append(
                new_memory_item(
                    "rejected",
                    sentence,
                    source,
                    0.1,
                    "short_term",
                    "rejected",
                    ["sensitive", "policy"],
                    "Rejected due to sensitive memory policy.",
                    current_date,
                )
            )
            notes.append("Sensitive memory rejected by policy.")
            continue
        if contains_any(lower, TEMPORARY_HINTS):
            if reject_temporary:
                rejected.append(
                    new_memory_item(
                        "temporary_state",
                        sentence,
                        source,
                        0.45,
                        "short_term",
                        "rejected",
                        ["temporary", "policy"],
                        "Rejected as temporary state due to extraction policy.",
                        current_date,
                    )
                )
                notes.append("Temporary state rejected by policy.")
                continue

        extracted_types: list[tuple[str, str, float, list[str], str]] = []
        if contains_any(lower, PREFERENCE_HINTS):
            memory_type = "workflow_preference" if contains_any(lower, WORKFLOW_HINTS) else "user_preference"
            lifespan = "long_term" if prefer_long_term else "medium_term"
            extracted_types.append(
                (
                    memory_type,
                    lifespan,
                    0.92 if memory_type == "workflow_preference" else 0.9,
                    ["preference", "workflow"] if memory_type == "workflow_preference" else ["preference"],
                    "Extracted explicit preference from conversation.",
                )
            )
        if contains_any(lower, PROJECT_HINTS):
            extracted_types.append(
                (
                    "project_context",
                    "long_term",
                    0.88,
                    ["project", "context"],
                    "Extracted project context from conversation.",
                )
            )
        if contains_any(lower, CONSTRAINT_HINTS):
            extracted_types.append(
                (
                    "technical_constraint",
                    "long_term",
                    0.9,
                    ["constraint", "technical"],
                    "Extracted technical constraint from conversation.",
                )
            )
        if contains_any(lower, FEEDBACK_HINTS):
            extracted_types.append(
                (
                    "feedback",
                    "medium_term",
                    0.7,
                    ["feedback"],
                    "Extracted feedback from conversation.",
                )
            )

        seen_types: set[str] = set()
        for memory_type, lifespan, confidence, tags, reason in extracted_types:
            if memory_type in seen_types:
                continue
            seen_types.add(memory_type)
            candidates.append(
                new_memory_item(
                    memory_type,
                    sentence,
                    source,
                    confidence,
                    lifespan,
                    "candidate",
                    tags,
                    reason,
                    current_date,
                )
            )

    return candidates, rejected, notes


def reject_duplicate(candidate: dict[str, Any], existing_index: dict[tuple[str, str], dict[str, Any]], current_date: str) -> dict[str, Any] | None:
    key = canonical_key(str(candidate["type"]), str(candidate["content"]))
    if key in existing_index:
        return new_memory_item(
            "rejected",
            candidate["content"],
            candidate["source"],
            0.4,
            "short_term",
            "rejected",
            ["duplicate", "validation"],
            "Rejected as a duplicate of an existing memory.",
            current_date,
        )
    return None


def build_output(payload: dict[str, Any]) -> dict[str, Any]:
    conversation = payload.get("conversation")
    if not isinstance(conversation, list) or not conversation:
        raise ValueError("conversation is required and must be a non-empty array")

    task_notes = normalize_string_list(payload.get("task_notes"))
    existing_memories = normalize_memories(payload.get("existing_memories"), str(payload.get("current_date", "") or ""), "existing_memory")
    policy = payload.get("extraction_policy") if isinstance(payload.get("extraction_policy"), dict) else {}
    current_date = normalize_text(str(payload.get("current_date", "") or ""))

    existing_index = {canonical_key(mem["type"], mem["content"]): mem for mem in existing_memories}
    candidates: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    notes: list[str] = []
    seen_candidate_keys: set[tuple[str, str]] = set()

    for message in conversation:
        if not isinstance(message, dict):
            continue
        if str(message.get("role", "")).lower() != "user":
            continue
        content = normalize_text(str(message.get("content", "") or ""))
        if not content:
            continue
        extracted_candidates, extracted_rejected, extracted_notes = extract_from_text(content, "conversation", policy, current_date)
        notes.extend(extracted_notes)
        for item in extracted_rejected:
            rejected.append(item)
        for item in extracted_candidates:
            key = canonical_key(item["type"], item["content"])
            if key in seen_candidate_keys:
                rejected.append(
                    new_memory_item(
                        "rejected",
                        item["content"],
                        item["source"],
                        0.4,
                        "short_term",
                        "rejected",
                        ["duplicate", "validation"],
                        "Rejected as a duplicate within the same extraction run.",
                        current_date,
                    )
                )
                continue
            duplicate = reject_duplicate(item, existing_index, current_date)
            if duplicate is not None:
                rejected.append(duplicate)
                continue
            seen_candidate_keys.add(key)
            candidates.append(item)

    for note in task_notes:
        extracted_candidates, extracted_rejected, extracted_notes = extract_from_text(note, "task_notes", policy, current_date)
        notes.extend(extracted_notes)
        rejected.extend(extracted_rejected)
        for item in extracted_candidates:
            key = canonical_key(item["type"], item["content"])
            if key in seen_candidate_keys:
                continue
            duplicate = reject_duplicate(item, existing_index, current_date)
            if duplicate is not None:
                rejected.append(duplicate)
                continue
            seen_candidate_keys.add(key)
            candidates.append(item)

    policy_notes = notes + [
        "Candidates are classified from conversation and task notes.",
        "Temporary states are rejected when policy enables it.",
        "Sensitive memory is rejected unless explicitly allowed.",
    ]

    return {
        "candidates": candidates,
        "rejected": rejected,
        "summary": {
            "extracted_count": len(candidates),
            "rejected_count": len(rejected),
            "policy_notes": list(dict.fromkeys(policy_notes)),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the memory-extractor runtime.")
    parser.add_argument("input_path", help="Path to the input JSON file.")
    args = parser.parse_args()

    try:
        payload = load_input(Path(args.input_path))
        output = build_output(payload)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"error: unexpected runtime failure: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
