# Options

Date checked: 2026-05-04.

## Test Runner

Option A is `pytest` as the default runner. Recommendation: choose `pytest` because it supports simple test discovery, direct assertions, fixtures, parametrization, approximate equality, and a mature Python testing workflow. Sources: https://docs.pytest.org/en/stable/getting-started.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Option B is Python `unittest`. Recommendation: keep `unittest` only as compatibility knowledge because it is in the standard library, while the project stack already selected `pytest`. Sources: https://docs.python.org/3/library/unittest.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Decision pressure: Phase 1 needs readable tests for many research invariants, so `pytest` is the better default. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.

## Property Testing

Option A is Hypothesis for generated inputs. Recommendation: choose Hypothesis for invariants that should hold across broad valid inputs, such as nonnegative liquidity, capped sinks, ledger conservation, timestamp monotonicity, and leakage guards. Sources: https://hypothesis.readthedocs.io/, https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Option B is hand-written parametrized edge cases. Recommendation: keep hand-written cases for named examples and regressions, but do not rely on them alone for accounting and leakage invariants. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html.

Decision pressure: use both, with hand-written cases for explainability and Hypothesis for input coverage. Sources: https://hypothesis.readthedocs.io/, https://docs.pytest.org/en/stable/getting-started.html.

## Numerical Validation

Option A is deterministic synthetic cases with known residuals. Recommendation: choose deterministic synthetic cases for conservation, symmetry, known-model limits, and convergence checks because expected behavior can be stated before implementation. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doi.org/10.1017/CBO9780511791253, https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.

Option B is empirical-only validation on market data. Recommendation: reject empirical-only validation because market data cannot isolate accounting defects, hidden future joins, or known limiting behavior. Sources: https://scikit-learn.org/stable/common_pitfalls.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/04-numerical-discretization/DECISION.md.

Decision pressure: start with deterministic synthetic validation, then add empirical diagnostics after invariants pass. Sources: https://doi.org/10.1017/CBO9780511791253, https://data.lobsterdata.com/info/DataStructure.php.

## Data Tests

Option A is strict schema validation at adapter boundaries. Recommendation: choose strict schema validation for input records, config, and event ledgers because silent coercion can mask vendor issues and future-data mistakes. Sources: https://docs.pydantic.dev/latest/concepts/strict_mode/, https://pandera.readthedocs.io/en/stable/dataframe_schemas.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

Option B is late validation inside feature builders. Recommendation: reject late-only validation because bad timestamps, negative sizes, or duplicate event identifiers should fail before they affect feature windows. Sources: https://scikit-learn.org/stable/common_pitfalls.html, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Decision pressure: validate early at adapter boundaries and again after feature materialization. Sources: https://docs.pydantic.dev/latest/concepts/strict_mode/, https://pandera.readthedocs.io/en/stable/dataframe_schemas.html.

## Backtest Validation

Option A is walk-forward time splits with a gap or embargo. Recommendation: choose walk-forward splits with a gap at least as large as the largest feature lookback and label horizon overlap risk. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/08-feature-engineering-and-labels/README.md.

Option B is random cross-validation. Recommendation: reject random cross-validation for time-series performance claims because it can train on future data and evaluate on earlier samples. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://scikit-learn.org/stable/common_pitfalls.html.

Decision pressure: use chronological train, validation, and test windows for all reported performance. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Benchmarks

Option A is lightweight `pytest` timing for local sanity checks. Recommendation: use quick local timing only for developer feedback, not for long-term performance claims. Sources: https://docs.pytest.org/en/stable/getting-started.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Option B is `asv` for benchmark history. Recommendation: choose `asv` when Phase 1 needs repeatable benchmark history for feature builders, joins, event replay fixtures, and metric computation. Sources: https://asv.readthedocs.io/, https://asv.readthedocs.io/en/v0.6.3/using.html.

Decision pressure: use simple local timing first and add `asv` after stable interfaces exist. Sources: https://asv.readthedocs.io/, https://www.mlflow.org/docs/latest/ml/tracking.

## Metric Reporting

Option A is model metrics plus transaction-cost-aware backtest metrics. Recommendation: choose both because predictor quality and simulated economic quality answer different questions. Sources: https://scikit-learn.org/stable/modules/model_evaluation.html, https://sklearn.org/1.7/modules/generated/sklearn.metrics.brier_score_loss.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551.

Option B is accuracy-only reporting. Recommendation: reject accuracy-only reporting because imbalance and probability quality matter for directional and jump tasks. Sources: https://sklearn.org/stable/modules/generated/sklearn.metrics.precision_score.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.recall_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html.

Decision pressure: report accuracy, precision, recall, calibration, Brier score, Sharpe, max drawdown, turnover, average slippage, and performance after fees. Sources: https://scikit-learn.org/stable/modules/model_evaluation.html, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.sec.gov/rules-regulations/fee-rate-advisories/section-31-transaction-fees-basic-information-firms.

## Open Questions

Should Phase 1 include `asv` immediately or wait until feature contracts settle?

Should property tests run in every local invocation or only in a slower validation profile?

Should data schemas use Pandera directly if Polars remains the primary dataframe engine, or should schemas live at the Pydantic record boundary first?

How should benchmark baselines be normalized across different Mac M3 thermal states?
