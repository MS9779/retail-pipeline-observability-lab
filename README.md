# Retail Pipeline Observability Lab

> **Independent project. Synthetic data. No employer data or internal logic.**

This project demonstrates simple, repeatable health checks for a fictional retail event pipeline.

```text
Input:   daily order events
Check:   is the data fresh, complete, unique, and structurally valid?
Output:  a small health report with clear follow-up actions
```

## What it checks

```text
✓ Required columns
✓ Duplicate event IDs
✓ Event freshness
✓ Expected daily volume
✓ Invalid event types
```

## Why it matters

```text
A pipeline can finish successfully and still deliver bad data.
These checks make data-health failures visible before reporting consumers rely on them.
```

## Run it

```bash
python3 src/check_pipeline.py
python3 tests/test_pipeline.py
```

## Example result

```json
{
  "status": "attention_required",
  "checks": ["DUPLICATE_EVENT_ID", "LOW_DAILY_VOLUME"]
}
```

## Portfolio wording

```text
Independent Project — Retail Pipeline Observability Lab

Built a Python health-check workflow for fictional retail event data. Added
schema, freshness, volume, duplicate, and event-type checks, then generated a
plain-language report to support dependable reporting and faster issue triage.
```

## Important boundary

```text
This is personal learning work using fictional records.
It is not an employer project and includes no production data, credentials,
internal documents, screenshots, metrics, or proprietary logic.
```
