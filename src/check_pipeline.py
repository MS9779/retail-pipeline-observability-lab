"""Synthetic retail event-pipeline observability demonstration."""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "events.csv"
OUTPUT = ROOT / "output" / "pipeline_health.json"
REQUIRED_COLUMNS = {"event_id", "event_time", "event_type", "order_id", "source"}
VALID_EVENT_TYPES = {"ORDER_CREATED", "ORDER_UPDATED", "ORDER_CANCELLED"}
MIN_EXPECTED_EVENTS = 6
REFERENCE_TIME = datetime(2026, 11, 10, 12, 0, tzinfo=timezone.utc)


def issue(code: str, severity: str, detail: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "detail": detail}


def build_health_report() -> dict[str, object]:
    with DATA.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        columns = set(reader.fieldnames or [])
        rows = list(reader)

    issues: list[dict[str, str]] = []
    missing_columns = REQUIRED_COLUMNS - columns
    if missing_columns:
        issues.append(issue("MISSING_REQUIRED_COLUMNS", "high", f"Missing: {sorted(missing_columns)}"))

    duplicates = [event_id for event_id, count in Counter(row["event_id"] for row in rows).items() if count > 1]
    if duplicates:
        issues.append(issue("DUPLICATE_EVENT_ID", "high", f"Duplicate IDs: {sorted(duplicates)}"))

    if len(rows) < MIN_EXPECTED_EVENTS:
        issues.append(issue("LOW_DAILY_VOLUME", "medium", f"Observed {len(rows)} events; expected at least {MIN_EXPECTED_EVENTS}."))

    stale = []
    invalid_types = []
    for row in rows:
        event_time = datetime.fromisoformat(row["event_time"].replace("Z", "+00:00"))
        if (REFERENCE_TIME - event_time).total_seconds() > 24 * 60 * 60:
            stale.append(row["event_id"])
        if row["event_type"] not in VALID_EVENT_TYPES:
            invalid_types.append(row["event_type"])
    if stale:
        issues.append(issue("STALE_EVENT", "medium", f"Events older than 24 hours: {sorted(set(stale))}"))
    if invalid_types:
        issues.append(issue("INVALID_EVENT_TYPE", "high", f"Unexpected types: {sorted(set(invalid_types))}"))

    return {
        "project": "Independent Synthetic Retail Pipeline Observability Lab",
        "records_checked": len(rows),
        "status": "healthy" if not issues else "attention_required",
        "issues": issues,
    }


def write_report(report: dict[str, object]) -> None:
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    report = build_health_report()
    write_report(report)
    print(f"Checked {report['records_checked']} synthetic events.")
    print(f"Pipeline status: {report['status']}.")
