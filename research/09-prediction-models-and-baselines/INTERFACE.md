# Prediction Model Interface

## Purpose

This interface describes the Phase 1 research contract for prediction models and baselines. It is a planning interface only and does not define production code.

Recommendation: Keep the prediction interface swappable so logistic regression, ridge, random forests, boosted trees, and later sequence models can share the same fit, predict, evaluate, and report contract. Sources: https://scikit-learn.org/stable/developers/develop.html, https://scikit-learn.org/stable/install.html.

## Inputs

The prediction model receives point-in-time feature rows.

```text
feature_frame
  symbol
  venue
  timestamp_ns
  horizon
  feature_set_version
  feature columns available at or before timestamp_ns
```

Recommendation: Require `timestamp_ns`, `horizon`, and `feature_set_version` on every feature row so split logic, leakage checks, and reproducibility can be audited. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://parquet.apache.org/docs/overview/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Labels arrive through a separate point-in-time label frame.

```text
label_frame
  symbol
  venue
  timestamp_ns
  label_timestamp_ns
  horizon
  label_name
  label_value
  cost_model_version
```

Recommendation: Store labels separately from features so feature construction cannot accidentally consume future returns, future spread states, or future fills. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Model Contract

The conceptual model protocol is:

```text
PredictionModel
  fit(train_features, train_labels, validation_features, validation_labels, config) -> FittedPredictionModel
  predict(features) -> prediction_frame
  explain(features) -> diagnostics_frame
  save_metadata() -> model_metadata
```

Recommendation: Match the broad scikit-learn estimator pattern for Phase 1 models because logistic regression, ridge, lasso, random forests, and histogram gradient boosting already follow it. Sources: https://scikit-learn.org/stable/developers/develop.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html.

## Prediction Output

Prediction output must be model-neutral.

```text
prediction_frame
  symbol
  venue
  timestamp_ns
  horizon
  model_id
  model_family
  prediction_type
  y_pred
  y_score
  probability_down
  probability_flat
  probability_up
  expected_return_ticks
  expected_return_bps
  cost_model_version
  expected_cost_ticks
  expected_slippage_ticks
  expected_net_edge_ticks
  no_trade_threshold_ticks
```

Recommendation: Include gross prediction, estimated cost, estimated slippage, expected net edge, and no-trade threshold in the prediction output for every model family. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692, https://arxiv.org/abs/1011.6402.

Recommendation: Keep prediction output separate from order intent, because Phase 0 and Phase 1 prediction work must not create live-trading code paths. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://ecfr.io/Title-17/Section-240.15c3-5.

## Cost Model Interface

The cost model is a research evaluator, not an execution engine.

```text
CostModel
  estimate_cost(decision_context, side, size, horizon) -> cost_estimate
```

Cost estimates include:

```text
cost_estimate
  spread_cost_ticks
  explicit_fee_ticks
  market_impact_ticks
  slippage_ticks
  total_cost_ticks
  stress_scenario
```

Recommendation: Pass every proposed model through the same cost model so model comparisons are not distorted by inconsistent friction assumptions. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

Recommendation: Use at least base, adverse, and severe slippage scenarios in reports. Sources: https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions.

## Model Families

The interface must support these model families:

- `majority_class`
- `zero_return`
- `previous_sign`
- `logistic_regression`
- `ridge`
- `lasso`
- `random_forest`
- `hist_gradient_boosting`
- `xgboost_optional`
- `lightgbm_deferred`
- `temporal_cnn_deferred`
- `lstm_deferred`
- `transformer_deferred`
- `state_space_deferred`
- `physics_informed_nn_rejected_phase1`

Recommendation: Include deferred and rejected model families in metadata only, not implementation, so Phase 1 reports can compare decisions without creating deep-learning or physics-informed code. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855, https://arxiv.org/abs/1706.03762, https://doi.org/10.1016/j.jcp.2018.10.045.

## Training Configuration

Training configuration should include:

```text
model_config
  model_family
  model_params
  feature_set_version
  label_version
  split_policy
  train_start_ns
  train_end_ns
  validation_start_ns
  validation_end_ns
  test_start_ns
  test_end_ns
  gap_ns
  cost_model_version
  random_seed
```

Recommendation: Record split windows, gap, feature version, label version, cost version, and random seed for each run. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://mlflow.org/docs/latest/ml/tracking/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Diagnostics

Diagnostics should include:

```text
diagnostics
  coefficients_or_importance
  calibration_metrics
  gross_metrics
  net_cost_metrics
  turnover
  coverage
  regime_breakdowns
  leakage_check_status
  validation_failures
```

Recommendation: Always report gross metrics beside net-cost metrics so users can see whether a model fails because it cannot forecast or because forecast edge is too small after costs. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Report diagnostics by symbol, horizon, time-of-day bucket, volatility regime, and fragility regime. Sources: https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402.

## Open Questions

- Should cost model versions live in the label frame, prediction frame, or both?
- Should `probability_flat` be required for all classifiers, or only for ternary labels?
- Should model metadata include package versions before any production package exists?
- Should sequence-model metadata be reserved now, or added only when L2 or L3 tensors exist?
