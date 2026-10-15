# Figure 1 Individual Replication Blocker Unblock Prompt

Copy this whole prompt into GPT Pro. It already includes the candidates to work; do not add anything manually.

You are helping complete rows for Figure 1 of a meta-science dataset about original findings and larger replication/follow-up attempts.

Context:
We have already built and run a broad search system for individual replication papers. The discovery system is finding real candidates. The current bottleneck is not broad search strategy. The bottleneck is converting candidate paper pairs into row-level evidence with enough source grounding to plot.

Do not spend your answer designing new generic search strategies. Do not return prose. Return only valid JSON.

Goal:
For each candidate, determine whether it can become a plotted Figure 1 row now, and if so extract enough row-level information to support it.

A candidate becomes a plotted row only when there is:

1. Affirmative evidence that the replication/follow-up paper is actually retesting a specific earlier paper/result.
2. A specific original study/result/outcome/contrast mapped to a specific replication study/result/outcome/contrast.
3. Original N and replication N.
4. Original effect and replication effect on a defensible Figure 1 scale.
5. Value-bearing source objects that can be mirrored locally: full-text article, PDF, PMC/HTML/XML, supplement, OSF/Figshare/Dataverse/Zenodo data, trial registry result, accepted manuscript, or authoritative report.

Current Figure 1 routes:

- strict_figure1a:
  Use when both original and replication are D/SMD-compatible. Acceptable inputs include Cohen's d, Hedges g, SMD, means+SDs+n, mean difference+pooled SD+n, or t/F/r with df and group n if conversion is documented.

- d_equivalent_figure1b:
  Use for comparative binary/clinical outcomes when event-count or OR/RR/RD inputs support conversion to d-equivalent. Prefer event counts by arm. If using OR/logOR/RR/RD, record assumptions and required baseline-risk inputs.

- native_only:
  Use when the replication relation is real and values/N are available, but the metric is not defensibly convertible to Figure 1 D/SMD or binary d-equivalent. Examples: regression interactions, moderation models, adjusted hazard ratios without conversion inputs, AUC/model validation, unclear multi-factor native outcomes.

- coverage_only:
  Use when the relation is real but public value-bearing source objects or exact values are missing.

- reject:
  Use when there is no matched original/replication result, the source is metadata-only, review-only, same-data reanalysis, computational reproduction only, no independent replication/follow-up sample, no comparator for a binary endpoint, or the replication N is not larger under current policy.

Important rules:

- Metadata-only is not enough.
- A citation is not enough.
- A DOI landing page is not enough unless it contains the actual value-bearing text.
- Do not promote from title/abstract alone unless the title/abstract contains the exact needed N/effect values.
- Do not collapse multiple outcomes or multiple original target studies into one row.
- Preserve the exact original text before cleaning values.
- If the replication paper has several experiments, choose the cleanest matched larger-N replication for the original target, or mark the candidate as needing more evidence.
- If the replication gives a pooled/meta-analytic effect across labs or studies, use it only if the paper clearly maps that pooled estimate to the original target and the aggregation level is defensible.
- If a value is taken from a planning/power-analysis statement rather than an original result table, explicitly flag that.
- Preserve signed effects in notes and verbatim text, but Figure 1 D should be a nonnegative magnitude unless explicitly stated otherwise.
- If original and replication effects use different contrasts, mark needs_more_evidence or reject. Do not mix unmatched contrasts.
- If replication N is not larger than original N for the matched contrast, mark reject unless there is a clearly defensible larger pooled replication estimate.
- Prefer source-reported D/Hedges g/SMD when available. Otherwise compute with an explicit formula.

Useful conversion formulas:

- Independent-groups t to d:
  d = t * sqrt(1/n1 + 1/n2)
- Approximate equal-groups t to d when only total N is known:
  d approximately equals 2t / sqrt(df)
  Use only if equal groups are reasonable and flag the assumption.
- F with 1 numerator df to t:
  t = sqrt(F), then use t-to-d route if n/df support it.
- r to d:
  d = 2r / sqrt(1 - r^2)
- OR to d-equivalent:
  d = log(OR) * sqrt(3) / pi
- Event counts to OR:
  OR = (treatment_events * control_nonevents) / (treatment_nonevents * control_events)
  then OR_to_d. Note zero-cell corrections if used.

Your task for each candidate:

1. Locate or identify the best value-bearing source objects for both original and replication.
2. Resolve the exact original target: paper, study/experiment, outcome, contrast, timepoint.
3. Resolve the exact replication target: paper, study/experiment, outcome, contrast, timepoint.
4. Extract original N/effect and replication N/effect with verbatim support.
5. Compute D or d-equivalent if needed.
6. Decide: ready_for_row, needs_more_evidence, native_only, coverage_only, or reject.
7. For any non-ready candidate, state the precise missing source object or value.

Return only valid JSON: an array of candidate decision objects. Use this schema exactly:

```json
[
  {
    "candidate_id": "",
    "decision": "ready_for_row|needs_more_evidence|native_only|coverage_only|reject",
    "replication_kind": "direct_replication|close_replication|clinical_followup|clinical_reversal|independent_validation|genetics_replication_cohort|other",
    "row_policy": "strict_figure1a|d_equivalent_figure1b|native_only|coverage_only|reject",
    "original": {
      "title": "",
      "authors_year": "",
      "doi": "",
      "pmid": "",
      "pmcid": "",
      "registry_id": "",
      "study_or_experiment": "",
      "outcome": "",
      "contrast": "",
      "timepoint": "",
      "population": "",
      "n": "",
      "n_by_arm": {},
      "effect": "",
      "effect_metric": "",
      "event_counts": {
        "treatment_events": null,
        "treatment_total": null,
        "control_events": null,
        "control_total": null
      },
      "verbatim_effect_text": "",
      "verbatim_n_text": "",
      "verbatim_selector_text": "",
      "source_url": "",
      "locator": ""
    },
    "replication": {
      "title": "",
      "authors_year": "",
      "doi": "",
      "pmid": "",
      "pmcid": "",
      "registry_id": "",
      "study_or_experiment": "",
      "outcome": "",
      "contrast": "",
      "timepoint": "",
      "population": "",
      "n": "",
      "n_by_arm": {},
      "effect": "",
      "effect_metric": "",
      "event_counts": {
        "treatment_events": null,
        "treatment_total": null,
        "control_events": null,
        "control_total": null
      },
      "verbatim_effect_text": "",
      "verbatim_n_text": "",
      "verbatim_selector_text": "",
      "source_url": "",
      "locator": ""
    },
    "relationship_evidence": {
      "evidence_type": "title_exact_replication|abstract_direct_replication|abstract_failed_replication|methods_original_study_mapping|methods_original_materials|table_pair_mapping|clinical_confirmatory_trial|clinical_reversal_followup|trial_registry_reference|repository_readme|other",
      "verbatim_text": "",
      "source_url": "",
      "locator": "",
      "strength_0_to_5": null
    },
    "conversion": {
      "route": "native_d|means_sds_to_d|t_to_d|f_to_d|r_to_d|event_counts_to_logor_to_d|or_to_d|rr_with_baseline_to_or_to_d|native_only|none",
      "formula": "",
      "computed_original_d": null,
      "computed_replication_d": null,
      "figure1_original_d_magnitude": null,
      "figure1_replication_d_magnitude": null,
      "assumptions": []
    },
    "source_objects_to_mirror": [
      {
        "url": "",
        "object_type": "html|pdf|pmc_xml|supplement|dataset|registry_json|accepted_manuscript|preprint|repository|other",
        "why_needed": ""
      }
    ],
    "blockers": [],
    "dedupe_or_overlap_notes": "",
    "notes": ""
  }
]
```

Candidates to work:

```json
[
  {
    "candidate_id": "IND-015",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Red-romance exact target and value-bearing replication source unresolved.",
    "candidate_name": "Red-romance preregistered replications",
    "candidate_route": "strict_figure1a",
    "current_local_scan_decision": "source_blocked_original_value_bearing_text_missing",
    "original_title": "Romantic Red: Red Enhances Men's Attraction to Women; plus related red-romance women-rating-men study",
    "original_doi": "",
    "replication_title": "Is Red Really Romantic? Two Pre-Registered Replications of the Red-Romance Hypothesis",
    "replication_doi": "10.1027/1864-9335/a000296",
    "outcome_or_result_option": "Red-romance preregistered replications",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "0.09",
      "N_replication": "242"
    },
    "current_blocker": "source_blocked_needs_manual_acquisition",
    "known_original_support_text": "Crossref metadata and references identify red-romance original targets including Elliot & Niesta (2008) and Elliot et al. (2010), but local bytes do not expose the exact original study-level attraction effect sizes and Ns needed for a matched row.",
    "known_replication_support_text": "Mirrored Crossref metadata for Lehmann and Calin-Jageman (2017), DOI 10.1027/1864-9335/a000296, reports two preregistered replications: men rating women, d = 0.09, 95% CI [-0.17, 0.34], N = 242; women rating men, signed d = -0.09, 95% CI [-0.30, 0.12], N = 360. Hogrefe full/PDF routes currently mirror Cloudflare challenge pages, not value-bearing article text.",
    "conversion_or_policy_note": "Do not promote from metadata alone. Replication D magnitudes are exposed in Crossref abstract text, but original D/N values and exact matched original study/outcome rows remain missing from local value-bearing bytes.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch001/IND-015/crossref_red_romance_10_1027_1864_9335_a000296.json | data/raw/replication_projects/individual_search_batch001/IND-015/hogrefe_red_romance_full_attempt.html | data/raw/replication_projects/individual_search_batch001/IND-015/hogrefe_red_romance_pdf_attempt.html | data/raw/replication_projects/individual_search_batch001/IND-015/red_meta_analysis_probe/pmc10480976_meta_analysis.html",
    "requested_gpt_action": "manual_acquisition_of_hogrefe_article_or_author_manuscript",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "IND-023",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "d_equivalent_figure1b",
    "prior_replication_kind": "clinical_followup",
    "local_verifier_action": "held",
    "local_reason": "Activated protein C event counts not mirrored in this batch.",
    "candidate_name": "Activated protein C severe-sepsis mortality follow-up",
    "candidate_route": "d_equivalent_figure1b",
    "current_local_scan_decision": "not_row_replication_analyzed_n_not_larger",
    "original_title": "Efficacy and Safety of Recombinant Human Activated Protein C for Severe Sepsis",
    "original_doi": "10.1056/NEJM200103083441001",
    "replication_title": "Drotrecogin Alfa (Activated) in Adults with Septic Shock",
    "replication_doi": "10.1056/NEJMoa1202290",
    "outcome_or_result_option": "Activated protein C 28-day mortality, PROWESS versus PROWESS-SHOCK",
    "current_numeric_fields_if_any": {
      "D_original": "0.1683",
      "N_original": "1690",
      "D_replication": "0.0624",
      "N_replication": "1680"
    },
    "current_blocker": "needs_event_counts_or_open_trial_source_objects",
    "known_original_support_text": "Mirrored PubMed XML for PMID 11236773 reports the PROWESS trial DOI 10.1056/NEJM200103083441001, 1690 randomized patients treated, 840 placebo and 850 drotrecogin alfa activated. Mortality was 30.8 percent in placebo and 24.7 percent in drotrecogin alfa activated, absolute risk reduction 6.1 percent, P = 0.005.",
    "known_replication_support_text": "Mirrored PubMed XML for PMID 22616830 reports PROWESS-SHOCK DOI 10.1056/NEJMoa1202290. At 28 days, 223 of 846 DrotAA patients (26.4%) and 202 of 834 placebo patients (24.2%) had died, relative risk 1.09, P = 0.31.",
    "conversion_or_policy_note": "This row remains held because the analyzed 28-day replication N (846 + 834 = 1680) is not larger than the original N = 1690, despite the broader trial randomization count being 1697. Convert binary mortality contrasts with abs(log(OR) * sqrt(3) / pi): original d = 0.1683 from reported percentages 0.247 and 0.308; replication d = 0.0624 from 223/846 versus 202/834.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch001/clinical_pubmed_sources/pubmed_clinical_followup_records_11794169_24635773_25272316_25992746_11236773_22616830_11794168_19318384.xml",
    "requested_gpt_action": "resolve_nejm_or_open_source_routes_and_extract_mortality_counts",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_006071e798115bf1",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Original four-condition crossover interaction does not match replication two-condition pro-intuition/pro-reflection contrast.",
    "candidate_name": "Shenhav/Rand/Greene intuitive mindset and belief in God",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_original_effect_not_sufficiently_exposed",
    "original_title": "Shenhav, Rand and Greene (2012)",
    "original_doi": "",
    "replication_title": "Does intuitive mindset influence belief in God? A registered replication of Shenhav, Rand and Greene (2012)",
    "replication_doi": "10.1017/s1930297500007348",
    "outcome_or_result_option": "Shenhav/Rand/Greene intuitive mindset and belief in God",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "373",
      "D_replication": "6.448",
      "N_replication": "858"
    },
    "current_blocker": "not_row_original_effect_not_sufficiently_exposed",
    "known_original_support_text": "Mirrored article says Shenhav et al. (2012; Study 3) randomly assigned 373 MTurk workers to four conditions and the current study omitted two conditions.",
    "known_replication_support_text": "Mirrored article reports a registered replication in Turkey and the main belief-in-God outcome means/SDs and t statistic.",
    "conversion_or_policy_note": "Open article was mirrored and the registered-replication relation is real. The article reports original Study 3 N = 373 across four conditions and replication results for two conditions, but it uses assumed/reanalyzed small d values for planning rather than the matched original reported effect for the exact plotted contrast.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/01_academicrepository_khas_edu_tr_handle_20_500_12469_2831_d0bd654fa705.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/02_www_cambridge_org_core_journals_judgment_and_decision_making_article_doe_a1ce03884c97.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/03_jbaron_org_journal_18_18412_jdm18412_html_76b3d2c676b7.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/04_doaj_org_article_5937e200778e46fa85dc65470859823c_568d6dfc514e.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/05_doaj_org_article_82a252b91a674344b6a5f8d0792f7774_5de1e476642e.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/06_api_osf_io_v2_registrations_734eu_f7ebd2ff263e.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/07_osf_io_dh5e8_c1df7be23f68.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/08_openalex_org_w2888851667_16b660aaccf6.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/09_www_cambridge_org_core_journals_judgment_and_decision_making_article_doe_0c3a74662f6a.html | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/original_attempts/shenhav_rand_greene_2012_jepg.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_006071e798115bf1/original_attempts/shenhav_rand_greene_2012_jepg.txt",
    "requested_gpt_action": "Extract Shenhav/Rand/Greene original two-condition effect and N for the intuitive-mindset belief-in-God target, then map to the replication t/N.",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_025c30471725eba5",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "close_replication",
    "local_verifier_action": "held",
    "local_reason": "Religious-priming source does not resolve a single original paper/outcome/effect.",
    "candidate_name": "Auditory religious cues and dishonest behavior",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_conceptual_extension_no_single_original_effect",
    "original_title": "",
    "original_doi": "",
    "replication_title": "Replicating and extending the effects of auditory religious cues on dishonest behavior",
    "replication_doi": "10.1371/journal.pone.0237007",
    "outcome_or_result_option": "Auditory religious cues and dishonest behavior",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": "408"
    },
    "current_blocker": "not_row_conceptual_extension_no_single_original_effect",
    "known_original_support_text": "Mirrored PLOS article frames the work as replicating and extending religious priming effects but cites several prior religious-prime/prosociality sources rather than resolving a single original D/N target.",
    "known_replication_support_text": "The article reports N = 408 and moderation by religiosity/ritual participation in a dishonest-behavior game.",
    "conversion_or_policy_note": "Do not promote without a single original paper, matched outcome, and original effect/N. Keep as context for religious-priming replication mining.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch004/api_candidate_025c30471725eba5/01_journals_plos_org_plosone_article_id_10_1371_journal_pone_0237007_f5db93457e71.html",
    "requested_gpt_action": "retain_as_context_source_until_exact_original_target_is_resolved",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_44137bf63c3bbdfa",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Schiller OSF registration lacks completed value-bearing replication results.",
    "candidate_name": "Schiller et al. (Nature, 2010) -> Registered Replication of Schiller et al. (Nature, 2010)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_protocol_or_repository_only",
    "original_title": "Schiller et al. (Nature, 2010)",
    "original_doi": "",
    "replication_title": "Registered Replication of Schiller et al. (Nature, 2010)",
    "replication_doi": "10.17605/osf.io/k2w4a",
    "outcome_or_result_option": "Schiller et al. Nature 2010 registered replication OSF record",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Triage resolved the target as Schiller et al. (Nature, 2010), but only the OSF registration DOI was routed.",
    "known_replication_support_text": "The mirrored/source URLs identify a Registered Replication of Schiller et al. record, not extracted result values.",
    "conversion_or_policy_note": "The candidate is an OSF registration/source package rather than a value-bearing replication article in this batch. It should remain a no-repull target until a completed paper/result source is resolved.",
    "source_object_urls_from_search": [
      "https://doi.org/10.17605/osf.io/k2w4a",
      "https://osf.io/k2w4a/",
      "10.17605/osf.io/k2w4a"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_44137bf63c3bbdfa/01_osf_io_k2w4a_c1df7be23f68.html | data/raw/replication_projects/individual_search_batch006/api_candidate_44137bf63c3bbdfa/02_osf_io_k2w4a_c1df7be23f68.html | data/raw/replication_projects/individual_search_batch006/api_candidate_44137bf63c3bbdfa/03_osf_io_k2w4a_c1df7be23f68.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_44137bf63c3bbdfa/doi_resolver__10_17605_osf_io_k2w4a__osf_io__c1df7be23f68.html",
    "requested_gpt_action": "resolve_completed_replication_article_or_results_package_before_value_extraction",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_49040530056b1fbf",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Education/conspiracy values and metric route unresolved.",
    "candidate_name": "van Prooijen (2017) -> Education and conspiracy beliefs: A replication of van Prooijen (2017)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "van Prooijen (2017)",
    "original_doi": "",
    "replication_title": "Education and conspiracy beliefs: A replication of van Prooijen (2017)",
    "replication_doi": "10.1002/acp.4037",
    "outcome_or_result_option": "Education and conspiracy beliefs replication",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1002/acp.4037"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_49040530056b1fbf/semantic_scholar_landing_page__10_1002_acp_4037__www_semanticscholar_org__8ce2c9e363df.html",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_4dc2cff8320f0b0e",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Sex-difference reaction original D/N and single focal outcome unresolved.",
    "candidate_name": "Reactions to female- versus male-favoring sex differences",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_replication_n_not_larger",
    "original_title": "Reactions to male-favoring vs. female-favoring sex differences: A pre-registered experiment and Southeast Asian replication",
    "original_doi": "10.1111/bjop.12463",
    "replication_title": "People react more positively to female- than to male-favoring sex differences: A direct replication of a counterintuitive finding",
    "replication_doi": "10.1371/journal.pone.0266171",
    "outcome_or_result_option": "Reactions to female- versus male-favoring sex differences",
    "current_numeric_fields_if_any": {
      "D_original": "0.50",
      "N_original": "492",
      "D_replication": "0.58",
      "N_replication": "303"
    },
    "current_blocker": "not_row_original_effect_and_d_route_not_sufficiently_exposed",
    "known_original_support_text": "Mirrored OSF original paper and supplementary tables report Study 1 N = 492 and the focal overall Reaction to Research Sex Favoured effect F(1, 488) = 31.90, p < .001, d = 0.50.",
    "known_replication_support_text": "Mirrored PMC/PLOS replication article reports a direct replication with final N = 303 and the focal overall-reaction main effect of Sex Favored, F(1, 299) = 24.48, p < .001, d = 0.58.",
    "conversion_or_policy_note": "Open PLOS/PMC article and OSF source files were mirrored, and the direct-replication relation is real. The matched focal overall-reaction contrast is source-backed, but the 2022 exact replication analyzed N = 303 versus original Study 1 N = 492, so it fails the current Figure 1 larger-replication rule.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/01_journals_plos_org_plosone_article_id_10_1371_journal_pone_0266171_7c8e7ffc22d0.html | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/02_pmc_ncbi_nlm_nih_gov_articles_pmc8967052_13d49c6d103e.html | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/03_pubmed_ncbi_nlm_nih_gov_35353872_31bee0960424.html | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/04_cronfa_swansea_bjop12463_accepted_manuscript_20260507.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/04_cronfa_swansea_record_51534_20260507.html | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/05_cronfa_swansea_51534_author_original_20260507.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/06_osf_6n5up_files_api_20260507.json | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/07_osf_ctnez_files_api_20260507.json | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/08_osf_6n5up_osfstorage_api_20260507.json | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/09_osf_original_paper_stewart_williams_2020_20260507.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/09_osf_original_paper_stewart_williams_2020_20260507.txt | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/10_osf_original_supplementary_tables_20260507.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/10_osf_original_supplementary_tables_20260507.txt | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/11_osf_original_study1_data_20260507.sav | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/12_osf_exact_replication_data_20260507.sav | data/raw/replication_projects/individual_search_batch006/api_candidate_4dc2cff8320f0b0e/manifest_sha256.tsv",
    "requested_gpt_action": "retain_as_context_until_original_effect_and_single_outcome_d_route_are_extracted",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_53e20f8627a320c7",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "close_replication",
    "local_verifier_action": "held",
    "local_reason": "Positive-affirmation target is plural/ambiguous and values not mirrored.",
    "candidate_name": "past findings regarding positive affirmations and self-esteem -> On the failure to replicate past findings regarding positive affirmations and self-esteem",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "past findings regarding positive affirmations and self-esteem",
    "original_doi": "",
    "replication_title": "On the failure to replicate past findings regarding positive affirmations and self-esteem",
    "replication_doi": "10.1016/j.jcbs.2020.03.003",
    "outcome_or_result_option": "Positive affirmations and self-esteem",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1016/j.jcbs.2020.03.003"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_53e20f8627a320c7/01_linkinghub_elsevier_com_retrieve_pii_s2212144719301103_bd49689bf85e.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_53e20f8627a320c7/doi_resolver__10_1016_j_jcbs_2020_03_003__linkinghub_elsevier_com__bd49689bf85e.html",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_64a39a53876c51c1",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "strict_figure1a",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Weapon-focus original focal cell Ns and final replication value table still need source-mapped extraction.",
    "candidate_name": "unresolved original target -> Four (and a Half) Preregistered Failures to Replicate the Weapon Focus Effect in Online Samples.",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_original_n_or_target_effect_missing",
    "original_title": "Pickel and Sneyd (2018; Experiment 2)",
    "original_doi": "",
    "replication_title": "Four (and a Half) Preregistered Failures to Replicate the Weapon Focus Effect in Online Samples.",
    "replication_doi": "10.1037/law0000469",
    "outcome_or_result_option": "Weapon focus effect online preregistered failures",
    "current_numeric_fields_if_any": {
      "D_original": "2.03",
      "N_original": "",
      "D_replication": "-0.138",
      "N_replication": "1316"
    },
    "current_blocker": "original_n_needed",
    "known_original_support_text": "Mirrored PMC article says the power analysis used Pickel and Sneyd (2018; Experiment 2; White/Neutral condition) target-description d approximately 2.03.",
    "known_replication_support_text": "Mirrored PMC article reports five preregistered experiments and random-effects meta-analysis of target-description accuracy g = -0.138.",
    "conversion_or_policy_note": "Open PMC article was mirrored and reports five preregistered experiments with total n = 1,316 plus a meta-analytic target-description g = -0.138. It also reports a source-planning original target-description d approximately 2.03 from Pickel and Sneyd (2018, Experiment 2), but this batch did not resolve the original paper's actual analyzed N and exact outcome row.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1037/law0000469",
      "https://pmc.ncbi.nlm.nih.gov/articles/PMC12610937/",
      "https://pubmed.ncbi.nlm.nih.gov/41234291/"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/01_psycnet_apa_org_443_doilanding_doi_10_1037_law0000469_64104e8822dc.html | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/02_pmc_ncbi_nlm_nih_gov_articles_pmc12610937_d5386ee1d706.html | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/03_pubmed_ncbi_nlm_nih_gov_41234291_9c3b5f3a6df6.html | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel2018_headers.txt | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel2018_pubmed_headers.txt | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel_sneyd_2018_attempt.html | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel_sneyd_2018_pubmed.html | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel_sneyd_2018_squarespace.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel_sneyd_2018_squarespace.txt | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/pickel_sneyd_2018_squarespace_headers.txt | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/NIHMS2094767-supplement-3.docx | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/data_analysis_script_output.zip | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/extracted/Analyses/Analyses/singlePaperMeta.qmd | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/extracted/Analyses/Cleaned Data/Exp 1 data.csv | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/extracted/Analyses/Cleaned Data/Exp 2 data.csv | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/extracted/Analyses/Cleaned Data/Exp 4a data.csv | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/extracted/Analyses/Cleaned Data/Exp 4b data.csv | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/extracted/Analyses/Output/Analyses/Single-Paper Meta-Analysis.html | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/osf_data_analysis_folder_files.json | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/osf_tz7nb_files_osfstorage.json | data/raw/replication_projects/individual_search_batch006/api_candidate_64a39a53876c51c1/supplement_osf/preregistration_deviation_table.docx | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_64a39a53876c51c1/openalex_landing_page_url__10_1037_law0000469__pubmed_ncbi_nlm_nih_gov__6685cfd787f7.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_64a39a53876c51c1/openalex_landing_page_url__10_1037_law0000469__pubmed_ncbi_nlm_nih_gov__a4d4de9df92d.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_64a39a53876c51c1/semantic_scholar_landing_page__10_1037_law0000469__www_semanticscholar_org__43f2b75ad98e.html",
    "requested_gpt_action": "Resolve Pickel and Sneyd (2018) Experiment 2 original N/effect and map it to the replication's target-description or lineup outcome.",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_705797b93ca7def0",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Money-priming SES target is moderation/native unless exact values are extracted.",
    "candidate_name": "Schuler and Wänke (2016) -> Does Subjective SES Moderate the Effect of Money Priming on Socioeconomic System Support? A Replication of Schuler and Wänke (2016)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "Schuler and Wänke (2016)",
    "original_doi": "",
    "replication_title": "Does Subjective SES Moderate the Effect of Money Priming on Socioeconomic System Support? A Replication of Schuler and Wänke (2016)",
    "replication_doi": "10.1177/1948550617740941",
    "outcome_or_result_option": "Money priming and socioeconomic system support",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1177/1948550617740941"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_705797b93ca7def0/crawford_etal_2017_money_priming_replication_pdf.pdf | data/raw/replication_projects/individual_search_batch006/api_candidate_705797b93ca7def0/crawford_etal_2017_money_priming_replication_pdf.txt | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_705797b93ca7def0/semantic_scholar_landing_page__10_1177_1948550617740941__www_semanticscholar_org__3ed038622535.html",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_74f56abca426fbc9",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Letter-priming original and replication N/effects missing.",
    "candidate_name": "the Results of Ciani and Sheldon (2010) -> Is Intelligence Enhanced by Letter Priming? A Failure to Replicate the Results of Ciani and Sheldon (2010)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "the Results of Ciani and Sheldon (2010)",
    "original_doi": "",
    "replication_title": "Is Intelligence Enhanced by Letter Priming? A Failure to Replicate the Results of Ciani and Sheldon (2010)",
    "replication_doi": "10.2466/04.03.pr0.112.2.533-544",
    "outcome_or_result_option": "Ciani and Sheldon letter priming and intelligence",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.2466/04.03.pr0.112.2.533-544"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_74f56abca426fbc9/openalex_landing_page_url__10_2466_04_03_pr0_112_2_533_544__pubmed_ncbi_nlm_nih_gov__c1cfdd48916c.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_74f56abca426fbc9/openalex_landing_page_url__10_2466_04_03_pr0_112_2_533_544__pubmed_ncbi_nlm_nih_gov__d6b55411ea53.html",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_b3869535651b5f0e",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Character morality source values unresolved.",
    "candidate_name": "Eden, Daalmans, and Johnson (2017) -> Character morality, enjoyment, and appreciation: a replication of Eden, Daalmans, and Johnson (2017)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "Eden, Daalmans, and Johnson (2017)",
    "original_doi": "",
    "replication_title": "Character morality, enjoyment, and appreciation: a replication of Eden, Daalmans, and Johnson (2017)",
    "replication_doi": "10.1080/15213269.2021.1884096",
    "outcome_or_result_option": "Character morality, enjoyment, and appreciation media replication",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1080/15213269.2021.1884096"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_b3869535651b5f0e/openalex_landing_page_url__10_1080_15213269_2021_1884096__osf_io__c1df7be23f68.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_b3869535651b5f0e/openalex_landing_page_url__10_1080_15213269_2021_1884096__researchrepository_wvu_edu__b62ea57de8cc.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_b3869535651b5f0e/wvu_character_morality_replication.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_b3869535651b5f0e/wvu_character_morality_replication_retry_20260507.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_b3869535651b5f0e/wvu_character_morality_replication_viewcontent_20260507.pdf",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_c49eb133d5977b06",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "strict_figure1a",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Rabbitt original analyzed N is missing and replication d values need scoring reconciliation.",
    "candidate_name": "Rabbitt (1968) Experiment 2 -> Recall of Speech is Impaired by Subsequent Masking Noise: A Replication of Rabbitt (1968) Experiment 2",
    "candidate_route": "strict_figure1a",
    "current_local_scan_decision": "manual_acquisition_needed_original_n",
    "original_title": "Rabbitt (1968) Experiment 2",
    "original_doi": "",
    "replication_title": "Recall of Speech is Impaired by Subsequent Masking Noise: A Replication of Rabbitt (1968) Experiment 2",
    "replication_doi": "10.1080/25742442.2021.1896908",
    "outcome_or_result_option": "Rabbitt Experiment 2 speech masking direct replication",
    "current_numeric_fields_if_any": {
      "D_original": "0.19",
      "N_original": "",
      "D_replication": "0.19",
      "N_replication": "200"
    },
    "current_blocker": "original_n_needed",
    "known_original_support_text": "Mirrored PMC replication reports the original effect as d = 0.19, but does not give the original total N for the focal result.",
    "known_replication_support_text": "Mirrored PMC replication reports a final analyzed replication sample of 200 and d = 0.19.",
    "conversion_or_policy_note": "Do not promote until original Rabbitt N is extracted from the original article or another value-bearing source.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1080/25742442.2021.1896908",
      "https://www.ncbi.nlm.nih.gov/pmc/articles/8262135",
      "https://openalex.org/W3122990348"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch001/api_candidate_c49eb133d5977b06/02_pmc_ncbi_nlm_nih_gov_articles_pmc8262135_f0add6db277d.html | data/raw/replication_projects/individual_search_batch001/api_candidate_c49eb133d5977b06/03_openalex_org_w3122990348_158469730ed2.html | data/raw/replication_projects/individual_search_batch001/api_candidate_c49eb133d5977b06/02_pmc_ncbi_nlm_nih_gov_articles_pmc8262135_5425c883081d.html | data/raw/replication_projects/individual_search_batch001/api_candidate_c49eb133d5977b06/02_pmc_ncbi_nlm_nih_gov_articles_pmc8262135_6dcd4fd4d23b.html | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/brown_rabbitt_pdf.pdf | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/brown_rabbitt_pdf.txt | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/cinii.html | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/doi.html | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/jina_doi_markdown.txt | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/jina_sage_markdown.txt | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/jina_sage_pdf_markdown.txt | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/pubmed.html | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/sage_full.html | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/original_attempts/sage_pdf.pdf | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/Preprint.pdf | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/Preprint.txt | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/Rabbitt_prereg.pdf | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/._data_analysis | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._.DS_Store | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._.Rhistory | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._Figure2.png | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._Figure2.tiff | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._RabbittAnalysis.R | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._correct_responses.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._exclude.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._longresponse.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/__MACOSX/data_analysis/._rabbitt_data_from_gorilla.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/.DS_Store | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/.Rhistory | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/Figure2.png | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/Figure2.tiff | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/RabbittAnalysis.R | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/correct_responses.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/exclude.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/longresponse.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis/data_analysis/rabbitt_data_from_gorilla.csv | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/data_analysis.zip | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/files.json | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/osf_qjbxw/node.json | data/raw/replication_projects/individual_search_batch002/api_candidate_c49eb133d5977b06/manual/rabbitt_replication_pmc.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_c49eb133d5977b06/embedded_pdf__1c22cd936e7e__nihms-1679219.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_c49eb133d5977b06/openalex_landing_page_url__10_1080_25742442_2021_1896908__dialnet_unirioja_es__12b96061995d.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_c49eb133d5977b06/semantic_scholar_landing_page__10_1080_25742442_2021_1896908__www_semanticscholar_org__15a2f15e1ff9.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_c49eb133d5977b06/semantic_scholar_open_access_pdf__10_1080_25742442_2021_1896908__pmc_ncbi_nlm_nih_gov__d4139a16a798.html",
    "requested_gpt_action": "Resolve Rabbitt (1968) Experiment 2 original analyzed N and confirm the exact target-description outcome that maps to the open preregistered weapon-focus replication.",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_ccd98d70dd2472bf",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "close_replication",
    "local_verifier_action": "held",
    "local_reason": "Name-priming conceptual replication needs exact outcome mapping and values.",
    "candidate_name": "Krause Et Al. (2012) -> Mixed Evidence for Name Priming Effects as a Measure of Implicit Self-Esteem: A Conceptual Replication of Krause Et Al. (2012)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "Krause Et Al. (2012)",
    "original_doi": "",
    "replication_title": "Mixed Evidence for Name Priming Effects as a Measure of Implicit Self-Esteem: A Conceptual Replication of Krause Et Al. (2012)",
    "replication_doi": "10.1521/soco.2021.39.5.591",
    "outcome_or_result_option": "Name priming effects as implicit self-esteem",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1521/soco.2021.39.5.591"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/01_osf_name_priming_data_20260507.rar | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/02_osf_name_priming_analysis_syntax_20260507.R | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/03_osf_name_priming_experiment_20260507.rar | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/article_attempts/jusepeitis_dissertation_name_priming_replication_20260508.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/article_attempts/jusepeitis_dissertation_name_priming_replication_20260508.txt | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/556db04dfdf99b26054b1768_ebapt_repl2012_2020-10-12_16h53.40.244.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/56d8ed30d13f6b000c542ce7_ebapt_repl2012_2020-10-12_16h45.04.903.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5702439e7a84480009b6413d_ebapt_repl2012_2020-10-12_16h20.52.339.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/58a0a74460cd820001e99d04_ebapt_repl2012_2020-10-12_17h04.00.305.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/58c537bfb101a7000129391a_ebapt_repl2012_2020-10-12_16h34.08.222.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/58d4ebdec8677b0001a2107b_ebapt_repl2012_2020-10-12_16h56.17.187.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/59bc3a373a9ab60001119730_ebapt_repl2012_2020-10-12_16h47.22.119.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5a0b3848844c7a00015e4cf5_ebapt_repl2012_2020-10-12_16h54.41.867.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5afdcfb796a88e0001ff3fdc_ebapt_repl2012_2020-10-12_16h34.57.973.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5b0d0f0ebd9c3100015655d9_ebapt_repl2012_2020-10-12_16h42.18.753.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5b648251bd56550001bf31fd_ebapt_repl2012_2020-10-12_16h39.01.760.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5be4b528453f3b000189eeb4_ebapt_repl2012_2020-10-12_16h00.53.439.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5be6b18edcdffd00012742ec_ebapt_repl2012_2020-10-12_16h46.52.881.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c1b7fbebdb7e80001834945_ebapt_repl2012_2020-10-12_15h29.36.061.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c338ac6c75f190001e7fb97_ebapt_repl2012_2020-10-12_15h16.40.479.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c3665ba25d5920001199bec_ebapt_repl2012_2020-10-12_16h39.00.149.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c3b07f0688b59000102d44e_ebapt_repl2012_2020-10-12_16h43.44.221.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c3d0d156d874c0001bd80f8_ebapt_repl2012_2020-10-12_16h52.33.723.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c79d035998fb70001efcf1e_ebapt_repl2012_2020-10-12_16h41.47.420.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5c854499f29fd90001a2c6c0_ebapt_repl2012_2020-10-12_16h51.12.470.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5cac76acd6a3130016e3542b_ebapt_repl2012_2020-10-12_16h46.15.376.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5cbf710909dc4a001c1af7b5_ebapt_repl2012_2020-10-12_15h42.31.957.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5cddd8482f24b70018d1a57d_ebapt_repl2012_2020-10-12_16h42.05.302.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5cfceedaac238700182fd78b_ebapt_repl2012_2020-10-12_16h50.03.363.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5d2f449b9f98c5001a6c3598_ebapt_repl2012_2020-10-12_16h30.37.780.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5d53bc573d414c0001f3f007_ebapt_repl2012_2020-10-12_15h20.01.217.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5d6fda2bde432b0019b19ba7_ebapt_repl2012_2020-10-12_16h54.20.301.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5d79fdc2cf587a001a3c1d53_ebapt_repl2012_2020-10-12_16h53.15.303.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5da0f6e6b16ded001628cfd7_ebapt_repl2012_2020-10-12_16h56.48.338.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5da727bfc2a70a0011a128e0_ebapt_repl2012_2020-10-12_16h30.37.466.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5da7f34e25a3890016e536bb_ebapt_repl2012_2020-10-13_15h39.50.541.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5dd08cf019eecb169dc131ba_ebapt_repl2012_2020-10-12_16h55.58.229.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5dee2c94ad51834cf95af141_ebapt_repl2012_2020-10-12_17h02.18.624.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e0a1904e863562b1b299b3a_ebapt_repl2012_2020-10-12_16h31.15.459.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e19e8964af67a25fe2dedd9_ebapt_repl2012_2020-10-12_16h31.20.758.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e21ce87a79c2b4bd0b8f096_ebapt_repl2012_2020-10-12_15h35.58.406.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e2ccde0f6283e000bd3fc97_ebapt_repl2012_2020-10-12_16h36.47.512.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e5163d4873db0000b04b00f_ebapt_repl2012_2020-10-12_17h01.24.632.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e5832478c2b6f03f9acd234_ebapt_repl2012_2020-10-12_15h17.34.310.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e5baf4674c9533805ebae09_ebapt_repl2012_2020-10-12_16h38.54.348.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e5fbff6de7bcc2fc7f396db_ebapt_repl2012_2020-10-12_16h33.49.238.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e6d2835e0de62000922c8c2_ebapt_repl2012_2020-10-12_16h52.17.831.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e6e28b24acb203ddcbbc059_ebapt_repl2012_2020-10-12_16h42.29.934.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e8f3166c38d4a1fee4f08cc_ebapt_repl2012_2020-10-12_16h30.48.828.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5e94aa8e11d9b92eff5f1a16_ebapt_repl2012_2020-10-12_16h38.31.924.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea14bf64f71e2000acbc618_ebapt_repl2012_2020-10-12_15h38.16.681.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea563a366da51000b0a15e2_ebapt_repl2012_2020-10-12_15h57.41.142.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea76b989a31b913d6e8f809_ebapt_repl2012_2020-10-12_16h32.21.895.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea8286db500e122d8c9a19c_ebapt_repl2012_2020-10-14_09h29.06.979.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea94f21fb690102f181d74d_ebapt_repl2012_2020-10-12_16h40.22.823.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea9797bba9d14067376865d_ebapt_repl2012_2020-10-12_15h29.19.939.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ea9aae7ae93690e1ba7a99d_ebapt_repl2012_2020-10-12_16h50.19.389.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5eb181ce611ac50989d4bd03_ebapt_repl2012_2020-10-12_16h35.39.801.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5eb8ffbad25d258696a07c34_ebapt_repl2012_2020-10-12_15h20.24.922.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ebb16149ca0440dee9f9f61_ebapt_repl2012_2020-10-12_16h35.59.287.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ed102aa081ad5000960454c_ebapt_repl2012_2020-10-12_15h35.54.250.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ee109bf0173420dde18a960_ebapt_repl2012_2020-10-12_16h35.03.416.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5ee7acdb4e70e705cf1afe84_ebapt_repl2012_2020-10-12_16h53.29.010.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5eec7e3fc1a268000977b80b_ebapt_repl2012_2020-10-12_16h48.57.186.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5eee888b66da9e33cc3255a7_ebapt_repl2012_2020-10-12_16h57.09.170.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f06084122eb5a1227c74e31_ebapt_repl2012_2020-10-12_16h46.51.429.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f0ba1d25a4ca34cfb84d421_ebapt_repl2012_2020-10-12_16h37.09.293.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f0d9ede34d11c0176884a58_ebapt_repl2012_2020-10-12_16h59.06.247.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f0f2d844bd1730900000db5_ebapt_repl2012_2020-10-12_16h51.13.166.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f0f59fa7f396506b1c9d889_ebapt_repl2012_2020-10-12_16h50.45.599.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f17d20539078c0800cb4e7b_ebapt_repl2012_2020-10-12_16h58.27.197.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f17d428bd9d12188729a005_ebapt_repl2012_2020-10-12_15h08.53.559.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f17f19860e0fd09f24bdbfd_ebapt_repl2012_2020-10-12_16h02.27.800.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f185b5110646a00097ad68a_ebapt_repl2012_2020-10-12_16h38.31.688.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f1b69bb06c7d636c51e1917_ebapt_repl2012_2020-10-12_16h35.49.408.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f1c442e79caaa4b8a53eed3_ebapt_repl2012_2020-10-12_16h52.58.419.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f1d646d6807dd674c8666b0_ebapt_repl2012_2020-10-12_16h53.16.228.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f21d770d10e6915a51f1251_ebapt_repl2012_2020-10-12_16h43.18.560.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f23c2bb95e7ff1a1bd79a69_ebapt_repl2012_2020-10-12_16h55.38.916.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f256d997ee6c41efe46450c_ebapt_repl2012_2020-10-12_16h35.51.249.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f26ac012c3253000810f747_ebapt_repl2012_2020-10-14_09h29.47.836.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f2dba0d9b99b70d9372563d_ebapt_repl2012_2020-10-12_16h34.00.311.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f319af1ffb5b108c512a882_ebapt_repl2012_2020-10-12_15h39.54.806.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f3342fec5947d15604de5ea_ebapt_repl2012_2020-10-12_16h36.15.959.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f392e09e30eac47168adb72_ebapt_repl2012_2020-10-12_16h47.57.253.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f49837a1782f64f283c66c6_ebapt_repl2012_2020-10-12_16h40.30.336.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f4cd7926e1f3e8ed56bd215_ebapt_repl2012_2020-10-12_16h51.40.495.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f4d0bf47200c995a830e51f_ebapt_repl2012_2020-10-12_16h29.35.017.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f509ef3a8de8e21b09e82eb_ebapt_repl2012_2020-10-12_16h34.50.049.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f5e5ccbba0acc0d855f67e9_ebapt_repl2012_2020-10-12_16h44.48.706.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f6218d864b0fe2046c7d4a2_ebapt_repl2012_2020-10-12_16h31.39.318.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f6338275152ec3ed903be42_ebapt_repl2012_2020-10-12_16h49.54.247.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f68c08cf9c15f0333c6d281_ebapt_repl2012_2020-10-12_15h53.10.486.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f6cb7f8b5f3c709d49bd88b_ebapt_repl2012_2020-10-12_17h00.01.207.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f707ac93d9ed564a8b47939_ebapt_repl2012_2020-10-12_17h15.11.737.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f75d43fed909d28697acdc9_ebapt_repl2012_2020-10-12_17h30.10.493.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f75f5d98ef339016a98661d_ebapt_repl2012_2020-10-12_16h42.30.480.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f778cad5a7eb92e6365ebb9_ebapt_repl2012_2020-10-12_16h34.18.609.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f7c09657b93161f82ed7610_ebapt_repl2012_2020-10-12_16h33.45.914.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f8051b402daee04b8108440_ebapt_repl2012_2020-10-12_16h45.33.109.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/5f805610004fc9055b5e6885_ebapt_repl2012_2020-10-12_16h36.48.712.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/extracted_data_20260507/Prolific/prolific_export_5f76e60eedfdcc18da67cc96.csv | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/openalex_landing_page_url__10_1521_soco_2021_39_5_591__api_osf_io__8b5db1424b47.bin | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/openalex_landing_page_url__10_1521_soco_2021_39_5_591__osf_io__c1df7be23f68.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/osf_6awqn_children_api_20260507.json | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/osf_6awqn_files_api_20260507.json | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/osf_6awqn_osfstorage_api_20260507.json | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/osf_8nawp_osfstorage_api_20260507.json | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/osf_bnfsv_osfstorage_api_20260507.json | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_ccd98d70dd2472bf/osf_hbzv8_osfstorage_api_20260507.json",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_d51bbeeeb3386937",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "CBCA contextual-bias original and replication values unresolved.",
    "candidate_name": "the Criteria‐Based Content Analysis Condition in Bogaard Et al. (2014) -> Contextual Bias in Verbal Credibility Assessment: A Preregistered Direct Replication of the Criteria‐Based Content Analysis Condition in Bogaard Et al. (2014)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_duplicate_existing_contextual_bias_osf_raw_source_family",
    "original_title": "Contextual bias in verbal credibility assessment: Criteria-Based Content Analysis, Reality Monitoring and Scientific Content Analysis",
    "original_doi": "10.1002/acp.2959",
    "replication_title": "Contextual Bias in Verbal Credibility Assessment: A Preregistered Direct Replication of the Criteria-Based Content Analysis Condition in Bogaard et al. (2014)",
    "replication_doi": "10.1002/acp.70168",
    "outcome_or_result_option": "CBCA positive versus negative contextual-information score",
    "current_numeric_fields_if_any": {
      "D_original": "0.577068",
      "N_original": "32",
      "D_replication": "0.327149",
      "N_replication": "105"
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Mirrored OSF node f2xrv is titled as a preregistered direct replication of the CBCA condition of Bogaard et al. (2014). Its Original Study folder includes Original Dataset.sav. The mirrored Bogaard Analysis.R script filters the original data to conditie == 1 for the CBCA condition, sums 19 CBCA criteria for two negative-information statements and two positive-information statements, averages the two statements per valence, and computes Cohen's d as the paired mean difference divided by the standard deviation of paired differences. Recomputing from Original Dataset.sav gives 128 total cases, 32 CBCA-condition cases, positive mean = 12.984375, negative mean = 10.234375, mean paired difference = 2.75, paired-difference SD = 4.765467, t(31) = 3.264391, and dz = 0.577068.",
    "known_replication_support_text": "Mirrored OSF FinalData.xlsx has one DataFull sheet with 105 analyzed replication rows. Mirrored FinalData.R records the CBCA original effect estimate to_cbca = 0.577 and replication effect estimate tr_cbca = 0.327 for the replication Bayes factor. Recomputing the matched positive-versus-negative CBCA contrast from the Pos1/Pos2 and Neg1/Neg2 CBCA columns gives positive mean = 15.248652, negative mean = 13.959357, mean paired difference = 1.289295, paired-difference SD = 3.940999, t(104) = 3.352283, and dz = 0.327149.",
    "conversion_or_policy_note": "The mirrored OSF files resolve the candidate values, but the same underlying CBCA raw-data contrast is already represented in the current root table by the source family `Contextual bias in verbal credibility (OSF raw)` as `contextual_bias_cbca_scores`. Do not add a second plotted row for the same source-result; retain these candidate-local mirrors as support context if source_result rows are rebuilt.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1002/acp.70168"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/acp_70168.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/bogaard_2014_contextual_bias_accepted.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/bogaard_2014_contextual_bias_citeseerx.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/osf_f2xrv/original_dataset.sav | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/osf_f2xrv/osf_node_f2xrv_api_20260507.json | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/osf_f2xrv/replication_bogaard_analysis.R | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/osf_f2xrv/replication_finaldata.R | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/osf_f2xrv/replication_finaldata.xlsx | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/portsmouth_original.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/portsmouth_original_slash.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d51bbeeeb3386937/rg_replication.html",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_d98523e0ce3e5e0d",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held",
    "local_reason": "Online-image credibility exact Shen target and values unresolved.",
    "candidate_name": "Shen et al.'s (2019) Study on Online Image Credibility -> Contextual Changes, Credible Conclusions? A Direct and Conceptual Replication of Shen et al.'s (2019) Study on Online Image Credibility",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_direct_replication_n_not_larger_and_multi_claim_native",
    "original_title": "Fake images: The effects of source, intermediary, and digital media literacy on contextual assessment of image credibility online",
    "original_doi": "10.1177/1461444818799526",
    "replication_title": "Contextual Changes, Credible Conclusions? A Direct and Conceptual Replication of Shen et al.'s (2019) Study on Online Image Credibility",
    "replication_doi": "10.1080/15213269.2025.2595452",
    "outcome_or_result_option": "Online image credibility contextual direct/conceptual replication",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "3476",
      "D_replication": "",
      "N_replication": "634"
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Mirrored Taylor & Francis replication PDF/text identifies Shen et al. (2019) as the target and reports that the original online survey had 3,476 US-based participants aged at least 18 years. The paper states the original publication did not report individual effect sizes and mostly reported null results across multiple ANCOVA/predictor claims.",
    "known_replication_support_text": "The mirrored article states it conducted a direct replication with identical stimuli and US sampling plus a conceptual German/AI-stimulus replication. It reports final N = 634 for the direct replication and N = 513 for the conceptual replication, and summarizes claim-level outcomes rather than one matched D/SMD contrast.",
    "conversion_or_policy_note": "Do not promote: the focal direct replication N is smaller than the original N, and the result grain is a multi-claim ANCOVA/predictor replication without a single matched D/N row under current Figure 1 policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1080/15213269.2025.2595452"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch003/api_candidate_d98523e0ce3e5e0d/01_www_tandfonline_com_action_cookieabsent_26fcd1037997.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d98523e0ce3e5e0d/embedded_pdf__1fd1aa8d293c__Contextual_Changes__Credible_Conclusions__A_Direct_and_Conceptual_Replication_of_Shen_et_al._s__2019__Study_on_Online_Image_Credibility.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d98523e0ce3e5e0d/embedded_pdf__8f881b5c8e48__Contextual_Changes__Credible_Conclusions__A_Direct_and_Conceptual_Replication_of_Shen_et_al._s__2019__Study_on_Online_Image_Credibility.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d98523e0ce3e5e0d/embedded_pdf__8f881b5c8e48__Contextual_Changes__Credible_Conclusions__A_Direct_and_Conceptual_Replication_of_Shen_et_al._s__2019__Study_on_Online_Image_Credibility.txt | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d98523e0ce3e5e0d/embedded_pdf__d75f00c30965__Contextual_Changes__Credible_Conclusions__A_Direct_and_Conceptual_Replication_of_Shen_et_al._s__2019__Study_on_Online_Image_Credibility.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_d98523e0ce3e5e0d/openalex_landing_page_url__10_1080_15213269_2025_2595452__epub_ub_uni_muenchen_de__d405a57f2487.html",
    "requested_gpt_action": "Extract exact Shen online-image-credibility original and direct-replication effect/N values or classify as native-only/coverage-only.",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_f5027ea48e83c6e2",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "close_replication",
    "local_verifier_action": "held",
    "local_reason": "Darkness/dishonesty changed task and lacks matched original D/N.",
    "candidate_name": "Darkness and dishonesty conceptual replication using coin toss task",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_conceptual_changed_task_original_effect_missing",
    "original_title": "Experiment 1 of Zhong, Bohns, and Gino (2010)",
    "original_doi": "",
    "replication_title": "Darkness promotes dishonesty in a coin toss task: A pre-registered conceptual replication of Experiment 1 of Zhong, Bohns, and Gino (2010)",
    "replication_doi": "10.1371/journal.pone.0294484",
    "outcome_or_result_option": "Darkness and dishonesty conceptual replication using coin toss task",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "0.374",
      "N_replication": "102"
    },
    "current_blocker": "not_row_conceptual_changed_task_original_effect_missing",
    "known_original_support_text": "Mirrored PLOS article identifies Zhong, Bohns, and Gino (2010) Experiment 1 as the original target but does not provide a matched original D/N effect for the coin-toss endpoint.",
    "known_replication_support_text": "Mirrored PLOS article reports final replication N = 102, dark-condition reported-score M = 5.96 SD = 1.48 versus light-condition M = 5.39 SD = 1.56, t(100) = 1.885, p = .031, Cohen's d = 0.374.",
    "conversion_or_policy_note": "Do not promote because the replication changed the task from the original and the mirrored source does not expose the original matched effect size/N.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch004/api_candidate_f5027ea48e83c6e2/01_journals_plos_org_plosone_article_id_10_1371_journal_pone_0294484_b54c0aa73b72.html",
    "requested_gpt_action": "retain_as_context_source_until_original_effect_inputs_are_mirrored",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_f998e9bbe8b93e3b",
    "prior_gpt_decision": "needs_more_evidence",
    "prior_row_policy": "coverage_only",
    "prior_replication_kind": "independent_validation",
    "local_verifier_action": "held",
    "local_reason": "Cognitive-interview original target and matched replication outcome unresolved.",
    "candidate_name": "the effectiveness of the cognitive interview -> An independent replication of the effectiveness of the cognitive interview",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_needs_value_bearing_article",
    "original_title": "the effectiveness of the cognitive interview",
    "original_doi": "",
    "replication_title": "An independent replication of the effectiveness of the cognitive interview",
    "replication_doi": "10.1002/acp.2350050604",
    "outcome_or_result_option": "Cognitive interview effectiveness independent replication",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "",
    "known_replication_support_text": "",
    "conversion_or_policy_note": "Do not promote from metadata alone. The batch found affirmative replication-language evidence, but did not mirror enough value-bearing source text for a matched original effect, original N, replication effect, and replication N under the current Figure 1 row policy.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1002/acp.2350050604"
    ],
    "local_source_file_summary_or_paths": "",
    "requested_gpt_action": "manual_acquisition_or_repository_parse_if_prioritized",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_7c25e95e83db7d9a",
    "prior_gpt_decision": "native_only",
    "prior_row_policy": "native_only",
    "prior_replication_kind": "independent_validation",
    "local_verifier_action": "held_native_only",
    "local_reason": "Carotid real-world validation is not a single resolved RCT-to-follow-up event-count pair.",
    "candidate_name": "Randomized Controlled Trial Results for Carotid Endarterectomy -> Real-World Replication of Randomized Controlled Trial Results for Carotid Endarterectomy",
    "candidate_route": "native_only",
    "current_local_scan_decision": "source_blocked_clinical_observational_validation_not_current_pair",
    "original_title": "Randomized Controlled Trial Results for Carotid Endarterectomy",
    "original_doi": "",
    "replication_title": "Real-World Replication of Randomized Controlled Trial Results for Carotid Endarterectomy",
    "replication_doi": "10.1001/archneur.64.10.1496",
    "outcome_or_result_option": "Real-world replication of carotid endarterectomy randomized trial results",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Candidate title indicates a real-world replication/validation of RCT results, but the JAMA route was blocked by 403 and no matched event-count pair was mirrored.",
    "known_replication_support_text": "No value-bearing source object was mirrored locally for this batch.",
    "conversion_or_policy_note": "Keep as clinical context/manual acquisition; do not treat as Figure 1B without event counts and a specific trial-to-follow-up mapping.",
    "source_object_urls_from_search": [
      "https://doi.org/10.1001/archneur.64.10.1496"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_7c25e95e83db7d9a/openalex_landing_page_url__10_1001_archneur_64_10_1496__ora_ox_ac_uk__852d7e9b6654.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_7c25e95e83db7d9a/openalex_landing_page_url__10_1001_archneur_64_10_1496__ora_ox_ac_uk__e2e00e094e42.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_7c25e95e83db7d9a/openalex_landing_page_url__10_1001_archneur_64_10_1496__pubmed_ncbi_nlm_nih_gov__46a0c7f378ef.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_7c25e95e83db7d9a/openalex_landing_page_url__10_1001_archneur_64_10_1496__pubmed_ncbi_nlm_nih_gov__d8113d58532b.html",
    "requested_gpt_action": "manual_acquisition_if_clinical_real_world_validation_rows_are_in_scope",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_821f217890822e88",
    "prior_gpt_decision": "native_only",
    "prior_row_policy": "native_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held_native_only",
    "local_reason": "Color-priming target is interaction/native ANOVA without a matched strict SMD contrast.",
    "candidate_name": "the Mehta and Zhu (2009) color-priming effect on anagram solution times -> Failure to replicate the Mehta and Zhu (2009) color-priming effect on anagram solution times",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_native_interaction_original_effect_range_no_exact_d_route",
    "original_title": "Blue or red? Exploring the effect of color on cognitive task performances",
    "original_doi": "10.1126/science.1169144",
    "replication_title": "Failure to replicate the Mehta and Zhu (2009) color-priming effect on anagram solution times",
    "replication_doi": "10.3758/s13423-013-0548-3",
    "outcome_or_result_option": "Mehta and Zhu color-priming anagram solution times",
    "current_numeric_fields_if_any": {
      "D_original": "0.81",
      "N_original": "69",
      "D_replication": "2",
      "N_replication": "263"
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Mirrored replication PDF/text reports that Mehta and Zhu's first color-anagram experiment had n = 69 and that Cohen's d values ranged from 0.81 to 1.1 on p. 1227. It does not expose one exact source D for a single matched Figure 1 contrast.",
    "known_replication_support_text": "Mirrored Psychonomic Bulletin & Review article states it directly replicated Mehta and Zhu's anagram procedure with the same anagrams, instructions, and colors. It reports 269 participants recruited, 263 usable, and a nonsignificant Color x Word Type interaction: F(4,496) = 1.84, p = .12, eta^2 = .007; log-transformed solution times F(4,496) = 2.2, p = .06, eta^2 = .008.",
    "conversion_or_policy_note": "The value-bearing replication PDF/text is now mirrored, so this is not an acquisition blocker. Do not promote because the focal claim is the Background Color x Word Type interaction from a 3-by-3 mixed design; the replication reports eta-squared interaction statistics, while the original effect is exposed only as a d range rather than one matched D/N contrast.",
    "source_object_urls_from_search": [
      "https://doi.org/10.3758/s13423-013-0548-3"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_821f217890822e88/01_link_springer_com_article_10_3758_s13423_013_0548_3_error_cookies_not_su_6018d0080996.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_821f217890822e88/doi_resolver__10_3758_s13423_013_0548_3__link_springer_com__4c9d8d11264e.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_821f217890822e88/doi_resolver__10_3758_s13423_013_0548_3__link_springer_com__eb3e95f0a2bc.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_821f217890822e88/embedded_pdf__41aec7058c75__s13423-013-0548-3.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_821f217890822e88/embedded_pdf__41aec7058c75__s13423-013-0548-3.txt | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_821f217890822e88/openalex_landing_page_url__10_3758_s13423_013_0548_3__pubmed_ncbi_nlm_nih_gov__58712b75692d.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_821f217890822e88/openalex_landing_page_url__10_3758_s13423_013_0548_3__pubmed_ncbi_nlm_nih_gov__7dd9d03be342.html",
    "requested_gpt_action": "Decide whether the Mehta/Zhu anagram color-priming interaction can be converted to a defensible Figure 1 D row; if yes, return exact original and replication effect/N with formula.",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_bb6c827070cfa1f7",
    "prior_gpt_decision": "native_only",
    "prior_row_policy": "native_only",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "held_native_only",
    "local_reason": "Cockroach social-facilitation claim is an interaction with no current strict SMD route.",
    "candidate_name": "Cockroach audience by task-difficulty social-facilitation interaction",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_original_effect_not_statistically_mapped",
    "original_title": "Zajonc, Heingartner, and Herman’s (1969) Social-Facilitation Study",
    "original_doi": "",
    "replication_title": "Replicating Roaches: A Preregistered Direct Replication of Zajonc, Heingartner, and Herman’s (1969) Social-Facilitation Study",
    "replication_doi": "10.1177/0956797620902101",
    "outcome_or_result_option": "Cockroach audience by task-difficulty social-facilitation interaction",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "40",
      "D_replication": "",
      "N_replication": "120"
    },
    "current_blocker": "not_row_original_effect_not_statistically_mapped",
    "known_original_support_text": "Search/PDF snippets identify original Zajonc et al. N = 40 for the critical 2 x 2 interaction, but also note the original article did not provide a clear statistical test of the central interaction.",
    "known_replication_support_text": "The replication article is source-blocked locally by SAGE 403 in this batch; search snippets report preregistered target N = 120 and a direct replication of the audience by task-difficulty claim.",
    "conversion_or_policy_note": "Do not promote without a source-mapped original D/statistic for the central interaction; retain as a context/manual-acquisition lead.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "",
    "requested_gpt_action": "manual_acquisition_if_interaction_effects_become_in_scope",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_96a758378eb37b0e",
    "prior_gpt_decision": "reject",
    "prior_row_policy": "reject",
    "prior_replication_kind": "close_replication",
    "local_verifier_action": "rejected",
    "local_reason": "Rapid-naming task does not establish a matched original task/outcome pair.",
    "candidate_name": "in the rapid naming task -> Phonological priming: Failure to replicate in the rapid naming task",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "not_row_native_anova_original_effect_missing",
    "original_title": "in the rapid naming task",
    "original_doi": "",
    "replication_title": "Phonological priming: Failure to replicate in the rapid naming task",
    "replication_doi": "10.3758/bf03334046",
    "outcome_or_result_option": "Phonological priming rapid-naming failure",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": "60"
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Mirrored article states Experiment 1 tried to replicate the phonological priming effect reported by Hillinger (1980), and the discussion says the results coincide with Martin and Jensen's (1988) failure to obtain significant phonological or graphemic priming effects. It does not provide Hillinger's original N/effect as a D-scale row input.",
    "known_replication_support_text": "Mirrored Bulletin of the Psychonomic Society PDF/text reports Experiment 1 had 60 college students and no significant priming effect for words; Experiment 2 had 80 college students and again showed no advantage for graphemic or phonemic similarity over the unrelated condition.",
    "conversion_or_policy_note": "The replication article PDF/text is now mirrored, so this is not an acquisition blocker. Do not promote because the source reports native minF'/ANOVA-style lexical-decision/naming results and does not expose a matched original D/N effect from Hillinger (1980) or Martin and Jensen (1988).",
    "source_object_urls_from_search": [
      "https://doi.org/10.3758/bf03334046"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_96a758378eb37b0e/01_link_springer_com_article_10_3758_bf03334046_error_cookies_not_supported_298b26a951ab.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_96a758378eb37b0e/doi_resolver__10_3758_bf03334046__link_springer_com__3b1aab19bff8.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_96a758378eb37b0e/doi_resolver__10_3758_bf03334046__link_springer_com__acfd9f712379.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_96a758378eb37b0e/embedded_pdf__4a772153e936__BF03334046.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_96a758378eb37b0e/embedded_pdf__4a772153e936__BF03334046.txt | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_96a758378eb37b0e/openalex_oa_url__10_3758_bf03334046__link_springer_com__ce365607a87b.pdf | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_96a758378eb37b0e/semantic_scholar_landing_page__10_3758_bf03334046__www_semanticscholar_org__cb400cd20894.html",
    "requested_gpt_action": "Determine whether the phonological-priming rapid-naming paper is a valid close/direct row or should be rejected because the task differs from Hillinger's lexical-decision original.",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_9db26ff9b8058473",
    "prior_gpt_decision": "reject",
    "prior_row_policy": "reject",
    "prior_replication_kind": "close_replication",
    "local_verifier_action": "rejected",
    "local_reason": "Social-distance focal replication N is smaller than original under current larger-N rule.",
    "candidate_name": "Social-distance priming Study 1 near-versus-far food-judgment replication",
    "candidate_route": "strict_figure1a",
    "current_local_scan_decision": "not_row_replication_n_not_larger_or_original_effect_missing",
    "original_title": "Effects on Social and Food Judgments",
    "original_doi": "",
    "replication_title": "Priming of Social Distance? Failure to Replicate Effects on Social and Food Judgments",
    "replication_doi": "10.1371/journal.pone.0042510",
    "outcome_or_result_option": "Social-distance priming Study 1 near-versus-far food-judgment replication",
    "current_numeric_fields_if_any": {
      "D_original": "0.76",
      "N_original": "56",
      "D_replication": "",
      "N_replication": "44"
    },
    "current_blocker": "not_row_replication_n_not_larger_or_original_effect_missing",
    "known_original_support_text": "Mirrored PLOS paper Table 1 reports Williams and Bargh Study 4 d = 0.76, calculated from t = -2.86 assuming equal 28 participants per group.",
    "known_replication_support_text": "Mirrored PLOS paper reports Study 1 analyzed N = 71 after exclusions, with focal close/far cells 22 and 22; the focal replication N is therefore smaller than the original focal N.",
    "conversion_or_policy_note": "The clean focal contrast fails the current larger-replication-N rule. The companion Study 2 may be usable only after original Study 3 effect extraction.",
    "source_object_urls_from_search": [],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/01_journals_plos_org_plosone_article_file_id_10_1371_journal_pone_0042510_t_6c57bac0ed58.pdf | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/02_journals_plos_org_plosone_article_id_10_1371_journal_pone_0042510_b6712e218027.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/03_pubmed_ncbi_nlm_nih_gov_22952597_586846f50ecf.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/05_journals_plos_org_plosone_article_id_10_1371_journal_pone_0042510_b6712e218027.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/06_doaj_org_article_e8e46da29cce40e8a55999b5cda66f5d_d1a30f9535c8.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/07_pmc_ncbi_nlm_nih_gov_articles_pmc3430642_33c0ec5ac84f.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/08_openalex_org_w2106777508_158469730ed2.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/03_pubmed_ncbi_nlm_nih_gov_22952597_0e7131dc0940.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/03_pubmed_ncbi_nlm_nih_gov_22952597_47e83895724e.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/07_pmc_ncbi_nlm_nih_gov_articles_pmc3430642_d9760d492c6e.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/07_pmc_ncbi_nlm_nih_gov_articles_pmc3430642_f0e81aaab47f.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/original_williams_bargh_2008/crossref_10.1111_j.1467-9280.2008.02084.x.json | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/original_williams_bargh_2008/pmc_html.html | data/raw/replication_projects/individual_search_batch001/api_candidate_9db26ff9b8058473/original_williams_bargh_2008/pmc_xml.html",
    "requested_gpt_action": "do_not_promote_unless_policy_allows_smaller_focal_replication_or_original_study3_effect_is_extracted",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  },
  {
    "candidate_id": "api_candidate_fcdbe8ce78bf22a0",
    "prior_gpt_decision": "reject",
    "prior_row_policy": "reject",
    "prior_replication_kind": "direct_replication",
    "local_verifier_action": "rejected",
    "local_reason": "Duplicate Schiller OSF registration hit with no value-bearing results.",
    "candidate_name": "Schiller et al. (Nature, 2010) -> Registered Replication of Schiller et al. (Nature, 2010)",
    "candidate_route": "coverage_only",
    "current_local_scan_decision": "source_blocked_protocol_or_repository_only",
    "original_title": "Schiller et al. (Nature, 2010)",
    "original_doi": "",
    "replication_title": "Registered Replication of Schiller et al. (Nature, 2010)",
    "replication_doi": "10.17605/osf.io/8chqu",
    "outcome_or_result_option": "Schiller et al. Nature 2010 registered replication duplicate OSF record",
    "current_numeric_fields_if_any": {
      "D_original": "",
      "N_original": "",
      "D_replication": "",
      "N_replication": ""
    },
    "current_blocker": "value_bearing_source_object_needed",
    "known_original_support_text": "Triage resolved the target as Schiller et al. (Nature, 2010).",
    "known_replication_support_text": "The routed DOI is an OSF registration/package record and duplicates the Schiller registration family.",
    "conversion_or_policy_note": "Duplicate OSF registration/source-package hit for the Schiller replication family; no completed value-bearing source was resolved in this batch.",
    "source_object_urls_from_search": [
      "https://doi.org/10.17605/osf.io/8chqu",
      "https://osf.io/8chqu/",
      "10.17605/osf.io/8chqu"
    ],
    "local_source_file_summary_or_paths": "data/raw/replication_projects/individual_search_batch006/api_candidate_fcdbe8ce78bf22a0/01_osf_io_8chqu_c1df7be23f68.html | data/raw/replication_projects/individual_search_batch006/api_candidate_fcdbe8ce78bf22a0/02_osf_io_8chqu_c1df7be23f68.html | data/raw/replication_projects/individual_search_batch006/api_candidate_fcdbe8ce78bf22a0/03_osf_io_8chqu_c1df7be23f68.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_fcdbe8ce78bf22a0/doi_resolver__10_17605_osf_io_8chqu__osf_io__c1df7be23f68.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_fcdbe8ce78bf22a0/openalex_landing_page_url__10_17605_osf_io_8chqu__api_osf_io__7d77fd3ba84a.bin | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_fcdbe8ce78bf22a0/openalex_landing_page_url__10_17605_osf_io_8chqu__osf_io__c1df7be23f68.html | data/raw/replication_projects/individual_auto_mining_blockers/api_candidate_fcdbe8ce78bf22a0/openalex_oa_url__10_17605_osf_io_8chqu__osf_io__c1df7be23f68.html",
    "requested_gpt_action": "resolve_completed_replication_article_or_results_package_before_value_extraction",
    "expected_json_decision_values": "ready_for_row | needs_more_evidence | native_only | reject"
  }
]
```
