from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


SCAN_TSV = Path("steps/corpus_results/figure1/fred_archive_rescue_20260507/fred-archive-rescue-candidate-scan.tsv")
PROMOTED_CSV = Path(
    "data/derived/replication_pairs/harvest/promoted/fred_archive_rescue_high_precision__promoted_pairs.csv"
)
AUDIT_TSV = Path("steps/corpus_results/figure1/fred_archive_rescue_20260507/fred-archive-rescue-promoted-audit.tsv")


MANUAL_APPROVALS = {
    "soscisubmission18_1": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_2": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_3": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_4": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_5": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_6": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_7": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_8": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_9": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_10": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_11": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
    "soscisubmission18_12": (
        "Manual archive review: unique original/replication DOI pair absent from the root table; "
        "replication reference self-describes a direct replication and extension of Granow et al. (2018); "
        "FReD archive row has complete validated row-level N/r values and a matched outcome label."
    ),
}

MANUAL_APPROVALS.update(
    {
        "ms634_1": (
            "Manual archive review: no broad root-table match for the original/replication pair; "
            "OSF registry row names the original face-recognition bias claim and the replication source; "
            "FReD archive row has complete validated row-level N/r values and no exclusion flag."
        ),
        "soscisubmission6_1": (
            "Manual archive review: no broad root-table match for this original/replication pair; "
            "FReD archive row names the age-of-acquisition outcome and Catling/Elsherif replication source; "
            "row has complete validated row-level N/r values and no exclusion flag."
        ),
        "soscisubmission6_2": (
            "Manual archive review: no broad root-table match for this original/replication pair; "
            "FReD archive row names the age-of-acquisition outcome and Catling/Elsherif replication source; "
            "row has complete validated row-level N/r values and no exclusion flag."
        ),
        "soscisubmission8_1": (
            "Manual archive retention: this row was promoted from the high-precision bucket before the "
            "FReD rescue rows were integrated into the root table; subsequent duplicate-aware scans mark "
            "the DOI pair as present because of that existing promotion. FReD archive row has same_design=1, "
            "same_test=1, complete row-level N/r values, and no exclusion flag."
        ),
        "soscisubmission11_1": (
            "Manual archive review: no broad root-table match for the original/replication pair; "
            "FReD archive row names the laypeople-prediction replication source; "
            "row has complete validated row-level N/r values and no exclusion flag."
        ),
    }
)

MANUAL_APPROVALS.update(
    {
        "e9d3k_1": (
            "Manual archive review: no root match for the original/replication DOI pair; "
            "OSF registration title explicitly identifies this as a Cheung & Heine 2015 Study 3 "
            "replication and registration responses mark the replication successful; FReD archive row "
            "has complete validated row-level N/r values for Study 3 and no exclusion flag. Mirrored "
            "relation metadata under data/raw/replication_projects/fred_archive_rescue/"
            "e9d3k_cheung_heine_study3/."
        ),
    }
)

MANUAL_APPROVALS.update(
    {
        "h8vjx_1": (
            "Manual archive review: no root-table row for OSF registration H8VJX; the registration "
            "title explicitly identifies a Schnall et al. 2008 student replication and the archived "
            "OSF files include the hand-washing/no-hand-washing script, moral-judgment materials, "
            "SPSS syntax, output, and dataset. The original DOI is already represented elsewhere, "
            "but this is a distinct replication source object. FReD provides complete original N/r "
            "values; the replication D/N promoted here are recomputed from the mirrored OSF SPSS "
            "dataset using the supplied syntax because the FReD archive row's n_replication=47 does "
            "not match the analyzed SPSS dataset N=46."
        ),
    }
)

EXTRA_SUPPORT_FILES = {
    "e9d3k_1": [
        "data/raw/replication_projects/fred_archive_rescue/e9d3k_cheung_heine_study3/osf_registration_e9d3k.json",
        "data/raw/replication_projects/fred_archive_rescue/e9d3k_cheung_heine_study3/crossref_10.1177_0146167215610520.json",
        "data/raw/replication_projects/fred_archive_rescue/e9d3k_cheung_heine_study3/manifest_sha256.tsv",
    ],
    "h8vjx_1": [
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/osf_registration_h8vjx.json",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/crossref_10.1111_j.1467-9280.2008.02227.x.json",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/osf_archive_storage_children_api.json",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/osf_files/Script.docx",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/osf_files/Materials.docx",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/osf_files/Syntax1-replicatoin.sps",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/osf_files/data_set_1.sav",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/h8vjx_recompute_summary.tsv",
        "data/raw/replication_projects/fred_archive_rescue/h8vjx_schnall_cleanliness_student_replication/manifest_sha256.tsv",
    ],
}

CUSTOM_VALUE_OVERRIDES = {
    "h8vjx_1": {
        "D_replication": 0.7216357850017555,
        "N_replication": 46,
        "verbatim_n_text_replication": (
            "Mirrored OSF SPSS dataset data_set_1.sav contains 46 analyzed rows after applying the "
            "supplied Syntax1-replicatoin.sps composite; condition counts are 24 no-hand-washing "
            "and 22 hand-washing. FReD archive row h8vjx_1 separately records n_replication=47."
        ),
        "verbatim_effect_text_replication": (
            "Recomputed from mirrored OSF SPSS dataset data_set_1.sav using supplied syntax "
            "Composite=(dog + trolley + wallet + planecrash + resume + kitten)/6. Condition 0 "
            "mean=5.305555555555556, SD=0.5849702207143863, n=24; condition 1 mean=5.75, "
            "SD=0.6480535991503183, n=22; equal-variance t=2.44487188635196; Cohen's d for "
            "condition 1 minus condition 0 = 0.7216357850017555. FReD archive row h8vjx_1 "
            "records es_replication=-0.3345448 as Pearson r, equivalent to D magnitude=0.7099999027390547."
        ),
        "d_n_transformation_note": (
            "Original D uses FReD archive Pearson r to d as abs(2*r/sqrt(1-r^2)). Replication D is "
            "recomputed from the mirrored OSF SPSS dataset with the supplied syntax as the raw two-group "
            "standardized mean difference; Figure 1 stores the nonnegative magnitude."
        ),
    }
}


def slugify(value: object) -> str:
    text = "" if pd.isna(value) else str(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "row"


def first_nonempty(*values: object) -> str:
    for value in values:
        if pd.isna(value):
            continue
        text = str(value).strip()
        if text and text.lower() != "nan":
            return text
    return ""


def provenance_files(row: pd.Series) -> str:
    files = [str(row["source_artifact_local_path"])]
    files.extend(EXTRA_SUPPORT_FILES.get(str(row["rowid"]), []))
    return " ; ".join(files)


def support_text(row: pd.Series, side: str, field: str) -> str:
    side_label = "original" if side == "original" else "replication"
    if field == "n":
        n_col = "n_original" if side == "original" else "n_replication"
        study_col = "study_original" if side == "original" else "study_replication"
        ref_col = "ref_original" if side == "original" else "ref_replication"
        return (
            f"FReD archive Data row {row['rowid']}: {n_col}={row[n_col]}; "
            f"study_{side_label}={first_nonempty(row[study_col], 'not reported')}; "
            f"{ref_col}={row[ref_col]}"
        )
    es_col = "es_original" if side == "original" else "es_replication"
    d_col = "D_original_magnitude" if side == "original" else "D_replication_magnitude"
    return (
        f"FReD archive Data row {row['rowid']}: {es_col}={row[es_col]} as Pearson r; "
        f"converted Figure 1 D magnitude={row[d_col]}"
    )


def main() -> None:
    if not SCAN_TSV.exists():
        raise SystemExit(f"Missing scan file: {SCAN_TSV}. Run scripts/scan_fred_archive_rescue_candidates.py first.")

    scan = pd.read_csv(SCAN_TSV, sep="\t")
    rows = scan.loc[
        scan["archive_rescue_status"].eq("high_precision_candidate")
        | scan["rowid"].astype(str).isin(MANUAL_APPROVALS)
    ].copy()
    if rows.empty:
        out = pd.DataFrame(
            columns=[
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
        )
    else:
        records = []
        for _, row in rows.iterrows():
            rowid = str(row["rowid"])
            overrides = CUSTOM_VALUE_OVERRIDES.get(rowid, {})
            outcome = first_nonempty(row.get("effect"), row.get("description"), row.get("outcome"), row.get("rowid"))
            original_study = first_nonempty(row.get("study_original"))
            replication_study = first_nonempty(row.get("study_replication"))
            if original_study or replication_study:
                outcome = f"{outcome}; original study {original_study or 'not reported'}; replication study {replication_study or 'not reported'}"

            records.append(
                {
                    "source_dataset": "FReD archive rescue high-precision rows",
                    "project": "FReD archive rescue",
                    "pair_id": "fred_archive_" + slugify(row["rowid"]),
                    "original_title": row["ref_original"],
                    "replication_title": row["ref_replication"],
                    "original_doi": row["doi_original"],
                    "replication_doi": row["doi_replication"],
                    "outcome": outcome,
                    "D_original": row["D_original_magnitude"],
                    "N_original": row["n_original"],
                    "D_replication": overrides.get("D_replication", row["D_replication_magnitude"]),
                    "N_replication": overrides.get("N_replication", row["n_replication"]),
                    "raw_file": provenance_files(row),
                    "n_source_file": provenance_files(row),
                    "verbatim_n_text_original": support_text(row, "original", "n"),
                    "verbatim_n_text_replication": overrides.get(
                        "verbatim_n_text_replication", support_text(row, "replication", "n")
                    ),
                    "verbatim_effect_text_original": support_text(row, "original", "effect"),
                    "verbatim_effect_text_replication": overrides.get(
                        "verbatim_effect_text_replication", support_text(row, "replication", "effect")
                    ),
                    "d_n_transformation_note": overrides.get(
                        "d_n_transformation_note", row["d_n_transformation_note"]
                    ),
                    "match_author": "fred_archive_" + slugify(row["rowid"]),
                    "source_artifact_sha256": row["source_artifact_sha256"],
                    "archive_rescue_status": row["archive_rescue_status"],
                    "manual_approval_note": MANUAL_APPROVALS.get(str(row["rowid"]), ""),
                    "same_design": row["same_design"],
                    "same_test": row["same_test"],
                    "result": row["result"],
                    "notes_validation": row["notes_validation"],
                }
            )
        out = pd.DataFrame(records)

    PROMOTED_CSV.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_TSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(PROMOTED_CSV, index=False)
    out.to_csv(AUDIT_TSV, sep="\t", index=False)
    print(f"Wrote {len(out)} promoted rows: {PROMOTED_CSV}")
    print(f"Wrote audit: {AUDIT_TSV}")


if __name__ == "__main__":
    main()
