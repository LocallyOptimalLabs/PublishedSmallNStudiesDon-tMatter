#!/usr/bin/env python3
"""Audit Many Labs 3 site-level rows without promoting one-to-many pairs.

The live build already uses ``data/raw/replication_projects/altmejd/data.csv``
for aggregate Many Labs 3 rows.  This pass keeps the lab/site audit trail but
does not add site-level rows to Figure 1 because they violate the 1:1 pair rule.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "data" / "raw" / "replication_projects" / "altmejd" / "data.csv"
PROMOTED_CSV = (
    ROOT
    / "data"
    / "derived"
    / "replication_pairs"
    / "harvest"
    / "promoted"
    / "ml3_site_level_effects__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "ml3_site_level_effects"
    / "ml3-site-level-effects-audit.tsv"
)

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
    "altmejd_id",
    "lab_id",
    "effect_type",
    "original_r",
    "replication_r",
    "original_p",
    "replication_p",
    "aggregated",
    "drop",
    "source_artifact_sha256",
    "source_row_text",
    "conversion_note",
    "audit_decision",
    "audit_note",
]


def clean(value: Any) -> str:
    text = "" if pd.isna(value) else str(value)
    text = re.sub(r"[\t\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def slugify(value: Any) -> str:
    text = clean(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "row"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def r_to_d(value: Any) -> float:
    try:
        r = float(value)
    except Exception:
        return math.nan
    if not math.isfinite(r) or abs(r) >= 1:
        return math.nan
    return abs(2 * r / math.sqrt(1 - r * r))


def numeric(value: Any) -> float:
    try:
        out = float(value)
    except Exception:
        return math.nan
    return out if math.isfinite(out) else math.nan


def row_text(row: pd.Series) -> str:
    return " | ".join(f"{key}={clean(value)}" for key, value in row.items())


def write_rows(path: Path, rows: list[dict[str, Any]], columns: list[str], delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in columns})


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(SOURCE_CSV)

    source_hash = sha256(SOURCE_CSV)
    raw_file = rel(SOURCE_CSV)
    df = pd.read_csv(SOURCE_CSV)
    ml3 = df.loc[df["project"].astype(str).eq("ml3")].copy()

    promoted: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for idx, row in ml3.iterrows():
        aggregated = bool(row.get("aggregated")) if not pd.isna(row.get("aggregated")) else False
        dropped = bool(row.get("drop")) if not pd.isna(row.get("drop")) else False
        original_r = numeric(row.get("effect_size.o"))
        replication_r = numeric(row.get("effect_size.r"))
        n_original = numeric(row.get("n.o"))
        n_replication = numeric(row.get("n.r"))
        d_original = r_to_d(original_r)
        d_replication = r_to_d(replication_r)

        title = clean(row.get("title"))
        lab_id = clean(row.get("lab_id"))
        altmejd_id = clean(row.get("id"))
        effect_type = clean(row.get("effect_type"))
        base = {
            "source_dataset": "Altmejd harmonized Many Labs 3 site-level rows",
            "project": "Many Labs 3",
            "pair_id": f"ml3_site_{slugify(altmejd_id)}_{slugify(lab_id)}",
            "original_title": title,
            "replication_title": f"Many Labs 3 site-level replication of {title} (lab_id={lab_id})",
            "original_doi": "",
            "replication_doi": "10.1016/j.jesp.2015.10.012",
            "outcome": f"{altmejd_id}; {effect_type}; lab_id={lab_id}",
            "D_original": f"{d_original:.15g}" if math.isfinite(d_original) else "",
            "N_original": f"{n_original:.15g}" if math.isfinite(n_original) else "",
            "D_replication": f"{d_replication:.15g}" if math.isfinite(d_replication) else "",
            "N_replication": f"{n_replication:.15g}" if math.isfinite(n_replication) else "",
            "raw_file": raw_file,
            "match_author": f"ml3_site_{slugify(altmejd_id)}_{slugify(lab_id)}",
            "altmejd_id": altmejd_id,
            "lab_id": lab_id,
            "effect_type": effect_type,
            "original_r": f"{original_r:.15g}" if math.isfinite(original_r) else "",
            "replication_r": f"{replication_r:.15g}" if math.isfinite(replication_r) else "",
            "original_p": clean(row.get("p_value.o")),
            "replication_p": clean(row.get("p_value.r")),
            "aggregated": aggregated,
            "drop": dropped,
            "source_artifact_sha256": source_hash,
            "source_row_text": row_text(row),
            "conversion_note": (
                "Altmejd effect_size.o and effect_size.r are on the correlation scale, matching the "
                "existing Many Labs 3 aggregate builder. Converted both to nonnegative D magnitudes "
                "with abs(2*r/sqrt(1-r^2))."
            ),
        }

        if aggregated:
            base["audit_decision"] = "not_promoted_aggregate_row"
            base["audit_note"] = "Held out because aggregate Many Labs 3 rows are already integrated."
        elif dropped:
            base["audit_decision"] = "not_promoted_drop_flag"
            base["audit_note"] = "Held out because the Altmejd row is flagged drop=True."
        elif not lab_id:
            base["audit_decision"] = "not_promoted_missing_site"
            base["audit_note"] = "Held out because this site-level pass requires a lab_id."
        elif not all(math.isfinite(x) for x in [d_original, d_replication, n_original, n_replication]):
            base["audit_decision"] = "not_promoted_missing_effect_or_n"
            base["audit_note"] = "Held out because one or more D/N inputs is missing or nonfinite."
        elif n_original < 10 or n_replication < 10:
            base["audit_decision"] = "not_promoted_fails_min_n_10"
            base["audit_note"] = "Held out because current Figure 1 strict rows require both sides N >= 10."
        elif n_replication <= n_original:
            base["audit_decision"] = "not_promoted_replication_n_not_larger"
            base["audit_note"] = "Held out because the site-level replication N is not larger than the original N."
        else:
            base["audit_decision"] = "not_promoted_one_to_many_site_level_grain"
            base["audit_note"] = (
                "Held out because the current Figure 1 policy requires 1:1 original-vs-replication "
                "pairs. Site-level Many Labs rows fan one original result into multiple lab-specific "
                "replication rows; use aggregate ML3 rows instead."
            )

        base["source_row_number"] = idx + 2
        audit.append(base)

    return promoted, audit


def main() -> None:
    promoted, audit = build_rows()
    write_rows(PROMOTED_CSV, promoted, PROMOTED_COLUMNS)
    write_rows(AUDIT_TSV, audit, AUDIT_COLUMNS + ["source_row_number"], delimiter="\t")
    print(f"wrote {len(promoted)} promoted rows to {PROMOTED_CSV}")
    print(f"wrote {len(audit)} audit rows to {AUDIT_TSV}")


if __name__ == "__main__":
    main()
