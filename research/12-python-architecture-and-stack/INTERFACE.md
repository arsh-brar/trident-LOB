# Architecture Interfaces

## Interface Principles

Use Python protocols for major component boundaries so implementations are swappable without forcing inheritance. This matches the repository preference for modular swappable architecture and mypy's static checking model [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Use Pydantic models for external boundary records and manifests, while allowing internal numerical paths to use NumPy arrays, Polars frames, Arrow tables, and DuckDB relations where appropriate. This combines strict input validation with efficient local analytical execution [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/), [NumPy install](https://numpy.org/install/), [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/), [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview).

Use UTC nanosecond or microsecond timestamps and explicit split boundaries in all data contracts. This is required to prevent future-data leakage and to align event streams, order book fields, news forcing, and validation windows [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [Apache Parquet overview](https://parquet.apache.org/docs/overview/).

## Proposed Boundary Types

Recommend these logical records as Pydantic-validated boundary objects: `RunConfig`, `DataSliceSpec`, `EventBatchManifest`, `FeatureMatrixManifest`, `LabelSpec`, `ModelSpec`, `BacktestSpec`, `ValidationReport`, and `ArtifactRef`. Strict validation should be enabled at external boundaries to reject accidental type coercion [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Recommend these in-memory interchange types: `pl.LazyFrame` for deferred feature queries, `pl.DataFrame` for materialized tabular batches, `numpy.ndarray` for numerical kernels, DuckDB relations for SQL planning, and Parquet paths for persisted artifacts [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/), [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview), [NumPy install](https://numpy.org/install/), [Apache Parquet overview](https://parquet.apache.org/docs/overview/).

## Component Interfaces

Data adapters should expose offline reads only in Phase 1, returning validated event manifests and lazy tabular handles. This follows the no-live-trading rule and supports market data, news forcing, and scheduled event streams without broker actions [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [Polars Parquet](https://docs.pola.rs/user-guide/io/parquet/).

```text
DataAdapter
  describe_available_slices() -> list[DataSliceSpec]
  load_events(slice_spec) -> EventBatchManifest plus lazy frame handle
```

Event stores should persist immutable event batches as partitioned Parquet and expose DuckDB query handles. This keeps Phase 1 local, auditable, and queryable without a server [DuckDB data ingestion](https://duckdb.org/docs/stable/clients/python/data_ingestion), [Apache Parquet overview](https://parquet.apache.org/docs/overview/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

```text
EventStore
  register_batch(manifest) -> ArtifactRef
  query_events(slice_spec, columns, filters) -> lazy tabular handle
```

Feature builders should accept only past and present events relative to each label timestamp, emit feature manifests, and record lookback windows. This directly enforces the no-future-data rule [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/).

```text
FeatureBuilder
  build_features(slice_spec, feature_spec) -> FeatureMatrixManifest
  describe_feature_lineage(feature_manifest) -> lineage report
```

Turbulence estimators should estimate `k`, `epsilon`, and derived fragility measures from visible order book fields, quote-revision velocities, imbalance, depth changes, and exogenous forcing. Numerical implementations should use NumPy and SciPy first [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install).

```text
TurbulenceEstimator
  fit(calibration_slice, features) -> fitted estimator artifact
  transform(slice_spec, features) -> turbulence feature artifact
```

Price-interface estimators should estimate the latent balance interface where buy and sell pressure meet, and should report uncertainty or failure modes rather than forcing a price prediction [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [SciPy install](https://scipy.org/install), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

```text
PriceInterfaceEstimator
  fit(calibration_slice, features) -> fitted estimator artifact
  estimate_interface(slice_spec, features) -> interface artifact
```

Prediction models should implement fit, predict, and predict_proba or score only for offline research datasets. scikit-learn should be the first implementation target, and XGBoost should be optional after baseline gates [scikit-learn install](https://scikit-learn.org/stable/install.html), [XGBoost install](https://xgboost.readthedocs.io/en/release_3.0.0/install.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

```text
PredictionModel
  fit(train_features, train_labels, validation_data) -> fitted model artifact
  predict(features) -> predictions artifact
  explain(features) -> optional explanation artifact
```

Backtesters should consume frozen predictions, labels, costs, and risk constraints, never live market connections. They must report transaction-cost-adjusted and out-of-sample metrics before any research conclusion is made [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/).

```text
Backtester
  run(backtest_spec, prediction_artifact, cost_spec) -> validation report
```

Paper-trading adapters should remain interface stubs only in Phase 1 planning and must not place live trades. This preserves the project rule that live trading is blocked by explicit validation gates and later compliance checks [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

```text
PaperTradingAdapter
  validate_environment() -> readiness report
  submit_simulated_order(order_intent) -> simulated receipt
```

Risk managers should be pure offline evaluators during Phase 1, checking position, loss, concentration, and halt rules against simulated outputs only [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

```text
RiskManager
  evaluate(backtest_state, proposed_action) -> allow, block, or reduce
```

Report generators should render traceable research summaries from MLflow artifacts, validation reports, and Parquet manifests, with citations and without profitability claims unless validation evidence supports the statement [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/), [Apache Parquet overview](https://parquet.apache.org/docs/overview/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

```text
ReportGenerator
  render(validation_report, artifact_refs) -> report artifact
```

