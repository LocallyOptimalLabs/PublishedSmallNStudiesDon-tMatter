# Figure 1 Individual Replication Vast Search Execution - batch008

- Run ID: `2026-05-05_individual_replication_vast_search_batch008`
- Query calls logged: 24
- Query calls with API errors: 0
- Raw hits screened: 120
- Relation-scored candidate units emitted: 24
- Recall probe surface checks passed: 0/0

## Route Counts

- `coverage_only`: 24

## Surface Hit Counts

- `europepmc`: 60
- `plos`: 60

## Query Surface Counts

- `europepmc`: 12
- `plos`: 12

## Outputs

- Query log: `steps/searches/figure1/individualrepsearch-query-log-batch008.tsv`
- Screened hits: `steps/searches/figure1/individualrepsearch-screening-hits-batch008.tsv`
- Recall probe results: `steps/searches/figure1/individualrepsearch-recall-probe-results-batch008.tsv`
- Candidate manifest: `steps/searches/figure1/individualrepsearch-api-batch008.json`
- Raw API responses: `steps/searches/figure1/individualrepsearch_api_batch008/raw/`

## Interpretation

This first execution is a metadata/API pass. It establishes relation-candidate discovery and recall logging, but it does not by itself verify values from local source bytes. Candidates emitted here should be resolved to original targets and full text/source objects before any row promotion.
