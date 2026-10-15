#!/usr/bin/env python3
"""Promote conservative rows from Sobkow et al. 2022 Polish JDM replications."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    ROOT
    / "data"
    / "raw"
    / "replication_projects"
    / "individual_search_batch004"
    / "api_candidate_cea01115b41068aa"
)
MAIN_PDF = RAW_DIR / "01_journals_pan_pl_content_124284_pdf_master_2022_03_ppb_02_sobkow_pdf_e4a9cdfe8e9f.pdf"
SUPPLEMENT = RAW_DIR / "osf_svge5_supplement_table_s1.pdf"
OUT_CSV = (
    ROOT
    / "data"
    / "derived"
    / "replication_pairs"
    / "harvest"
    / "promoted"
    / "jdm_polish_conceptual_replications__promoted_pairs.csv"
)
AUDIT_TSV = (
    ROOT
    / "steps"
    / "corpus_results"
    / "figure1"
    / "jdm_polish_conceptual_replications"
    / "jdm-polish-conceptual-replications-promoted-audit.tsv"
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
    "original_source_text",
    "replication_source_text",
    "conversion_note",
    "selection_note",
]


def r_to_d(r: float) -> float:
    return 2 * abs(r) / math.sqrt(1 - r * r)


def clean(value: Any) -> str:
    return str(value).replace("\t", " ").replace("\n", " ").replace("\r", " ").strip()


def row(
    pair_id: str,
    original_title: str,
    original_doi: str,
    outcome: str,
    d_original: float,
    n_original: int,
    d_replication: float,
    n_replication: int,
    match_author: str,
    original_source_text: str,
    replication_source_text: str,
    conversion_note: str,
) -> dict[str, Any]:
    return {
        "source_dataset": "Sobkow et al. 2022 Polish JDM conceptual replication",
        "project": "Polish JDM conceptual replications",
        "pair_id": pair_id,
        "original_title": original_title,
        "replication_title": "Conceptual replication study of fifteen JDM effects: Insights from the Polish sample",
        "original_doi": original_doi,
        "replication_doi": "10.24425/ppb.2022.141862",
        "outcome": outcome,
        "D_original": f"{d_original:.6g}",
        "N_original": str(n_original),
        "D_replication": f"{d_replication:.6g}",
        "N_replication": str(n_replication),
        "raw_file": f"{MAIN_PDF.relative_to(ROOT)} ; {SUPPLEMENT.relative_to(ROOT)}",
        "match_author": match_author,
        "original_source_text": original_source_text,
        "replication_source_text": replication_source_text,
        "conversion_note": conversion_note,
        "selection_note": (
            "Promoted from Sobkow et al. Supplementary Table S1 only when the source gives a matched "
            "original/replication effect, the replication N is larger, and the metric is already Cohen's d "
            "or a simple Pearson/point-biserial r converted with d = 2r/sqrt(1-r^2)."
        ),
    }


def build_rows() -> list[dict[str, Any]]:
    return [
        row(
            pair_id="jdm_polish_s01_dependent_decision_style_procrastination",
            original_title="Relating Decision-Making Styles to Social Orientation and Time Approach",
            original_doi="10.1002/bdm.2066",
            outcome="Dependent decision-making style and procrastination correlation",
            d_original=r_to_d(0.277),
            n_original=118,
            d_replication=r_to_d(0.165),
            n_replication=202,
            match_author="Sobkow_2022_S01_Geisler_Allwood_2018",
            original_source_text=(
                "Main PDF describes Geisler and Allwood's original sample as 118 Swedish students and says "
                "the original relationship between dependent decision style and procrastination was r = .277. "
                "Supplementary Table S1 lists original effect size r = .277."
            ),
            replication_source_text=(
                "Main PDF reports the Polish replication N = 202 and r = .165, p = .019 for the same "
                "dependent decision style/procrastination relationship. Supplementary Table S1 lists "
                "replication effect size r = .165, p = .019."
            ),
            conversion_note="Converted both Pearson correlations to D magnitudes with d = 2r/sqrt(1-r^2).",
        ),
        row(
            pair_id="jdm_polish_s05_subjective_numeracy_low_payoff",
            original_title=(
                "Numerate decision makers don't use more effortful strategies unless it pays: "
                "A process tracing investigation of skilled and adaptive strategy selection in risky decision making"
            ),
            original_doi="",
            outcome="Subjective numeracy and EV-maximizing choices in low-payoff problems",
            d_original=0.408,
            n_original=133,
            d_replication=0.173,
            n_replication=202,
            match_author="Sobkow_2022_S05_Traczyk_2018_low_payoff",
            original_source_text=(
                "Main PDF reports Traczyk et al. original N = 133 and low-payoff subjective-numeracy "
                "relationship r = .200, p = .021, d = 0.408; Supplementary Table S1 lists r = .200, p = .021."
            ),
            replication_source_text=(
                "Main PDF reports Polish replication N = 202 and low-payoff relationship r = .086, "
                "p = .221, d = 0.173; Supplementary Table S1 lists r = .086, p = .221."
            ),
            conversion_note="Used source-reported Cohen's d values from the main PDF.",
        ),
        row(
            pair_id="jdm_polish_s05_subjective_numeracy_high_payoff",
            original_title=(
                "Numerate decision makers don't use more effortful strategies unless it pays: "
                "A process tracing investigation of skilled and adaptive strategy selection in risky decision making"
            ),
            original_doi="",
            outcome="Subjective numeracy and EV-maximizing choices in high-payoff problems",
            d_original=0.683,
            n_original=133,
            d_replication=0.398,
            n_replication=202,
            match_author="Sobkow_2022_S05_Traczyk_2018_high_payoff",
            original_source_text=(
                "Main PDF reports Traczyk et al. original N = 133 and high-payoff subjective-numeracy "
                "relationship r = .323, p < .001, d = 0.683; Supplementary Table S1 lists r = .323, p < .001."
            ),
            replication_source_text=(
                "Main PDF reports Polish replication N = 202 and high-payoff relationship r = .195, "
                "p = .005, d = 0.398; Supplementary Table S1 lists r = .195, p = .005."
            ),
            conversion_note="Used source-reported Cohen's d values from the main PDF.",
        ),
        row(
            pair_id="jdm_polish_c13_information_focus_control_young_adults",
            original_title=(
                "Following your heart or your head: Focusing on emotions versus information "
                "differentially influences the decisions of younger and older adults"
            ),
            original_doi="10.1037/a0018500",
            outcome="Information focus versus control decision quality in younger adults",
            d_original=0.65,
            n_original=40,
            d_replication=0.21,
            n_replication=129,
            match_author="Sobkow_2022_C13_Mikels_2010_information_control",
            original_source_text=(
                "Supplementary Table S1 lists the focal younger-adult information-focus versus control "
                "effect as t(38) = 2.08, p < .05, d = 0.65. The df implies N = 40 for the two-condition contrast."
            ),
            replication_source_text=(
                "Supplementary Table S1 lists the Polish replication information-focus versus control "
                "effect as t(127) = 1.17, p = .244, d = 0.21. The df implies N = 129 for the two-condition contrast."
            ),
            conversion_note="Used source-reported Cohen's d values from Supplementary Table S1.",
        ),
        row(
            pair_id="jdm_polish_c25_anchoring_mean_point_biserial",
            original_title="Measures of Anchoring in Estimation Tasks",
            original_doi="10.1177/01461672952111004",
            outcome="Mean point-biserial estimate-anchor correlation across 15 anchoring tasks",
            d_original=r_to_d(0.42),
            n_original=103,
            d_replication=r_to_d(0.46),
            n_replication=202,
            match_author="Sobkow_2022_C25_Jacowitz_Kahneman_1995",
            original_source_text=(
                "Main PDF reports Jacowitz and Kahneman original N = 103 and says the mean point-biserial "
                "correlation between estimates and anchors over 15 problems was r = .42."
            ),
            replication_source_text=(
                "Main PDF reports the Polish replication N = 202 and says the mean point-biserial "
                "correlation between estimates and anchors over 15 problems was r = .46, p < .001."
            ),
            conversion_note="Converted both point-biserial correlations to D magnitudes with d = 2r/sqrt(1-r^2).",
        ),
    ]


def write_table(path: Path, rows: list[dict[str, Any]], columns: list[str], delimiter: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore", delimiter=delimiter)
        writer.writeheader()
        for item in rows:
            writer.writerow({column: clean(item.get(column, "")) for column in columns})


def main() -> None:
    missing = [path for path in [MAIN_PDF, SUPPLEMENT] if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing mirrored source object(s): " + ", ".join(str(path) for path in missing))
    rows = build_rows()
    write_table(OUT_CSV, rows, PROMOTED_COLUMNS, ",")
    write_table(AUDIT_TSV, rows, AUDIT_COLUMNS, "\t")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"Wrote {AUDIT_TSV.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
