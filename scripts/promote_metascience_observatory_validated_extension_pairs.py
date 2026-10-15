#!/usr/bin/env python3
"""Promote validated Metascience/FReD API extension rows.

The rows selected here are source-result rows from the mirrored Metascience
FReD API.  The gate is deliberately narrower than the API: validated
direct/close rows only, finite normalized r and N fields, DOI-backed identities
on both sides, no CurateScience rows, no exact numeric duplicate already in the
root table, and only source families with explicit original/replication result
mapping rather than site/lab fan-out.
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
    / "metascience_observatory_validated_extension__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "metascience_observatory_validated_extension_20260508"
    / "metascience-validated-extension-promotion-audit.tsv"
)
SUMMARY_MD = AUDIT_TSV.with_name("metascience-validated-extension-promotion-summary.md")


SOURCE_DATASET_BY_TAG = {
    "": "Metascience Observatory FReD API validated blank-tag rows",
    "Soto et al LOPPRP": "Metascience Observatory FReD API Soto LOPPRP extension rows",
    "RSESR": "Metascience Observatory FReD API RSESR extension rows",
    "SPRRR": "Metascience Observatory FReD API SPRRR extension rows",
}
PROJECT_BY_TAG = {
    "": "Metascience Observatory validated direct/close rows",
    "Soto et al LOPPRP": "Life Outcomes of Personality Replication Project",
    "RSESR": "Replicability of Sports and Exercise Science Research",
    "SPRRR": "Social Psychology Registered Replication Reports",
}
OWN_SOURCE_DATASETS = set(SOURCE_DATASET_BY_TAG.values())


# These replication projects are already represented by dedicated parsers in the
# root table.  They are not promoted from the untagged Metascience bucket here
# even when the API supplies a DOI and value tuple.
KNOWN_INTEGRATED_REPLICATION_DOIS_FOR_BLANK_TAG = {
    "10.1126/science.aac4716",
    "10.1007/s13164-018-0400-9",
    "10.1177/2515245918810225",
    "10.1177/2515245920958687",
    "10.1177/2515245920927643",
    "10.1177/2515245920917931",
    "10.1177/2515245918781032",
    "10.1016/j.jesp.2015.10.012",
}


def rounded_d(value: Any) -> float | None:
    value = pd.to_numeric(value, errors="coerce")
    if not np.isfinite(value):
        return None
    return round(float(value), 5)


def rounded_n(value: Any) -> int | None:
    value = pd.to_numeric(value, errors="coerce")
    if not np.isfinite(value):
        return None
    return int(round(float(value)))


def value_tuple(row: pd.Series | dict[str, Any]) -> tuple[float | None, int | None, float | None, int | None]:
    return (
        rounded_d(row["D_original"]),
        rounded_n(row["N_original"]),
        rounded_d(row["D_replication"]),
        rounded_n(row["N_replication"]),
    )


def directish(value: Any) -> bool:
    text = clean(value).lower()
    return "direct" in text or "close" in text


def load_existing_value_keys() -> dict[str, set[tuple[Any, ...]]]:
    root = pd.read_csv(ROOT_TSV, sep="\t", dtype=str).fillna("")
    root = root[~root["source_dataset"].isin(OWN_SOURCE_DATASETS)].copy()
    for col in ["D_original", "N_original", "D_replication", "N_replication"]:
        root[col] = pd.to_numeric(root[col], errors="coerce")
    root["original_doi_norm"] = root["original_doi"].str.lower().str.strip()
    root["replication_doi_norm"] = root["replication_doi"].str.lower().str.strip()
    root["original_title_norm"] = root["original_title"].map(norm_text)
    root["replication_title_norm"] = root["replication_title"].map(norm_text)
    root["outcome_norm"] = root["outcome_label"].map(norm_text)

    keys: dict[str, set[tuple[Any, ...]]] = {
        "doi_pair_value": set(),
        "title_pair_value": set(),
        "original_value": set(),
        "original_outcome_value": set(),
    }
    for _, row in root.iterrows():
        values = value_tuple(row)
        original_doi = clean(row["original_doi_norm"])
        replication_doi = clean(row["replication_doi_norm"])
        original_title = clean(row["original_title_norm"])
        replication_title = clean(row["replication_title_norm"])
        outcome = clean(row["outcome_norm"])
        if original_doi and replication_doi:
            keys["doi_pair_value"].add((original_doi, replication_doi, *values))
        if original_title and replication_title:
            keys["title_pair_value"].add((original_title, replication_title, *values))
        if original_doi:
            keys["original_value"].add((f"doi:{original_doi}", *values))
        if original_title:
            keys["original_value"].add((f"title:{original_title}", *values))
        if original_doi and outcome:
            keys["original_outcome_value"].add((f"doi:{original_doi}", outcome, *values))
    return keys


def is_existing_numeric_duplicate(row: pd.Series, keys: dict[str, set[tuple[Any, ...]]]) -> bool:
    values = value_tuple(row)
    original_doi = clean(row["original_doi"])
    replication_doi = clean(row["replication_doi"])
    original_title = clean(row["original_title_norm"])
    replication_title = clean(row["replication_title_norm"])
    outcome = clean(row["description_norm"])

    if original_doi and replication_doi and (original_doi, replication_doi, *values) in keys["doi_pair_value"]:
        return True
    if original_title and replication_title and (
        original_title,
        replication_title,
        *values,
    ) in keys["title_pair_value"]:
        return True
    if original_doi and (f"doi:{original_doi}", *values) in keys["original_value"]:
        return True
    if original_title and (f"title:{original_title}", *values) in keys["original_value"]:
        return True
    if original_doi and outcome and (f"doi:{original_doi}", outcome, *values) in keys[
        "original_outcome_value"
    ]:
        return True
    return False


def prepare_candidates() -> pd.DataFrame:
    payload = json.loads(API_JSON.read_text(encoding="utf-8"))
    rows = pd.DataFrame(payload["rows"]).fillna("")
    rows = rows.reset_index(names="api_row_index")

    rows["original_n_num"] = to_num(rows["original_n"]).fillna(to_num(rows["n_original"]))
    rows["replication_n_num"] = to_num(rows["replication_n"]).fillna(to_num(rows["n_replication"]))
    rows["original_r_num"] = to_num(rows["original_es_r"]).fillna(to_num(rows["es_original"]))
    rows["replication_r_num"] = to_num(rows["replication_es_r"]).fillna(to_num(rows["es_replication"]))
    rows["D_original"] = rows["original_r_num"].map(lambda x: abs(scalar_r_to_d(x)))
    rows["D_replication"] = rows["replication_r_num"].map(lambda x: abs(scalar_r_to_d(x)))
    rows["N_original"] = rows["original_n_num"]
    rows["N_replication"] = rows["replication_n_num"]
    rows["original_doi"] = rows["original_url"].map(doi_from_url)
    rows["replication_doi"] = rows["replication_url"].map(doi_from_url)
    rows["original_title_norm"] = rows["original_title"].map(norm_text)
    rows["replication_title_norm"] = rows["replication_title"].map(norm_text)
    rows["description_norm"] = rows["description"].map(norm_text)
    rows["promotion_status"] = "held_not_in_allowed_source_family"

    allowed_family = rows["replication_initiative_tag"].isin(SOURCE_DATASET_BY_TAG)
    rows.loc[allowed_family, "promotion_status"] = "held_pending_gate"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate") & rows["source"].eq("Curate Science scrape"),
        "promotion_status",
    ] = "held_curatescience_mapping_noise"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate") & ~rows["validated"].str.lower().eq("yes"),
        "promotion_status",
    ] = "held_not_validated_yes"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate") & ~rows["replication_type"].map(directish),
        "promotion_status",
    ] = "held_not_direct_or_close"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate")
        & ~rows[["original_n_num", "replication_n_num", "original_r_num", "replication_r_num"]]
        .notna()
        .all(axis=1),
        "promotion_status",
    ] = "held_missing_numeric_r_or_n"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate")
        & (
            rows["original_n_num"].lt(10)
            | rows["replication_n_num"].lt(10)
            | rows["replication_n_num"].le(rows["original_n_num"])
            | rows["original_r_num"].abs().ge(1)
            | rows["replication_r_num"].abs().ge(1)
        ),
        "promotion_status",
    ] = "held_failed_current_dn_gate"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate")
        & (rows["original_doi"].eq("") | rows["replication_doi"].eq("")),
        "promotion_status",
    ] = "held_missing_doi_backed_pair_identity"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate") & rows["description_norm"].eq(""),
        "promotion_status",
    ] = "held_missing_outcome_description"
    rows.loc[
        rows["promotion_status"].eq("held_pending_gate")
        & rows["replication_initiative_tag"].eq("")
        & rows["replication_doi"].isin(KNOWN_INTEGRATED_REPLICATION_DOIS_FOR_BLANK_TAG),
        "promotion_status",
    ] = "held_blank_tag_known_integrated_project_duplicate_risk"

    existing_keys = load_existing_value_keys()
    pending = rows["promotion_status"].eq("held_pending_gate")
    duplicate_mask = pd.Series(False, index=rows.index)
    duplicate_mask.loc[pending] = rows.loc[pending].apply(
        lambda row: is_existing_numeric_duplicate(row, existing_keys), axis=1
    )
    rows.loc[pending & duplicate_mask, "promotion_status"] = "held_existing_numeric_duplicate"

    promotable = rows["promotion_status"].eq("held_pending_gate")
    within_key_cols = [
        "replication_initiative_tag",
        "original_doi",
        "replication_doi",
        "description_norm",
        "D_original",
        "N_original",
        "D_replication",
        "N_replication",
    ]
    duplicated = rows.loc[promotable, within_key_cols].duplicated(keep="first")
    if not duplicated.empty:
        rows.loc[duplicated[duplicated].index, "promotion_status"] = "held_duplicate_within_candidate_set"

    rows.loc[rows["promotion_status"].eq("held_pending_gate"), "promotion_status"] = "promoted"
    return rows


def build_promoted(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates[candidates["promotion_status"].eq("promoted")].copy()
    records: list[dict[str, Any]] = []
    api_rel = str(API_JSON.relative_to(ROOT))
    api_sha = sha256_file(API_JSON)
    last_updated = json.loads(API_JSON.read_text(encoding="utf-8")).get("lastUpdated", "")
    for _, row in rows.iterrows():
        tag = clean(row["replication_initiative_tag"])
        source_dataset = SOURCE_DATASET_BY_TAG[tag]
        original_title = clean(row["original_title"]) or clean(row["original_url"])
        replication_title = clean(row["replication_title"]) or clean(row["replication_url"])
        outcome = clean(row["description"])
        records.append(
            {
                "source_dataset": source_dataset,
                "project": PROJECT_BY_TAG[tag],
                "pair_id": stable_id(
                    "metascience_validated_extension",
                    row["api_row_index"],
                    tag,
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
                "D_original": float(row["D_original"]),
                "N_original": float(row["N_original"]),
                "D_replication": float(row["D_replication"]),
                "N_replication": float(row["N_replication"]),
                "raw_file": api_rel,
                "n_source_file": api_rel,
                "match_author": f"{original_title} | {outcome}",
                "source_artifact_sha256": api_sha,
                "verbatim_n_text_original": f"Metascience API row {row['api_row_index']}: original_n={row['original_n']}; n_original={row['n_original']}",
                "verbatim_n_text_replication": f"Metascience API row {row['api_row_index']}: replication_n={row['replication_n']}; n_replication={row['n_replication']}",
                "verbatim_effect_text_original": (
                    f"Metascience API row {row['api_row_index']}: original_es_r={row['original_es_r']}; "
                    f"es_original={row['es_original']}; original_es={row['original_es']}"
                ),
                "verbatim_effect_text_replication": (
                    f"Metascience API row {row['api_row_index']}: replication_es_r={row['replication_es_r']}; "
                    f"es_replication={row['es_replication']}; replication_es={row['replication_es']}"
                ),
                "d_n_transformation_note": (
                    "Metascience API exposes normalized Pearson r fields. Figure 1 D is "
                    "abs(2*r/sqrt(1-r^2)); signed r is preserved in verbatim effect text. "
                    "Rows passed validated/direct-or-close/DN gates and exact numeric "
                    "root-duplicate screening."
                ),
                "replication_type": clean(row["replication_type"]),
                "validated": clean(row["validated"]),
                "replication_initiative_tag": tag,
                "metascience_source": clean(row["source"]),
                "metascience_last_updated": last_updated,
                "api_row_index": int(row["api_row_index"]),
            }
        )
    return pd.DataFrame(records)


def write_summary(candidates: pd.DataFrame, promoted: pd.DataFrame) -> None:
    status_counts = (
        candidates["promotion_status"].value_counts().rename_axis("status").reset_index(name="rows")
    )
    source_counts = (
        promoted["source_dataset"].value_counts().rename_axis("source_dataset").reset_index(name="rows")
        if not promoted.empty
        else pd.DataFrame(columns=["source_dataset", "rows"])
    )
    lines = [
        "# Metascience Observatory validated extension promotion",
        "",
        f"- Source API mirror: `{API_JSON.relative_to(ROOT)}`",
        f"- Source SHA-256: `{sha256_file(API_JSON)}`",
        f"- Promoted rows: {len(promoted):,}",
        f"- Promoted CSV: `{PROMOTED_CSV.relative_to(ROOT)}`",
        f"- Audit TSV: `{AUDIT_TSV.relative_to(ROOT)}`",
        "",
        "## Promotion Gate",
        "",
        "Rows are promoted only when they are validated, direct/close, non-CurateScience, "
        "DOI-backed on both sides, have finite normalized r and N fields, pass the current "
        "Figure 1 D/N gate, and are not exact numeric duplicates already represented in "
        "the root table. Untagged rows with known integrated replication-project DOIs are held.",
        "",
        "## Promoted Sources",
        "",
        source_counts.to_markdown(index=False),
        "",
        "## Status Counts",
        "",
        status_counts.to_markdown(index=False),
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
    print(f"Wrote summary: {SUMMARY_MD.relative_to(ROOT)}")
    print(candidates["promotion_status"].value_counts().head(40).to_string())


if __name__ == "__main__":
    main()
