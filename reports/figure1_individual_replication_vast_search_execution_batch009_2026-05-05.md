# Figure 1 Individual Replication Vast Search Execution - batch009

- Run ID: `2026-05-05_individual_replication_vast_search_batch009`
- Query calls logged: 24
- Query calls with API errors: 0
- Raw hits screened: 258
- Relation-scored candidate units emitted: 9
- Recall probe surface checks passed: 0/0

## Route Counts

- `coverage_only`: 9

## Surface Hit Counts

- `crossref`: 144
- `europepmc`: 114

## Query Surface Counts

- `crossref`: 12
- `europepmc`: 12

## Outputs

- Query log: `steps/searches/figure1/individualrepsearch-query-log-batch009.tsv`
- Screened hits: `steps/searches/figure1/individualrepsearch-screening-hits-batch009.tsv`
- Recall probe results: `steps/searches/figure1/individualrepsearch-recall-probe-results-batch009.tsv`
- Candidate manifest: `steps/searches/figure1/individualrepsearch-api-batch009.json`
- Raw API responses: `steps/searches/figure1/individualrepsearch_api_batch009/raw/`

## Interpretation

This first execution is a metadata/API pass. It establishes relation-candidate discovery and recall logging, but it does not by itself verify values from local source bytes. Candidates emitted here should be resolved to original targets and full text/source objects before any row promotion.
