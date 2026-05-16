#!/usr/bin/env python3
"""Minimal kairos-lite runtime."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


VALID_PERMISSION_LEVELS = {"observe", "suggest", "draft", "execute"}
VALID_OUTPUT_MODES = {"brief", "checklist", "report", "alert"}
VALID_SCHEDULE_TYPES = {"one_time", "recurring", "manual"}
DANGEROUS_ACTIONS = {
    "delete_files",
    "modify_source_code",
    "commit_code",
    "push_code",
    "execute_shell_commands",
    "access_external_services",
}
DEFAULT_FORBIDDEN_ACTIONS = [
    "modify_source_code",
    "delete_files",
    "commit_code",
    "push_code",
    "unrestricted_background_execution",
]


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


def normalize_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def normalize_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    items: list[str] = []
    for item in value:
        if isinstance(item, str):
            text = item.strip()
            if text:
                items.append(text)
    return items


def parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def normalize_schedule(raw: Any, has_schedule: bool) -> tuple[dict[str, str], list[str]]:
    risks: list[str] = []
    if not isinstance(raw, dict):
        if not has_schedule:
            risks.append("No explicit schedule was provided.")
        return {"type": "manual", "value": "manual"}, risks
    schedule_type = normalize_text(raw.get("type"))
    schedule_value = normalize_text(raw.get("value"))
    if schedule_type not in VALID_SCHEDULE_TYPES:
        schedule_type = "manual"
        schedule_value = "manual"
        risks.append("No explicit schedule was provided.")
    if not schedule_value:
        schedule_value = "manual" if schedule_type == "manual" else ""
        if schedule_type == "manual":
            risks.append("No explicit schedule was provided.")
    return {"type": schedule_type, "value": schedule_value}, risks


def detect_dangerous_actions(actions: list[str]) -> list[str]:
    dangerous = []
    for action in actions:
        if action in DANGEROUS_ACTIONS and action not in dangerous:
            dangerous.append(action)
    return dangerous


def build_output(payload: dict[str, Any]) -> dict[str, Any]:
    job_goal = normalize_text(payload.get("job_goal"))
    if not job_goal:
        raise ValueError("job_goal is required and must be non-empty")

    permission_level = normalize_text(payload.get("permission_level")) or "observe"
    output_mode = normalize_text(payload.get("output_mode")) or "brief"
    current_date_text = normalize_text(payload.get("current_date"))
    current_date = parse_date(current_date_text)
    expiry_raw = normalize_text(payload.get("expiry"))
    context = normalize_text(payload.get("context"))
    requires_user_approval = payload.get("requires_user_approval", True)
    if not isinstance(requires_user_approval, bool):
        requires_user_approval = bool(requires_user_approval)

    allowed_actions = normalize_list(payload.get("allowed_actions"))
    forbidden_actions = normalize_list(payload.get("forbidden_actions"))
    for default_action in DEFAULT_FORBIDDEN_ACTIONS:
        if default_action not in forbidden_actions:
            forbidden_actions.append(default_action)

    risks: list[str] = []
    if permission_level not in VALID_PERMISSION_LEVELS:
        return {
            "job_goal": job_goal,
            "job_status": "INVALID",
            "lifecycle_stage": "schedule",
            "schedule": {"type": "manual", "value": "manual"},
            "permission_level": permission_level,
            "allowed_actions": allowed_actions,
            "forbidden_actions": forbidden_actions,
            "requires_user_approval": requires_user_approval,
            "execution_mode": "plan_only",
            "job_plan": [],
            "brief": "",
            "expiry": expiry_raw,
            "is_expired": False,
            "risks": [f"Invalid permission level: {permission_level}"],
            "next_step": "Fix the input permission level and resubmit the job.",
        }

    schedule, schedule_risks = normalize_schedule(payload.get("schedule"), "schedule" in payload)
    risks.extend(schedule_risks)

    dangerous_actions = detect_dangerous_actions(allowed_actions)
    if dangerous_actions:
        for action in dangerous_actions:
            if action not in forbidden_actions:
                forbidden_actions.append(action)
        risks.append("Dangerous action requested and blocked by permission policy.")

    is_expired = False
    if expiry_raw:
        expiry_date = parse_date(expiry_raw)
        if expiry_date is not None and current_date is not None and expiry_date < current_date:
            is_expired = True
        elif expiry_date is None:
            pass
    else:
        risks.append("No expiry was provided.")

    job_status = "PLANNED"
    if is_expired:
        job_status = "EXPIRED"
    elif permission_level == "execute":
        job_status = "REQUIRES_APPROVAL"
        risks.append("Execute permission requires explicit user approval and is not performed by kairos-lite runtime.")
    elif dangerous_actions:
        job_status = "BLOCKED"
    elif requires_user_approval:
        job_status = "REQUIRES_APPROVAL"

    lifecycle_stage = "schedule"
    if is_expired:
        lifecycle_stage = "expire"
    elif job_status == "REQUIRES_APPROVAL":
        lifecycle_stage = "permission"
    elif job_status == "BLOCKED":
        lifecycle_stage = "permission"
    elif output_mode == "brief":
        lifecycle_stage = "brief"

    job_plan = [
        "Validate schedule.",
        "Check permission boundary.",
        "Prepare job draft or observation plan.",
        "Generate brief.",
        "Check expiry before execution.",
    ]

    brief = (
        f"Job: {job_goal}. This runtime only generates a plan, not a background execution. "
        f"Permission level: {permission_level}. User approval required: {str(requires_user_approval).lower()}. "
        f"Expired: {str(is_expired).lower()}."
    )

    if is_expired:
        next_step = "Update expiry or recreate the job."
    elif job_status == "REQUIRES_APPROVAL":
        next_step = "Confirm permissions and schedule with the user."
    elif job_status == "INVALID":
        next_step = "Fix the invalid input and resubmit the job."
    elif job_status == "PLANNED":
        next_step = "Save the job plan or hand it to an external scheduler."
    elif job_status == "BLOCKED":
        next_step = "Remove dangerous actions and resubmit the job."
    else:
        next_step = "Review the generated plan and brief."

    if not expiry_raw:
        expiry_output = ""
    else:
        expiry_output = expiry_raw

    return {
        "job_goal": job_goal,
        "job_status": job_status,
        "lifecycle_stage": lifecycle_stage,
        "schedule": schedule,
        "permission_level": permission_level,
        "allowed_actions": allowed_actions,
        "forbidden_actions": forbidden_actions,
        "requires_user_approval": requires_user_approval,
        "execution_mode": "plan_only",
        "job_plan": job_plan,
        "brief": brief,
        "expiry": expiry_output,
        "is_expired": is_expired,
        "risks": risks,
        "next_step": next_step,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the kairos-lite runtime.")
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
