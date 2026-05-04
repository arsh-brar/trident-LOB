# Decision

Date checked: 2026-05-04.

## Decision

Build a Phase 0 validation plan for a CPU-only Phase 1 research predictor. The plan uses `pytest`, Hypothesis, deterministic synthetic fixtures, strict data validation, chronological backtest splits, transaction-cost-aware metrics, and dry-run paper simulation. It does not approve production code, live trading, broker routing, live credentials, or profitability claims. Recommendation: make validation gates a required part of the research workflow before any model or paper-trading result is accepted. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://docs.pytest.org/en/stable/getting-started.html.

## Accepted Test Families

Recommendation: require unit tests for deterministic calculations, including tick conversion, spread, midprice return, OFI proxy, top-book depth, realized volatility proxy for `k`, decay proxy for `epsilon`, fragility, market Reynolds number, cost model, slippage model, ledger updates, and metrics. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://arxiv.org/abs/1011.6402, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md.

Recommendation: require property tests for nonnegative quantities, capped execution, timestamp ordering, no future-data eligibility, symmetric no-drift, and cash-position conservation over generated event sequences. Sources: https://hypothesis.readthedocs.io/, https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Recommendation: require numerical tests for accounting residuals, positivity, deterministic symmetry, known-model limiting cases, and convergence diagnostics on synthetic tick grids. Sources: https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://doi.org/10.1017/CBO9780511791253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/04-numerical-discretization/DECISION.md.

Recommendation: require data tests for schema, types, UTC nanosecond timestamps, duplicate keys, negative sizes, crossed quotes, missing NBBO, stale quotes, corporate action metadata, and point-in-time news availability. Sources: https://docs.pydantic.dev/latest/concepts/strict_mode/, https://pandera.readthedocs.io/en/stable/dataframe_schemas.html, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Recommendation: require backtest tests for chronological splits, train-only preprocessing, feature-window eligibility, label horizon separation, fees, slippage, turnover, drawdown, and leakage sentinels. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://scikit-learn.org/stable/common_pitfalls.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: require integration tests for offline fixture ingestion, feature building, baseline fit, prediction scoring, backtest ledger, validation report, benchmark report, and dry-run order-intent logging. Sources: https://www.mlflow.org/docs/latest/ml/tracking, https://docs.alpaca.markets/docs/trading/paper-trading/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Accepted Validation Cases

Recommendation: accounting validation must compare integrated liquidity changes with event-level adds, cancellations, executions, and boundary flux. The case fails if residuals exceed the declared tolerance or if unmatched execution is hidden. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://data.lobsterdata.com/info/DataStructure.php, https://doi.org/10.1017/CBO9780511791253.

Recommendation: nonnegative liquidity validation must generate stress executions and reject any state with negative `q_s`, negative source, negative cancellation rate, negative execution, negative `k`, nonpositive `epsilon`, or negative `nu_t`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1016/j.jcp.2021.110253.

Recommendation: symmetric no-drift validation must mirror both sides of the book and require expected deterministic price drift to be zero within tolerance. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1412.0141.

Recommendation: known-model limiting validation must test the `k = 0` source-sink limit, the linear latent book square-root impact limit, and the best-bid-best-ask OFI over depth limit. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1412.0141, https://doi.org/10.1103/PhysRevX.1.021006, https://arxiv.org/abs/1011.6402.

Recommendation: backtest leakage validation must fail if any feature uses a timestamp later than `t_pred`, if train transforms fit on validation or test data, or if label horizon overlap leaks into the training window. Sources: https://scikit-learn.org/stable/common_pitfalls.html, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: paper-trading dry-run validation must prove that Phase 1 can emit hypothetical order intents, rejects, and fills into a simulated ledger without live endpoints, live credentials, or live order submission. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://ecfr.io/Title-17/Section-240.15c3-5, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Metrics Decision

Recommendation: classification reports must include accuracy, precision, recall, calibration, and Brier score for each symbol, horizon, and split when sample counts are sufficient. Sources: https://scikit-learn.org/stable/modules/model_evaluation.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.precision_score.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.recall_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html, https://sklearn.org/1.7/modules/generated/sklearn.metrics.brier_score_loss.html.

Recommendation: backtest reports must include Sharpe, max drawdown, turnover, average slippage, gross performance, fees, and performance after fees. Sources: https://www.jstor.org/stable/2351741, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.sec.gov/rules-regulations/fee-rate-advisories/section-31-transaction-fees-basic-information-firms, https://www.interactivebrokers.com/en/pricing/commissions-home.php?menu=A.

Recommendation: no profitability statement may be emitted unless the run is out-of-sample, transaction-cost-adjusted, leakage-clean, and compared against simple baselines. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551.

## Benchmarks Decision

Recommendation: Phase 1 benchmarks should measure feature-build throughput, event-fixture throughput, model-fit wall time, prediction throughput, metric computation time, peak memory when available, and report generation time on the local Mac M3 CPU environment. Sources: https://asv.readthedocs.io/, https://www.mlflow.org/docs/latest/ml/tracking, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Recommendation: benchmark reports must include data shape, symbols, date range, rows, feature count, event count, Python version, package lock identity, CPU mode, and git revision when available. Sources: https://asv.readthedocs.io/en/v0.6.3/using.html, https://www.mlflow.org/docs/latest/ml/tracking, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Non-Decision

This decision does not choose universal metric thresholds, approve model promotion, approve live trading, approve broker integration, approve paid data, or claim that TRIDENT variables are profitable.

## Open Questions

What minimum sample count is required before per-symbol calibration and Sharpe are reportable?

Should the first Phase 1 validation profile block merges on property tests or run them as nightly checks?

Which `epsilon` estimator should define the canonical nonnegative and limiting-case tests?

Should paper-trading dry-run validation simulate Alpaca semantics exactly or use a provider-neutral paper ledger first?

How should benchmark regressions be judged across thermal and battery states on the Mac M3?
