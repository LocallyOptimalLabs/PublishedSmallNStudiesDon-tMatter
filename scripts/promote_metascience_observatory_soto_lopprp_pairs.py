#!/usr/bin/env python3
"""Promote conservative Soto LOPPRP rows from the mirrored Metascience API."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
API_JSON = (
    ROOT
    / "data"
    / "raw"
    / "replication_projects"
    / "metascience_observatory"
    / "live_check_2026-05-08"
    / "api_fred_2026-05-08.json"
)
ROOT_TSV = ROOT / "FIGURE1_REPLICATION_PAIRS.tsv"
PROMOTED_CSV = (
    ROOT
    / "data"
    / "derived"
    / "replication_pairs"
    / "harvest"
    / "promoted"
    / "metascience_observatory_soto_lopprp__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "metascience_observatory_soto_lopprp_20260508"
    / "metascience-soto-lopprp-promotion-audit.tsv"
)
SUMMARY_MD = AUDIT_TSV.with_name("metascience-soto-lopprp-promotion-summary.md")


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value)
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def norm_text(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).lower()).strip()


def to_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace("", np.nan), errors="coerce")


def doi_from_url(value: Any) -> str:
    match = re.search(r"(10\.\d{4,9}/[^\s\"<>]+)", clean(value), flags=re.IGNORECASE)
    if not match:
        return ""
    doi = match.group(1).strip().lower()
    doi = doi.rstrip(".,);]")
    return doi


def scalar_r_to_d(value: Any) -> float:
    r = pd.to_numeric(value, errors="coerce")
    if not np.isfinite(r) or abs(float(r)) >= 1:
        return np.nan
    return float(2 * float(r) / np.sqrt(1 - float(r) ** 2))


def stable_id(prefix: str, *parts: Any, size: int = 16) -> str:
    joined = "\x1f".join(clean(part) for part in parts)
    return f"{prefix}_{hashlib.sha256(joined.encode('utf-8')).hexdigest()[:size]}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def root_soto_titles() -> set[str]:
    root = pd.read_csv(ROOT_TSV, sep="\t", dtype=str).fillna("")
    soto = root[
        root.astype(str)
        .apply(lambda col: col.str.contains("Soto|Life Outcomes", case=False, na=False))
        .any(axis=1)
    ].copy()
    return set(soto["original_title"].map(norm_text))


def load_candidates() -> pd.DataFrame:
    payload = json.loads(API_JSON.read_text(encoding="utf-8"))
    rows = pd.DataFrame(payload["rows"]).fillna("")
    d = rows[rows["replication_initiative_tag"].eq("Soto et al LOPPRP")].copy()

    d["original_n_num"] = to_num(d["original_n"]).fillna(to_num(d["n_original"]))
    d["replication_n_num"] = to_num(d["replication_n"]).fillna(to_num(d["n_replication"]))
    d["original_r_num"] = to_num(d["original_es_r"]).fillna(to_num(d["es_original"]))
    d["replication_r_num"] = to_num(d["replication_es_r"]).fillna(to_num(d["es_replication"]))
    d["original_title_norm"] = d["original_title"].map(norm_text)
    d["replication_title_norm"] = d["replication_title"].map(norm_text)
    d["description_norm"] = d["description"].map(norm_text)
    d["original_doi"] = d["original_url"].map(doi_from_url)
    d["replication_doi"] = d["replication_url"].map(doi_from_url)

    existing_titles = root_soto_titles()
    d["promotion_status"] = "held"
    d.loc[~d["validated"].str.lower().eq("yes"), "promotion_status"] = "held_not_validated_yes"
    d.loc[
        d["promotion_status"].eq("held")
        & ~d["replication_type"].str.lower().str.contains("direct|close", regex=True, na=False),
        "promotion_status",
    ] = "held_not_direct_or_close"
    d.loc[
        d["promotion_status"].eq("held")
        & (
            d[["original_n_num", "replication_n_num", "original_r_num", "replication_r_num"]]
            .notna()
            .all(axis=1)
            .eq(False)
        ),
        "promotion_status",
    ] = "held_missing_numeric_d_or_n_inputs"
    d.loc[
        d["promotion_status"].eq("held")
        & (
            (d["original_n_num"] < 10)
            | (d["replication_n_num"] < 10)
            | (d["replication_n_num"] <= d["original_n_num"])
            | (d["original_r_num"].abs() >= 1)
            | (d["replication_r_num"].abs() >= 1)
        ),
        "promotion_status",
    ] = "held_failed_current_dn_gate"
    d.loc[
        d["promotion_status"].eq("held")
        & d["original_title_norm"].isin(existing_titles),
        "promotion_status",
    ] = "held_existing_soto_original_title"
    d.loc[
        d["promotion_status"].eq("held")
        & d["original_title_norm"].eq("")
        & d["original_doi"].eq(""),
        "promotion_status",
    ] = "held_missing_original_identity"
    d.loc[
        d["promotion_status"].eq("held")
        & d["replication_title_norm"].eq("")
        & d["replication_doi"].eq(""),
        "promotion_status",
    ] = "held_missing_replication_identity"
    d.loc[
        d["promotion_status"].eq("held")
        & d["description_norm"].eq(""),
        "promotion_status",
    ] = "held_missing_outcome_description"

    key_cols = [
        "original_doi",
        "replication_doi",
        "original_title_norm",
        "description_norm",
        "original_n_num",
        "replication_n_num",
        "original_r_num",
        "replication_r_num",
    ]
    d["duplicate_within_promotable_bucket"] = (
        d.loc[d["promotion_status"].eq("held"), key_cols].duplicated(keep="first")
    )
    d.loc[
        d["promotion_status"].eq("held") & d["duplicate_within_promotable_bucket"],
        "promotion_status",
    ] = "held_duplicate_within_promotable_bucket"
    d.loc[d["promotion_status"].eq("held"), "promotion_status"] = "promoted_conservative_new_soto_title"
    return d


def build_promoted(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates[candidates["promotion_status"].eq("promoted_conservative_new_soto_title")].copy()
    records: list[dict[str, Any]] = []
    api_rel = str(API_JSON.relative_to(ROOT))
    api_sha = sha256_file(API_JSON)
    for _, row in rows.iterrows():
        d_original = abs(scalar_r_to_d(row["original_r_num"]))
        d_replication = abs(scalar_r_to_d(row["replication_r_num"]))
        original_title = clean(row["original_title"]) or clean(row["original_url"])
        replication_title = clean(row["replication_title"]) or clean(row["replication_url"])
        outcome = clean(row["description"])
        pair_id = stable_id(
            "metascience_soto_lopprp",
            row["original_doi"],
            row["replication_doi"],
            original_title,
            outcome,
            row["original_n_num"],
            row["replication_n_num"],
            row["original_r_num"],
            row["replication_r_num"],
        )
        records.append(
            {
                "source_dataset": "Metascience Observatory FReD API Soto LOPPRP rows",
                "project": "Life Outcomes of Personality Replication Project",
                "pair_id": pair_id,
                "original_title": original_title,
                "replication_title": replication_title,
                "original_doi": clean(row["original_doi"]),
                "replication_doi": clean(row["replication_doi"]),
                "outcome": outcome,
                "D_original": d_original,
                "N_original": float(row["original_n_num"]),
                "D_replication": d_replication,
                "N_replication": float(row["replication_n_num"]),
                "raw_file": api_rel,
                "n_source_file": api_rel,
                "match_author": f"{original_title} | {outcome}",
                "source_artifact_sha256": api_sha,
                "verbatim_n_text_original": f"Metascience API row: original_n={row['original_n']}; n_original={row['n_original']}",
                "verbatim_n_text_replication": f"Metascience API row: replication_n={row['replication_n']}; n_replication={row['n_replication']}",
                "verbatim_effect_text_original": (
                    f"Metascience API row: original_es_r={row['original_es_r']}; "
                    f"es_original={row['es_original']}; original_es={row['original_es']}"
                ),
                "verbatim_effect_text_replication": (
                    f"Metascience API row: replication_es_r={row['replication_es_r']}; "
                    f"es_replication={row['es_replication']}; replication_es={row['replication_es']}"
                ),
                "d_n_transformation_note": (
                    "Metascience API exposes normalized Pearson r fields. Figure 1 D is "
                    "abs(2*r/sqrt(1-r^2)); signed r is preserved in verbatim effect text."
                ),
                "replication_type": clean(row["replication_type"]),
                "validated": clean(row["validated"]),
                "replication_initiative_tag": clean(row["replication_initiative_tag"]),
                "metascience_last_updated": json.loads(API_JSON.read_text(encoding="utf-8")).get(
                    "lastUpdated", ""
                ),
            }
        )
    return pd.DataFrame(records)


def write_summary(candidates: pd.DataFrame, promoted: pd.DataFrame) -> None:
    counts = candidates["promotion_status"].value_counts().rename_axis("status").reset_index(name="rows")
    lines = [
        "# Metascience Observatory Soto LOPPRP promotion",
        "",
        f"- Source API mirror: `{API_JSON.relative_to(ROOT)}`",
        f"- Source SHA-256: `{sha256_file(API_JSON)}`",
        f"- Candidate Soto rows: {len(candidates):,}",
        f"- Promoted conservative new-title rows: {len(promoted):,}",
        f"- Promoted CSV: `{PROMOTED_CSV.relative_to(ROOT)}`",
        f"- Audit TSV: `{AUDIT_TSV.relative_to(ROOT)}`",
        "",
        "## Status Counts",
        "",
        counts.to_markdown(index=False),
        "",
        "## Promotion Rule",
        "",
        "Rows are promoted only when `validated == yes`, replication type is direct/close, "
        "both sides have finite normalized Pearson r and N, `N_replication > N_original`, "
        "both N are at least 10, the original title is not already represented by the current "
        "Soto/Life Outcomes rows, and source identity plus outcome text are present.",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    candidates = load_candidates()
    promoted = build_promoted(candidates)
    PROMOTED_CSV.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_TSV.parent.mkdir(parents=True, exist_ok=True)
    promoted.to_csv(PROMOTED_CSV, index=False)
    candidates.to_csv(AUDIT_TSV, sep="\t", index=False)
    write_summary(candidates, promoted)
    print(f"Wrote {len(promoted)} promoted rows: {PROMOTED_CSV.relative_to(ROOT)}")
    print(f"Wrote audit: {AUDIT_TSV.relative_to(ROOT)}")
    print(f"Wrote summary: {SUMMARY_MD.relative_to(ROOT)}")
    print(candidates["promotion_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
