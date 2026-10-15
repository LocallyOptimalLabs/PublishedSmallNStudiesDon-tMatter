# Figure 1 pair invariant check

- Input rows: 2,695
- Included rows under current D/N rule: 2,026
- Critical violations: 0
- Warnings: 116
- Duplicate/fan-out review groups: 11
- Source-evidence gaps are critical: no
- Batch source filters: (none)

## Check Counts

| Severity | Check | Rows |
|---|---:|---:|
| warning | included_missing_source_artifact_sha256 | 94 |
| warning | included_source_artifact_url_only | 11 |
| warning | many_rows_for_same_source_pair | 11 |

## Top Included Sources

| Source dataset | Included rows |
|---|---:|
| FReD filtered pair table | 702 |
| SCORE analyst join | 172 |
| LOOPR coding workbook | 104 |
| Individual replication paper value scan | 78 |
| RPP canonical OSF csv | 63 |
| REPEAT Supplementary Data 6 outcomes and sample sizes | 60 |
| Metascience Observatory FReD API Soto LOPPRP rows | 60 |
| Metascience Observatory FReD API validated blank-tag rows | 46 |
| Metascience Observatory FReD API Soto LOPPRP extension rows | 44 |
| Sensory marketing article Table 5 and OSF workbooks | 38 |
| Boyce student replication corpus | 36 |
| Metascience Observatory FReD API SRP rows | 36 |
| Coppock 2019 generalizability corpus | 35 |
| RPCB | 33 |
| Kerschbaumer 2020 rheumatology phase II/III | 32 |
| Communication privacy SEM paths | 30 |
| FORRT Reversals database conservative rows | 28 |
| Many Labs 2 public join | 28 |
| EPRP complete data | 27 |
| Decision-market pair table | 26 |
| BRI primary t experiment table | 21 |
| Many Labs 5 overarching analyses | 20 |
| FReD archive rescue high-precision rows | 19 |
| ReplicationSuccess SSRP.rda | 18 |
| Transparent Replications mirrored report tables | 18 |
| 251 Rescue parsed data | 17 |
| Sports science supplemental outcomes table | 16 |
| Experimental asset-market replication appendix tables | 14 |
| ReplicationSuccess RProjects.rda | 11 |
| Altmejd harmonized Many Labs 1 | 10 |
| Pipeline supplement + packet data | 10 |
| Altmejd harmonized Many Labs 3 | 10 |
| Metascience Observatory FReD API RSESR extension rows | 9 |
| Metascience Observatory FReD API miscellaneous validated rows | 9 |
| Awesome replicability paired raw csvs | 9 |
| Public-admin blame Wiley table reconstruction | 9 |
| Clinical published replication workbook | 7 |
| EQIPD stagewise open-field lab contrasts | 7 |
| EERP 2016 supplement (manual) | 7 |
| Metascience Observatory FReD API RSESR rows | 6 |

## Output Artifacts

- Violations and warnings: `steps/corpus_results/figure1/invariant_checks/current_full_goal3000_20260508/figure1-pair-invariant-violations.tsv`
- Duplicate/fan-out review groups: `steps/corpus_results/figure1/invariant_checks/current_full_goal3000_20260508/figure1-pair-duplicate-fanout-review.tsv`
- Summary: `steps/corpus_results/figure1/invariant_checks/current_full_goal3000_20260508/figure1-pair-invariant-summary.md`
