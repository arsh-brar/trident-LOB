# Research

## Scope

This document defines Phase 1 feature and label research for TRIDENT-LOB. Phase 1 is a CPU-only feature pipeline, not a production solver, not live trading code, and not a profitability claim. This follows the project model specification and risk decisions. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md

Phase 1 must use ticks as the internal price coordinate, seconds as the internal time coordinate, and log returns or basis points only as normalized feature and reporting views. This matches the prior coordinate decision and exchange tick-size practice. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

The feature set must be modular and separable into TRIDENT-derived features, ordinary microstructure features, technical baseline features, and news features. This keeps original TRIDENT claims testable against simple and literature-supported baselines before any complex model is introduced. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Data Grain

The preferred Phase 1 input grain is top-of-book quotes plus trades plus bars. Bars-only mode is allowed for architecture tests, but features that require quotes, queues, or trade signs must be marked unavailable or degraded rather than fabricated from future information. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://lobsterdata.com/info/DataStructure.php

Each feature row represents a prediction decision time `t_pred`. A feature is eligible only if every input event used to compute it has `available_at <= t_pred`. This applies to bars, quotes, trades, corporate actions, symbol metadata, news, SEC filings, and scheduled-event fields. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://www.sec.gov/edgar/sec-api-documentation, https://massive.com/docs/rest/stocks/news?auth=signup

## TRIDENT-Derived Features

Phase 1 should compute `k` as realized tick variance intensity over trailing windows:

```text
k_t(w) = sum_{u in (t-w, t]} Delta mid_ticks_u^2 / w_seconds
```

This is a point-in-time volatility-energy proxy, not a structural turbulence estimate. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418

Phase 1 should compute `epsilon` as a positive volatility decay or recovery-capacity proxy, with a default exponentially weighted decay estimate and alternatives based on spread recovery and depth replenishment when quote data is present:

```text
epsilon_t(w) = max(lambda_decay_t(w) * k_t(w), epsilon_floor)
```

This keeps the k-epsilon analogy numerically positive while admitting uncertainty about the best financial proxy. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1016/j.jedc.2015.09.012

Phase 1 should compute eddy diffusivity and fragility only as derived features:

```text
nu_t = C_mu * k_t^2 / (epsilon_t + epsilon_0)
fragility_t = k_t^2 / (epsilon_t + epsilon_0)
```

These features must be reported in raw, clipped, z-scored, and within-symbol time-of-day percentile forms so the research can separate level effects from intraday seasonality. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1080/713665670

Phase 1 should compute market Reynolds number using the prior dimensionless formula:

```text
R_m = (abs(I_t) / (D_top_t + D_star)) / (epsilon_t / (k_t + k_0) + gamma_u)
```

`I_t` should be signed aggressive trade imbalance when classified trades exist, top-of-book OFI when quotes exist, and signed volume proxy only in bars-only mode. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, https://arxiv.org/abs/1011.6402, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Phase 1 should include production decomposition features: imbalance production, withdrawal production, and optional news production. Quote-shear production should be deferred until L2 or L3 depth is available. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobsterdata.com/info/DataStructure.php

Phase 1 should include the price-interface proxy `L_L1_proxy = 2 * harmonic_mean(best_bid_size, best_ask_size) / max(spread_ticks, 1)` when top-of-book quotes are available. It must be labeled as an L1 liquidity proxy, not as identified latent liquidity. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/03-latent-order-book-and-price-interface/DECISION.md, https://arxiv.org/abs/1412.0141, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

## Ordinary Microstructure Features

Phase 1 should include spread in ticks and basis points, midprice, midprice return, quote imbalance, bid size, ask size, harmonic top depth, minimum top depth, quote update rate, trade count, signed trade imbalance, realized spread proxy, and OFI. These are required controls because short-horizon price changes are strongly related to OFI and depth. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1287/opre.1090.0780, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

The OFI feature should use only quote changes observed up to `t_pred`. If the best bid or ask price changes within a quote update, the contribution should follow the Cont, Kukanov, and Stoikov event accounting logic rather than a simple size difference. Sources: https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

Phase 1 should include time-of-day controls, market session flags, halt or LULD state when available, and symbol liquidity buckets. These controls reduce confounding from intraday seasonality and abnormal market states. Sources: https://doi.org/10.1080/713665670, https://www.nyse.com/markets/hours-calendars, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan

## Technical Baseline Features

Phase 1 should include simple technical baselines computed from trailing bars only: lagged returns, rolling realized volatility, rolling volume, VWAP distance, high-low range, close-to-close momentum, reversal, moving-average gap, and rolling dollar volume. These features create a basic non-LOB benchmark before TRIDENT variables are credited. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Technical features must be shifted so an aggregated bar ending after `t_pred` is never used at `t_pred`. If the prediction decision is made at the close of a completed minute, only the completed minute and older data are eligible. If the decision is inside a minute, only partial bar data explicitly observed before `t_pred` is eligible. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## News Features

Phase 1 should consume the provider-neutral `N_t` ledger from the news decision and output symbol-specific signed score, symbol-specific energy, count, novel count, market signed score, market energy, scheduled-event risk, and macro scheduled-event risk. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.alphavantage.co/documentation/

News features must use `available_at`, `source_published_at`, and removal or correction fields to avoid future news leakage. SEC filings and macro data must use the time the filing or release became available, not the period the filing describes. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://www.sec.gov/edgar/sec-api-documentation, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule

Scheduled-event features should split pre-event anticipation from post-event actual information. Calendar knowledge can contribute before the scheduled event only if `calendar_known_at <= t_pred`; actual values can contribute only if `actual_available_at <= t_pred`. Sources: https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm, https://massive.com/docs/rest/partners/benzinga/earnings

## Labels

Phase 1 should define labels at 1 minute, 5 minutes, 15 minutes, and 30 minutes. The 1 and 5 minute labels are primary because the model specification names them and because top-of-book OFI is most defensible at short horizons. The 15 and 30 minute labels are secondary stress and news-response horizons. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://arxiv.org/abs/1011.6402, https://massive.com/docs/rest/stocks/news?auth=signup

The core return labels should be future midprice log return, future tick return, and future basis-point return:

```text
y_ret_h = log(mid_{t+h}) - log(mid_t)
y_ticks_h = mid_ticks_{t+h} - mid_ticks_t
```

The label uses future data by definition, but no future data can enter the features. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

The core direction label should be three-class with a neutral band:

```text
y_dir_h =  1 if y_ticks_h > cost_ticks_h + buffer_ticks
y_dir_h = -1 if y_ticks_h < -cost_ticks_h - buffer_ticks
y_dir_h =  0 otherwise
```

The neutral band makes the class label transaction-cost-aware and avoids treating economically tiny moves as actionable direction. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://doi.org/10.1080/14697680903373692, https://arxiv.org/abs/1011.6402

Phase 1 should define event labels for spread widening, local jump, depth depletion, and high-fragility persistence:

```text
spread_widen_h = 1[max_spread_ticks(t, t+h] >= spread_ticks_t + spread_threshold]
local_jump_h = 1[max_abs_mid_tick_move(t, t+h] >= jump_threshold_ticks]
depth_deplete_h = 1[min_D_top(t, t+h] <= depth_depletion_fraction * D_top_t]
fragility_persist_h = 1[median_fragility(t, t+h] >= symbol_tod_quantile_90]
```

These labels test the TRIDENT claim that fragility and Reynolds-like pressure should predict liquidity stress beyond OFI and depth. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://arxiv.org/abs/1011.6402

Phase 1 should include transaction-cost-aware labels for later backtest research, but these labels must remain research outputs and must not create live order code. The label should subtract an estimated half-spread, fees when known, and slippage buffer from the future move. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://doi.org/10.1080/14697680903373692

## Class Imbalance

Class imbalance should be handled first by label design, then by class weights, then by threshold tuning on validation data only. Oversampling should not be the default for time series because duplicated or synthetic samples can distort temporal dependence. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

The primary imbalanced-class metrics should be per-class precision, recall, macro F1, balanced accuracy, average precision for one-vs-rest stress labels, and calibration curves. Accuracy alone is not sufficient when neutral or no-event classes dominate. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html, https://sklearn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

## Splits

Phase 1 should use chronological train, validation, and test splits with an embargo gap at least as long as the maximum label horizon plus the maximum feature lookback. This prevents overlapping feature and label windows from allowing future information to bleed into training. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

The default split should be anchored by time, not random rows: train on the earliest 60 percent of eligible rows, validate on the next 20 percent, and test on the final 20 percent, with symbol and date boundaries preserved where possible. Walk-forward validation should be added when enough history exists. Sources: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

Cross-symbol experiments should include both within-symbol splits and held-out-symbol tests. Within-symbol tests measure temporal generalization; held-out-symbol tests measure whether TRIDENT features have portable structure rather than symbol memorization. Sources: https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Open Questions

Which `epsilon` proxy gives the most stable out-of-sample labels and features: volatility decay, spread recovery, depth recovery, or a filtered latent state?

Should the neutral band be set by quoted spread, realized spread, estimated fees, empirical noise, or all of them?

Do 15 and 30 minute horizons help news-response research, or do they dilute microstructure signal too much?

How much history is needed before time-of-day percentiles for fragility are reliable by symbol?

Should stress labels be calibrated globally, per symbol, or per symbol liquidity bucket?

