#!/usr/bin/env python3
"""Promote conservative SRP rows from the mirrored Metascience API."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from promote_metascience_observatory_soto_lopprp_pairs import (
    API_JSON,
    ROOT,
    ROOT_TSV,
    clean,
    doi_from_url,
    norm_text,
    scalar_r_to_d,
    sha256_file,
    stable_id,
    to_num,
)


PROMOTED_CSV = (
    ROOT
    / "data"
    / "derived"
    / "replication_pairs"
    / "harvest"
    / "promoted"
    / "metascience_observatory_srp__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "metascience_observatory_srp_20260508"
    / "metascience-srp-promotion-audit.tsv"
)
SUMMARY_MD = AUDIT_TSV.with_name("metascience-srp-promotion-summary.md")
SRP_REPLICATION_DOI = "10.1098/rsos.231240"


def load_root_keys() -> set[tuple[str, str]]:
    root = pd.read_csv(ROOT_TSV, sep="\t", dtype=str).fillna("")
    return set(zip(root["original_title"].map(norm_text), root["outcome_label"].map(norm_text)))


def load_candidates() -> pd.DataFrame:
    payload = json.loads(API_JSON.read_text(encoding="utf-8"))
    rows = pd.DataFrame(payload["rows"]).fillna("")
    d = rows[rows["replication_initiative_tag"].eq("SRP")].copy()
    d["original_n_num"] = to_num(d["original_n"]).fillna(to_num(d["n_original"]))
    d["replication_n_num"] = to_num(d["replication_n"]).fillna(to_num(d["n_replication"]))
    d["original_r_num"] = to_num(d["original_es_r"]).fillna(to_num(d["es_original"]))
    d["replication_r_num"] = to_num(d["replication_es_r"]).fillna(to_num(d["es_replication"]))
    d["original_title_norm"] = d["original_title"].map(norm_text)
    d["description_norm"] = d["description"].map(norm_text)
    d["original_doi"] = d["original_url"].map(doi_from_url)
    d["replication_doi"] = d["replication_url"].map(doi_from_url)

    root_keys = load_root_keys()
    d["promotion_status"] = "held"
    d.loc[~d["validated"].str.lower().eq("yes"), "promotion_status"] = "held_not_validated_yes"
    d.loc[
        d["promotion_status"].eq("held")
        & ~d["replication_type"].str.lower().str.contains("direct|close", regex=True, na=False),
        "promotion_status",
    ] = "held_not_direct_or_close"
    d.loc[
        d["promotion_status"].eq("held")
        & ~d["source"].eq("FReD explorer (Feb 2026 import)"),
        "promotion_status",
    ] = "held_unexpected_source_label"
    d.loc[
        d["promotion_status"].eq("held")
        & ~d["replication_doi"].eq(SRP_REPLICATION_DOI),
        "promotion_status",
    ] = "held_unexpected_replication_doi"
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
    existing_key = pd.Series(
        [
            (orig, outcome) in root_keys
            for orig, outcome in zip(d["original_title_norm"], d["description_norm"])
        ],
        index=d.index,
    )
    d.loc[
        d["promotion_status"].eq("held") & existing_key,
        "promotion_status",
    ] = "held_existing_original_title_outcome"
    d.loc[
        d["promotion_status"].eq("held")
        & (d["original_title_norm"].eq("") | d["description_norm"].eq("")),
        "promotion_status",
    ] = "held_missing_identity_or_outcome"
    d.loc[d["promotion_status"].eq("held"), "promotion_status"] = "promoted_conservative_srp"
    return d


def build_promoted(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates[candidates["promotion_status"].eq("promoted_conservative_srp")].copy()
    records: list[dict[str, Any]] = []
    api_rel = str(API_JSON.relative_to(ROOT))
    api_sha = sha256_file(API_JSON)
    last_updated = json.loads(API_JSON.read_text(encoding="utf-8")).get("lastUpdated", "")
    for _, row in rows.iterrows():
        original_title = clean(row["original_title"]) or clean(row["original_url"])
        replication_title = clean(row["replication_title"]) or clean(row["replication_url"])
        outcome = clean(row["description"])
        records.append(
            {
                "source_dataset": "Metascience Observatory FReD API SRP rows",
                "project": "Student Replication Project",
                "pair_id": stable_id(
                    "metascience_srp",
                    row["original_doi"],
                    row["replication_doi"],
                    original_title,
                    outcome,
                    row["original_n_num"],
                    row["replication_n_num"],
                    row["original_r_num"],
                    row["replication_r_num"],
                ),
                "original_title": original_title,
                "replication_title": replication_title,
                "original_doi": clean(row["original_doi"]),
                "replication_doi": clean(row["replication_doi"]),
                "outcome": outcome,
                "D_original": abs(scalar_r_to_d(row["original_r_num"])),
                "N_original": float(row["original_n_num"]),
                "D_replication": abs(scalar_r_to_d(row["replication_r_num"])),
                "N_replication": float(row["replication_n_num"]),
                "raw_file": api_rel,
                "n_source_file": api_rel,
                "match_author": f"{original_title} | {outcome}",
                "source_artifact_sha256": api_sha,
                "verbatim_n_text_original": f"Metascience API row: original_n={row['original_n']}; n_original={row['n_original']}",
                "verbatim_n_text_replication": f"Metascience API row: replication_n={row['replication_n']}; n_replication={row['n_replication']}",
                "verbatim_effect_text_original": f"Metascience API row: original_es_r={row['original_es_r']}; es_original={row['es_original']}",
                "verbatim_effect_text_replication": f"Metascience API row: replication_es_r={row['replication_es_r']}; es_replication={row['es_replication']}",
                "d_n_transformation_note": "Metascience API exposes normalized Pearson r fields. Figure 1 D is abs(2*r/sqrt(1-r^2)).",
                "replication_type": clean(row["replication_type"]),
                "validated": clean(row["validated"]),
                "replication_initiative_tag": clean(row["replication_initiative_tag"]),
                "metascience_last_updated": last_updated,
            }
        )
    return pd.DataFrame(records)


def write_summary(candidates: pd.DataFrame, promoted: pd.DataFrame) -> None:
    counts = candidates["promotion_status"].value_counts().rename_axis("status").reset_index(name="rows")
    lines = [
        "# Metascience Observatory SRP promotion",
        "",
        f"- Source API mirror: `{API_JSON.relative_to(ROOT)}`",
        f"- Source SHA-256: `{sha256_file(API_JSON)}`",
        f"- Candidate SRP rows: {len(candidates):,}",
        f"- Promoted conservative SRP rows: {len(promoted):,}",
        f"- Promoted CSV: `{PROMOTED_CSV.relative_to(ROOT)}`",
        f"- Audit TSV: `{AUDIT_TSV.relative_to(ROOT)}`",
        "",
        "## Status Counts",
        "",
        counts.to_markdown(index=False),
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
    print(candidates["promotion_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
