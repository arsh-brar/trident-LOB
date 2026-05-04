# Prediction Models And Baselines Research

## Scope

This Phase 0 note covers prediction models and baselines for TRIDENT-LOB. It does not approve production code, broker connectivity, live trading, or profitability claims.

Recommendation: Phase 1 should treat prediction as an offline, CPU-only research task that tests whether TRIDENT-derived features improve out-of-sample forecasts over simple microstructure baselines. Sources: https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://scikit-learn.org/stable/install.html.

Recommendation: Every model result should be reported before costs and after estimated spread, fee, market-impact, and slippage costs, because high short-horizon accuracy can still be economically unusable after execution friction. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692, https://arxiv.org/abs/1011.6402.

## Prediction Tasks

Phase 1 should support these offline targets:

- next 1-minute and 5-minute direction.
- next 1-minute and 5-minute return in ticks or basis points.
- probability of spread widening.
- probability of local jump.
- probability that a signal remains profitable after estimated transaction costs and slippage.

Recommendation: Use leakage-safe time splits with a purge or gap between training and evaluation windows, because standard shuffled cross-validation can train on future observations in time series. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Feature Context

The expected Phase 1 feature families are spread, top-of-book depth, OFI or signed trade imbalance, queue imbalance when available, realized volatility proxy for `k`, decay or recovery proxy for `epsilon`, fragility `k^2 / epsilon`, market Reynolds number, and optional point-in-time news forcing.

Recommendation: TRIDENT variables should enter as incremental features over spread, depth, OFI, signed volume, realized volatility, and time-of-day controls, not as a replacement for established baselines. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670, https://www.nber.org/papers/w8160.

Recommendation: News and calendar features should be used only when their `available_at` timestamp is at or before prediction time. Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items.

## Model Landscape

### Logistic Regression

Logistic regression is the default Phase 1 classifier for direction, spread widening, and jump labels. It is fast, transparent, regularized by default in scikit-learn, and produces probabilities that can be thresholded against estimated costs.

Recommendation: Use logistic regression as the first directional baseline and require cost-aware thresholding before any signal is considered useful. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Transaction-cost evaluation: accept only thresholds where expected signed edge exceeds spread crossing, fees, market impact, and slippage under conservative fill assumptions. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

### Ridge And Lasso

Ridge should be the default linear regression baseline for return prediction. Lasso should be a diagnostic feature-selection model, not the primary model, because sparse selection can be unstable under correlated microstructure features.

Recommendation: Use ridge for next-horizon return regression and lasso only as a sensitivity check on feature stability. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Transaction-cost evaluation: translate predicted returns into net expected edge after costs before comparing models. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

### Random Forests

Random forests are useful as nonlinear diagnostics because they handle interactions and are available in scikit-learn, but they can be slower and less stable than linear baselines on high-frequency rolling windows.

Recommendation: Use random forests as a bounded nonlinear diagnostic after linear baselines pass validation, with shallow depth or minimum leaf constraints. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Transaction-cost evaluation: compare net edge by decile of predicted probability or predicted return, since tree ensembles can look strong on classification metrics while failing after spread and slippage. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://arxiv.org/abs/1011.6402.

### Gradient Boosting

Histogram gradient boosting in scikit-learn is the preferred first boosted-tree option because it fits the Phase 1 scikit-learn stack and avoids adding optional dependencies before they are justified.

Recommendation: Use scikit-learn histogram gradient boosting as the first strong tabular baseline after logistic and ridge, with early stopping and time-split validation. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html.

Transaction-cost evaluation: require boosted-tree gains to survive net-cost thresholding, turnover caps, and slippage stress. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### LightGBM

LightGBM is a strong tabular model candidate, but it should be secondary in Phase 1 because macOS installation can involve OpenMP and local build friction.

Recommendation: Defer LightGBM until scikit-learn boosted trees or XGBoost show that boosted trees are worth the added dependency surface. Sources: https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html, https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html.

Transaction-cost evaluation: LightGBM should be judged on net-cost performance and calibration, not only AUC, accuracy, or raw return prediction. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### XGBoost

XGBoost is the preferred optional external boosted-tree package because its documentation lists prebuilt Python wheels for macOS including Apple Silicon.

Recommendation: Add XGBoost as an optional `ml` dependency only after scikit-learn baselines have established a need for stronger boosted trees. Sources: https://xgboost.readthedocs.io/en/release_3.0.0/install.html, https://scikit-learn.org/stable/install.html.

Transaction-cost evaluation: XGBoost must beat logistic, ridge, and histogram gradient boosting after estimated costs, slippage stress, and turnover penalties. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### Temporal CNNs

Temporal CNNs are plausible for L2 or L3 sequence tensors and have strong evidence as sequence baselines. DeepLOB combines convolutional filters with LSTMs for LOB prediction, and generic temporal convolutional networks have compared favorably with recurrent networks on sequence tasks.

Recommendation: Defer temporal CNNs until there is enough event or multi-level LOB history to justify sequence tensors, and benchmark them against tabular boosted trees first. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855, https://arxiv.org/abs/1803.01271.

Transaction-cost evaluation: temporal CNN outputs must be converted to execution decisions only in simulation, with net-cost curves by horizon and predicted confidence. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

### LSTMs

LSTMs are designed for long sequence memory, and DeepLOB uses LSTM modules after convolutional LOB feature extraction. They are heavier than Phase 1 needs when features are already aggregated to minute or top-of-book windows.

Recommendation: Do not use LSTMs as Phase 1 baselines unless temporal CNNs and boosted trees leave a clear residual sequence problem. Sources: https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855, https://arxiv.org/abs/1803.01271.

Transaction-cost evaluation: LSTM improvements must survive walk-forward net returns after spread, impact, and slippage, not just sequence classification metrics. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

### Transformers

Transformers are powerful sequence models, but attention has high data and compute demands relative to the current CPU-only Phase 1 target. They are more defensible for later multi-symbol, long-window LOB tensors or news-plus-market fusion.

Recommendation: Defer transformers until large point-in-time datasets, baselines, and compute budgets justify them. Sources: https://arxiv.org/abs/1706.03762, https://scikit-learn.org/stable/install.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Transaction-cost evaluation: transformer outputs should be evaluated under the same net-cost, slippage, turnover, and drawdown constraints as all simpler models. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

### State-Space Models

Modern structured state-space models such as S4 and Mamba are attractive for long sequences because they target efficient sequence modeling. They remain research extensions for TRIDENT unless a later phase has long event streams and a clear need beyond temporal CNNs.

Recommendation: Treat neural state-space models as Phase 2 or later research models, not Phase 1 baselines. Sources: https://arxiv.org/abs/2111.00396, https://arxiv.org/abs/2312.00752, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Transaction-cost evaluation: state-space model claims must include net-cost performance and ablations against tabular features, temporal CNNs, and LSTMs. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692.

### Physics-Informed Neural Networks

Physics-informed neural networks can impose differential-equation residuals, but TRIDENT Phase 1 does not yet validate the full PDE or identify source and sink terms from L2 or L3 event data.

Recommendation: Do not use physics-informed neural networks in Phase 1. Revisit them only after source-sink accounting, nonnegativity, and finite-volume diagnostics are validated on L2 or L3 data. Sources: https://doi.org/10.1016/j.jcp.2018.10.045, https://data.lobsterdata.com/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats/mbp-10.

Transaction-cost evaluation: even if a physics-informed neural network fits a PDE residual, it must still beat simpler models after estimated transaction costs and slippage before any trading interpretation is discussed. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Deep Learning Justification

Deep learning may be justified later if the project has high-quality L2 or L3 event tensors, enough out-of-sample history, stable labels, and a demonstrated residual sequence signal that linear and boosted tabular models cannot capture.

Recommendation: Phase 1 should not use deep learning by default because the available target stack is CPU-only, the data plan starts with bars and top-of-book quotes, and the project requires simple baselines before complex models. Sources: https://scikit-learn.org/stable/install.html, https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Open Questions

- Does the missing `research/08-feature-engineering-and-labels/DECISION.md` change the final label definitions for direction, return, spread widening, or jump probability?
- Which transaction-cost model should become the Phase 1 default for marketable orders, passive orders, and no-trade thresholds?
- How much net-cost improvement over logistic and ridge is required before boosted trees become required rather than optional?
- Does fragility add incremental signal after spread, depth, OFI, realized volatility, and time-of-day controls?
- Is there enough L2 or L3 history in the next phase to make sequence models statistically credible?
