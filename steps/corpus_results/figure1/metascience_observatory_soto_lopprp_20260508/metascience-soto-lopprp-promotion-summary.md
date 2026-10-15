# Metascience Observatory Soto LOPPRP promotion

- Source API mirror: `data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json`
- Source SHA-256: `34547aaf4d5b25183c4783bc299c063a2cb13dde0dcaeef8188db67d339e4880`
- Candidate Soto rows: 121
- Promoted conservative new-title rows: 60
- Promoted CSV: `data/derived/replication_pairs/harvest/promoted/metascience_observatory_soto_lopprp__promoted_pairs.csv`
- Audit TSV: `steps/corpus_results/figure1/metascience_observatory_soto_lopprp_20260508/metascience-soto-lopprp-promotion-audit.tsv`

## Status Counts

| status                               |   rows |
|:-------------------------------------|-------:|
| promoted_conservative_new_soto_title |     60 |
| held_existing_soto_original_title    |     44 |
| held_failed_current_dn_gate          |     14 |
| held_missing_numeric_d_or_n_inputs   |      3 |

## Promotion Rule

Rows are promoted only when `validated == yes`, replication type is direct/close, both sides have finite normalized Pearson r and N, `N_replication > N_original`, both N are at least 10, the original title is not already represented by the current Soto/Life Outcomes rows, and source identity plus outcome text are present.
