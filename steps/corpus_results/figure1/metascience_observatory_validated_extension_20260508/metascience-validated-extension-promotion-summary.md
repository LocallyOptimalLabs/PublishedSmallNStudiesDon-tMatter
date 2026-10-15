# Metascience Observatory validated extension promotion

- Source API mirror: `data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json`
- Source SHA-256: `34547aaf4d5b25183c4783bc299c063a2cb13dde0dcaeef8188db67d339e4880`
- Promoted rows: 109
- Promoted CSV: `data/derived/replication_pairs/harvest/promoted/metascience_observatory_validated_extension__promoted_pairs.csv`
- Audit TSV: `steps/corpus_results/figure1/metascience_observatory_validated_extension_20260508/metascience-validated-extension-promotion-audit.tsv`

## Promotion Gate

Rows are promoted only when they are validated, direct/close, non-CurateScience, DOI-backed on both sides, have finite normalized r and N fields, pass the current Figure 1 D/N gate, and are not exact numeric duplicates already represented in the root table. Untagged rows with known integrated replication-project DOIs are held.

## Promoted Sources

| source_dataset                                              |   rows |
|:------------------------------------------------------------|-------:|
| Metascience Observatory FReD API validated blank-tag rows   |     54 |
| Metascience Observatory FReD API Soto LOPPRP extension rows |     44 |
| Metascience Observatory FReD API RSESR extension rows       |      9 |
| Metascience Observatory FReD API SPRRR extension rows       |      2 |

## Status Counts

| status                                                 |   rows |
|:-------------------------------------------------------|-------:|
| held_not_validated_yes                                 |   5230 |
| held_not_in_allowed_source_family                      |   1316 |
| held_missing_numeric_r_or_n                            |    416 |
| held_existing_numeric_duplicate                        |    214 |
| promoted                                               |    109 |
| held_curatescience_mapping_noise                       |     68 |
| held_failed_current_dn_gate                            |     67 |
| held_missing_doi_backed_pair_identity                  |     25 |
| held_blank_tag_known_integrated_project_duplicate_risk |      9 |
| held_missing_outcome_description                       |      2 |
