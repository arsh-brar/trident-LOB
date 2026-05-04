# Prediction Models And Baselines Decision

## Decision

Phase 1 will use a CPU-only, offline prediction stack. The accepted first models are logistic regression for classification, ridge regression for returns, and lasso only for feature-stability diagnostics.

Recommendation: Start with logistic regression, ridge, and lasso diagnostics before any nonlinear or deep model. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

The accepted second-stage models are random forests and scikit-learn histogram gradient boosting. They may be used only after leakage checks, feature contracts, and linear baselines pass.

Recommendation: Use random forests and histogram gradient boosting as bounded nonlinear baselines, not as replacements for linear reporting. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html.

XGBoost is approved only as an optional later dependency. LightGBM is deferred until there is a specific boosted-tree validation need.

Recommendation: Prefer XGBoost over LightGBM for the first optional external boosted-tree test on the local Mac M3 because XGBoost documents prebuilt macOS Apple Silicon wheels and LightGBM macOS installation can involve OpenMP setup. Sources: https://xgboost.readthedocs.io/en/release_3.0.0/install.html, https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html.

Deep learning is not approved for default Phase 1 baselines. Temporal CNNs, LSTMs, transformers, and state-space models are deferred until L2 or L3 sequence tensors and validated simple baselines exist.

Recommendation: Defer temporal CNNs, LSTMs, transformers, and state-space models because the Phase 1 data target is bars, top-of-book quotes, trades, and optional news, while these models need larger sequence datasets and more careful overfitting controls. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855, https://arxiv.org/abs/1803.01271, https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory, https://arxiv.org/abs/1706.03762, https://arxiv.org/abs/2111.00396, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Physics-informed neural networks are rejected for Phase 1 because full TRIDENT PDE terms are not yet identified from event accounting.

Recommendation: Revisit physics-informed neural networks only after L2 or L3 source-sink reconstruction and finite-volume validation gates exist. Sources: https://doi.org/10.1016/j.jcp.2018.10.045, https://data.lobsterdata.com/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats/mbp-10.

## Required Cost Treatment

Every proposed model must be evaluated against transaction costs and slippage before it is considered useful.

Recommendation: Report raw forecast metrics, then net-cost decision metrics that subtract spread crossing, explicit fees when available, market impact, and slippage. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692, https://arxiv.org/abs/1011.6402.

Recommendation: Include a no-trade threshold for every classifier and regressor, because a statistically correct forecast can still be too small to trade after costs. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Do not claim profitability from model scores or simulated returns unless out-of-sample, transaction-cost-adjusted, slippage-stressed evidence exists. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Required Baselines

The required Phase 1 model comparison order is:

1. No-skill baselines: majority class, zero return, previous return sign, no-trade.
2. Literature feature baselines: spread, depth, OFI, signed volume, realized volatility, time-of-day.
3. TRIDENT feature increment: `k`, `epsilon`, fragility, market Reynolds number, optional `N_t`.
4. Linear models: logistic regression, ridge, lasso diagnostic.
5. Nonlinear scikit-learn models: random forest, histogram gradient boosting.
6. Optional boosted tree: XGBoost.
7. Deferred models: LightGBM, temporal CNN, LSTM, transformer, state-space model, physics-informed neural network.

Recommendation: Use this ordering so that complex models must prove incremental value over simple baselines and established microstructure controls. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Model Promotion Gates

Recommendation: Promote a model only if it improves out-of-sample forecast metrics, calibration, and net-cost decision metrics over all simpler eligible models. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Require symbol-level, horizon-level, and regime-level reporting before accepting a model as a general baseline. Sources: https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402.

Recommendation: Store model outputs as predictions and diagnostics only, with no broker endpoint, live order routing, or live-trading enable flag. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://ecfr.io/Title-17/Section-240.15c3-5.

## Non-Decision

This decision does not approve production prediction code, paid data purchase, paper-trading integration, live trading, broker routing, or profitability claims.

Recommendation: Keep Phase 1 prediction work in offline research workflows until validation gates approve broader integration. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://ecfr.io/Title-17/Section-240.15c3-5, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Open Questions

- What exact cost assumptions should be used for Phase 1 marketable fills, passive fills, partial fills, and rejected fills?
- What minimum net-cost improvement over logistic and ridge justifies adding XGBoost?
- Should LightGBM be excluded permanently if XGBoost and scikit-learn boosted trees are sufficient?
- Does the missing feature and label decision from `research/08` require revising the target list?
- Should no-trade be modeled as a third class or as a thresholding policy over binary probabilities and regression forecasts?
