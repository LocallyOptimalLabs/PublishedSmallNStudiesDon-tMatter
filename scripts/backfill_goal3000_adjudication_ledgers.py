#!/usr/bin/env python3
"""Backfill durable Figure 1 adjudication ledgers for the 3k-row goal."""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508"
REVIEWED_AT = "2026-05-08"
SHA256_CACHE: dict[Path, str] = {}

REVIEWCUE_RESOLUTION_OVERRIDES = {
    "review_figure1_search_leads_29d4d29c1ba2": {
        "status": "hold_nonhuman_llm_replication_not_current_figure1",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The article and OSF README describe replication of human scenario experiments using GPT-4, Claude, and "
            "DeepSeek responses. This has many human-vs-LLM effect rows, but the replication units are model outputs, "
            "not larger human replication samples under the current Figure 1 standard."
        ),
        "possible_reuse": "LLM-as-participant comparison project; nonhuman replication sensitivity analysis; source-methods appendix",
        "next_action": "Do not count toward goal3000. Revisit only if Figure 1 policy explicitly admits nonhuman LLM replications.",
    },
    "review_figure1_search_leads_6061ab8657b3": {
        "status": "hold_meta_analysis_vs_replication_aggregate_not_current_figure1",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Kvarven/Strømland/Johannesson source compares meta-analytic aggregate effects with multiple-lab replication "
            "project effects across 15 meta-replication pairs. This is not the current Figure 1 unit of one original study/result "
            "versus a larger replication result."
        ),
        "possible_reuse": "meta-analysis-vs-replication comparison figure; source-family crosswalk for known replication projects",
        "next_action": "Skip for goal3000 rows unless extracting only as a separately scoped aggregate/meta-analysis project.",
    },
    "review_figure1_search_leads_27d5775f87b9": {
        "status": "hold_reanalysis_compilation_not_pair_table",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The OSF qdx7p package contains available Diener et al. replication datasets and a cleaning/analysis script, "
            "but it does not expose a source-backed original-result D/N paired with a larger replication-result D/N. "
            "Using study sites as rows would create site-level fanout and newly constructed analyses."
        ),
        "possible_reuse": "well-being replication data package; possible raw-data recomputation project if separately scoped",
        "next_action": "Skip for goal3000 row discovery unless a source-backed original/replication result table is identified.",
    },
    "review_figure1_search_leads_ec299d9c57b4": {
        "status": "resolved_duplicate_existing_fred_row_provenance_hardening",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The OSF node and accepted manuscript support one source-backed primary row for Olson and Fazio (2001) "
            "Experiment 2 explicit pleasantness ratings versus Moran et al. (2021)'s preregistered primary Olson/Fazio-criterion "
            "analysis, but the same original/replication result is already represented in the live root table as FReD row "
            "fred_soscisubmission38_1_1_1066. Do not add a second plotted row; use the new mirrors for provenance hardening "
            "or conversion reconciliation only."
        ),
        "possible_reuse": "RRR provenance hardening; awareness-criterion sensitivity; surveillance-task prior-literature meta-analysis",
        "next_action": "Keep skipped for goal3000. Revisit only to attach source support to the existing FReD row or reconcile effect conversion.",
    },
    "review_figure1_search_leads_6720e58edd1a": {
        "status": "resolved_known_rrr_source_family",
        "figure1_decision": "skip_already_accounted_for_or_policy_blocked",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The ego-depletion RRR is already represented by existing RRR Hagger/manual and Hagger RTV rows. "
            "Additional lab/site-level rows would create one-to-many fanout; further work should harden aggregate provenance only."
        ),
        "possible_reuse": "RRR provenance hardening; aggregate-vs-site sensitivity",
        "next_action": "Skip for goal3000 row discovery unless replacing, not adding to, the existing ego-depletion representation.",
    },
    "review_figure1_search_leads_1a654f61e08b": {
        "status": "resolved_rpcb_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Reproducibility Project: Cancer Biology source family is already represented by 118 RPCB root rows; "
            "current filters include 33 D/N rows and exclude 85 by current gates."
        ),
        "possible_reuse": "RPCB provenance hardening and source-result support",
        "next_action": "Use only for RPCB source-result provenance; do not re-ingest for new rows.",
    },
    "review_figure1_search_leads_c003e8bf12be": {
        "status": "resolved_many_labs_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for_or_site_fanout",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "Many Labs data are already represented through the live Many Labs builders and FReD/Metascience overlaps. "
            "The remaining JOPD/OSF package is useful for provenance, but lab/site rows are not valid extra 1:1 rows."
        ),
        "possible_reuse": "Many Labs provenance hardening; lab-level heterogeneity appendix",
        "next_action": "Skip for goal3000 row discovery.",
    },
    "review_figure1_search_leads_24788ac9a7b9": {
        "status": "resolved_boyce_srp_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Boyce/student-replication source family is already represented by Boyce corpus, SRP, FReD, and Metascience rows. "
            "Current root search finds 156 related rows; further bulk ingest risks duplicate source assertions."
        ),
        "possible_reuse": "Boyce/SRP provenance hardening and duplicate reconciliation",
        "next_action": "Skip for new goal3000 rows unless a row-level dedupe audit identifies a missing canonical pair.",
    },
    "review_figure1_search_leads_c7808e6c3826": {
        "status": "resolved_decision_market_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Decision-Market Replication Project is already represented by the decision-market pair table and related online-experiment rows. "
            "Current root search finds 26 decision-market rows included by current D/N rules."
        ),
        "possible_reuse": "Decision-market provenance hardening; OSF file-level support",
        "next_action": "Skip for goal3000 row discovery.",
    },
    "review_figure1_search_leads_17f20eab2f6e": {
        "status": "resolved_eerp_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Experimental Economics Replication Project is already represented by 25 EERP root rows from "
            "ReplicationSuccess and manual supplement routes; 18 currently pass the D/N rule."
        ),
        "possible_reuse": "EERP provenance hardening",
        "next_action": "Skip for new goal3000 rows unless replacing a weaker duplicate with stronger source support.",
    },
    "review_figure1_search_leads_404c6c8bc341": {
        "status": "resolved_context_hub_not_row_source",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The FORRT large-scale replication projects hub is a discovery/index source, not a value-bearing original/replication pair table. "
            "FORRT/FReD-derived rows are already handled through FReD, Metascience, and FORRT-specific promotion audits."
        ),
        "possible_reuse": "project alias discovery; source-family index",
        "next_action": "Skip as a new-row source; use only to discover named projects not already in the queue.",
    },
    "review_figure1_search_leads_4c3314063449": {
        "status": "resolved_fred_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for_or_policy_blocked",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "FReD is already a major live source family. Current root search finds over 1,100 FReD/FORRT/Metascience-related rows, "
            "and the latest FReD archive rescue scan found no remaining high-precision bulk candidates."
        ),
        "possible_reuse": "FReD provenance hardening; row-level duplicate audit; metric policy work",
        "next_action": "Skip bulk re-ingest for goal3000; only promote manually verified nonduplicate rows.",
    },
    "review_figure1_search_leads_8deda84acf73": {
        "status": "resolved_rpp_source_family_already_integrated",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Reproducibility Project: Psychology source family is already represented by 96 RPP canonical OSF CSV rows "
            "plus related overlap routes. Rechecking the OSF project is provenance work, not new-row discovery."
        ),
        "possible_reuse": "RPP provenance hardening and source-result support",
        "next_action": "Skip for new goal3000 rows.",
    },
    "review_figure1_search_leads_38018a44fd54": {
        "status": "hold_computational_replication_journal_not_current_figure1",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "ReScience C is a computational replication journal/source index. It may contain original-paper links and code, "
            "but it is not itself a human/biomedical original-vs-larger-replication D/N table."
        ),
        "possible_reuse": "computational reproducibility project inventory",
        "next_action": "Do not pursue for current Figure 1 rows without a specific article-level human/experimental D/N mapping.",
    },
    "review_figure1_search_leads_95434678b310": {
        "status": "resolved_already_integrated_no_new_rows",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Sports Science Replication Centre result article is already represented in the root table through "
            "the direct sports supplemental outcomes table plus Metascience/FReD RSESR streams. The latest audit found "
            "RSESR candidates already promoted, duplicate-held, failed by current D/N gates, missing numeric fields, "
            "or not validated. Rechecking this review cue is zero-yield unless doing provenance hardening."
        ),
        "possible_reuse": "provenance hardening for existing sports/RSESR rows; source-family coverage audit",
        "next_action": "Do not pursue for new goal3000 rows; use only to harden source-result provenance or dedupe policy.",
    },
    "review_figure1_search_leads_75bf3c17e235": {
        "status": "hold_nonhuman_llm_replication_not_current_figure1",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Figshare/OSF data package is the code/data child for the Nature Computational Science LLM scenario "
            "replication article. The checked OSF README says the study compares original human studies with LLM "
            "responses and aggregates human/LLM effect sizes, not original human samples versus larger human replications."
        ),
        "possible_reuse": "LLM-as-participant comparison project; data-processing provenance for the Nature LLM article",
        "next_action": "Do not inspect the zip for current Figure 1 rows unless nonhuman LLM replications become in scope.",
    },
    "review_figure1_search_leads_07969abf10b1": {
        "status": "resolved_existing_result_package_provenance_only",
        "figure1_decision": "skip_not_new_pair_source",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The 0_master do-file is a local replication-package orchestration script for an already cataloged political-science "
            "source family, not a standalone original-vs-larger-replication effect table."
        ),
        "possible_reuse": "file-level provenance for the Direct Aid source family",
        "next_action": "Use only if hardening file-level provenance; do not count as a new Figure 1 row source.",
    },
    "review_figure1_search_leads_7d811dec6207": {
        "status": "resolved_existing_result_package_provenance_only",
        "figure1_decision": "skip_not_new_pair_source",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Zenodo replication package is a local artifact already routed to an existing political-science source family. "
            "It is useful file-level provenance, not a new row-yielding corpus."
        ),
        "possible_reuse": "file-level provenance for the Bangladesh authoritarian-election source family",
        "next_action": "Use only if hardening file-level provenance; do not count as a new Figure 1 row source.",
    },
    "review_figure1_search_leads_889e202a4dd5": {
        "status": "resolved_rrr_colling_att_snarc_already_integrated",
        "figure1_decision": "skip_already_accounted_for",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Zenodo/GitHub FischerRRR eyetracking code snapshot is an artifact for the Colling et al. Att-SNARC "
            "registered replication report. That source family is already integrated as four current D/N rows from the "
            "local RRR Colling 2020 Att-SNARC table reconstruction. Re-ingesting the code snapshot would duplicate "
            "already plotted ISI-level rows."
        ),
        "possible_reuse": "source-file provenance for RRR Colling 2020; raw-data recomputation audit",
        "next_action": "Skip for goal3000 row discovery; use only to harden the existing RRR Colling source family.",
    },
    "review_figure1_search_leads_115f5ee33aea": {
        "status": "promoted_current_figure1_row",
        "figure1_decision": "promoted_to_current_figure1",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "Resolved as a strict single-row promotion: Kosfeld et al. (2005) oxytocin/placebo investor trust-game "
            "effect versus Kroll et al. (2026)'s own n=211 direct replication. The pooled Kroll+Declerck n=532 "
            "estimate was checked and intentionally not used for the plotted row to avoid multi-replication aggregation "
            "when a single matched larger replication estimate is available."
        ),
        "possible_reuse": "OXT/trust replication source-result support; pooled-replication sensitivity using Kroll+Declerck n=532",
        "next_action": "Already counted in goal3000. Revisit only for source-result provenance hardening or a separately scoped pooled-analysis sensitivity.",
    },
    "review_figure1_search_leads_b7d63ec6dc91": {
        "status": "coverage_only_tandf_challenge_no_value_source",
        "figure1_decision": "coverage_only_manual_acquisition_needed",
        "skip_in_goal3000": "yes_until_manual_acquisition",
        "mismatch_or_blocker": (
            "The victim-impact curriculum article has only Crossref bibliographic metadata locally. DOI resolution redirects to "
            "Taylor & Francis and the mirrored landing attempt is a Cloudflare challenge/HTTP 403 page, not value-bearing text. "
            "No original-effect, replication-effect, or matched D/N values were available from accessible artifacts."
        ),
        "possible_reuse": "criminal-justice curriculum replication lead; manual/library acquisition task",
        "next_action": "Skip automated goal3000 work until a PDF/HTML/full text, supplement, or data artifact is manually acquired.",
    },
    "review_figure1_search_leads_f5860736bcb1": {
        "status": "source_route_404_project_unavailable",
        "figure1_decision": "coverage_only_source_unavailable",
        "skip_in_goal3000": "yes_until_source_reappears",
        "mismatch_or_blocker": (
            "The Caballero 2021 replication project was routed from OSF search metadata, but the checked OSF API route "
            "kdbsa now returns 404. The saved cue text describes a direct replication of Caballero et al. Study 2, but no "
            "retrievable value-bearing project file, original value text, replication N, or replication effect was acquired."
        ),
        "possible_reuse": "economic-scarcity/construal replication lead if OSF route reappears or user supplies files",
        "next_action": "Skip for goal3000 unless the OSF project or a mirrored copy becomes available.",
    },
    "review_figure1_search_leads_5a6989d0ac69": {
        "status": "planned_registration_route_404_no_results",
        "figure1_decision": "coverage_only_registration_unavailable",
        "skip_in_goal3000": "yes_until_source_reappears",
        "mismatch_or_blocker": (
            "The earth-science citation lead was a planned replication/scaling registration for White 2019, but the OSF API "
            "route u49zv now returns 404. No completed replication result, value-bearing data artifact, or original-vs-larger "
            "D/N mapping was acquired."
        ),
        "possible_reuse": "citation-practice replication lead if registration/results reappear",
        "next_action": "Skip for current Figure 1 until a public completed result source is found.",
    },
    "review_figure1_search_leads_6c2f7ee495da": {
        "status": "hold_computational_replication_code_not_current_figure1",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The ECLS-K OSF project is public and contains an R Markdown analysis and SAS extraction script for a ReScience X "
            "computational replication. It is code for re-running an observational ECLS-K analysis, not a source-backed "
            "original experimental result versus a larger replication result with D/N values."
        ),
        "possible_reuse": "computational reproducibility inventory; education-data reproducibility context",
        "next_action": "Skip for current Figure 1 rows unless a separate computational-reproducibility figure is scoped.",
    },
    "review_figure1_search_leads_6e23c48b1120": {
        "status": "hold_data_only_course_assignment_original_target_missing",
        "figure1_decision": "hold_context_source_not_plot_ready",
        "skip_in_goal3000": "yes",
        "mismatch_or_blocker": (
            "The Stroop OSF node is a public course-assignment dataset. The mirrored SAV has 416 rows corresponding to 104 "
            "participants across posture/congruency cells, but no source-backed original target paper, original effect/N, "
            "replication analysis result, or claim that this is a larger replication of a specific original study."
        ),
        "possible_reuse": "teaching dataset; Stroop raw-data exercise; parser coverage for SAV files",
        "next_action": "Skip for current Figure 1 unless an original target and value-bearing replication report are supplied.",
    },
}

COMMON_COLUMNS = [
    "reviewed_at",
    "workstream",
    "candidate_id",
    "status",
    "figure1_decision",
    "skip_in_goal3000",
    "reviewed_question",
    "source_evidence_paths",
    "source_checksums",
    "relation_evidence",
    "original_value_evidence",
    "replication_value_evidence",
    "mismatch_or_blocker",
    "possible_reuse",
    "next_action",
    "row_count",
    "source_artifact",
]

YING_COLUMNS = [
    "reviewed_at",
    "workstream",
    "candidate_id",
    "ying_pair",
    "status",
    "figure1_decision",
    "skip_in_goal3000",
    "reviewed_question",
    "source_evidence_paths",
    "source_checksums",
    "relation_evidence",
    "original_value_evidence",
    "replication_value_evidence",
    "mismatch_or_blocker",
    "possible_reuse",
    "next_action",
]

METASCIENCE_OUTSIDE_COLUMNS = COMMON_COLUMNS + [
    "source",
    "tag",
    "original_title",
    "replication_title",
    "description",
    "original_doi",
    "replication_doi",
    "original_n_num",
    "replication_n_num",
    "D_original",
    "D_replication",
    "current_root_same_doi_pair_rows",
    "current_root_same_original_doi_rows",
    "current_root_same_replication_doi_rows",
    "root_value_alias_match_count",
]


def clean(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value)
    text = text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except Exception:
        return str(path)


def slug(value: object, max_len: int = 60) -> str:
    text = clean(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return (text[:max_len].strip("_") or "untitled")


def file_sha256(path: Path) -> str:
    key = path.resolve()
    if key in SHA256_CACHE:
        return SHA256_CACHE[key]
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    digest = h.hexdigest()
    SHA256_CACHE[key] = digest
    return digest


def read_table(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    sep = "\t" if path.suffix == ".tsv" else ","
    return pd.read_csv(path, sep=sep)


def split_support_paths(value: object) -> list[Path]:
    paths: list[Path] = []
    for part in re.split(r"\s+\|\s+|;", clean(value)):
        part = part.strip()
        if not part:
            continue
        path = Path(part)
        if not path.is_absolute():
            path = ROOT / path
        paths.append(path)
    return paths


def path_evidence(paths: list[Path], max_checksums: int = 12) -> tuple[str, str]:
    existing = [path for path in paths if path.exists()]
    checksums = [f"{rel(path)}={file_sha256(path)}" for path in existing[:max_checksums]]
    return "; ".join(rel(path) for path in existing), "; ".join(checksums)


def promoted_individual_scan_ids() -> tuple[set[str], set[str]]:
    promoted_path = ROOT / "data/derived/replication_pairs/harvest/promoted/individual_replication_papers__promoted_pairs.csv"
    promoted = read_table(promoted_path)
    if promoted is None:
        return set(), set()
    candidate_ids = set(promoted.get("match_author", pd.Series(dtype=str)).astype(str))
    pair_blob = "\n".join(promoted.fillna("").astype(str).apply(lambda series: " ".join(series.tolist()), axis=1).tolist())
    value_scan_ids: set[str] = set()
    scan = read_table(ROOT / "steps/individual_replication_papers/figure1/individual-paper-value-scan-batch001.tsv")
    if scan is not None and "value_scan_id" in scan.columns:
        for value_scan_id in scan["value_scan_id"].astype(str):
            if value_scan_id and value_scan_id in pair_blob:
                value_scan_ids.add(value_scan_id)
    return candidate_ids, value_scan_ids


def individual_value_scan_reviewcue_summaries() -> dict[str, dict[str, str]]:
    scan_path = ROOT / "steps/individual_replication_papers/figure1/individual-paper-value-scan-batch001.tsv"
    scan = read_table(scan_path)
    if scan is None:
        return {}
    promoted_candidates, promoted_values = promoted_individual_scan_ids()
    summaries: dict[str, dict[str, str]] = {}
    for candidate_id, group in scan.groupby("candidate_id", dropna=False):
        candidate_id = clean(candidate_id)
        if not candidate_id.startswith("review_figure1_search_leads_"):
            continue
        decisions = [clean(x) for x in group["scan_decision"].tolist()]
        likely_rows = pd.to_numeric(group.get("likely_new_strict_rows_if_promoted", 0), errors="coerce").fillna(0).astype(int)
        ready = group["scan_decision"].astype(str).eq("ready_for_source_result_build")
        promoted = candidate_id in promoted_candidates or any(clean(x) in promoted_values for x in group["value_scan_id"])
        if promoted and ready.any():
            status = "promoted_current_figure1_rows"
            figure1_decision = "promoted_to_current_figure1"
            row_count = str(int(ready.sum()))
            mismatch = (
                "Resolved by individual-paper value scan and promoted to current Figure 1. "
                "Non-promoted options for the same candidate, if any, remain held in the value-scan artifact."
            )
            next_action = "Already counted in goal3000; do not re-add. Revisit only for provenance hardening or sensitivity policy."
        else:
            status = "held_or_rejected_by_individual_value_scan"
            figure1_decision = "held_or_rejected_by_individual_value_scan"
            row_count = str(int(likely_rows.sum()))
            mismatch = " | ".join(clean(x) for x in group["conversion_or_policy_note"].tolist() if clean(x))[:2500]
            next_action = " | ".join(clean(x) for x in group["next_action"].tolist() if clean(x))[:1800]
        support_paths = []
        for value in group.get("local_support_paths", pd.Series(dtype=str)).tolist():
            support_paths.extend(split_support_paths(value))
        source_paths, checksums = path_evidence(support_paths)
        summaries[candidate_id] = {
            "reviewed_at": REVIEWED_AT,
            "status": status,
            "figure1_decision": figure1_decision,
            "skip_in_goal3000": "yes",
            "source_evidence_paths": source_paths or rel(scan_path),
            "source_checksums": checksums,
            "original_value_evidence": " | ".join(clean(x) for x in group["original_support_text"].tolist() if clean(x))[:2500],
            "replication_value_evidence": " | ".join(clean(x) for x in group["replication_support_text"].tolist() if clean(x))[:2500],
            "mismatch_or_blocker": mismatch or "See individual-paper value scan row for the resolved hold/reject/promote decision.",
            "possible_reuse": "individual-paper value scan provenance; future metric/policy sensitivity where applicable",
            "next_action": next_action,
            "row_count": row_count,
            "source_artifact": rel(scan_path),
        }
    return summaries


def add_individual_value_scan_rows(rows: list[dict[str, object]]) -> None:
    scan_path = ROOT / "steps/individual_replication_papers/figure1/individual-paper-value-scan-batch001.tsv"
    scan = read_table(scan_path)
    if scan is None:
        return
    promoted_candidates, promoted_values = promoted_individual_scan_ids()
    for row in scan.to_dict("records"):
        value_scan_id = clean(row.get("value_scan_id"))
        candidate_id = clean(row.get("candidate_id"))
        decision = clean(row.get("scan_decision"))
        likely_rows = clean(row.get("likely_new_strict_rows_if_promoted")) or "0"
        is_promoted = decision == "ready_for_source_result_build" and (
            candidate_id in promoted_candidates or value_scan_id in promoted_values
        )
        if is_promoted:
            figure1_decision = "promoted_to_current_figure1"
            status = "promoted_current_figure1_row"
            skip = "yes"
            blocker = clean(row.get("conversion_or_policy_note"))
            next_action = "Already counted in the current individual-replication promoted CSV; do not re-add as a new row."
        else:
            figure1_decision = "held_or_rejected_by_individual_value_scan"
            status = decision
            skip = "yes"
            blocker = clean(row.get("conversion_or_policy_note"))
            next_action = clean(row.get("next_action"))
        support_paths, checksums = path_evidence(split_support_paths(row.get("local_support_paths")))
        rows.append(
            {
                "reviewed_at": REVIEWED_AT,
                "workstream": "individual_replication_paper_value_scan",
                "candidate_id": f"individual_value_scan_{value_scan_id}",
                "status": status,
                "figure1_decision": figure1_decision,
                "skip_in_goal3000": skip,
                "reviewed_question": clean(row.get("result_option_label")),
                "source_evidence_paths": support_paths or rel(scan_path),
                "source_checksums": checksums,
                "relation_evidence": f"candidate_id={candidate_id}; route={clean(row.get('candidate_route'))}",
                "original_value_evidence": clean(row.get("original_support_text")),
                "replication_value_evidence": clean(row.get("replication_support_text")),
                "mismatch_or_blocker": blocker,
                "possible_reuse": "individual paper provenance; future metric, endpoint, or duplicate-policy sensitivity",
                "next_action": next_action,
                "row_count": likely_rows,
                "source_artifact": rel(scan_path),
            }
        )


def add_source_rows(rows: list[dict[str, object]]) -> None:
    add_individual_value_scan_rows(rows)

    probe_path = ROOT / "steps/corpus_results/figure1/corpus_strategy_rate_probe/corpus-strategy-rate-probe-2026-05-08.tsv"
    probe = read_table(probe_path)
    if probe is not None:
        for row in probe.to_dict("records"):
            decision = clean(row.get("decision"))
            rows.append(
                {
                    "reviewed_at": REVIEWED_AT,
                    "workstream": "corpus_strategy_rate_probe",
                    "candidate_id": clean(row.get("probe_id")),
                    "status": decision,
                    "figure1_decision": "no_new_current_figure1_rows",
                    "skip_in_goal3000": "yes" if row.get("estimated_new_included_rows", 0) == 0 else "revisit",
                    "reviewed_question": f"Can this source/strategy yield valid new 1:1 Figure 1 D/N rows? {clean(row.get('candidate_or_source'))}",
                    "source_evidence_paths": clean(row.get("local_artifact_or_table")),
                    "source_checksums": "",
                    "relation_evidence": clean(row.get("observed_signal")),
                    "original_value_evidence": "",
                    "replication_value_evidence": "",
                    "mismatch_or_blocker": clean(row.get("reason")),
                    "possible_reuse": "audit/context source or future policy-specific source review",
                    "next_action": clean(row.get("next_action")),
                    "row_count": "",
                    "source_artifact": rel(probe_path),
                }
            )

    staged_specs = [
        (
            "li_2024_pd1_pdl1_phase2_phase3_orr",
            ROOT / "data/derived/replication_pairs/harvest/staged/li_2024_pd1_pdl1_phase2_phase3_orr__stage.csv",
            "native_one_arm_orr_not_randomized_treatment_contrast",
            "Staged Li 2024 phase II/III oncology rows contain matched phase-study ORR responder counts, but ORR is a one-arm activity metric rather than a randomized treatment contrast on the current Figure 1 D axis.",
        ),
        (
            "wils_2023_ibd_phase2_phase3_response_rates",
            ROOT / "data/derived/replication_pairs/harvest/staged/wils_2023_ibd_phase2_phase3_response_rates__stage.csv",
            "native_treatment_arm_response_rate_not_treatment_contrast",
            "Staged Wils 2023 IBD rows contain phase 2/3 treatment-arm response rates, not active-vs-control effects.",
        ),
    ]
    for source_id, path, status, reason in staged_specs:
        df = read_table(path)
        if df is None:
            continue
        raw_files = sorted(clean(x) for x in df.get("raw_file", pd.Series(dtype=str)).dropna().unique())
        checksums = []
        for raw in raw_files[:5]:
            p = Path(raw)
            if p.exists():
                checksums.append(f"{rel(p)}={file_sha256(p)}")
        rows.append(
            {
                "reviewed_at": REVIEWED_AT,
                "workstream": "staged_native_metric_tables",
                "candidate_id": source_id,
                "status": status,
                "figure1_decision": "hold_native_only_not_current_d_equivalent",
                "skip_in_goal3000": "yes_until_metric_policy_changes",
                "reviewed_question": "Can this staged clinical phase table be bulk promoted as current Figure 1 D/N rows?",
                "source_evidence_paths": "; ".join([rel(path), *raw_files]),
                "source_checksums": "; ".join(checksums),
                "relation_evidence": f"{len(df)} staged early-phase/later-phase candidate rows from parser output.",
                "original_value_evidence": "Native original-side response fields present in staged rows.",
                "replication_value_evidence": "Native replication-side response fields present in staged rows.",
                "mismatch_or_blocker": reason,
                "possible_reuse": "native-metric clinical pilot-to-phase-III sensitivity analysis; metric-policy worklist",
                "next_action": "Do not promote into current Figure 1 without a defensible randomized-effect conversion policy.",
                "row_count": len(df),
                "source_artifact": rel(path),
            }
        )

    k_path = ROOT / "data/derived/replication_pairs/harvest/staged/kerschbaumer_2020_rheumatology_phase2_phase3__stage.csv"
    k_df = read_table(k_path)
    if k_df is not None:
        for endpoint in ["ACR50", "ACR70"]:
            subset = k_df[k_df["endpoint"].eq(endpoint)]
            if subset.empty:
                continue
            raw_files = sorted(clean(x) for x in subset.get("raw_file", pd.Series(dtype=str)).dropna().unique())
            rows.append(
                {
                    "reviewed_at": REVIEWED_AT,
                    "workstream": "staged_endpoint_fanout_tables",
                    "candidate_id": f"kerschbaumer_2020_{endpoint.lower()}_held_endpoint_fanout",
                    "status": "hold_endpoint_fanout",
                    "figure1_decision": "hold_not_promoted_current_figure1",
                    "skip_in_goal3000": "yes_until_endpoint_policy_changes",
                    "reviewed_question": f"Can Kerschbaumer {endpoint} rows be added after ACR20 promotion?",
                    "source_evidence_paths": "; ".join([rel(k_path), *raw_files]),
                    "source_checksums": "",
                    "relation_evidence": f"{len(subset)} staged {endpoint} rows share phase2/phase3 trial mappings with other ACR endpoints.",
                    "original_value_evidence": f"{endpoint} original response counts and Ns are present in staged rows.",
                    "replication_value_evidence": f"{endpoint} replication response counts and Ns are present in staged rows.",
                    "mismatch_or_blocker": "Additional ACR endpoints would create multiple endpoint rows for the same phase2/phase3 study pair beyond the already selected conservative endpoint.",
                    "possible_reuse": "endpoint-sensitivity appendix or clinical multi-endpoint robustness analysis",
                    "next_action": "Do not promote extra endpoints into current Figure 1 without an explicit endpoint multiplicity policy.",
                    "row_count": len(subset),
                    "source_artifact": rel(k_path),
                }
            )

    audit_specs = [
        (ROOT / "steps/corpus_results/figure1/metascience_observatory_validated_extension_20260508/metascience-validated-extension-promotion-audit.tsv", "metascience_validated_extension", "promotion_status"),
        (ROOT / "steps/corpus_results/figure1/metascience_observatory_misc_validated_20260508/metascience-misc-validated-promotion-audit.tsv", "metascience_misc_validated", "promotion_status"),
        (ROOT / "steps/corpus_results/figure1/metascience_observatory_soto_lopprp_20260508/metascience-soto-lopprp-promotion-audit.tsv", "metascience_soto_lopprp", "promotion_status"),
        (ROOT / "steps/corpus_results/figure1/metascience_observatory_srp_20260508/metascience-srp-promotion-audit.tsv", "metascience_srp", "promotion_status"),
        (ROOT / "steps/corpus_results/figure1/fred_archive_rescue_20260507/fred-archive-rescue-promoted-audit.tsv", "fred_archive_rescue", "archive_rescue_status"),
        (ROOT / "steps/corpus_results/figure1/ml1_site_level_effects/ml1-site-level-effects-audit.tsv", "ml1_site_level_effects", "audit_decision"),
        (ROOT / "steps/corpus_results/figure1/ml3_site_level_effects/ml3-site-level-effects-audit.tsv", "ml3_site_level_effects", "audit_decision"),
        (ROOT / "steps/corpus_results/figure1/ml5_site_level_single_effects/ml5-site-level-single-effects-audit.tsv", "ml5_site_level_single_effects", "audit_decision"),
    ]
    for path, workstream, status_col in audit_specs:
        df = read_table(path)
        if df is None or status_col not in df.columns:
            continue
        for status, count in df[status_col].fillna("missing_status").value_counts().sort_index().items():
            if str(status).startswith("promoted") and "site_level" not in workstream:
                continue
            blocker = status
            if "site_level" in workstream:
                blocker = f"{status}; site/lab-level rows are audit artifacts and are not valid 1:1 Figure 1 root rows unless aggregated."
            rows.append(
                {
                    "reviewed_at": REVIEWED_AT,
                    "workstream": workstream,
                    "candidate_id": f"{workstream}_{status}",
                    "status": clean(status),
                    "figure1_decision": "held_or_rejected_by_audit",
                    "skip_in_goal3000": "yes",
                    "reviewed_question": "What happened to rows in this promotion/audit artifact that did not become safe current Figure 1 rows?",
                    "source_evidence_paths": rel(path),
                    "source_checksums": "",
                    "relation_evidence": f"{count} audit rows with this status.",
                    "original_value_evidence": "See source audit rows for row-level original fields where present.",
                    "replication_value_evidence": "See source audit rows for row-level replication fields where present.",
                    "mismatch_or_blocker": clean(blocker),
                    "possible_reuse": "audit trail; duplicate diagnostics; fanout/multiplicity or policy-change sensitivity",
                    "next_action": "Skip for goal3000 unless a row-level audit explicitly changes the decision.",
                    "row_count": int(count),
                    "source_artifact": rel(path),
                }
            )

    manual_source_specs = [
        {
            "candidate_id": "metascience_misc_ssrp_source_alias_duplicate_batch_20260508",
            "workstream": "structured_source_duplicate_diagnostics",
            "status": "resolved_duplicate_existing_root_source_aliases",
            "figure1_decision": "skip_already_accounted_for",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Are the apparently DOI-new Metascience miscellaneous SSRP/SPRRR/direct rows actually new Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json",
                ROOT / "data/raw/replication_projects/replicationsuccess/SSRP.rda",
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-dedup-candidate-surface-20260508.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-dedup-strong-singleton-candidates-20260508.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-sourcealias-duplicate-diagnostics-20260508.tsv",
                ROOT / "steps/corpus_results/figure1/metascience_observatory_misc_validated_20260508/metascience-misc-validated-promotion-audit.tsv",
            ],
            "relation_evidence": (
                "The live DOI-pair screen found 21 Metascience misc rows that looked new because the existing root aliases "
                "had missing DOI fields or used a different publication-version DOI. A source-alias/value-tuple diagnostic "
                "matched all 21 to existing root rows."
            ),
            "original_value_evidence": (
                "The diagnostic matched candidate original N/D values against existing root rows, including 14 Social Sciences "
                "Replication Project rows already represented from ReplicationSuccess SSRP.rda."
            ),
            "replication_value_evidence": (
                "The same exact D/N value-tuple matches cover the replication-side effects and Ns; the Metascience API rows "
                "do not add new plotted evidence under current duplicate policy."
            ),
            "mismatch_or_blocker": (
                "DOI-only duplicate checks were insufficient because existing root rows can be source-family aliases without DOI "
                "metadata. The attempted SSRP allowlist was rolled back before finalization."
            ),
            "possible_reuse": "DOI enrichment for existing SSRP/FReD rows; source-alias reconciliation; duplicate-check regression tests",
            "next_action": "Skip these candidates for goal3000. Use the diagnostic to harden duplicate detection before future structured-source promotions.",
            "row_count": "21 duplicate aliases resolved; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "metascience_misc_singleton_current_root_duplicate_probe_20260509",
            "workstream": "structured_source_duplicate_diagnostics",
            "status": "resolved_stale_nonduplicate_surface_existing_root_rows",
            "figure1_decision": "skip_already_accounted_for",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Are the older Metascience misc singleton/nonduplicate candidates still new against the live Figure 1 root table?",
            "source_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-unreviewed-current-nonduplicates.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-dedup-strong-singleton-candidates-20260508.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-sourcealias-duplicate-diagnostics-20260508.tsv",
            ],
            "relation_evidence": (
                "The stale misc nonduplicate surface included singleton-looking DOI-pair rows, but live-root inspection showed "
                "the sampled rows were already represented through current FReD/Metascience source families or source-alias rows."
            ),
            "original_value_evidence": (
                "The checked singleton rows preserved original DOI/title/N/r or D fields in the Metascience/FReD API surface, "
                "but those values matched existing root rows or publication-version aliases."
            ),
            "replication_value_evidence": (
                "The checked replication-side DOI/title/N/r or D fields likewise matched existing FReD/Metascience rows, "
                "including rows already promoted in the current singleton-direct stream."
            ),
            "mismatch_or_blocker": (
                "The file name `metascience-misc-unreviewed-current-nonduplicates.tsv` is stale after later promotions and "
                "live dedupe work. Treat it as a historical candidate surface, not evidence that rows remain additive."
            ),
            "possible_reuse": "dedupe regression input; DOI/source-alias enrichment for existing FReD and Metascience rows",
            "next_action": "Do not reopen this surface for goal3000 without regenerating it against the current root table and source-alias checks.",
            "row_count": "+0 current Figure 1 rows; stale candidate surface closed as duplicate/covered",
        },
        {
            "candidate_id": "metascience_outside_allowed_family_overlap_batch_20260508",
            "workstream": "structured_source_duplicate_diagnostics",
            "status": "resolved_outside_allowed_source_family_overlaps",
            "figure1_decision": "skip_already_accounted_for_or_needs_reconciliation",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can strict numeric Metascience/FReD rows outside the current source-family allowlist safely add new Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json",
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-outside-allowed-family-strict-numeric-candidates-20260508.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-outside-allowed-family-adjudication-20260508.tsv",
            ],
            "relation_evidence": (
                "The outside-family scan found 160 strict numeric Metascience/FReD candidates from RP:P, SRP, SMR, SSRP, ML5, ML2, "
                "XPHIR, and EROE tags. Row-level adjudication classified them as exact DOI duplicates, value/source aliases, "
                "or source-family overlaps needing reconciliation rather than additive promotion."
            ),
            "original_value_evidence": (
                "The row-level adjudication ledger preserves original title, DOI/URL, N, r, and computed D fields from the "
                "Metascience/FReD candidate surface."
            ),
            "replication_value_evidence": (
                "The row-level adjudication ledger preserves replication title, DOI/URL, N, r, and computed D fields from the "
                "Metascience/FReD candidate surface."
            ),
            "mismatch_or_blocker": (
                "The 21 candidates that survived DOI-pair and exact value-alias filters were manually resolved as existing "
                "RPP/EPRP/Many Labs 2/Many Labs 5 source-family aliases or fanout risks. Bulk promotion would duplicate live rows "
                "or add one-to-many outcome/site-family rows."
            ),
            "possible_reuse": "source-family duplicate reconciliation; DOI enrichment; conversion discrepancy audit; future row-grain policy review",
            "next_action": "Skip this outside-family surface for goal3000 new-row discovery. Revisit only to replace or reconcile existing rows, not to add duplicates.",
            "row_count": "160 row-level adjudications; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "hagen_hcsp_main_sheet_deleted_20260509",
            "workstream": "structured_source_access_blocked",
            "status": "blocked_value_table_deleted",
            "figure1_decision": "hold_source_table_unavailable",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Hagen Cumulative Science Project I Shiny/GitHub bundle be recovered as a high-yield structured Figure 1 table?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/github_master.zip",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/148059e84112__edit.html",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/main_sheet_export_csv.headers.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/main_sheet_export_csv.html",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/main_sheet_htmlview.headers.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/main_sheet_htmlview.html",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/main_sheet_pub_csv.headers.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/main_sheet_pub_csv.html",
            ],
            "relation_evidence": (
                "The GitHub README and Shiny app identify the project as Hagen Cumulative Science Project I, estimating the "
                "reproducibility of JDM research. The app expected a main Google Sheet with study-level original and replication "
                "effect-size fields, plus a separate codebook sheet."
            ),
            "original_value_evidence": (
                "The accessible codebook sheet defines columns such as N.Original, p.value.Original, Effect.size.Original, "
                "CI_low.Original, and CI_high.Original. The actual value-bearing main sheet is not present in the GitHub zip."
            ),
            "replication_value_evidence": (
                "The app/codebook defines Effect.size.Replication, CI_low.Replication, and CI_high.Replication, but the main "
                "Google Sheet containing row values returned HTTP 410 on export, htmlview, and pub CSV routes."
            ),
            "mismatch_or_blocker": (
                "The mirrored Shiny app is only a template around an external Google Sheet. The codebook remains accessible, but "
                "the value-bearing main sheet says the requested file has been deleted, so no source-backed row values can be promoted."
            ),
            "possible_reuse": "manual acquisition request; Wayback/owner follow-up; source-family metadata for JDM replication inventory",
            "next_action": "Skip for goal3000 until the deleted main sheet or an equivalent archived dataset is obtained.",
            "row_count": "+0 current Figure 1 rows; main value table unavailable",
        },
        {
            "candidate_id": "many_smiles_collaboration_2022_context_hold_20260509",
            "workstream": "structured_source_context_hold",
            "status": "hold_broad_multicondition_replication_existing_strack_row",
            "figure1_decision": "hold_context_source_not_additive_current_figure1",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Many Smiles Collaboration article and data package yield additive current Figure 1 rows?",
            "source_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/many_smiles/8f4464df0b3d__s41562-022-01458-9.html",
                ROOT / "data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/many_smiles/data.zip",
            ],
            "relation_evidence": (
                "The mirrored Nature Human Behaviour article and data package describe a multi-country Many Smiles "
                "Collaboration test of facial-feedback manipulations, including pen-in-mouth, facial mimicry, and voluntary "
                "facial action conditions. The local data zip has source CSVs for country counts, trial-level ratings, and "
                "participant-level happy-minus-neutral differences."
            ),
            "original_value_evidence": (
                "The candidate is related to the Strack pen-in-mouth facial-feedback literature, but the currently live root "
                "table already has a Strack original row paired to the Wagenmakers RRR aggregate. The Many Smiles package did "
                "not provide a new source-backed original benchmark effect/N distinct from that represented target."
            ),
            "replication_value_evidence": (
                "The local data zip contains Fig1/Fig2/Fig3 source CSVs, including 3,878 participant-level rows in Fig3_Source.csv "
                "and multi-condition happiness differences. Promoting would require selecting one condition/aggregation from a "
                "broader multi-condition project and would risk duplicating the existing Strack target."
            ),
            "mismatch_or_blocker": (
                "Current Figure 1 requires a single matched original result versus a single larger replication result. This "
                "source is better treated as a broad facial-feedback replication context or sensitivity source unless policy "
                "explicitly selects a Many Smiles aggregation and replaces, rather than duplicates, the existing Strack/RRR row."
            ),
            "possible_reuse": "facial-feedback replication context; Strack provenance hardening; multi-condition or later-replication sensitivity analysis",
            "next_action": "Skip for goal3000 new-row discovery. Revisit only for a replacement/sensitivity row with an explicit duplicate policy.",
            "row_count": "+0 current Figure 1 rows; context/data source held",
        },
        {
            "candidate_id": "nakagawa_yang_ecoevo_insilico_se_only_hold_20260509",
            "workstream": "raw_corpus_viability_hold",
            "status": "hold_insilico_meta_analysis_no_pair_n",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Nakagawa/Yang ecology/evolution in-silico replication repositories yield current Figure 1 D/N rows?",
            "source_paths": [
                ROOT / "data/raw/corpus_candidates/nakagawa_yang/replication_EcoEvo_git/README.md",
                ROOT / "data/raw/corpus_candidates/nakagawa_yang/EcoEvo_PB/README.md",
                ROOT / "data/raw/corpus_candidates/nakagawa_yang/replication_EcoEvo_git/data/sensitivity/dat_processed_SMD.csv",
                ROOT / "data/raw/corpus_candidates/nakagawa_yang/replication_EcoEvo_git/data/sensitivity/dat_processed_Zr.csv",
                ROOT / "data/raw/corpus_candidates/nakagawa_yang/replication_EcoEvo_git/data/sensitivity/dat_processed_lnRR.csv",
                ROOT / "data/raw/corpus_candidates/nakagawa_yang/replication_EcoEvo_git/data/sensitivity/dat_processed_rob.csv",
                ROOT / "reports/corpus_suggestion_tracker.md",
                ROOT / "reports/acquisition/corpus_acquisition_log.md",
                ROOT / "reports/figure1_many_replication_corpora_gpt_help_request_2026-05-04.md",
                ROOT / "steps/corpus_results/figure1/figure1-raw-viability-summary.tsv",
            ],
            "relation_evidence": (
                "The mirrored repository README describes a large-scale in-silico replication project in ecology and evolution, "
                "and the companion EcoEvo publication-bias repository describes 88 independent meta-analytic cases. Prior "
                "corpus notes flagged it as promising but unresolved for D-vs-N extraction."
            ),
            "original_value_evidence": (
                "Checked processed files expose study/meta-analysis identifiers plus effect-size columns such as eff.size, "
                "var.eff.size, se.eff.size, z, and grouped_es. The robust processed file exposes es, var, study, se, z, count, "
                "and w. No source-backed original-study N field or original-vs-replication N pair was found in these checked tables."
            ),
            "replication_value_evidence": (
                "The repository supports model-based in-silico replicability estimates and confidence intervals, not a row-level "
                "larger-replication result with a distinct replication N and matched D value for each original result."
            ),
            "mismatch_or_blocker": (
                "Current Figure 1 needs one original result paired with one larger replication/follow-up result and both Ns. "
                "This source is a meta-analytic/in-silico replicability corpus with SE/variance/z fields, not an explicit "
                "original-vs-larger-replication D/N pair table."
            ),
            "possible_reuse": "SE-based replicability/meta-analysis comparator; ecology/evolution publication-bias context; future raw-dataset audit for constituent sample sizes",
            "next_action": "Skip for goal3000 unless a row-level table with explicit original N and larger-replication N is found or a separate SE-based figure is scoped.",
            "row_count": "+0 current Figure 1 rows; context/source-family held",
        },
        {
            "candidate_id": "i4r_public_workbook_context_only_computational_reproduction_20260509",
            "workstream": "structured_source_context_hold",
            "status": "hold_computational_reproduction_not_new_sample_dn_pair",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the public Institute for Replication workbook be bulk promoted as current Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/i4r/meta_database.xlsx",
                ROOT / "data/raw/replication_projects/i4r/meta_database.csv",
                ROOT / "steps/source_inventory/figure1/gpt_many_replication_candidates_20260504/candidate-intake-ledger.tsv",
                ROOT / "steps/source_inventory/figure1/result_artifact_acquisition/source-artifact-parser-candidate-queue.tsv",
                ROOT / "steps/corpus_results/figure1/codex_local_high_inspect/corpus-results-summary.tsv",
            ],
            "relation_evidence": (
                "The I4R workbook sheets are Computational Reproducibility, Coding Errors, and Robustness Checks. The robustness "
                "sheet contains original and replicated coefficients/standard errors/p-values for same-paper robustness checks, "
                "while the other sheets classify computational reproduction and coding errors."
            ),
            "original_value_evidence": (
                "The workbook includes original coefficients, standard errors, and p-values in the robustness-check sheet, but "
                "not original experimental D/N values for an early study result paired to a later larger-sample replication."
            ),
            "replication_value_evidence": (
                "The workbook includes re-run/robustness-check coefficients, standard errors, and p-values, but these are same-data "
                "or computational/robustness reproductions rather than new-sample larger replication effects with replication N."
            ),
            "mismatch_or_blocker": (
                "I4R is valuable for computational reproducibility and robustness auditing, but it is not a current Figure 1 "
                "source of original-vs-larger-replication D/N pairs. Promoting it would mix same-data reproduction or robustness "
                "checks with new-sample replication rows."
            ),
            "possible_reuse": "computational reproducibility figure; robustness-change sensitivity; source-family inventory for economics/political-science replication packages",
            "next_action": "Skip for goal3000 row discovery. Revisit only if a separate computational-reproduction figure or a new-sample I4R subset is explicitly scoped.",
            "row_count": "+0 current Figure 1 rows; public workbook held as context",
        },
        {
            "candidate_id": "batch008_finger_flexion_haeffel_2025_outcome_mismatch",
            "workstream": "individual_search_batch008_adjudication",
            "status": "not_row_original_target_outcome_mismatch",
            "figure1_decision": "reject_current_figure1_mismatched_outcome",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can Haeffel et al. 2025 repeated finger-flexion direct replication yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "steps/searches/figure1/individualrepsearch-screening-hits-batch008.tsv",
                ROOT / "data/raw/replication_projects/individual_search_batch008/finger_flexion_haeffel_2025/pmc12501816.html",
            ],
            "relation_evidence": (
                "The PMC article says Study 1 was a direct replication using the same task, equipment, and undergraduate population "
                "as Haeffel (2011), with n=216. It also says Study 2 was a conceptual online replication with n=246."
            ),
            "original_value_evidence": (
                "The article summarizes the original Haeffel (2011) finding as a significant gender-by-condition interaction on "
                "BAS-Fun and persistence, with no main condition effects for positive or negative affect; it gives original sample "
                "size n=186 but not a matched original positive-affect D/N result."
            ),
            "replication_value_evidence": (
                "Study 1 reports direct-replication positive-affect main effect F(1,209)=7.89, p=.01, eta_p^2=.02, Cohen's d=-0.40, "
                "n=216, while approach-reward and persistence effects were nonsignificant. Study 2 reports a different conceptual "
                "replication effect on approach-reward motivation."
            ),
            "mismatch_or_blocker": (
                "The significant direct-replication effect is positive affect, whereas the original reported focal effect was a "
                "gender-by-condition interaction on BAS-Fun/persistence. Promoting would mix outcome and model terms."
            ),
            "possible_reuse": "motor-movement/embodiment replication context; multiple-comparison/cherry-picking case study; source-result support if original Haeffel values are later acquired",
            "next_action": "Skip for goal3000 unless the original Haeffel paper/source exposes an exact same-outcome positive-affect D/N or policy admits outcome-switch sensitivity rows.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "batch008_hiv_influential_studies_prior_reject_confirmed",
            "workstream": "individual_search_batch008_adjudication",
            "status": "prior_value_scan_reject_review_or_source_family_not_single_pair",
            "figure1_decision": "reject_current_figure1_not_single_pair",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the PLOS replication of influential HIV prevention/treatment studies yield a strict individual Figure 1 row?",
            "source_paths": [
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-value-scan-batch001.tsv",
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-dedupe-baseline-batch005.tsv",
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-result-option-disposition-batch003.tsv",
                ROOT / "data/raw/replication_projects/individual_search_batch002/api_candidate_099c6eb209be07e5/01_journals_plos_org_plosone_article_id_10_1371_journal_pone_0240159_474a5ae8debf.html",
            ],
            "relation_evidence": (
                "Candidate api_candidate_099c6eb209be07e5 is DOI 10.1371/journal.pone.0240159, titled as a replication of "
                "influential biomedical, social, behavioural, and structural HIV prevention/treatment studies."
            ),
            "original_value_evidence": (
                "The prior value scan recorded this as a review/context-source lead rather than one resolved original paper "
                "with one matched original D/N endpoint."
            ),
            "replication_value_evidence": (
                "The mirrored PLOS article is value-bearing for a multi-study replication assessment, but the checked artifacts "
                "did not resolve one single original-vs-larger replication effect/N pair for current Figure 1."
            ),
            "mismatch_or_blocker": (
                "This is a source-family/review-style HIV replication assessment, not a single original result paired with one "
                "larger replication result under the individual-paper route. It was already rejected in the value scan as "
                "`not_row_reject_review_or_source_family_not_single_pair`."
            ),
            "possible_reuse": "HIV intervention replication corpus lead; source-family mining if a separate structured HIV table is scoped",
            "next_action": "Do not redo as an individual-paper candidate. Revisit only through a corpus/source-family parser that exposes explicit 1:1 mappings and D/N values.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "batch008_phone_presence_przybylski_weinstein_2021_native_multilevel_hold",
            "workstream": "individual_search_batch008_adjudication",
            "status": "not_row_native_multilevel_group_count_no_current_d_route",
            "figure1_decision": "hold_native_metric_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can Linares and Sellier 2021 phone-presence replication yield strict current Figure 1 rows?",
            "source_paths": [
                ROOT / "steps/searches/figure1/individualrepsearch-screening-hits-batch008.tsv",
                ROOT / "data/raw/replication_projects/individual_search_batch008/phone_presence_replication_2021/plos_pone_0251451.html",
                ROOT / "data/raw/replication_projects/individual_search_batch008/phone_presence_replication_2021/pone.0251451.s007.docx",
                ROOT / "data/raw/replication_projects/individual_search_batch008/phone_presence_replication_2021/pone.0251451.s010.docx",
            ],
            "relation_evidence": (
                "The PLOS article identifies itself as a close replication of Przybylski and Weinstein (2013); it reports two "
                "experiments with N=356 participants and 136 groups, following the original phone-versus-notebook conversation procedure."
            ),
            "original_value_evidence": (
                "S1/S4 table workbooks compare original Study 1 and Study 2 relationship-quality/trust/empathy fixed effects from "
                "Przybylski and Weinstein with the replications, using group counts and multilevel fixed-effect b/t/p fields."
            ),
            "replication_value_evidence": (
                "S1 table reports Study 1 dyad and triad relationship measures with phone/notebook means, group counts, ICCs, "
                "and multilevel fixed effects; S4 reports Study 2 triads in the same native multilevel format."
            ),
            "mismatch_or_blocker": (
                "The value-bearing source is a multilevel/group-level analysis table with Ngroups and unstandardized fixed effects, "
                "not a directly reported or currently accepted D/N conversion. Converting b/t/group-count fields ad hoc would alter standards."
            ),
            "possible_reuse": "native-metric appendix; future multilevel-to-D conversion policy; phone-presence replication source-result provenance",
            "next_action": "Skip for goal3000 until a defensible and approved multilevel/group-count-to-D conversion is implemented.",
            "row_count": "+0 current Figure 1 rows; two replication studies held",
        },
        {
            "candidate_id": "batch008_watching_eyes_rotella_2021_broad_effect_hold",
            "workstream": "individual_search_batch008_adjudication",
            "status": "not_row_broad_effect_family_no_single_original_target",
            "figure1_decision": "reject_current_figure1_no_single_original_pair",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can Rotella et al. 2021 watching-eyes replication yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "steps/searches/figure1/individualrepsearch-screening-hits-batch008.tsv",
                ROOT / "data/raw/replication_projects/individual_search_batch008/watching_eyes_replication_2021/plos_pone_0255531.html",
            ],
            "relation_evidence": (
                "The PLOS article says it sought to replicate the watching-eyes effect and an observation/prosociality interaction, "
                "and cites many possible prior watching-eyes studies rather than one exclusive original target."
            ),
            "original_value_evidence": (
                "The checked article does not identify a single source-backed original D/N value to pair with the replication; it frames "
                "the target as a broader watching-eyes/observation literature."
            ),
            "replication_value_evidence": (
                "The article reports a preregistered dictator-game study with n=189 and says neither public decisions nor eye images "
                "increased giving, but the result is not paired to one original source-result."
            ),
            "mismatch_or_blocker": (
                "Current Figure 1 requires one original result versus one larger replication result. This candidate is a broad effect-family "
                "replication/extension with no single original target and would require a new selector policy."
            ),
            "possible_reuse": "watching-eyes literature map; broad-effect replication context; future selector-policy case study",
            "next_action": "Skip for goal3000 unless a later source explicitly maps the replication contrast to one original source-result with D/N values.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_95434678_rsesr_already_integrated",
            "workstream": "reviewcue_resolved_source_family",
            "status": "resolved_already_integrated_no_new_rows",
            "figure1_decision": "skip_already_accounted_for",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Does the RSESR/Sports Science Replication Centre review cue still offer new current Figure 1 rows?",
            "source_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "data/raw/replication_projects/sports/sports_supp_table1.docx",
                ROOT / "data/raw/replication_projects/sports/sports_sample_size_calculations.xlsx",
                ROOT / "data/raw/replication_projects/sports/sports_allselectedstudies.xlsx",
                ROOT / "data/derived/replication_pairs/harvest/promoted/metascience_observatory_validated_extension__promoted_pairs.csv",
                ROOT / "data/derived/replication_pairs/harvest/promoted/metascience_observatory_misc_validated__promoted_pairs.csv",
                ROOT / "steps/corpus_results/figure1/metascience_observatory_validated_extension_20260508/metascience-validated-extension-promotion-audit.tsv",
                ROOT / "steps/corpus_results/figure1/metascience_observatory_misc_validated_20260508/metascience-misc-validated-promotion-audit.tsv",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/keep_in_corpora_and_databases/title_estimating_the_replicability_of_sports_and_exercise_science_research.json",
            ],
            "relation_evidence": (
                "Review cue 95434678b310 identified DOI 10.1007/s40279-025-02201-w as the Sports Science Replication "
                "Centre result article with 25 replication studies. Current root search finds 34 RSESR/sports rows: "
                "19 direct sports supplemental-outcomes rows, 9 Metascience Observatory RSESR extension rows, and 6 "
                "Metascience Observatory RSESR rows; 31 pass the current D/N gate and 3 fail current D/N gates."
            ),
            "original_value_evidence": "Existing rows preserve original D/N values from sports supplemental tables or Metascience/FReD API RSESR fields.",
            "replication_value_evidence": "Existing rows preserve replication D/N values from sports supplemental tables or Metascience/FReD API RSESR fields.",
            "mismatch_or_blocker": (
                "No new source-family rows remain from this cue after accounting for already-promoted rows, duplicate-held "
                "rows, current D/N failures, missing numeric rows, and not-validated rows in the promotion audits."
            ),
            "possible_reuse": "provenance hardening for sports/RSESR rows; duplicate-source reconciliation; field-specific appendix",
            "next_action": "Skip for new goal3000 row discovery. Revisit only for source-result provenance or deduplication policy work.",
            "row_count": "34 root rows; 31 current D/N included; +0 new rows from recheck",
        },
        {
            "candidate_id": "reviewcue_29d4d29c_llm_scenario_nonhuman_hold",
            "workstream": "reviewcue_context_source_hold",
            "status": "hold_nonhuman_llm_replication_not_current_figure1",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Nature Computational Science LLM scenario-replication article or its OSF data package yield current Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/nature_s43588_025_00840_7.html",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/osf_j6wmn_metadata.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/osf_j6wmn_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/osf_j6wmn_osfstorage_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/osf_readme.md",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/osf_readme_data_processing.xlsx",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/keep_in_corpora_and_databases/title_a_large_scale_replication_of_scenario_based_experiments_in_psychology_and_management_using_large_language_models.json",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_result_table_worklist/title_can_large_language_models_replace_human_subjects_a_large_scale_replication_of_scenario_based_experiments_in_psychology_a.json",
            ],
            "relation_evidence": (
                "Article DOI 10.1038/s43588-025-00840-7 and OSF node j6wmn describe replication of 156 human "
                "scenario-based psychology/management experiments using GPT-4, Claude, and DeepSeek."
            ),
            "original_value_evidence": (
                "OSF README says the aggregate coding sheets include human_size, human_effsize, human_p_value, "
                "human_sig, and original study metadata hand-coded or drawn from original published articles."
            ),
            "replication_value_evidence": (
                "OSF README says the replication-side data are LLM responses and LLM_effsize/LLM_p_value fields from "
                "GPT-4, Claude, and DeepSeek study-level analyses."
            ),
            "mismatch_or_blocker": (
                "The source is explicitly human original studies versus nonhuman model-output replications. It has "
                "effect-size tables but no larger human replication N under the current Figure 1 population standard."
            ),
            "possible_reuse": "LLM-as-participant comparison project; nonhuman replication sensitivity appendix; prompt/data provenance",
            "next_action": "Skip for goal3000. Revisit only if nonhuman LLM replications become a separately scoped figure.",
            "row_count": "156 scenario experiments reported; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_6061ab8657b3_meta_analysis_vs_multilab_hold",
            "workstream": "reviewcue_context_source_hold",
            "status": "hold_meta_analysis_vs_replication_aggregate_not_current_figure1",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Kvarven et al. meta-analysis-versus-multiple-lab-replication source yield current Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/meta_analysis_vs_multilab_replications/nature_s41562_019_0787_z.html",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/meta_analysis_vs_multilab_replications/osf_vw3p6_metadata.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/meta_analysis_vs_multilab_replications/osf_vw3p6_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/meta_analysis_vs_multilab_replications/osf_vw3p6_osfstorage_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/meta_analysis_vs_multilab_replications/data_and_code_kvarven_et_al.zip",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/keep_in_corpora_and_databases/title_comparing_meta_analyses_and_pre_registered_multiple_labs_replication_projects.json",
            ],
            "relation_evidence": (
                "Nature article DOI 10.1038/s41562-019-0787-z says the study compares meta-analyses with large-scale "
                "preregistered multiple-laboratory replications and identified 15 meta-replication pairs."
            ),
            "original_value_evidence": "The checked source describes meta-analytic aggregate effect sizes, not individual original-study source-result values.",
            "replication_value_evidence": "The checked source describes multiple-lab replication project effect sizes and OSF data/code, not new original-vs-larger pair rows.",
            "mismatch_or_blocker": (
                "Aggregate meta-analysis effect versus replication-project effect is a different estimand/grain from the current "
                "Figure 1 one-original-result versus larger-replication-result row."
            ),
            "possible_reuse": "meta-analysis-vs-replication comparison figure; crosswalk to known RPP/ML/EERP/RRR source families",
            "next_action": "Skip for goal3000 row discovery; reuse only for a separate aggregate/meta-analysis project.",
            "row_count": "15 meta-replication pairs reported; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_27d5775f87b9_diener_osf_compilation_hold",
            "workstream": "reviewcue_context_source_hold",
            "status": "hold_reanalysis_compilation_not_pair_table",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Diener et al. OSF compilation yield current Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/osf_qdx7p_metadata.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/osf_qdx7p_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/osf_qdx7p_osfstorage_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/osf_qdx7p_data_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/osf_qdx7p_original_materials_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/README.Rmd",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/Diener_et_al_replication_data.csv",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/diener_osf_qdx7p/cleaned_diener_et_al_dataset.csv",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/keep_in_corpora_and_databases/title_compilation_of_diener_et_al_2010_osf_multi_site_replication_projects.json",
            ],
            "relation_evidence": (
                "OSF metadata says the page consists of data from Diener et al. replication datasets available on OSF and "
                "analysis conducted at the University of Minnesota. The downloaded data have 1,171 participant rows across nine study_site values."
            ),
            "original_value_evidence": "No source-backed original-study D/N or original effect text was found in the checked metadata, README, or downloaded CSV headers.",
            "replication_value_evidence": "Downloaded participant-level CSVs and README support reanalysis, not a plotted replication D/N result table.",
            "mismatch_or_blocker": (
                "Current Figure 1 needs a 1:1 source-backed original result and larger replication result. This package is a multi-site "
                "raw-data/reanalysis compilation, and using sites as rows would create invalid fanout."
            ),
            "possible_reuse": "well-being replication raw-data recomputation project; data package provenance",
            "next_action": "Skip for goal3000 unless a source-backed original/replication result table is located.",
            "row_count": "1,171 participant rows; 9 study sites; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "corpus_lead_social_exclusion_multisite_v5s6d_protocol_hold",
            "workstream": "corpus_lead_protocol_hold",
            "status": "hold_protocol_or_registration_no_final_replication_values",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes_until_final_results_or_data_table",
            "reviewed_question": "Can the Social Exclusion Multi-Site Replication Study OSF v5s6d yield current Figure 1 rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_v5s6d/node.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_v5s6d/files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_v5s6d/manifest.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_v5s6d/social_exclusion_multilab_rrr_pdf.pdf",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_v5s6d/social_exclusion_multilab_rrr_pdf.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/osf_t7zme_node.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/osf_t7zme_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/osf_t7zme_osfstorage.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/osf_9mwp3_node.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/osf_9mwp3_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/osf_9mwp3_osfstorage.json",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/coldfinger_confirmatory_Lazarevic_et_al.Rmd",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/coldfinger_confirmatory_Lazarevic_et_al.html",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/coldfinger_data.sav",
                ROOT / "data/raw/replication_projects/lead_harvest/osf_social_exclusion_multisite_followups/new_power_simulation_Lazarevic_et_al.R",
                ROOT / "data/raw/replication_projects/lead_harvest/social_exclusion_cold_blooded_loneliness/ijzerman_2012_cold_blooded_loneliness_mpg.pdf",
                ROOT / "data/raw/replication_projects/lead_harvest/social_exclusion_cold_blooded_loneliness/ijzerman_2012_cold_blooded_loneliness_mpg.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/social_exclusion_cold_blooded_loneliness/pubmed_22717422.txt",
                ROOT / "steps/searches/figure1/searchyield-figure1-corpusdb-expanded-new-leads.tsv",
            ],
            "relation_evidence": (
                "OSF node metadata titles the package 'Social Exclusion Multi-Site Replication Study' and describes it as "
                "a multi-site replication and extension of IJzerman et al. (2012). The mirrored PDF says the authors "
                "replicate IJzerman et al. (2012) with a highly powered multi-laboratory design. The referenced child "
                "nodes t7zme and 9mwp3 are titled 'Data Analytic Plan (Before registration)' and 'Power Calculation "
                "(Before registration)'."
            ),
            "original_value_evidence": (
                "The original Acta Psychologica PDF was mirrored after this check. It reports Study 1 social exclusion "
                "with the exclusion condition nnet=21, one participant excluded for technical failure, and a time x "
                "condition effect F(1, 38)=6.07, p=0.018. These original-side inputs may be reusable, but they do not "
                "complete a Figure 1 pair without final replication values."
            ),
            "replication_value_evidence": (
                "The mirrored PDF describes planned replication sample sizes, including a projected minimum N=500 and "
                "N=95 per cluster for power analysis, and states confirmatory analysis criteria in future-tense terms. "
                "The t7zme Rmd/HTML output contains model estimates, but the file explicitly begins by generating mock "
                "data for the preregistration analysis plan. The 9mwp3 branch exposes power-calculation materials and "
                "coldfinger_data.sav, not final multi-site replication results."
            ),
            "mismatch_or_blocker": (
                "The checked OSF/PDF package is protocol, power, and mock-analysis-plan documentation, not a final "
                "result-bearing article, table, or dataset output. Planned N, power inputs, and simulated/mock model "
                "estimates cannot be used as replication D/N."
            ),
            "possible_reuse": "social thermoregulation replication protocol provenance; future registered-report or result follow-up",
            "next_action": "Skip for goal3000 until a final result-bearing data table or article is obtained; do not promote planned values.",
            "row_count": "Original Study 1 N/effect located; protocol planned minimum N=500; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "individual_api_candidate_dae655618ec4c3be_bicultural_mainland_china_hold",
            "workstream": "individual_replication_paper_fulltext_hold",
            "status": "hold_mixed_original_target_and_metric_mismatch",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes_until_original_same_contrast_values_resolved",
            "reviewed_question": "Can Wang et al. 2025 Mainland China biculturalism yield strict Figure 1 original-vs-larger-replication rows?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/individual_search_batch001/api_candidate_dae655618ec4c3be/02_pmc_ncbi_nlm_nih_gov_articles_pmc11984341_e00733f452bc.html",
                ROOT / "data/raw/replication_projects/individual_search_batch001/api_candidate_dae655618ec4c3be/03_pubmed_ncbi_nlm_nih_gov_39804441_829d70c6b7de.html",
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-search-triage-batch001.tsv",
                ROOT / "steps/searches/figure1/individualrepsearch-screening-hits-batch008.tsv",
            ],
            "relation_evidence": (
                "The PMC full text says Study 1 replicated Hong et al. (1997) Experiment 2 and the initial test from "
                "Hong et al. (2000), testing whether Hong Kong college students are still bicultural. It also states "
                "that the authors made design changes, including separating internal and external attribution questions "
                "and using fish images adapted from Morris and Peng's original animation."
            ),
            "original_value_evidence": (
                "The article reports original comparison benchmarks only as omnibus f values: Hong et al. (2000) N=75, "
                "f=0.37, and Hong et al. (1997) N=75, f=0.18. It does not provide a same-source original pairwise "
                "Chinese-prime versus American-prime d for the exact current Study 1 contrast."
            ),
            "replication_value_evidence": (
                "Study 1 reports final N=107, randomized American N=36, Chinese N=35, neutral N=36. For internal "
                "attributions, it reports omnibus F(2,104)=20.23, p<.001, f2=.388 and pairwise American-versus-Chinese "
                "d=1.479. Study 2 reports Mainland China college-student extension N=272 with American-versus-Chinese "
                "d=1.062, but this is a population extension rather than the original Hong Kong population."
            ),
            "mismatch_or_blocker": (
                "Current Figure 1 needs one matched original result and one larger replication result on the same D axis. "
                "This candidate mixes Hong et al. 1997/2000 targets, gives original benchmarks as omnibus f rather than "
                "the same pairwise d contrast, and Study 2 changes population from Hong Kong to Mainland China."
            ),
            "possible_reuse": "biculturalism replication/extension case study; source-backed original-paper chase if Hong et al. pairwise values are later mirrored",
            "next_action": "Skip for goal3000 unless the original Hong et al. exact pairwise contrast values are obtained and matched to Study 1 only.",
            "row_count": "Study 1 N=107 and Study 2 N=272 available; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "individual_api_candidate_4b3dfa6a8bcf03d8_mmn_inclass_abstract_only_hold",
            "workstream": "individual_replication_paper_coverage_hold",
            "status": "coverage_only_abstract_relation_values_missing",
            "figure1_decision": "coverage_only_not_plot_ready",
            "skip_in_goal3000": "yes_until_full_text_and_original_values_acquired",
            "reviewed_question": "Can Scharf and Muller 2026 MMN conceptual in-class replication yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/individual_search_batch001/api_candidate_4b3dfa6a8bcf03d8/01_linkinghub_elsevier_com_retrieve_pii_s0167876026000127_728b66864305.html",
                ROOT / "data/raw/replication_projects/individual_search_batch001/api_candidate_4b3dfa6a8bcf03d8/02_pubmed_ncbi_nlm_nih_gov_41558583_4b33a4941abc.html",
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-search-triage-batch001.tsv",
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-source-mirror-batch001.tsv",
            ],
            "relation_evidence": (
                "PubMed abstract PMID 41558583 describes a conceptual in-class replication of Sussman, Ritter, and "
                "Vaughan Jr. (1998), saying the replication used a subset of the original predictable-versus-random "
                "pitch-deviant conditions and changed aspects of the original design."
            ),
            "original_value_evidence": (
                "No original Sussman et al. (1998) source object, original N, or original MMN effect text was acquired in "
                "the checked artifacts. The candidate entered through an abstract/direct-replication search hit only."
            ),
            "replication_value_evidence": (
                "The PubMed abstract reports a replication sample of 25 participants and qualitative frequentist/Bayesian "
                "evidence for ERP differences in the predictable-versus-random MMN window, but it does not provide a "
                "matched numeric D/SMD or complete value-bearing result table. The Elsevier DOI route mirrored only a "
                "LinkingHub redirect page, not full text."
            ),
            "mismatch_or_blocker": (
                "Current Figure 1 needs same-outcome original and larger replication D/N values. This candidate currently "
                "has only an abstract-level relation, replication N=25, and qualitative result language; original values "
                "and replication effect values are missing, and the replication is conceptual with design changes."
            ),
            "possible_reuse": "psychophysiology/MMN replication coverage; manual acquisition task if Elsevier full text or original Sussman source becomes available",
            "next_action": "Do not promote from abstract metadata. Revisit only after full text and the original Sussman value-bearing source are mirrored.",
            "row_count": "replication abstract N=25; +0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_ec299d9c57b4_olson_fazio_rrr_duplicate_primary",
            "workstream": "reviewcue_individual_rrr_duplicate",
            "status": "resolved_duplicate_existing_fred_row_provenance_hardening",
            "figure1_decision": "skip_already_accounted_for",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Olson/Fazio surveillance-task registered replication report yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/osf_hs32y_metadata.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/osf_hs32y_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/osf_hs32y_osfstorage_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/preregistered_materials_and_code.zip",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/extracted/meta-analysis_exclude_awere.csv",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/extracted/cohen Ds from papers.R",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/extracted/analysis.Rmd",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/olson_fazio_2001_psychscience_osu.pdf",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/olson_fazio_2001_psychscience_osu.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/moran_2021_accepted_manuscript_ugent.pdf",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/moran_2021_accepted_manuscript_ugent.txt",
            ],
            "relation_evidence": (
                "OSF node hs32y and the accepted manuscript identify a preregistered high-powered close replication of "
                "Olson and Fazio (2001)'s surveillance-task study. The manuscript says the final protocol was approved by "
                "the original authors and that it represents a close conceptual replication of Olson and Fazio (2001)."
            ),
            "original_value_evidence": (
                "Original PDF reports Experiment 2 with 56 undergraduate women, six excluded for noticing at least one "
                "CS-US contingency, and explicit pleasantness-rating effect t(48)=1.92, p=.03. The OSF prior-meta-analysis "
                "CSV records the same explicit Pleasantness ratings row as analyzed N=50, d=0.27, Hedges g=0.265846."
            ),
            "replication_value_evidence": (
                "Accepted manuscript reports total N=1478 and the primary analysis under the original Olson/Fazio awareness "
                "criterion as n=1340, Hedges g=0.12, 95% CI [0.05, 0.20], z=3.17, p=.002."
            ),
            "mismatch_or_blocker": (
                "The primary pleasantness-rating/Olson-Fazio-criterion row is already represented in the live root table as "
                "FReD row fred_soscisubmission38_1_1_1066. Promoting the individual-paper extraction would duplicate a plotted "
                "result. IAT, alternate awareness criteria, site-level effects, and prior-literature meta-analysis rows are also "
                "not added because they would create outcome or criterion fanout."
            ),
            "possible_reuse": "awareness-criterion sensitivity appendix; RRR provenance hardening; surveillance-task meta-analysis inventory",
            "next_action": "Keep skipped for goal3000; use the mirrored files only to harden or reconcile the existing FReD row.",
            "row_count": "+0 current Figure 1 rows; one duplicate primary row held; alternate candidate rows held as fanout",
        },
        {
            "candidate_id": "reviewcue_889e202a4dd5_fischer_att_snarc_rrr_already_integrated",
            "workstream": "reviewcue_resolved_source_family",
            "status": "resolved_rrr_colling_att_snarc_already_integrated",
            "figure1_decision": "skip_already_accounted_for",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Does the FischerRRR eyetracking Zenodo/GitHub code snapshot offer new current Figure 1 rows?",
            "source_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "data/derived/replication_pairs/harvest/promoted/rrr_colling_snarc__promoted_pairs.csv",
                ROOT / "data/raw/replication_projects/lead_harvest/rrr_colling_2020/colling_snarc_table_reconstruction.csv",
                ROOT / "data/raw/replication_projects/lead_harvest/rrr_colling_2020/github_attentional_snarc/attentional_snarc-master.zip",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_ljcolling_fischerrrr_eyetracking_fischer_et_al_2003_multi_lab_replication_main_task.json",
            ],
            "relation_evidence": (
                "Review cue 889e202a4dd5 routes DOI 10.5281/zenodo.3406447 and GitHub ljcolling/FischerRRR-eyetracking as a "
                "code snapshot for the Fischer et al. (2003) multi-lab replication main task. The live root table already has "
                "Colling et al. (2020) RRR rows for Fischer, Castel, Dodd, and Pratt (2003)."
            ),
            "original_value_evidence": (
                "Existing promoted RRR Colling rows preserve Fischer et al. original Att-SNARC D/N values for 250, 500, 750, "
                "and 1000 ms ISI outcomes."
            ),
            "replication_value_evidence": (
                "Existing promoted RRR Colling rows preserve Colling et al. replication D/N values for the same four ISI outcomes "
                "from the local table reconstruction."
            ),
            "mismatch_or_blocker": (
                "The review-cue artifact is a code/data support object for an already integrated source family. Promoting it as a new "
                "source would duplicate the four existing Att-SNARC plotted rows."
            ),
            "possible_reuse": "RRR Colling source-file provenance; raw-data recomputation audit; code availability appendix",
            "next_action": "Skip for goal3000 row discovery. Use only for source-file provenance or recomputation checks on existing rows.",
            "row_count": "4 existing current D/N rows; +0 new rows from this code snapshot",
        },
        {
            "candidate_id": "reviewcue_115f5ee33aea_oxytocin_trust_kroll_2026_promoted",
            "workstream": "reviewcue_individual_paper_promoted",
            "status": "promoted_current_figure1_row",
            "figure1_decision": "promoted_to_current_figure1",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Kroll et al. oxytocin trust registered report yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "scripts/scan_individual_replication_batch001_values.py",
                ROOT / "data/derived/replication_pairs/harvest/promoted/individual_replication_papers__promoted_pairs.csv",
                ROOT / "data/raw/replication_projects/review_cue_figure1_search_leads/oxytocin_trust_kroll_2026/kosfeld_2005_nature_oxytocin_increases_trust.pdf",
                ROOT / "data/raw/replication_projects/review_cue_figure1_search_leads/oxytocin_trust_kroll_2026/kosfeld_2005_nature_oxytocin_increases_trust.txt",
                ROOT / "data/raw/replication_projects/review_cue_figure1_search_leads/oxytocin_trust_kroll_2026/pci_rr_article_1136.html",
                ROOT / "data/raw/replication_projects/review_cue_figure1_search_leads/oxytocin_trust_kroll_2026/kroll_2026_stage2_manuscript_osf_kgz8h.pdf",
                ROOT / "data/raw/replication_projects/review_cue_figure1_search_leads/oxytocin_trust_kroll_2026/kroll_2026_stage2_manuscript_osf_kgz8h.txt",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_absence_of_a_meaningful_effect_of_intranasal_oxytocin_on_trusting_behavior_a_registered_report_with_pooled_equivalence_t.json",
            ],
            "relation_evidence": (
                "The PCI/OSF Stage 2 manuscript and review-cue receipt identify Kroll et al. (2026) as a large-scale "
                "replication of Kosfeld et al. (2005). The manuscript states that Kosfeld's key analysis used 29 vs. 29 "
                "investors on/off oxytocin, and that the new study tested the same oxytocin/placebo trust-game investment outcome."
            ),
            "original_value_evidence": (
                "Kosfeld et al. Table 1 reports trust-experiment investor mean transfers of 9.6 for oxytocin and 8.1 for placebo, "
                "SDs 2.8 and 3.1, and n=29 in each arm. The Kroll Stage 2 manuscript summarizes the original effect as "
                "Cohen's d=.51."
            ),
            "replication_value_evidence": (
                "Kroll et al. report final own-data N=211, with 99 oxytocin and 112 placebo participants. Hypothesis 1b reports "
                "Hedges' g=-.12, 96% CI [-.40, .17], for the standardized effect of oxytocin on interpersonal trust; Figure 1 "
                "stores the nonnegative magnitude 0.12."
            ),
            "mismatch_or_blocker": (
                "Promoted one matched row using the own direct replication only. The source also reports a pooled Kroll+Declerck "
                "N=532 estimate, Hedges' g=-.07, but that was held out of the plotted row to avoid collapsing multiple replication "
                "studies when a same-paper single-replication estimate exists."
            ),
            "possible_reuse": "pooled-replication sensitivity; OXT/trust source-result provenance; equivalence-testing methods appendix",
            "next_action": "Already counted in goal3000; do not re-add. Use only for provenance hardening or an explicit pooled-analysis sensitivity.",
            "row_count": "+1 current Figure 1 D/N row; pooled n=532 estimate checked and not promoted",
        },
        {
            "candidate_id": "reviewcue_b7d63ec6dc91_victim_impact_curriculum_source_blocked",
            "workstream": "reviewcue_individual_paper_source_blocked",
            "status": "coverage_only_tandf_challenge_no_value_source",
            "figure1_decision": "coverage_only_manual_acquisition_needed",
            "skip_in_goal3000": "yes_until_manual_acquisition",
            "reviewed_question": "Can the victim-impact curriculum multi-site replication article yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/victim_impact_curriculum/crossref_10.1080_1478601x.2015.1014037.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/victim_impact_curriculum/doi_landing_headers.txt",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/victim_impact_curriculum/doi_landing.html",
                ROOT / "steps/source_inventory/figure1/result_artifact_acquisition/figure1-result-artifact-acquisition-attempts.tsv",
                ROOT / "steps/source_inventory/figure1/result_artifact_acquisition/figure1-result-artifact-acquisition-manual-tasks.tsv",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_administering_a_victim_impact_curriculum_to_inmates_a_multi_site_replication.json",
            ],
            "relation_evidence": (
                "Crossref and the review-cue receipt identify DOI 10.1080/1478601x.2015.1014037, title 'Administering a "
                "victim impact curriculum to inmates: a multi-site replication'."
            ),
            "original_value_evidence": "No source-backed original D/N or original effect text was acquired; only Crossref metadata and an access-blocked landing page are local.",
            "replication_value_evidence": "No value-bearing replication effect/N text was acquired; the DOI landing attempt ended at a Cloudflare/Taylor & Francis HTTP 403 challenge page.",
            "mismatch_or_blocker": (
                "Public automated acquisition did not produce a value-bearing article, supplement, or dataset. Current artifacts "
                "support a bibliographic lead and access blocker only."
            ),
            "possible_reuse": "criminal-justice curriculum replication lead; manual/library acquisition task",
            "next_action": "Skip automated goal3000 work until a PDF/HTML/full text, supplement, or data artifact is manually acquired.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_f5860736bcb1_caballero_project_404",
            "workstream": "reviewcue_individual_paper_source_blocked",
            "status": "source_route_404_project_unavailable",
            "figure1_decision": "coverage_only_source_unavailable",
            "skip_in_goal3000": "yes_until_source_reappears",
            "reviewed_question": "Can the Caballero 2021 replication project yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/caballero_2021_replication/osf_kdbsa_api.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/caballero_2021_replication/osf_kdbsa_http_status.txt",
                ROOT / "steps/review_cue/figure1_search_leads/reviewcue-codex-expanded001-figure1_search_leads.json",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_caballero_2021_replication_project.json",
            ],
            "relation_evidence": (
                "The saved review-cue/search metadata describes a direct replication of Study 2 from Caballero et al. (2021), "
                "using the Bimboola economic-scarcity manipulation and Behavioral Identification Form."
            ),
            "original_value_evidence": "No source-backed original effect/N text was acquired from the now-unavailable OSF route.",
            "replication_value_evidence": "No replication N/effect/result file was acquired; OSF API node kdbsa returned 404.",
            "mismatch_or_blocker": "The only concrete project route is unavailable, so the lead is not retraceable to value-bearing bytes.",
            "possible_reuse": "economic-scarcity/construal replication lead if OSF route reappears or user supplies files",
            "next_action": "Skip for goal3000 unless the OSF project or a mirrored copy becomes available.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_5a6989d0ac69_earth_science_citation_project_404",
            "workstream": "reviewcue_individual_paper_source_blocked",
            "status": "planned_registration_route_404_no_results",
            "figure1_decision": "coverage_only_registration_unavailable",
            "skip_in_goal3000": "yes_until_source_reappears",
            "reviewed_question": "Can the earth-science citation replication project yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/earth_science_citation_replication/osf_u49zv_api.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/earth_science_citation_replication/osf_u49zv_http_status.txt",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_earth_science_citation_replication_project.json",
            ],
            "relation_evidence": "Review-cue metadata says the registration planned to replicate White 2019 and scale the original study.",
            "original_value_evidence": "No original citation-practice effect/N text was acquired.",
            "replication_value_evidence": "No completed replication result file or value text was acquired; OSF API node u49zv returned 404.",
            "mismatch_or_blocker": "The available evidence is a planned-registration lead with an unavailable OSF route, not a completed source-backed replication result.",
            "possible_reuse": "citation-practice replication lead if registration/results reappear",
            "next_action": "Skip for current Figure 1 until a public completed result source is found.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_6c2f7ee495da_ecls_k_computational_replication_hold",
            "workstream": "reviewcue_context_source_hold",
            "status": "hold_computational_replication_code_not_current_figure1",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the ECLS-K replication project yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/ecls_k_replication/osf_gvzwe_api.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/ecls_k_replication/osf_gvzwe_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/ecls_k_replication/osf_gvzwe_osfstorage_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/ecls_k_replication/osf_hsgj2_api.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/ecls_k_replication/Replication_Analysis_Using_R.Rmd",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/ecls_k_replication/EXTRACTfinal.sas",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_ecls_k_replication_project.json",
            ],
            "relation_evidence": "The OSF node title is 'ECLS-K Replication Project' and its description says it is for a ReScience X article.",
            "original_value_evidence": "No original experimental D/N source-result values were present; the files are analysis/extraction scripts for an existing observational education dataset.",
            "replication_value_evidence": "The mirrored R Markdown file runs lmer models on ECLS-K variables but does not expose a plotted original-vs-larger replication D/N pair.",
            "mismatch_or_blocker": "This is computational reproducibility code, not a human experimental original/replication effect pair under current Figure 1 policy.",
            "possible_reuse": "computational reproducibility inventory; education-data reproducibility context",
            "next_action": "Skip for current Figure 1 rows unless a separate computational-reproducibility figure is scoped.",
            "row_count": "+0 current Figure 1 rows",
        },
        {
            "candidate_id": "reviewcue_6e23c48b1120_stroop_dataset_original_target_missing",
            "workstream": "reviewcue_context_source_hold",
            "status": "hold_data_only_course_assignment_original_target_missing",
            "figure1_decision": "hold_context_source_not_plot_ready",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the Stroop replication study dataset yield a strict current Figure 1 row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/stroop_replication_dataset/osf_un4cb_api.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/stroop_replication_dataset/osf_un4cb_files.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/stroop_replication_dataset/osf_un4cb_osfstorage_listing.json",
                ROOT / "data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/stroop_replication_dataset/osf_un4cb_dataset_folder_listing.json",
                ROOT / "data/raw/source_artifacts/figure1_acquisition_tabular_first/repo_search_osf_1b6223afbba2/source_artifact_bf22977820c1e363__Stroop_final_dataset_RP.sav",
                ROOT / "steps/source_inventory/figure1/result_artifact_acquisition/mirror_sample_tabular_first/artifact_samples/source_artifact_bf22977820c1e363.json",
                ROOT / "steps/review_cue/figure1_search_leads/receipts/route_to_individual_replication_paper_worklist/title_stroop_replication_study_dataset.json",
            ],
            "relation_evidence": "The OSF node title is 'Stroop Replication Study Dataset' and the description says it was collected for a University of Bristol course assignment.",
            "original_value_evidence": "No original target paper, original N, or original effect was identified in OSF metadata or the mirrored SAV dataset.",
            "replication_value_evidence": "The mirrored SAV contains 416 cell-level rows for 104 participants across posture/congruency cells, but no asserted replication effect or report text.",
            "mismatch_or_blocker": "Data-only teaching package lacks a retraceable original-vs-larger replication mapping and value-bearing result assertion.",
            "possible_reuse": "teaching dataset; Stroop raw-data exercise; parser coverage for SAV files",
            "next_action": "Skip for current Figure 1 unless an original target and value-bearing replication report are supplied.",
            "row_count": "+0 current Figure 1 rows; 104 participants inferred from SAV IDs",
        },
        {
            "candidate_id": "reviewcue_known_source_family_overlap_batch_20260508",
            "workstream": "reviewcue_resolved_source_family",
            "status": "resolved_known_source_families_already_integrated_or_context_only",
            "figure1_decision": "skip_already_accounted_for_or_not_row_source",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Which review-cue advance rows are aliases for source families already represented or context-only hubs?",
            "source_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "steps/review_cue/figure1_search_leads/reviewcue-routing-table-figure1_search_leads.tsv",
                ROOT / "steps/corpus_results/figure1/fred_live_rescue_20260508/fred-archive-rescue-candidate-scan.tsv",
                ROOT / "steps/corpus_results/figure1/goal3000_strategy_probe_20260508/local-tabular-side-field-candidate-scan.tsv",
            ],
            "relation_evidence": (
                "Resolved review-cue aliases include RPCB, Many Labs/JOPD, Boyce/SRP, Decision-Market, EERP, FReD/FORRT, "
                "RPP, RSESR, and selected file-level result packages. These sources already have live root rows or are context/provenance indexes."
            ),
            "original_value_evidence": "Live root rows and source-family builders already preserve numeric D/N values where rows are in scope.",
            "replication_value_evidence": "Live root rows and source-family builders already preserve numeric D/N values where rows are in scope.",
            "mismatch_or_blocker": (
                "No new safe bulk row pool remains in these aliases without duplicate re-ingest, site/lab fanout, or non-value-bearing context-source promotion."
            ),
            "possible_reuse": "source-result provenance hardening; duplicate-source reconciliation; context source catalog",
            "next_action": "Keep these review cues skipped for goal3000; revisit only for provenance or dedupe audits.",
            "row_count": "resolved 12 review-cue aliases; +0 new rows",
        }
    ]
    batch009_common_paths = [
        ROOT / "reports/figure1_individual_replication_vast_search_execution_batch009_2026-05-05.md",
        ROOT / "steps/searches/figure1/individualrepsearch-query-log-batch009.tsv",
        ROOT / "steps/searches/figure1/individualrepsearch-screening-hits-batch009.tsv",
        ROOT / "steps/searches/figure1/individualrepsearch-api-batch009.json",
    ]
    batch009_candidate_specs = [
        {
            "candidate_id": "batch009_positive_single_center_multicenter_rct_review_context",
            "status": "reject_systematic_review_context_not_single_pair",
            "figure1_decision": "reject_current_figure1_not_single_pair",
            "reviewed_question": "Can the critical-care single-center versus multicenter RCT systematic review yield immediate current Figure 1 rows?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/crossref/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0063_crossref.json",
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/crossref/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0072_crossref.json",
            ],
            "relation_evidence": (
                "Metadata hit DOI 10.1186/s13054-023-04755-5 states that mortality reduction shown by single-center RCTs "
                "is typically not replicated by multicenter RCTs."
            ),
            "original_value_evidence": (
                "The batch009 metadata/API pass did not resolve one original critical-care trial, one original effect/N, "
                "or a matched original source object."
            ),
            "replication_value_evidence": (
                "The metadata describes a systematic review pattern across trials, not one larger replication effect/N row "
                "ready for current Figure 1."
            ),
            "mismatch_or_blocker": (
                "Review/context article. It may contain a structured trial mapping if separately parsed, but the batch009 "
                "evidence is not a single source-backed 1:1 original-vs-larger-replication result."
            ),
            "possible_reuse": "clinical single-center versus multicenter RCT corpus lead; review-level source-family mining",
            "next_action": "Do not promote from metadata. Revisit only through a dedicated parser that extracts explicit trial pairs and D/N-convertible outcomes.",
        },
        {
            "candidate_id": "batch009_somatostatin_pancreatic_fistula_review_context",
            "status": "reject_review_context_no_single_matched_pair",
            "figure1_decision": "reject_current_figure1_not_single_pair",
            "reviewed_question": "Can the somatostatin-analog pancreatic-fistula review yield a strict current Figure 1 row?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0063_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1245/s10434-025-17660-8 says early randomized trials showed benefit, "
                "while subsequent single-center studies failed to confirm results."
            ),
            "original_value_evidence": "No one original trial effect/N was identified by the metadata pass.",
            "replication_value_evidence": "No one larger replication effect/N was identified by the metadata pass.",
            "mismatch_or_blocker": (
                "Narrative/review context rather than an explicit 1:1 original trial versus larger replication result. "
                "The cited later evidence is also described as subsequent single-center studies, not clearly larger replications."
            ),
            "possible_reuse": "clinical review context; pancreatic-surgery evidence-history lead",
            "next_action": "Skip for goal3000 unless full-text parsing finds an explicit larger matched trial pair with D/N-convertible values.",
        },
        {
            "candidate_id": "batch009_glenzocimab_actisave_original_target_unresolved",
            "status": "coverage_only_original_target_not_resolved",
            "figure1_decision": "hold_needs_more_evidence_not_plot_ready",
            "reviewed_question": "Can ACTISAVE glenzocimab be paired to an earlier source-backed beneficial result?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0066_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1161/strokeaha.125.052935 says ACTISAVE failed to confirm a beneficial "
                "effect of glenzocimab on mRS in acute ischemic stroke."
            ),
            "original_value_evidence": (
                "The metadata does not identify the earlier beneficial study, its endpoint/timepoint, original N, or original effect."
            ),
            "replication_value_evidence": (
                "The abstract snippet contains ACTISAVE event counts, but a matched D/N conversion and original target were not resolved."
            ),
            "mismatch_or_blocker": (
                "Confirmatory-trial language without a resolved original source/result. Promoting would rely on an implicit target."
            ),
            "possible_reuse": "stroke clinical-trial follow-up lead; possible future binary/ordinal outcome conversion case",
            "next_action": "Hold until the earlier glenzocimab result and matched ACTISAVE endpoint are source-verified.",
        },
        {
            "candidate_id": "batch009_cerebrolysin_clinch_future_confirmatory_pilot",
            "status": "reject_pilot_no_completed_larger_replication",
            "figure1_decision": "reject_current_figure1_future_trial_only",
            "reviewed_question": "Can the CLINCH cerebrolysin pilot be used as a current Figure 1 replication row?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0068_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.3389/fneur.2025.1602956 says positive pilot results would support a larger "
                "confirmatory trial and inform sample size."
            ),
            "original_value_evidence": "The article is itself a pilot/feasibility trial, not the original side of a completed larger replication pair.",
            "replication_value_evidence": "No completed larger confirmatory replication result was present in the metadata pass.",
            "mismatch_or_blocker": "Future-tense confirmatory-trial planning is not an observed larger replication attempt.",
            "possible_reuse": "future clinical follow-up watchlist; pilot-to-confirmatory trial inventory",
            "next_action": "Skip for current Figure 1 until a completed larger confirmatory trial is published with matched values.",
        },
        {
            "candidate_id": "batch009_scopolamine_antidepressant_already_promoted",
            "status": "skip_already_accounted_for",
            "figure1_decision": "skip_already_accounted_for",
            "reviewed_question": "Is the scopolamine antidepressant replication candidate new after batch009 rediscovery?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/crossref/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0069_crossref.json",
            ],
            "extra_paths": [
                ROOT / "FIGURE1_REPLICATION_PAIRS.tsv",
                ROOT / "steps/individual_replication_papers/figure1/individual-paper-value-scan-batch001.tsv",
                ROOT / "data/derived/replication_pairs/harvest/promoted/individual_replication_papers__promoted_pairs.csv",
            ],
            "relation_evidence": (
                "Batch009 rediscovered DOI 10.1016/j.biopsych.2009.11.021, title 'Replication of Scopolamine's "
                "Antidepressant Efficacy in Major Depressive Disorder'."
            ),
            "original_value_evidence": (
                "The existing individual value scan row `batch014_value_scopolamine_antidepressant_block1` already records "
                "the Furey and Drevets original MADRS block-1 D=2.7 and N=18."
            ),
            "replication_value_evidence": (
                "The promoted row already records the independent scopolamine replication MADRS block-1 D=1.38 and N=22."
            ),
            "mismatch_or_blocker": (
                "Already represented in the live root table as `individual_api_candidate_710fd7eb55fc9d77_scopolamine_antidepressant_efficacy_first_random`."
            ),
            "possible_reuse": "provenance hardening only; duplicate-detection regression case",
            "next_action": "Do not add a second row. Use only for source-result support or duplicate-check tests.",
        },
        {
            "candidate_id": "batch009_glp1_dementia_target_trial_emulation_validation",
            "status": "reject_observational_validation_not_original_replication_pair",
            "figure1_decision": "reject_current_figure1_not_trial_replication_pair",
            "reviewed_question": "Can the GLP-1 dementia target-trial emulation validation article yield a current Figure 1 row?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0069_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1111/dom.70384 describes target-trial emulation in one EHR network with "
                "external validation in TriNetX."
            ),
            "original_value_evidence": "No original experimental source result was identified; the lead is an observational emulation design.",
            "replication_value_evidence": "External validation is across EHR data networks, not a larger replication trial result with D/N values.",
            "mismatch_or_blocker": "Observational validation/target-trial emulation is outside the current original-vs-larger experimental replication row standard.",
            "possible_reuse": "real-world evidence validation inventory; observational robustness project",
            "next_action": "Skip for current Figure 1.",
        },
        {
            "candidate_id": "batch009_tbi_machine_learning_external_validation",
            "status": "reject_ml_phenotype_validation_not_effect_replication",
            "figure1_decision": "reject_current_figure1_not_effect_replication",
            "reviewed_question": "Can the TBI phenotype external-validation study yield a current Figure 1 row?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0070_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1089/neu.2019.6705 describes external validation of machine-learning "
                "phenotypes in TRACK-TBI Pilot."
            ),
            "original_value_evidence": "No original intervention/behavioral effect or source-backed original D/N result is present.",
            "replication_value_evidence": "The external validation concerns phenotype reproducibility, not a matched larger replication effect.",
            "mismatch_or_blocker": "Prediction/phenotype validation is not an original effect versus larger replication effect pair.",
            "possible_reuse": "prediction-model external validation corpus; non-Figure-1 reproducibility inventory",
            "next_action": "Skip for current Figure 1.",
        },
        {
            "candidate_id": "batch009_pseudomonas_cf_vaccine_cochrane_review_context",
            "status": "hold_review_context_unpublished_large_trial",
            "figure1_decision": "hold_needs_more_evidence_not_plot_ready",
            "reviewed_question": "Can the Pseudomonas aeruginosa cystic-fibrosis vaccine review yield a strict current Figure 1 row?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0071_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1002/14651858.cd001399.pub4 says one large trial failed to confirm an "
                "earlier study according to a company press release, while another large trial reported RR 0.91."
            ),
            "original_value_evidence": "The metadata pass did not resolve the earlier study's exact effect/N or source object.",
            "replication_value_evidence": (
                "The review snippet says one large trial had no published data and another reports a relative risk, but no "
                "matched D/N-converted 1:1 pair was extracted."
            ),
            "mismatch_or_blocker": (
                "Review context with unpublished/press-release trial evidence and native RR outcome. Not plot-ready under current D/N standard."
            ),
            "possible_reuse": "clinical failed-confirmation context; binary/RR conversion policy test case if trial reports are obtained",
            "next_action": "Hold until original and replication trial reports are acquired and a matched D conversion is approved.",
        },
        {
            "candidate_id": "batch009_epipan_acute_pancreatitis_original_target_unresolved",
            "status": "coverage_only_original_target_not_resolved",
            "figure1_decision": "hold_needs_more_evidence_not_plot_ready",
            "reviewed_question": "Can EPIPAN thoracic epidural analgesia be paired to an earlier hypothesized-benefit source?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0072_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1186/s13054-023-04502-w says the first multicenter randomized trial did "
                "not show the hypothesized benefit of epidural analgesia in acute pancreatitis."
            ),
            "original_value_evidence": "No earlier original source result with matched endpoint/effect/N was identified by the metadata pass.",
            "replication_value_evidence": "The multicenter trial is identified, but no D/N-convertible matched endpoint was extracted.",
            "mismatch_or_blocker": "Hypothesized benefit language is insufficient to infer a source-backed original result.",
            "possible_reuse": "acute-pancreatitis clinical follow-up lead",
            "next_action": "Hold until earlier source evidence and matched EPIPAN values are obtained.",
        },
        {
            "candidate_id": "batch009_benzoate_alzheimers_confirmatory_language_unresolved",
            "status": "coverage_only_original_target_not_resolved",
            "figure1_decision": "hold_needs_more_evidence_not_plot_ready",
            "reviewed_question": "Can the benzoate Alzheimer's dose-finding trial be paired to an earlier source-backed result?",
            "raw_paths": [
                "steps/searches/figure1/individualrepsearch_api_batch009/raw/europepmc/07_clinical_d_equivalent_followup_pubmed_pmc_clinicaltrials_gov_crossref_0073_europepmc.json",
            ],
            "relation_evidence": (
                "Europe PMC metadata for DOI 10.1111/pcn.13504 says a confirmatory trial with biomarkers was needed and "
                "that the study aimed to confirm benzoate as a novel Alzheimer's treatment."
            ),
            "original_value_evidence": "The earlier benzoate result, its endpoint/timepoint, original N, and source-backed effect were not resolved.",
            "replication_value_evidence": "The dose-finding trial is identified, but matched D/N-convertible replication values were not extracted.",
            "mismatch_or_blocker": "Confirmatory language alone is not enough for a current Figure 1 row.",
            "possible_reuse": "Alzheimer's clinical follow-up lead; biomarker-confirmatory trial context",
            "next_action": "Hold until the original result and matched replication endpoint are source-verified.",
        },
    ]
    for spec in batch009_candidate_specs:
        manual_source_specs.append(
            {
                "candidate_id": spec["candidate_id"],
                "workstream": "individual_search_batch009_metadata_adjudication",
                "status": spec["status"],
                "figure1_decision": spec["figure1_decision"],
                "skip_in_goal3000": "yes",
                "reviewed_question": spec["reviewed_question"],
                "source_paths": [
                    *batch009_common_paths,
                    *(ROOT / raw_path for raw_path in spec["raw_paths"]),
                    *spec.get("extra_paths", []),
                ],
                "relation_evidence": spec["relation_evidence"],
                "original_value_evidence": spec["original_value_evidence"],
                "replication_value_evidence": spec["replication_value_evidence"],
                "mismatch_or_blocker": spec["mismatch_or_blocker"],
                "possible_reuse": spec["possible_reuse"],
                "next_action": spec["next_action"],
                "row_count": "+0 current Figure 1 rows; batch009 metadata pass only",
            }
        )

    for spec in manual_source_specs:
        existing_paths = [path for path in spec["source_paths"] if path.exists()]
        checksums = [f"{rel(path)}={file_sha256(path)}" for path in existing_paths]
        rows.append(
            {
                "reviewed_at": REVIEWED_AT,
                "workstream": spec["workstream"],
                "candidate_id": spec["candidate_id"],
                "status": spec["status"],
                "figure1_decision": spec["figure1_decision"],
                "skip_in_goal3000": spec["skip_in_goal3000"],
                "reviewed_question": spec["reviewed_question"],
                "source_evidence_paths": "; ".join(rel(path) for path in existing_paths),
                "source_checksums": "; ".join(checksums),
                "relation_evidence": spec["relation_evidence"],
                "original_value_evidence": spec["original_value_evidence"],
                "replication_value_evidence": spec["replication_value_evidence"],
                "mismatch_or_blocker": spec["mismatch_or_blocker"],
                "possible_reuse": spec["possible_reuse"],
                "next_action": spec["next_action"],
                "row_count": spec["row_count"],
                "source_artifact": "; ".join(rel(path) for path in existing_paths),
            }
        )


def write_source_ledger() -> Path:
    rows: list[dict[str, object]] = []
    add_source_rows(rows)
    df = pd.DataFrame(rows, columns=COMMON_COLUMNS).fillna("")
    path = OUT_DIR / "source-strategy-adjudication.tsv"
    df.to_csv(path, sep="\t", index=False)
    return path


def classify_metascience_outside_candidate(row: pd.Series) -> tuple[str, str]:
    tag = clean(row.get("tag"))
    original_title = clean(row.get("original_title"))
    doi_pair_rows = float(row.get("current_root_same_doi_pair_rows") or 0)
    value_alias_rows = float(row.get("root_value_alias_match_count") or 0)
    same_original_doi_rows = float(row.get("current_root_same_original_doi_rows") or 0)
    same_replication_doi_rows = float(row.get("current_root_same_replication_doi_rows") or 0)

    if doi_pair_rows > 0:
        return (
            "reject_duplicate_existing_root_doi_pair",
            (
                f"Exact original/replication DOI pair is already represented in {doi_pair_rows:g} root row(s). "
                "Adding the Metascience/FReD assertion would duplicate an existing plotted source-family row."
            ),
        )
    if value_alias_rows > 0:
        return (
            "reject_duplicate_existing_root_value_alias",
            (
                f"Candidate D/N value tuple matched {value_alias_rows:g} existing root row(s), even when DOI aliases differ "
                "or are absent from the root row."
            ),
        )
    if tag == "RP:P":
        return (
            "reject_duplicate_existing_rpp_source_family_alias",
            (
                "Apparently DOI/value-new RP:P candidate is the same represented RPP/OSC 2015 pair already in the "
                "RPP canonical OSF source family. The Metascience row has source-family/N metadata differences, so it is "
                "useful for reconciliation, not a second plotted row."
            ),
        )
    if tag == "XPHIR":
        return (
            "reject_duplicate_existing_eprp_source_family_alias",
            (
                "The XPHIR row is the Machery cross-cultural semantics experimental-philosophy pair already represented "
                "in the EPRP source family; exact value matching missed it because of source-title and rounding aliases."
            ),
        )
    if tag == "ML2":
        if "similarity" in original_title.lower():
            return (
                "reject_many_labs2_outcome_fanout_existing_source_family",
                (
                    "Many Labs 2 Direction/Similarity candidates are source-family overlaps with the live Many Labs 2 "
                    "public join. Multiple Metascience rows split related Gati/Tversky outcomes, so bulk promotion would "
                    "risk outcome fanout rather than add new strict 1:1 pairs."
                ),
            )
        return (
            "reject_duplicate_existing_many_labs2_source_family_alias",
            (
                "Many Labs 2 candidate is an alias of an existing Many Labs 2 public-join row. The checked source differs "
                "in conversion or bibliographic metadata, but not in represented original-vs-replication relationship."
            ),
        )
    if tag == "ML5":
        return (
            "reject_duplicate_or_fanout_existing_many_labs5_source_family_alias",
            (
                "Many Labs 5 candidates overlap existing RPP, SRP, and FReD Many Labs 5 rows. Several rows contain multiple "
                "replication estimates for one original target; adding them from this outside-family surface would risk "
                "duplicate source-family aliases or one-to-many fanout."
            ),
        )
    if same_original_doi_rows > 0 or same_replication_doi_rows > 0:
        return (
            "hold_source_family_overlap_needs_row_level_reconciliation",
            (
                "Candidate shares an original or replication DOI with live root rows but did not match exact DOI pair/value "
                "tuple. Treat as a reconciliation item, not a safe new-row source."
            ),
        )
    return (
        "hold_outside_allowed_family_needs_reconstruction",
        "No safe current-Figure-1 row decision was reconstructable from the outside-family scan alone.",
    )


def write_metascience_outside_family_ledger() -> Path | None:
    surface_path = OUT_DIR / "metascience-outside-allowed-family-strict-numeric-candidates-20260508.tsv"
    surface = read_table(surface_path)
    if surface is None:
        return None
    raw_api = ROOT / "data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json"
    root_path = ROOT / "FIGURE1_REPLICATION_PAIRS.tsv"
    evidence_paths = [path for path in [surface_path, raw_api, root_path] if path.exists()]
    evidence_text = "; ".join(rel(path) for path in evidence_paths)
    checksums = "; ".join(f"{rel(path)}={file_sha256(path)}" for path in evidence_paths)
    rows = []
    for idx, row in surface.reset_index(drop=True).iterrows():
        status, blocker = classify_metascience_outside_candidate(row)
        tag = clean(row.get("tag"))
        source = clean(row.get("source")) or "Metascience Observatory / FReD API"
        candidate_id = f"metascience_outside_{idx + 1:03d}_{tag.lower()}_{slug(row.get('original_title'), 44)}"
        rows.append(
            {
                "reviewed_at": REVIEWED_AT,
                "workstream": "metascience_outside_allowed_family_strict_numeric",
                "candidate_id": candidate_id,
                "status": status,
                "figure1_decision": "skip_already_accounted_for_or_needs_reconciliation",
                "skip_in_goal3000": "yes",
                "reviewed_question": "Is this outside-allowlist Metascience/FReD strict numeric candidate a safe new Figure 1 row?",
                "source_evidence_paths": evidence_text,
                "source_checksums": checksums,
                "relation_evidence": (
                    f"{tag} candidate from {source}: original '{clean(row.get('original_title'))}' versus "
                    f"replication '{clean(row.get('replication_title'))}'. Description: {clean(row.get('description'))}"
                ),
                "original_value_evidence": (
                    f"original_n={clean(row.get('original_n_num'))}; D_original={clean(row.get('D_original'))}; "
                    f"r_original={clean(row.get('original_r_num'))}; doi={clean(row.get('original_doi'))}; "
                    f"url={clean(row.get('original_url'))}"
                ),
                "replication_value_evidence": (
                    f"replication_n={clean(row.get('replication_n_num'))}; D_replication={clean(row.get('D_replication'))}; "
                    f"r_replication={clean(row.get('replication_r_num'))}; doi={clean(row.get('replication_doi'))}; "
                    f"url={clean(row.get('replication_url'))}"
                ),
                "mismatch_or_blocker": (
                    f"{blocker} Overlap counters: current_root_same_doi_pair_rows={clean(row.get('current_root_same_doi_pair_rows'))}; "
                    f"current_root_same_original_doi_rows={clean(row.get('current_root_same_original_doi_rows'))}; "
                    f"current_root_same_replication_doi_rows={clean(row.get('current_root_same_replication_doi_rows'))}; "
                    f"root_value_alias_match_count={clean(row.get('root_value_alias_match_count'))}."
                ),
                "possible_reuse": "source-family duplicate reconciliation; DOI enrichment; conversion-discrepancy audit; future row-grain policy review",
                "next_action": "Do not promote from this outside-family surface during goal3000 unless a separate row-level reconciliation replaces an existing row instead of adding a duplicate.",
                "row_count": "1",
                "source_artifact": rel(surface_path),
                "source": source,
                "tag": tag,
                "original_title": clean(row.get("original_title")),
                "replication_title": clean(row.get("replication_title")),
                "description": clean(row.get("description")),
                "original_doi": clean(row.get("original_doi")),
                "replication_doi": clean(row.get("replication_doi")),
                "original_n_num": clean(row.get("original_n_num")),
                "replication_n_num": clean(row.get("replication_n_num")),
                "D_original": clean(row.get("D_original")),
                "D_replication": clean(row.get("D_replication")),
                "current_root_same_doi_pair_rows": clean(row.get("current_root_same_doi_pair_rows")),
                "current_root_same_original_doi_rows": clean(row.get("current_root_same_original_doi_rows")),
                "current_root_same_replication_doi_rows": clean(row.get("current_root_same_replication_doi_rows")),
                "root_value_alias_match_count": clean(row.get("root_value_alias_match_count")),
            }
        )
    out = OUT_DIR / "metascience-outside-allowed-family-adjudication-20260508.tsv"
    pd.DataFrame(rows, columns=METASCIENCE_OUTSIDE_COLUMNS).fillna("").to_csv(out, sep="\t", index=False)
    return out


def write_reviewcue_ledger() -> Path | None:
    path = ROOT / "steps/review_cue/figure1_search_leads/reviewcue-routing-table-figure1_search_leads.tsv"
    df = read_table(path)
    if df is None:
        return None
    value_scan_summaries = individual_value_scan_reviewcue_summaries()
    rows = []
    for row in df.to_dict("records"):
        decision = clean(row.get("decision"))
        skip = "no" if clean(row.get("advances_to_figure1_pair_intake")).lower() == "true" else "yes"
        candidate_id = clean(row.get("review_id")) or clean(row.get("lead_key"))
        out_row = {
            "reviewed_at": clean(row.get("created_at")) or REVIEWED_AT,
            "workstream": "review_cue_figure1_search_leads",
            "candidate_id": candidate_id,
            "status": decision,
            "figure1_decision": clean(row.get("routing_class")),
            "skip_in_goal3000": skip,
            "reviewed_question": clean(row.get("lead_key")),
            "source_evidence_paths": "; ".join(x for x in [clean(row.get("receipt_path")), clean(row.get("sources_checked_json"))] if x),
            "source_checksums": "",
            "relation_evidence": clean(row.get("route_payload_json")),
            "original_value_evidence": "",
            "replication_value_evidence": "",
            "mismatch_or_blocker": clean(row.get("reason")),
            "possible_reuse": clean(row.get("notes")) or "review cue routing provenance",
            "next_action": clean(row.get("next_action")),
            "row_count": "",
            "source_artifact": rel(path),
        }
        if candidate_id in value_scan_summaries:
            out_row.update(value_scan_summaries[candidate_id])
        if candidate_id in REVIEWCUE_RESOLUTION_OVERRIDES:
            out_row.update(REVIEWCUE_RESOLUTION_OVERRIDES[candidate_id])
        rows.append(
            {
                key: clean(value)
                for key, value in out_row.items()
            }
        )
    out = OUT_DIR / "reviewcue-adjudication.tsv"
    pd.DataFrame(rows, columns=COMMON_COLUMNS).fillna("").to_csv(out, sep="\t", index=False)
    return out


def write_ying_ledger() -> Path:
    ledger_path = OUT_DIR / "ying-candidate-adjudication.tsv"
    if ledger_path.exists():
        ledger = pd.read_csv(ledger_path, sep="\t").fillna("")
    else:
        ledger = pd.DataFrame(columns=YING_COLUMNS)

    scan_path = OUT_DIR / "ying-exact-value-candidate-scan.tsv"
    scan = read_table(scan_path)
    promoted_path = ROOT / "data/derived/replication_pairs/harvest/promoted/ying_2023_partial_reconstruction__promoted_pairs.csv"
    promoted = read_table(promoted_path)
    promoted_nums: set[int] = set()
    if promoted is not None and "pair_id" in promoted.columns:
        extracted = promoted["pair_id"].astype(str).str.extract(r"ying_2023_pair_(\d+)")[0].dropna()
        promoted_nums = set(extracted.astype(int))

    existing_ids = set(ledger.get("candidate_id", pd.Series(dtype=str)).astype(str))
    existing_pairs = set()
    if "ying_pair" in ledger.columns:
        for value in ledger["ying_pair"]:
            try:
                existing_pairs.add(int(value))
            except Exception:
                pass

    rows = ledger.to_dict("records")

    def ying_abstract_paths(pair: int) -> list[Path]:
        base = ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts"
        return sorted(base.glob(f"{pair:03d}_*.json"))

    def checked_ying_row(
        pair: int,
        slug_text: str,
        status: str,
        decision: str,
        reviewed_question: str,
        relation: str,
        original: str,
        replication: str,
        blocker: str,
        reuse: str,
        next_action: str,
        skip: str = "yes",
        workstream: str = "ying_checked_not_promoted_backfill",
        extra_paths: list[Path] | None = None,
    ) -> dict[str, object]:
        source_paths = [*ying_abstract_paths(pair), *(extra_paths or [])]
        return {
            "reviewed_at": REVIEWED_AT,
            "workstream": workstream,
            "candidate_id": f"ying_2023_pair_{pair:03d}_{slug_text}",
            "ying_pair": pair,
            "status": status,
            "figure1_decision": decision,
            "skip_in_goal3000": skip,
            "reviewed_question": reviewed_question,
            "source_paths": source_paths,
            "relation_evidence": relation,
            "original_value_evidence": original,
            "replication_value_evidence": replication,
            "mismatch_or_blocker": blocker,
            "possible_reuse": reuse,
            "next_action": next_action,
        }

    promoted_manual_rows = [
        {
            "reviewed_at": REVIEWED_AT,
            "workstream": "ying_abstract_value_rescue",
            "candidate_id": "ying_2023_pair_001_expressive_writing_24wk_ppa",
            "ying_pair": 1,
            "status": "promoted",
            "figure1_decision": "promoted_to_current_figure1",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the expressive-writing smoking-cessation pilot and larger trial support a matched 24-week abstinence row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/001_pilot_10_1002_jclp_20208.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/001_full_10_1080_14622200601078525.json",
            ],
            "relation_evidence": (
                "The Ying roster links the 2005 expressive-writing pilot to the 2007 larger young-adult smoking-cessation trial. "
                "The later trial evaluates the same expressive-writing adjunct to brief office intervention plus nicotine patch therapy."
            ),
            "original_value_evidence": (
                "Pilot abstract reports participants randomized to brief office intervention N=30 or expressive writing plus brief office "
                "intervention N=30. It reports biochemically confirmed 30-day point-prevalence abstinence at week 24 of 20% versus 10% "
                "for brief office only versus expressive writing plus brief office."
            ),
            "replication_value_evidence": (
                "Larger-trial abstract reports n=99 brief office intervention and n=97 expressive writing plus brief office intervention. "
                "It reports abstinence rates at 24 weeks of 12% versus 11% for brief office versus expressive writing plus brief office."
            ),
            "mismatch_or_blocker": (
                "Promoted as sensitivity-grade because the later abstract gives rounded percentages rather than exact event counts. "
                "The endpoint and timepoint are matched at 24-week biochemically confirmed abstinence, unlike the held WebQuit/SmartQuit "
                "rows whose available full-scale values are at different follow-up windows."
            ),
            "possible_reuse": "smoking-cessation pilot-to-full-scale clinical replication; rounded-percentage conversion sensitivity",
            "next_action": "Already counted in current Ying reconstruction after this batch; revisit only if full text exposes exact 24-week event counts.",
        },
        {
            "reviewed_at": REVIEWED_AT,
            "workstream": "ying_abstract_value_rescue",
            "candidate_id": "ying_2023_pair_165_arthroplasty_decision_quality",
            "ying_pair": 165,
            "status": "promoted",
            "figure1_decision": "promoted_to_current_figure1",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the arthroplasty patient-decision-aid pilot and larger trial support a matched decision-quality row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/165_pilot_10_1186_1471_2474_15_54.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/165_full_10_1016_j_joca_2015_07_024.json",
            ],
            "relation_evidence": (
                "The Ying roster links the 2014 patient-decision-aid pilot for knee arthroplasty consultation to the "
                "2015 larger RCT of patient decision aids for hip or knee arthroplasty. Both test a PtDA plus surgeon "
                "preference report against usual education/control in osteoarthritis patients considering joint arthroplasty."
            ),
            "original_value_evidence": (
                "Pilot Europe PMC abstract reports 142 patients randomized to PtDA intervention (n=71) or usual education "
                "(n=71), and reports decision quality based on knowledge of 71% versus 47%."
            ),
            "replication_value_evidence": (
                "Larger-trial Europe PMC abstract reports 343 patients randomized to intervention (n=174) or control "
                "(n=169), and reports good decision quality in 56.1% intervention versus 44.5% control."
            ),
            "mismatch_or_blocker": (
                "Promoted as sensitivity-grade because the matched endpoint is decision quality/knowledge, while the "
                "larger trial's primary outcome was wait time and the pilot listed feasibility as main outcomes. No "
                "wait-time D row is promoted from these abstracts."
            ),
            "possible_reuse": "arthroplasty patient-decision-aid replication; secondary decision-quality endpoint sensitivity",
            "next_action": "Already counted in current Ying reconstruction after this batch; revisit only if full texts provide exact counts or a primary wait-time SMD conversion.",
        },
        {
            "reviewed_at": REVIEWED_AT,
            "workstream": "ying_exact_value_pmc_rescue",
            "candidate_id": "ying_2023_pair_101_emdr_refugee_htq",
            "ying_pair": 101,
            "status": "promoted",
            "figure1_decision": "promoted_to_current_figure1",
            "skip_in_goal3000": "yes",
            "reviewed_question": "Can the EMDR refugee pilot and larger RCT support a current Figure 1 HTQ PTSD symptom row?",
            "source_paths": [
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/101_pilot_10_3402_ejpt_v2i0_5881.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/101_full_10_1192_bjp_bp_115_167775.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/emdr_refugee/PMC3402110_pmc_xml.xml",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/emdr_refugee/PMC3402110_paperclip.content.lines",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/emdr_refugee/PMC3402110_paperclip.meta.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/emdr_refugee/sha256sums.txt",
            ],
            "relation_evidence": (
                "The pilot full text states it was conducted in preparation for a randomised trial comparing EMDR and "
                "stabilisation with traumatised refugees. The larger RCT tests EMDR versus stabilisation as usual in "
                "refugees and uses HTQ among its primary PTSD symptom outcomes."
            ),
            "original_value_evidence": (
                "Pilot Table 3 reports completer post-treatment HTQ DSM-IV means 2.54 (SD 0.56) for EMDR (n=5) and "
                "3.04 (SD 0.25) for stabilisation (n=5), converted to Hedges g=1.041429."
            ),
            "replication_value_evidence": (
                "Europe PMC abstract for the larger RCT reports 72 randomized refugees and primary outcome effect sizes "
                "CAPS -0.04 and HTQ 0.20; Figure 1 uses the matched nonnegative HTQ magnitude 0.20."
            ),
            "mismatch_or_blocker": (
                "Promoted as sensitivity-grade because the pilot D uses completer post-treatment arm summaries, while "
                "the larger-trial HTQ D is currently taken from a value-bearing abstract rather than a full-text table."
            ),
            "possible_reuse": "refugee PTSD psychotherapy replication; completer-vs-ITT sensitivity; EMDR/stabilisation clinical replication provenance",
            "next_action": "Already counted in current Figure 1. Revisit only if full larger-trial tables expose a stronger adjusted HTQ conversion.",
        },
    ]

    checked_manual_rows = [
        checked_ying_row(
            5,
            "head_neck_cancer_survival_endpoint_mismatch",
            "hold_endpoint_and_comparator_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the phase II head-and-neck cancer pilot and larger trial support a matched survival row?",
            "Ying links a head-and-neck cancer pilot to a later larger trial in the same treatment area.",
            "Pilot-side abstract/source route reports earlier failure-free or locoregional disease-control outcomes around a 3-year horizon.",
            "Full-scale abstract/source route reports a different survival estimand, including 2-year overall survival context.",
            "The available source evidence does not expose the same endpoint, time horizon, and comparator contrast on both sides. Promoting would mix failure-free/locoregional control with overall survival.",
            "oncology pilot-to-phase-III context; possible survival-metric sensitivity if full tables are acquired",
            "Skip until value-bearing full texts establish a same-endpoint contrast and an accepted D-equivalent conversion.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            27,
            "pediatric_art_zero_event_timepoint_mismatch",
            "hold_zero_event_and_timepoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the pediatric ART pilot and larger trial support an AIDS-free survival row?",
            "Ying links the pilot pediatric antiretroviral therapy trial to a later larger pediatric ART trial.",
            "Pilot abstract/source route has no AIDS/death events at about median 134 weeks, leaving no stable D-equivalent event contrast from the available source text.",
            "Full trial abstract/source route reports AIDS-free survival around 144 weeks in a larger sample.",
            "The checked evidence combines a zero-event pilot side with a different follow-up window. The current Figure 1 rules do not support promoting this as a matched D/N row.",
            "pediatric ART context; possible survival-event sensitivity if exact full-text event counts are acquired",
            "Skip until exact same-timepoint event counts and a zero-cell handling policy are available.",
            "yes_until_exact_counts_and_zero_cell_policy",
        ),
        checked_ying_row(
            42,
            "esophageal_pressure_outcome_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the esophageal-pressure ventilation pilot and larger EPVent trial support a matched row?",
            "Ying links the esophageal-pressure-guided ventilation pilot to a later larger EPVent trial.",
            "Pilot abstract/source route emphasizes oxygenation and physiologic ventilation outcomes.",
            "Full-scale source route reports a composite such as death plus free-from-mechanical-ventilation days rather than the same oxygenation outcome.",
            "The available value evidence is not a matched outcome or scale. Promoting would mix a physiologic oxygenation result with a clinical composite.",
            "critical-care ventilation context; possible endpoint-specific sensitivity if full tables are parsed",
            "Skip until the larger trial exposes the same oxygenation endpoint and a source-backed D/N conversion.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            71,
            "hydromorphone_noninferiority_native_outcome_hold",
            "hold_noninferiority_native_metric_mismatch",
            "hold_native_or_mismatched_not_plot_ready",
            "Can the hydromorphone-assisted treatment pilot and SALOME trial support a matched D/N row?",
            "Ying links hydromorphone-assisted treatment pilot evidence to the larger SALOME injectable-opioid treatment trial.",
            "Pilot-side source route is based on NAOMI-derived retention or treatment-response rates.",
            "Full-scale source route is a SALOME noninferiority comparison with different treatment framing and outcomes.",
            "The checked evidence is a native noninferiority/rate comparison and does not provide the same original target contrast with a current accepted D conversion.",
            "opioid-treatment replication context; native-rate or noninferiority sensitivity project",
            "Skip for current Figure 1 unless an exact same-outcome randomized contrast and conversion route are sourced.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            72,
            "licensed_premises_full_hr_native_hold",
            "hold_native_hazard_metric_and_value_gap",
            "hold_native_or_mismatched_not_plot_ready",
            "Can the licensed-premises intervention pilot and larger evaluation support a matched D/N row?",
            "Ying links a licensed-premises intervention pilot to a later larger alcohol/licensed-premises evaluation.",
            "Pilot-side abstract/source route has broad effect-size language without exact matched source values in the checked artifact.",
            "Full-scale abstract/source route reports hazard-ratio style results rather than a directly matched SMD/D result.",
            "The checked source text lacks exact pilot-side values and the larger result is native HR-scale evidence without an accepted current D conversion.",
            "alcohol/licensed-premises context; native hazard-ratio sensitivity worklist",
            "Skip until full text/data provide exact same-outcome values and an approved HR-to-D route.",
            "yes_until_exact_values_and_metric_policy",
        ),
        checked_ying_row(
            73,
            "polypill_cvd_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the polypill pilot and larger trial support a matched row?",
            "Ying links a polypill pilot to a larger cardiovascular prevention trial.",
            "Pilot-side source route reports surrogate risk-factor outcomes such as blood pressure or LDL.",
            "Full-scale source route reports cardiovascular event or hazard-ratio outcomes.",
            "The checked evidence does not match the same endpoint class. Promoting would mix surrogate BP/LDL effects with downstream CVD event effects.",
            "clinical surrogate-vs-event sensitivity; cardiovascular pilot-to-outcome context",
            "Skip until a same-endpoint source-backed contrast is found.",
        ),
        checked_ying_row(
            78,
            "same_doi_not_larger_replication",
            "reject_same_article_not_replication",
            "reject_not_current_figure1_pair",
            "Can Ying pair 078 be promoted as a pilot/full-scale replication row?",
            "The mirrored Europe PMC records resolve the pilot and full side to the same DOI/article.",
            "The pilot-side and full-side artifacts are the same article route.",
            "The replication-side artifact is not an independent larger follow-up source.",
            "This is not a 1:1 original-vs-larger-replication pair under current Figure 1 rules.",
            "Ying roster data-quality audit; duplicate DOI detection",
            "Do not promote. Keep only as a roster duplicate/quality-control record.",
        ),
        checked_ying_row(
            81,
            "life_falls_rate_ratio_native_hold",
            "hold_native_rate_ratio_no_current_d_route",
            "hold_native_only_not_current_d_equivalent",
            "Can the LiFE falls pilot and larger BMJ trial support a matched D/N row?",
            "Ying links the LiFE falls pilot to the larger LiFE falls trial.",
            "Pilot-side source route reports a falls rate ratio around 0.23 rather than a directly source-backed SMD.",
            "Full-scale source route reports an incidence rate ratio around 0.69 for falls.",
            "The relation and broad endpoint are plausible, but both sides are native falls-rate metrics and the current Figure 1 pipeline lacks an accepted rate-ratio-to-D conversion for this row.",
            "falls-prevention native-rate sensitivity; candidate for future metric policy",
            "Hold as native-only until a defensible D-equivalent conversion policy and exact event/person-time inputs are added.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            96,
            "reproductive_coercion_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the reproductive-coercion pilot and larger trial support a matched row?",
            "Ying links the pilot reproductive coercion intervention to a later larger trial in the same intervention family.",
            "Pilot-side source route emphasizes ending an unsafe relationship.",
            "Full-scale source route reports reproductive coercion, partner violence, resource knowledge, and self-efficacy endpoints.",
            "The checked source evidence does not expose a same endpoint/contrast pair. Promoting would mix relationship-ending behavior with other reproductive-coercion/IPV outcomes.",
            "IPV/reproductive-health intervention context; endpoint-harmonization worklist",
            "Skip until exact same-outcome values are acquired.",
        ),
        checked_ying_row(
            108,
            "bedaquiline_hazard_ratio_native_hold",
            "hold_native_hazard_metric_no_current_d_route",
            "hold_native_only_not_current_d_equivalent",
            "Can the bedaquiline pilot and larger TB trial support a matched D/N row?",
            "Ying links a bedaquiline pilot/source route to a larger tuberculosis treatment trial.",
            "Pilot-side checked values are not available as a same-contrast D/N row from the abstract route.",
            "Full-scale source route reports time-to-event or hazard-ratio style evidence.",
            "The available evidence is native survival/time-to-event evidence and lacks a current accepted D conversion plus same-contrast original values.",
            "TB treatment replication context; survival/native-metric sensitivity worklist",
            "Hold until exact event/time-to-event inputs and an accepted HR-to-D conversion policy are available.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            109,
            "terminal_cancer_cbt_intervention_subgroup_mismatch",
            "hold_intervention_and_subgroup_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the CBT terminal-cancer pilot and larger intervention trial support a matched row?",
            "Ying links a CBT pilot in terminal cancer to a later larger psychological-intervention trial.",
            "Pilot-side source route concerns individual CBT.",
            "Full-scale source route concerns an app/education intervention, with overall null evidence and a severe-subgroup signal rather than the same population-wide contrast.",
            "The intervention delivery, comparator framing, and subgroup/overall contrast do not match closely enough for a 1:1 Figure 1 row.",
            "psycho-oncology intervention context; subgroup-sensitivity caution example",
            "Skip unless full texts identify a same intervention, endpoint, and population contrast.",
        ),
        checked_ying_row(
            120,
            "smoke_free_home_endpoint_population_mismatch",
            "hold_endpoint_population_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the smoke-free homes pilot and larger Bangladesh trial support a matched row?",
            "Ying links a smoke-free homes pilot to a larger household-air-pollution/smoke-free intervention trial.",
            "Pilot-side source route reports follow-up log cotinine or tobacco-smoke exposure biomarker evidence.",
            "Full-scale source route reports 12-month PM2.5 or household-air-quality evidence in a Bangladesh context.",
            "The checked evidence differs in endpoint, measurement scale, follow-up context, and population, so it is not a matched D/N row.",
            "smoke-free home intervention context; exposure-endpoint harmonization worklist",
            "Skip until same biomarker or same air-quality endpoint values are available.",
        ),
        checked_ying_row(
            121,
            "glyceryl_trinitrate_stroke_timepoint_outcome_mismatch",
            "hold_timepoint_and_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the GTN stroke pilot and larger ENOS-style trial support a matched row?",
            "Ying links a glyceryl trinitrate acute-stroke pilot to a larger stroke trial.",
            "Pilot-side source route includes early blood-pressure evidence around 2 hours plus mRS/death context.",
            "Full-scale source route reports longer-horizon functional outcome such as 90-day mRS.",
            "The checked evidence mixes early physiologic response with later clinical functional outcome and does not expose a same-timepoint D/N row.",
            "stroke treatment context; early-physiology versus functional-outcome sensitivity",
            "Skip until same endpoint/timepoint values are source-backed.",
        ),
        checked_ying_row(
            125,
            "ms_exercise_process_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the MS exercise pilot and larger trial support a matched activity row?",
            "Ying links an MS exercise pilot/process evaluation to a later larger exercise trial.",
            "Pilot-side source route emphasizes feasibility/process/progression evidence rather than a clean matched outcome value.",
            "Full-scale source route reports GLTEQ or activity-scale outcomes.",
            "The checked artifacts do not expose the same outcome and contrast as source-backed D/N values.",
            "MS exercise intervention context; activity-endpoint extraction worklist",
            "Skip until full text gives exact matched outcome values on both sides.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            127,
            "prostate_bone_metastases_relative_change_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the prostate bone-metastases exercise pilot and larger trial support a matched row?",
            "Ying links a prostate cancer bone-metastases pilot to a later larger exercise trial.",
            "Pilot-side abstract/source route reports relative changes without enough CI/SD/count detail for a clean D conversion.",
            "Full-scale source route reports mean-difference/CI style evidence.",
            "The checked abstract-level source evidence is insufficient to reconstruct a same-outcome D/N row without full text tables or data.",
            "oncology exercise context; manual full-text acquisition target",
            "Hold until full texts provide exact means/SDs, CIs, or event counts for a same outcome.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            133,
            "patient_navigation_timepoint_endpoint_mismatch",
            "hold_timepoint_and_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the patient-navigation pilot and larger trial support a matched row?",
            "Ying links a patient-navigation pilot to a later larger patient-navigation trial.",
            "Pilot-side source route reports treatment engagement at about 3 months.",
            "Full-scale source route reports biochemically confirmed abstinence at about 12 months.",
            "This is the exact failure mode we need to avoid: a real pilot/full-scale relation but mismatched outcome and follow-up window.",
            "smoking/patient-navigation context; endpoint-timepoint mismatch example",
            "Skip unless a same endpoint and same follow-up window can be found in full text.",
        ),
        checked_ying_row(
            138,
            "teen_cancer_acp_native_congruence_hold",
            "hold_native_or_model_metric_not_current_d_route",
            "hold_native_only_not_current_d_equivalent",
            "Can the adolescent cancer advance-care-planning pilot and larger trial support a matched row?",
            "Ying links the teen cancer ACP pilot to a later larger ACP trial.",
            "Pilot-side source route involves congruence/latent-class or odds-style evidence rather than a clean SMD/D from abstract values.",
            "Full-scale source route reports ACP-related outcomes with model-based/native estimates.",
            "The checked evidence does not provide a same native-to-D conversion route or matched endpoint values at the current evidence standard.",
            "advance-care-planning native-metric sensitivity; possible full-text table extraction",
            "Hold until exact same-outcome counts or model outputs can be converted defensibly.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            147,
            "sahara_risk_score_not_treatment_effect",
            "hold_not_same_treatment_effect",
            "hold_not_promoted_current_figure1",
            "Can the SAHARA pilot and larger digital intervention trial support a matched row?",
            "Ying links SAHARA-related pilot/development work to a later larger digital intervention study.",
            "Pilot-side checked artifact centers on a risk score or feasibility/development signal rather than the later treatment effect.",
            "Full-scale source route reports a digital-intervention myocardial infarction or risk-score endpoint.",
            "The available original-side evidence is not a source-backed original treatment effect matching the larger trial result.",
            "digital cardiac intervention context; risk-score validation vs intervention distinction",
            "Skip unless the pilot exposes a same treatment contrast and value-bearing D/N inputs.",
        ),
        checked_ying_row(
            148,
            "parkinson_ot_abstract_no_numeric_effect",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the Parkinson occupational-therapy pilot and larger trial support a matched row?",
            "Ying links a Parkinson occupational-therapy pilot to a larger occupational-therapy RCT.",
            "Pilot abstract/source route reports negligible-to-small effects but does not give exact numeric effect and N/effect extraction for the matched contrast.",
            "Full-scale source route is a larger OT trial with relevant outcomes, but the matched pilot effect is not source-backed from the checked abstract.",
            "The replication relation is plausible, but the original-side value evidence is insufficient at abstract level.",
            "Parkinson OT context; manual full-text value extraction target",
            "Hold until pilot full text/data provide exact same-outcome effect/N values.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            156,
            "vitiligo_endpoint_control_mismatch",
            "hold_endpoint_and_control_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the vitiligo pilot and larger trial support a matched row?",
            "Ying links a vitiligo pilot to a larger vitiligo trial.",
            "Pilot-side source route uses a different endpoint/control framing from the larger trial.",
            "Full-scale source route reports larger-trial vitiligo outcomes under a different control or endpoint structure.",
            "The checked pair does not preserve the same outcome and comparator contrast, so it is not a safe 1:1 row.",
            "vitiligo clinical-trial context; endpoint/control harmonization worklist",
            "Skip until full texts identify a same endpoint/control contrast.",
        ),
        checked_ying_row(
            163,
            "lumbopelvic_feedback_design_arm_n_gap",
            "hold_design_mismatch_and_arm_n_gap",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the lumbopelvic feedback pilot and larger trial support a matched row?",
            "Ying links a movement-feedback pilot to a later larger low-back-pain/lumbopelvic feedback trial.",
            "Pilot-side source route gives a constant-feedback versus control effect around d=0.60 but checked abstract data do not preserve the exact arm Ns for that contrast.",
            "Full-scale source route is a cluster/sham trial with mean-difference/CI evidence around N=130.",
            "The available evidence has intervention/design differences plus an arm-N gap, so a plotted row would be under-specified.",
            "low-back-pain feedback intervention context; full-text extraction target",
            "Hold until exact arm Ns and a same intervention/control contrast are source-backed.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            174,
            "bullying_aggression_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the bullying/aggression pilot and larger trial support a matched row?",
            "Ying links an anti-bullying/aggression intervention pilot to a later larger school-based trial.",
            "Pilot-side source route appears to be an HTA/feasibility source without exact matched D/N values in the checked abstract route.",
            "Full-scale source route reports larger Good Behaviour Game or bullying/aggression outcomes.",
            "The checked evidence did not yield an exact same outcome, contrast, and D/N value pair from source text.",
            "school aggression/bullying context; full-text table extraction target",
            "Hold until exact matched values are acquired from full text, supplement, or data.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            199,
            "ecouch_multiple_outcomes_ambiguous_fanout",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can the e-couch pilot and larger implementation trial support a single matched row?",
            "Ying links e-couch pilot evidence to a later larger depression/anxiety implementation trial.",
            "Pilot-side source route reports ranges of d values across multiple outcomes and timepoints.",
            "Full-scale source route reports multiple arms/outcomes/timepoints rather than one explicitly matched original target.",
            "The row grain is ambiguous and would create one-to-many outcome/timepoint fanout without an explicit canonical result.",
            "internet mental-health intervention context; possible multi-outcome sensitivity appendix",
            "Do not promote without an explicit same-outcome/timepoint selector.",
        ),
        checked_ying_row(
            200,
            "social_status_eating_population_interaction_mismatch",
            "hold_population_model_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the social-status eating pilot and larger adolescent trial support a matched row?",
            "Ying links a social-status/eating pilot to a later larger adolescent eating study.",
            "Pilot-side source route is a crossover young-adult social-status eating design.",
            "Full-scale source route reports an adolescent sample with sex-interaction/model-based evidence.",
            "The population and statistical contrast do not match the original-side pilot effect closely enough for a 1:1 D/N row.",
            "eating/social-status context; model-contrast mismatch example",
            "Skip unless a same population and same model contrast can be sourced.",
        ),
        checked_ying_row(
            202,
            "mrsa_native_duration_composite_mismatch",
            "hold_native_metric_and_endpoint_mismatch",
            "hold_native_or_mismatched_not_plot_ready",
            "Can the MRSA treatment pilot and larger trial support a matched row?",
            "Ying links an MRSA pilot to a later larger MRSA trial.",
            "Pilot-side source route reports duration or negative-binomial time-ratio style evidence.",
            "Full-scale source route reports composite or persistent-bacteremia outcomes.",
            "The checked values are native/model metrics and mismatched endpoints, not a same-outcome D/N pair.",
            "MRSA clinical-trial context; native-metric and endpoint-harmonization worklist",
            "Skip until same-endpoint values and a defensible conversion route are available.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            211,
            "primum_feasibility_vs_mai_score",
            "hold_feasibility_original_no_matched_effect",
            "hold_not_promoted_current_figure1",
            "Can the PRIMUM pilot and larger trial support a matched MAI score row?",
            "Ying links the PRIMUM pilot to a later larger PRIMUM medication-safety trial.",
            "Pilot-side source route says outcomes were unfeasible or missing rather than reporting a source-backed same-outcome effect.",
            "Full-scale source route reports MAI score evidence.",
            "The original-side artifact does not provide the same value-bearing outcome as the larger trial.",
            "medication-safety intervention context; feasibility-to-effect caution example",
            "Skip unless pilot full text/data expose exact same MAI-style values.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            212,
            "vbi_pedometer_timepoint_mismatch",
            "hold_timepoint_mismatch_despite_numeric_values",
            "hold_not_promoted_current_figure1",
            "Can the VBI pedometer pilot and larger Step It Up trial support a matched accelerometry row?",
            "Ying links the four-arm VBI primary-care pilot to the larger two-arm Step It Up pedometer RCT.",
            "Pilot abstract reports total N=394, Pedometer n=74 and Health Check control n=157; primary accelerometer effect at 4 weeks is +23.5 cpm, 95% CI -51.3 to +98.3.",
            "Full trial abstract reports intervention n=505 and control n=502; primary accelerometer activity volume at 3 months is 8.8 cpm, 95% CI -18.7 to 36.3.",
            "The values are tempting and source-backed, but the follow-up windows are not matched: 4 weeks in the pilot versus 3 months in the larger trial.",
            "physical-activity VBI context; timepoint-mismatch sensitivity if policy later allows nearest follow-up",
            "Do not promote under the current same-timepoint standard. Revisit only if same-window larger-trial values are found or policy changes.",
        ),
        checked_ying_row(
            213,
            "nimodipine_pilot_counts_missing",
            "hold_needs_full_text_original_counts",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the nimodipine vestibular schwannoma pilot and larger trial support a matched row?",
            "Ying links a nimodipine pilot/source route to a later larger vestibular-schwannoma treatment trial.",
            "Pilot abstract/source route reports significant p-values for hearing or facial nerve preservation, but the checked abstract does not provide event counts or effect-size inputs for the matched outcome.",
            "Full-scale source route has larger-trial event/outcome evidence, but cannot be paired safely without source-backed pilot counts.",
            "The replication relation is real enough to retain, but original-side value evidence is missing at the required level.",
            "vestibular schwannoma/nimodipine clinical context; manual full-text extraction target",
            "Hold until pilot full text or supplement provides exact matched counts/effect inputs.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            218,
            "smarter_weight_loss_timepoint_arm_gap",
            "hold_timepoint_and_arm_detail_gap",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the SMARTER pilot and larger trial support a matched weight-loss row?",
            "Ying links the SMARTER pilot to a later larger weight-loss self-monitoring trial.",
            "Pilot-side source route reports 12-week three-group weight-loss percentages without enough per-arm count/detail from the checked abstract.",
            "Full-scale source route reports a 6-month SM+FB versus SM comparison.",
            "The checked evidence has a timepoint mismatch and incomplete arm-specific original values for the exact larger-trial contrast.",
            "weight-loss self-monitoring context; manual full-text extraction and endpoint-selector worklist",
            "Hold until exact same-arm, same-timepoint values are source-backed.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            225,
            "naltrexone_hiv_outcome_population_mismatch",
            "hold_endpoint_population_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the naltrexone/HIV pilot and larger trial support a matched row?",
            "Ying links a naltrexone/HIV pilot to a later larger trial.",
            "Pilot-side source route mixes OUD/AUD initiation or retention outcomes.",
            "Full-scale source route emphasizes OUD viral suppression or opioid-use outcomes.",
            "The checked evidence does not preserve the same population/substance-use subgroup and endpoint contrast.",
            "HIV/OUD pharmacotherapy context; endpoint/population harmonization worklist",
            "Skip until a same endpoint and same population contrast is sourced.",
        ),
        checked_ying_row(
            232,
            "melanoma_genomic_risk_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the melanoma genomic-risk pilot and larger trial support a matched row?",
            "Ying links melanoma genomic-risk feedback pilot evidence to a later larger trial.",
            "Pilot-side source route reports confidence identifying melanoma.",
            "Full-scale source route reports sunburn, skin-exam, or sun-protection behavior endpoints.",
            "The checked evidence does not match the same outcome/construct.",
            "melanoma genomic-risk context; endpoint-selection worklist",
            "Skip until same endpoint values are source-backed.",
        ),
        checked_ying_row(
            235,
            "mhealth_hiv_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the mHealth HIV pilot and larger trial support a matched row?",
            "Ying links an mHealth HIV pilot to a later larger mobile-health intervention trial.",
            "Pilot-side source route reports adherence or quality-of-life outcomes.",
            "Full-scale source route reports depression symptoms.",
            "The checked artifacts do not expose the same endpoint, so no 1:1 row is promoted.",
            "mHealth HIV context; endpoint harmonization",
            "Skip until same endpoint values are found.",
        ),
        checked_ying_row(
            237,
            "botox_rehab_between_group_value_gap",
            "hold_no_original_between_group_value",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the botulinum-toxin rehabilitation pilot and larger stroke trial support a matched row?",
            "Ying links a botox/rehabilitation pilot to a later larger stroke rehabilitation trial.",
            "Pilot-side checked abstract route does not provide a clean between-group numeric value for the matched outcome.",
            "Full-scale source route reports mean-difference style values.",
            "Original-side between-group effect evidence is missing at the current standard.",
            "stroke rehabilitation context; manual full-text extraction target",
            "Hold until pilot full text gives exact matched between-group values.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            238,
            "pharm_chf_feasibility_vs_adherence_qol",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the PHARM-CHF pilot and larger trial support a matched row?",
            "Ying links the PHARM-CHF pilot to the larger PHARM-CHF trial.",
            "Pilot-side source route is feasibility-focused and may report only a systolic-BP indicator without a usable numeric matched effect.",
            "Full-scale source route reports medication adherence or quality-of-life outcomes.",
            "The checked original-side endpoint is not a matched value-bearing effect for the larger trial outcome.",
            "heart-failure pharmacy intervention context; full-text extraction target",
            "Skip until exact same outcome values are sourced.",
        ),
        checked_ying_row(
            239,
            "engager_feasibility_vs_core_om",
            "hold_feasibility_original_no_matched_effect",
            "hold_not_promoted_current_figure1",
            "Can the ENGAGER pilot and larger trial support a matched CORE-OM row?",
            "Ying links the ENGAGER pilot to a later larger trial.",
            "Pilot-side source route emphasizes retention/feasibility rather than a clean matched clinical effect.",
            "Full-scale source route reports CORE-OM or mental-health outcome evidence.",
            "The original-side checked artifact does not provide a same outcome/effect value.",
            "ENGAGER mental-health intervention context; full-text extraction target",
            "Skip until exact same outcome values are acquired.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            240,
            "hiit_mvpa_timepoint_mismatch",
            "hold_timepoint_mismatch_despite_effect_text",
            "hold_not_promoted_current_figure1",
            "Can the HIIT pilot and larger trial support a matched MVPA row?",
            "Ying links an HIIT physical-activity pilot to a larger intervention trial.",
            "Pilot-side source route reports a 24-week MVPA effect around d=1.52.",
            "Full-scale source route reports 12-month MVPA evidence.",
            "The available values are not at the same follow-up timepoint, and the checked context/direction is not sufficient to override the same-timepoint rule.",
            "HIIT physical-activity context; timepoint sensitivity if policy changes",
            "Do not promote under current same-timepoint standard.",
        ),
        checked_ying_row(
            242,
            "internet_ptsd_active_comparator_mismatch",
            "hold_active_comparator_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the internet PTSD pilot and larger noninferiority trial support a matched row?",
            "Ying links a guided internet PTSD pilot to a later larger guided internet CBT-TF trial.",
            "Pilot-side source route compares guided self-help/internet treatment against delayed or waitlist control with a large Cohen's d.",
            "Full-scale source route is a noninferiority comparison of guided internet CBT-TF versus face-to-face CBT-TF.",
            "The larger trial does not replicate the original waitlist/delayed-control contrast; it uses an active comparator noninferiority design.",
            "PTSD internet-therapy context; active-comparator sensitivity",
            "Skip unless a same waitlist/control contrast is source-backed in the larger trial.",
        ),
    ]

    additional_checked_manual_rows = [
        checked_ying_row(
            105,
            "interact_bp_hematoma_vs_rankin_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the INTERACT pilot and larger INTERACT2 trial support a matched blood-pressure row?",
            "Ying links the INTERACT acute intracerebral haemorrhage blood-pressure pilot to the larger INTERACT2 trial.",
            "Pilot abstract reports N=203 intensive BP lowering and N=201 standard BP management, with primary efficacy endpoint proportional change in haematoma volume at 24 h and safety/clinical outcomes to 90 days.",
            "Larger-trial abstract reports N=2,839 and primary outcome death or major disability on modified Rankin scale at 90 days.",
            "The available value-bearing abstracts point to different primary endpoints: haematoma-volume change in the pilot versus death/major disability or ordinal mRS in the larger trial.",
            "ICH intensive-BP clinical context; possible endpoint-specific source-result extraction if full tables are parsed",
            "Hold until the same endpoint and timepoint values are source-backed on both sides.",
        ),
        checked_ying_row(
            2,
            "uk_harp_ldl_surrogate_vs_sharp_events",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can UK-HARP-II and SHARP support a matched ezetimibe/simvastatin row?",
            "Ying links the UK-HARP-II biochemical pilot to the larger SHARP CKD trial.",
            "Pilot abstract reports N=203 and biochemical LDL-cholesterol changes after adding ezetimibe to simvastatin.",
            "Full SHARP abstract reports N=9,270 and major atherosclerotic events for simvastatin plus ezetimibe versus placebo.",
            "The pilot source is a surrogate LDL/tolerability study, while the larger trial source is an event-outcome trial with a different comparator framing.",
            "CKD lipid-treatment surrogate-to-events context",
            "Skip until a same-endpoint contrast is sourced; do not convert LDL lowering into cardiovascular-event replication.",
        ),
        checked_ying_row(
            61,
            "dexmedetomidine_noninferiority_two_trial_native_hold",
            "hold_noninferiority_native_metric_mismatch",
            "hold_native_or_mismatched_not_plot_ready",
            "Can the dexmedetomidine pilot and MIDEX/PRODEX phase 3 trials support a matched sedation row?",
            "Ying links the small dexmedetomidine versus standard-care sedation trial to the larger MIDEX and PRODEX trials.",
            "Pilot abstract reports N=41 dexmedetomidine and N=44 standard care, target RASS percentages, ICU stay, and noninferiority not confirmed.",
            "Full abstract reports two separate randomized trials comparing dexmedetomidine with midazolam and propofol, with sedation, ventilation, and interaction outcomes.",
            "The larger source combines two comparator-specific trials and noninferiority/native sedation metrics; the checked abstract route does not identify one exact original contrast and one exact larger-trial contrast.",
            "ICU sedation replication context; comparator-specific noninferiority sensitivity",
            "Hold until one comparator-specific full trial and same native endpoint can be converted under an accepted policy.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            197,
            "airways_feasibility_three_arm_vs_two_arm_functional_outcome",
            "hold_design_mismatch_and_arm_n_gap",
            "hold_not_promoted_current_figure1",
            "Can the OHCA supraglottic-airway feasibility trial and AIRWAYS-2 support a matched row?",
            "Ying links the AIRWAYS feasibility study to the larger AIRWAYS-2 randomized trial.",
            "Pilot abstract reports a cluster feasibility trial comparing i-gel, laryngeal mask airway supreme, and current practice, with feasibility as the primary outcome.",
            "Full AIRWAYS-2 abstract reports a two-strategy SGA versus tracheal-intubation comparison with functional outcome.",
            "The checked evidence changes both row grain and endpoint: three-arm feasibility/device comparison versus two-arm clinical functional-outcome strategy trial.",
            "OHCA airway-management context; design-transition example",
            "Skip unless source texts identify a same device/strategy contrast and same clinical endpoint.",
        ),
        checked_ying_row(
            129,
            "motor_cognitive_training_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the motor-cognitive training pilot and larger trial support a dual-task gait row?",
            "Ying links the assisted-living motor-cognition pilot to the larger strength-balance plus cognitive-training trial.",
            "Pilot abstract reports N=16, motor versus motor-cognition groups, with secondary dual-task gait outcomes but no exact matched effect values in the checked abstract.",
            "Full abstract reports N=182 and multiple dual-task gait, divided-attention, and physical/cognitive outcomes.",
            "The relation and broad outcome family are plausible, but the checked abstracts expose a multi-outcome surface without exact same-outcome values.",
            "aging motor-cognitive training context; full-text table extraction target",
            "Hold until exact same dual-task gait or divided-attention values and arm Ns are extracted.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            152,
            "trust_tibial_fracture_feasibility_vs_function",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the TRUST pilot and definitive tibial-fracture trial support a matched LIPUS row?",
            "Ying links the TRUST pilot to the definitive TRUST randomized clinical trial.",
            "Pilot abstract reports N=51 and states the goals were recruitment, protocol adherence, follow-up, and data-collection feasibility.",
            "Full abstract reports N=501 and tests functional recovery and radiographic healing after tibial fracture.",
            "The pilot abstract is explicitly feasibility-focused and does not provide the same value-bearing treatment outcome as the definitive trial.",
            "orthopedic LIPUS trial context; feasibility-to-efficacy caution",
            "Hold until pilot full text exposes a same functional or radiographic outcome value.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            172,
            "parity_antibiotics_feasibility_vs_surgical_infection",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the PARITY pilot and larger antibiotic-regimen trial support a matched infection row?",
            "Ying links the PARITY pilot RCT to the larger PARITY randomized trial after endoprosthetic reconstruction.",
            "Pilot abstract reports feasibility outcomes including enrolment, follow-up, and protocol deviations.",
            "Full abstract reports 1-year surgical site infection after 5-day versus 1-day postoperative antibiotics.",
            "The pilot abstract does not expose the same infection endpoint values as the larger trial.",
            "orthopedic oncology antibiotic-regimen context; full-text extraction target",
            "Hold until pilot full text provides exact same infection-outcome values.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            31,
            "lt_patch_travellers_diarrhoea_full_text_counts_needed",
            "hold_needs_full_text_original_counts",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the LT patch phase II and phase III traveller-diarrhoea trials support a matched ETEC row?",
            "Ying links the phase II heat-labile-toxin patch traveller-diarrhoea field trial to the phase III patch vaccine field trial.",
            "Pilot abstract reports N=59 LT patch and N=111 placebo among analysed participants and gives placebo event counts and vaccine efficacy, but the checked abstract route does not expose LT-patch event counts for the exact phase III endpoint.",
            "Full abstract reports N=821 LT patch and N=823 placebo with moderate/severe ETEC diarrhoea 30 versus 46 and vaccine efficacy 34.6%.",
            "The larger-trial endpoint is value-bearing, but the pilot-side exact event counts for the same endpoint are missing from the abstract route.",
            "traveller-diarrhoea vaccine phase II/III context; likely high-value manual full-text target",
            "Hold until full text/supplement provides exact pilot event counts for the same ETEC diarrhoea endpoint.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            87,
            "barrett_screening_participation_denominator_gap",
            "hold_timepoint_and_arm_detail_gap",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the Barrett screening pilot and larger community trial support a matched participation row?",
            "Ying links a Barrett esophagus screening pilot to a larger community comparative-effectiveness trial of screening techniques.",
            "Pilot abstract reports recruiting 20 per procedure arm and an overall participation probability of 38% with several screening modalities.",
            "Full abstract reports N=459 invited and N=209 participating across muTNE, huTNE, and sEGD arms.",
            "The checked abstracts do not preserve the exact same arm-level invitation denominators and the pilot includes VCE while the larger trial compares different endoscopy settings.",
            "Barrett screening participation context; arm-denominator extraction target",
            "Hold until arm-specific invitation and participation counts can be matched across the same modalities.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            122,
            "patient_advocates_asthma_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the asthma patient-advocate pilot and larger RCT support a matched asthma-outcome row?",
            "Ying links a patient-advocate pilot for low-income adults with asthma to a larger patient-advocate RCT.",
            "Pilot abstract reports PA versus minimal-intervention comparison and feasibility/preliminary effectiveness, but the checked abstract route does not expose exact matched outcome values.",
            "Full abstract reports a 6-month PA intervention versus usual care and multiple asthma outcomes.",
            "The source relation is plausible, but exact same-outcome effect/N values are not present in the abstract-level evidence.",
            "asthma patient-advocate clinical context; full-text extraction target",
            "Hold until same asthma outcome values and arm Ns are source-backed.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            220,
            "naltrexone_hiv_pilot_feasibility_vs_drinking_outcomes",
            "hold_feasibility_original_no_matched_effect",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the oral naltrexone in women with HIV pilot and RCT support a matched drinking-outcome row?",
            "Ying links the naltrexone feasibility pilot to the larger oral naltrexone versus placebo RCT in women living with HIV.",
            "Pilot abstract emphasizes acceptability, feasibility, design challenges, and pilot study methods for hazardous drinking.",
            "Full abstract reports N=96 naltrexone and N=98 placebo with drinking-reduction and HIV clinical outcomes.",
            "The checked abstract route does not expose exact pilot treatment-effect values for the same outcome as the larger RCT.",
            "HIV/unhealthy-alcohol-use pharmacotherapy context; full-text extraction target",
            "Hold until pilot value tables provide a same drinking endpoint and an accepted D conversion.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            54,
            "face_advance_care_acceptability_native_hold",
            "hold_native_or_model_metric_not_current_d_route",
            "hold_native_or_mismatched_not_plot_ready",
            "Can FACE advance-care-planning pilot and larger trial support a matched acceptability row?",
            "Ying links the FACE adolescent HIV pilot to the larger randomized trial of family-centered advance care planning.",
            "Pilot abstract reports N=38 dyads and feasibility, acceptability, and safety of a three-session intervention.",
            "Full abstract reports a fully powered RCT and acceptability/feasibility/worthwhile outcomes.",
            "The checked values are acceptability/feasibility constructs, not an exposed same treatment-effect D/N row from the abstract route.",
            "pediatric advance-care-planning context; possible acceptability-methods reuse",
            "Hold unless full text yields exact comparable randomized outcome values and a conversion policy.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            98,
            "protect_rolofylline_dose_finding_vs_phase3_native_hold",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can PROTECT rolofylline pilot and phase 3 trial support a matched acute-heart-failure row?",
            "Ying links the PROTECT dose-finding pilot to the larger rolofylline phase 3 trial.",
            "Pilot abstract reports N=301 across placebo and three rolofylline dose arms, intended to identify dose and refine endpoints.",
            "Full abstract reports a larger placebo-controlled rolofylline trial with dyspnea, renal-function, and clinical-course outcomes.",
            "The original source has multiple dose arms and endpoint refinement, while the checked route lacks an explicit one original dose/outcome matched to one phase 3 endpoint.",
            "acute-heart-failure dose-finding context; dose-specific source-result extraction target",
            "Hold until a prespecified dose/outcome mapping and exact values are sourced.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            37,
            "aspree_feasibility_vs_disability_free_survival",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the ASPREE pilot and full ASPREE trial support a matched aspirin row?",
            "Ying links the ASPREE feasibility pilot to the larger ASPREE trial.",
            "Pilot abstract reports feasibility of a primary prevention trial over 12 months.",
            "Full abstract reports disability-free survival, death, dementia, or persistent physical disability over years of follow-up.",
            "The pilot abstract is feasibility-focused and does not contain the full trial's clinical endpoint values.",
            "ASPREE trial-development context",
            "Skip unless a same clinical endpoint from the pilot is found in full text.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            234,
            "idebenone_dmd_pef_full_text_needed",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the idebenone DMD pilot and DELOS phase 3 trial support a matched respiratory-function row?",
            "Ying links the 12-month idebenone randomized trial to the larger DELOS phase 3 trial in Duchenne muscular dystrophy.",
            "Pilot abstract route reports idebenone results but the checked abstract does not expose exact same respiratory-function effect inputs.",
            "Full DELOS abstract reports idebenone efficacy on respiratory function in a larger placebo-controlled phase 3 trial.",
            "This is a plausible high-value clinical pair, but the checked abstract evidence is insufficient for exact matched D/N extraction.",
            "Duchenne muscular dystrophy respiratory-function context; high-priority full-text table extraction target",
            "Hold until exact pilot and full respiratory-function values are extracted from full text or supplements.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            149,
            "hip_attack_feasibility_vs_mortality_complications",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can HIP ATTACK pilot and full trial support a matched accelerated-surgery row?",
            "Ying links the HIP ATTACK pilot to the full international HIP ATTACK trial.",
            "Pilot abstract reports accelerated versus standard care with feasibility outcomes such as recruitment and care timing.",
            "Full abstract reports accelerated surgery versus standard care with mortality and major complications.",
            "The pilot abstract does not expose the same clinical endpoint values used in the definitive trial.",
            "hip-fracture accelerated-surgery context",
            "Hold until pilot full text exposes exact mortality/complication or same clinical endpoint values.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            164,
            "stroke_oxygen_protocol_not_source_result",
            "hold_protocol_or_registration_no_final_replication_values",
            "hold_not_promoted_current_figure1",
            "Can the SO2S protocol route support a matched oxygen-treatment row?",
            "Ying links a Stroke Oxygen Study protocol/source route to the final larger oxygen-supplementation RCT.",
            "The pilot-side checked artifact is a study protocol that mentions prior pilot evidence rather than the value-bearing pilot trial report itself.",
            "Full abstract reports death and disability at 90 days in the large Stroke Oxygen Study.",
            "A protocol that references earlier pilot results is not enough source evidence for original D/N extraction.",
            "stroke oxygen trial-development context; source acquisition task",
            "Hold until the actual pilot result source and exact values are mirrored.",
            "yes_until_original_source_object_acquired",
        ),
        checked_ying_row(
            208,
            "gapp_pelvic_pain_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can GaPP1 pilot and GaPP2 full trial support a matched chronic-pelvic-pain row?",
            "Ying links the GaPP1 pilot randomized trial to the larger GaPP2 multicentre trial.",
            "Pilot abstract reports gabapentin versus placebo/matched management for chronic pelvic pain and names potential effectiveness as a secondary objective.",
            "Full abstract reports a multicentre placebo-controlled trial with chronic pelvic pain outcomes.",
            "The checked abstracts do not expose exact same pain-outcome values on both sides.",
            "chronic pelvic pain gabapentin context; full-text extraction target",
            "Hold until exact same pain outcome values and arm Ns are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            30,
            "eccentric_exercise_design_mismatch",
            "hold_design_mismatch_and_arm_n_gap",
            "hold_not_promoted_current_figure1",
            "Can the eccentric-endurance pilot and later downhill-hiking study support a matched row?",
            "Ying links an eccentric endurance exercise pilot to a larger downhill-hiking controlled study.",
            "Pilot abstract reports N=45 in a randomized crossover upward/downward hiking design.",
            "Full abstract reports N=127 with an active downhill group and comparison structure over two months.",
            "The intervention family overlaps, but the design, controls, and extracted endpoints do not define a clean 1:1 randomized replication row.",
            "exercise/metabolic-risk context; design-transition example",
            "Skip unless a source-backed same contrast and endpoint are identified.",
        ),
        checked_ying_row(
            244,
            "reset_it_insulin_selector_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the intermittent-insulin pilot and RESET-IT main trial support a matched beta-cell-function row?",
            "Ying links a 24-person intermittent intensive-insulin maintenance trial to the 108-person RESET-IT main trial.",
            "Pilot abstract reports induction intensive insulin therapy followed by intermittent IIT versus daily metformin, with serial ISSI-2 beta-cell function outcomes.",
            "Full abstract reports induction IIT followed by metformin with or without periodic IIT and ISSI-2 outcomes.",
            "The same broad beta-cell-function construct is present, but exact matched values and the arm/maintenance-therapy selector are not established from the abstract route.",
            "type 2 diabetes beta-cell-function context; full-text extraction target",
            "Hold until exact ISSI-2 values and a defensible arm-selector mapping are sourced.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            26,
            "xylitol_tolerability_vs_otitis_media_endpoint",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the xylitol tolerability pilot and larger AOM prevention trial support a matched row?",
            "Ying links a xylitol tolerability pilot to a larger xylitol syrup acute-otitis-media prevention trial.",
            "Pilot abstract reports tolerability/acceptance implications in young children.",
            "Full abstract reports prevention of acute otitis media.",
            "The checked evidence moves from tolerability to clinical disease prevention; no same value-bearing endpoint is exposed.",
            "pediatric xylitol context; tolerability-to-efficacy caution",
            "Skip unless same AOM prevention values are found in the pilot source.",
        ),
        checked_ying_row(
            41,
            "tardis_triple_antiplatelet_feasibility_vs_events",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the triple-antiplatelet pilot and TARDIS trial support a matched stroke row?",
            "Ying links the phase II triple-antiplatelet pilot to the larger TARDIS trial.",
            "Pilot abstract reports tolerability to randomized treatment as the primary outcome and halted recruitment.",
            "Full abstract reports efficacy and safety event outcomes in acute cerebral ischaemia.",
            "The pilot value-bearing endpoint is tolerability/feasibility, not the same recurrent-event or bleeding endpoint as the larger trial.",
            "stroke antiplatelet trial-development context",
            "Hold until same clinical event values are sourced from the pilot.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            47,
            "pd_ot_vs_pt_ot_intervention_mismatch",
            "hold_intervention_and_subgroup_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the Parkinson occupational-therapy pilot and PD REHAB trial support a matched therapy row?",
            "Ying links the PD OT pilot to the larger PD REHAB trial.",
            "Pilot abstract tests immediate occupational therapy versus delayed occupational therapy/no immediate treatment.",
            "Full abstract tests individualized physiotherapy and occupational therapy versus no therapy in mild to moderate Parkinson disease.",
            "The larger intervention adds physiotherapy and uses a broader pragmatic therapy package, so it is not the same original OT contrast.",
            "Parkinson rehabilitation context; intervention-composition mismatch",
            "Skip unless a same OT-only contrast is source-backed.",
        ),
        checked_ying_row(
            4,
            "life_p_physical_performance_vs_mobility_disability",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can LIFE-P and LIFE support a matched physical-activity row?",
            "Ying links the LIFE-P pilot to the larger LIFE physical-activity trial.",
            "Pilot abstract reports physical-performance measures such as SPPB over the pilot follow-up.",
            "Full abstract reports prevention of major mobility disability as the primary endpoint.",
            "The trial family is direct, but the checked abstract endpoints are not the same plotted result.",
            "older-adult physical-activity context; surrogate/performance-to-disability example",
            "Hold until same endpoint values are sourced on both sides.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            146,
            "upbeat_behavior_process_vs_pregnancy_clinical_outcomes",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the UPBEAT pilot and full trial support a matched pregnancy-intervention row?",
            "Ying links the UPBEAT pilot to the larger UPBEAT randomized trial.",
            "Pilot abstract reports diet/activity behaviour change and process evaluation.",
            "Full abstract reports gestational diabetes and large-for-gestational-age infant outcomes.",
            "The checked evidence moves from behaviour/process endpoints to clinical pregnancy outcomes.",
            "UPBEAT pregnancy-intervention context",
            "Skip unless a same behaviour endpoint is available from the larger trial or same clinical endpoint is available from the pilot.",
        ),
        checked_ying_row(
            176,
            "breast_reconstruction_decision_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the preconsultation education pilot and phase 3 breast-reconstruction trial support a matched decision-quality row?",
            "Ying links a postmastectomy breast-reconstruction educational-group pilot to a larger phase 3 randomized trial.",
            "Pilot abstract names decisional conflict, self-efficacy, satisfaction, involvement, knowledge, anxiety, and related outcomes but no exact matched values in the checked abstract.",
            "Full abstract reports patient knowledge, anxiety, and decisional conflict.",
            "The outcome family overlaps, but exact values and a single outcome selector are missing from the abstract route.",
            "breast-reconstruction decision-support context; full-text extraction target",
            "Hold until exact same outcome values are sourced and one selector is documented.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            137,
            "falls_surface_perturbation_native_rate_hold",
            "hold_native_rate_ratio_no_current_d_route",
            "hold_native_only_not_current_d_equivalent",
            "Can the surface-perturbation pilot and pragmatic trial support a matched falls-prevention row?",
            "Ying links the SPTT pilot to the larger pragmatic surface-perturbation trial.",
            "Pilot abstract reports a falls-prevention exercise/training comparison and feasibility of a larger pragmatic trial.",
            "Full abstract reports falls and fall-related injury outcomes.",
            "The current abstract route does not expose exact matched values, and the natural endpoint is native falls-rate/count evidence without a current D route.",
            "falls-prevention surface-perturbation context; native-rate sensitivity",
            "Hold until exact events/person-time and an accepted rate-to-D policy are available.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            23,
            "breast_cancer_exercise_performance_vs_bmd",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the breast-cancer exercise pilot and 12-month exercise trial support a matched row?",
            "Ying links a vigorous aerobic exercise pilot to a larger supervised/home exercise trial in breast cancer patients.",
            "Pilot abstract emphasizes physical performance and feasibility, with bone-loss potential assessed.",
            "Full abstract reports bone mineral density by skeletal site and menopausal status.",
            "The checked evidence does not identify one same endpoint and contrast; physical performance and BMD are mixed.",
            "breast-cancer exercise context",
            "Hold until same endpoint values are sourced on both sides.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            247,
            "pediatric_hiv_incentive_dose_selector_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can the pediatric HIV testing incentive pilot and larger randomized trial support a matched uptake row?",
            "Ying links a Kenyan pediatric HIV testing incentive pilot to a larger randomized incentive trial.",
            "Pilot abstract reports N=60 women randomized to $5, $10, or $15 incentives, with 73% child testing and comparison to a historical no-incentive cohort.",
            "Full abstract reports a five-arm randomized trial with $0, $1.25, $2.50, $5, and $10 incentives.",
            "The candidate has many dose arms and the pilot lacks a randomized no-incentive comparator matching the full trial's $0 arm.",
            "financial-incentive dose-response context; possible dose-response sensitivity",
            "Do not promote without an explicit same-dose randomized contrast and selector policy.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            59,
            "nursing_home_pneumonia_protocol_vs_incidence",
            "hold_endpoint_and_control_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the nursing-home pneumonia pilot and cluster RCT support a matched prevention row?",
            "Ying links a protocol-testing pilot to a larger cluster-randomized pneumonia-prevention trial.",
            "Pilot abstract reports residents assigned to oral brushing/chlorhexidine frequencies or swallowing interventions, focused on feasibility/adherence and risk factors.",
            "Full abstract reports a multicomponent protocol versus usual care and radiographically documented pneumonia incidence.",
            "The intervention packages, control structure, and value-bearing endpoint are not matched.",
            "nursing-home pneumonia prevention context",
            "Skip unless a same intervention/control and same endpoint can be extracted.",
        ),
        checked_ying_row(
            69,
            "esophageal_brachytherapy_dfs_vs_dysphagia_relief",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the esophageal brachytherapy pilot and IAEA trial support a matched palliation row?",
            "Ying links the pilot HDRILBT plus EBRT trial to a larger IAEA multicentre trial.",
            "Pilot abstract emphasizes dysphagia-free survival and overall survival after HDRILBT with or without EBRT.",
            "Full abstract reports dysphagia-relief experience as the primary outcome, plus other palliation scores and survival.",
            "The checked primary endpoints are not the same estimand, and the abstract route does not provide matched D/N values.",
            "esophageal-cancer palliation context; endpoint-harmonization target",
            "Hold until full texts identify a same palliation endpoint and exact values.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            21,
            "chronic_depression_four_arm_selector_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can the chronic-depression pilot and larger self-management support trial support a matched row?",
            "Ying links a four-arm chronic-depression pilot to a larger organized self-management support service trial.",
            "Pilot abstract reports four intervention/usual-care variants and multiple outcomes across 3, 6, 9, and 12 months.",
            "Full abstract reports a two-arm 18-month self-management support service versus treatment as usual with depression and recovery outcomes.",
            "The pilot has multiple components and timepoints, and the checked abstracts do not define one exact original contrast matched to the full trial.",
            "chronic-depression self-management context",
            "Hold until a same contrast/outcome/timepoint selector and exact values are sourced.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            79,
            "harp_patient_activation_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the HARP pilot and larger peer-led self-management trial support a patient-activation row?",
            "Ying links the HARP peer-led medical self-management pilot to the larger HARP randomized trial.",
            "Pilot abstract reports N=80 and a significant patient-activation group-by-time result, including relative improvement versus decline.",
            "Full abstract reports N=198 HARP and N=202 usual care with assessments at baseline, 3 months, and 6 months.",
            "The pilot has suggestive patient-activation text, but the checked abstract route does not provide matched full-trial exact patient-activation values for conversion.",
            "serious-mental-illness peer self-management context; full-text extraction target",
            "Hold until exact patient-activation values on both sides are source-backed.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            85,
            "breathing_training_full_text_values_needed",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the malignant-lung-disease breathing-training pilot and larger trial support a matched breathlessness row?",
            "Ying links a high- versus low-intensity breathing-technique feasibility trial to a larger three-session versus one-session trial.",
            "Pilot abstract reports N=22, follow-up at 8 weeks, and breathlessness severity/distress plus other outcomes, but not exact matched values.",
            "Full abstract reports a larger multicentre trial of three versus one session with breathlessness outcomes.",
            "This is plausibly matched, but the checked abstract evidence lacks exact same-outcome values and arm Ns for a D conversion.",
            "breathlessness intervention context; high-priority full-text extraction target",
            "Hold until exact NRS breathlessness values are extracted.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            219,
            "mouthwash_timepoint_endpoint_mismatch",
            "hold_timepoint_and_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the Listerine pharyngeal-gonorrhoea pilot and OMEGA trial support a matched row?",
            "Ying links an antiseptic mouthwash pilot RCT to the larger OMEGA trial.",
            "Pilot abstract reports an immediate post-gargle pharyngeal culture/viability outcome in MSM with pharyngeal gonorrhoea.",
            "Full OMEGA abstract reports prevention/incidence of oropharyngeal gonorrhoea over a 12-week intervention period.",
            "The outcome and time window differ: immediate clearance/inhibition versus longer-term prevention/incidence.",
            "gonorrhoea mouthwash context; endpoint/timepoint mismatch example",
            "Do not promote under current same-endpoint and same-timepoint rules.",
        ),
        checked_ying_row(
            113,
            "docc_pediatric_behavior_cluster_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the DOCC pilot and larger pediatric behavioral-health cluster RCT support a matched row?",
            "Ying links the doctor-office collaborative-care preliminary trial to the larger cluster randomized DOCC trial.",
            "Pilot abstract reports N=55 DOCC and N=23 enhanced usual care and multiple diagnostic, process, and family outcomes.",
            "Full abstract reports N=160 DOCC and N=161 enhanced usual care with ADHD, parenting stress, goal attainment, and CGI-I outcomes.",
            "The relation is real, but the abstract route does not expose a single matched outcome and exact values for conversion.",
            "pediatric behavioral-health collaborative care context; full-text extraction target",
            "Hold until exact same outcome values and cluster-handling policy are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            110,
            "vitamin_d_cf_survival_vs_exacerbation_endpoint_gap",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the vitamin D cystic-fibrosis pilot and DISC trial support a matched row?",
            "Ying links the high-dose vitamin D pilot to the larger DISC trial in adults with cystic fibrosis.",
            "Pilot abstract reports N=30 and vitamin D status, clinical outcomes, adverse events, and survival analyses after pulmonary exacerbation.",
            "Full DISC abstract reports recurrence of pulmonary exacerbations and related clinical outcomes after bolus plus maintenance vitamin D.",
            "The checked abstracts do not provide a same endpoint/timepoint value pair; survival/hospital-free-days style pilot evidence would not match time-to-next-exacerbation framing.",
            "cystic-fibrosis vitamin D context",
            "Hold until exact same endpoint values are sourced.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            86,
            "deploy_extension_vs_ydpp_trial_intervention_timepoint",
            "hold_timepoint_and_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the DEPLOY extension pilot and larger YMCA DPP trial support a matched weight-loss row?",
            "Ying links the DEPLOY YMCA lifestyle extension pilot to a larger YMCA Diabetes Prevention Program trial.",
            "Pilot abstract reports a long-term extension where all prior participants were offered maintenance intervention after the original cluster-randomized trial.",
            "Full abstract reports a 12-month randomized comparative-effectiveness trial with YDPP versus brief lifestyle counseling.",
            "The pilot extension is not the same randomized intervention window or contrast as the larger trial.",
            "diabetes-prevention YMCA intervention context",
            "Skip unless the original randomized DEPLOY trial values, not extension-only values, are matched to the larger trial.",
        ),
        checked_ying_row(
            20,
            "quetiapine_alcoholism_subgroup_primary_endpoint_mismatch",
            "hold_endpoint_and_control_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the quetiapine alcoholism pilot and larger XR trial support a matched drinking row?",
            "Ying links a Type A/Type B alcoholism quetiapine pilot to the larger quetiapine XR trial in heavy-drinking alcohol-dependent patients.",
            "Pilot abstract reports Type A and Type B subgroups and multiple drinking outcomes, with source text suggesting subgroup-specific abstinence/drinking results.",
            "Full abstract reports N=224 and states no differences on the primary drinking outcomes.",
            "The checked abstracts do not expose the same outcome, subgroup, and exact full-trial value pair; using the pilot subgroup result against the full primary aggregate would bend row grain.",
            "alcohol pharmacotherapy context; subgroup-vs-aggregate caution",
            "Hold until same subgroup/outcome values are available or skip under current aggregate-matching rules.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            248,
            "calm_feasibility_vs_advanced_cancer_outcomes",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can CALM feasibility and full RCT support a matched advanced-cancer psychotherapy row?",
            "Ying links the CALM randomized feasibility trial to the larger CALM randomized controlled trial.",
            "Pilot abstract reports feasibility and preliminary psychological outcomes for Managing Cancer And Living Meaningfully.",
            "Full abstract reports the larger psychological-intervention RCT in advanced cancer.",
            "The checked abstract route lacks exact same outcome values and uses feasibility/preliminary-effect framing.",
            "advanced-cancer psychotherapy context; full-text extraction target",
            "Hold until exact same depression/distress or other primary outcome values are sourced.",
            "yes_until_full_text_value_evidence",
        ),
    ]

    secondary_checked_manual_rows = [
        checked_ying_row(
            153,
            "carpal_tunnel_quickdash_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the ultra-minimally invasive carpal-tunnel pilot and later RCT support a matched QuickDASH row?",
            "Ying links the Ultra-MIS external pilot study to the later randomized trial comparing 1-mm ultrasound-guided release with 2-cm mini-open release.",
            "Pilot abstract states QuickDASH at final follow-up was the primary variable but does not expose exact arm means, SDs, CI, or effect estimate.",
            "Full abstract states postoperative QuickDASH was the primary variable in a larger randomized trial, but the checked abstract route does not provide extractable values.",
            "The same primary outcome is plausible, but exact same-outcome values are missing from the local abstract route.",
            "carpal-tunnel surgical-technique replication; full-text table extraction target",
            "Hold until full text or tables provide exact QuickDASH values and arm Ns.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            29,
            "influenza_household_cluster_three_arm_metric_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can the Hong Kong household influenza pilot and larger cluster RCT support a matched transmission row?",
            "Ying links a preliminary household non-pharmaceutical-intervention trial to the larger facemask/hand-hygiene cluster randomized trial.",
            "Pilot abstract reports a three-arm household cluster trial with laboratory-confirmed influenza in contacts as the primary outcome.",
            "Full abstract reports a larger household cluster trial with control, hand hygiene, and facemask-plus-hand-hygiene arms.",
            "The source family is relevant, but the checked route leaves several possible contrasts and a clustered binary endpoint without a documented D-equivalent conversion.",
            "household influenza NPI context; cluster/binary metric policy target",
            "Hold until one contrast is selected, exact contact counts/events are sourced, and cluster-aware conversion policy is documented.",
            "yes_until_explicit_selector_and_metric_policy",
        ),
        checked_ying_row(
            90,
            "healthy_homework_stepcount_model_metric_mismatch",
            "hold_native_or_model_metric_not_current_d_route",
            "hold_native_or_mismatched_not_plot_ready",
            "Can the Healthy Homework pilot and larger trial support a matched physical-activity row?",
            "Ying links the Healthy Homework pilot to the larger cluster randomized Healthy Homework trial; both use pedometer-measured child physical activity.",
            "Pilot PMC full text reports N=57 intervention and N=40 control, and an intervention effect of 2,830 steps/day with 95% CI 560 to 5,300.",
            "Full PMC full text reports N=675 children and GLMM coefficients for weekday school, weekday home, and weekend steps at T1 and T2, including transformed/model-based estimates rather than the same raw all-day step-count effect.",
            "The relation is real and both sources are local, but the available effect metrics are not the same: raw all-day step-count contrast in the pilot versus domain/timepoint-specific GLMM coefficients in the larger trial.",
            "child physical-activity intervention context; transformed-model metric conversion target",
            "Hold until a defensible conversion chooses the same step-count domain and converts the GLMM output to current Figure 1 D.",
            "yes_until_explicit_selector_and_metric_policy",
            extra_paths=[
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260509/healthy_homework/PMC3256102_content.lines",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260509/healthy_homework/PMC3256102_meta.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260509/healthy_homework/PMC6729097_content.lines",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260509/healthy_homework/PMC6729097_meta.json",
                ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260509/healthy_homework/sha256sums.txt",
            ],
        ),
        checked_ying_row(
            43,
            "task_stroke_caregiver_multioutcome_selector_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can TASK stroke-caregiver pilot and larger TASK II trial support a matched caregiver-outcome row?",
            "Ying links the TASK pilot to the larger TASK II randomized clinical trial.",
            "Pilot abstract reports N=21 TASK and N=19 attention control, with six caregiver outcomes and significant optimism/task-difficulty/threat-appraisal findings at several timepoints.",
            "Full abstract reports N=123 TASK II and N=131 control with prespecified depressive symptoms, life changes, and unhealthy-days outcomes.",
            "The two abstracts expose different primary/prespecified outcome sets and no single same-outcome selector.",
            "stroke-caregiver intervention context; multioutcome selector target",
            "Hold until one same outcome and timepoint is explicitly selected from full-text values.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            190,
            "heartsleep_cbti_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the heart-failure CBT-I pilot and HeartSleep RCT support a matched insomnia row?",
            "Ying links the self-management CBT-I pilot to the larger HeartSleep randomized trial.",
            "Pilot abstract reports N=29 CBT-I and N=19 attention control with insomnia severity, actigraphy, fatigue, depression, sleepiness, and function outcomes.",
            "Full abstract reports a larger grouped RCT with insomnia severity, sleep efficiency, fatigue, and function outcomes across one year.",
            "The same intervention and broad outcomes are present, but exact same-outcome values are not exposed in the checked abstract route.",
            "CBT-I in heart failure context; full-text extraction target",
            "Hold until exact insomnia-severity or sleep-efficiency values and arm Ns are extracted.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            93,
            "hydrolyzed_formula_survival_endpoint_metric_hold",
            "hold_native_hazard_metric_no_current_d_route",
            "hold_native_only_not_current_d_equivalent",
            "Can the hydrolyzed-infant-formula pilot and larger trial support a matched beta-cell-autoimmunity row?",
            "Ying links the dietary-manipulation pilot to the larger hydrolyzed-formula randomized trial in infants at type 1 diabetes risk.",
            "Pilot abstract reports N=242 and emergence of diabetes-associated autoantibodies over a mean 4.7-year observation period.",
            "Full abstract reports N=2,159 and cumulative incidence of diabetes-associated autoantibodies.",
            "The endpoint is time-to/cumulative autoimmunity rather than a directly exposed current D route in the abstract-level evidence.",
            "type 1 diabetes prevention context; survival/cumulative-incidence conversion target",
            "Hold until exact event counts/time-to-event estimates and an accepted conversion are documented.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            180,
            "remind_memory_rehab_population_and_outcome_mismatch",
            "hold_endpoint_population_mismatch",
            "hold_not_promoted_current_figure1",
            "Can ReMiND pilot and the traumatic-brain-injury memory rehabilitation trial support a matched row?",
            "Ying links a memory rehabilitation RCT to a larger pragmatic memory rehabilitation trial.",
            "Pilot abstract reports N=72 with traumatic brain injury, stroke, or multiple sclerosis and compares compensation, restitution, and self-help group programs.",
            "Full abstract reports N=328 traumatic brain injury participants and intervention versus usual care, with EMQ-p at 6 months as primary outcome.",
            "The population, intervention arms, and comparator structure changed; no exact same original contrast is identified.",
            "memory rehabilitation context; population/arm-grain caution",
            "Skip unless a same TBI-only contrast and same EMQ endpoint can be sourced.",
        ),
        checked_ying_row(
            32,
            "project_story_eflip_three_arm_bmiz_selector_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_needs_more_evidence_not_plot_ready",
            "Can Project STORY and E-FLIP support a matched rural childhood obesity row?",
            "Ying links the Project STORY parent-only/family-based pilot to the later E-FLIP for Kids trial.",
            "Pilot abstract reports a three-arm parent-only, family-based, wait-list control design and BMI z-score effects at month 4 and month 10.",
            "Full abstract reports a three-arm family-based, parent-only, health-education condition trial and BMIz changes at year 1 and year 2.",
            "The source relation is plausible, but the row needs an explicit arm/timepoint selector; abstract values are rounded/model-based and multiarm.",
            "rural childhood obesity intervention context; arm/timepoint selector target",
            "Hold until one same arm contrast and timepoint are selected and exact model outputs are converted.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            76,
            "home_plus_feasibility_vs_multifollowup_behavior",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can HOME pilot and HOME Plus full trial support a matched home-food-environment row?",
            "Ying links the HOME pilot to the HOME Plus randomized controlled trial.",
            "Pilot abstract reports N=22 intervention and N=22 control with feasibility/acceptability and several psychosocial, anthropometric, dietary, and home-environment measures.",
            "Full abstract reports N=81 intervention and N=79 control with food-environment and nutrition-related outcomes at 12 and 21 months.",
            "The abstract route has many possible outcomes/timepoints but no exact same-outcome D/N-ready value pair.",
            "childhood-obesity home-food-environment context",
            "Hold until exact same outcome and timepoint values are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            140,
            "pregnancy_chocolate_population_and_measure_mismatch",
            "hold_endpoint_population_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the pregnancy chocolate pilot and later trial support a matched endothelial-function row?",
            "Ying links a healthy-pregnancy flavanol-rich chocolate pilot to a later trial in pregnant women at risk of preeclampsia.",
            "Pilot abstract reports healthy pregnant women with normal blood pressure and FMD/BP outcomes after high- versus low-flavanol chocolate.",
            "Full abstract reports women at risk of preeclampsia and reactive hyperemia index, augmentation index, and BP outcomes.",
            "The population and vascular-function measurement changed, so the checked source route does not preserve a same outcome/contrast.",
            "pregnancy chocolate/flavanol vascular-function context",
            "Skip unless same measurement and population values are sourced.",
        ),
        checked_ying_row(
            39,
            "diabetes_screening_anxiety_vs_population_mortality",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the diabetes-screening pilot and ADDITION-Cambridge mortality trial support a matched row?",
            "Ying links a general-practice diabetes-screening feasibility/anxiety trial to the larger ADDITION-Cambridge population mortality trial.",
            "Pilot abstract reports screening uptake and short-term anxiety/self-rated health outcomes.",
            "Full abstract reports population mortality over 10 years after screening and treatment policies.",
            "The checked evidence moves from feasibility/psychological short-term outcomes to long-term mortality.",
            "diabetes screening trial-development context",
            "Skip unless the same outcome class is sourced on both sides.",
        ),
        checked_ying_row(
            221,
            "ms_spasticity_app_cohort_then_randomization_mismatch",
            "hold_design_mismatch_and_arm_n_gap",
            "hold_not_promoted_current_figure1",
            "Can the MS spasticity app pilot and multicenter study support a matched row?",
            "Ying links a randomized app-based home-therapy pilot to a later multicenter study.",
            "Pilot abstract reports N=20 randomized app versus paper home program after inpatient rehabilitation, with all patients later receiving the app.",
            "Full abstract reports initial MIR in a cohort, then randomizes MIR responders to app or paper self-training.",
            "The later study's enrichment after MIR response and two-stage design do not cleanly replicate the pilot randomized contrast.",
            "MS spasticity app context; staged/enriched design caution",
            "Skip unless a same randomized contrast and exact values are isolated.",
        ),
        checked_ying_row(
            246,
            "electroacupuncture_back_surgery_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the electroacupuncture pilot and multicentre trial support a matched VAS pain row?",
            "Ying links a pilot randomized electroacupuncture plus usual care trial to a larger multicentre trial for non-acute pain after back surgery.",
            "Pilot abstract reports the same VAS pain primary outcome but does not expose extractable between-arm effect values in the local abstract route.",
            "Full abstract reports larger-trial VAS and ODI mean differences at week 5.",
            "The larger side is value-bearing, but the pilot-side exact same VAS effect is missing from the checked abstract route.",
            "electroacupuncture back-surgery pain context; high-priority full-text extraction target",
            "Hold until pilot full text gives exact VAS values and arm Ns.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            80,
            "glaucoma_mi_feasibility_vs_adherence_trial",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the glaucoma motivational-interviewing feasibility study and larger adherence trial support a matched row?",
            "Ying links a glaucoma educator motivational-interviewing feasibility study to a larger medication-adherence RCT.",
            "Pilot abstract evaluates feasibility criteria including fidelity, training, delivery, receipt, and enactment.",
            "Full abstract reports MEMS/self-report adherence effects for motivational interviewing or reminders versus usual care.",
            "The original artifact is feasibility-focused and does not expose a same adherence treatment-effect row.",
            "glaucoma medication-adherence context",
            "Skip unless a same adherence outcome effect is sourced from the pilot.",
        ),
        checked_ying_row(
            135,
            "bci_cognitive_training_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the BCI cognitive-training pilot and larger trial support a matched RBANS/cognitive row?",
            "Ying links a brain-computer-interface cognitive-training pilot in healthy elderly to a larger personalized neurofeedback trial.",
            "Pilot abstract reports N=15 intervention and N=16 waitlist control and usability/preliminary efficacy.",
            "Full abstract reports a larger randomized trial with RBANS total score as primary outcome.",
            "The checked abstracts do not expose exact same cognitive-outcome values for a D conversion.",
            "healthy-elderly cognitive training context; full-text extraction target",
            "Hold until exact same outcome values are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            57,
            "switch_tv_monitor_vs_family_screentime_package",
            "hold_intervention_and_subgroup_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the TV-time-monitor pilot and SWITCH trial support a matched screen-time row?",
            "Ying links a home-based electronic TV time-monitor pilot to the larger SWITCH family-delivered screen-time weight-loss intervention.",
            "Pilot abstract tests an electronic TV time monitor plus advice versus advice control for six weeks.",
            "Full abstract tests a broader 20-week family-delivered intervention targeting screen-based sedentary behaviour, body composition, activity, and diet.",
            "The larger intervention package is not the same original time-monitor contrast.",
            "child screen-time intervention context",
            "Skip unless a same electronic-monitor contrast is sourced.",
        ),
    ]

    final_remaining_scan_rows = [
        checked_ying_row(
            178,
            "avatar_psyrats_original_n_gap",
            "hold_needs_full_text_original_counts",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the AVATAR proof-of-concept study and larger AVATAR RCT support a matched PSYRATS hallucinations row?",
            "Ying links the small AVATAR therapy proof-of-concept trial to the larger single-blind AVATAR therapy RCT.",
            "Pilot abstract reports PSYRATS auditory hallucination score reduction of 8.75 and therapy effect size 0.8, but does not expose original arm Ns in the checked abstract.",
            "Full abstract reports N=75 AVATAR and N=75 supportive counselling, with PSYRATS-AH mean difference -3.82 (SE 1.47) at 12 weeks.",
            "The endpoint is plausible, but the original-side arm Ns and exact D/N conversion inputs are not fully source-backed from local evidence.",
            "AVATAR therapy replication; high-priority original full-text acquisition",
            "Hold until the original article is acquired and arm Ns/effect conversion are verified.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            53,
            "sms_smoking_pilot_intensity_vs_cluster_trial",
            "hold_design_mismatch_and_arm_n_gap",
            "hold_not_promoted_current_figure1",
            "Can the SMS smoking-cessation pilot and larger cluster RCT support a matched abstinence row?",
            "Ying links an individual SMS smoking-cessation pilot to a larger school-class cluster randomized SMS trial.",
            "Pilot abstract reports three arms: control, one weekly SMS feedback, and three weekly SMS feedbacks, with no significant short-term smoking-variable differences.",
            "Full abstract reports a two-arm cluster randomized SMS intervention versus assessment-only control in vocational school classes.",
            "The intervention intensity, randomization unit, and contrast changed; no exact same original contrast is identified.",
            "SMS smoking-cessation intervention context",
            "Skip unless a same feedback-intensity contrast and exact abstinence values are sourced.",
        ),
        checked_ying_row(
            173,
            "legacy_intervention_qol_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the pediatric cancer digital-storytelling pilot and larger legacy-intervention RCT support a matched QOL row?",
            "Ying links the digital-storytelling legacy-making pilot to the larger web-based legacy-intervention RCT.",
            "Pilot abstract reports N=15 intervention and N=13 control, and only qualitative/small nonsignificant PedsQL improvements without exact effect values.",
            "Full abstract reports N=150 randomized and analysed dyads with small Cohen's d values for selected PedsQL Cancer Module dimensions.",
            "The checked abstract route lacks exact same QOL dimension values from the pilot and a single outcome selector.",
            "pediatric palliative legacy intervention context",
            "Hold until full text provides exact same PedsQL dimension values and an outcome selector.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            28,
            "restorative_yoga_waitlist_vs_stretching_comparator_mismatch",
            "hold_active_comparator_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the restorative yoga pilot and PRYSMS trial support a matched metabolic row?",
            "Ying links a restorative-yoga pilot to the larger PRYSMS trial in metabolic syndrome.",
            "Pilot abstract reports restorative yoga versus wait-list control and feasibility/metabolic trends.",
            "Full abstract reports restorative yoga versus active stretching with fasting glucose and other metabolic outcomes at 6 and 12 months.",
            "The larger trial uses an active stretching comparator rather than the pilot's wait-list control.",
            "restorative yoga/metabolic syndrome context",
            "Skip unless same comparator contrast values are sourced.",
        ),
        checked_ying_row(
            217,
            "wins_net_feasibility_vs_distress_info_slopes",
            "hold_feasibility_original_no_matched_effect",
            "hold_not_promoted_current_figure1",
            "Can the WINS NET feasibility study and later RCT support a matched distress/information row?",
            "Ying links the WINS feasibility study to a larger web-based personalised information/support RCT in neuroendocrine tumor patients.",
            "Pilot abstract reports N=10 standard care and N=10 intervention, feasibility/interview findings, and several Cohen's d exploratory effects.",
            "Full abstract reports N=49 standard care and N=53 intervention, with no difference in distress and information/satisfaction slopes.",
            "The original feasibility study reports exploratory mixed outcomes and does not define a single same primary endpoint as the larger trial.",
            "neuroendocrine tumor eHealth context",
            "Hold only for a later full-text outcome-selector pass.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            119,
            "hirrem_insomnia_waitlist_vs_sham_timepoint_mismatch",
            "hold_timepoint_and_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the HIRREM insomnia pilot and larger sham-controlled trial support a matched ISI row?",
            "Ying links the HIRREM wait-list crossover pilot to the larger placebo/sham-controlled insomnia trial.",
            "Pilot abstract reports N=20, HIRREM plus usual care versus usual care, and differential ISI change of -10.3 points after the initial intervention period.",
            "Full abstract reports N=56 linked-brainwave tones and N=51 random tones, with differential ISI change at 8-10 weeks of -2.05 points.",
            "The comparator and follow-up window differ: usual-care wait-list crossover versus active sham placebo, and a different post-intervention timing.",
            "HIRREM insomnia context; comparator/timepoint sensitivity",
            "Do not promote under current same-comparator and same-timepoint rules.",
        ),
        checked_ying_row(
            99,
            "systemchange_transplant_median_adherence_metric_hold",
            "hold_native_or_model_metric_not_current_d_route",
            "hold_native_or_mismatched_not_plot_ready",
            "Can TIMELink and MAGIC/SystemCHANGE support a matched transplant medication-adherence row?",
            "Ying links the TIMELink pilot to the larger MAGIC/SystemCHANGE randomized trial.",
            "Pilot abstract reports N=8 intervention and N=5 attention control nonadherent recipients, with Cohen's d=1.4 for medication adherence.",
            "Full abstract reports N=89 completers and median adherence/IQR differences at 6 and 12 months.",
            "The larger result is median/IQR adherence, not a currently accepted D conversion from the abstract route.",
            "kidney-transplant medication-adherence context; median/IQR conversion target",
            "Hold until full text/data provide mean/SD or an accepted median/IQR-to-D policy.",
            "yes_until_metric_policy_changes",
        ),
        checked_ying_row(
            128,
            "lightning_process_feasibility_no_effect_values",
            "hold_feasibility_original_no_matched_effect",
            "hold_not_promoted_current_figure1",
            "Can the SMILE feasibility study and full Lightning Process trial support a matched SF-36 physical-function row?",
            "Ying links the SMILE feasibility randomized trial to the full paediatric CFS/ME Lightning Process RCT.",
            "Pilot abstract reports recruitment/acceptability changes to the full protocol and recommends changing the full-study primary outcome.",
            "Full abstract reports SF-36-PFS adjusted mean differences at 6 and 12 months.",
            "The pilot abstract does not provide the same value-bearing SF-36-PFS effect; it is feasibility/protocol work.",
            "paediatric CFS/ME Lightning Process context",
            "Skip unless pilot full text exposes exact same outcome values.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            9,
            "welfare_rights_feasibility_vs_casp_mortality_quality_of_life",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can welfare-rights advice pilot and definitive domiciliary trial support a matched HRQOL row?",
            "Ying links a primary-care welfare-rights pilot to a larger domiciliary welfare-rights advice RCT.",
            "Pilot abstract reports feasibility/acceptability and identification of outcome measures.",
            "Full abstract reports CASP-19 health-related quality of life and economic/process outcomes at 24 months.",
            "The pilot route is not value-bearing for the same CASP-19 endpoint.",
            "welfare-rights social intervention context",
            "Skip unless exact same HRQOL values are found in the pilot source.",
        ),
        checked_ying_row(
            66,
            "guided_imagery_cortisol_vs_lifestyle_behaviors",
            "hold_endpoint_population_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the guided-imagery cortisol pilot and Imagine HEALTH trial support a matched row?",
            "Ying links an acute guided-imagery stress-reduction pilot to the larger Imagine HEALTH lifestyle trial.",
            "Pilot abstract route is an acute salivary cortisol/stress-reduction study in overweight Latino adolescents.",
            "Full abstract reports lifestyle behaviors and obesity-related outcomes in a guided-imagery lifestyle intervention.",
            "The endpoint and intervention frame changed from acute cortisol response to broader lifestyle behavior.",
            "guided-imagery adolescent health context",
            "Skip unless same endpoint values are sourced.",
        ),
        checked_ying_row(
            222,
            "civic_spinal_cord_mortality_arm_n_gap",
            "hold_needs_full_text_original_counts",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the Bangladesh SCI pilot and CIVIC trial support a matched 2-year mortality row?",
            "Ying links the SCI community-based-care pilot to the full CIVIC trial.",
            "Pilot abstract reports N=30 and two deaths, one in each group, at 2 years, but does not expose exact randomized arm Ns in the local source.",
            "Full abstract reports N=204 intervention and N=206 control, with 15 versus 16 deaths at 2 years.",
            "This is close to a valid row, but the original arm denominators are not explicitly source-backed in the checked local abstract.",
            "spinal-cord-injury community-care replication; high-priority original full-text acquisition",
            "Hold until the pilot full text or table confirms arm Ns and mortality counts.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            223,
            "spg_osas_pcrit_vs_ahi_endpoint_mismatch",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the SPG osteopathic manipulation pilot and larger OSAS trial support a matched row?",
            "Ying links a proof-of-concept crossover study to a larger crossover OSAS trial.",
            "Pilot abstract primary endpoint is responder status on critical closing pressure at 30 min.",
            "Full abstract primary endpoint is apnoea-hypopnoea index, with PNIF and awake Pcrit secondary endpoints at 30 min and 24 h.",
            "The primary endpoints differ and the larger trial's Pcrit secondary endpoint is not the same responder definition.",
            "OSAS osteopathic manipulation context",
            "Skip unless a same Pcrit definition is sourced on both sides.",
        ),
        checked_ying_row(
            19,
            "computer_tailored_physical_activity_population_followup_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the computer-tailored adolescent physical-activity pilot and larger trial support a matched row?",
            "Ying links a pilot computer-tailored PA intervention to a larger computer-tailored PA trial.",
            "Pilot abstract route reports acceptability/feasibility/effectiveness but not exact same outcome values in the checked local evidence.",
            "Full abstract route reports effectiveness versus generic advice.",
            "The checked abstracts lack exact matched PA values and a timepoint selector.",
            "adolescent computer-tailored physical-activity context",
            "Hold until exact same outcome/timepoint values are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            205,
            "parent_mentors_obesity_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can parent-mentor obesity pilot and Growing Healthy Together trial support a matched BMI row?",
            "Ying links a parent-mentor pilot to a larger low-income Latino early-childhood-obesity parent-mentor trial.",
            "Pilot abstract route does not expose exact same BMI or weight-status values for a D conversion.",
            "Full abstract route reports parent-mentor randomized clinical trial outcomes.",
            "The relation is plausible but exact matched values are missing from the local abstract route.",
            "early childhood obesity parent-mentor context",
            "Hold until exact same BMI/weight outcome values are extracted.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            56,
            "hiv_youth_motivational_intervention_multirisk_outcome_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can Healthy Choices and the multisite HIV youth motivational trial support a matched row?",
            "Ying links a Healthy Choices motivational enhancement pilot to a larger multisite motivational intervention trial in youth living with HIV.",
            "Pilot abstract route covers multiple health risk behaviors in HIV-positive youth.",
            "Full abstract route targets multiple risk behaviors and health outcomes.",
            "The current evidence does not specify one original target behavior/outcome and matched larger-trial result.",
            "HIV youth motivational intervention context",
            "Hold until an explicit outcome selector and exact values are sourced.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            8,
            "kaledo_cluster_boardgame_value_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the Kaledo pilot and larger cluster trial support a matched nutrition/behavior row?",
            "Ying links the Kaledo educational board-game pilot to the larger school cluster randomized trial.",
            "Pilot abstract route reports nutritional knowledge/healthy eating behavior but exact matched values are not exposed in the checked evidence.",
            "Full abstract route reports a cluster randomized healthy lifestyle promotion trial.",
            "The candidate needs cluster-aware exact values and a same outcome selector.",
            "school nutrition board-game context",
            "Hold until exact same outcome values and cluster handling are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            207,
            "wise_teacher_student_mental_health_feasibility_vs_cluster_outcomes",
            "hold_feasibility_original_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can WISE pilot and full WISE high-school trial support a matched mental-health row?",
            "Ying links the WISE pilot cluster RCT to the full WISE cluster randomized trial.",
            "Pilot abstract route emphasizes support/training feasibility and school-level mental-health intervention development.",
            "Full abstract route reports teacher well-being and student-support outcomes.",
            "The checked pilot route does not expose exact same primary outcome values.",
            "school mental-health intervention context",
            "Hold until same outcome values are extracted from full text.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            188,
            "virtual_field_trip_pilot_vs_classroom_activity_trial",
            "hold_endpoint_and_control_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the virtual field trips pilot and larger physically active lessons trial support a matched row?",
            "Ying links a virtual-field-trip pilot to a larger Virtual Traveller physically active lessons cluster RCT.",
            "Pilot abstract route reports feasibility/activity in physically active lessons.",
            "Full abstract route reports lesson activity and on-task behavior in a cluster randomized trial.",
            "The checked abstract evidence lacks exact values and does not establish the same endpoint/control contrast.",
            "school physically active lessons context",
            "Hold until exact same endpoint values are available.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            16,
            "aromatase_acupuncture_pilot_full_text_needed",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the acupuncture pilot and larger sham-controlled aromatase-inhibitor joint-symptom trial support a matched row?",
            "Ying links an acupuncture pilot to a larger randomized, blinded, sham-controlled acupuncture trial.",
            "Pilot abstract route does not expose exact same joint-symptom values in the local evidence.",
            "Full abstract route reports acupuncture for aromatase inhibitor-associated joint symptoms.",
            "The relation and endpoint are plausible, but exact matched values are missing.",
            "acupuncture for aromatase-inhibitor joint symptoms; full-text extraction target",
            "Hold until exact same pain/joint-symptom values and arm Ns are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            48,
            "hylan_dose_finding_vs_single_injection_selector_gap",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can the hylan G-F 20 dosing pilot and single-injection RCT support a matched OA knee row?",
            "Ying links a five-regimen viscosupplementation dose/safety pilot to a larger single-injection placebo-controlled trial.",
            "Pilot abstract route has multiple dosing regimens.",
            "Full abstract route tests one 6 mL intra-articular hylan G-F 20 treatment versus placebo.",
            "The original dose selector and exact same contrast are not established.",
            "knee osteoarthritis viscosupplementation dose-finding context",
            "Hold until a prespecified dose mapping and exact values are sourced.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            229,
            "vitamin_d_copd_respiratory_strength_vs_exacerbation_metric_gap",
            "hold_endpoint_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the COPD vitamin D pilot and larger trial support a matched row?",
            "Ying links a vitamin D-deficient COPD pilot to a larger vitamin D supplementation RCT.",
            "Pilot title/source route emphasizes respiratory muscle strength and physical performance.",
            "Full title/source route emphasizes vitamin D supplementation in COPD patients with low serum vitamin D, with broader clinical outcomes.",
            "The checked evidence does not identify a same endpoint/value pair.",
            "COPD vitamin D context",
            "Hold until exact same outcome values are sourced.",
            "yes_until_same_endpoint_full_text",
        ),
        checked_ying_row(
            17,
            "mind_body_weight_loss_maintenance_intervention_mismatch",
            "hold_intervention_and_subgroup_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the mind-body weight-loss maintenance pilot and TAT weight-loss maintenance trial support a matched row?",
            "Ying links a two-mind-body-interventions pilot to a larger Tapas Acupressure Technique trial.",
            "Pilot abstract route compares two mind-body interventions for weight-loss maintenance.",
            "Full abstract route tests TAT for weight-loss maintenance.",
            "The original intervention family and comparator are not the same clean contrast.",
            "weight-loss maintenance mind-body intervention context",
            "Skip unless exact same TAT contrast values are isolated.",
        ),
        checked_ying_row(
            50,
            "fast_indicate_phase2_three_arm_vs_factorial_package",
            "hold_ambiguous_one_to_many_outcomes",
            "hold_not_promoted_current_figure1",
            "Can the stroke upper-limb phase II trial and FAST-INdiCATE support a matched row?",
            "Ying links a phase II upper-limb stroke trial to the FAST-INdiCATE trial.",
            "Pilot abstract route reports CPT, CPT+CPT, and CPT+FST arms with ARAT as primary outcome.",
            "Full abstract route includes functional strength training and movement performance therapy packages.",
            "The multiarm intervention mapping and exact contrast are not established from the checked evidence.",
            "stroke upper-limb rehabilitation context",
            "Hold until a same contrast and exact ARAT values are sourced.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            97,
            "activity_pacing_tailored_vs_time_based_intervention_mismatch",
            "hold_intervention_and_subgroup_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the tailored activity-pacing pilot and larger OA pacing trial support a matched row?",
            "Ying links a tailored versus general activity-pacing pilot to a later time-based activity-pacing trial.",
            "Pilot abstract compares tailored activity pacing with general pacing.",
            "Full abstract evaluates time-based activity pacing as a singular intervention for osteoarthritis.",
            "The intervention and comparator are not the same original contrast.",
            "osteoarthritis activity-pacing context",
            "Skip unless a same tailored/general pacing contrast is sourced.",
        ),
        checked_ying_row(
            63,
            "depression_acupuncture_pilot_protocol_no_results",
            "hold_protocol_or_registration_no_final_replication_values",
            "hold_not_promoted_current_figure1",
            "Can the depression acupuncture/counselling pilot and full primary-care trial support a matched row?",
            "Ying links an acupuncture/counselling pilot protocol to the full PLoS Medicine trial.",
            "Pilot-side checked artifact is a Trials protocol/design paper rather than value-bearing pilot results.",
            "Full abstract reports N=755 and BDI-II outcomes for acupuncture, counselling, and usual care.",
            "A protocol source is not sufficient original value evidence.",
            "depression acupuncture/counselling context",
            "Hold until value-bearing pilot result source is found.",
            "yes_until_original_source_object_acquired",
        ),
        checked_ying_row(
            115,
            "gua_sha_neck_back_vs_low_back_population_mismatch",
            "hold_endpoint_population_mismatch",
            "hold_not_promoted_current_figure1",
            "Can the Gua Sha pilot and later low-back-pain RCT support a matched row?",
            "Ying links a Gua Sha pilot in chronic neck and low-back pain to a later chronic low-back-pain RCT.",
            "Pilot abstract pools or includes chronic neck pain and chronic low-back pain patients.",
            "Full abstract is chronic low-back pain only with two Gua Sha treatments versus waitlist.",
            "The population and possibly subgroup contrast do not match from the abstract route.",
            "Gua Sha pain intervention context",
            "Hold unless low-back-only pilot values are sourced.",
            "yes_until_same_population_values",
        ),
        checked_ying_row(
            167,
            "umezu_polyphenols_bp_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the Umezu polyphenols pilot and larger BP trial support a matched blood-pressure row?",
            "Ying links a 15-person Umezu polyphenols safety/adherence pilot to a larger 72-person community BP trial.",
            "Pilot abstract reports BP followed at home/office but does not expose exact between-arm BP effect values.",
            "Full abstract reports home and office BP patterns and a community placebo-controlled trial.",
            "The endpoint is plausible, but exact same BP values are missing from local abstract evidence.",
            "Umezu polyphenols blood-pressure context",
            "Hold until exact same BP values and arm Ns are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            195,
            "hydrocortisone_ptsd_retention_vs_caps_outcome_gap",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the hydrocortisone-augmented PE pilot and larger combat-veteran PTSD trial support a matched CAPS row?",
            "Ying links a 24-veteran hydrocortisone augmentation pilot to a 60-veteran randomized placebo-controlled trial.",
            "Pilot abstract reports improved treatment retention and outcome but does not expose exact CAPS values in the checked local evidence.",
            "Full abstract reports CAPS primary outcome and secondary outcomes.",
            "The same intervention family is plausible, but exact same outcome values are missing.",
            "PTSD prolonged-exposure augmentation context",
            "Hold until exact CAPS values and arm Ns are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            114,
            "advanced_cancer_symptom_cluster_values_missing",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the advanced-cancer CBS pilot and larger CBS trial support a matched symptom-cluster row?",
            "Ying links a patient-controlled cognitive-behavioral pilot to a larger brief CBS intervention RCT for pain/fatigue/sleep disturbance.",
            "Pilot abstract reports N=43 intervention and N=43 control with symptom-cluster outcomes but no exact effect values in the abstract.",
            "Full abstract reports N=164 and symptom cluster severity, distress, and interference at 3, 6, and 9 weeks.",
            "The outcome family is plausible, but exact same timepoint/outcome values are missing from the abstract route.",
            "advanced-cancer symptom-cluster intervention context",
            "Hold until exact values and a timepoint selector are extracted.",
            "yes_until_explicit_selector_and_values",
        ),
        checked_ying_row(
            228,
            "blood_donor_redonation_rates_full_text_needed",
            "hold_needs_full_text_value_evidence",
            "hold_needs_more_evidence_not_plot_ready",
            "Can the inactive blood donor pilot and larger reactivation trial support a matched re-donation row?",
            "Ying links a pilot randomized telephone/SMS/no-intervention trial to a larger inactive-donor reactivation RCT.",
            "Pilot abstract reports N=1,188 and statistically different re-donation rates, but exact per-arm re-donation counts/rates are truncated from the checked local route.",
            "Full abstract reports N=11,880 and primary re-donation rate across telephone, SMS, and no-intervention groups, but no exact event counts in the abstract.",
            "This is a plausible row family, but both sides need exact arm-level re-donation counts before conversion.",
            "blood-donor reactivation context; high-priority full-text extraction target",
            "Hold until full text provides exact per-arm re-donation counts for a selected contrast.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            11,
            "girls_on_the_move_pilot_design_vs_cluster_mvpa",
            "hold_design_mismatch_and_arm_n_gap",
            "hold_not_promoted_current_figure1",
            "Can Girls on the Move pilot and group randomized trial support a matched MVPA row?",
            "Ying links the Girls on the Move feasibility pilot to a larger group randomized trial.",
            "Pilot abstract reports a pretest-posttest control group design by instructional grade.",
            "Full abstract reports 24 schools pair-matched and cluster randomized, with MVPA primary outcome.",
            "The pilot randomization/design and exact outcome values are not sufficient for a matched D/N row.",
            "adolescent physical-activity intervention context",
            "Hold until exact values and cluster/design handling are sourced.",
            "yes_until_full_text_value_evidence",
        ),
        checked_ying_row(
            88,
            "school_support_hiv_cluster_biomarker_metric_hold",
            "hold_native_or_model_metric_not_current_d_route",
            "hold_native_or_mismatched_not_plot_ready",
            "Can the Kenyan orphan school-support pilot and larger HIV prevention trial support a matched biomarker row?",
            "Ying links the pilot school-support trial to the larger clustered randomized HIV prevention trial.",
            "Pilot abstract reports N=105 and GEE risk-factor results for HIV-related behaviors.",
            "Full abstract reports N=835 in 26 schools and HIV/HSV-2 biomarkers analysed with survey logistic regression or GEE.",
            "The endpoint/metric is clustered binary biomarker or risk-factor evidence without exact D-equivalent inputs in the abstract route.",
            "structural HIV prevention context",
            "Hold until exact event counts/model outputs and a cluster-aware conversion policy are available.",
            "yes_until_metric_policy_changes",
        ),
    ]

    for manual in [
        *promoted_manual_rows,
        *checked_manual_rows,
        *additional_checked_manual_rows,
        *secondary_checked_manual_rows,
        *final_remaining_scan_rows,
    ]:
        candidate_id = clean(manual["candidate_id"])
        if candidate_id in existing_ids:
            continue
        source_paths, checksums = path_evidence(manual.pop("source_paths"))
        manual["source_evidence_paths"] = source_paths
        manual["source_checksums"] = checksums
        rows.append(manual)
        existing_ids.add(candidate_id)
        try:
            existing_pairs.add(int(manual["ying_pair"]))
        except Exception:
            pass

    if promoted is not None:
        for row in promoted.to_dict("records"):
            pair_id = clean(row.get("pair_id"))
            match = re.search(r"ying_2023_pair_(\d+)", pair_id)
            if not match:
                continue
            pair = int(match.group(1))
            candidate_id = pair_id
            if pair in existing_pairs or candidate_id in existing_ids:
                continue
            source_paths, checksums = path_evidence(split_support_paths(row.get("raw_file")))
            notes = clean(row.get("notes"))
            rows.append(
                {
                    "reviewed_at": REVIEWED_AT,
                    "workstream": "ying_promoted_contract_backfill",
                    "candidate_id": candidate_id,
                    "ying_pair": pair,
                    "status": "promoted",
                    "figure1_decision": "promoted_to_current_figure1",
                    "skip_in_goal3000": "yes",
                    "reviewed_question": (
                        "Backfill promoted Ying row already present in the promoted pair contract and current Figure 1 root table."
                    ),
                    "source_evidence_paths": source_paths or clean(row.get("raw_file")),
                    "source_checksums": checksums,
                    "relation_evidence": (
                        f"Ying promoted pair contract row for pilot '{clean(row.get('original_title'))}' versus "
                        f"larger trial '{clean(row.get('replication_title'))}'. Original DOI={clean(row.get('original_doi'))}; "
                        f"replication DOI={clean(row.get('replication_doi'))}."
                    ),
                    "original_value_evidence": (
                        f"Outcome={clean(row.get('outcome'))}; D_original={clean(row.get('D_original'))}; "
                        f"N_original={clean(row.get('N_original'))}. {notes}"
                    )[:2500],
                    "replication_value_evidence": (
                        f"Outcome={clean(row.get('outcome'))}; D_replication={clean(row.get('D_replication'))}; "
                        f"N_replication={clean(row.get('N_replication'))}. {notes}"
                    )[:2500],
                    "mismatch_or_blocker": (
                        "No blocker for current goal accounting: this row is already promoted. This ledger row exists to "
                        "prevent re-review of a valid row whose detailed candidate-level disposition was missing."
                    ),
                    "possible_reuse": "Ying promoted-row provenance hardening; source-result support extraction",
                    "next_action": "Already counted in current Figure 1; do not re-add. Revisit only for source-result provenance hardening.",
                }
            )
            existing_ids.add(candidate_id)
            existing_pairs.add(pair)

    if scan is not None:
        pmc_to_pair: dict[str, int] = {}
        scan_by_pair = {}
        for _, row in scan.iterrows():
            pair = int(row["pair"])
            scan_by_pair[pair] = row
            for col in ["pilot_pmcid", "full_pmcid"]:
                value = clean(row.get(col))
                if value:
                    pmc_to_pair[value] = pair

        found: dict[int, list[Path]] = defaultdict(list)
        base = ROOT / "data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508"
        if base.exists():
            for path in base.rglob("*"):
                if not path.is_file():
                    continue
                match = re.search(r"(PMC\d+)", path.name)
                if match and match.group(1) in pmc_to_pair:
                    found[pmc_to_pair[match.group(1)]].append(path)

        for pair in sorted(found):
            if pair in promoted_nums or pair in existing_pairs:
                continue
            row = scan_by_pair.get(pair)
            if row is None:
                continue
            candidate_id = f"ying_2023_pair_{pair:03d}_prior_fulltext_rescue_needs_reconstruction"
            if candidate_id in existing_ids:
                continue
            paths = sorted({rel(path) for path in found[pair]})
            checksums = []
            for path_text in paths[:12]:
                p = ROOT / path_text
                if p.exists():
                    checksums.append(f"{path_text}={file_sha256(p)}")
            rows.append(
                {
                    "reviewed_at": REVIEWED_AT,
                    "workstream": "ying_exact_value_pmc_rescue",
                    "candidate_id": candidate_id,
                    "ying_pair": pair,
                    "status": "prior_reject_needs_reconstruction",
                    "figure1_decision": "not_counted_current_figure1_pending_reconstruction",
                    "skip_in_goal3000": "yes_until_reconstructed",
                    "reviewed_question": "Local full-text rescue artifacts exist, but no durable candidate-level reject/hold detail was found.",
                    "source_evidence_paths": "; ".join(paths),
                    "source_checksums": "; ".join(checksums),
                    "relation_evidence": f"Ying scan candidate: pilot '{clean(row.get('pilot_title'))}' versus full '{clean(row.get('full_title'))}'.",
                    "original_value_evidence": clean(row.get("pilot_snippet"))[:900],
                    "replication_value_evidence": clean(row.get("full_snippet"))[:900],
                    "mismatch_or_blocker": "Prior local full-text acquisition implies this candidate was checked, but exact final blocker was not found in durable ledger/log artifacts.",
                    "possible_reuse": "Reconstructable candidate for future adjudication; source paths prevent blind rediscovery.",
                    "next_action": "Before retrying, inspect the listed local full-text artifacts and replace this reconstruction row with a specific promote/hold/reject decision.",
                }
            )

    out = pd.DataFrame(rows, columns=YING_COLUMNS).fillna("")
    out.to_csv(ledger_path, sep="\t", index=False)
    return ledger_path


def write_summary(paths: list[Path | None]) -> Path:
    summary_rows = []
    for path in paths:
        if path is None or not path.exists():
            continue
        df = pd.read_csv(path, sep="\t")
        group_cols = [col for col in ["workstream", "status"] if col in df.columns]
        if group_cols:
            grouped = df.groupby(group_cols, dropna=False).size().reset_index(name="rows")
            grouped.insert(0, "ledger", rel(path))
            summary_rows.append(grouped)
    summary = pd.concat(summary_rows, ignore_index=True) if summary_rows else pd.DataFrame()
    out = OUT_DIR / "adjudication-ledger-backfill-summary.tsv"
    summary.to_csv(out, sep="\t", index=False)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metascience_outside = write_metascience_outside_family_ledger()
    source = write_source_ledger()
    reviewcue = write_reviewcue_ledger()
    ying = write_ying_ledger()
    summary = write_summary([source, reviewcue, ying, metascience_outside])
    for path in [source, reviewcue, ying, metascience_outside, summary]:
        if path:
            df = pd.read_csv(path, sep="\t")
            print(f"{rel(path)}\t{len(df)}")


if __name__ == "__main__":
    main()
