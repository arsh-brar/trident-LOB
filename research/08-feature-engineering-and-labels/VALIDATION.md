# Validation

## Validation Goal

The Phase 1 feature and label system is valid only if it is point-in-time, CPU-only, reproducible, baseline-comparable, and free of trading side effects. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md

## Leakage Gates

Gate 1: for every feature row, `feature_available_at_max_ns <= t_pred_ns`. Any violation fails the dataset. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Gate 2: completed bar features must use only bars whose close time and provider availability time are not later than `t_pred_ns`. Partial bar features require explicit partial observations. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Gate 3: quote and trade features must use only events with event time and availability time not later than `t_pred_ns`; out-of-order events must be sorted by availability before feature aggregation. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://arxiv.org/abs/1011.6402

Gate 4: news, SEC filings, macro releases, and scheduled events must pass the news eligibility rule before aggregation. Actual release values must not enter pre-release anticipation features. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://www.sec.gov/edgar/sec-api-documentation, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule

Gate 5: validation and test splits must include an embargo of at least `max_label_horizon + max_feature_lookback`. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Feature Validity Gates

Gate 6: all TRIDENT positivity constraints must hold for accepted rows: `k >= 0`, `epsilon > 0`, `nu_t >= 0`, `D_top >= 0`, and `fragility >= 0`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

Gate 7: bars-only data must not output quote-only features as if they were observed. Quote-dependent columns must be null or marked degraded. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://lobsterdata.com/info/DataStructure.php

Gate 8: OFI must be computed from top-of-book event logic, not future return direction. Sources: https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

Gate 9: time-of-day normalized percentiles must be fit on training data only, then applied to validation and test. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Gate 10: news novelty must use only prior eligible events in the same cluster, never future duplicates. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://docs.benzinga.com/api-reference/news-api/get-news-items

## Label Validity Gates

Gate 11: every non-null label must use future outcome data strictly after `t_pred_ns` and within the declared horizon policy. Missing, halted, stale, or session-invalid future outcomes must produce null labels with reason codes. Sources: https://www.nyse.com/markets/hours-calendars, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md

Gate 12: cost-aware direction labels must store `cost_ticks` and `buffer_ticks` used to define the neutral band. Sources: https://doi.org/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Gate 13: class distributions must be reported by symbol, horizon, date bucket, and split. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html

Gate 14: stress labels must report base rates and minimum positive counts before model fitting. Sources: https://sklearn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Split And Model-Comparison Gates

Gate 15: random row splits are prohibited for Phase 1 validation. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Gate 16: every model comparison must include at least one technical baseline and one ordinary microstructure baseline before evaluating TRIDENT-derived feature lift. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670

Gate 17: feature ablations must report baseline-only, baseline plus news, baseline plus TRIDENT, and baseline plus TRIDENT plus news when the relevant data exists. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://massive.com/docs/rest/stocks/news?auth=signup, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Gate 18: no validation report may claim profitability unless an explicit later task adds transaction-cost-adjusted out-of-sample backtesting and risk gates. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk

## Required Reports

The validation report must include row counts, null counts, feature availability checks, label base rates, split date ranges, embargo length, class weights, metrics by horizon, metrics by symbol, and ablation lift over baselines. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html

The leakage report must list the maximum source availability timestamp per feature family and must fail closed when a feature family lacks availability metadata. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://www.sec.gov/edgar/sec-api-documentation, https://massive.com/docs/rest/stocks/news?auth=signup

The imbalance report must include per-class precision, recall, macro F1, balanced accuracy, average precision for binary stress labels, confusion matrices, and selected thresholds with validation-only provenance. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html

## Acceptance Criteria

Accept the Phase 1 feature and label dataset only when all leakage, feature validity, label validity, split, and reporting gates pass. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Accept TRIDENT-derived features as useful only if they improve validation and test metrics over ordinary microstructure and technical baselines, with no leakage violations and no degradation concentrated in rare stress regimes. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Reject any report that converts signals into live orders, broker instructions, or live-trading enablement. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5

## Open Questions

What base-rate threshold should block model fitting for rare stress labels?

Should embargo length include maximum news decay half-life, or only the explicit feature lookback window?

Should validation require both within-symbol and held-out-symbol success before TRIDENT features become default?

How should feature drift be measured across market regimes without overfitting regime definitions?

