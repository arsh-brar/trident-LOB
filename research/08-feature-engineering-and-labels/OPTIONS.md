# Options

## Feature Set Options

Option A is a minimal bars-only feature set. It includes lagged returns, rolling volatility, rolling volume, VWAP distance, high-low range, and time-of-day controls. This option is useful for architecture tests but should not be used to claim TRIDENT source-sink or latent-liquidity validation because bars do not contain quote queues or event-level book changes. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://lobsterdata.com/info/DataStructure.php

Option B is the Phase 1 default top-of-book feature set. It adds spread, bid size, ask size, top depth, queue imbalance, OFI, quote update rate, signed trade imbalance when trades exist, and TRIDENT proxies for `k`, `epsilon`, fragility, `nu_t`, `R_m`, and L1 price-interface liquidity. This option best matches the Phase 1 target while remaining CPU-only. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Option C is an enriched event-level feature set using L2 or L3 messages. It adds depth ladders, price-level depletion, replenishment, cancellation, execution rates, queue-reactive state, and quote-shear production. This option should be deferred to Phase 2 or a paid-data pilot because full source and sink accounting needs L2 or L3 data. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md, https://lobsterdata.com/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats/mbp-10

Option D is a news-enriched Phase 1 feature set. It adds `N_signed`, `N_energy`, `N_count`, `N_novel_count`, market forcing, and scheduled-event risk to Option B. This option should be enabled only when timestamped point-in-time news availability is recorded. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.sec.gov/edgar/sec-api-documentation

Recommendation: choose Option B as the required Phase 1 default and Option D as an optional extension. Keep Option A as a degraded mode and defer Option C. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Label Options

Option 1 is raw future return regression at fixed horizons. It is easy to evaluate but can overstate practical value because small returns inside spread and fees may be statistically visible yet economically unusable. Sources: https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Option 2 is three-class direction with a neutral cost band. It directly encodes whether the future move clears estimated transaction costs and a noise buffer. Sources: https://doi.org/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Option 3 is stress-event labeling for spread widening, local jump, depth depletion, and fragility persistence. It tests TRIDENT's liquidity-stress claims more directly than ordinary direction prediction. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://arxiv.org/abs/1011.6402

Option 4 is barrier-style labeling with upper and lower return barriers plus a time horizon. It can align labels with economic thresholds, but it is more complex and needs careful purging because labels can overlap heavily. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Recommendation: use Option 1 for regression baselines, Option 2 as the primary direction label, and Option 3 as the primary TRIDENT stress-label family. Treat Option 4 as a later validation experiment, not the first default. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Horizon Options

The 1 minute horizon is the shortest default Phase 1 horizon. It is close enough to top-of-book OFI and spread dynamics to be meaningful with L1 quotes. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402

The 5 minute horizon is the second default Phase 1 horizon. It is named by the model specification and may give turbulence and news features more time to show persistence. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doi.org/10.1080/713665670

The 15 and 30 minute horizons are exploratory. They may be useful for news and scheduled-event response, but they can dilute top-of-book microstructure signal. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://www.bls.gov/schedule/news_release/, https://arxiv.org/abs/1011.6402

Recommendation: require 1 minute and 5 minute labels in Phase 1, include 15 minute and 30 minute labels only when data coverage and embargo rules remain adequate. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

## Class Imbalance Options

Option A is neutral-band tuning. Wider neutral bands reduce false actionable labels and may increase the neutral class. Narrower bands increase directional labels but can label noise as signal. Sources: https://doi.org/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Option B is class-weighted fitting. It preserves row order and uses inverse-frequency weights or model-specific class weights. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

Option C is validation-only threshold tuning. It chooses probability thresholds using validation precision-recall curves and never touches test outcomes. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html

Option D is resampling. It can be useful for non-temporal classification, but it should not be the Phase 1 default because duplicated or synthetic time-series rows can distort temporal dependence and leakage audits. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Recommendation: use Options A, B, and C in that order. Do not use resampling as a default Phase 1 method. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Split Options

Option A is a single chronological holdout split. It is simple and audit-friendly, but it gives only one estimate of out-of-sample performance. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Option B is walk-forward validation with expanding train windows, fixed validation windows, and embargo gaps. It gives more robust estimates while preserving time order. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Option C is random row splitting. It is rejected for Phase 1 because neighboring time-series rows share overlapping features and future labels, which makes random rows vulnerable to leakage and optimistic estimates. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Option D is held-out-symbol validation. It should supplement, not replace, chronological splits because it tests cross-symbol portability. Sources: https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402

Recommendation: use Option A for the first audit, Option B for model selection, and Option D for portability checks. Reject random row splitting. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Open Questions

Should Phase 1 make news-enriched features optional by config or separate dataset version?

Should stress-event labels be horizon-specific or use one standardized threshold family across horizons?

Should the primary direction label use midprice exits, quote exits, or cost-adjusted executable price approximations?

What minimum test period is enough for rare local-jump labels?

