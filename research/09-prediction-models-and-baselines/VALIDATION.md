# Prediction Model Validation

## Validation Position

Prediction validation is a Phase 1 research gate. It validates forecasts, costs, slippage, and leakage controls. It does not authorize live trading.

Recommendation: Treat validation as a fail-closed process where leakage, missing timestamps, impossible labels, or net-cost failure blocks model promotion. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://ecfr.io/Title-17/Section-240.15c3-5.

## Required Checks

### Leakage Checks

Recommendation: Verify every feature timestamp is less than or equal to the prediction timestamp and every label timestamp is strictly after the prediction timestamp. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Use time-ordered train, validation, and test splits with a gap when labels overlap feature windows. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### Baseline Checks

Recommendation: Compare every trained model against majority class, zero return, previous sign, no-trade, spread and depth controls, OFI, signed volume, realized volatility, and time-of-day controls. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670, https://www.nber.org/papers/w8160.

Recommendation: Report TRIDENT feature contribution as an ablation over literature controls, not as a standalone score. Sources: https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### Cost And Slippage Checks

Recommendation: For every proposed model, compute net expected value after spread, fees, estimated impact, and slippage. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

Recommendation: Stress the cost model with at least base, adverse, and severe slippage assumptions before reporting any model as useful. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk.

Recommendation: Include a no-trade threshold and report coverage, turnover, hit rate, average gross edge, average cost, and average net edge. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### Model-Specific Checks

Recommendation: Logistic regression must report calibration, coefficient signs, regularization strength, and net-cost threshold curves. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions.

Recommendation: Ridge must report residual distribution, rank correlation, directional conversion performance, and net-cost threshold curves. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions.

Recommendation: Lasso must report selected-feature stability across time splits before any feature-selection claim is accepted. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Random forests must report depth, leaf size, feature importance stability, probability calibration, and net-cost decile curves. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions.

Recommendation: Histogram gradient boosting must report early-stopping behavior, validation loss, calibration, and net-cost decile curves. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html.

Recommendation: XGBoost and LightGBM must pass the same checks as histogram gradient boosting and must justify the added dependency with net-cost improvement. Sources: https://xgboost.readthedocs.io/en/release_3.0.0/install.html, https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Temporal CNNs, LSTMs, transformers, state-space models, and physics-informed neural networks must not be promoted unless they beat simple and boosted tabular baselines after costs and slippage. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855, https://arxiv.org/abs/1803.01271, https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory, https://arxiv.org/abs/1706.03762, https://arxiv.org/abs/2111.00396, https://doi.org/10.1016/j.jcp.2018.10.045.

## Required Metrics

Forecast metrics:

- classification: accuracy, balanced accuracy, log loss, Brier score, ROC AUC when class balance permits.
- regression: MAE, RMSE, rank correlation, sign accuracy, residual by regime.
- calibration: probability calibration curve and expected calibration error.

Recommendation: Forecast metrics should be reported by symbol, horizon, time-of-day bucket, volatility regime, and fragility regime. Sources: https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402.

Decision metrics:

- gross edge per decision.
- estimated spread cost.
- estimated fee cost when available.
- estimated market impact.
- slippage stress.
- net edge per decision.
- coverage and turnover.
- drawdown of simulated research ledger.

Recommendation: Decision metrics should be secondary to forecast validation in Phase 1 and must not be described as live trading performance. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Promotion Criteria

Recommendation: A model can be promoted from diagnostic to accepted baseline only if it improves net-cost out-of-sample performance over simpler baselines, has stable results across at least two time splits, and has no leakage violations. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: A complex model can be promoted only if its incremental net-cost benefit exceeds its maintenance cost and dependency risk. Sources: https://xgboost.readthedocs.io/en/release_3.0.0/install.html, https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: No model can be promoted to paper-trading integration from this decision alone. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://ecfr.io/Title-17/Section-240.15c3-5.

## Failure Conditions

Recommendation: Fail validation if a model uses future data, lacks a no-trade threshold, improves only in sample, fails after costs, depends on unavailable data, or requires GPU acceleration in Phase 1. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://scikit-learn.org/stable/install.html.

Recommendation: Fail validation if any report claims profitability without out-of-sample, transaction-cost-adjusted, slippage-stressed evidence. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk.

## Open Questions

- What cost and slippage presets should represent base, adverse, and severe conditions?
- Should model reports include exact broker fees, or use fee-free assumptions plus spread, impact, and slippage until a broker is selected?
- How many walk-forward splits are enough for a Phase 1 baseline decision?
- Should calibration be mandatory for regression-derived direction signals, or only for probability classifiers?
- What evidence threshold is enough to move XGBoost from optional to required?
