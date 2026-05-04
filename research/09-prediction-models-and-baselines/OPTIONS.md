# Prediction Model Options

## Evaluation Rule

Recommendation: Compare models first as forecasts and then as simulated decisions after transaction costs, slippage, market impact, and turnover constraints. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://www.tandfonline.com/doi/abs/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Report no-trade as an explicit alternative, because many short-horizon predictions will not clear spread and slippage. Sources: https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions, https://arxiv.org/abs/1011.6402.

## Options Table

| Model | Phase 1 role | Strength | Cost and slippage test | Recommendation |
| --- | --- | --- | --- | --- |
| Logistic regression | Default classifier | Transparent, fast, calibrated enough for first thresholds | Require predicted class edge to exceed spread, fees, impact, and slippage | Use first for direction, spread widening, and jump labels. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions |
| Ridge | Default return regression | Stable under correlated features | Require predicted return to exceed cost buffer | Use first for return targets. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions |
| Lasso | Feature stability diagnostic | Sparse coefficients | Require selected features to improve net-cost results out of sample | Use only as a sensitivity tool. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 |
| Random forest | Nonlinear diagnostic | Captures interactions without external dependencies | Compare net-cost probability deciles and turnover | Use after linear baselines. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions |
| Scikit-learn histogram gradient boosting | First strong tabular model | Fast boosted trees in existing stack | Require net improvement over logistic, ridge, and random forest | Use as first boosted-tree baseline. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html, https://scikit-learn.org/stable/install.html |
| LightGBM | Secondary boosted-tree candidate | Strong tabular performance | Require net-cost improvement large enough to justify dependency friction | Defer until boosted trees are proven useful. Sources: https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html, https://www.risk.net/journal-of-risk/technical-paper/2161150/optimal-execution-portfolio-transactions |
| XGBoost | Optional external boosted-tree candidate | Mature package with macOS Apple Silicon wheels | Require net-cost gain after slippage stress and turnover caps | Add only as optional `ml` dependency. Sources: https://xgboost.readthedocs.io/en/release_3.0.0/install.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 |
| Temporal CNN | Later sequence model | Good sequence baseline, useful for LOB tensors | Require simulated net edge by horizon and confidence bucket | Defer until L2 or L3 sequence tensors exist. Sources: https://arxiv.org/abs/1803.01271, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855 |
| LSTM | Later recurrent model | Can model longer dependencies | Require improvement over temporal CNNs after costs | Defer unless sequence residuals justify it. Sources: https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855 |
| Transformer | Later large sequence or fusion model | Attention can fuse long context and cross-feature interactions | Require net-cost gain, turnover control, and stability across symbols | Defer beyond Phase 1. Sources: https://arxiv.org/abs/1706.03762, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 |
| State-space model | Later long-sequence model | S4 and Mamba target efficient long-sequence modeling | Require ablations against tabular, temporal CNN, and LSTM models after costs | Defer beyond Phase 1. Sources: https://arxiv.org/abs/2111.00396, https://arxiv.org/abs/2312.00752 |
| Physics-informed neural network | Later PDE-constrained model | Can include differential-equation residuals | Require both PDE residual validation and net-cost improvement | Reject for Phase 1. Sources: https://doi.org/10.1016/j.jcp.2018.10.045, https://data.lobsterdata.com/info/DataStructure.php |

## Option A: Linear Baseline Stack

This stack uses logistic regression for classification, ridge for returns, and lasso for feature-stability diagnostics.

Recommendation: Choose this as the first Phase 1 model stack because it is CPU-only, interpretable, fast to validate, and aligned with simple-baseline policy. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html, https://scikit-learn.org/stable/install.html.

## Option B: Scikit-Learn Tree Stack

This stack adds random forests and histogram gradient boosting after the linear baselines.

Recommendation: Use this stack only after linear models and feature leakage checks pass, because boosted and ensemble trees increase model search space and overfitting risk. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html, https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Option C: External Boosted Trees

This stack adds XGBoost and possibly LightGBM as optional dependencies.

Recommendation: Prefer XGBoost before LightGBM for local Phase 1 optional testing because XGBoost documents macOS Apple Silicon wheels, while LightGBM macOS installation can depend on Homebrew, CMake, and OpenMP details. Sources: https://xgboost.readthedocs.io/en/release_3.0.0/install.html, https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html.

## Option D: Deep Sequence Models

This stack includes temporal CNNs, LSTMs, transformers, and modern state-space models.

Recommendation: Defer this stack until L2 or L3 event tensors exist and simpler models leave a validated residual sequence problem. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3519855, https://arxiv.org/abs/1803.01271, https://arxiv.org/abs/1706.03762, https://arxiv.org/abs/2111.00396.

## Option E: Physics-Informed Neural Models

This stack adds PDE residual losses or differentiable TRIDENT state dynamics.

Recommendation: Reject this stack for Phase 1 because full PDE source-sink identification requires L2 or L3 event accounting before a physics-informed residual is meaningful. Sources: https://doi.org/10.1016/j.jcp.2018.10.045, https://data.lobsterdata.com/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats/mbp-10.

## Open Questions

- Should the first cost model assume market orders only, passive orders only, or both with separate fill assumptions?
- What minimum out-of-sample period is required before adding optional boosted-tree dependencies?
- Should labels be ternary with a no-trade middle class, or binary plus a separate cost-aware decision threshold?
- Should feature importance reports use coefficients, permutation importance, SHAP-style summaries, or only ablation tables?
