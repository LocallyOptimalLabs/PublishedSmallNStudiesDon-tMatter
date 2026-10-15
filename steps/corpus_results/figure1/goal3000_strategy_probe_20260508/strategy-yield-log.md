# Goal 3000 Strategy Yield Log

## 2026-05-08T15:59:19Z - Ying/txt2stop Endpoint Rescue

- Strategy: continue structured Ying pilot/full-scale pair reconstruction after corpus/database bulk routes failed current 1:1 and value-evidence checks.
- Inputs checked: Rabbitt individual-paper blocker; Ying pair 051 txt2stop pilot/full-scale smoking cessation.
- Elapsed time: approximately 28 minutes for this sub-batch, including Rabbitt source retry, txt2stop PDF/PMC mirroring, endpoint audit, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_051_txt2stop_smoking_cessation`.
- Source evidence: mirrored pilot PDF/text, mirrored full-scale article PDF/text, mirrored PMC HTML, and Europe PMC JSON records under `data/raw/replication_projects/lead_harvest/ying_2023/`.
- Conversion: Chinn log(OR) to d for matched 6-month self-reported no-smoking-in-past-7-days endpoint; pilot from 15/97 vs 19/93, full-scale from 24.2% vs 18.3%.
- Rejection/hold reasons encountered: Rabbitt remains held because the original 1968 Experiment 2 N is not present in local value-bearing bytes or accessible DOI/abstract mirrors; txt2stop primary endpoints were not mixed because pilot and full-scale primary definitions differ.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,684 root rows, 2,015 D/N-included rows, 0 critical invariant violations for the 8 included Ying rows.
- Decision: expand Ying endpoint mining, but tighten to pairs with full value-bearing article/PMC/PDF text and exactly matched endpoint definitions. Expected rate is low one-by-one unless multiple abstracts expose the same endpoint cleanly.

## 2026-05-08T16:02:48Z - Ying/Oxytocin Matched Endpoint Rescue

- Strategy: continue Ying first-60 endpoint mining, prioritizing pairs where the pilot and full-scale papers explicitly share the same binary clinical endpoint.
- Inputs checked: Ying pair 055 oxytocin bolus-plus-infusion pilot and full-scale elective caesarean-section trial.
- Elapsed time: approximately 8 minutes after the txt2stop row, including ScienceDirect/Jina source mirroring, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_055_oxytocin_uterotonic`.
- Source evidence: Europe PMC JSON records plus mirrored ScienceDirect/Jina pilot page under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/oxytocin/`.
- Conversion: Chinn log(OR) to d for need for an additional uterotonic agent; pilot from reported 5% versus 11%, full-scale from reported adjusted OR 0.61.
- Rejection/hold reasons encountered: major obstetric haemorrhage was not added as a second row because it would double-count the same trial pair/outcome family; the single retained endpoint is the one with clear benefit in both pilot and full-scale reports.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,685 root rows, 2,016 D/N-included rows, 0 critical invariant violations for the 9 included Ying rows.
- Decision: expand nearby Ying clinical pairs with the same discipline, but keep one endpoint per pilot/full-scale pair unless the original source explicitly establishes independent primary contrasts.

## 2026-05-08T16:04:49Z - Ying/CHIPS Severe Hypertension Endpoint Rescue

- Strategy: continue Ying clinical endpoint mining using Europe PMC abstract records where both pilot and full-scale trials expose the same binary endpoint.
- Inputs checked: Ying pair 022 CHIPS pilot and full-scale less-tight versus tight hypertension control in pregnancy.
- Elapsed time: approximately 6 minutes after the oxytocin row.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_022_chips_severe_hypertension`.
- Source evidence: Europe PMC JSON records under `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/`.
- Conversion: Chinn log(OR) to d for severe hypertension; pilot from 38/66 versus 26/65, full-scale from 40.6% versus 27.5%.
- Rejection/hold reasons encountered: other CHIPS maternal/perinatal outcomes were not promoted from the same pair; primary endpoints differed across the pilot/full-scale articles, so this row is explicitly endpoint-specific.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,686 root rows, 2,017 D/N-included rows, 0 critical invariant violations for the 10 included Ying rows.
- Decision: continue mining first-60 Ying abstract pairs for matched binary endpoints; current narrowed strategy is yielding source-backed rows at a much better rate than isolated individual-paper N rescues.

## 2026-05-08T16:14:59Z - Ying/PITCHES Matched Itch Endpoint Rescue

- Strategy: continue Ying endpoint mining, but use open-access full-text XML where abstracts expose only part of the matched pilot/full-scale outcome.
- Inputs checked: Ying pair 052 ursodeoxycholic acid/PITCHES pilot and full-scale intrahepatic cholestasis of pregnancy trials; Ying pair 001 expressive-writing smoking cessation was reviewed and held because the exposed abstinence definitions/timepoints did not match cleanly.
- Elapsed time: approximately 10 minutes after the CHIPS row, including Europe PMC fullTextXML mirroring, endpoint audit, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_052_pitches_maternal_itch`.
- Source evidence: Europe PMC JSON records plus mirrored Europe PMC fullTextXML and parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/pitches/`.
- Conversion: CI-derived Hedges g for maternal worst-itch VAS; pilot from mean difference -16.2 mm, 95% CI -26.5 to -5.9, n=56/55; full-scale from adjusted mean difference -5.7 mm, 95% CI -9.7 to -1.7, model Ns 241/227.
- Rejection/hold reasons encountered: the full-scale perinatal primary composite was not mixed with the pilot itch primary endpoint; the row uses only the matched maternal itch endpoint.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,687 root rows, 2,018 D/N-included rows, 0 critical invariant violations for the 11 included Ying rows.
- Decision: expand the open-access fullTextXML rescue route for Ying pairs where abstracts show a plausible shared endpoint but withhold the exact larger-trial value.

## 2026-05-08T16:22:22Z - Ying 061-120 Abstract Cache Expansion

- Strategy: expand the high-yield Ying route beyond the first-60 cache by mirroring Europe PMC DOI records for pairs 061-120, then promote only pairs where both pilot and full-scale abstracts expose a same-outcome D route.
- Inputs checked: 120 DOI-side lookups for Ying pairs 061-120; 118 raw Europe PMC JSON files fetched, 2 sides had missing DOI in the roster. Detailed scan saved at `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/ying_epmc_abstract_scan_061_120.csv`.
- Elapsed time: approximately 7 minutes after the PITCHES row, including API mirroring, numeric screen, code patch, D/N regeneration, and invariant check.
- Included-row delta: +2 current Figure 1 D/N rows.
- New rows: `ying_2023_pair_068_connect_readmission`; `ying_2023_pair_070_chest_pain_choice_knowledge`.
- Source evidence: Europe PMC JSON records under `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/`.
- Conversion: CONNECT uses Chinn log(OR) from reported 6-month readmission percentages, 37% vs 47% in the pilot and 25.6% vs 27.9% in the full-scale trial. Chest Pain Choice uses CI-derived Hedges g from patient-knowledge mean differences, 0.67 (95% CI 0.34 to 1.0) in the pilot and 0.66 (95% CI 0.46 to 0.86) in the full-scale trial.
- Rejection/hold reasons encountered: several plausible pairs were held because the comparator changed, the endpoint changed, or the abstract exposed only feasibility/native results without enough exact value text; no secondary outcomes from the same pair were added as extra rows.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,689 root rows, 2,020 D/N-included rows, 0 critical invariant violations for the 13 included Ying rows.
- Decision: continue screening the 061-120 cache before expanding further; abstract-cache expansion is currently the fastest valid-row strategy because it amortizes source discovery over many known pilot/full-scale mappings.

## 2026-05-08T16:27:29Z - Ying/IBS Matched Primary Endpoint Rescue

- Strategy: continue screening the 061-120 Europe PMC cache, promoting only exact one-pair/one-endpoint rows and mirroring fullTextXML when available for source-side audit.
- Inputs checked: Ying pair 074 acupuncture for irritable bowel syndrome pilot and full-scale primary-care pragmatic trial.
- Elapsed time: approximately 5 minutes after the 061-120 cache expansion log, including fullTextXML mirroring, endpoint audit, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_074_acupuncture_ibs_sss`.
- Source evidence: Europe PMC JSON records plus mirrored Europe PMC fullTextXML and parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/ibs/`.
- Conversion: CI-derived Hedges g for the matched primary IBS Symptom Severity Score endpoint at 3 months; pilot from 138 points, 95% CI 66 to 210, one-to-two allocation 20/10 from N=30; full-scale from -27.43, 95% CI -48.66 to -6.21, n=116/117.
- Rejection/hold reasons encountered: responder-count and later follow-up outcomes from the same pair were not added as extra rows; the row stays at the primary 3-month IBS SSS endpoint to preserve 1:1 pair grain.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,690 root rows, 2,021 D/N-included rows, 0 critical invariant violations for the 14 included Ying rows.
- Decision: continue screening the 061-120 cache. The current route remains productive, but likely has limited remaining capacity because many cached pairs fail on changed comparator, changed endpoint, or abstract-only incomplete value text.

## 2026-05-08T16:40:35Z - Ying 121-248 Mirrored Full-Text Endpoint Batch

- Strategy: promote only already-mirrored Ying 121-248 candidate pairs with explicit pilot/full-scale relationship, one matched endpoint, value-bearing local source files, and a defensible D conversion; keep multi-endpoint alternatives out of the plotted file.
- Inputs checked: pair 123 thermal clothing/heart-failure hospital days, pair 150 ActWell body weight, and pair 226 STOP pharmacy quit rate.
- Elapsed time: approximately 13 minutes after the IBS batch, including source-text recheck, code patch, D/N regeneration, and invariant check.
- Included-row delta: +3 current Figure 1 D/N rows.
- New rows: `ying_2023_pair_123_thermal_clothing_hospital_days`, `ying_2023_pair_150_actwell_weight_loss`, `ying_2023_pair_226_stop_pharmacy_quit_rate`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML and parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/{thermal,actwell,stop}/`.
- Conversion: thermal and ActWell use CI-derived Hedges g for matched continuous primary outcomes; STOP uses Chinn log(OR) d-equivalents from matched 4-week quit-rate counts and is marked sensitivity-grade because the full trial primary endpoint was service throughput.
- Rejection/hold reasons encountered: secondary thermal/ActWell outcomes were not added as extra rows; STOP throughput and retention were not added; the STOP row uses the quit-outcome denominators rather than the broader pilot throughput count to preserve endpoint grain.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,693 root rows, 2,024 D/N-included rows, 0 critical invariant violations and 0 warnings for the 17 included Ying rows.
- Decision: this narrow rescue route remains valid but low-throughput. Continue with already-cached high-confidence candidates only when the endpoint match is tight; otherwise shift back toward structured corpora with explicit pair/value fields.

## 2026-05-08T16:48:54Z - Ying Exact-Value Abstract Cluster

- Strategy: filter the cached Ying Europe PMC abstracts for pairs where both pilot and full-scale records expose exact outcome values, then promote only one matched endpoint per pilot/full-scale pair.
- Inputs checked: high-signal exact-value candidates from the Ying 001-248 cache, with REHAB-HF held because the pilot SPPB adjusted effect lacked a clean variance route.
- Elapsed time: approximately 8 minutes after the prior Ying batch, including candidate filtering, PMC mirroring for available full texts, code patch, D/N regeneration, and invariant check.
- Included-row delta: +5 current Figure 1 D/N rows.
- New rows: `ying_2023_pair_136_very_brief_smoking_advice_7day_ppa`, `ying_2023_pair_144_aphasia_word_finding`, `ying_2023_pair_161_rotator_cuff_spadi`, `ying_2023_pair_162_gsp_function_score`, `ying_2023_pair_182_scimitar_smoking_cessation`.
- Source evidence: Europe PMC JSON records for all five pairs, plus mirrored PMC full text for the very-brief smoking advice, Big CACTUS aphasia, and SCIMITAR+ full-scale articles under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/`.
- Conversion: smoking rows use Chinn log(OR) d-equivalents from reported counts or ORs; aphasia, rotator-cuff SPADI, and GSP function-score rows use CI-derived Hedges g from the matched endpoint estimates and effect-estimate Ns.
- Rejection/hold reasons encountered: REHAB-HF was held for conversion ambiguity; Text4Heart, CALM, and several other exact-looking rows remain held due endpoint/instrument drift, native-only effect type, or comparator changes. No secondary or alternative outcome from a promoted pair was added as an extra row.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,698 root rows, 2,029 D/N-included rows, 0 critical invariant violations and 0 warnings for the 22 included Ying rows.
- Decision: the exact-value abstract cluster is currently the highest valid yield route in the Ying workstream. Continue scanning for similarly exact pairs, but keep rejecting rows with endpoint drift or ambiguous variance.

## 2026-05-08T16:56:22Z - Ying/OCD PFIT Matched Response Rescue

- Strategy: promote a single high-confidence exact-value Ying pair only after mirroring both PMC full texts and confirming arm-level responder counts for the same PFIT versus standard child CBT contrast.
- Inputs checked: Ying pair 145 pediatric obsessive-compulsive disorder PFIT pilot and full-scale RCT.
- Elapsed time: approximately 7.5 minutes after the prior exact-value cluster, including PMC mirroring, parsed-text search, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_145_ocd_pfit_response`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML, parsed text, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/ocd_pfit/`.
- Conversion: Chinn log(OR) d-equivalents from the matched CGI-I responder endpoint. Pilot uses 7/10 PFIT responders versus 4/10 standard-treatment responders. Full-scale uses 21/31 PFIT responders versus 12/30 standard-treatment responders.
- Rejection/hold reasons encountered: remission was not added as a second row, and the replication plot N uses the 61 participants with posttreatment responder denominators rather than the broader 62 randomized sample.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,699 root rows, 2,030 D/N-included rows, 0 critical invariant violations and 0 warnings for the 23 included Ying rows.
- Decision: continue the exact-value Ying queue only for pairs with the same level of explicit denominator and endpoint alignment; this route is valid but too slow to reach 3,000 alone.

## 2026-05-08T17:02:57Z - Ying Exact-Value Queue With Hold Filters

- Strategy: continue the exact-value Ying queue but use the strict timepoint/metric filters before promotion; log the negative probes to avoid repeatedly chasing attractive but invalid exact-value abstracts.
- Inputs checked: pair 209 MumMoodBooster postnatal depression remission, pair 151 SmartQuit/iCanQuit smoking cessation, pair 100 CAPABLE disability, pair 083 integrated diabetes/depression care, and pair 233 caregiver depression prevention.
- Elapsed time: approximately 6.5 minutes after the OCD PFIT row, including four hold decisions, one PMC mirroring pass for the promoted row, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_233_caregiver_depression_incidence`.
- Source evidence: Europe PMC JSON records for the pilot/full-scale pair plus mirrored PMC HTML, parsed text, and SHA256 manifest for the full-scale article under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/caregiver_depression/`.
- Conversion: Chinn log(OR) d-equivalents from matched post-intervention major-depression incidence counts for complete cognitive-behavioral conference-call intervention versus usual-care control. Pilot uses 0/20 versus 2/19 with Haldane-Anscombe 0.5 continuity correction for the zero-event intervention arm. Full-scale uses 1/69 versus 7/80.
- Rejection/hold reasons encountered: MumMoodBooster held for 12-week pilot remission versus 21-week full-scale remission; SmartQuit held for 2-month pilot 30-day PPA versus 3-month or 12-month full-scale PPA; CAPABLE held because full-scale disability is a negative-binomial ratio of means rather than a recoverable D/SMD; integrated diabetes/depression held because full-scale 6-week adherence counts are figure-only rather than text-exact in the mirrored article. The caregiver behavioral-activation arm was not added as a second row.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,700 root rows, 2,031 D/N-included rows, 0 critical invariant violations and 0 warnings for the 24 included Ying rows.
- Decision: the strict exact-value queue is still producing valid rows, but at low throughput and with a high hold rate. Continue only for candidates with exact denominators, matched timing, and no alternate-arm fanout; meanwhile keep looking for structured sources with explicit pair/value fields.

## 2026-05-08T17:16:46Z - Metascience Singleton Direct Rows

- Strategy: mine the previously unreviewed Metascience/FReD API direct/close bucket, but promote only singleton DOI-backed pairs that survived duplicate checks, current D/N gates, and one-row-per-DOI-pair review.
- Inputs checked: 82 mechanically nonduplicate API rows from `metascience-misc-unreviewed-current-nonduplicates.tsv`; bulk-hold buckets included 18 SSRP rows already represented under weaker identity fields, 22 sensory-marketing rows from an existing multi-outcome family, 14 Asch warm/cold adjective fanout rows, and multiple repeated-effect FReD explorer DOI pairs.
- Elapsed time: approximately 13 minutes including candidate triage, allowlist-style promoter creation, D/N regeneration, and invariant check.
- Included-row delta: +5 current Figure 1 D/N rows.
- New rows: `metascience_singleton_direct_5e83210ebc4dd618`, `metascience_singleton_direct_14f68c7936e1018a`, `metascience_singleton_direct_b19fd99147ff1d7a`, `metascience_singleton_direct_eb391d2819ef7e15`, and `metascience_singleton_direct_4349aa593d00dc4e`.
- Source evidence: mirrored Metascience API JSON `data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json` with SHA-256 `34547aaf4d5b25183c4783bc299c063a2cb13dde0dcaeef8188db67d339e4880`; audit and summary under `steps/corpus_results/figure1/metascience_observatory_singleton_direct_20260508/`.
- Conversion: Metascience normalized Pearson `r` fields converted to nonnegative D magnitudes as `abs(2*r/sqrt(1-r^2))`; API N/effect fields are preserved as verbatim support in the promoted CSV.
- Rejection/hold reasons encountered: skipped bulk SSRP because root already represents SSRP; skipped sensory-marketing because the family already has many rows per source paper; skipped Asch and repeated FReD explorer DOI pairs because they were multi-outcome/fanout without a predeclared primary row; skipped rows lacking replication DOI-backed identity.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Metascience Observatory FReD API singleton direct rows' --strict-source-evidence --fail-on-critical`.
- Check result: 2,705 root rows, 2,036 D/N-included rows, 0 critical invariant violations and 0 warnings for the 5 included singleton direct rows.
- Decision: this route is clean but shallow. Expand only with reviewed singleton rows; do not bulk-promote the remaining unreviewed API rows without a stronger duplicate/fanout classifier.

## 2026-05-08T17:26:48Z - Ying/Rhinothermy Day-4 MJS Rescue

- Strategy: continue exact-value Ying rescue for a pair with identical symptom instrument and timepoint, using PMC/paperclip full text rather than abstract-only values.
- Inputs checked: GaPP1/GaPP2 was held for BPI-vs-NRS instrument drift and 6-month-vs-16-week timing; WebQuit remains held for 3-month pilot versus 12-month full-scale outcome exposure. Ying pair 236 rhinothermy was promoted after confirming both sides use day-4 Modified Jackson Score.
- Elapsed time: approximately 10 minutes after the Metascience singleton batch, including paperclip lookup, PMC mirroring, source checksum manifest, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_236_rhinothermy_day4_mjs`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML, paperclip full-text line files, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/rhinothermy/`.
- Conversion: CI-derived Hedges g for day-4 Modified Jackson Score; pilot from mixed-model difference -6.4, 95% CI -9.4 to -3.3 with day-4 Ns 19/10; full-scale from estimated difference 0.37, 95% CI -0.69 to 1.42 with randomized Ns 85/85.
- Rejection/hold reasons encountered: GaPP held for endpoint/timepoint drift; WebQuit held for no exact full-scale 3-month PPA value in mirrored text; no additional rhinothermy daily MJS or symptom-resolution endpoints were added.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,706 root rows, 2,037 D/N-included rows, 0 critical invariant violations and 0 warnings for the 25 included Ying rows.
- Decision: valid but still slow. Continue exact-value Ying only for same endpoint/same timepoint cases; search next for explicit binary clinical endpoints or structured singleton API rows.

## 2026-05-08T17:34:12Z - Ying/NPWT Caesarean SSI Rescue

- Strategy: promote a binary clinical endpoint where both pilot and definitive RCT report the same primary event outcome and arm counts.
- Inputs checked: Ying pair 183 negative-pressure wound therapy after caesarean section.
- Elapsed time: approximately 7 minutes after the rhinothermy row, including paperclip lookup, PMC mirroring, source checksum manifest, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_183_npwt_csection_ssi`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML, paperclip full-text line files, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/npwt_csection/`.
- Conversion: Chinn log(OR) d-equivalents from matched cumulative surgical-site infection counts; pilot uses 10/44 NPWT versus 12/43 standard dressing, full-scale uses 75/1017 NPWT versus 99/1018 standard dressing.
- Rejection/hold reasons encountered: wound complications, blistering, readmissions, and full-scale sensitivity analyses were not added as extra endpoints.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,707 root rows, 2,038 D/N-included rows, 0 critical invariant violations and 0 warnings for the 26 included Ying rows.
- Decision: exact binary clinical endpoints remain reliable but low-volume. Keep mining only when the pair has one clearly matched primary endpoint and local value-bearing full text.

## 2026-05-08T17:42:22Z - Ying/SMS Vaccine Visit-2 Completion Rescue

- Strategy: use a sensitivity-grade matched completion endpoint from a pilot/full-scale SMS vaccination reminder pair, while excluding related timeliness and visit-3 outcomes to preserve one plotted endpoint.
- Inputs checked: Ying pair 204 Guatemala SMS infant-vaccination reminder pilot and larger RCT.
- Elapsed time: approximately 8 minutes after the NPWT row, including paperclip lookup, PMC mirroring/parsing for the full-scale article, endpoint audit, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_204_sms_vaccine_visit2_completion`.
- Source evidence: Europe PMC JSON records plus mirrored pilot paperclip full-text lines, mirrored full-scale PMC HTML, parsed text, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/sms_vaccine_guatemala/`.
- Conversion: Chinn log(OR) d-equivalents from matched visit-2 completion counts; pilot maps 95.0% versus 90.1% to 152/160 intervention versus 145/161 usual care, full-scale uses 330/358 intervention versus 333/362 usual care.
- Rejection/hold reasons encountered: the full-scale paper highlights scheduled-date timeliness, so this is marked sensitivity-grade; visit-3 completion, scheduled-date timeliness, up-to-7-day timeliness, and per-protocol analyses were not added.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,708 root rows, 2,039 D/N-included rows, 0 critical invariant violations and 0 warnings for the 27 included Ying rows.
- Decision: this route is valid for bounded sensitivity rows but should not expand into multiple visit/timepoint rows from the same pilot/full-scale pair.

## 2026-05-08T17:44:25Z - Ying/REHAB-HF SPPB Rescue

- Strategy: continue exact-value Ying rescue only where the same primary endpoint, follow-up timepoint, and comparator are exposed in local full text.
- Inputs checked: Ying pair 230 REHAB-HF pilot and full-scale RCT.
- Elapsed time: approximately 2 minutes after the SMS vaccine row because both PMC full-text mirrors and parsed text were already present locally.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_230_rehabhf_sppb`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML, parsed text, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/rehabhf/`.
- Conversion: pilot Hedges g from reported 3-month SPPB LS means 7.4 +/- 0.5 versus 6.3 +/- 0.5 with outcome-complete Ns 12/12, treating the LS-mean SEs as group mean SEs; full-scale CI-derived Hedges g from adjusted mean difference 1.5 (95% CI 0.9 to 2.0) with primary-outcome Ns 149/155.
- Rejection/hold reasons encountered: six-minute walk, frailty, quality-of-life, rehospitalization, and death outcomes were not added as additional rows from the same pilot/full-scale pair.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,709 root rows, 2,040 D/N-included rows, 0 critical invariant violations and 0 warnings for the 28 included Ying rows.
- Decision: valid sensitivity row, but the LS-mean-SE conversion is a weaker route than count/CI rows. Continue only when exact primary endpoint values and outcome-complete Ns are exposed; prefer CI/count rows when available.

## 2026-05-08T17:48:22Z - Ying/Type-2-Diabetes Remission Rescue

- Strategy: promote a single binary remission endpoint from a pilot/full-scale diabetes-remission strategy pair, while excluding alternate pilot arms and later exploratory endpoints.
- Inputs checked: Ying pair 227 type-2-diabetes remission pilot and larger RCT; the nearby patient-navigation smoking pair was held because the pilot endpoint was treatment engagement at 3 months whereas the larger trial primary endpoint was biochemically confirmed cessation at 12 months.
- Elapsed time: approximately 4 minutes after REHAB-HF, using existing Europe PMC JSON value-bearing records.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_227_diabetes_remission`.
- Source evidence: Europe PMC JSON records `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/227_pilot_10_1210_jc_2016_3373.json` and `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/227_full_10_1210_clinem_dgaa248.json`.
- Conversion: Chinn log(OR) d-equivalents from matched remission counts, with the pilot 16-week intervention arm mapped to 11/27 versus 4/28 and the larger trial mapped to 19/77 versus 13/77.
- Rejection/hold reasons encountered: patient-navigation smoking cessation held for endpoint/timepoint mismatch.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,710 root rows, 2,041 D/N-included rows, 0 critical invariant violations and 0 warnings for the 29 included Ying rows.
- Decision: continue exact-value Ying only where the same endpoint and contrast are explicit; the route is reliable but still too slow for the 3,000-row target by itself.

## 2026-05-08T17:57:44Z - Ying/Topiramate Male Smoking-Cessation Rescue

- Strategy: continue the exact-value Ying queue, but allow a bounded sensitivity row only when the larger article explicitly identifies the pilot signal it is testing and the endpoint is the same.
- Inputs checked: CODES was held because the primary outcome is native count-model frequency and the convertible seizure-freedom endpoint is secondary with loose follow-up timing; PARITY was held because the pilot article exposes only the overall SSI rate, not SSI by antibiotic arm; ETEC patch vaccine was held because the phase-II abstract reports placebo ETEC cases and vaccine efficacy but not the vaccine-arm event count for the same endpoint. Ying pair 215 topiramate male smoking cessation was promoted.
- Elapsed time: approximately 9 minutes after the diabetes-remission row, including candidate-screen review, PMC mirroring for the full-scale article, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_215_topiramate_male_smoking_cessation`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML, parsed text, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/topiramate_smoking/`.
- Conversion: Chinn log(OR) d-equivalents from CO-confirmed four-week abstinence counts. Pilot male subgroup is uniquely reconstructed from the reported male total and percentages as 6/16 topiramate versus 3/22 placebo; full-scale male trial uses 5/63 topiramate versus 7/66 placebo.
- Rejection/hold reasons encountered: CODES, PARITY, and ETEC were not promoted because each failed a different exact matched-effect requirement; female pilot participants and relapse, withdrawal, weight, and adverse-event endpoints were not added from the topiramate pair.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,711 root rows, 2,042 D/N-included rows, 0 critical invariant violations and 0 warnings for the 30 included Ying rows.
- Decision: this is valid but sensitivity-grade. Continue mining abstract-cache candidates with exact denominators or CI-derived effects, but do not expand rows through subgroup/fanout alternatives.

## 2026-05-08T18:04:31Z - Ying/GEM Postpartum Weight-Goal Rescue

- Strategy: promote a full-text-backed clinical pilot/full-scale pair where the endpoint, timepoint, and intervention family line up exactly and the larger trial reports an adjusted OR for the same endpoint.
- Inputs checked: Ying pair 091 gestational-diabetes postpartum lifestyle intervention and GEM cluster RCT.
- Elapsed time: approximately 7 minutes after the topiramate row, including paperclip/PMC mirroring, table audit, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_091_gem_gdm_weight_goal`.
- Source evidence: Europe PMC JSON records plus mirrored PMC/paperclip full text and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/gem_gdm_weight/`.
- Conversion: Chinn log(OR) d-equivalents for the 12-month postpartum weight-goal endpoint. Pilot uses Table 2 counts 27/72 lifestyle intervention versus 18/84 usual care; full-scale GEM uses the 12-month measured-weight primary-analysis adjusted OR 1.25 from 676 intervention and 744 usual-care women.
- Rejection/hold reasons encountered: no earlier timepoint, subgroup, imputed/sensitivity, weight-change, physical-activity, diet, breastfeeding, or diabetes-incidence rows were added.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,712 root rows, 2,043 D/N-included rows, 0 critical invariant violations and 0 warnings for the 31 included Ying rows.
- Decision: expand similar full-text table-backed Ying pairs, but keep using only the endpoint/timepoint that the pilot and full-scale papers share.
- Conversion: Chinn log(OR) d-equivalents from post-intervention remission counts. Pilot uses the closer 16-week intensive-intervention arm versus control, 11/27 versus 4/28, based on reported 40.7% versus 14.3%. Full-scale uses primary remission at 24 weeks, 19/77 versus 13/77.
- Rejection/hold reasons encountered: pilot 8-week arm, on-treatment normoglycemia, later full-scale exploratory timepoints, and relapse hazard ratio were not added as extra rows.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,710 root rows, 2,041 D/N-included rows, 0 critical invariant violations and 0 warnings for the 29 included Ying rows.
- Decision: valid sensitivity row with a regimen-duration caveat. Continue the Ying exact-value path only for one clear endpoint per pair; this remains too slow to be the primary path to 3,000.

## 2026-05-08T18:11:28Z - Ying/FFIT 12-Week Percent Weight-Loss Rescue

- Strategy: continue bounded full-text-backed Ying rescue only when the same endpoint, contrast, and timepoint are explicit; avoid adding alternate outcomes from the same pilot/full-scale pair.
- Inputs checked: Ying pair 132 Football Fans in Training pilot and larger FFIT randomized trial.
- Elapsed time: approximately 7 minutes after the GEM row, including endpoint audit, value-evidence checksum manifest, code patch, D/N regeneration, and invariant check.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_132_ffit_12wk_percent_weight_loss`.
- Source evidence: Europe PMC JSON records plus mirrored Europe PMC fullTextXML/PMC full text and SHA256 value-evidence manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/ffit_weight/`.
- Conversion: Hedges g from the matched 12-week percentage body-weight-loss endpoint. Pilot Table 3 uses 4.6 +/- 2.8% for p-FFIT intervention men (n=44) versus -0.6 +/- 2.0% for waitlist comparison men (n=42). Full-scale Table 3 uses adjusted 12-week percentage-weight-change difference -4.71 percentage points (95% CI -5.44 to -3.98) with n=329 intervention and n=347 comparison.
- Rejection/hold reasons encountered: the pilot's 6- and 12-month intervention-only follow-up, the larger trial's 12-month primary endpoint, kilogram-weight-change rows, and 5% responder endpoints were not added as separate rows.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`.
- Check result: 2,713 root rows, 2,044 D/N-included rows, 0 critical invariant violations and 0 warnings for the 32 included Ying rows.
- Decision: valid sensitivity row. Continue using Ying only for isolated, table-backed rows; its current yield is still far below the rate needed for the 3,000-row target, so the next broad move should return to structured corpus/database routes.

## 2026-05-08T18:37:35Z - Ying/MumMoodBooster Diagnostic-Remission Rescue

- Strategy: use the existing Ying exact-value candidate queue only for a single full-text-backed pilot/full-scale pair with the same contrast and primary diagnostic endpoint.
- Inputs checked: Ying pair 209 MumMoodBooster postnatal-depression RCT and larger three-arm RCT. The face-to-face CBT arm, symptom-scale outcomes, and imputed/worst-case sensitivity proportions were intentionally excluded to preserve one row per matched MMB-versus-TAU remission contrast.
- Elapsed time: approximately 25 minutes after the FFIT row, including full-text table audit, code patch, D/N regeneration, and invariant checks.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_209_mummoodbooster_remission`.
- Source evidence: Europe PMC JSON records plus mirrored PMC HTML, parsed text, and SHA256 value-evidence manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/pair209_mummoodbooster/`.
- Conversion: Chinn log(OR) d-equivalents from observed diagnostic-remission counts. Pilot uses 12-week remission 15/19 MumMoodBooster versus 4/22 treatment-as-usual. Larger RCT uses Table 3 remission excluding lost-to-follow-up cases: 25 remission and 7 still diagnosed for MumMoodBooster versus 18 remission and 13 still diagnosed for treatment-as-usual.
- Rejection/hold reasons encountered: no face-to-face CBT contrast, symptom-scale rows, Figure 4 imputed proportions, or additional follow-up/sensitivity rows were added.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,714 root rows, 2,045 D/N-included rows, 0 critical invariant violations and 0 warnings for the 33 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid live row, but the rate is still far below the 3,000-row target. Keep Ying as a fallback for isolated high-confidence pairs and move the next main probe back to structured/corpus sources with explicit pair mappings.

## 2026-05-08T18:51:57Z - Structured-Corpus Leftover Probe: Metascience/FReD, Awesome, FORRT

- Strategy: look for faster row supply in already mirrored structured databases before continuing one-off paper chasing.
- Inputs checked: unreviewed Metascience/FReD misc singleton DOI-pair rows, Metascience rows held for missing normalized `r`/`N`, currently excluded root rows, unpromoted Awesome Replicability raw folders, and the 10 mechanically parseable FORRT Reversals entries from `forrt-reversals-conservative-candidate-scan.tsv`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Metascience singleton result: all complete DOI-pair candidates with enough metadata were already represented in the root table through FReD/Metascience DOI aliases, including Fath/Kay hierarchy corruption, Bargh automaticity/Doyen, Wakslak construal, and Moral Hypocrisy.
- Metascience native-effect result: rows with native numeric effects were mostly integrated-project/site/lab fanout or inconsistent native metrics; no blank-tag non-Curate DOI-backed direct/close row had a safe D route and larger replication N.
- Excluded-root result: 669 numeric root rows remain excluded because replication N is not larger or an N is below 10; no signed-D repair issue was found.
- Awesome result: the unpromoted folders expose replication-side data but not value-bearing original source rows, so they remain original-source acquisition tasks.
- FORRT result: the parseable leftovers are already represented, fail the larger-N rule, or fail exact 1:1 alignment. The apparent new chimpanzee handedness row reports the original effect as a range (`d = 0.69 to 0.97`) across behavior variants while the replication effect is a single later value, so it was not promoted.
- Checks: no root-table edits were made, so D/N regeneration was not rerun for this zero-yield probe. Current verified state remains 2,714 root rows and 2,045 D/N-included rows from the prior successful build.
- Decision: abandon these leftover structured-corpus tails as a high-throughput path. The next strategy should target a new or underused source with an explicit result table, not remainder rows already screened for ambiguity.

## 2026-05-08T19:01:21Z - Live FReD Workbook Current-Root Duplicate Probe

- Strategy: test whether the live FReD workbook downloaded on 2026-05-08 exposes new validated rows beyond the older local FReD workbook and the already promoted archive-rescue rows.
- Inputs checked: `data/raw/replication_projects/fred/live_check_2026-05-08/FReD_osf_z5u9b_2026-05-08.xlsx`, `steps/corpus_results/figure1/fred_live_rescue_20260508_current_root/fred-archive-rescue-candidate-scan.tsv`, and the current `FIGURE1_REPLICATION_PAIRS.tsv`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Result: the live workbook scan found 4,659 data rows, 425 complete validated rows with no explicit exclusion, and 296 rows passing the current D/N mechanical gates. Of those, 167 were known project overlaps, 128 were DOI-pair duplicate holds, and the single unresolved row was `q6tv8_1`.
- Duplicate review: `q6tv8_1` maps to the Epley/Gilovich anchoring cognitive-load self-generated-anchor row already present in the root table as `fred_q6tv8_1037` and `fred_q6tv8_1038` from the older FReD workbook, with the same original DOI, N values, D values, and outcome family but a newer OSF registration DOI alias for the replication source.
- Rejection/hold reasons encountered: no high-precision new live FReD rows remained after current-root duplicate review; the duplicate buckets are dominated by previously integrated FReD/OSF/DataReplicada/FORRT rows or same DOI-pair multi-row fanout that would need row-level manual review rather than bulk promotion.
- Checks: no root-table edits were made, so D/N regeneration was not rerun for this zero-yield probe. Current verified state remains 2,714 root rows and 2,045 D/N-included rows.
- Decision: abandon the current live FReD workbook scan as a high-throughput route unless a future script adds stronger DOI-alias and row-level duplicate resolution. Move to sources with genuinely new explicit pair tables.

## 2026-05-08T19:11:38Z - Ying/Auricular Acupressure Abstract-Exact Rescue

- Strategy: use the Ying exact-value candidate queue for a source-backed pilot/full-scale pair where both Europe PMC abstract records carry the same primary binary endpoint, arm Ns, and effect text.
- Inputs checked: Ying pair 196, `196_pilot_10_1371_journal_pone_0122724.json`, `196_full_10_1089_jicm_2021_0332.json`, and the existing root table/current D/N build.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_196_auricular_acupressure_insomnia_response`.
- Source evidence: Europe PMC JSON records under `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/`. The pilot abstract reports active AA n=32 versus sham AA n=31, week-8 clinical response 20/32 versus 10/31, and a full-scale trial is warranted. The full-scale abstract reports active AA n=64 versus sham AA n=69 with the same clinical-response definition, 55% versus 36%, OR=1.5, 95% CI 1.0 to 2.2.
- Conversion: Chinn log(OR) d-equivalents. Pilot D uses the exact event counts; full-scale D uses the reported OR because rounded percentages do not reproduce it exactly.
- Rejection/hold reasons encountered: PSQI-score trajectories, hypnotic-use outcomes, and follow-up timepoints were not added as extra rows to preserve one matched primary endpoint for the pilot/full-scale pair.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,715 root rows, 2,046 D/N-included rows, 0 critical invariant violations and 0 warnings for the 34 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid live row. The abstract-exact Ying path can keep adding isolated rows, but its observed rate is still low; keep parallel probing for structured sources with explicit pair/value tables.

## 2026-05-08T19:18:27Z - Ying/Group Physiotherapy Knee LEFS Rescue

- Strategy: promote one full-text-backed Ying pilot/full-scale pair where the intervention family, outcome measure, and 6-month timepoint match exactly enough for a single sensitivity row.
- Inputs checked: Ying pair 216, Europe PMC abstract records, and mirrored paperclip PMC line/meta files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/group_pt_knee/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_216_group_pt_knee_lefs_6mo`.
- Source evidence: the pilot full text reports 46 randomized participants, 23 per group, 6-month questionnaire return 21/21 intervention and 15/20 usual care, and 6-month LEFS 57.8 (SD 15.2) versus 45.0 (SD 20.8). The larger trial reports 180 randomized participants, 89 intervention and 91 usual care, and adjusted 6-month LEFS mean difference 5.41 (95% CI 1.06 to 9.77).
- Conversion: pilot D uses Hedges g from complete-case arm summaries; replication D is CI-derived Hedges g from the adjusted mean-difference CI and randomized arm Ns.
- Rejection/hold reasons encountered: 3-month, 12-month, per-protocol, imputed/sensitivity, KOOS, satisfaction, and adverse-event outcomes were not added as separate rows.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,716 root rows, 2,047 D/N-included rows, 0 critical invariant violations and 0 warnings for the 35 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row. This confirms paperclip-backed PMC rescue can add individual rows, but each row still takes enough adjudication that it cannot carry the 3,000 target alone.

## 2026-05-08T19:23:56Z - Ying/WHiTE X-Bolt Hip EQ-5D Rescue

- Strategy: promote a pilot/full-scale clinical-trial pair where both sources report the same implant comparison and the larger PMC full text exposes the same 12-month EQ-5D endpoint as the pilot's one-year primary endpoint.
- Inputs checked: Ying pair 206, Europe PMC abstract records, and mirrored paperclip PMC line/meta files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/white_hip_xbolt/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_206_white_xbolt_eq5d_12mo`.
- Source evidence: the pilot abstract reports 100 recruited participants, one-year EQ-5D-3L primary outcome available for 88 patients, and mean difference 0.03 (95% CI -0.17 to 0.120). The larger WHiTE Four full text reports 1,128 randomized participants, 564 per arm, and 12-month EQ-5D-5L mapped utility adjusted difference 0.026 (95% CI -0.016 to 0.068).
- Conversion: pilot D is CI-derived Hedges g using balanced 44/44 outcome-available patients; replication D is CI-derived Hedges g using randomized arm Ns.
- Rejection/hold reasons encountered: four-month primary endpoint, mortality, residential status, mobility, revision surgery, radiological, per-protocol, CACE, and missing-data sensitivity outcomes were not added separately.
- Checks: `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,717 root rows, 2,048 D/N-included rows, 0 critical invariant violations and 0 warnings for the 36 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row. The Ying + PMC rescue path is steadily producing rows, but the rate remains around one row per several minutes only when an already-scanned candidate has exact value text.

## 2026-05-08T19:34:00Z - Candidate Adjudication Ledger Started

- Strategy update: record expensive negative/held candidate checks in a machine-readable TSV so future Figure 1 passes do not redo them and other projects can reuse the exact source findings.
- New artifact: `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/ying-candidate-adjudication.tsv`.
- Initial rows logged: Ying pair 124 `WebQuit.org` versus `Smokefree.gov` and Ying pair 151 `SmartQuit/iCanQuit` versus `QuitGuide`.
- Decision: both are real pilot-to-definitive smoking-cessation sequences with value-bearing local PMC mirrors, but both are held/rejected for current Figure 1 because the checked value-bearing full-scale reports do not expose the exact same follow-up timepoint as the pilot values.
- Reuse note: keep these as endpoint-drift/design-change examples or possible candidates for a separately labeled nearest-follow-up analysis; do not promote them into current Figure 1 without an explicit policy change or newly found matched-timepoint source data.

## 2026-05-08T19:48:00Z - Backfilled Prior Reject/Hold Ledgers

- Strategy update: paused new row promotion to back-process prior rejected, held, and abandoned checks into durable machine-readable ledgers.
- Generator: `scripts/backfill_goal3000_adjudication_ledgers.py`.
- New/updated ledgers:
  - `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/source-strategy-adjudication.tsv` with 49 source/strategy audit rows.
  - `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/reviewcue-adjudication.tsv` with 80 review-cue routing/adjudication rows.
  - `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/ying-candidate-adjudication.tsv` with 14 Ying candidate rows: 2 detailed timepoint-mismatch holds and 12 older full-text-rescue candidates marked `prior_reject_needs_reconstruction`.
  - `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/adjudication-ledger-backfill-summary.tsv` with grouped counts.
- Coverage backfilled: corpus strategy rejects/holds; Many Labs 1/3/5 site-level and audit decisions; staged native-only Li/Wils clinical tables; Kerschbaumer ACR50/ACR70 endpoint fanout holds; FReD archive duplicate/manual holds; metascience duplicate/missing/failed-gate holds; review-cue rejects/context/route/escalate decisions; and Ying checked-not-promoted local full-text rescue candidates.
- Validation: all four TSVs read successfully with pandas after generation.
- Decision: resume row discovery only after adding any new reject/hold to these ledgers immediately, not just to prose logs.

## 2026-05-08T19:58:00Z - Ying/Text4Heart Hold Logged

- Strategy update: rechecked Ying pair 241 Text4Heart/Text4HeartII after paperclip-backed full-text mirroring exposed a possible self-reported Morisky medication-adherence comparison.
- Included-row delta: +0 current Figure 1 D/N rows.
- New adjudication row: `ying_2023_pair_241_text4heart` in `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/ying-candidate-adjudication.tsv`.
- Source evidence: mirrored paperclip line/meta files and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/text4heart/`.
- Hold reason: the explicit pilot-to-full relation maps a lifestyle-adherence pilot finding to a larger trial whose primary endpoint changed to objective medication possession ratio. The possible Morisky-to-Morisky row is secondary/exploratory on both sides, while the larger intervention removed the website and pedometer and revised message content.
- Validation: `ying-candidate-adjudication.tsv` reads with pandas and now has 15 rows: 3 detailed holds and 12 `prior_reject_needs_reconstruction` rows.
- Decision: do not promote Text4Heart under current Figure 1 rules. Keep it for a possible design-change or objective-versus-self-report adherence analysis.

## 2026-05-08T20:15:00Z - Ying/POPS2 Excessive Gestational Weight Gain Rescue

- Strategy: continue the Ying exact-value queue but require same endpoint/timepoint and exact value-bearing source text before promotion.
- Inputs checked: Ying pair 179 POPS/POPS2, Europe PMC abstract records, and mirrored Paperclip full-text line/meta files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/pops2_weight/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_179_pops2_excessive_gestational_weight_gain`.
- Source evidence: the pilot Table 2 reports excessive gestational weight gain at 38 weeks as 8/34 intervention versus 10/34 usual care. The full-scale POPS2 article explicitly cites the feasibility trial as preparation for the current study and reports the same 38-week excessive gestational weight-gain endpoint as 81/305 intervention versus 90/311 usual care, adjusted OR 0.84 (95% CI 0.53 to 1.33).
- Conversion: Chinn log(OR) d-equivalents. Pilot D uses exact event counts; replication D uses the reported adjusted OR from the primary analysis.
- Caveat: sensitivity-grade because the pilot designated the endpoint as secondary to inform the definitive trial, while the full-scale trial made it primary.
- Rejection/hold rows logged: `ying_2023_pair_186_low_mood_cbt` held for PHQ-9 timepoint/analysis mismatch, and `ying_2023_pair_201_hap_depression_india` held for depression endpoint-threshold and timepoint mismatch. Both are now in `ying-candidate-adjudication.tsv` with local source paths/checksums where available.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,718 root rows, 2,049 D/N-included rows, 0 critical invariant violations and 0 warnings for the 37 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row. The queue still yields at individual-paper speed, but the immediate adjudication logging avoided losing two negative checks from the same pass.

## 2026-05-08T20:31:00Z - Ying/Chuna Low-Back-Pain NRS Rescue

- Strategy: continue the exact-value queue, looking for a powered full-scale paper that explicitly uses the pilot to choose the later contrast and exposes the same primary endpoint.
- Inputs checked: Ying pair 231 Chuna manual therapy for non-acute low-back pain, Europe PMC abstract records, and mirrored Paperclip full-text line/meta files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/chuna_lbp/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_231_chuna_lbp_nrs_7wk`.
- Source evidence: the pilot full text says a future well-powered two-arm CMT+UC versus UC verification trial would be performed and reports week-7 primary NRS low-back-pain change as -1.75 (95% CI -2.70 to -0.80) for CMT+UC versus -1.95 (95% CI -2.82 to -1.08) for UC, with 20 participants per arm. The full-scale article states the powered sample was determined through the pilot and reports the same week-7 primary endpoint as -3.02 +/- 1.72 for CMT+UC versus -1.36 +/- 1.75 for UC, with 97 participants per arm.
- Conversion: Hedges g. Pilot D recovers arm SDs from the reported within-arm 95% CIs; replication D uses reported arm change SDs.
- Caveat: sensitivity-grade because the pilot had three arms and the selected CMT+UC versus UC contrast is the future-verification contrast, not the pilot arm with the largest within-pilot improvement.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,719 root rows, 2,050 D/N-included rows, 0 critical invariant violations and 0 warnings for the 38 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row. The strongest lesson from this pass is to prefer candidates where the full-scale article names the pilot as the sample-size/design basis and the value table reports the same endpoint directly.

## 2026-05-08T20:47:00Z - Ying/MS Cognitive Remediation Composite Rescue

- Strategy: continue the exact-value queue, but only promote intervention variants when the relation is explicit and the protocol, population, comparator, duration, and primary endpoint align.
- Inputs checked: Ying pair 177 MS cognitive remediation/telerehabilitation, Europe PMC abstract records, and mirrored Paperclip full-text line/meta files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/ms_cognitive_remediation/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_177_ms_cognitive_remediation_composite`.
- Source evidence: the pilot reports 12-week remote adaptive cognitive remediation versus ordinary computer games and Table 5 cognitive-composite z-score change of 0.46 +/- 0.59 for active participants with change data (n=10) versus -0.14 +/- 0.48 for controls (n=9), Cohen's d=1.11. The full-scale RCT cites the prior pilot as establishing the protocol, uses the same MS population, remote 12-week adaptive cognitive remediation versus ordinary-games active-control structure, and primary neuropsychological composite outcome, and reports 0.25 +/- 0.45 for ACR (n=74) versus 0.09 +/- 0.37 for active control (n=61), estimated difference 0.16 (95% CI 0.02 to 0.30) and Cohen's d=0.3883.
- Conversion: Hedges g from reported arm mean changes, SDs, and Ns.
- Caveat: sensitivity-grade because the adaptive software changed from Lumosity in the pilot to a Posit/BrainHQ research program in the larger trial. This is logged explicitly as an intervention-variant follow-up rather than an exact intervention clone.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,720 root rows, 2,051 D/N-included rows, 0 critical invariant violations and 0 warnings for the 39 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row under current follow-up policy. Do not add motor, individual neuropsychological tests, compliance, perceived cognition, or program-time outcomes as extra rows.

## 2026-05-08T20:55:00Z - Ying/ezParent Parent-Warmth Timepoint-Matched Rescue

- Strategy: prefer a same-timepoint row over the more tempting headline pilot result when the headline result would mismatch the larger trial's reported effect timing.
- Inputs checked: Ying pair 198 ezParent, Europe PMC abstract records, mirrored pilot Paperclip line/meta files, and mirrored PMC HTML for the pilot and larger RCT under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/ezparent_parenting/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_198_ezparent_parent_warmth_3mo`.
- Source evidence: the pilot Table 4 reports a source-computed between-group parent-warmth effect size of d=0.07 from baseline to 12 weeks, with 79 analyzed parents. The larger RCT cites the pilot, uses ezParent versus enhanced usual care, treats parenting behavior as the primary outcome family, and Table 3 reports the 3-month parental-warmth initial treatment effect as d=-0.05.
- Conversion: no conversion beyond storing nonnegative D magnitudes from source-reported Cohen d values.
- Caveat: sensitivity-grade because the pilot's significant parent-warmth result was at 24 weeks, while this row uses the matched 12-week/3-month pilot effect. The larger trial also intentionally scaled back the pilot's personalized introduction to test a fully self-administered implementation.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,721 root rows, 2,052 D/N-included rows, 0 critical invariant violations and 0 warnings for the 40 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row. Do not add the pilot 24-week warmth result, full 6/12-month descriptive means, moderation analyses, other parenting subscales, parenting stress, child behavior, satisfaction, or usage outcomes as extra rows.

## 2026-05-08T21:05:00Z - Ying/UTI Day-4 Symptom Resolution Rescue

- Strategy: continue the PMC-backed Ying exact-value queue, but allow only one endpoint for the trial pair and explicitly label comparator variants.
- Inputs checked: Ying pair 84 uncomplicated UTI, Europe PMC abstract records, and mirrored Paperclip line/meta files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/uti_ibuprofen/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_084_uti_day4_symptom_free`.
- Source evidence: the pilot identifies Day 4 symptom resolution as the primary endpoint and reports 21/36 ibuprofen patients versus 17/33 ciprofloxacin patients symptom-free. The larger trial explicitly cites the pilot, reports the same Day 4 symptom-free endpoint as 91/241 ibuprofen patients versus 129/243 fosfomycin patients, and is treated as the larger ibuprofen-first versus immediate-antibiotic strategy test.
- Conversion: Chinn log(OR) d-equivalents from the Day 4 symptom-free event counts. Pilot D = 0.152083; replication D = 0.343693.
- Caveat: sensitivity-grade because the antibiotic comparator changed from ciprofloxacin to fosfomycin and the larger trial made Day 4 symptom-free status secondary while using antibiotic courses and symptom-burden AUC as co-primary endpoints.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,722 root rows, 2,053 D/N-included rows, 0 critical invariant violations and 0 warnings for the 41 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: valid sensitivity row under current strategy-level comparator policy. Do not add symptom-burden AUC, antibiotic-course, pyelonephritis, relapse, or Day 7 outcomes as extra Figure 1 rows.

## 2026-05-08T21:13:00Z - Ying/BDD CBT Hold

- Strategy: use direct PMC HTML mirroring when Paperclip slabs are unavailable, but do not rescue rows through nearest-neighbor timepoints.
- Inputs checked: Ying pair 170 modular CBT-BDD pilot and larger CBT-BDD versus supportive psychotherapy RCT, Europe PMC records, and mirrored PMC HTML under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/bdd_cbt/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Value evidence found: pilot randomized 36 adults to immediate CBT-BDD versus a 12-week waitlist, with week-12 response 8/16 versus 2/17 and BDD-YBOCS change d=0.6; the 24-week CBT-BDD effect d=2.1 is uncontrolled after waitlist crossover. The larger RCT randomized 120 adults to CBT-BDD versus supportive psychotherapy for 24 weeks and reports overall growth-model d=-0.76, site-specific d=-0.25 and d=-1.36, plus week-24 completer responses 37/44 versus 28/48.
- Hold reason: the randomized pilot contrast is 12-week CBT-BDD versus waitlist, while the larger trial's primary contrast is 24-week CBT-BDD versus active supportive psychotherapy. That is comparator and timepoint drift under the current Figure 1 standard.
- Ledger update: `ying_2023_pair_170_bdd_cbt` added to `ying-candidate-adjudication.tsv` as a hold with source paths and checksums.
- Decision: do not promote under current rules. Keep as a design-evolution example or a possible future native-growth-model/active-comparator analysis.

## 2026-05-08T21:00:34Z - Ying/DECISION+ Immediate Antibiotic-Use Rescue

- Strategy: promote only if the pilot denominator can be tied to the same post-intervention endpoint rather than the all-period pilot total.
- Inputs checked: Ying pair 95 DECISION+/DECISION+2, Europe PMC records, and mirrored PMC HTML under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/decision_plus_antibiotics/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_095_decision_plus_immediate_antibiotic_use`.
- Source evidence: the larger CMAJ trial explicitly cites the pilot, reports the pilot immediate antibiotic-use decision result as control 49% versus DECISION+ 33%, says DECISION+ was modified and renamed DECISION+2, and says the sample size was based on the pilot. The pilot Table 2 gives T1 denominators of 81 DECISION+ and 70 control patients; Table 3 gives the matched T1 endpoint as 33% versus 49%. The larger trial reports the same primary endpoint as 27.2% versus 52.2% among 181 DECISION+2 and 178 control patients.
- Conversion: Chinn log(OR) d-equivalents from reported percentages. Pilot D = 0.368387; replication D = 0.591331.
- Caveat: sensitivity-grade because the training program was shortened/modified and the setting changed from private family medicine groups to family practice teaching units.
- Ledger update: `ying_2023_pair_095_decision_plus_immediate_antibiotic_use` added to `ying-candidate-adjudication.tsv` as promoted with source paths and checksums.
- Decision: valid sensitivity row under the current intervention-variant policy. Do not add baseline, T2 sustainability/replicability, filled-prescription, decision-role, agreement, or 2-week patient-outcome rows as extra Figure 1 rows.

## 2026-05-08T21:05:20Z - Ying/Mind-Body Low-Back-Pain Reconstruction Hold

- Strategy: back-process a `prior_reject_needs_reconstruction` row before chasing more new candidates.
- Inputs checked: Ying pair 36 active-control mind-body chronic low-back-pain pilot and larger RCT, Europe PMC abstract records, the stored PMC2849802 pilot HTML, and the stored PMC6361386 access artifact.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the pilot randomized 40 older adults to mindfulness meditation or health education, reports 16/20 and 19/20 completers, and says disability, pain, and psychological outcomes were measured at baseline, 8 weeks, and 4-month follow-up. The checked source exposes clinical outcomes mainly in Figure 2 and narrative "between-group differences did not reach statistical significance" text rather than tabulated effect values. The larger RCT abstract reports 282 randomized participants and source-reported RMDQ effect sizes of -0.23 at 8 weeks and -0.08 at 6 months.
- Access note: the existing `PMC6361386.html` artifact is a CAPTCHA/access page; Europe PMC advertises a PDF route but the PDF API returned HTTP 500 during this check. The full-trial abstract still provides enough value text for a hold decision, but not enough to promote without a valid original value route.
- Hold reason: no current Figure 1 row because the original/pilot D would require figure digitization or another value-bearing table/PDF source not yet mirrored.
- Ledger update: `ying_2023_pair_036_mindbody_lbp_active_control` added as a specific hold, superseding the earlier vague `prior_reject_needs_reconstruction` status for practical routing.
- Decision: skip for the current 3k grind unless a value-bearing pilot table/PDF is found or Figure 2 digitization is explicitly admitted as an extraction route.

## 2026-05-08T21:06:10Z - Ying/Chlorhexidine Wipes Reconstruction Hold

- Strategy: use existing Europe PMC abstract records to convert an ambiguous prior reconstruction row into a concrete hold when the mismatch is explicit.
- Inputs checked: Ying pair 25 chlorhexidine vaginal/neonatal or infant wipes, Europe PMC abstract records, and stored larger-trial PMC artifact.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the pilot enrolled 203 births, 103 receiving chlorhexidine, and was designed for tolerance, safety, acceptability, and feasibility; it explicitly says it was not powered to show significant neonatal outcome differences. The larger trial randomized 5,008 laboring women/neonates and reports primary neonatal sepsis or 7-day perinatal mortality as 3.1% versus 3.4%, RR 0.91.
- Hold reason: the pilot is a feasibility/safety precursor, while the larger trial is an efficacy trial with a different primary endpoint family. That fails the current matched outcome rule even though the intervention family is related.
- Ledger update: `ying_2023_pair_025_chlorhexidine_wipes` added as a specific hold, superseding the earlier vague reconstruction row for routing.
- Decision: skip for current Figure 1 unless a separate pilot source reports matched sepsis/mortality values.

## 2026-05-08T21:07:00Z - Ying/Pediatric Depression Native-HR Hold

- Strategy: distinguish real matched replication evidence from values that cannot enter the current D/N plot metric.
- Inputs checked: Ying pair 33 pediatric depression relapse-prevention CBT, mirrored PMC HTML/parsed text, and the existing staged row in `scripts/ingest_ying_partial_reconstruction.py`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the larger RCT explicitly says the 46-adolescent pilot led to the larger trial. The pilot reports primary time-to-relapse HR=8.80 for medication management versus medication management plus CBT. The larger RCT reports relapse HR=0.313 for medication management plus CBT versus medication management among 144 continuation-phase participants.
- Hold reason: this is a strong matched pair, but both values are Cox hazard ratios/time-to-event estimates. The current Figure 1 D/N contract has no accepted HR-to-d conversion for this row.
- Ledger update: `ying_2023_pair_033_pediatric_depression_relapse` added as `native_only`, superseding the vague reconstruction row for routing.
- Decision: keep staged for a future native-effect/survival-effect analysis; do not promote to current Figure 1 unless a defensible HR-to-d mapping is adopted.

## 2026-05-08T21:08:30Z - Ying/CAPABLE Disability Native-Metric Hold

- Strategy: check whether source-reported pilot d values can map to a source-reported full-trial d value without inventing a conversion.
- Inputs checked: Ying pair 100 CAPABLE, Europe PMC abstract records, and newly mirrored PMC HTML files under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/capable_disability/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the larger RCT explicitly cites the randomized pilot as underpowered and says the current RCT addressed that limitation. The pilot reports source-computed Cohen d values for ADL and IADL disability changes: 0.63 and 0.62. The larger trial reports primary ADL/IADL effects as negative-binomial ratios of means: adjusted ADL RR=0.70 and adjusted IADL RR=0.83.
- Hold reason: no current row because the full-trial effect is a native ratio-of-means metric, not a D/SMD, and approximate reconstruction from endpoint means and SEs would mix metrics with the pilot change-score d.
- Ledger update: `ying_2023_pair_100_capable_adl_disability` added as `native_only`, superseding the vague reconstruction row for routing.
- Decision: keep for a future native disability-effect or conversion-methods analysis; do not promote to current Figure 1 without an accepted ratio-of-means-to-d route.

## 2026-05-08T21:10:00Z - Ying/MCGP Within-Group Effect Hold

- Strategy: guard against treating source-reported within-group d values as 1:1 between-group replication effects.
- Inputs checked: Ying pair 82 meaning-centered group psychotherapy for advanced cancer, Europe PMC abstract records, mirrored PMC HTML, and parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/mcgp/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the larger RCT explicitly follows prior MCP pilot RCTs. The pilot randomized 90 patients to MCGP versus SGP and reports within-group d values for MCGP and SGP separately. The larger RCT randomized 253 patients and reports HLM group-by-time interactions plus descriptive within-group d values for each arm.
- Hold reason: the available d values are not between-group treatment effects. Promoting them would violate the Figure 1 1:1 contrast rule by comparing within-arm change rather than MCGP versus SGP.
- Ledger update: `ying_2023_pair_082_mcgp_spiritual_wellbeing` added as a specific hold, superseding the vague reconstruction row for routing.
- Decision: skip for current Figure 1 unless a source-backed between-group standardized model effect is recovered.

## 2026-05-08T21:17:53Z - Ying/Integrated Diabetes Depression Metric-Drift Hold

- Strategy: back-process a real pilot-to-larger-trial sequence without rescuing it through mixed outcome metrics.
- Inputs checked: Ying pair 83 integrated diabetes/depression treatment, mirrored PMC HTML and parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/pair083_diabetes_depression/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the larger trial cites the 58-participant pilot and says a pilot study was conducted. The pilot reports exact 6-week >=80% medication-adherence values plus 12-week HbA1c and CES-D post-treatment means. The larger trial reports exact 12-week HbA1c threshold, PHQ-9 remission, HbA1c change, and PHQ-9 change values; adherence improved, but exact adherence values are only in Figure 2 in the checked source.
- Hold reason: no exact common value metric is available in text/table across both papers. A row would require mixing pilot post scores with larger-trial change scores, CES-D with PHQ-9, or tabled pilot adherence with figure-only larger-trial adherence.
- Ledger update: `ying_2023_pair_083_integrated_diabetes_depression` added as a specific hold, superseding the vague reconstruction row for practical routing.
- Decision: skip for current Figure 1 unless exact larger-trial adherence values are recovered from a data/table source, or a future policy explicitly admits metric-drift sensitivity rows.

## 2026-05-08T21:23:54Z - Ying/SNAP Large-vs-Small Weight Rescue

- Strategy: test an apparent reject for a strict matched early timepoint before discarding it.
- Inputs checked: Ying pair 75 SNAP weight-gain prevention, mirrored PMC HTML/parsed text, Europe PMC records, and newly mirrored pilot CONSORT Figure 1 under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/snap_weight/`.
- Included-row delta: +1 current Figure 1 D/N row after regeneration/checks.
- New row: `ying_2023_pair_075_snap_large_vs_small_weight_16wk_4mo`.
- Source evidence: the pilot states it was conducted in preparation for a large-scale trial. The pilot randomized 52 adults, with the CONSORT figure showing 27 assigned to Small Changes and 25 to Large Changes, and reports 16-week weight change of -3.5 +/- 3.1 kg for Large Changes versus -1.5 +/- 1.8 kg for Small Changes. The larger SNAP RCT cites the pilot, randomized 200 to Small Changes and 197 to Large Changes, and reports 4-month weight losses of -3.60 (SE 0.22) kg and -1.48 (SE 0.23) kg.
- Conversion: Hedges g from pilot arm mean/SD/N summaries and from larger-trial model mean SEs with arm Ns. Pilot D = 0.784956; replication D = 0.667085.
- Caveat: sensitivity-grade because the larger RCT includes a third control arm and has a 3-year average primary endpoint; this row uses only the Large-vs-Small early end-of-program contrast matching the pilot timing.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,724 root rows, 2,055 D/N-included rows, 0 critical invariant violations and 0 warnings for the 43 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Ledger update: `ying_2023_pair_075_snap_large_vs_small_weight_16wk_4mo` added as promoted, superseding the prior vague reconstruction row for practical routing.
- Decision: promote one row only. Do not add control comparisons, the 3-year primary endpoint, 2-year endpoint, obesity incidence, >=1 lb gain, or behavioral-process outcomes as separate Figure 1 rows.

## 2026-05-08T21:29:36Z - Ying/TMD Worst Facial Pain Rescue

- Strategy: replace a vague prior reconstruction row after direct PMC HTML rescue exposed the needed full-text table.
- Inputs checked: Ying pair 40 whole-system traditional Chinese medicine for temporomandibular disorders, Europe PMC records, mirrored PMC HTML, and pandoc-parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/tmd/`.
- Included-row delta: +1 current Figure 1 D/N row after regeneration/checks.
- New row: `ying_2023_pair_040_tmd_tcm_worst_facial_pain`.
- Source evidence: the pilot is an earlier whole-system TCM/NM versus specialty-care TMD trial; the larger stepped-care RCT describes lessons from that pilot and uses TCM for the same condition. The pilot reports adjusted end-of-treatment worst-facial-pain difference for TCM versus specialty care of -1.11 +/- 0.43, with end-of-treatment Ns 42 and 50 for the TCM and specialty-care arms. The larger Table 4 reports the same worst-facial-pain short-term TCM-versus-self-care effect of -0.58 (SDE 0.29), and Table 3 supports combined allocation-period counts of TCM 81 versus self-care 82 for the SMD conversion.
- Conversion: Hedges g inferred from reported mean-difference standard errors and effect-estimate Ns. Pilot D = 0.535790; replication D = 0.311848.
- Caveat: sensitivity-grade because the larger trial used adaptive stepped-care/minimization and combined short-term allocation periods, rather than a simple parallel two-arm TCM-versus-care design.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,725 root rows, 2,056 D/N-included rows, 0 critical invariant violations and 0 warnings for the 44 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Ledger update: `ying_2023_pair_040_tmd_tcm_worst_facial_pain` added as promoted, superseding the prior vague reconstruction row for practical routing.
- Decision: promote one worst-facial-pain row only. Do not add naturopathic medicine, characteristic facial pain, average pain, social interference, response percentages, trajectory groups, or long-term outcomes as extra Figure 1 rows.

## 2026-05-08T21:32:28Z - Ying/Reparixin Islet-Transplant Hold

- Strategy: distinguish real phase-2 to phase-3 follow-up evidence from source values that are not extractable as a matched current Figure 1 D/N row.
- Inputs checked: Ying pair 107 reparixin/CXCR1-2 inhibition in islet transplantation, Europe PMC records, mirrored PMC HTML, and parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/reparixin/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the pilot says a phase-3 trial had commenced to confirm the pilot results. The phase-3 paper says the pilot finding prompted the phase-3 study. The pilot initially randomized 7 patients, 4 reparixin and 3 control, then after early results the protocol was amended so additional patients received reparixin only. The phase-3 trial randomized 51 patients and reports primary C-peptide AUC analysis sets of 27/18 and 24/15, plus secondary insulin-independence counts.
- Hold reason: the pilot's exact clinical efficacy values are narrative/figure-level rather than tabled arm estimates, and the protocol-amended phase-2 design does not provide a clean matched randomized endpoint. The phase-3 primary C-peptide AUC values are not exposed as text/table arm estimates, and using secondary insulin-independence counts would mix endpoint and protocol stages.
- Ledger update: `ying_2023_pair_107_reparixin_islet_transplant` added as a specific hold, superseding the vague reconstruction row for practical routing.
- Decision: skip for current Figure 1 unless exact pilot arm-level C-peptide or insulin-independence values are recovered from a source table/data supplement and the protocol-amended pilot design is explicitly admitted.

## 2026-05-08T21:43:00Z - Ying/Migraine MBSR Control-Mismatch Hold

- Strategy: back-process the remaining vague Ying full-text-rescue candidate and test whether a numeric primary endpoint can be used without changing the matched-contrast standard.
- Inputs checked: Ying pair 169, Europe PMC abstract records for the pilot and larger trial, mirrored larger-trial PMC HTML/parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/migraine_mbsr/`, and Wiley DOI access attempt for the pilot.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the larger RCT cites the pilot and says pilot effect sizes informed the sample-size estimate. The pilot randomized 19 participants to MBSR versus usual care and reports primary migraine-frequency change of 1.4 fewer migraines/month for MBSR versus control. The larger trial randomized/analyzed 45 MBSR and 44 headache-education participants and reports primary 12-week migraine-day change of -1.6 versus -2.0, group difference -0.5.
- Hold reason: the exact migraine-frequency values are present, but the contrast changed from usual care to an active headache-education comparator. Promoting it would loosen the current matched-control rule.
- Ledger update: `ying_2023_pair_169_migraine_mbsr_control_mismatch` added as a specific hold, superseding the prior vague reconstruction row for practical routing.
- Decision: skip for current Figure 1 unless a future sensitivity policy admits usual-care-to-active-comparator control drift.

## 2026-05-08T21:46:00Z - Ying/CODES Native-Metric And Follow-Up Hold

- Strategy: separate true proof-of-concept-to-pragmatic-trial evidence from a metric/timepoint mismatch that would otherwise look tempting.
- Inputs checked: Ying pair 184 CODES/PNES CBT, Europe PMC records, mirrored PMC HTML/parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/codes/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the larger CODES RCT explicitly says the 2010 proof-of-concept RCT informed the larger design. The pilot randomized 66 participants and reports primary seizure-frequency model effects plus source effect sizes 0.75 at end of treatment and 0.42 at follow-up; it also reports seizure-freedom OR=3.125 at 6-month follow-up. The larger trial randomized 368 participants and reports primary monthly seizure frequency as IRR=0.78 at 12 months, plus seizure-freedom OR=1.77 for the last 3 months of the 12-month study.
- Hold reason: the matched primary endpoint is represented by native rate/model metrics without a current D conversion. The binary seizure-freedom fallback is secondary and has a follow-up-anchor mismatch, the same class of failure that was rejected for WebQuit.
- Ledger update: `ying_2023_pair_184_codes_pnes_native_and_timepoint_mismatch` added as a specific hold, superseding the vague reconstruction row for routing.
- Decision: skip for current Figure 1 unless a matched D/SMD conversion is adopted for seizure-frequency rate models or an exact same-timepoint binary endpoint is recovered.

## 2026-05-08T21:50:00Z - Ying/VICKY BioC Rescue Native-Concordance Hold

- Strategy: use alternate full-text acquisition before deciding whether a CAPTCHA-blocked local mirror should remain a vague rejection.
- Inputs checked: Ying pair 194 VICKY family-health-history tool, Europe PMC records, direct PMC HTML attempts, and newly mirrored NCBI BioC XML/parsed text under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/vicky_family_history/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the direct PMC HTML files are CAPTCHA/access pages, but NCBI BioC exposed value-bearing text and tables. The pilot randomized 35 VICKY and 35 MFHP participants and reports health-condition sensitivity total 49% versus 31%, IRR=1.59. The larger trial analyzed 135 VICKY and 138 MFHP participants and reports tool completion 97% versus 51%, plus Table 2 concordance IRRs for first-degree relatives 1.53 and second-degree relatives 2.50.
- Hold reason: the common primary/concordance family of results is native Poisson IRR/count-concordance without a current IRR-to-D conversion. The binary completion result is exact in the larger trial but is not a clean matched primary/table endpoint in the pilot, and the later tool is VICKY 2.0 with a changed condition set.
- Ledger update: `ying_2023_pair_194_vicky_native_concordance_hold` added as `native_only`, superseding the prior vague reconstruction row for practical routing.
- Decision: keep for future native IRR/concordance or health-literacy-tool projects; skip for current Figure 1 unless native count-concordance metrics are admitted or a strict matched binary completion endpoint is explicitly approved.

## 2026-05-08T22:07:00Z - RSESR Review Cue Already Accounted For

- Strategy: close out a high-value review-cue source-family lead after checking whether it still has unharvested current Figure 1 rows.
- Inputs checked: review cue `review_figure1_search_leads_95434678b310`, `FIGURE1_REPLICATION_PAIRS.tsv`, raw sports artifacts under `data/raw/replication_projects/sports/`, Metascience RSESR promoted CSVs, and Metascience RSESR promotion audits.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the root table already contains 34 RSESR/sports rows tied to DOI `10.1007/s40279-025-02201-w`: 19 direct sports supplemental-outcomes rows, 9 Metascience Observatory RSESR extension rows, and 6 Metascience Observatory RSESR rows. Of these, 31 pass the current D/N rule and 3 fail current D/N gates. The validated-extension audit has additional RSESR rows held as duplicates, failed current D/N, missing numeric fields, or not validated; the misc audit has six promoted RSESR rows plus held rows.
- Hold reason: this review-cue lead has already been converted into the active source family; chasing it again is a zero-yield duplicate unless the task is provenance hardening or source-result deduplication.
- Ledger update: `reviewcue_95434678_rsesr_already_integrated` added to `source-strategy-adjudication.tsv`, and `review_figure1_search_leads_95434678b310` is now overridden to `resolved_already_integrated_no_new_rows` / `skip_already_accounted_for` in `reviewcue-adjudication.tsv`.
- Decision: skip for goal3000 row discovery. Revisit only for provenance hardening, duplicate-source reconciliation, or a field-specific appendix.

## 2026-05-08T22:15:00Z - LLM Scenario Replication Context-Only Hold

- Strategy: evaluate a tempting 156-row source-family lead without relaxing the human-replication population standard.
- Inputs checked: review cue `review_figure1_search_leads_29d4d29c1ba2`, result-table child cue `review_figure1_search_leads_75bf3c17e235`, Nature article DOI `10.1038/s43588-025-00840-7`, and OSF node `j6wmn`. Mirrored evidence is under `data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/llm_scenario_replication/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the article describes replication of 156 scenario-based psychology/management experiments using three large language models. The OSF README says the workflow presents identical experimental conditions to GPT-4, Claude, and DeepSeek; the key fields include `human_size`, `human_effsize`, `LLM_effsize`, and `LLM_p_value`.
- Hold reason: the source contains human-original versus model-output effects, not original human study versus larger human replication samples. Counting it would change the population definition of Figure 1.
- Ledger update: `reviewcue_29d4d29c_llm_scenario_nonhuman_hold` added to `source-strategy-adjudication.tsv`; both the article cue and the Figshare/OSF child cue are overridden to `hold_nonhuman_llm_replication_not_current_figure1` in `reviewcue-adjudication.tsv`.
- Decision: skip for goal3000. Reuse for an LLM-as-participant project, nonhuman replication sensitivity appendix, or prompt/data provenance work.

## 2026-05-08T22:24:00Z - Review-Cue Known Source-Family Alias Cleanup

- Strategy: close review-cue rows that were still marked `advance` but map to source families already represented in the live root table or to context-only hubs/packages.
- Inputs checked: `reviewcue-adjudication.tsv`, `FIGURE1_REPLICATION_PAIRS.tsv`, source-family builder references, FReD rescue scan summaries, and local staged-source notes.
- Included-row delta: +0 current Figure 1 D/N rows.
- Decisions applied: RPCB, Many Labs/JOPD, Boyce/SRP, Decision-Market, EERP, FReD/FORRT, RPP, ego-depletion RRR, ReScience C, Direct Aid package file, and Bangladesh package file are now skipped for new row discovery in the regenerated reviewcue ledger.
- Evidence found: these families are either already live in root rows, source-family context/provenance objects, or blocked by site/lab fanout. Examples: RPCB has 118 live root rows; Boyce/SRP-related rows are already represented through Boyce, SRP, FReD, and Metascience routes; FReD/FORRT already dominates the live source-family surface and the current rescue scan has no high-precision bulk pool.
- Ledger update: `reviewcue_known_source_family_overlap_batch_20260508` added to `source-strategy-adjudication.tsv`; remaining `skip_in_goal3000=no` review-cue rows dropped from 27 to 15.
- Decision: do not spend new-row discovery time on these aliases. Use them only for provenance hardening, duplicate reconciliation, or context-source cataloging.

## 2026-05-08T22:31:00Z - Meta-Analysis Versus Multi-Lab Replication Hold

- Strategy: evaluate whether the Kvarven et al. comparison source can be transformed into current Figure 1 rows without changing row grain.
- Inputs checked: review cue `review_figure1_search_leads_6061ab8657b3`, Nature Human Behaviour article DOI `10.1038/s41562-019-0787-z`, OSF node `vw3p6`, and the mirrored OSF zip `data_and_code_kvarven_et_al.zip`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the article says it compares meta-analyses to large-scale preregistered multi-lab replications and identified 15 meta-replication pairs; the OSF package contains the corresponding data/code.
- Hold reason: the value grain is meta-analytic aggregate effect versus replication-project aggregate effect, not one original study/result versus one larger replication result. Many underlying replication projects are already live source families.
- Ledger update: `reviewcue_6061ab8657b3_meta_analysis_vs_multilab_hold` added to `source-strategy-adjudication.tsv`, and the review cue now has `skip_in_goal3000=yes`.
- Decision: skip for goal3000. Reuse only for a separate meta-analysis-vs-replication figure or as a crosswalk to known source families.

## 2026-05-08T22:39:00Z - Diener OSF Compilation Reanalysis Hold

- Strategy: inspect whether the Diener et al. OSF compilation is a new original-vs-replication result table or just a reusable data package.
- Inputs checked: review cue `review_figure1_search_leads_27d5775f87b9`, OSF node `qdx7p`, OSF file listings, `README.Rmd`, `Diener_et_al_replication_data.csv`, and `cleaned_diener_et_al_dataset.csv`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: OSF metadata says the page consists of available Diener et al. replication datasets and University of Minnesota analyses. The downloaded CSVs contain 1,171 participant rows across nine `study_site` values and variables such as ladder, feelings, needs, income, and demographics.
- Hold reason: no source-backed original-study D/N or original effect text is paired to a larger replication effect. Treating study sites as rows would create site-level fanout, and recomputing a new analysis would be a separate raw-data project rather than extracting an asserted Figure 1 pair.
- Ledger update: `reviewcue_27d5775f87b9_diener_osf_compilation_hold` added to `source-strategy-adjudication.tsv`, and the review cue now has `skip_in_goal3000=yes`.
- Decision: skip for goal3000 unless a source-backed original/replication result table is later identified.

## 2026-05-08T22:55:00Z - Olson/Fazio RRR Duplicate-Provenance Hold

- Strategy: finish an apparently promising RRR cue by acquiring source bytes, extracting the exact primary values, then checking against the live root table before counting it.
- Inputs checked: review cue `review_figure1_search_leads_ec299d9c57b4`, OSF node `hs32y`, OSF preregistered materials/code zip, OSF prior-study meta-analysis CSV and `cohen Ds from papers.R`, the Ohio State mirror of Olson and Fazio (2001), and the Ghent accepted manuscript mirror for Moran et al. (2021). Mirrored evidence is under `data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/olson_fazio_rrr/`.
- Included-row delta: +0 current Figure 1 D/N rows after duplicate check.
- Evidence found: the original paper reports Experiment 2 with 56 participants, six excluded, and explicit pleasantness-rating effect `t(48)=1.92`, `p=.03`; the OSF prior-meta-analysis table records analyzed `N=50`, `d=0.27`, `g=0.265846`. The replication accepted manuscript reports a high-powered `N=1478` close replication and primary Olson/Fazio-criterion result `n=1340`, `Hedges g=0.12`, 95% CI `[0.05, 0.20]`, `p=.002`.
- Hold reason: the same original/replication result is already plotted from the live FReD row `fred_soscisubmission38_1_1_1066`. Promoting the new individual-paper extraction would create a duplicate plotted pair. The newly mirrored files are useful for provenance hardening and for reconciling the original-effect conversion discrepancy, not for adding another row.
- Ledger update: `reviewcue_ec299d9c57b4_olson_fazio_rrr_duplicate_primary` added to `source-strategy-adjudication.tsv`; the review cue now has status `resolved_duplicate_existing_fred_row_provenance_hardening` and `skip_in_goal3000=yes`.
- Checks: `python scripts/scan_individual_replication_batch001_values.py --replace`; `python scripts/promote_individual_replication_value_scan.py --replace`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,725 root rows, 2,056 current D/N-included rows, 0 critical invariant violations, 116 existing warnings.
- Decision: skip for goal3000 row discovery; revisit only to attach source support to the existing FReD row or to settle the conversion policy for this pair.

## 2026-05-08T23:03:00Z - Fischer Att-SNARC RRR Code Snapshot Already Integrated

- Strategy: close an individual-worklist review cue that was actually a support artifact for a live RRR source family.
- Inputs checked: review cue `review_figure1_search_leads_889e202a4dd5`, the live root table, the promoted `rrr_colling_snarc__promoted_pairs.csv`, local `rrr_colling_2020` raw directory, and the review-cue receipt for the Zenodo/GitHub code snapshot.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the live root table already contains four included Colling et al. (2020) Att-SNARC rows for Fischer et al. (2003), covering the 250, 500, 750, and 1000 ms ISI outcomes with replication `N=1105`.
- Hold reason: the Zenodo/GitHub item is code/data support for the already integrated source family. Re-ingesting it as an individual paper source would duplicate plotted rows rather than add new 1:1 pairs.
- Ledger update: `reviewcue_889e202a4dd5_fischer_att_snarc_rrr_already_integrated` added to `source-strategy-adjudication.tsv`; the review cue now has status `resolved_rrr_colling_att_snarc_already_integrated` and `skip_in_goal3000=yes`.
- Check result: review-cue rows still open for goal3000 dropped from 12 to 11.
- Decision: skip for goal3000 row discovery; use only for source-file provenance or raw-data recomputation of the existing Att-SNARC rows.

## 2026-05-08T23:18:00Z - Kroll/Kosfeld Oxytocin Trust Row Ledger Closure

- Strategy: close a review-cue route that had already been promoted to the live Figure 1 table, so it does not remain in the open goal3000 queue.
- Inputs checked: review cue `review_figure1_search_leads_115f5ee33aea`, the live root table, `scripts/scan_individual_replication_batch001_values.py`, the promoted individual-replication CSV, the mirrored Kosfeld et al. original PDF/text, the PCI RR Stage 2 page, and the Kroll et al. OSF Stage 2 PDF/text under `data/raw/replication_projects/review_cue_figure1_search_leads/oxytocin_trust_kroll_2026/`.
- Included-row delta: +0 new rows in this pass; the strict row was already live as `individual_review_figure1_search_leads_115f5ee33aea_oxytocin_trust_registered_report_pooled_equivale`.
- Evidence found: Kosfeld et al. Table 1 reports trust-game investor mean transfers 9.6 versus 8.1, SDs 2.8 versus 3.1, and n=29 versus n=29. Kroll et al. identifies the work as a large-scale replication of Kosfeld et al. (2005), reports final own-data N=211 with 99 oxytocin and 112 placebo participants, and reports the standardized replication effect as Hedges g=-0.12 with 96% CI [-0.40, 0.17].
- Promotion decision: the live row uses original Cohen d=0.51 and N=58, replication magnitude D=0.12 and N=211. The pooled Kroll+Declerck N=532 estimate, Hedges g=-0.07, was checked and intentionally not used for the plotted row because it aggregates two replication studies when a single matched larger replication estimate is available.
- Ledger update: `reviewcue_115f5ee33aea_oxytocin_trust_kroll_2026_promoted` added to `source-strategy-adjudication.tsv`; the review cue now has status `promoted_current_figure1_row`, decision `promoted_to_current_figure1`, and `skip_in_goal3000=yes`.
- Check result: review-cue rows still open for goal3000 dropped from 11 to 10; live table remains 2,725 root rows and 2,056 current D/N-included rows.
- Decision: already counted; do not re-add. Reuse only for source-result provenance hardening or a separately scoped pooled-analysis sensitivity.

## 2026-05-08T23:38:00Z - Review-Cue Individual-Route Backfill Closure

- Strategy: stop redoing already checked individual-paper routes by importing the full individual-paper value-scan TSV into the goal3000 adjudication ledger, then closing the remaining review-cue routes with concrete source/blocker evidence.
- Inputs checked: `steps/individual_replication_papers/figure1/individual-paper-value-scan-batch001.tsv`, promoted individual-replication CSV, all review-cue routing rows, and newly mirrored minimal acquisition evidence for the five still-open review-cue routes.
- Included-row delta: +0 new rows in this pass; this was backfill/queue cleanup only.
- Ledger update: `source-strategy-adjudication.tsv` now includes 197 `individual_replication_paper_value_scan` rows, preserving prior ready/promoted/held/rejected individual-paper decisions with support paths and checksums where local files exist.
- Review-cue closures: thin-air prejudice, high-variability phoneme training, repetition/truth, false-belief action prediction, infant-directed speech, and Kroll/Kosfeld now close automatically from the value-scan/pro promoted artifacts. The five remaining open routes were closed as specific holds: victim-impact article blocked by T&F/Cloudflare, Caballero OSF `kdbsa` 404, earth-science citation OSF `u49zv` 404/planned registration, ECLS-K computational replication code, and Stroop data-only course assignment.
- Mirrored evidence added: `data/raw/replication_projects/lead_harvest/figure1_reviewcue_20260508/victim_impact_curriculum/`, `caballero_2021_replication/`, `earth_science_citation_replication/`, `ecls_k_replication/`, and `stroop_replication_dataset/`.
- Check result: `reviewcue-adjudication.tsv` has 80 rows and no `skip_in_goal3000=no` rows remaining; `source-strategy-adjudication.tsv` has 259 rows; `adjudication-ledger-backfill-summary.tsv` has 179 grouped summary rows.
- Decision: the review-cue backfill queue is closed for current goal3000 discovery. Future work should move to new structured/high-yield sources or manually supplied acquisitions, not re-open these routed leads.

## 2026-05-08T22:45:00Z - Live-Dedup Metascience Misc SSRP Duplicate Lesson

- Strategy: regenerate the Metascience miscellaneous candidate surface against the live root table, then test whether DOI-backed SSRP rows were genuinely new.
- Inputs checked: `data/raw/replication_projects/metascience_observatory/live_check_2026-05-08/api_fred_2026-05-08.json`, `FIGURE1_REPLICATION_PAIRS.tsv`, `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-dedup-candidate-surface-20260508.tsv`, `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-dedup-strong-singleton-candidates-20260508.tsv`, and `steps/corpus_results/figure1/goal3000_strategy_probe_20260508/metascience-misc-live-sourcealias-duplicate-diagnostics-20260508.tsv`.
- Included-row delta: +0 current Figure 1 D/N rows after rollback.
- Evidence found: 21 apparently DOI-new Metascience misc candidates were exact value aliases of existing root rows. Fourteen SSRP rows matched `ReplicationSuccess SSRP.rda`; the remaining strong singleton candidates matched existing FReD rows for SPRRR/math, behavioral priming, and moral hypocrisy publication-version/preprint aliases.
- Failure mode: DOI-pair dedup alone missed existing rows whose root DOI fields are blank or use a different publication version. The temporary Metascience SSRP allowlist was removed before finalizing, and the live table returned to 2,725 root rows and 2,056 current included rows.
- Ledger update: `metascience-misc-live-sourcealias-duplicate-diagnostics-20260508.tsv` records the rejected candidates, exact D/N aliases, existing root source dataset, and native root row ID. `metascience-misc-validated-promotion-audit.tsv` remains at 15 promoted rows and 416 `held_not_reviewed_for_misc_allowlist` rows.
- Checks: `python scripts/promote_metascience_observatory_misc_validated_pairs.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: live table is 2,725 root rows with 2,056 current D/N-included rows; invariant check reports 0 critical violations and 116 existing warnings.
- Decision: skip Metascience misc SSRP for goal3000. Future source probes must include source-alias/value-tuple duplicate checks, not only DOI-pair duplicate checks.

## 2026-05-08T23:55:00Z - Metascience Outside-Family Overlap Closure

- Strategy: classify strict numeric Metascience/FReD candidates outside the current source-family allowlist after the DOI-only duplicate screen produced apparent nonduplicates.
- Inputs checked: `metascience-outside-allowed-family-strict-numeric-candidates-20260508.tsv`, `api_fred_2026-05-08.json`, and the live `FIGURE1_REPLICATION_PAIRS.tsv`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: 160 strict numeric outside-family candidates were not a safe additive pool. The row-level ledger now classifies 68 exact DOI-pair duplicates, 71 existing-root value aliases, 12 Many Labs 5 duplicate/fanout source-family aliases, 4 Many Labs 2 similarity fanout aliases, 2 RPP aliases, 2 Many Labs 2 aliases, and 1 EPRP/XPHIR alias.
- Failure mode: rows that survive DOI-pair and exact value-tuple filters can still be duplicates through source-family aliases, publication-version differences, rounded values, blank root DOI fields, or Many Labs outcome fanout.
- Ledger update: `metascience-outside-allowed-family-adjudication-20260508.tsv` adds 160 row-level adjudications; `source-strategy-adjudication.tsv` now includes `metascience_outside_allowed_family_overlap_batch_20260508`.
- Checks: `python scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: live table remains 2,725 root rows with 2,056 current D/N-included rows; invariant check reports 0 critical violations and 116 existing warnings.
- Decision: skip this outside-family surface for goal3000 new-row discovery. Revisit only to replace/reconcile existing rows or to harden duplicate detection.

## 2026-05-09T00:10:00Z - Individual Search Batch008 Triage Holds

- Strategy: test a small high-relation, DOI-new individual-paper batch after the structured/corpus probes were mostly duplicate, native-only, or fanout surfaces.
- Inputs checked: `steps/searches/figure1/individualrepsearch-screening-hits-batch008.tsv`, mirrored Haeffel finger-flexion PMC HTML, mirrored Linares/Sellier phone-presence PLOS HTML plus S1/S4 supplement workbooks, and mirrored Rotella watching-eyes PLOS HTML.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: Haeffel (2025) is a real larger follow-up/replication context, but the reported direct-replication value is for positive affect while the summarized original target effect is a gender-by-condition BAS-Fun/persistence interaction. Linares and Sellier (2021) is a close replication of Przybylski and Weinstein (2013), but the extracted tables use multilevel/group-count fields and unstandardized fixed effects without a current accepted D conversion. Rotella et al. (2021) tests a broad watching-eyes effect family and does not identify one source-backed original result as the target.
- Failure mode: high relation-score titles and abstracts are still too weak without a matched outcome/model and a current D route. PLOS supplement extensions can also be misleading: the phone-presence `.docx` supplements were actually Excel workbooks.
- Ledger update: `source-strategy-adjudication.tsv` now includes `batch008_finger_flexion_haeffel_2025_outcome_mismatch`, `batch008_phone_presence_przybylski_weinstein_2021_native_multilevel_hold`, and `batch008_watching_eyes_rotella_2021_broad_effect_hold`.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`.
- Decision: skip these three for goal3000 row discovery. Reuse the mirrors for provenance, native-metric sensitivity work, or a separate broad-effect-family inventory.

## 2026-05-09T00:20:00Z - Hagen HCSP Deleted Main Sheet Hold

- Strategy: revisit a previously blocked high-yield structured-source candidate, Hagen Cumulative Science Project I, to see whether the Shiny/GitHub bundle or Google routes still expose the value-bearing table.
- Inputs checked: mirrored GitHub zip `github_master.zip`, app `app.R`, accessible codebook sheet mirror `148059e84112__edit.html`, and fresh main-sheet `export`, `htmlview`, and `pub?output=csv` rechecks under `data/raw/replication_projects/lead_harvest/gpt_many_replication_candidates_20260504/hagen_hcsp/recheck_2026-05-09/`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the app expects a main Google Sheet with columns for `N.Original`, `Effect.size.Original`, `Effect.size.Replication`, and replication CIs. The separate codebook remains accessible and mirrored, but the value-bearing main sheet is not in the GitHub zip.
- Blocker: the main Google Sheet ID `1VBnEGbanAt5yLXkpMGRGJWZeuw1TLNVudksgXyksHq0` now returns HTTP 410 and a deleted-file page on all checked routes.
- Ledger update: `source-strategy-adjudication.tsv` now includes `hagen_hcsp_main_sheet_deleted_20260509` with local access-attempt artifacts and checksums.
- Decision: skip Hagen HCSP for goal3000 until the deleted main sheet or an equivalent archived dataset is obtained.

## 2026-05-08T23:40:00Z - Protocol/Abstract Individual Holds Backfilled

- Strategy: preserve recent zero-yield checks before returning to row discovery, so attractive leads do not get re-opened from memory.
- Inputs checked: Social Exclusion Multi-Site OSF protocol and child nodes, IJzerman original source mirrors, Wang et al. 2025 biculturalism PMC full text, and the Scharf/Muller 2026 MMN in-class replication PubMed/Elsevier redirect mirrors.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the Social Exclusion lead has original-side IJzerman Study 1 value text but only protocol, power, and mock-analysis-plan replication materials; Wang et al. has numeric replication values but mixes original targets and uses original omnibus f benchmarks rather than the exact pairwise d; the MMN lead has abstract-only relation evidence and replication N=25 with no original source values or numeric replication effect.
- Failure mode: protocol/future-tense materials, conceptual-replication abstracts, and broad original-target summaries can look promising but fail the matched value-bearing 1:1 row requirement.
- Ledger update: `source-strategy-adjudication.tsv` now has 268 rows; the new explicit holds are `corpus_lead_social_exclusion_multisite_v5s6d_protocol_hold`, `individual_api_candidate_dae655618ec4c3be_bicultural_mainland_china_hold`, and `individual_api_candidate_4b3dfa6a8bcf03d8_mmn_inclass_abstract_only_hold`.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`.
- Decision: skip these for goal3000 until final result-bearing replication values or exact same-contrast original values are acquired; reuse as context/provenance leads only.

## 2026-05-08T23:52:00Z - Ying/EMDR Refugee HTQ Rescue

- Strategy: continue the strict Ying route, using a matched primary HTQ endpoint only because the pilot has local full-text table values and the larger trial abstract contains exact value-bearing effect-size text.
- Inputs checked: Ying pair 101 EMDR versus stabilisation pilot and larger refugee PTSD RCT, Europe PMC records, mirrored PMC/Paperclip pilot full text, and SHA256 manifest under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260508/emdr_refugee/`.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_101_emdr_refugee_htq`.
- Source evidence: pilot Table 3 reports completer post-treatment HTQ DSM-IV means 2.54 (SD 0.56) for EMDR (n=5) versus 3.04 (SD 0.25) for stabilisation (n=5). The larger trial abstract reports 72 randomized refugees and primary outcome effect sizes for CAPS and HTQ; the matched HTQ effect size is 0.20.
- Conversion: pilot D is Hedges g from post-treatment completer arm summaries; replication D stores the source-reported nonnegative HTQ magnitude 0.20.
- Caveat: sensitivity-grade because the pilot value is completer/post-treatment rather than ITT adjusted change, and the larger-trial value is currently supported by the value-bearing abstract record.
- Checks: `python scripts/ingest_ying_partial_reconstruction.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`; `python scripts/backfill_goal3000_adjudication_ledgers.py`.
- Check result: 2,726 root rows, 2,057 D/N-included rows, 0 critical invariant violations and 0 warnings for the 45 included Ying rows; full-table invariant check reports 0 critical violations and 116 existing warnings.
- Decision: counted as one sensitivity row. Continue this route only for matched endpoint rows with local value-bearing text; do not add SCID, HTQ total, HSCL, WHOQOL, diagnosis-loss, safety, or follow-up rows.

## 2026-05-09T00:25:00Z - Stale Duplicate Probe Backfill

- Strategy: close two attractive-but-already-checked zero-yield surfaces before further discovery: stale Metascience misc singleton/current-root nonduplicates and the HIV influential-studies PLOS individual-paper lead.
- Inputs checked: `metascience-misc-unreviewed-current-nonduplicates.tsv`, `metascience-misc-live-dedup-strong-singleton-candidates-20260508.tsv`, `metascience-misc-live-sourcealias-duplicate-diagnostics-20260508.tsv`, `individual-paper-value-scan-batch001.tsv`, `individual-paper-dedupe-baseline-batch005.tsv`, and `individual-paper-result-option-disposition-batch003.tsv`.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the Metascience singleton/nonduplicate filename is stale after later promotions and source-alias diagnostics; sampled candidates were already represented through FReD/Metascience/ReplicationSuccess aliases. The HIV lead was already rejected as a multi-study review/source-family context article, not one original result paired with one larger replication result.
- Ledger update: `source-strategy-adjudication.tsv` now includes `metascience_misc_singleton_current_root_duplicate_probe_20260509` and `batch008_hiv_influential_studies_prior_reject_confirmed`; source-strategy rows increased from 268 to 270 and backfill summary rows from 195 to 197.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`.
- Decision: do not reopen either surface for goal3000 row discovery without a regenerated live-root/source-alias dedupe pass or an explicit structured HIV source-family parser.

## 2026-05-09T00:35:00Z - Many Smiles Context Hold

- Strategy: preserve the checked Many Smiles Collaboration article/data package as a reusable context source without promoting a risky duplicate or broad-effect row.
- Inputs checked: `FIGURE1_REPLICATION_PAIRS.tsv`, mirrored Nature Human Behaviour article `many_smiles/8f4464df0b3d__s41562-022-01458-9.html`, and local `many_smiles/data.zip` with Fig1/Fig2/Fig3 source CSVs.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the data package has 19 country counts, 6,016 trial-level happiness-rating rows, and 3,878 participant-level happy-minus-neutral rows across pen-in-mouth, facial mimicry, and voluntary facial-action conditions.
- Failure mode: the source is a broad multi-condition facial-feedback replication project. The Strack pen-in-mouth target is already represented in the live root table via the Wagenmakers RRR aggregate, and adding Many Smiles as another row would require an explicit duplicate/replacement policy and a selected aggregation.
- Ledger update: `source-strategy-adjudication.tsv` now includes `many_smiles_collaboration_2022_context_hold_20260509`.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`.
- Decision: skip for goal3000 new-row discovery. Reuse only for facial-feedback context, Strack provenance hardening, or a separately scoped sensitivity analysis.

## 2026-05-09T00:45:00Z - Clinical Follow-Up Search Batch009

- Strategy: run a narrow clinical D-equivalent follow-up search lane after structured/corpus sources mostly resolved as duplicates, native-only rows, or fanout risks.
- Inputs checked: `reports/figure1_individual_replication_vast_search_execution_batch009_2026-05-05.md`, `steps/searches/figure1/individualrepsearch-query-log-batch009.tsv`, `steps/searches/figure1/individualrepsearch-screening-hits-batch009.tsv`, `steps/searches/figure1/individualrepsearch-api-batch009.json`, and batch009 raw Crossref/Europe PMC response JSON files.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: the metadata pass screened 258 hits and emitted 9 candidate units; deduplicating relation-score hits gave 10 unique high-relation titles because the critical-care systematic review appeared from two query routes. Scopolamine was already promoted as an individual-paper row. The other leads were review/context sources, future pilot-to-confirmatory language, observational or machine-learning validation, or confirmatory-trial language without a resolved original target/effect.
- Failure mode: clinical "confirmatory", "failed to confirm", and "external validation" language is too broad at metadata level. It often identifies a useful literature lead but not a source-backed 1:1 original-vs-larger-replication row with matched D/N values.
- Ledger update: `source-strategy-adjudication.tsv` now includes 10 `individual_search_batch009_metadata_adjudication` rows and increased from 271 to 281 rows; `adjudication-ledger-backfill-summary.tsv` increased to 206 rows.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`.
- Decision: do not promote from batch009 metadata. Reuse only as a clinical corpus/mining queue if a dedicated parser resolves explicit trial-pair mappings and D/N-convertible outcomes.

## 2026-05-09T00:55:00Z - In-Silico/Computational Corpus Holds

- Strategy: preserve two previously attractive corpus/database surfaces as explicit holds before reopening source discovery.
- Inputs checked: Nakagawa/Yang mirrored ecology/evolution repositories under `data/raw/corpus_candidates/nakagawa_yang/`, including the README files and processed SMD/Zr/lnRR/robustness CSVs; I4R public workbook mirrors `data/raw/replication_projects/i4r/meta_database.xlsx` and `.csv`; prior corpus/intake notes that implied these sources had been checked but not promoted.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: Nakagawa/Yang exposes effect-size, variance, SE, z, study, and meta-analysis identifiers across tens of thousands of processed rows, but no explicit original N/replication N pair table. I4R exposes computational-reproduction, coding-error, and robustness-check sheets with coefficients/SEs/p-values, not new-sample larger-replication D/N rows.
- Failure mode: corpus names that say replication can still be in-silico, computational, same-data, or robustness-check replication rather than the current Figure 1 unit.
- Ledger update: added `nakagawa_yang_ecoevo_insilico_se_only_hold_20260509` and `i4r_public_workbook_context_only_computational_reproduction_20260509` to the source-strategy backfill script.
- Decision: skip both for goal3000 row discovery. Reuse Nakagawa/Yang for an SE/meta-analysis comparator or ecology/evolution context; reuse I4R for computational reproducibility or robustness-change work.

## 2026-05-09T01:05:00Z - Ying Expressive-Writing Smoking-Cessation Rescue

- Strategy: add only a matched Ying pilot-to-full-scale row where both sides expose the same endpoint and follow-up window in local value-bearing abstracts.
- Inputs checked: Ying roster pair 001, Europe PMC mirrors `001_pilot_10_1002_jclp_20208.json` and `001_full_10_1080_14622200601078525.json`, live root duplicate search by DOI/title, and the current Ying reconstruction scripts.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_001_expressive_writing_24wk_ppa`.
- Evidence found: the pilot randomized N=30 per arm and reports 24-week biochemically confirmed 30-day abstinence of 20% for brief office intervention only versus 10% for expressive writing plus brief office intervention. The larger trial randomized n=99 brief office and n=97 expressive writing plus brief office and reports 24-week abstinence of 12% versus 11%.
- Conversion: Figure 1 uses nonnegative Chinn log(OR) d-equivalents from the source-reported percentages: D_original=0.447089, N_original=60; D_replication=0.054202, N_replication=196.
- Caveat: sensitivity-grade because the larger-trial abstract gives rounded percentages rather than exact event counts; full text should be revisited if exact 24-week counts are later acquired.
- Ledger update: `ying-candidate-adjudication.tsv` now includes `ying_2023_pair_001_expressive_writing_24wk_ppa`; Ying promoted rows increased from 45 to 46.
- Checks: `python -m py_compile scripts/ingest_ying_partial_reconstruction.py scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/ingest_ying_partial_reconstruction.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,727 root rows, 2,058 D/N-included rows, 0 critical invariant violations; Ying batch check has 46 included rows and 0 warnings, full-table check has 116 existing warnings.

## 2026-05-09T01:18:00Z - Ying Arthroplasty Decision-Aid Rescue

- Strategy: keep exploiting the Ying pilot/full-scale roster only where both local abstracts carry the same value-bearing endpoint, while marking endpoint caveats explicitly.
- Inputs checked: Ying roster pair 165, Europe PMC mirrors `165_pilot_10_1186_1471_2474_15_54.json` and `165_full_10_1016_j_joca_2015_07_024.json`, live root duplicate search by DOI/title, and the current Ying reconstruction scripts.
- Included-row delta: +1 current Figure 1 D/N row.
- New row: `ying_2023_pair_165_arthroplasty_decision_quality`.
- Evidence found: the pilot randomized 142 patients 71/71 and reports decision quality based on knowledge of 71% for the patient decision aid versus 47% for usual education. The larger trial randomized 343 patients 174/169 and reports good decision quality of 56.1% versus 44.5%.
- Conversion: Figure 1 uses nonnegative Chinn log(OR) d-equivalents from source-reported percentages: D_original=0.559890, N_original=142; D_replication=0.256983, N_replication=343.
- Caveat: sensitivity-grade because the matched endpoint is decision quality/knowledge; the definitive trial primary outcome was wait time and no wait-time D row is promoted from these abstracts.
- Ledger update: `ying-candidate-adjudication.tsv` now includes `ying_2023_pair_165_arthroplasty_decision_quality`; Ying promoted rows increased from 46 to 47.
- Checks: `python -m py_compile scripts/ingest_ying_partial_reconstruction.py scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/ingest_ying_partial_reconstruction.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; `make figure1-corpus-dn-check figure1-replication-pairs-table`; `python scripts/check_figure1_pair_invariants.py --batch-source-dataset 'Ying 2023 manual partial reconstruction' --strict-source-evidence --fail-on-critical`; `python scripts/check_figure1_pair_invariants.py --fail-on-critical`.
- Check result: 2,728 root rows, 2,059 D/N-included rows, 0 critical invariant violations; Ying batch check has 47 included rows and 0 warnings, full-table check has 116 existing warnings.

## 2026-05-09T01:35:00Z - Ying Checked-Not-Promoted Backfill

- Strategy: preserve the high-effort Ying abstract checks that were reviewed during the rescue pass but not promoted, so later sessions do not reopen them from memory.
- Inputs checked: 37 pilot/full-scale Europe PMC abstract pairs under `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/`, including the VBI pedometer, patient-navigation, nimodipine, SMARTER, LiFE falls, internet PTSD, e-couch, and clinical pilot-to-trial near misses.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: many of these are real pilot-to-larger-trial relations, but they fail current Figure 1 on the row grain: endpoint mismatch (6), endpoint/population mismatch (2), timepoint/endpoint mismatch (2), feasibility/no matched original effect (2), native metric without current D route, full-text value gaps, duplicate same-DOI routes, active comparator or noninferiority mismatch, ambiguous multi-outcome fanout, or missing original between-group values.
- Important held numeric case: Ying pair 212, VBI pedometer, has source-backed pilot and larger-trial accelerometer effects, but the pilot is 4 weeks and the larger trial is 3 months, so it remains held under the same-timepoint rule.
- Ledger update: `ying-candidate-adjudication.tsv` now has 77 rows, including 37 `ying_checked_not_promoted_backfill` rows; `adjudication-ledger-backfill-summary.tsv` now has 236 grouped rows.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; pandas read of `ying-candidate-adjudication.tsv` and `adjudication-ledger-backfill-summary.tsv`.
- Decision: skip these checked-not-promoted Ying candidates for goal3000 unless the ledger's row-specific `next_action` is satisfied, usually full-text exact values, an accepted native-metric conversion, or a policy change on timepoint/endpoint matching.

## 2026-05-09T01:48:00Z - Ying Promoted-Contract Backfill

- Strategy: audit the Ying ledger against the already-promoted Ying contract before continuing discovery, because valid promoted rows should not look like unreviewed candidates.
- Inputs checked: `data/derived/replication_pairs/harvest/promoted/ying_2023_partial_reconstruction__promoted_pairs.csv`, `FIGURE1_REPLICATION_PAIRS.tsv`, and the current `ying-candidate-adjudication.tsv`.
- Included-row delta: +0 current Figure 1 D/N rows; this was ledger-only backfill for rows already counted.
- Evidence found: 36 promoted Ying rows were present in the promoted contract/root table but lacked a candidate-level adjudication row. Pair 145 OCD/PFIT was one visible example: it looked like a fresh candidate in `ying-exact-value-candidate-scan.tsv`, but was already included in the root table.
- Ledger update: `ying-candidate-adjudication.tsv` now has 113 rows, including 36 `ying_promoted_contract_backfill` rows; all 47 rows in `ying_2023_partial_reconstruction__promoted_pairs.csv` now have a Ying ledger pair number.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; pandas promoted-vs-ledger anti-join returned `missing_promoted=0`.
- Decision: treat the Ying promoted contract as closed for rediscovery. Future Ying work should filter against the ledger plus promoted contract before candidate review.

## 2026-05-09T01:55:00Z - Ying High-Score Hold Backfill

- Strategy: preserve the highest-scoring remaining Ying exact-value scan checks that were reviewed but not promotable from the local abstract evidence.
- Inputs checked: 40 pilot/full-scale Europe PMC abstract pairs under `data/raw/replication_projects/lead_harvest/ying_2023/epmc_abstracts/`, including INTERACT, UK-HARP/SHARP, dexmedetomidine MIDEX/PRODEX, AIRWAYS-2, TRUST, PARITY, LT patch travellers' diarrhoea, Barrett screening, asthma patient advocates, ASPREE, idebenone/DELOS, HIP ATTACK, GaPP, RESET-IT, HARP, DOCC, and CALM.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: many candidates are real pilot-to-larger-trial relations, but the value-bearing abstract route usually exposes feasibility/process endpoints, surrogate-to-clinical endpoint shifts, dose/comparator fanout, native rate/noninferiority metrics, protocol-only original routes, or missing exact same-outcome values.
- Notable full-text targets: LT patch travellers' diarrhoea, idebenone/DELOS, GaPP, HARP, breathing-training, DOCC, asthma patient advocates, and RESET-IT remain plausible only if full text or supplements expose exact same-outcome values and a documented selector.
- Ledger update: `ying-candidate-adjudication.tsv` now has 153 rows, including 77 `ying_checked_not_promoted_backfill` rows; unlogged pairs in `ying-exact-value-candidate-scan.tsv` dropped from 88 to 48.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; pandas read of `ying-candidate-adjudication.tsv`; promoted-vs-ledger anti-join still returned `missing_promoted=0`.
- Decision: do not reopen these 40 from abstract evidence alone. Revisit only through a full-text extraction batch, not another title/abstract scan.

## 2026-05-09T02:05:00Z - Ying Secondary Abstract/Full-Text Hold Backfill

- Strategy: continue closing the Ying exact-value scan backlog and test the best remaining local-PMC candidate before classifying it.
- Inputs checked: 16 more Ying pairs from `ying-exact-value-candidate-scan.tsv`, including carpal tunnel release, influenza household NPIs, Healthy Homework, TASK stroke caregivers, HeartSleep CBT-I, hydrolyzed infant formula, ReMiND memory rehabilitation, E-FLIP, HOME Plus, pregnancy chocolate, ADDITION-Cambridge, MS spasticity app, electroacupuncture after back surgery, glaucoma MI, BCI cognitive training, and SWITCH screen-time intervention.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: Healthy Homework had PMC full text on both sides and was mirrored under `data/raw/replication_projects/lead_harvest/ying_2023/full_text_rescue_20260509/healthy_homework/`; it remains held because the pilot reports a raw all-day steps/day effect while the larger trial reports domain/timepoint-specific GLMM coefficients. Other candidates were held for missing exact values, multiarm/cluster selectors, population/intervention shifts, feasibility endpoints, or native metric policy gaps.
- Ledger update: `ying-candidate-adjudication.tsv` now has 169 rows, including 93 `ying_checked_not_promoted_backfill` rows; unlogged pairs in `ying-exact-value-candidate-scan.tsv` dropped from 48 to 32.
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; pandas read of `ying-candidate-adjudication.tsv`; Healthy Homework row includes local mirrored full-text paths and checksums.
- Decision: remaining Ying backlog is lower-yield. Promote only if a full-text extraction exposes exact same-endpoint D/N values; otherwise finish backfill as holds rather than re-reviewing abstracts.

## 2026-05-09T02:15:00Z - Ying Exact-Value Scan Backlog Closed

- Strategy: finish logging the remaining Ying scan pairs so the exact-value scan is no longer a rediscovery queue.
- Inputs checked: final 32 unlogged scan pairs from `ying-exact-value-candidate-scan.tsv`, including AVATAR, SMS smoking cessation, pediatric legacy intervention, restorative yoga, NET WINS, HIRREM, SystemCHANGE transplant adherence, SMILE/Lightning Process, welfare-rights advice, guided imagery, CIVIC spinal cord injury, SPG/OSAS, adolescent physical activity, Kaledo, WISE, acupuncture, hylan, hydrocortisone PTSD, cancer symptom cluster, blood donor reactivation, and Kenyan school support.
- Included-row delta: +0 current Figure 1 D/N rows.
- Evidence found: several were close but still failed current row rules from local evidence. AVATAR needs original arm Ns/full text; CIVIC has same 2-year mortality but pilot arm denominators are not explicit in the checked local abstract; blood donor reactivation needs per-arm re-donation counts; HIRREM changes from wait-list usual care to sham placebo and a different follow-up window; SystemCHANGE full result is median/IQR adherence; several others are feasibility/protocol, multiarm selector, population, intervention, cluster, or endpoint mismatches.
- Ledger update: `ying-candidate-adjudication.tsv` now has 201 rows, including 125 `ying_checked_not_promoted_backfill` rows; every pair in `ying-exact-value-candidate-scan.tsv` now has a Ying ledger pair number (`remaining_scan_pairs=0`).
- Checks: `python -m py_compile scripts/backfill_goal3000_adjudication_ledgers.py`; `python scripts/backfill_goal3000_adjudication_ledgers.py`; pandas read confirmed `duplicate_candidate_ids=0`, `empty_paths=0`, and `remaining_scan_pairs=0`.
- Decision: treat Ying abstract/scan rediscovery as closed. The only viable future Ying work is targeted full-text extraction for explicit next-action rows, not another abstract scan.
