#!/usr/bin/env python3
"""Promote reviewed singleton direct rows from the mirrored Metascience API.

This keeps the unreviewed Metascience bucket narrow: DOI-backed direct/close
rows only, one row per DOI pair, finite normalized r/N fields, current D/N
gates, and explicit duplicate screening against the current root table.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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
    / "metascience_observatory_singleton_direct__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "metascience_observatory_singleton_direct_20260508"
    / "metascience-singleton-direct-promotion-audit.tsv"
)
SUMMARY_MD = AUDIT_TSV.with_name("metascience-singleton-direct-promotion-summary.md")


SAFE_ROWS = {
    (
        "10.1111/j.1467-9280.2008.02053.x",
        "10.17605/osf.io/73pnd",
        "errors are aversive",
    ): {
        "project": "Replication Project: Psychology",
        "source_dataset": "Metascience Observatory FReD API singleton direct rows",
    },
    (
        "10.1037/0022-3514.94.4.615",
        "10.17605/osf.io/etg7c",
        "social identity contingencies",
    ): {
        "project": "Individual direct replication",
        "source_dataset": "Metascience Observatory FReD API singleton direct rows",
    },
    (
        "10.1111/j.1467-9280.2008.02057.x",
        "10.17605/osf.io/hpk2m",
        "precision of the anchor",
    ): {
        "project": "Replication Project: Psychology",
        "source_dataset": "Metascience Observatory FReD API singleton direct rows",
    },
    (
        "10.1111/j.1467-9280.2006.01704.x",
        "10.17605/osf.io/q6tv8",
        "cognitive busyness",
    ): {
        "project": "Individual direct replication",
        "source_dataset": "Metascience Observatory FReD API singleton direct rows",
    },
    (
        "10.1111/j.1467-9280.2008.02091.x",
        "10.17605/osf.io/vqzx9",
        "sunny side of fairness",
    ): {
        "project": "Replication Project: Psychology",
        "source_dataset": "Metascience Observatory FReD API singleton direct rows",
    },
}


def value_tuple(row: pd.Series) -> tuple[float, int, float, int]:
    return (
        round(abs(scalar_r_to_d(row["original_r_num"])), 5),
        int(round(float(row["original_n_num"]))),
        round(abs(scalar_r_to_d(row["replication_r_num"])), 5),
        int(round(float(row["replication_n_num"]))),
    )


def current_root_keys() -> set[tuple[str, str, str, tuple[float, int, float, int]]]:
    if not ROOT_TSV.exists():
        return set()
    root = pd.read_csv(ROOT_TSV, sep="\t", dtype=str).fillna("")
    for col in ["D_original", "N_original", "D_replication", "N_replication"]:
        root[col] = pd.to_numeric(root[col], errors="coerce")
    keys: set[tuple[str, str, str, tuple[float, int, float, int]]] = set()
    for _, row in root.iterrows():
        original_doi = clean(row["original_doi"]).lower()
        replication_doi = clean(row["replication_doi"]).lower()
        outcome = norm_text(row["outcome_label"])
        if not original_doi or not replication_doi:
            continue
        if pd.isna(row["D_original"]) or pd.isna(row["D_replication"]):
            continue
        values = (
            round(float(row["D_original"]), 5),
            int(round(float(row["N_original"]))),
            round(float(row["D_replication"]), 5),
            int(round(float(row["N_replication"]))),
        )
        keys.add((original_doi, replication_doi, outcome, values))
    return keys


def load_candidates() -> pd.DataFrame:
    rows = pd.DataFrame(json.loads(API_JSON.read_text(encoding="utf-8"))["rows"]).fillna("")
    rows["original_n_num"] = to_num(rows["original_n"]).fillna(to_num(rows["n_original"]))
    rows["replication_n_num"] = to_num(rows["replication_n"]).fillna(to_num(rows["n_replication"]))
    rows["original_r_num"] = to_num(rows["original_es_r"]).fillna(to_num(rows["es_original"]))
    rows["replication_r_num"] = to_num(rows["replication_es_r"]).fillna(to_num(rows["es_replication"]))
    rows["original_doi"] = rows["original_url"].map(doi_from_url)
    rows["replication_doi"] = rows["replication_url"].map(doi_from_url)
    rows["description_norm"] = rows["description"].map(norm_text)
    rows["promotion_status"] = "held_not_singleton_allowlist"

    root_keys = current_root_keys()
    selected_indices: list[int] = []
    for (original_doi, replication_doi, description_token), spec in SAFE_ROWS.items():
        match = (
            rows["original_doi"].eq(original_doi)
            & rows["replication_doi"].eq(replication_doi)
            & rows["description_norm"].str.contains(description_token, regex=False, na=False)
        )
        if int(match.sum()) != 1:
            raise ValueError(
                f"Safe singleton row {original_doi} / {replication_doi} / {description_token} "
                f"matched {int(match.sum())} API rows"
            )
        idx = int(rows.index[match][0])
        row = rows.loc[idx]
        directish = "direct" in clean(row["replication_type"]).lower() or "close" in clean(
            row["replication_type"]
        ).lower()
        numeric = row[["original_n_num", "replication_n_num", "original_r_num", "replication_r_num"]].notna().all()
        passes_dn = bool(
            numeric
            and row["original_n_num"] >= 10
            and row["replication_n_num"] >= 10
            and row["replication_n_num"] > row["original_n_num"]
            and abs(row["original_r_num"]) < 1
            and abs(row["replication_r_num"]) < 1
        )
        root_key = (
            original_doi,
            replication_doi,
            norm_text(row["description"]),
            value_tuple(row),
        )
        if clean(row["validated"]).lower() != "yes":
            rows.loc[idx, "promotion_status"] = "held_not_validated_yes"
        elif not directish:
            rows.loc[idx, "promotion_status"] = "held_not_direct_or_close"
        elif not passes_dn:
            rows.loc[idx, "promotion_status"] = "held_failed_current_dn_gate"
        elif root_key in root_keys:
            rows.loc[idx, "promotion_status"] = "held_existing_exact_root_row"
        else:
            rows.loc[idx, "promotion_status"] = "promoted_singleton_direct"
            rows.loc[idx, "singleton_project"] = spec["project"]
            rows.loc[idx, "singleton_source_dataset"] = spec["source_dataset"]
            selected_indices.append(idx)

    rows["selected_for_singleton_review"] = rows.index.isin(selected_indices)
    return rows


def build_promoted(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates[candidates["promotion_status"].eq("promoted_singleton_direct")].copy()
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
                "source_dataset": clean(row["singleton_source_dataset"]),
                "project": clean(row["singleton_project"]),
                "pair_id": stable_id(
                    "metascience_singleton_direct",
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
                "verbatim_n_text_original": (
                    f"Metascience API row: original_n={row['original_n']}; n_original={row['n_original']}"
                ),
                "verbatim_n_text_replication": (
                    f"Metascience API row: replication_n={row['replication_n']}; "
                    f"n_replication={row['n_replication']}"
                ),
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
                    "abs(2*r/sqrt(1-r^2)); signed r is preserved in verbatim effect text. "
                    "Rows are reviewed singleton DOI-backed direct/close pairs from the "
                    "previously unreviewed misc bucket."
                ),
                "replication_type": clean(row["replication_type"]),
                "validated": clean(row["validated"]),
                "replication_initiative_tag": clean(row["replication_initiative_tag"]),
                "metascience_source": clean(row["source"]),
                "metascience_last_updated": last_updated,
            }
        )
    return pd.DataFrame(records)


def write_outputs(candidates: pd.DataFrame, promoted: pd.DataFrame) -> None:
    PROMOTED_CSV.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_TSV.parent.mkdir(parents=True, exist_ok=True)
    promoted.to_csv(PROMOTED_CSV, index=False)
    candidates.to_csv(AUDIT_TSV, sep="\t", index=False)

    selected = candidates[candidates["promotion_status"].ne("held_not_singleton_allowlist")].copy()
    status_counts = selected["promotion_status"].value_counts().rename_axis("status").reset_index(name="rows")
    lines = [
        "# Metascience Singleton Direct Promotion",
        "",
        f"- Source API mirror: `{API_JSON.relative_to(ROOT)}`",
        f"- Source SHA-256: `{sha256_file(API_JSON)}`",
        f"- Reviewed singleton rows: {len(selected):,}",
        f"- Promoted rows: {len(promoted):,}",
        f"- Promoted CSV: `{PROMOTED_CSV.relative_to(ROOT)}`",
        f"- Audit TSV: `{AUDIT_TSV.relative_to(ROOT)}`",
        "",
        "## Status Counts",
        "",
        status_counts.to_markdown(index=False),
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    candidates = load_candidates()
    promoted = build_promoted(candidates)
    write_outputs(candidates, promoted)
    print(f"Wrote {len(promoted)} promoted rows: {PROMOTED_CSV.relative_to(ROOT)}")
    print(candidates[candidates["promotion_status"].ne("held_not_singleton_allowlist")]["promotion_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
