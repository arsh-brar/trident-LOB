# TRIDENT-LOB Validation Gates

Status: Phase 0 validation plan. These gates do not approve live trading.

## 1. Data Leakage Tests

Required gates:

- Every feature row must satisfy `feature_available_at_max_ns <= t_pred_ns`.
- Every news event must satisfy `available_at_ns <= t_pred_ns`.
- Completed bars are eligible only after close time and provider availability time.
- Train transforms must fit on train data only.
- Label horizons must not overlap training windows after embargo.

Sources: [feature validation](../research/08-feature-engineering-and-labels/VALIDATION.md), [news validation](../research/07-news-and-exogenous-inputs/VALIDATION.md), https://scikit-learn.org/stable/common_pitfalls.html.

## 2. Walk-Forward Backtesting Rules

Use chronological 60 percent train, 20 percent validation, and 20 percent test for the first fixed split. Use walk-forward validation when at least three embargoed folds are available. The embargo must be at least `max_label_horizon + max_feature_lookback`. Random row splitting is rejected. Sources: [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## 3. Minimum Out-Of-Sample Predictive-Skill Thresholds

A Phase 1 model can be called an accepted research baseline only if it beats all simpler eligible baselines out of sample. Minimum thresholds:

- Classification: macro F1 improves by at least 0.02 absolute over the best simple baseline, and Brier score improves by at least 1 percent relative for probability outputs.
- Direction labels: per-class precision and recall must be reported for up, down, and no-trade classes.
- Regression: mean absolute error or root mean squared error must improve over zero-return and last-return baselines.
- Calibration: reliability curves must be reported for any probability used by the backtester.

These thresholds are research gates, not profitability claims. Sources: [prediction validation](../research/09-prediction-models-and-baselines/VALIDATION.md), [testing decision](../research/13-testing-validation-and-benchmarks/DECISION.md), https://scikit-learn.org/stable/modules/model_evaluation.html.

## 4. Minimum Transaction-Cost-Adjusted Performance Thresholds

Before a strategy can progress from diagnostic backtest to candidate paper simulation:

- Net performance after spread, slippage, and configured fees must beat no-trade and best simple baseline on the held-out test.
- Turnover, average slippage, reject counts, partial-fill counts, and gross versus net performance must be reported.
- Stress tests must include at least 2 times baseline slippage and a wider spread scenario.
- No result may be described as profitable unless it is out-of-sample, transaction-cost-adjusted, slippage-stressed, and reproducible.

Sources: [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## 5. Max Drawdown Thresholds

For Phase 1 research backtests, candidate strategies fail promotion if held-out max drawdown exceeds 5 percent of simulated research equity or exceeds 2 times the median drawdown of the best simple baseline, whichever is stricter. Phase 3 paper trading must use the risk agent defaults unless the user explicitly tightens them. Sources: [risk decision](../research/11-risk-controls-and-compliance/DECISION.md), [testing decision](../research/13-testing-validation-and-benchmarks/DECISION.md).

## 6. Paper-Trading Duration Requirement

Paper trading cannot begin in Phase 1. For a later Phase 3 paper task, require at least 30 trading days or 1,000 paper decisions, whichever is longer, before any live-readiness review can be discussed. The paper run must include reconciliation, rejects, slippage, latency, stale-data events, halts, risk rejects, and manual review. Sources: [paper plan](PHASE_3_PAPER_TRADING.md), [risk blockers](../research/11-risk-controls-and-compliance/LIVE_TRADING_BLOCKERS.md), https://docs.alpaca.markets/docs/trading/paper-trading/.

## 7. Conditions That Block Live Trading

Live trading is blocked if any condition below is true:

- Phase 0 or Phase 1 is active.
- Any live endpoint, live credential path, live order router, or live-trading flag exists.
- Leakage tests fail.
- Simple baselines are missing.
- Transaction-cost-adjusted and slippage-stressed results are missing.
- Drawdown, exposure, or order-rate gates fail.
- Paper-trading duration and reconciliation gates are incomplete.
- Broker, margin, short-sale, and compliance review is incomplete.
- User has not explicitly requested a future live-readiness review after all gates pass.

Sources: [risk blockers](../research/11-risk-controls-and-compliance/LIVE_TRADING_BLOCKERS.md), [risk decision](../research/11-risk-controls-and-compliance/DECISION.md), https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://ecfr.io/Title-17/Section-240.15c3-5.

