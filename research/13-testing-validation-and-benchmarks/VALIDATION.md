# Validation

Date checked: 2026-05-04.

## Gate Policy

Recommendation: validation must fail closed when a hard gate fails, including future-data use, negative liquidity, uncapped execution, impossible timestamps, live-trading endpoint exposure, live credential exposure, NaN metrics, or missing transaction-cost accounting. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://scikit-learn.org/stable/common_pitfalls.html, https://ecfr.io/Title-17/Section-240.15c3-5.

Recommendation: validation must separate hard failures, soft warnings, and open questions so research uncertainty is visible without weakening safety gates. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://www.mlflow.org/docs/latest/ml/tracking, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Unit Tests

Recommendation: unit tests must cover tick conversion, spread in ticks and basis points, midprice return, signed imbalance, OFI proxy, top-book depth, realized variance `k`, volatility-decay `epsilon`, `nu_t`, fragility, market Reynolds number, prediction metrics, ledger cash updates, position updates, fees, slippage, and drawdown. Sources: https://docs.pytest.org/en/stable/getting-started.html, https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://arxiv.org/abs/1011.6402, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md.

Acceptance: deterministic examples pass exactly for integer accounting and within declared tolerances for floating-point quantities.

## Property Tests

Recommendation: property tests must generate valid and adversarial event sequences to check nonnegative quantities, capped sinks, cash-position conservation, monotone time, no future availability, symmetric side relabeling, and bounded probability outputs. Sources: https://hypothesis.readthedocs.io/, https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Acceptance: no generated case produces negative accepted liquidity, negative accepted `k`, nonpositive accepted `epsilon`, future-data eligibility, unbalanced ledger state, or probability outside `[0, 1]`.

## Numerical Tests

Recommendation: numerical tests must include accounting residuals, nonnegative limiter behavior, no-drift symmetry, known-model limits, finite-volume conservation diagnostics, and convergence trend checks on synthetic tick grids. Sources: https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose, https://doi.org/10.1017/CBO9780511791253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/04-numerical-discretization/DECISION.md.

Acceptance: each numerical test declares `rtol`, `atol`, grid size, timestep, and expected residual before execution.

## Data Tests

Recommendation: data tests must reject malformed schemas, mixed timezones, non-UTC timestamps, event timestamps after availability when impossible, duplicate primary keys, crossed quotes, negative prices, negative sizes, stale NBBO, missing halt status, and news rows unavailable at prediction time. Sources: https://docs.pydantic.dev/latest/concepts/strict_mode/, https://pandera.readthedocs.io/en/stable/dataframe_schemas.html, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Acceptance: invalid fixtures fail before feature building, and valid fixtures preserve source timestamps and provider identifiers in the validated output.

## Backtest Tests

Recommendation: backtest tests must verify chronological train, validation, and test windows; gap or embargo logic; train-only preprocessing; label horizon exclusion; explicit costs; slippage; turnover; position limits; max drawdown; and leakage sentinel rejection. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://scikit-learn.org/stable/common_pitfalls.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/10-backtesting-paper-trading-and-execution/README.md.

Acceptance: a deliberately leaked future-return feature is rejected, and a clean baseline run reports gross performance, fees, average slippage, turnover, max drawdown, Sharpe, and performance after fees.

## Integration Tests

Recommendation: integration tests must run offline from fixture data through validation, feature building, baseline fitting, scoring, backtesting, reporting, benchmark logging, and paper dry-run intent logging. Sources: https://www.mlflow.org/docs/latest/ml/tracking, https://docs.alpaca.markets/docs/trading/paper-trading/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Acceptance: integration tests produce a validation report and no live endpoint, live credential, or live order submission path is present.

## Required Validation Cases

Recommendation: accounting case. Build a synthetic two-sided book with known adds, cancellations, executions, and boundary flux. Verify that integrated `q_s` changes match event accounting. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://data.lobsterdata.com/info/DataStructure.php, https://doi.org/10.1017/CBO9780511791253.

Acceptance: accounting residual is zero for integer event replay and within declared tolerance for finite-volume diagnostics.

Recommendation: nonnegative liquidity case. Generate execution requests larger than visible depth and verify accepted execution is capped by available depth. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1016/j.jcp.2021.110253.

Acceptance: `q_plus`, `q_minus`, `lambda_s`, `mu_s`, `e_s`, `k`, `epsilon`, and `nu_t` remain in their allowed domains after the accepted update.

Recommendation: symmetric no-drift case. Mirror bid and ask liquidity, arrivals, cancellations, market orders, and forcing. Verify expected deterministic drift is zero. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1412.0141.

Acceptance: deterministic price movement is zero within declared tolerance and changes sign correctly under side relabeling.

Recommendation: known-model limiting cases. Test source-sink behavior when `k = 0`, square-root impact under a linear latent book, and OFI over depth when only best bid and ask are retained. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1412.0141, https://doi.org/10.1103/PhysRevX.1.021006, https://arxiv.org/abs/1011.6402.

Acceptance: limiting-case outputs match the simplified formulas within declared tolerances and do not claim structural identification from bars-only data.

Recommendation: backtest leakage case. Inject a future-return feature, a future news availability timestamp, and a scaler fit on all data. Verify all three are rejected. Sources: https://scikit-learn.org/stable/common_pitfalls.html, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Acceptance: validation fails before model fitting and reports the specific leakage rule that was violated.

Recommendation: paper-trading dry-run case. Generate hypothetical order intents, pass them through risk checks, simulate fills, update a paper ledger, and prove no live broker endpoint is reachable. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://ecfr.io/Title-17/Section-240.15c3-5, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Acceptance: all outputs are marked `DRY_RUN`, no live credentials are loaded, no order is routed, and the report states that paper results are simulated.

## Metrics

Recommendation: accuracy must be computed as correct predictions divided by total predictions for thresholded direction, spread-widening, and jump tasks. Sources: https://scikit-learn.org/stable/modules/model_evaluation.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.precision_score.html.

Recommendation: precision must be reported as true positives over predicted positives, and recall must be reported as true positives over actual positives. Sources: https://sklearn.org/stable/modules/generated/sklearn.metrics.precision_score.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.recall_score.html.

Recommendation: calibration must compare predicted probabilities with observed frequencies by probability bins, and Brier score must measure mean squared probability error. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html, https://sklearn.org/1.7/modules/generated/sklearn.metrics.brier_score_loss.html.

Recommendation: Sharpe must use excess return divided by return volatility and must be interpreted cautiously under non-normal returns and multiple testing. Sources: https://www.jstor.org/stable/2351741, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551.

Recommendation: max drawdown must be computed from the peak-to-trough decline of the equity curve, turnover from traded notional or shares relative to portfolio size, average slippage from execution price versus decision or benchmark price, and performance after fees from net returns after commissions, regulatory fees, and slippage. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.sec.gov/rules-regulations/fee-rate-advisories/section-31-transaction-fees-basic-information-firms, https://www.interactivebrokers.com/en/pricing/commissions-home.php?menu=A.

## Open Questions

What hard thresholds should be used for calibration error and Brier score by horizon?

Should max drawdown be measured intraday, daily, or both for Phase 1 reports?

How should turnover be normalized for strategies that frequently exit to cash?

What is the right slippage benchmark for top-of-book data when quote queue position is unknown?

How should validation distinguish weak predictive signal from ordinary sampling uncertainty?
