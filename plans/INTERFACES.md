# TRIDENT-LOB Interfaces

Status: Phase 0 interface plan. This is not production code.

## Shared Principles

All records must carry event time and availability time. Features must be computed only from data with `available_at <= t_pred`. All components must be swappable through protocols or narrow contracts. Sources: [repository rules](../AGENTS.md), [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), [architecture decision](../research/12-python-architecture-and-stack/DECISION.md).

## Core Records

```text
BarRecord:
  symbol
  venue
  interval
  open
  high
  low
  close
  volume
  vwap
  event_start_ns
  event_end_ns
  available_at_ns
  source
```

```text
QuoteRecord:
  symbol
  venue
  bid_price
  ask_price
  bid_size
  ask_size
  event_ts_ns
  available_at_ns
  source
```

```text
TradeRecord:
  symbol
  venue
  price
  size
  side
  event_ts_ns
  available_at_ns
  source
```

```text
NewsEvent:
  event_id
  symbols
  event_type
  source
  source_published_at_ns
  provider_created_at_ns
  first_seen_at_ns
  available_at_ns
  sentiment
  relevance
  novelty_group
```

Sources: [data interface](../research/06-data-requirements-and-vendors/INTERFACE.md), [news interface](../research/07-news-and-exogenous-inputs/INTERFACE.md), https://databento.com/docs/standards-and-conventions.

## Component Contracts

```text
DataAdapter.load(request) -> DataBatch
EventStore.write(batch, manifest) -> DatasetId
EventStore.scan(query) -> Iterable[Record]
FeatureBuilder.build(records, clock) -> FeatureFrame
LabelBuilder.build(records, horizons, costs) -> LabelFrame
SplitBuilder.build(labels, lookback, horizon) -> SplitManifest
TurbulenceEstimator.transform(features) -> TurbulenceFrame
PriceInterfaceEstimator.transform(features) -> InterfaceFrame
Predictor.fit(train_frame, validation_frame) -> ModelArtifact
Predictor.predict(feature_frame) -> PredictionFrame
Backtester.run(predictions, market_events, risk_config) -> BacktestReport
RiskManager.evaluate(intent, state) -> RiskDecision
ReportGenerator.render(run_manifest) -> ReportArtifact
```

Sources: [architecture interface](../research/12-python-architecture-and-stack/INTERFACE.md), [feature interface](../research/08-feature-engineering-and-labels/INTERFACE.md), [backtesting interface](../research/10-backtesting-paper-trading-and-execution/INTERFACE.md).

## Required Quality Flags

- `data_mode`: bars, L1, L2, L3, synthetic.
- `is_structural`: false for bars-only TRIDENT proxies.
- `availability_passed`: true only when all inputs are point-in-time.
- `license_class`: free, delayed, real-time, paid, research-only, paper-trading-suitable, live-trading-suitable.
- `secret_free`: true only when no secret values are present.
- `paid_payload_free`: true only when paid raw data is not committed.

Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), [reproducibility decision](../research/14-reproducibility-and-experiment-tracking/DECISION.md).

## Extension Points

- Data adapters can add providers without changing feature contracts.
- Estimators can swap `epsilon` definitions while preserving output schema.
- Predictors can add optional XGBoost or later sequence models after gates.
- Backtest fill models can swap conservative bars-only, L1 quote, L2 depth, or L3 queue modes.
- Paper adapters must stay behind risk manager and paper-only guards.

Sources: [orchestration plan](ORCHESTRATION.md), [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md), [risk decision](../research/11-risk-controls-and-compliance/DECISION.md).

