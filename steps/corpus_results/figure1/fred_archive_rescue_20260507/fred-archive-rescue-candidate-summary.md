# FReD Archive Rescue Candidate Scan - 2026-05-07

This is a duplicate-aware audit projection over the archived FReD workflow workbook. It does not promote rows.

- Source workbook: `data/raw/corpus_candidates/fred/freshness_check_2026-04-27/FReD_2.4.1.archive.xlsx`
- Source SHA-256: `b022e9cfcedc6b452d92efd6a9ed23506d558789a8ec87a3be4387e2523f8aa6`
- Audit TSV: `steps/corpus_results/figure1/fred_archive_rescue_20260507/fred-archive-rescue-candidate-scan.tsv`
- Archive rows scanned: 4659
- Complete validated rows with no explicit exclusion: 425
- Rows passing current Figure 1 mechanical D/N gates: 296

## Status Counts

| status                                 |   rows |
|:---------------------------------------|-------:|
| not_value_complete                     |   4234 |
| known_project_overlap_hold             |    167 |
| blocked_by_current_dn_gate             |    129 |
| duplicate_doi_pair_hold                |    110 |
| needs_manual_match_or_duplicate_review |     19 |

## Figure 1 Gate Rows by Source and Status

| source                 | archive_rescue_status                  |   rows |
|:-----------------------|:---------------------------------------|-------:|
| Boyce_etal2023         | known_project_overlap_hold             |     35 |
| FORRT                  | needs_manual_match_or_duplicate_review |      7 |
| Individual submissions | duplicate_doi_pair_hold                |     90 |
| Individual submissions | needs_manual_match_or_duplicate_review |      5 |
| OSC 2015               | known_project_overlap_hold             |     61 |
| OSF Registries         | duplicate_doi_pair_hold                |      5 |
| OSF Registries         | needs_manual_match_or_duplicate_review |      7 |
| SSRP                   | known_project_overlap_hold             |     18 |
| XPHI                   | known_project_overlap_hold             |      3 |
| datareplicada          | duplicate_doi_pair_hold                |     15 |
| openmkt                | known_project_overlap_hold             |     50 |

## Interpretation

The high-precision bucket requires a complete validated row, current D/N gates, no current root duplicate flag, and explicit `same_design == 1` plus `same_test == 1`. Other mechanically complete rows remain useful as a review queue, but they should not be bulk-promoted without row-level match and duplicate review.
