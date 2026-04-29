from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from pathlib import Path

from .classifier import classify
from .models import Classification
from .reader import iter_units


def run_pipeline(export_dir: Path, min_public_score: float, chunk_chars: int) -> dict[str, object]:
    public_rows: list[Classification] = []
    excluded_rows: list[Classification] = []
    skipped_rows: list[Classification] = []
    unit_count = 0

    for unit in iter_units(export_dir, chunk_chars):
        unit_count += 1
        result = classify(unit)
        if result.decision == "public_candidate" and result.score >= min_public_score:
            public_rows.append(result)
        elif result.decision.startswith("exclude"):
            excluded_rows.append(result)
        else:
            skipped_rows.append(result)

    return {
        "unit_count": unit_count,
        "public": public_rows,
        "excluded": excluded_rows,
        "skipped": skipped_rows,
        "summary": build_summary(unit_count, public_rows, excluded_rows, skipped_rows),
    }


def build_summary(
    unit_count: int,
    public_rows: list[Classification],
    excluded_rows: list[Classification],
    skipped_rows: list[Classification],
) -> dict[str, object]:
    return {
        "units_scanned": unit_count,
        "public_candidate_units": len(public_rows),
        "excluded_units": len(excluded_rows),
        "skipped_units": len(skipped_rows),
        "public_topic_counts": dict(Counter(primary_topic(row) for row in public_rows)),
        "exclusion_reason_counts": dict(Counter(reason for row in excluded_rows for reason in row.exclusion_reasons)),
        "identifier_hit_counts": dict(Counter(hit for row in excluded_rows for hit in row.identifier_hits)),
    }


def primary_topic(row: Classification) -> str:
    return row.public_topics[0][0] if row.public_topics else "Unclassified"


def rows_as_dicts(rows: list[Classification]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]

