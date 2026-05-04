# Interface

Date checked: 2026-05-04.

## Purpose

This file defines research contracts for testing, validation, and benchmarks. It is not production code. Recommendation: expose validation through stable manifests and result records so data adapters, feature builders, models, backtesters, paper adapters, risk managers, and report generators can remain swappable. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://docs.pydantic.dev/latest/concepts/strict_mode/.

## Validation Manifest

Recommendation: every validation run should declare a manifest with `run_id`, `git_revision`, `created_at_utc`, `python_version`, `package_lock_id`, `data_fixture_id`, `symbols`, `time_range`, `horizons`, `feature_cutoff_policy`, `label_policy`, `cost_policy`, `paper_mode`, and `random_seed`. Sources: https://www.mlflow.org/docs/latest/ml/tracking, https://scikit-learn.org/stable/common_pitfalls.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Required manifest fields:

```text
run_id
created_at_utc
git_revision
python_version
package_lock_id
data_fixture_id
symbols
start_time_utc
end_time_utc
horizons
max_feature_lookback
max_label_horizon
split_policy
fee_policy
slippage_policy
paper_mode
random_seed
```

Recommendation: `paper_mode` must be `DRY_RUN` for Phase 1, and validation must fail closed if a live endpoint or live credential field appears. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://docs.alpaca.markets/docs/trading/paper-trading/, https://ecfr.io/Title-17/Section-240.15c3-5.

## Test Case Record

Recommendation: each test case should record `case_id`, `family`, `fixture`, `preconditions`, `expected_property`, `tolerance`, `observed_value`, `status`, and `source_urls`. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://hypothesis.readthedocs.io/.

Allowed `family` values:

```text
unit
property
numerical
data
backtest
integration
benchmark
```

Recommendation: test cases for numerical behavior must store both absolute and relative tolerances rather than relying on implicit defaults. Sources: https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://doi.org/10.1017/CBO9780511791253.

## Data Validation Interface

Recommendation: adapter outputs should expose records with strict types and point-in-time fields before feature builders consume them. Sources: https://docs.pydantic.dev/latest/concepts/strict_mode/, https://pandera.readthedocs.io/en/stable/dataframe_schemas.html, https://databento.com/docs/standards-and-conventions.

Minimum market record fields:

```text
symbol
event_time_utc_ns
available_at_utc_ns
source
sequence_id
bid_price_ticks
ask_price_ticks
bid_size
ask_size
trade_price_ticks
trade_size
trade_side
halt_status
corporate_action_version
```

Minimum news or exogenous event fields:

```text
event_id
source
source_published_at
first_seen_at
available_at
removed_at
symbol_tags
event_type
sentiment_raw
sentiment_normalized
novelty
relevance
```

Recommendation: data validation must reject records where `available_at` is after the prediction timestamp for feature computation. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://scikit-learn.org/stable/common_pitfalls.html.

## Metric Result Interface

Recommendation: metric results should be long-form records keyed by run, split, symbol, horizon, metric name, gross or net basis, value, denominator, sample count, and source URLs. Sources: https://scikit-learn.org/stable/modules/model_evaluation.html, https://www.mlflow.org/docs/latest/ml/tracking.

Required metric names:

```text
accuracy
precision
recall
calibration
brier_score
sharpe
max_drawdown
turnover
average_slippage
performance_after_fees
```

Recommendation: classification metrics must include threshold metadata and probability calibration metadata, because different thresholds can change precision and recall while probability quality is captured by calibration and Brier score. Sources: https://sklearn.org/stable/modules/generated/sklearn.metrics.precision_score.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.recall_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html, https://sklearn.org/1.7/modules/generated/sklearn.metrics.brier_score_loss.html.

Recommendation: backtest metrics must distinguish gross returns, slippage, commissions, regulatory fees, and net performance after fees. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.sec.gov/rules-regulations/fee-rate-advisories/section-31-transaction-fees-basic-information-firms, https://www.interactivebrokers.com/en/pricing/commissions-home.php?menu=A.

## Benchmark Result Interface

Recommendation: benchmark results should record `benchmark_id`, `component`, `input_shape`, `rows`, `events`, `features`, `wall_time_seconds`, `rows_per_second`, `events_per_second`, `peak_memory_mb`, `cpu_info`, and `status`. Sources: https://asv.readthedocs.io/, https://asv.readthedocs.io/en/v0.6.3/using.html, https://www.mlflow.org/docs/latest/ml/tracking.

Required benchmark components:

```text
data_schema_validation
feature_building
turbulence_estimation
price_interface_estimation
baseline_model_fit
prediction_scoring
backtest_ledger
metric_report
paper_dry_run
```

Recommendation: benchmark failures should block claims about scalability but should not hide validation failures, because correctness gates have priority over speed. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://asv.readthedocs.io/, https://scikit-learn.org/stable/common_pitfalls.html.

## Report Interface

Recommendation: each validation report should have sections for scope, data fixtures, validation cases, metric tables, benchmark tables, failures, warnings, and open questions. Sources: https://www.mlflow.org/docs/latest/ml/tracking, https://docs.pytest.org/en/stable/getting-started.html.

Recommendation: reports must not state or imply profitability unless out-of-sample, transaction-cost-adjusted, leakage-clean evidence exists and the claim is explicitly labeled as simulated research. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551.

## Open Questions

Should validation manifests be stored as JSON, YAML, Parquet metadata, or MLflow artifacts?

Should metric records support confidence intervals in Phase 1 or wait until sample sizes are known?

Should benchmark results include energy or battery state on Apple Silicon, or only CPU and wall time?

Should `source_urls` be required on every result record or only on report-level recommendations?
