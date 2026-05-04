# Phase 1 Predictor Plan

Status: Phase 0 plan. This does not authorize production trading, live broker endpoints, live credentials, or profitability claims.

## Goal

Build a CPU-only Mac M3 compatible offline research predictor that loads historical bars, L1 quotes, trades, calendars, corporate actions, and optional news, then tests TRIDENT-inspired features against simple baselines using leakage-safe walk-forward validation and transaction-cost-aware backtests. Sources: [model spec](../docs/TRIDENT_LOB_MODEL.md), [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md).

## Inputs

- Bars: open, high, low, close, volume, VWAP, `event_ts`, `available_at`.
- L1 quotes: bid, ask, bid size, ask size, quote timestamp, availability timestamp.
- Trades when available: price, size, side classification if available, timestamp, availability timestamp.
- Corporate actions and calendars.
- Optional news and scheduled events with `available_at`.

Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), [news decision](../research/07-news-and-exogenous-inputs/DECISION.md), https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

## Feature Families

Required ordinary features: spread, midprice return, bid size, ask size, harmonic depth, minimum depth, quote imbalance, OFI, signed trade imbalance, trade count, quote update rate, spread change, and time-of-day controls. Sources: [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), https://arxiv.org/abs/1011.6402.

Required TRIDENT proxies: `k`, `epsilon`, `nu_t`, fragility, imbalance production, withdrawal production, market Reynolds number, and L1 price-interface liquidity proxy. Sources: [turbulence decision](../research/02-turbulence-closure-and-fragility/DECISION.md), [price-interface decision](../research/03-latent-order-book-and-price-interface/DECISION.md).

Required technical baselines: lagged returns, rolling realized volatility, rolling volume, rolling dollar volume, VWAP distance, high-low range, momentum, reversal, and moving-average gap. Sources: [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), https://doi.org/10.1080/713665670.

## Labels

Required horizons are 1 minute and 5 minutes. Labels include future midprice log return, future tick return, future basis-point return, cost-aware three-class direction, spread widening, local jump, top-depth depletion, and fragility persistence. Sources: [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), [validation decision](../research/13-testing-validation-and-benchmarks/DECISION.md).

## Model Order

1. Majority class, zero return, previous return sign, no-trade.
2. Literature features with simple rules.
3. Logistic regression and ridge regression.
4. Lasso diagnostics for feature stability.
5. Random forest and histogram gradient boosting after linear baselines pass.
6. Optional XGBoost only after the above passes.

Sources: [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md), https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html, https://xgboost.readthedocs.io/en/release_3.0.0/install.html.

## Validation

Use chronological train, validation, and test splits with embargo at least `max_label_horizon + max_feature_lookback`. Walk-forward validation is required when enough history exists for at least three validation folds. Random row splitting is rejected. Sources: [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Every report must show raw forecast metrics and net-cost decision metrics after spread, slippage, fees when configured, turnover, and drawdown. Sources: [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md), [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md).

## Definition Of Done

- Offline data schemas include event and availability timestamps.
- Feature builder proves `feature_available_at_max <= t_pred`.
- Baselines run before TRIDENT feature ablations.
- Validation report includes leakage, calibration, Brier score, macro F1, precision, recall, gross and net metrics.
- Backtest is event-driven for promoted results.
- No live broker endpoint, live credential path, live order router, or live-trading flag exists.

