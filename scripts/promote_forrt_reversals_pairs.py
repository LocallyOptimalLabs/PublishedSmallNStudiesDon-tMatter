#!/usr/bin/env python3
"""Promote conservative Figure 1 rows from the mirrored FORRT reversals page.

The FORRT reversals page is a value-bearing source object for a small number of
original-vs-larger follow-up rows: it gives the represented papers, local
sample-size text, and d-equivalent effect sizes in the same HTML entry.  This
script promotes only rows that have exact D, exact N, a named original and
larger follow-up/meta-analytic critique, and no known current Figure 1 duplicate.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
RAW_HTML = (
    ROOT
    / "data"
    / "raw"
    / "replication_projects"
    / "lead_harvest"
    / "figure1_research_followup_20260504"
    / "forrt_reversals"
    / "12_html_database_https_forrt_org_reversals.bin"
)
CROSSREF_DIR = RAW_HTML.parent / "crossref"
PROMOTED = ROOT / "data" / "derived" / "replication_pairs" / "harvest" / "promoted"
AUDIT_DIR = ROOT / "steps" / "corpus_results" / "figure1" / "research_followup_20260504"
PROMOTED_CSV = PROMOTED / "forrt_reversals_conservative_rows__promoted_pairs.csv"
AUDIT_TSV = AUDIT_DIR / "forrt-reversals-conservative-promoted-audit.tsv"


def clean_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"[\t\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except Exception:
        return str(path)


def extract_entry_text(label: str) -> str:
    html = RAW_HTML.read_text(errors="ignore")
    pos = html.lower().find(f"<strong>{label.lower()}")
    if pos < 0:
        soup = BeautifulSoup(html, "html.parser")
        for candidate in soup.find_all("strong"):
            candidate_text = clean_text(candidate.get_text(" ", strip=True)).lower()
            if candidate_text.startswith(label.lower()):
                pos = html.lower().find(str(candidate).lower())
                break
    if pos < 0:
        raise ValueError(f"Could not find FORRT entry with label prefix: {label}")

    start = html.rfind("<li><p>", 0, pos)
    if start < 0:
        start = pos
    next_marker = html.find("</p></li><li><p><strong", pos + 1)
    if next_marker >= 0:
        entry_html = html[start : next_marker + len("</p></li>")]
    else:
        entry_html = html[start:]
    return clean_text(BeautifulSoup(entry_html, "html.parser").get_text(" ", strip=True))


def assert_contains(text: str, *needles: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise ValueError(f"FORRT source text missing expected support text: {missing}")


def build_rows() -> list[dict[str, Any]]:
    raw_file = rel(RAW_HTML)
    rows = [
        {
            "entry_label": "Door-in-the-face effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_door_in_the_face_genschow_2021",
            "original_title": "Reciprocal concessions procedure for inducing compliance: The door-in-the-face technique",
            "replication_title": "Genschow et al. 2021 door-in-the-face replication and critique",
            "original_doi": "10.1037/h0076284",
            "replication_doi": "10.1037/pspa0000261",
            "outcome": "Door-in-the-face request-size manipulation and compliance",
            "D_original": 0.47,
            "N_original": 72.0,
            "D_replication": 0.40,
            "N_replication": 391.0,
            "match_author": "forrt_door_in_the_face_cialdini_genschow",
            "required_source_fragments": [
                "n=72",
                "Genschow et al. 2021",
                "n=391",
                "Original effect size: OR= 2.36 ( d = .47).",
                "Replication effect size: Genschow et al.: OR= 2.082 ( d = .40).",
            ],
            "d_n_transformation_note": "FORRT reports odds ratios and d-equivalent values; Figure 1 stores the reported nonnegative d magnitudes. N values are copied from the same FORRT entry.",
        },
        {
            "entry_label": "Left-cradling bias",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_left_cradling_bias_packheiser_2019",
            "original_title": "Handedness as a major determinant of functional cradling bias",
            "replication_title": "Handedness and sex effects on lateral biases in human cradling: Three meta-analyses",
            "original_doi": "10.1080/13576500500513565",
            "replication_doi": "10.1016/j.neubiorev.2019.06.035",
            "outcome": "Left-cradling bias / child cradling lateralization",
            "D_original": 1.06,
            "N_original": 765.0,
            "D_replication": 0.34,
            "N_replication": 6799.0,
            "match_author": "forrt_left_cradling_bias_van_der_meer_packheiser",
            "required_source_fragments": [
                "n=765",
                "Packheiser et al. 2019",
                "n=6799",
                "Original effect size: d = 1.06.",
                "Replication effect size: Packheiser et al.: d = 0.34.",
            ],
            "d_n_transformation_note": "FORRT reports source d values directly; the replication is a larger meta-analytic follow-up. Figure 1 stores nonnegative d magnitudes.",
        },
        {
            "entry_label": "Handedness differences - schizophrenia",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_handedness_schizophrenia_sommer_2001",
            "original_title": "Imbalance of hemispheric functions in the major psychoses: A study of handedness in the People's Republic of China",
            "replication_title": "Handedness, language lateralisation and anatomical asymmetry in schizophrenia",
            "original_doi": "10.1016/0006-3223(85)90216-1",
            "replication_doi": "10.1192/bjp.178.4.344",
            "outcome": "Non-right-handedness in schizophrenia versus healthy controls",
            "D_original": 0.59,
            "N_original": 657.0,
            "D_replication": 0.26,
            "N_replication": 5467.0,
            "match_author": "forrt_handedness_schizophrenia_shan_ming_sommer",
            "required_source_fragments": [
                "n=225 schizophrenics and 432 controls",
                "Sommer et al. 2001",
                "n=5467",
                "Original effect size: d = 0.59.",
                "Replication effect size: Sommer et al.: d = 0.26.",
            ],
            "d_n_transformation_note": "FORRT reports d values directly. The promoted original N sums the FORRT group-size text, 225 schizophrenia cases plus 432 controls = 657.",
        },
        {
            "entry_label": "Age of acquisition influence on lexical retrieval",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_age_of_acquisition_written_word_naming_catling_2020",
            "original_title": "Effects of consistency and age of acquisition on reading and spelling among developing readers",
            "replication_title": "The hunt for the age of acquisition effect: It's in the links!",
            "original_doi": "10.1007/s11145-005-2032-6",
            "replication_doi": "10.1016/j.actpsy.2020.103138",
            "outcome": "Age-of-acquisition effect in written word naming",
            "D_original": 0.50,
            "N_original": 40.0,
            "D_replication": 0.38,
            "N_replication": 48.0,
            "match_author": "forrt_age_of_acquisition_weekes_catling",
            "required_source_fragments": [
                "Experiment 2: n = 40",
                "Catling and Elsherif 2020",
                "Experiment 4b: n = 48",
                "Original effect size: d = 0.50",
                "Replication effect size: Catling and Elsherif: Experiment 4b: d = 0.38",
            ],
            "d_n_transformation_note": "FORRT reports both d values as calculated from reported t statistics using its linked conversion route. Figure 1 stores the nonnegative d magnitudes.",
        },
        {
            "entry_label": "Handedness differences - cognitive ability",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_handedness_cognitive_ability_somers_2015",
            "original_title": "Possible Basis for the Evolution of Lateral Specialization of the Human Brain",
            "replication_title": "Somers et al. 2015 handedness and cognitive ability meta-analysis",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Left- versus right-handedness difference in spatial ability",
            "D_original": 1.42,
            "N_original": 25.0,
            "D_replication": 0.14,
            "N_replication": 218351.0,
            "match_author": "forrt_handedness_cognitive_ability_levy_somers",
            "required_source_fragments": [
                "Left handers have a supposed deficit in spatial ability.",
                "n=25",
                "Somers et al. 2015",
                "n = 218,351",
                "Original effect size: d = 1.42.",
                "Somers et al.: g = 0.14",
            ],
            "d_n_transformation_note": "FORRT reports the original d and larger meta-analytic g directly. Figure 1 stores both as nonnegative standardized effect magnitudes; the FORRT status is mixed and the sensitivity-analysis caveat is preserved in the source text.",
        },
        {
            "entry_label": "Sex differences in implicit maths attitudes",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_implicit_maths_attitudes_klein_2014",
            "original_title": "Math = male, me = female, therefore math != me",
            "replication_title": "Klein et al. 2014 implicit math attitudes replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Sex differences in implicit math and science attitudes",
            "D_original": 1.01,
            "N_original": 170.0,
            "D_replication": 0.56,
            "N_replication": 5842.0,
            "match_author": "forrt_implicit_maths_attitudes_nosek_klein",
            "required_source_fragments": [
                "Sex differences in implicit maths attitudes",
                "n = 170",
                "Klein et al. 2014",
                "n=5842",
                "Original effect size: d =1.01",
                "Replication effect size: Klein et al.: d =0.56",
            ],
            "d_n_transformation_note": "FORRT reports both d values directly for the same implicit math-attitudes claim. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Warmer-hearts-warmer-room effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_warmer_hearts_warmer_room_ebersole_2016",
            "original_title": "Warmer hearts, warmer rooms: How positive communal traits increase estimates of ambient temperature",
            "replication_title": "Ebersole et al. 2016 warmer-hearts-warmer-room replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Positive communal trait priming and estimated ambient room temperature",
            "D_original": 0.86,
            "N_original": 80.0,
            "D_replication": 0.06,
            "N_replication": 3119.0,
            "match_author": "forrt_warmer_hearts_warmer_room_szymkow_ebersole",
            "required_source_fragments": [
                "Warmer-hearts-warmer-room effect",
                "Experiment 1: N = 80",
                "Ebersole et al. 2016",
                "n = 3,119",
                "Original effect size: d = .86",
                "Replication effect size: Ebersole et al.: d = .06",
            ],
            "d_n_transformation_note": "FORRT reports the Ebersole-coded original d and larger replication d directly. Figure 1 uses the first original experiment N tied to the reported original d and stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Phonological working memory impairment in dyslexic adults",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_phonological_working_memory_dyslexia_elsherif_2021",
            "original_title": "Pseudoword repetition ability in learning-disabled children",
            "replication_title": "Elsherif et al. 2021 dyslexic adults phonological working memory follow-up",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Nonword/pseudoword repetition phonological working-memory deficit in dyslexia",
            "D_original": 0.97,
            "N_original": 44.0,
            "D_replication": 1.54,
            "N_replication": 134.0,
            "match_author": "forrt_phonological_working_memory_taylor_elsherif",
            "required_source_fragments": [
                "Phonological working memory impairment in dyslexic adults",
                "neurotypical: n 1 = 20, dyslexic: n 2 = 24",
                "Elsherif et al. 2021",
                "NT: n = 84, AWD: n = 50",
                "Original effect size: d = 0.97",
                "Replication effect size: Elsherif et al.: d = 1.54",
            ],
            "d_n_transformation_note": "FORRT reports both d values directly or via its linked t-statistic conversion. The promoted original N sums neurotypical and dyslexic groups, 20 + 24 = 44; the promoted replication N sums the matched NT and adults-with-dyslexia groups, 84 + 50 = 134, excluding the non-focal AWS group.",
        },
        {
            "entry_label": "Social comparison",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_social_comparison_fat_talk_pollet_2021",
            "original_title": "Who is most likely to fat talk? A social comparison perspective",
            "replication_title": "Pollet et al. 2021 social comparison and fat talk replication/meta-analysis",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Body dissatisfaction x social comparison interaction on fat talk",
            "D_original": 0.36,
            "N_original": 143.0,
            "D_replication": 0.02,
            "N_replication": 560.0,
            "match_author": "forrt_social_comparison_fat_talk_corning_pollet",
            "required_source_fragments": [
                "No robust evidence for an interaction effect between body dissatisfaction and social comparison on fat talk.",
                "n = 143",
                "Pollet et al. 2021",
                "n = 189 and n = 371",
                "g = 0.36.",
                "g (meta-analysis)=0.02",
            ],
            "d_n_transformation_note": "FORRT reports the original Hedges g and the Pollet et al. meta-analytic Hedges g. Figure 1 stores nonnegative standardized effect magnitudes. The promoted replication N sums the two replication samples named in the same FORRT entry, 189 + 371 = 560.",
        },
        {
            "entry_label": "Big brother effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_big_brother_watched_eyes_northover_2017",
            "original_title": "Cues of being watched enhance co-operation in a real-world setting",
            "replication_title": "Northover et al. 2017 watched-eyes cooperation meta-analysis",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Watched-eye cues and cooperative behavior",
            "D_original": 1.948,
            "N_original": 48.0,
            "D_replication": 0.13,
            "N_replication": 20000.0,
            "match_author": "forrt_big_brother_bateson_northover",
            "required_source_fragments": [
                "Being watched makes someone more likely to cooperate.",
                "N=48",
                "Northover et al. (2017",
                "meta-analysis: n=20000",
                "Original effect size: _d _= 1.948.",
                "2nd meta-analysis: g =0.13",
            ],
            "d_n_transformation_note": "FORRT reports the original d and Northover et al. second meta-analysis g directly. Figure 1 stores both as nonnegative standardized effect magnitudes and uses the second meta-analysis N reported in the same entry.",
        },
        {
            "entry_label": "Reference framing",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_reference_framing_ruggeri_2020",
            "original_title": "Prospect Theory: An analysis of decisions under risk",
            "replication_title": "Ruggeri et al. 2020 multinational reference-framing replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Gain/loss reference framing in risky choice problems",
            "D_original": 1.3700523051231532,
            "N_original": 136.0,
            "D_replication": 0.8655863658122135,
            "N_replication": 4098.0,
            "match_author": "forrt_reference_framing_kahneman_tversky_ruggeri",
            "required_source_fragments": [
                "Risk preferences change depending on whether a choice is presented in terms of gains or losses",
                "Problem 12 n = 68, Problem 13 n = 68",
                "Ruggeri et al. 2020",
                "n=4,098",
                "Original effect size: log OR = -2.485",
                "Replication effect size: log OR = -1.570",
            ],
            "d_n_transformation_note": "FORRT reports original and replication log odds ratios. Figure 1 converts each absolute log OR to d-equivalent as abs(logOR) * sqrt(3) / pi. The promoted original N sums the two source problem samples, 68 + 68 = 136.",
        },
        {
            "entry_label": "Overweighting small probabilities",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_overweighting_small_probabilities_ruggeri_2020",
            "original_title": "Prospect Theory: An analysis of decisions under risk",
            "replication_title": "Ruggeri et al. 2020 multinational small-probability-weighting replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Overweighting or overreaction to changes from zero to very small probabilities",
            "D_original": 0.6781345413688042,
            "N_original": 66.0,
            "D_replication": 1.5326943292725819,
            "N_replication": 4098.0,
            "match_author": "forrt_overweighting_small_probabilities_kahneman_tversky_ruggeri",
            "required_source_fragments": [
                "People tend to overweight/overreact to changes in probability from 0 to very small probabilities",
                "n=66",
                "Ruggeri et al. 2020",
                "n=4,098",
                "Original effect size: Log OR= -1.23.",
                "Replication effect size: Ruggeri et al.: Log OR= -2.78",
            ],
            "d_n_transformation_note": "FORRT reports original and replication log odds ratios. Figure 1 converts each absolute log OR to d-equivalent as abs(logOR) * sqrt(3) / pi.",
        },
        {
            "entry_label": "Certainty effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_certainty_effect_ruggeri_2020",
            "original_title": "Prospect Theory: An analysis of decisions under risk",
            "replication_title": "Ruggeri et al. 2020 multinational certainty-effect replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Certainty effect item 1 versus item 2 contrast",
            "D_original": 0.7498072977736373,
            "N_original": 66.0,
            "D_replication": 0.9482857001254824,
            "N_replication": 4098.0,
            "match_author": "forrt_certainty_effect_kahneman_tversky_ruggeri",
            "required_source_fragments": [
                "The tendency to overweight the importance of an increase from 99% to 100% probability",
                "n=66",
                "Ruggeri et al. 2020",
                "n=4,098",
                "Original effect size: Log OR = -1.36",
                "Replication effect size: Ruggeri et al.: Log OR = -1.72",
            ],
            "d_n_transformation_note": "FORRT reports original and replication log odds ratios. Figure 1 converts each absolute log OR to d-equivalent as abs(logOR) * sqrt(3) / pi.",
        },
        {
            "entry_label": "Magnitude effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_magnitude_effect_ruggeri_2020",
            "original_title": "Prospect Theory: An analysis of decisions under risk",
            "replication_title": "Ruggeri et al. 2020 multinational magnitude-effect replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Magnitude perception / relative value scaling in risky choice problem 14",
            "D_original": 1.1258136044512994,
            "N_original": 72.0,
            "D_replication": 1.108171079797802,
            "N_replication": 4098.0,
            "match_author": "forrt_magnitude_effect_kahneman_tversky_ruggeri",
            "required_source_fragments": [
                "Problem 14 n = 72",
                "multinational replication study n=4,098",
                "Original effect size: log OR = -2.042",
                "Replication effect size: Ruggeri et al.: log OR = -2.010",
            ],
            "d_n_transformation_note": "FORRT reports original and replication log odds ratios. Figure 1 converts each absolute log OR to d-equivalent as abs(logOR) * sqrt(3) / pi.",
        },
        {
            "entry_label": "Isolation effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_isolation_effect_ruggeri_2020",
            "original_title": "Prospect Theory: An analysis of decisions under risk",
            "replication_title": "Ruggeri et al. 2020 multinational isolation-effect replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Isolation effect / differential weighting of distinctive choice features",
            "D_original": 1.0458709146151397,
            "N_original": 165.0,
            "D_replication": 0.9389131089033119,
            "N_replication": 4098.0,
            "match_author": "forrt_isolation_effect_kahneman_tversky_ruggeri",
            "required_source_fragments": [
                "Problem 4 n=95, Problem 11 n=70",
                "multinational replication study, n=4,098",
                "Original effect size: log OR = 1.897",
                "Replication effect size: Ruggeri et al.: log OR = 1.703",
            ],
            "d_n_transformation_note": "FORRT reports original and replication log odds ratios. Figure 1 converts each absolute log OR to d-equivalent as abs(logOR) * sqrt(3) / pi. The promoted original N sums the two source problem samples, 95 + 70 = 165.",
        },
        {
            "entry_label": "Foot-in-the-door effect",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_foot_in_the_door_gamian_wilk_dolinski_2019",
            "original_title": "Compliance without pressure: The foot-in-the-door technique",
            "replication_title": "Gamian-Wilk and Dolinski 2019 foot-in-the-door replications",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Small initial request increasing compliance with a larger request",
            "D_original": 2.16,
            "N_original": 156.0,
            "D_replication": 4.83,
            "N_replication": 240.0,
            "match_author": "forrt_foot_in_the_door_freedman_fraser_gamian_wilk_dolinski",
            "required_source_fragments": [
                "getting people to comply with a very small initial request increases the likelihood",
                "n=156",
                "Gamian-Wilk and Dolinski 2019",
                "n=60 in each of 4 replication studies; 240 total",
                "Original effect size: OR = 3.912; d = 2.16.",
                "OR = 8.76, d = 4.83 if aggregating across all 4 replications",
            ],
            "d_n_transformation_note": "FORRT reports the original and aggregate-replication d-equivalent values directly. Figure 1 stores nonnegative standardized effect magnitudes and uses the FORRT-preferred aggregate across all four replication studies.",
        },
        {
            "entry_label": "Content effect for cheater detection",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_cheater_detection_wason_van_lier_2013",
            "original_title": "The logic of social exchange: Has natural selection shaped how humans reason? Studies with the Wason selection task",
            "replication_title": "Van Lier, Revlin and De Neys 2013 cheater-detection Wason-task replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Cheater-detection content effect in the Wason selection task",
            "D_original": 1.0952168057789922,
            "N_original": 24.0,
            "D_replication": 0.77,
            "N_replication": 117.0,
            "match_author": "forrt_cheater_detection_cosmides_van_lier",
            "required_source_fragments": [
                "performance improvement on the Wason selection task if it involves cheater detection",
                "n=24",
                "Van Lier et al.2013",
                "n=117",
                "Original effect size: OR = 7.29",
                "Replication effect size: Van Lier, Revlin and De Neys: d =0.77.",
            ],
            "d_n_transformation_note": "FORRT reports the original odds ratio and replication d. Figure 1 converts the original OR to d-equivalent as abs(log(7.29)) * sqrt(3) / pi = 1.0952168057789922 and stores nonnegative magnitudes.",
        },
        {
            "entry_label": "Contagious yawning in dogs",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_contagious_yawning_dogs_madsen_persson_2012",
            "original_title": "Dogs catch human yawns",
            "replication_title": "Madsen and Persson 2012 contagious-yawning replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Yawning after observing a human yawn versus mouth-movement control",
            "D_original": 1.02,
            "N_original": 29.0,
            "D_replication": 0.61,
            "N_replication": 32.0,
            "match_author": "forrt_contagious_yawning_joly_mascheroni_madsen_persson",
            "required_source_fragments": [
                "Dogs have been shown to yawn more after observing a person yawn than after a control condition",
                "n = 29",
                "Madsen and Persson 2012",
                "n = 32",
                "Original effect size: d = 1.02",
                "Madsen and Persson: d = 0.61",
            ],
            "d_n_transformation_note": "FORRT reports the original and Madsen-Persson replication d values directly or as calculated d values. Figure 1 stores nonnegative standardized effect magnitudes and uses the only larger named replication in the entry.",
        },
        {
            "entry_label": "Temporal preferences in chimpanzees and bonobos",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_temporal_preferences_chimpanzees_bonobos_rosati_hare_2013",
            "original_title": "The evolutionary origins of human patience: temporal preferences in chimpanzees, bonobos, and human adults",
            "replication_title": "Rosati and Hare 2013 temporal-preferences follow-up",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Species difference in waiting for larger later rewards",
            "D_original": 1.89,
            "N_original": 10.0,
            "D_replication": 0.68,
            "N_replication": 38.0,
            "match_author": "forrt_temporal_preferences_rosati_rosati_hare",
            "required_source_fragments": [
                "wait longer than bonobos",
                "n = 5 (chimpanzees), n = 5 (bonobos)",
                "Rosati and Hare 2013",
                "n = 23 (chimpanzees), n = 15 (bonobos)",
                "Original effect size: d = 1.89",
                "Replication effect size: Rosati and Hare: d = 0.68",
            ],
            "d_n_transformation_note": "FORRT reports calculated original and replication d values. The promoted original N sums 5 + 5 = 10; the promoted replication N sums 23 + 15 = 38. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Risk preferences in chimpanzees and bonobos",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_risk_preferences_chimpanzees_bonobos_rosati_hare_2013",
            "original_title": "A fruit in the hand or two in the bush? Divergent risk preferences in chimpanzees and bonobos",
            "replication_title": "Rosati and Hare 2013 risky-choice follow-up",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Species difference in choosing risky versus guaranteed rewards",
            "D_original": 4.80,
            "N_original": 10.0,
            "D_replication": 1.26,
            "N_replication": 37.0,
            "match_author": "forrt_risk_preferences_heilbronner_rosati_hare",
            "required_source_fragments": [
                "choose risky options more than bonobos",
                "n = 5 (chimpanzees), n = 5 (bonobos)",
                "Rosati and Hare 2013",
                "n = 24 (chimpanzees), n = 13 (bonobos)",
                "Original effect size: d = 4.80",
                "Replication effect size: Rosati and Hare: d = 1.26",
            ],
            "d_n_transformation_note": "FORRT reports calculated original and replication d values. The promoted original N sums 5 + 5 = 10; the promoted replication N sums 24 + 13 = 37. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Age of acquisition influence on face recognition",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_age_of_acquisition_face_recognition_lima_2022",
            "original_title": "Age of acquisition in face categorisation: Is there an instance-based account?",
            "replication_title": "Lima et al. 2022 age-of-acquisition face-recognition follow-up",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Correlation of face age-of-acquisition with recognition speed or accuracy",
            "D_original": 1.1547005383792517,
            "N_original": 9.0,
            "D_replication": 0.3241763593892431,
            "N_replication": 180.0,
            "match_author": "forrt_age_of_acquisition_face_recognition_lewis_lima",
            "required_source_fragments": [
                "Early-acquired faces are recognised more quickly and accurately",
                "n = 9",
                "Lima et al. 2022",
                "n = 180",
                "Original effect size: r = -0.50.",
                "Replication effect size: Lima et al.: r = -0.16.",
            ],
            "d_n_transformation_note": "FORRT reports original and replication correlations. Figure 1 converts each to a d-equivalent magnitude using abs(2*r/sqrt(1-r^2)).",
        },
        {
            "entry_label": "Eye narrowing in felines",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_eye_narrowing_humphreys_2020_replication",
            "original_title": "The role of cat eye narrowing movements in cat-human communication",
            "replication_title": "Humphreys et al. 2020 eye-narrowing replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Slow-blink / eye-narrowing response following human slow blink",
            "D_original": 0.56,
            "N_original": 21.0,
            "D_replication": 0.71,
            "N_replication": 24.0,
            "match_author": "forrt_eye_narrowing_humphreys_replication",
            "required_source_fragments": [
                "more likely to narrow their eyes following a slow blink",
                "experiment 1: n = 21",
                "Humphreys et al. 2020b",
                "n = 24",
                "Original effect size: Experiment 1: d = 0.56",
                "Replication effect size: Humphreys et al.: slow blinking versus control trials: d = 0.71",
            ],
            "d_n_transformation_note": "FORRT reports the original experiment-1 d and the larger replication slow-blinking versus control d directly. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Mate guarding",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_mate_guarding_tunka_yanar_2020",
            "original_title": "Conspicuous Consumption, Relationships, and Rivals: Women's Luxury Products as Signals to Other Women",
            "replication_title": "Tunka and Yanar 2020 direct mate-guarding replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Luxury possessions as a signal of partner devotion",
            "D_original": 0.24,
            "N_original": 69.0,
            "D_replication": 0.27,
            "N_replication": 255.0,
            "match_author": "forrt_mate_guarding_wang_griskevicius_tunka_yanar",
            "required_source_fragments": [
                "Women use conspicuous luxurious goods to deter female rivals",
                "Study 1: N=69",
                "direct replications Study 2, N=255",
                "Original effect size: d =0.24.",
                "Study 2: a reversal is observed",
                "d =-0.27",
            ],
            "d_n_transformation_note": "FORRT reports the original d and the direct-replication Study 2 d directly. Figure 1 stores the nonnegative magnitude of the signed replication reversal.",
        },
        {
            "entry_label": "Product size and status",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_product_size_status_small_large_tunca_2022",
            "original_title": "Super size me: product size as a signal of status",
            "replication_title": "Tunca et al. 2022 direct product-size/status replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Small versus large product-size choice among low-power participants",
            "D_original": 1.49,
            "N_original": 183.0,
            "D_replication": 0.09,
            "N_replication": 415.0,
            "match_author": "forrt_product_size_status_dubois_tunca_small_large",
            "required_source_fragments": [
                "People who are low in power choose supersized foods and drinks to signal status",
                "Study 1: n = 183",
                "direct replication of study 1 of Dubois et al. 2012; n=415",
                "small vs. large product size: d =1.49",
                "small vs. large product size: d = 0.09",
            ],
            "d_n_transformation_note": "FORRT reports the matched Study 1 original and direct-replication d values directly. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Product size and status",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_product_size_status_medium_large_tunca_2022",
            "original_title": "Super size me: product size as a signal of status",
            "replication_title": "Tunca et al. 2022 direct product-size/status replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Medium versus large product-size choice among low-power participants",
            "D_original": 0.89,
            "N_original": 183.0,
            "D_replication": 0.11,
            "N_replication": 415.0,
            "match_author": "forrt_product_size_status_dubois_tunca_medium_large",
            "required_source_fragments": [
                "People who are low in power choose supersized foods and drinks to signal status",
                "Study 1: n = 183",
                "direct replication of study 1 of Dubois et al. 2012; n=415",
                "medium vs. large product size: d =0.89",
                "medium vs. large product size: d = 0.11",
            ],
            "d_n_transformation_note": "FORRT reports the matched Study 1 original and direct-replication d values directly. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Product size and status",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_product_size_status_small_medium_tunca_2022",
            "original_title": "Super size me: product size as a signal of status",
            "replication_title": "Tunca et al. 2022 direct product-size/status replication",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Small versus medium product-size choice among low-power participants",
            "D_original": 0.62,
            "N_original": 183.0,
            "D_replication": 0.01,
            "N_replication": 415.0,
            "match_author": "forrt_product_size_status_dubois_tunca_small_medium",
            "required_source_fragments": [
                "People who are low in power choose supersized foods and drinks to signal status",
                "Study 1: n = 183",
                "direct replication of study 1 of Dubois et al. 2012; n=415",
                "small vs. medium product size: d =0.62",
                "small vs. medium: d =-0.01",
            ],
            "d_n_transformation_note": "FORRT reports the matched Study 1 original and direct-replication d values directly. Figure 1 stores the nonnegative magnitude of the signed replication value.",
        },
        {
            "entry_label": "Playboy Effect.",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_playboy_effect_sexual_attraction_balzarini_2017",
            "original_title": "Influence of Popular Erotica on Judgments of Strangers and Mates",
            "replication_title": "Balzarini et al. 2017 playboy-effect replication meta-analysis",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Erotica exposure and men's sexual attraction to their partner",
            "D_original": 1.05,
            "N_original": 30.0,
            "D_replication": 0.02,
            "N_replication": 445.0,
            "match_author": "forrt_playboy_effect_kenrick_balzarini_sexual_attraction",
            "required_source_fragments": [
                "Men exposed to erotic images of the opposite-sex",
                "Experiment 2: n_ _= 30",
                "meta-analysis n = 445",
                "Reduced sexual attraction to partner ( d = 1.05)",
                "Sexual attraction to partner:",
                "Meta-analysis: d = 0.02 [-0.21, 0.24]",
            ],
            "d_n_transformation_note": "FORRT reports male-participant original and replication meta-analytic d values directly. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Playboy Effect.",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_playboy_effect_love_for_partner_balzarini_2017",
            "original_title": "Influence of Popular Erotica on Judgments of Strangers and Mates",
            "replication_title": "Balzarini et al. 2017 playboy-effect replication meta-analysis",
            "original_doi": "",
            "replication_doi": "",
            "outcome": "Erotica exposure and men's love for their partner",
            "D_original": 0.77,
            "N_original": 30.0,
            "D_replication": 0.02,
            "N_replication": 445.0,
            "match_author": "forrt_playboy_effect_kenrick_balzarini_love_for_partner",
            "required_source_fragments": [
                "Men exposed to erotic images of the opposite-sex",
                "Experiment 2: n_ _= 30",
                "meta-analysis n = 445",
                "reduced love for partner ( d = 0.77)",
                "Love for partner:",
                "Meta-analysis: d = 0.02 [-0.22, 0.26]",
            ],
            "d_n_transformation_note": "FORRT reports male-participant original and replication meta-analytic d values directly. Figure 1 stores nonnegative standardized effect magnitudes.",
        },
        {
            "entry_label": "Mutual exclusivity bias",
            "source_dataset": "FORRT Reversals database conservative rows",
            "project": "Other direct replications",
            "pair_id": "forrt_mutual_exclusivity_lewis_2020",
            "original_title": "Children's use of mutual exclusivity to constrain the meanings of words",
            "replication_title": "The role of developmental change and linguistic experience in the mutual exclusivity effect",
            "original_doi": "10.1016/0010-0285(88)90017-5",
            "replication_doi": "10.1016/j.cognition.2020.104191",
            "outcome": "Mutual-exclusivity forced-choice novel-label bias",
            "D_original": 1.688,
            "N_original": 20.0,
            "D_replication": 1.27,
            "N_replication": 2505.0,
            "match_author": "forrt_mutual_exclusivity_markman_wachtel_lewis",
            "extra_source_files": [
                CROSSREF_DIR / "crossref_mutual_exclusivity_markman_wachtel_1988.json",
                CROSSREF_DIR / "pubmed_lewis_mutual_exclusivity_2020_32143015.xml",
                CROSSREF_DIR / "doi_10_1016_j_cognition_2020_104191.html",
            ],
            "required_source_fragments": [
                "Study 1: n=20",
                "Lewis et al. 2020",
                "meta-analysis, n=2505",
                "Original effect size: g =1.688 [0.655, 2.720].",
                "Replication effect size: Lewis et al.: d =1.27 [0.99, 1.55].",
            ],
            "d_n_transformation_note": "FORRT reports the original Hedges g and larger meta-analytic d directly. Figure 1 stores both as nonnegative standardized effect magnitudes and records the metric labels in the verbatim support text.",
        },
    ]

    out: list[dict[str, Any]] = []
    for row in rows:
        source_text = extract_entry_text(row["entry_label"])
        assert_contains(source_text, *row.pop("required_source_fragments"))
        source_files = [RAW_HTML, *row.pop("extra_source_files", [])]
        source_files_text = " ; ".join(rel(Path(path)) for path in source_files)
        out.append(
            {
                **row,
                "raw_file": source_files_text,
                "n_source_file": source_files_text,
                "verbatim_source_row_text": source_text,
                "verbatim_effect_text_original": source_text,
                "verbatim_effect_text_replication": source_text,
                "verbatim_n_text_original": source_text,
                "verbatim_n_text_replication": source_text,
            }
        )
    return out


def main() -> None:
    if not RAW_HTML.exists():
        raise FileNotFoundError(RAW_HTML)
    PROMOTED.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    out = pd.DataFrame(build_rows())
    promoted_cols = [
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
        "n_source_file",
        "verbatim_n_text_original",
        "verbatim_n_text_replication",
        "verbatim_effect_text_original",
        "verbatim_effect_text_replication",
        "d_n_transformation_note",
        "match_author",
    ]
    out[promoted_cols].to_csv(PROMOTED_CSV, index=False)
    out.to_csv(AUDIT_TSV, sep="\t", index=False)
    print(f"Wrote promoted rows: {len(out)}")
    print(f"Wrote file: {PROMOTED_CSV}")
    print(f"Wrote audit: {AUDIT_TSV}")


if __name__ == "__main__":
    main()
