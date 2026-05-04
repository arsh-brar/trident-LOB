# Interface

## Purpose

This interface defines Phase 1 research contracts for feature rows, label rows, leakage metadata, and split manifests. It is a planning contract only and does not implement production code or trading code. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md

## Inputs

The feature builder should accept provider-neutral tables for bars, top-of-book quotes, trades, news events, calendars, corporate actions, symbol definitions, and optional market-state events. Recommendation: keep these inputs separate rather than merging them into one raw table, because data adapters and event stores must remain swappable. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Every input table must expose canonical timestamps:

```text
event_time_ns
available_at_ns
received_at_ns optional
source_published_at_ns optional
provider_updated_at_ns optional
```

Recommendation: compute features from availability time, not event time alone, because news, filings, aggregates, and vendor revisions can become observable after the economic event time. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://www.sec.gov/edgar/sec-api-documentation, https://massive.com/docs/rest/stocks/news?auth=signup

## Feature Row Contract

Each feature row must have one symbol, one prediction timestamp, one horizon family, and point-in-time metadata:

```text
symbol
venue optional
t_pred_ns
session_date
tick_size
currency
data_mode
max_feature_lookback_ns
feature_available_at_max_ns
feature_version
```

Recommendation: include `feature_available_at_max_ns` so validation can prove that no feature input became available after `t_pred_ns`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Required TRIDENT-derived feature groups:

```text
trident_k_w
trident_epsilon_w
trident_nu_t_w
trident_fragility_w
trident_fragility_pct_symbol_tod_w
trident_R_m_w
trident_P_imbalance_w
trident_P_withdrawal_w
trident_P_news_w optional
trident_L_L1_proxy
```

Recommendation: suffix features with their trailing window, for example `_30s`, `_60s`, `_300s`, because window identity is part of the feature definition and leakage audit. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/02-turbulence-closure-and-fragility/DECISION.md, https://doi.org/10.1080/713665670

Required ordinary microstructure feature groups:

```text
spread_ticks
spread_bps
mid_ticks
mid_return_lag_w
bid_size
ask_size
D_top
D_top_harmonic
D_top_min
queue_imbalance
OFI_w
signed_trade_imbalance_w optional
trade_count_w optional
quote_update_count_w
spread_change_w
session_minute
```

Recommendation: mark trade-derived features nullable rather than backfilling with future trade signs when trade classification is unavailable. Sources: https://arxiv.org/abs/1011.6402, https://databento.com/docs/knowledge-base/new-users/market-data-schemas, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md

Required technical baseline feature groups:

```text
ret_lag_w
realized_vol_w
volume_w
dollar_volume_w
vwap_distance_w
range_hl_w
momentum_w
reversal_w
ma_gap_w
```

Recommendation: all technical features must be based on completed bars or explicitly observed partial bars only. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Required news feature groups when news is enabled:

```text
N_signed_symbol_w
N_energy_symbol_w
N_count_symbol_w
N_novel_count_symbol_w
N_signed_market_w
N_energy_market_w
N_scheduled_risk_symbol_w
N_scheduled_risk_market_w
```

Recommendation: keep symbol and market news forcing separate so macro events do not masquerade as company-specific events. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://www.bls.gov/schedule/news_release/, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

## Label Row Contract

Each label row must join to a feature row by symbol and `t_pred_ns`:

```text
symbol
t_pred_ns
horizon_seconds
label_available_at_min_ns
label_version
y_return_log
y_return_ticks
y_return_bps
y_dir_cost_aware
y_spread_widen
y_local_jump
y_depth_deplete
y_fragility_persist
cost_ticks
buffer_ticks
```

Recommendation: store label availability separately from feature availability because labels intentionally use future outcomes while features must not. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

The cost-aware direction label must use the same `mid_t` observed at `t_pred_ns` and future midprice at `t_pred_ns + horizon_seconds`. If the future timestamp is missing, stale, halted, or outside the session policy, the label must be null with a reason code. Sources: https://www.nyse.com/markets/hours-calendars, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md

## Split Manifest Contract

Each dataset version must include a split manifest:

```text
dataset_id
split_id
symbol_universe
train_start_ns
train_end_ns
validation_start_ns
validation_end_ns
test_start_ns
test_end_ns
embargo_ns
max_label_horizon_ns
max_feature_lookback_ns
held_out_symbols optional
created_at_ns
```

Recommendation: make split manifests immutable for a model run so validation and test results can be reproduced without accidental split drift. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253

## Null And Quality Flags

Feature rows should include compact quality flags:

```text
has_bars
has_quotes
has_trades
has_news
is_regular_session
is_halted
is_luld_state
is_stale_quote
has_crossed_or_locked_quote
leakage_check_passed
```

Recommendation: prefer explicit nulls and quality flags over silent imputation for unavailable market structure features. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md

## Expected Outputs

The feature pipeline should output Parquet tables for features, labels, split manifests, and validation reports. Recommendation: use Parquet with Polars or DuckDB in Phase 1 because the selected stack is CPU-only and local. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://docs.pola.rs/user-guide/concepts/lazy-api/, https://duckdb.org/docs/stable/clients/python/overview, https://parquet.apache.org/docs/overview/

## Open Questions

Should feature and label tables be one wide table for model convenience or separate tables for stronger leakage auditing?

Should `horizon_seconds` be a row dimension or should each horizon become a separate wide column family?

How should split manifests represent early closes and irregular sessions?

Should null TRIDENT features fail validation or pass as degraded mode when only bars are available?

