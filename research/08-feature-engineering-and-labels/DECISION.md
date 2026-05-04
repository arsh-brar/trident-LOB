# Decision

Status: Phase 0 decision. This does not authorize production code, live trading code, broker routing, paid data purchase, or profitability claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270

## Chosen Phase 1 Feature Set

Phase 1 will use a CPU-only, point-in-time feature pipeline with four feature families: TRIDENT-derived features, ordinary microstructure features, technical baseline features, and news features. Recommendation: TRIDENT variables must be tested as incremental features over ordinary microstructure and technical baselines, not as standalone proof of a PDE model. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Ticks are the internal price coordinate and seconds are the internal time coordinate. Basis points and log returns are reporting and normalization views only. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

The required TRIDENT-derived Phase 1 features are `k`, `epsilon`, `nu_t`, fragility, imbalance production, withdrawal production, market Reynolds number, and L1 price-interface liquidity. Recommendation: compute these as observable proxies only, with no claim that Phase 1 identifies structural turbulence or full source-sink dynamics. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/03-latent-order-book-and-price-interface/DECISION.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

The required ordinary microstructure features are spread, midprice return, bid size, ask size, harmonic and minimum top depth, quote imbalance, OFI, signed trade imbalance when trades exist, trade count, quote update rate, spread change, and time-of-day controls. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1287/opre.1090.0780, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

The required technical baseline features are lagged returns, rolling realized volatility, rolling volume, rolling dollar volume, VWAP distance, high-low range, close-to-close momentum, reversal, and moving-average gap. Recommendation: these baselines must be present before crediting TRIDENT variables with predictive value. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

News features are optional in the first runnable Phase 1 dataset but required in the interface contract. When present, they must include symbol signed score, symbol energy, symbol count, novel count, market signed score, market energy, symbol scheduled risk, and market scheduled risk. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.sec.gov/edgar/sec-api-documentation, https://www.bls.gov/schedule/news_release/

## Chosen Labels

The required Phase 1 horizons are 1 minute and 5 minutes. The optional research horizons are 15 minutes and 30 minutes. Recommendation: use 1 and 5 minutes for default model selection, and use 15 and 30 minutes only when embargo and data-coverage checks pass. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

The required regression labels are future midprice log return, future tick return, and future basis-point return at each approved horizon. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://doi.org/10.1080/713665670

The required direction label is three-class and transaction-cost-aware:

```text
y_dir_h =  1 if future_mid_tick_return_h > cost_ticks_h + buffer_ticks_h
y_dir_h = -1 if future_mid_tick_return_h < -cost_ticks_h - buffer_ticks_h
y_dir_h =  0 otherwise
```

Recommendation: use the three-class label as the primary direction target because it avoids labeling inside-spread noise as tradable movement. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://doi.org/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

The required stress labels are spread widening, local jump, top-depth depletion, and fragility persistence. Recommendation: evaluate TRIDENT variables primarily on these labels because they are closest to the model's liquidity-fragility claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://arxiv.org/abs/1011.6402

## Leakage Decision

Every feature must be computed from observations with `available_at <= t_pred`. No feature may use future bars, future quotes, future trades, future corporate-action corrections, future news, future SEC filings, future macro actuals, or future provider revisions. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://www.sec.gov/edgar/sec-api-documentation, https://massive.com/docs/rest/stocks/news?auth=signup, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Bars must be shifted according to the decision clock. A completed bar is eligible only after its close time and provider availability time. An in-progress bar is eligible only if the dataset explicitly records partial information observed before `t_pred`. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

News and scheduled events must use the news ledger's point-in-time availability fields. Scheduled-event anticipation and released actuals must be separate features. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

## Class Imbalance Decision

Class imbalance will be handled by transaction-cost-aware neutral bands, class-weighted fitting, validation-only threshold tuning, and imbalanced metrics. Resampling is not a Phase 1 default. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

The required metrics for imbalanced labels are macro F1, per-class precision and recall, balanced accuracy, one-vs-rest average precision for stress labels, confusion matrices, and calibration summaries. Accuracy alone is insufficient. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

## Split Decision

The default train-validation-test split is chronological: earliest 60 percent train, next 20 percent validation, final 20 percent test, with an embargo gap before each validation or test region. The embargo must be at least `max_label_horizon + max_feature_lookback`. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Walk-forward validation is required for model selection when the dataset has enough history for at least three validation folds after embargo. Random row splitting is rejected. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Held-out-symbol evaluation should be added after within-symbol chronological validation passes. Recommendation: use it to test portability of TRIDENT-derived features, not as a replacement for time-based out-of-sample testing. Sources: https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402

## Non-Decisions

This decision does not select a production model, approve a full PDE solver, approve paper broker integration, approve live trading, approve paid data purchase, or claim profitability. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk

## Open Questions

Should `cost_ticks_h` use half-spread only, half-spread plus fee estimates, or a horizon-specific slippage model?

Should stress thresholds be fixed in ticks, symbol-normalized by spread, or percentile-based by time-of-day bucket?

Which `epsilon` proxy should become the default after validation: volatility decay, spread recovery, depth recovery, or a filtered latent decay state?

Should news features be included in the default model comparison or run as a separate ablation until availability timestamps are proven reliable?

What sample length is required before local-jump and depth-depletion labels are stable enough for model selection?

