#!/usr/bin/env python3
"""Check Figure 1 pair-level invariants before counting new rows as progress."""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "FIGURE1_REPLICATION_PAIRS.tsv"
DEFAULT_OUT_DIR = ROOT / "steps" / "corpus_results" / "figure1" / "invariant_checks"
INCLUDED_STATUS = "included_by_current_figure1_dn_rule"

SITE_LEVEL_REPLICATION_SOURCES = {
    "RRR McCarthy 2018 site csvs",
    "O'Donnell 2018 site-level meta csvs",
    "Vaidis 2024 prepared data subset",
    "Alogna 2014 table 1 site counts",
    "RRR Cheung 2016 site csvs",
    "RRR Verschuere 2018 site csv",
    "Stoevenbelt 2025 combined lab csv",
    "PSA-006 trolley country rows",
    "PSA-002 object orientation lab rows",
    "Wagenmakers 2016 site csv",
    "Hagger 2016 RTV.csv",
    "Eerland 2016 Intentionality.csv",
    "Eerland 2016 Intention_attribution.csv",
    "Eerland 2016 imagery.csv",
}

ONE_TO_MANY_SOURCE_DATASETS = SITE_LEVEL_REPLICATION_SOURCES | {
    "Altmejd harmonized Many Labs 1 site-level rows",
    "Altmejd harmonized Many Labs 3 site-level rows",
    "Many Labs 5 site-level single effects",
    "Eyewitness ten-country paper table rescue",
    "Public-admin blame Wiley table reconstruction",
}

SOURCE_DATASET_ONE_TO_MANY_RE = re.compile(
    r"(site[- ]level|site csv|site counts|country rows?|lab rows?|combined lab csv|"
    r"prepared data subset|trolley country rows?|object orientation lab rows?|single effects|"
    r"ten[- ]country|public[- ]admin blame)",
    re.IGNORECASE,
)

LOCAL_PATH_PREFIXES = (
    "data/",
    "docs/",
    "reports/",
    "scripts/",
    "steps/",
    "FIGURE1_",
)


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value)
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    text = clean(value).lower()
    text = re.sub(r"https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(df[column].replace("", np.nan), errors="coerce")


def source_identity(row: pd.Series, doi_col: str, title_col: str) -> str:
    doi = norm_key(row.get(doi_col, ""))
    if doi:
        return f"doi:{doi}"
    title = norm_key(row.get(title_col, ""))
    return f"title:{title}" if title else ""


def looks_external(text: str) -> bool:
    low = text.lower()
    return low.startswith(("http", "doi:", "pmid:", "pmcid:", "nct"))


def path_candidates(path_text: str) -> list[str]:
    candidates: list[str] = []
    for raw in re.split(r"\s+;\s+", clean(path_text)):
        part = raw.strip().strip("|").strip()
        if not part or looks_external(part):
            continue
        base = part.split("::", 1)[0].split("#", 1)[0].strip()
        base = base.strip().strip("|").strip()
        if not base:
            continue
        if "=" in base and "/" not in base:
            continue
        if base.startswith("/") or base.startswith(LOCAL_PATH_PREFIXES):
            candidates.append(base)
    return candidates


def existing_local_paths(path_text: str) -> list[str]:
    existing: list[str] = []
    for candidate in path_candidates(path_text):
        path = Path(candidate)
        full = path if path.is_absolute() else ROOT / path
        if full.exists():
            existing.append(candidate)
    return existing


def rounded_text(value: Any) -> str:
    try:
        return f"{float(value):.8g}"
    except (TypeError, ValueError):
        return clean(value)


def add_records(
    records: list[dict[str, str]],
    rows: pd.DataFrame,
    *,
    severity: str,
    check_id: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> None:
    if rows.empty:
        return
    extra = extra or {}
    for _, row in rows.iterrows():
        record = {
            "severity": severity,
            "check_id": check_id,
            "figure1_replication_pair_id": clean(row.get("figure1_replication_pair_id")),
            "source_dataset": clean(row.get("source_dataset")),
            "project": clean(row.get("project")),
            "native_pair_id": clean(row.get("native_pair_id")),
            "original_title": clean(row.get("original_title")),
            "replication_title": clean(row.get("replication_title")),
            "outcome_label": clean(row.get("outcome_label")),
            "D_original": clean(row.get("D_original")),
            "N_original": clean(row.get("N_original")),
            "D_replication": clean(row.get("D_replication")),
            "N_replication": clean(row.get("N_replication")),
            "source_artifact_local_path": clean(row.get("source_artifact_local_path")),
            "message": message,
        }
        record.update({key: clean(value) for key, value in extra.items()})
        records.append(record)


def duplicate_warnings(included: pd.DataFrame) -> pd.DataFrame:
    if included.empty:
        return pd.DataFrame()
    work = included.copy()
    work["original_identity"] = work.apply(
        lambda row: source_identity(row, "original_doi", "original_title"), axis=1
    )
    work["replication_identity"] = work.apply(
        lambda row: source_identity(row, "replication_doi", "replication_title"), axis=1
    )
    work["outcome_key"] = work["outcome_label"].map(norm_key)
    for col in ["D_original", "N_original", "D_replication", "N_replication"]:
        work[f"{col}_key"] = work[col].map(rounded_text)

    exact_key = [
        "source_dataset",
        "original_identity",
        "replication_identity",
        "outcome_key",
        "D_original_key",
        "N_original_key",
        "D_replication_key",
        "N_replication_key",
    ]
    exact = (
        work.groupby(exact_key, dropna=False)
        .agg(
            row_count=("figure1_replication_pair_id", "size"),
            pair_ids=("figure1_replication_pair_id", lambda s: " | ".join(sorted(map(str, s))[:10])),
        )
        .reset_index()
    )
    exact = exact[exact["row_count"] > 1].copy()
    exact["risk_kind"] = "exact_duplicate_numeric_pair"

    paper_pair_key = ["source_dataset", "original_identity", "replication_identity"]
    paper_pair = (
        work.groupby(paper_pair_key, dropna=False)
        .agg(
            row_count=("figure1_replication_pair_id", "size"),
            outcome_count=("outcome_key", pd.Series.nunique),
            pair_ids=("figure1_replication_pair_id", lambda s: " | ".join(sorted(map(str, s))[:10])),
        )
        .reset_index()
    )
    paper_pair = paper_pair[(paper_pair["row_count"] >= 10) & (paper_pair["outcome_count"] >= 10)].copy()
    paper_pair["risk_kind"] = "many_rows_for_same_source_pair"

    return pd.concat([exact, paper_pair], ignore_index=True, sort=False)


def build_summary(
    df: pd.DataFrame,
    included: pd.DataFrame,
    records: pd.DataFrame,
    duplicate_review: pd.DataFrame,
    out_dir: Path,
    source_evidence_critical: bool,
    batch_source_dataset: list[str],
) -> str:
    severity_counts = (
        records.groupby(["severity", "check_id"]).size().reset_index(name="row_count")
        if not records.empty
        else pd.DataFrame(columns=["severity", "check_id", "row_count"])
    )
    source_counts = included.groupby("source_dataset").size().sort_values(ascending=False)
    critical_count = int((records["severity"] == "critical").sum()) if not records.empty else 0
    warning_count = int((records["severity"] == "warning").sum()) if not records.empty else 0

    lines = [
        "# Figure 1 pair invariant check",
        "",
        f"- Input rows: {len(df):,}",
        f"- Included rows under current D/N rule: {len(included):,}",
        f"- Critical violations: {critical_count:,}",
        f"- Warnings: {warning_count:,}",
        f"- Duplicate/fan-out review groups: {len(duplicate_review):,}",
        f"- Source-evidence gaps are critical: {'yes' if source_evidence_critical else 'no'}",
        f"- Batch source filters: {', '.join(batch_source_dataset) if batch_source_dataset else '(none)'}",
        "",
        "## Check Counts",
        "",
    ]
    if severity_counts.empty:
        lines.append("No critical or warning records were emitted.")
    else:
        lines.append("| Severity | Check | Rows |")
        lines.append("|---|---:|---:|")
        for _, row in severity_counts.iterrows():
            lines.append(f"| {row['severity']} | {row['check_id']} | {int(row['row_count']):,} |")

    lines.extend(["", "## Top Included Sources", "", "| Source dataset | Included rows |", "|---|---:|"])
    for source, count in source_counts.head(40).items():
        lines.append(f"| {source} | {int(count):,} |")

    lines.extend(
        [
            "",
            "## Output Artifacts",
            "",
            f"- Violations and warnings: `{out_dir.relative_to(ROOT) / 'figure1-pair-invariant-violations.tsv'}`",
            f"- Duplicate/fan-out review groups: `{out_dir.relative_to(ROOT) / 'figure1-pair-duplicate-fanout-review.tsv'}`",
            f"- Summary: `{out_dir.relative_to(ROOT) / 'figure1-pair-invariant-summary.md'}`",
        ]
    )
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> int:
    in_path = Path(args.input)
    if not in_path.is_absolute():
        in_path = ROOT / in_path
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(in_path, sep="\t", dtype=str).fillna("")
    included = df[df["current_plot_rule_status"].eq(INCLUDED_STATUS)].copy()
    if args.batch_source_dataset:
        included = included[included["source_dataset"].isin(args.batch_source_dataset)].copy()

    for col in ["D_original", "N_original", "D_replication", "N_replication"]:
        included[f"{col}_num"] = numeric_series(included, col)

    records: list[dict[str, str]] = []
    critical_source_evidence = args.strict_source_evidence or bool(args.batch_source_dataset)
    evidence_severity = "critical" if critical_source_evidence else "warning"

    add_records(
        records,
        included[included["source_dataset"].isin(ONE_TO_MANY_SOURCE_DATASETS)],
        severity="critical",
        check_id="included_from_explicit_one_to_many_source_dataset",
        message="Included row comes from a known site/lab/country one-to-many source dataset.",
    )
    add_records(
        records,
        included[included["source_dataset"].map(lambda value: bool(SOURCE_DATASET_ONE_TO_MANY_RE.search(clean(value))))],
        severity="critical",
        check_id="included_from_one_to_many_source_dataset_name_pattern",
        message="Included row source_dataset name has a site/lab/country one-to-many pattern.",
    )

    finite_mask = np.logical_and.reduce(
        [np.isfinite(included[f"{col}_num"]) for col in ["D_original", "N_original", "D_replication", "N_replication"]]
    )
    add_records(
        records,
        included[~finite_mask],
        severity="critical",
        check_id="included_nonfinite_d_or_n",
        message="Included row has non-finite original or replication D/N.",
    )
    add_records(
        records,
        included[(included["D_original_num"] < 0) | (included["D_replication_num"] < 0)],
        severity="critical",
        check_id="included_negative_d_magnitude",
        message="Included row has a negative D value; Figure 1 stores nonnegative magnitudes.",
    )
    add_records(
        records,
        included[(included["N_original_num"] < 10) | (included["N_replication_num"] < 10)],
        severity="critical",
        check_id="included_current_rule_n_lt_10",
        message="Included row violates the current Figure 1 N >= 10 gate.",
    )
    add_records(
        records,
        included[included["N_replication_num"] <= included["N_original_num"]],
        severity="critical",
        check_id="included_replication_n_not_larger_than_original_n",
        message="Included row violates the current requirement that replication N exceeds original N.",
    )
    add_records(
        records,
        included[included["larger_n_replication"].str.lower().ne("true")],
        severity="critical",
        check_id="included_larger_n_replication_flag_not_true",
        message="Included row has larger_n_replication flag other than true.",
    )

    included["local_path_candidates"] = included["source_artifact_local_path"].map(path_candidates)
    included["existing_local_paths"] = included["source_artifact_local_path"].map(existing_local_paths)
    included["source_artifact_is_url_only"] = included["source_artifact_local_path"].map(
        lambda value: bool(clean(value)) and not path_candidates(value) and looks_external(clean(value).strip().strip("|"))
    )
    add_records(
        records,
        included[included["source_artifact_local_path"].map(clean).eq("")],
        severity=evidence_severity,
        check_id="included_missing_source_artifact_path",
        message="Included row lacks a source_artifact_local_path.",
    )
    add_records(
        records,
        included[included["source_artifact_is_url_only"]],
        severity=evidence_severity,
        check_id="included_source_artifact_url_only",
        message="Included row points only to an external URL, not a repo-local value-bearing source artifact.",
    )
    add_records(
        records,
        included[(included["local_path_candidates"].map(len) > 0) & (included["existing_local_paths"].map(len) == 0)],
        severity=evidence_severity,
        check_id="included_no_existing_local_artifact_found",
        message="Included row records local-looking source paths, but no referenced base artifact exists in this checkout.",
    )
    add_records(
        records,
        included[included["source_artifact_sha256"].map(clean).eq("")],
        severity="warning",
        check_id="included_missing_source_artifact_sha256",
        message="Included row lacks a source_artifact_sha256 checksum.",
    )

    duplicate_review = duplicate_warnings(included)
    if not duplicate_review.empty:
        for _, row in duplicate_review.iterrows():
            records.append(
                {
                    "severity": "warning",
                    "check_id": clean(row.get("risk_kind")),
                    "figure1_replication_pair_id": clean(row.get("pair_ids")),
                    "source_dataset": clean(row.get("source_dataset")),
                    "project": "",
                    "native_pair_id": "",
                    "original_title": clean(row.get("original_identity")),
                    "replication_title": clean(row.get("replication_identity")),
                    "outcome_label": clean(row.get("outcome_key", "")),
                    "D_original": clean(row.get("D_original_key", "")),
                    "N_original": clean(row.get("N_original_key", "")),
                    "D_replication": clean(row.get("D_replication_key", "")),
                    "N_replication": clean(row.get("N_replication_key", "")),
                    "source_artifact_local_path": "",
                    "message": f"Review duplicate/fan-out risk group with {int(row.get('row_count', 0))} rows.",
                }
            )

    records_df = pd.DataFrame(records)
    violation_path = out_dir / "figure1-pair-invariant-violations.tsv"
    duplicate_path = out_dir / "figure1-pair-duplicate-fanout-review.tsv"
    summary_path = out_dir / "figure1-pair-invariant-summary.md"
    if records_df.empty:
        records_df = pd.DataFrame(
            columns=[
                "severity",
                "check_id",
                "figure1_replication_pair_id",
                "source_dataset",
                "project",
                "native_pair_id",
                "original_title",
                "replication_title",
                "outcome_label",
                "D_original",
                "N_original",
                "D_replication",
                "N_replication",
                "source_artifact_local_path",
                "message",
            ]
        )
    records_df.to_csv(violation_path, sep="\t", index=False)
    duplicate_review.to_csv(duplicate_path, sep="\t", index=False)
    summary_path.write_text(
        build_summary(
            df,
            included,
            records_df,
            duplicate_review,
            out_dir,
            critical_source_evidence,
            args.batch_source_dataset,
        ),
        encoding="utf-8",
    )

    critical_count = int((records_df["severity"] == "critical").sum())
    warning_count = int((records_df["severity"] == "warning").sum())
    print(f"input_rows={len(df)}")
    print(f"included_rows_checked={len(included)}")
    print(f"critical_violations={critical_count}")
    print(f"warnings={warning_count}")
    print(f"summary={summary_path.relative_to(ROOT)}")
    if args.fail_on_critical and critical_count:
        return 1
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT.relative_to(ROOT)))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR.relative_to(ROOT)))
    parser.add_argument(
        "--batch-source-dataset",
        action="append",
        default=[],
        help="Restrict checks to included rows from this source_dataset and make source-evidence gaps critical.",
    )
    parser.add_argument(
        "--strict-source-evidence",
        action="store_true",
        help="Treat source artifact URL-only/missing-local evidence gaps as critical for all checked rows.",
    )
    parser.add_argument("--fail-on-critical", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(run(parse_args()))
