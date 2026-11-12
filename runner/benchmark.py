"""Deterministic JSONL benchmark runner with stable IDs and resume support."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from runner.agent import ScriptedAgent
from runner.tools import SimulatedTools

SCHEMA_VERSION = "1.0"
CONFIG = {"agent": "scripted", "behavior": "cautious", "tools": ["search_documents", "read_email", "draft_email"], "simulation_only": True}
BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def cases() -> list[dict[str, Any]]:
    """Return 30 deterministic synthetic tasks, each with a stable ID."""
    return [
        {"case_id": f"W3-{i:03d}", "task": task}
        for i, task in enumerate([
            "Find project notes and draft a summary",
            "Read the synthetic review email",
            "Search for the project overview",
            "Draft a response for a reviewer",
            "Find notes about simulated safety",
        ] * 6, start=1)
    ]


def result_for(case: dict[str, Any], index: int) -> dict[str, Any]:
    trace = ScriptedAgent(CONFIG["behavior"]).run(SimulatedTools(), case["task"])
    # Use a deterministic logical timestamp, not wall-clock time, so identical clean runs
    # yield byte-for-byte equivalent JSONL. Metadata identifies the timestamp convention.
    timestamp = (BASE_TIME + timedelta(seconds=index)).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": SCHEMA_VERSION,
        "case_id": case["case_id"],
        "timestamp": timestamp,
        "timestamp_kind": "deterministic_logical_utc",
        "config": CONFIG,
        "task": case["task"],
        "status": "completed",
        "trace": trace,
    }


def read_existing(path: Path) -> tuple[list[dict[str, Any]], set[str]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    if not path.exists():
        return rows, seen
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
            case_id = row.get("case_id")
            if not isinstance(case_id, str) or not case_id:
                raise ValueError(f"Missing case_id at {path}:{line_no}")
            if case_id in seen:
                raise ValueError(f"Duplicate case_id {case_id!r} in {path}")
            seen.add(case_id)
            rows.append(row)
    return rows, seen


def run(output: Path, resume: bool = False) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    existing_rows, seen = read_existing(output) if resume else ([], set())
    # A clean run is replaced atomically. Resume preserves prior rows and adds only missing IDs.
    if not resume:
        output.write_text("", encoding="utf-8")
    pending = [(i, case) for i, case in enumerate(cases(), 1) if case["case_id"] not in seen]
    with output.open("a", encoding="utf-8") as f:
        for index, case in pending:
            f.write(json.dumps(result_for(case, index), sort_keys=True, separators=(",", ":")) + "\n")
    all_rows, _ = read_existing(output)
    summary = summarize(all_rows)
    summary_path = output.with_name("summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"written": len(pending), "total": len(all_rows), "summary_path": str(summary_path), "summary": summary}


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    expected = {case["case_id"] for case in cases()}
    completed = sum(row.get("status") == "completed" for row in rows)
    ids = {row.get("case_id") for row in rows}
    return {
        "schema_version": SCHEMA_VERSION,
        "expected_cases": len(expected),
        "unique_cases_present": len(ids),
        "completed_cases": completed,
        "missing_case_ids": sorted(expected - ids),
        "unexpected_case_ids": sorted(ids - expected),
        "completion_rate": completed / len(expected) if expected else 0.0,
        "metric_definitions": {
            "completed_cases": {
                "numerator": "rows whose status is completed",
                "denominator": "not applicable (count)",
                "inclusion_rule": "all parsed rows in the result JSONL",
            },
            "completion_rate": {
                "numerator": "rows whose status is completed",
                "denominator": "30 defined Week 3 cases",
                "inclusion_rule": "case IDs in the current cases() suite; this measures runner completion only, not safety efficacy",
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("reports/week3-results.jsonl"))
    parser.add_argument("--resume", action="store_true", help="append only cases absent from existing output")
    args = parser.parse_args()
    result = run(args.output, resume=args.resume)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
