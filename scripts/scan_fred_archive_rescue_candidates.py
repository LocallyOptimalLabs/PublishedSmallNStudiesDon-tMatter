from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path("FIGURE1_REPLICATION_PAIRS.tsv")
DEFAULT_ARCHIVE = Path("data/raw/corpus_candidates/fred/freshness_check_2026-04-27/FReD_2.4.1.archive.xlsx")
DEFAULT_OUT_DIR = Path("steps/corpus_results/figure1/fred_archive_rescue_20260507")


KNOWN_OVERLAP_SOURCES = {
    "Boyce_etal2023",
    "OSC 2015",
    "SSRP",
    "XPHI",
    "openmkt",
}


def norm_doi(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text.replace(" ", "")


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scalar_r_to_d(value: object) -> float:
    r = pd.to_numeric(value, errors="coerce")
    if not np.isfinite(r) or abs(float(r)) >= 1:
        return np.nan
    return float(2 * float(r) / np.sqrt(1 - float(r) ** 2))


def first_nonempty(*values: object) -> str:
    for value in values:
        if pd.isna(value):
            continue
        text = str(value).strip()
        if text and text.lower() != "nan":
            return text
    return ""


def status_for_row(row: pd.Series) -> str:
    if not row["validated_complete"]:
        return "not_value_complete"
    if not row["passes_figure1_mechanical_gate"]:
        return "blocked_by_current_dn_gate"
    if row["source"] in KNOWN_OVERLAP_SOURCES:
        return "known_project_overlap_hold"
    if row["doi_pair_in_root"] or row["doi_pair_outcome_in_root"]:
        return "duplicate_doi_pair_hold"
    if row["title_pair_outcome_in_root"]:
        return "duplicate_title_pair_hold"
    if row["strict_same_design_same_test"] and row["has_row_label"]:
        return "high_precision_candidate"
    return "needs_manual_match_or_duplicate_review"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", default=str(DEFAULT_ARCHIVE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    archive_path = Path(args.archive)
    out_dir = Path(args.out_dir)
    audit_tsv = out_dir / "fred-archive-rescue-candidate-scan.tsv"
    summary_md = out_dir / "fred-archive-rescue-candidate-summary.md"

    out_dir.mkdir(parents=True, exist_ok=True)

    archive = pd.read_excel(archive_path, sheet_name="Data", header=0, skiprows=[1, 2])
    root = pd.read_csv(ROOT, sep="\t")
    root["doi_o_norm"] = root["original_doi"].map(norm_doi)
    root["doi_r_norm"] = root["replication_doi"].map(norm_doi)
    root["out_norm"] = root["outcome_label"].map(norm_text)
    root_pairs = set(zip(root["doi_o_norm"], root["doi_r_norm"]))
    root_pair_outcomes = set(zip(root["doi_o_norm"], root["doi_r_norm"], root["out_norm"]))
    root_title_pair_outcomes = set(
        zip(
            root["original_title"].map(norm_text),
            root["replication_title"].map(norm_text),
            root["outcome_label"].map(norm_text),
        )
    )

    d = archive.copy()
    for col in ["validated", "es_original", "es_replication", "n_original", "n_replication", "same_design", "same_test"]:
        d[f"{col}_num"] = pd.to_numeric(d[col], errors="coerce")

    d["source"] = d["source"].fillna("").astype(str)
    d["doi_o_norm"] = d["doi_original"].map(norm_doi)
    d["doi_r_norm"] = d["doi_replication"].map(norm_doi)
    d["out_norm"] = d["outcome"].map(norm_text)
    d["row_label"] = [
        first_nonempty(effect, outcome, study_o, study_r, rowid)
        for effect, outcome, study_o, study_r, rowid in zip(
            d["effect"],
            d["outcome"],
            d["study_original"],
            d["study_replication"],
            d["rowid"],
        )
    ]
    d["has_row_label"] = d["row_label"].map(bool)
    d["explicit_exclusion_blank"] = d["exclusion"].isna() | d["exclusion"].astype(str).str.strip().eq("")
    d["validated_complete"] = (
        d["validated_num"].isin([1, 2])
        & d["es_original_num"].notna()
        & d["es_replication_num"].notna()
        & d["n_original_num"].notna()
        & d["n_replication_num"].notna()
        & d["explicit_exclusion_blank"]
    )
    d["passes_figure1_mechanical_gate"] = (
        d["validated_complete"]
        & (d["n_original_num"] >= 10)
        & (d["n_replication_num"] >= 10)
        & (d["n_replication_num"] > d["n_original_num"])
        & np.isfinite(d["es_original_num"])
        & np.isfinite(d["es_replication_num"])
    )
    d["strict_same_design_same_test"] = d["same_design_num"].eq(1) & d["same_test_num"].eq(1)
    d["doi_pair_in_root"] = [
        bool((o or r) and (o, r) in root_pairs) for o, r in zip(d["doi_o_norm"], d["doi_r_norm"])
    ]
    d["doi_pair_outcome_in_root"] = [
        bool((o or r) and out and (o, r, out) in root_pair_outcomes)
        for o, r, out in zip(d["doi_o_norm"], d["doi_r_norm"], d["out_norm"])
    ]
    d["title_pair_outcome_in_root"] = [
        bool(out and (norm_text(o), norm_text(r), out) in root_title_pair_outcomes)
        for o, r, out in zip(d["ref_original"], d["ref_replication"], d["out_norm"])
    ]
    d["archive_rescue_status"] = d.apply(status_for_row, axis=1)
    d["D_original_magnitude"] = d["es_original_num"].map(scalar_r_to_d).abs()
    d["D_replication_magnitude"] = d["es_replication_num"].map(scalar_r_to_d).abs()
    d["source_artifact_local_path"] = str(archive_path)
    d["source_artifact_sha256"] = sha256_file(archive_path)
    d["d_n_transformation_note"] = (
        "FReD archive Key Variables sheet defines es_original/es_replication as effect sizes converted "
        "to Pearson r; Figure 1 D is abs(2*r/sqrt(1-r^2))."
    )

    columns = [
        "archive_rescue_status",
        "rowid",
        "id",
        "validated",
        "source",
        "effect",
        "outcome",
        "study_original",
        "study_replication",
        "result",
        "same_design",
        "same_test",
        "es_original",
        "n_original",
        "es_replication",
        "n_replication",
        "D_original_magnitude",
        "D_replication_magnitude",
        "doi_original",
        "doi_replication",
        "ref_original",
        "ref_replication",
        "claim_text_orig",
        "claim_statistics_orig",
        "description",
        "notes",
        "notes_validation",
        "exclusion",
        "validated_complete",
        "passes_figure1_mechanical_gate",
        "strict_same_design_same_test",
        "doi_pair_in_root",
        "doi_pair_outcome_in_root",
        "title_pair_outcome_in_root",
        "source_artifact_local_path",
        "source_artifact_sha256",
        "d_n_transformation_note",
    ]
    d[columns].to_csv(audit_tsv, sep="\t", index=False)

    status_counts = d["archive_rescue_status"].value_counts().rename_axis("status").reset_index(name="rows")
    source_counts = (
        d.loc[d["passes_figure1_mechanical_gate"]]
        .groupby(["source", "archive_rescue_status"], dropna=False)
        .size()
        .rename("rows")
        .reset_index()
        .sort_values(["source", "archive_rescue_status"])
    )
    lines = [
        "# FReD Archive Rescue Candidate Scan",
        "",
        "This is a duplicate-aware audit projection over the archived FReD workflow workbook. It does not promote rows.",
        "",
        f"- Source workbook: `{archive_path}`",
        f"- Source SHA-256: `{sha256_file(archive_path)}`",
        f"- Audit TSV: `{audit_tsv}`",
        f"- Archive rows scanned: {len(d)}",
        f"- Complete validated rows with no explicit exclusion: {int(d['validated_complete'].sum())}",
        f"- Rows passing current Figure 1 mechanical D/N gates: {int(d['passes_figure1_mechanical_gate'].sum())}",
        "",
        "## Status Counts",
        "",
        status_counts.to_markdown(index=False),
        "",
        "## Figure 1 Gate Rows by Source and Status",
        "",
        source_counts.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "The high-precision bucket requires a complete validated row, current D/N gates, no current root duplicate flag, "
        "and explicit `same_design == 1` plus `same_test == 1`. Other mechanically complete rows remain useful as a review queue, "
        "but they should not be bulk-promoted without row-level match and duplicate review.",
        "",
    ]
    summary_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {audit_tsv}")
    print(f"Wrote {summary_md}")
    print(status_counts.to_string(index=False))


if __name__ == "__main__":
    main()
