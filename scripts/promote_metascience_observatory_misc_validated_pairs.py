#!/usr/bin/env python3
"""Promote explicitly reviewed miscellaneous Metascience/FReD API rows.

This is intentionally allowlist-based.  The broad untagged Metascience bucket
contains useful individual rows, but it also contains known project duplicates
and noisy CurateScience mappings.  The rows promoted here were selected from
validated, direct/close API rows after excluding known integrated projects and
near-duplicate source assertions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from promote_metascience_observatory_soto_lopprp_pairs import (
    API_JSON,
    ROOT,
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
    / "metascience_observatory_misc_validated__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "metascience_observatory_misc_validated_20260508"
    / "metascience-misc-validated-promotion-audit.tsv"
)
SUMMARY_MD = AUDIT_TSV.with_name("metascience-misc-validated-promotion-summary.md")


SAFE_ALLOWLIST: dict[str, dict[str, str]] = {
    "misc_spending_money_positive_affect": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Registered replication report / individual replication",
        "original_doi": "10.1126/science.1150952",
        "replication_doi": "10.1037/pspa0000191",
        "outcome_contains": "positive affect",
    },
    "misc_spending_money_retrospective_positive_emotion": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Registered replication report / individual replication",
        "original_doi": "10.1126/science.1150952",
        "replication_doi": "10.1037/pspa0000191",
        "outcome_contains": "retrospective positive emotion",
    },
    "misc_red_romance_crep_edinburgh": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "CREP / individual replication",
        "original_doi": "10.1037/a0019689",
        "replication_doi": "10.17605/osf.io/dqv9y",
        "outcome_contains": "color red increases attractiveness ratings",
    },
    "misc_affective_expectation_negative": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Individual replication",
        "original_doi": "10.1207/s15324834basp2504_5",
        "replication_doi": "10.31234/osf.io/akfzh",
        "outcome_contains": "negative expectations",
    },
    "misc_affective_expectation_no_expectations": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Individual replication",
        "original_doi": "10.1207/s15324834basp2504_5",
        "replication_doi": "10.31234/osf.io/akfzh",
        "outcome_contains": "no expectations",
    },
    "misc_affective_expectation_positive": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Individual replication",
        "original_doi": "10.1207/s15324834basp2504_5",
        "replication_doi": "10.31234/osf.io/akfzh",
        "outcome_contains": "positive expectations",
    },
    "misc_variety_quantity_six_studies": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Individual replication",
        "original_doi": "10.1086/598971",
        "replication_doi": "10.31234/osf.io/v643q",
        "outcome_contains": "variety reduces perceived quantity",
    },
    "misc_social_distance_plos": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Individual replication",
        "original_doi": "10.1111/j.1467-9280.2008.02084.x",
        "replication_doi": "10.1371/journal.pone.0042510",
        "outcome_contains": "spatial distance",
    },
    "misc_retrieval_inhibition_cortex": {
        "source_dataset": "Metascience Observatory FReD API miscellaneous validated rows",
        "project": "Individual replication",
        "original_doi": "10.1038/nn.3973",
        "replication_doi": "10.1016/j.cortex.2018.03.026",
        "outcome_contains": "competing memories",
    },
    "rsesr_heel_wedge": {
        "source_dataset": "Metascience Observatory FReD API RSESR rows",
        "project": "Replicability of Sports and Exercise Science Research",
        "original_doi": "10.1519/jsc.0000000000001655",
        "replication_doi": "10.1007/s40279-025-02201-w",
        "outcome_contains": "heel wedge",
    },
    "rsesr_caffeinated_gum": {
        "source_dataset": "Metascience Observatory FReD API RSESR rows",
        "project": "Replicability of Sports and Exercise Science Research",
        "original_doi": "10.1123/ijspp.2019-0098",
        "replication_doi": "10.1007/s40279-025-02201-w",
        "outcome_contains": "caffeinated chewing gum",
    },
    "rsesr_caffeine_vertical_jump": {
        "source_dataset": "Metascience Observatory FReD API RSESR rows",
        "project": "Replicability of Sports and Exercise Science Research",
        "original_doi": "10.1519/jsc.0000000000001280",
        "replication_doi": "10.1007/s40279-025-02201-w",
        "outcome_contains": "vertical jump height",
    },
    "rsesr_cluster_set_bench_press": {
        "source_dataset": "Metascience Observatory FReD API RSESR rows",
        "project": "Replicability of Sports and Exercise Science Research",
        "original_doi": "10.1519/jsc.0000000000003166",
        "replication_doi": "10.1007/s40279-025-02201-w",
        "outcome_contains": "cluster-set",
    },
    "rsesr_y_balance_fatigue": {
        "source_dataset": "Metascience Observatory FReD API RSESR rows",
        "project": "Replicability of Sports and Exercise Science Research",
        "original_doi": "10.1016/j.jsams.2017.06.007",
        "replication_doi": "10.1007/s40279-025-02201-w",
        "outcome_contains": "y-balance",
    },
    "rsesr_volleyball_landing": {
        "source_dataset": "Metascience Observatory FReD API RSESR rows",
        "project": "Replicability of Sports and Exercise Science Research",
        "original_doi": "10.1080/17461391.2017.1308560",
        "replication_doi": "10.1007/s40279-025-02201-w",
        "outcome_contains": "ankle dorsiflexion",
    },
}


KNOWN_DUPLICATE_REPLICATION_DOIS = {
    "10.1126/science.aac4716",
    "10.1007/s13164-018-0400-9",
    "10.1177/2515245918810225",
    "10.1177/2515245920958687",
    "10.1177/2515245920927643",
    "10.1177/2515245920917931",
    "10.1177/2515245918781032",
    "10.1016/j.jesp.2015.10.012",
}


def directish(value: Any) -> bool:
    text = clean(value).lower()
    return "direct" in text or "close" in text or "same population" in text or "closely follows" in text


def prepare_candidates() -> pd.DataFrame:
    rows = pd.DataFrame(json.loads(API_JSON.read_text(encoding="utf-8"))["rows"]).fillna("")
    rows["original_n_num"] = to_num(rows["original_n"]).fillna(to_num(rows["n_original"]))
    rows["replication_n_num"] = to_num(rows["replication_n"]).fillna(to_num(rows["n_replication"]))
    rows["original_r_num"] = to_num(rows["original_es_r"]).fillna(to_num(rows["es_original"]))
    rows["replication_r_num"] = to_num(rows["replication_es_r"]).fillna(to_num(rows["es_replication"]))
    rows["original_doi"] = rows["original_url"].map(doi_from_url)
    rows["replication_doi"] = rows["replication_url"].map(doi_from_url)
    rows["description_norm"] = rows["description"].map(norm_text)
    rows["promotion_status"] = "held_not_reviewed_for_misc_allowlist"

    mechanical = (
        rows["validated"].str.lower().eq("yes")
        & rows["replication_type"].map(directish)
        & rows[["original_n_num", "replication_n_num", "original_r_num", "replication_r_num"]]
        .notna()
        .all(axis=1)
        & rows["original_n_num"].ge(10)
        & rows["replication_n_num"].ge(10)
        & rows["replication_n_num"].gt(rows["original_n_num"])
        & rows["original_r_num"].abs().lt(1)
        & rows["replication_r_num"].abs().lt(1)
    )
    rows.loc[~mechanical, "promotion_status"] = "held_failed_validated_direct_numeric_dn_gate"
    rows.loc[
        mechanical & rows["source"].eq("Curate Science scrape"),
        "promotion_status",
    ] = "held_curatescience_mapping_noise"
    rows.loc[
        mechanical & rows["replication_doi"].isin(KNOWN_DUPLICATE_REPLICATION_DOIS),
        "promotion_status",
    ] = "held_known_integrated_project_duplicate_risk"

    for row_id, spec in SAFE_ALLOWLIST.items():
        outcome_contains = norm_text(spec["outcome_contains"])
        match = (
            rows["original_doi"].eq(spec["original_doi"])
            & rows["replication_doi"].eq(spec["replication_doi"])
            & rows["description_norm"].str.contains(outcome_contains, regex=False, na=False)
        )
        if match.sum() != 1:
            raise ValueError(f"Allowlist row {row_id} matched {int(match.sum())} API rows")
        rows.loc[match, "promotion_status"] = f"promoted_{row_id}"
        rows.loc[match, "allowlist_row_id"] = row_id
        rows.loc[match, "allowlist_project"] = spec["project"]
        rows.loc[match, "allowlist_source_dataset"] = spec["source_dataset"]

    promoted = rows["promotion_status"].str.startswith("promoted_")
    dup_key = [
        "original_doi",
        "replication_doi",
        "original_n_num",
        "replication_n_num",
        "original_r_num",
        "replication_r_num",
    ]
    duplicate_promoted_value = rows.loc[promoted, dup_key].duplicated(keep="first")
    if duplicate_promoted_value.any():
        dup_indices = duplicate_promoted_value[duplicate_promoted_value].index
        rows.loc[dup_indices, "promotion_status"] = "held_duplicate_promoted_value_tuple"
    return rows


def build_promoted(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates[candidates["promotion_status"].str.startswith("promoted_")].copy()
    records: list[dict[str, Any]] = []
    api_rel = str(API_JSON.relative_to(ROOT))
    api_sha = sha256_file(API_JSON)
    last_updated = json.loads(API_JSON.read_text(encoding="utf-8")).get("lastUpdated", "")
    for _, row in rows.iterrows():
        original_title = clean(row["original_title"]) or clean(row["original_url"])
        replication_title = clean(row["replication_title"]) or clean(row["replication_url"])
        outcome = clean(row["description"])
        row_id = clean(row["allowlist_row_id"])
        records.append(
            {
                "source_dataset": clean(row["allowlist_source_dataset"]),
                "project": clean(row["allowlist_project"]),
                "pair_id": stable_id(
                    "metascience_misc",
                    row_id,
                    row["original_doi"],
                    row["replication_doi"],
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
                "d_n_transformation_note": "Metascience API exposes normalized Pearson r fields. Figure 1 D is abs(2*r/sqrt(1-r^2)). Rows are from an explicit manual allowlist after duplicate/project-noise screening.",
                "replication_type": clean(row["replication_type"]),
                "validated": clean(row["validated"]),
                "replication_initiative_tag": clean(row["replication_initiative_tag"]),
                "metascience_last_updated": last_updated,
                "allowlist_row_id": row_id,
            }
        )
    return pd.DataFrame(records)


def write_summary(candidates: pd.DataFrame, promoted: pd.DataFrame) -> None:
    counts = candidates["promotion_status"].value_counts().rename_axis("status").reset_index(name="rows")
    source_counts = (
        promoted["source_dataset"].value_counts().rename_axis("source_dataset").reset_index(name="rows")
        if not promoted.empty
        else pd.DataFrame(columns=["source_dataset", "rows"])
    )
    lines = [
        "# Metascience Observatory miscellaneous validated promotion",
        "",
        f"- Source API mirror: `{API_JSON.relative_to(ROOT)}`",
        f"- Source SHA-256: `{sha256_file(API_JSON)}`",
        f"- Promoted rows: {len(promoted):,}",
        f"- Promoted CSV: `{PROMOTED_CSV.relative_to(ROOT)}`",
        f"- Audit TSV: `{AUDIT_TSV.relative_to(ROOT)}`",
        "",
        "## Promoted Sources",
        "",
        source_counts.to_markdown(index=False),
        "",
        "## Status Counts",
        "",
        counts.to_markdown(index=False),
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    candidates = prepare_candidates()
    promoted = build_promoted(candidates)
    PROMOTED_CSV.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_TSV.parent.mkdir(parents=True, exist_ok=True)
    promoted.to_csv(PROMOTED_CSV, index=False)
    candidates.to_csv(AUDIT_TSV, sep="\t", index=False)
    write_summary(candidates, promoted)
    print(f"Wrote {len(promoted)} promoted rows: {PROMOTED_CSV.relative_to(ROOT)}")
    print(f"Wrote audit: {AUDIT_TSV.relative_to(ROOT)}")
    print(candidates["promotion_status"].value_counts().head(30).to_string())


if __name__ == "__main__":
    main()
