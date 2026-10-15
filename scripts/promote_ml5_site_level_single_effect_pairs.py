#!/usr/bin/env python3
"""Promote strict site-level Many Labs 5 single-effect rows.

This is intentionally narrower than the aggregate Many Labs 5 builder in
``scripts/analyze_replication_pairs.py``.  It uses the mirrored public single
effects table, keeps the site/protocol grain explicit, and promotes only rows
whose metric already has a current Figure 1 D-axis route.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = (
    ROOT
    / "data"
    / "raw"
    / "replication_projects"
    / "ml5"
    / "Summary Effect Sizes - Single Effects (including Orig and RPP).csv"
)
OUT_CSV = (
    ROOT
    / "data"
    / "derived"
    / "replication_pairs"
    / "harvest"
    / "promoted"
    / "ml5_site_level_single_effects__promoted_pairs.csv"
)
AUDIT_DIR = ROOT / "steps" / "corpus_results" / "figure1" / "ml5_site_level_single_effects"
AUDIT_TSV = AUDIT_DIR / "ml5-site-level-single-effects-audit.tsv"

PROMOTED_COLUMNS = [
    "source_dataset",
    "project",
    "pair_id",
    "original_title",
    "replication_title",
    "original_doi",
    "replication_doi",
    "outcome",
    "D_original",
    "N_original",
    "D_replication",
    "N_replication",
    "raw_file",
    "match_author",
]

AUDIT_COLUMNS = PROMOTED_COLUMNS + [
    "site",
    "protocol_source",
    "original_metric",
    "original_value",
    "replication_metric",
    "replication_value",
    "original_row_number",
    "replication_row_number",
    "original_source_row_text",
    "replication_source_row_text",
    "source_artifact_sha256",
    "conversion_note",
    "audit_decision",
    "audit_note",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def clean(value: Any) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"[\t\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(value: Any) -> str:
    text = clean(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "row"


def row_text(row: dict[str, str]) -> str:
    return " | ".join(f"{key}={clean(value)}" for key, value in row.items())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def numeric(value: Any) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return math.nan


def r_to_d(r: float) -> float:
    if not math.isfinite(r) or abs(r) >= 1:
        return math.nan
    return abs(2 * r / math.sqrt(1 - r * r))


def metric_to_d(metric: str, value: Any) -> tuple[float, str, bool]:
    metric_clean = clean(metric).lower()
    x = numeric(value)
    if not math.isfinite(x):
        return math.nan, "numeric effect value missing or nonfinite", False
    if metric_clean in {"r", "rp"}:
        return r_to_d(x), "converted correlation to D magnitude as abs(2*r/sqrt(1-r^2))", True
    if metric_clean in {"d", "g"}:
        return abs(x), f"used source-reported {metric_clean} as nonnegative SMD magnitude", True
    return math.nan, f"metric {metric_clean or 'blank'} is not in the current strict ML5 site-level D route", False


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str], delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def main() -> None:
    if not SOURCE_CSV.exists():
        raise SystemExit(f"Missing source table: {SOURCE_CSV}")

    source_hash = sha256(SOURCE_CSV)
    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row_number, row in enumerate(reader, start=2):
            item = dict(row)
            item["_row_number"] = str(row_number)
            rows.append(item)

    originals = {row["Study"]: row for row in rows if row.get("Source") == "Original"}
    promoted: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    raw_file = rel(SOURCE_CSV)

    for row in rows:
        protocol_source = clean(row.get("Source"))
        if protocol_source not in {"ML5 RP:P", "ML5 Revised"}:
            continue
        original = originals.get(row.get("Study", ""))
        if original is None:
            continue

        d_original, original_conversion, original_ok = metric_to_d(
            original.get("ES.Metric", ""), original.get("Value", "")
        )
        d_replication, replication_conversion, replication_ok = metric_to_d(
            row.get("ES.Metric", ""), row.get("Value", "")
        )
        n_original = numeric(original.get("N"))
        n_replication = numeric(row.get("N"))
        figure_label = clean(row.get("Figure3StudyLabel") or row.get("Study"))
        site = clean(row.get("Site"))
        protocol_slug = slugify(protocol_source)
        site_slug = slugify(site)
        study_slug = slugify(row.get("Study"))

        base = {
            "source_dataset": "Many Labs 5 site-level single effects",
            "project": "Many Labs 5",
            "pair_id": f"ml5_site_{study_slug}_{protocol_slug}_{site_slug}",
            "original_title": figure_label,
            "replication_title": f"{figure_label} ({protocol_source} site: {site})",
            "original_doi": "",
            "replication_doi": "10.1177/2515245920958687",
            "outcome": f"{figure_label}; {protocol_source}; site={site}",
            "D_original": f"{d_original:.15g}" if math.isfinite(d_original) else "",
            "N_original": f"{n_original:.15g}" if math.isfinite(n_original) else "",
            "D_replication": f"{d_replication:.15g}" if math.isfinite(d_replication) else "",
            "N_replication": f"{n_replication:.15g}" if math.isfinite(n_replication) else "",
            "raw_file": raw_file,
            "match_author": f"ml5_site_{study_slug}_{protocol_slug}_{site_slug}",
            "site": site,
            "protocol_source": protocol_source,
            "original_metric": clean(original.get("ES.Metric")),
            "original_value": clean(original.get("Value")),
            "replication_metric": clean(row.get("ES.Metric")),
            "replication_value": clean(row.get("Value")),
            "original_row_number": original.get("_row_number", ""),
            "replication_row_number": row.get("_row_number", ""),
            "original_source_row_text": row_text({k: v for k, v in original.items() if not k.startswith("_")}),
            "replication_source_row_text": row_text({k: v for k, v in row.items() if not k.startswith("_")}),
            "source_artifact_sha256": source_hash,
            "conversion_note": f"Original: {original_conversion}. Replication: {replication_conversion}.",
        }

        if not original_ok or not replication_ok:
            base["audit_decision"] = "not_promoted_unsupported_metric"
            base["audit_note"] = (
                "Held out to avoid adding eta-squared or pseudo-R2 conversions in this site-level pass."
            )
        elif not (math.isfinite(n_original) and math.isfinite(n_replication)):
            base["audit_decision"] = "not_promoted_missing_n"
            base["audit_note"] = "Held out because original or replication N is missing/nonfinite."
        elif n_original < 10 or n_replication < 10:
            base["audit_decision"] = "not_promoted_fails_min_n_10"
            base["audit_note"] = "Held out because current Figure 1 strict rows require both sides N >= 10."
        elif n_replication <= n_original:
            base["audit_decision"] = "not_promoted_replication_n_not_larger"
            base["audit_note"] = "Held out because the site-level replication N is not larger than the original N."
        else:
            base["audit_decision"] = "promoted_strict_site_level_row"
            base["audit_note"] = (
                "Promoted because the mirrored ML5 table gives original and site-level replication "
                "effect/N values, the effect metric uses an existing D route, and the site-level "
                "replication N is larger than the original N."
            )
            promoted.append({key: base[key] for key in PROMOTED_COLUMNS})

        audit_rows.append(base)

    write_csv(OUT_CSV, promoted, PROMOTED_COLUMNS)
    write_csv(AUDIT_TSV, audit_rows, AUDIT_COLUMNS, delimiter="\t")
    print(f"wrote {len(promoted)} promoted rows to {OUT_CSV}")
    print(f"wrote {len(audit_rows)} audit rows to {AUDIT_TSV}")


if __name__ == "__main__":
    main()
