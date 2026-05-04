# Interface

## Boundary

This is a Phase 0 research interface for a future turbulence estimator component. It defines inputs, outputs, and validation expectations only. It does not define production code, live trading code, broker access, or order routing. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Input requirements

Recommendation: The minimum Phase 1 input should be point-in-time bars, top-of-book quotes when available, trades when available, and symbol metadata including tick size. Ticks remain the internal coordinate. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes.

Required Phase 1 fields:

```text
symbol
venue or feed
event_ts
decision_ts
mid_price
bid_price
ask_price
bid_size
ask_size
trade_price, optional
trade_size, optional
trade_sign, optional
bar_ohlcv, optional
tick_size
halt_or_session_state, optional
```

Recommendation: L2 or L3 extensions should add price-level depth, event action, order ID when available, side, price, size, and sequence or matching-engine timestamp. This is required for source and sink accounting and quote-shear production. Sources: https://databento.com/docs/schemas-and-data-formats/mbp-10, https://databento.com/docs/schemas-and-data-formats, https://lobster-data.de/info/DataStructure.php.

L2 or L3 fields:

```text
level
side
price_ticks
size_shares
order_count, optional
event_action, optional
order_id, optional
sequence_number, optional
```

Recommendation: Optional news input should be a timestamped event stream with source, relevance, sentiment, novelty, symbol mapping, and release timestamp. It must be point-in-time and must not use revised or future data. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://www.nyse.com/markets/hours-calendars.

## Output contract

Recommendation: The turbulence estimator should output only features and diagnostics, not trade decisions. Outputs should be keyed by `symbol`, `decision_ts`, `horizon`, and `window`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Required outputs:

```text
k
k_method
epsilon
epsilon_method
nu_t
fragility
fragility_percentile
P_imbalance
P_withdrawal
P_shear, optional
P_news, optional
R_m, optional
quality_flags
source_data_level
```

Recommended units:

```text
price coordinate: ticks
time: seconds
k: ticks squared per second squared
epsilon: ticks squared per second cubed
nu_t: ticks squared per second
fragility: derived closure units
depth: shares
imbalance: shares per second or OFI units per second
```

Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

## Estimator methods

Recommendation: The interface should allow swappable estimator methods for `k`, `epsilon`, and production terms. This follows the project modularity rule and allows direct baseline comparison. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://doi.org/10.1198/073500102753410408.

Supported `k_method` values:

```text
realized_tick_variance
quote_motion_variance
residual_energy
```

Supported `epsilon_method` values:

```text
volatility_decay
spread_recovery
depth_recovery
closure_residual
```

Supported production flags:

```text
imbalance
withdrawal
shear
news
```

## Quality flags

Recommendation: Every output row should carry quality flags because turbulence proxies can become invalid under stale data, crossed markets, missing depth, halted sessions, zero denominators, or insufficient window length. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Quality flags:

```text
OK
INSUFFICIENT_WINDOW
STALE_INPUT
CROSSED_OR_LOCKED_MARKET
MISSING_DEPTH
ZERO_OR_NEGATIVE_EPSILON
HALT_OR_SESSION_BREAK
OUT_OF_ORDER_EVENT
FUTURE_DATA_RISK
L2_L3_REQUIRED
```

## Baseline interface

Recommendation: The same feature table should include baseline columns or join keys for realized volatility, GARCH forecasts, stochastic volatility forecasts, OFI, spread, depth, VPIN-like toxicity, and Hawkes intensities where available. This prevents TRIDENT features from being evaluated in isolation. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1016/0304-4076(86)90063-1, https://doi.org/10.1198/073500102753410408, https://arxiv.org/abs/1011.6402, https://doi.org/10.1093/rfs/hhs053, https://arxiv.org/abs/1502.04592.

## Downstream handoff

Recommendation: Downstream prediction models should receive only timestamp-safe features and labels generated after the feature decision time. No future returns, future recovery times, revised news, or post-window events may enter feature rows. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

The turbulence estimator hands off feature rows to the feature builder and validation components. It does not hand off orders, routes, broker instructions, or live credentials.
