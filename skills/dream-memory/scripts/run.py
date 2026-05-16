#!/usr/bin/env python3
"""Minimal dream-memory runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


LONG_TERM_TYPES = {
    "user_preference",
    "workflow_preference",
    "project_context",
    "technical_constraint",
    "reference",
}

NEGATION_HINTS = ("do not", "don't", "不要", "不能", "must not", "avoid", "never")
MUST_HINTS = ("must", "always", "必须", "need to")


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


def normalize_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str):
            stripped = normalize_text(item)
            if stripped:
                result.append(stripped)
    return result


def stable_id(memory_type: str, content: str) -> str:
    digest = hashlib.sha1(f"{memory_type}\0{normalize_text(content).lower()}".encode("utf-8")).hexdigest()
    return f"{memory_type}-{digest[:12]}"


def canonical_key(item: dict[str, Any]) -> tuple[str, str]:
    return str(item["type"]), normalize_text(str(item["content"])).lower()


def parse_date(value: Any) -> date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        try:
            return datetime.fromisoformat(text).date()
        except ValueError:
            return None


def normalize_memory_item(raw: Any, current_date: str, default_source: str) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    memory_type = str(raw.get("type", "rejected")).strip() or "rejected"
    content = normalize_text(str(raw.get("content", "") or ""))
    if not content:
        return None
    return {
        "id": str(raw.get("id") or stable_id(memory_type, content)),
        "type": memory_type,
        "content": content,
        "source": str(raw.get("source") or default_source),
        "confidence": float(raw.get("confidence", 0.5) or 0.5),
        "lifespan": str(raw.get("lifespan", "medium_term") or "medium_term"),
        "status": str(raw.get("status", "active") or "active"),
        "tags": normalize_list(raw.get("tags")),
        "created_at": raw.get("created_at") if raw.get("created_at") is not None else current_date,
        "updated_at": raw.get("updated_at") if raw.get("updated_at") is not None else current_date,
        "expires_at": raw.get("expires_at"),
        "reason": str(raw.get("reason", "") or ""),
    }


def normalize_memories(value: Any, current_date: str, default_source: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    result: list[dict[str, Any]] = []
    for raw in value:
        item = normalize_memory_item(raw, current_date, default_source)
        if item is not None:
            result.append(item)
    return result


def item_priority(item: dict[str, Any], source_rank: int) -> tuple[float, date, int]:
    confidence = float(item.get("confidence", 0.0) or 0.0)
    updated = parse_date(item.get("updated_at")) or parse_date(item.get("created_at")) or date.min
    return confidence, updated, source_rank


def is_duplicate_content(left: str, right: str) -> bool:
    a = normalize_text(left).lower()
    b = normalize_text(right).lower()
    if not a or not b:
        return False
    if ("prefer java" in a and "prefer python" in b) or ("prefer python" in a and "prefer java" in b):
        return False
    left_neg = any(hint in a for hint in NEGATION_HINTS)
    right_neg = any(hint in b for hint in NEGATION_HINTS)
    left_must = any(hint in a for hint in MUST_HINTS)
    right_must = any(hint in b for hint in MUST_HINTS)
    if (left_neg and right_must) or (right_neg and left_must):
        return False
    if a == b or a in b or b in a:
        return True
    return SequenceMatcher(None, a, b).ratio() >= 0.95


def cluster_memories(items: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    clusters: list[list[dict[str, Any]]] = []
    for item in items:
        placed = False
        for cluster in clusters:
            head = cluster[0]
            if str(head["type"]) == str(item["type"]) and is_duplicate_content(str(head["content"]), str(item["content"])):
                cluster.append(item)
                placed = True
                break
        if not placed:
            clusters.append([item])
    return clusters


def is_short_term_expired(item: dict[str, Any], current_date: date | None, expire_short_term: bool) -> bool:
    if str(item.get("status")) == "expired":
        return True
    expires_at = parse_date(item.get("expires_at"))
    if current_date is not None and expires_at is not None and expires_at < current_date:
        return True
    if not expire_short_term:
        return False
    if str(item.get("lifespan")) != "short_term":
        return False
    if str(item.get("type")) in LONG_TERM_TYPES:
        return False
    return True


def conflict_reason(left: dict[str, Any], right: dict[str, Any]) -> str | None:
    left_text = str(left.get("content", "")).lower()
    right_text = str(right.get("content", "")).lower()
    if "prefer java" in left_text and "prefer python" in right_text:
        return "Conflicting preference between Java and Python."
    if "prefer python" in left_text and "prefer java" in right_text:
        return "Conflicting preference between Java and Python."
    left_neg = any(hint in left_text for hint in NEGATION_HINTS)
    right_neg = any(hint in right_text for hint in NEGATION_HINTS)
    left_must = any(hint in left_text for hint in MUST_HINTS)
    right_must = any(hint in right_text for hint in MUST_HINTS)
    if (left_neg and right_must) or (right_neg and left_must):
        return "Conflicting negation and obligation detected."
    return None


def matches_query(item: dict[str, Any], query: str) -> bool:
    q = normalize_text(query).lower()
    if not q:
        return False
    haystack = " ".join([str(item.get("content", "")), " ".join(normalize_list(item.get("tags")))]).lower()
    tokens = [token for token in re.split(r"[\s,.;:!?/\\]+", q) if token]
    return any(token in haystack for token in tokens) or q in haystack


def build_output(payload: dict[str, Any]) -> dict[str, Any]:
    existing_raw = payload.get("existing_memories")
    candidate_raw = payload.get("memory_candidates")
    if not isinstance(existing_raw, list):
        raise ValueError("existing_memories is required and must be an array")
    if not isinstance(candidate_raw, list):
        raise ValueError("memory_candidates is required and must be an array")

    current_date_text = normalize_text(str(payload.get("current_date", "") or ""))
    current_date = parse_date(current_date_text)
    merge_policy = payload.get("merge_policy") if isinstance(payload.get("merge_policy"), dict) else {}
    merge_duplicates = bool(merge_policy.get("merge_duplicates", True))
    expire_short_term = bool(merge_policy.get("expire_short_term", True))
    detect_conflicts = bool(merge_policy.get("detect_conflicts", True))
    retrieval_query = normalize_text(str(payload.get("retrieval_query", "") or ""))

    existing_memories = normalize_memories(existing_raw, current_date_text, "existing_memory")
    candidate_memories = normalize_memories(candidate_raw, current_date_text, "memory_candidate")
    working_items = existing_memories + candidate_memories

    active_memories: list[dict[str, Any]] = []
    merged_memories: list[dict[str, Any]] = []
    expired_memories: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []

    if merge_duplicates:
        for cluster in cluster_memories([item for item in working_items if str(item.get("status")) != "rejected"]):
            if not cluster:
                continue
            winner_source = max(
                cluster,
                key=lambda item: item_priority(item, 1 if str(item.get("source")) == "existing_memory" else 0),
            )
            winner = dict(winner_source)
            winner_id = str(winner_source["id"])
            for item in cluster:
                if str(item.get("id")) == winner_id:
                    continue
                merged_copy = dict(item)
                merged_copy["reason"] = merged_copy.get("reason") or f"Merged into {winner['id']} due to duplicate content."
                merged_memories.append(merged_copy)
            active_memories.append(winner)
    else:
        active_memories = [item for item in working_items if str(item.get("status")) != "rejected"]

    deduped_active: list[dict[str, Any]] = []
    for item in active_memories:
        if is_short_term_expired(item, current_date, expire_short_term):
            expired_copy = dict(item)
            expired_copy["status"] = "expired"
            expired_copy["reason"] = expired_copy.get("reason") or "Expired by lifecycle policy."
            expired_memories.append(expired_copy)
            continue
        if str(item.get("status")) == "rejected":
            continue
        active_copy = dict(item)
        active_copy["status"] = "active"
        deduped_active.append(active_copy)

    active_memories = deduped_active

    if detect_conflicts:
        for index, left in enumerate(active_memories):
            for right in active_memories[index + 1 :]:
                if str(left.get("type")) != str(right.get("type")):
                    continue
                reason = conflict_reason(left, right)
                if reason is None:
                    continue
                left["status"] = "conflict"
                right["status"] = "conflict"
                conflicts.append(
                    {
                        "existing_id": left["id"],
                        "candidate_id": right["id"],
                        "reason": reason,
                    }
                )

    retrieved_memories = [item for item in active_memories if retrieval_query and matches_query(item, retrieval_query)]

    return {
        "active_memories": active_memories,
        "merged_memories": merged_memories,
        "expired_memories": expired_memories,
        "conflicts": conflicts,
        "retrieved_memories": retrieved_memories,
        "summary": {
            "active_count": len(active_memories),
            "merged_count": len(merged_memories),
            "expired_count": len(expired_memories),
            "conflict_count": len(conflicts),
            "retrieved_count": len(retrieved_memories),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the dream-memory runtime.")
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
