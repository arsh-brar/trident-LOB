# Research

Date checked: 2026-05-04.

## Scope

This work defines the Phase 0 testing, validation, and benchmark plan for TRIDENT-LOB. It does not approve production code, live trading, broker routing, paid data purchase, or profitability claims. Recommendation: treat Phase 1 as a CPU-only research predictor with invariant checks, leakage checks, benchmark baselines, and dry-run paper simulation only. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Testing Layers

Recommendation: use unit tests for deterministic functions such as tick conversion, spread, OFI, realized variance, `epsilon` floors, fragility, market Reynolds number, fees, slippage, position accounting, and metric formulas. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md.

Recommendation: use property tests for invariants over many generated inputs, especially nonnegative liquidity, capped execution sinks, monotone timestamps, no future-data joins, order-ledger cash and position balance, and symmetry under bid and ask relabeling. Sources: https://hypothesis.readthedocs.io/, https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Recommendation: use numerical tests for tolerances, conservation residuals, finite-volume diagnostic identities, known-model limits, and convergence trends on synthetic grids, with explicit absolute and relative tolerances for each test. Sources: https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://doi.org/10.1017/CBO9780511791253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/04-numerical-discretization/DECISION.md.

Recommendation: use data tests for schema, dtype, timezone, UTC nanosecond ordering, duplicate event keys, impossible quotes, negative sizes, stale quotes, corporate-action metadata, and point-in-time availability fields. Sources: https://docs.pydantic.dev/latest/concepts/strict_mode/, https://pandera.readthedocs.io/en/stable/dataframe_schemas.html, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Recommendation: use backtest tests for walk-forward splits, train-test separation, feature-window eligibility, label horizon exclusion, cost application, fill assumptions, turnover accounting, and leakage sentinels that deliberately fail when future columns are exposed. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://scikit-learn.org/stable/common_pitfalls.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/10-backtesting-paper-trading-and-execution/README.md.

Recommendation: use integration tests for the complete offline path from fixture data to features, model fit, prediction, backtest ledger, report metrics, MLflow artifact metadata, and paper dry-run order-intent logging. Sources: https://www.mlflow.org/docs/latest/ml/tracking, https://docs.alpaca.markets/docs/trading/paper-trading/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Required Validation Cases

Recommendation: include an accounting case that integrates liquidity changes and compares them with adds, cancellations, executions, and boundary flux. This is a hard gate because the model specification defines order-book accounting as a verification check. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://data.lobsterdata.com/info/DataStructure.php, https://doi.org/10.1017/CBO9780511791253.

Recommendation: include a nonnegative liquidity case where generated executions are larger than available depth and the accepted sink is capped without producing negative `q_s`, `k`, `epsilon`, or `nu_t`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1016/j.jcp.2021.110253.

Recommendation: include a symmetric no-drift case where bids and asks, arrivals, cancellations, market orders, and forcing are mirrored, then expected deterministic price drift is zero within tolerance. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1412.0141.

Recommendation: include known-model limiting cases for `k = 0`, linear latent book square-root impact, and top-of-book OFI over depth. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1412.0141, https://doi.org/10.1103/PhysRevX.1.021006, https://arxiv.org/abs/1011.6402.

Recommendation: include a backtest leakage case where an intentionally shifted future-return feature is injected and the validation layer rejects it before model fitting. Sources: https://scikit-learn.org/stable/common_pitfalls.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Recommendation: include a paper-trading dry-run case where hypothetical order intents pass through risk checks and ledger simulation but no live endpoint, credential, or order router can be reached. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://ecfr.io/Title-17/Section-240.15c3-5, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Metrics

Recommendation: report classification accuracy, precision, recall, calibration curve error, and Brier score for direction, spread-widening, and jump-probability tasks. Sources: https://scikit-learn.org/stable/modules/model_evaluation.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.precision_score.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.recall_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html, https://sklearn.org/1.7/modules/generated/sklearn.metrics.brier_score_loss.html.

Recommendation: report strategy metrics only after transaction costs, including Sharpe, max drawdown, turnover, average slippage, and performance after fees. Sources: https://www.jstor.org/stable/2351741, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.sec.gov/rules-regulations/fee-rate-advisories/section-31-transaction-fees-basic-information-firms, https://www.interactivebrokers.com/en/pricing/commissions-home.php?menu=A.

Recommendation: report benchmark metrics for wall time, peak memory when available, rows per second, events per second, feature windows per second, and benchmark hardware metadata. Sources: https://asv.readthedocs.io/, https://www.mlflow.org/docs/latest/ml/tracking, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Open Questions

Which acceptance thresholds should become hard Phase 1 gates rather than warning thresholds?

How much out-of-sample improvement over OFI, depth, spread, and realized-volatility baselines is enough to justify keeping TRIDENT turbulence features?

Should calibration be judged globally, per symbol, per horizon, or per time-of-day bucket?

What minimum history length is required before Sharpe and drawdown metrics are stable enough to report?

Can Phase 1 top-of-book fixtures stress accounting enough, or does source-sink accounting need a small L2 or L3 paid pilot?
