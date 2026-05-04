# Interface

## Purpose

This document defines Phase 0 research interfaces for later agents. It is not production code and does not define trading behavior.

## Unit configuration

Recommended interface:

```text
UnitConfig
  symbol: string
  venue: string optional
  timestamp: datetime
  price_coordinate: "ticks"
  tick_size: float
  raw_price_currency: string optional
  time_unit: "seconds"
  size_unit: "shares"
  normalization_window: string
```

Recommendation: make `tick_size` point-in-time metadata rather than a hardcoded constant, because minimum price increments can vary by security and rule. Source: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes

## Observed L1 input

Recommended interface:

```text
TopOfBookRecord
  symbol: string
  ts_event: datetime
  bid_px_raw: float
  ask_px_raw: float
  bid_px_tick: int
  ask_px_tick: int
  bid_size: float
  ask_size: float
  last_trade_px_raw: float optional
  last_trade_size: float optional
  trade_side: string optional
```

Recommendation: support L1 top-of-book and trades in Phase 1 because normalized data providers expose top-of-book, trades, and bar schemas separately. Source: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

## Observed bar input

Recommended interface:

```text
BarRecord
  symbol: string
  ts_start: datetime
  ts_end: datetime
  open_raw: float
  high_raw: float
  low_raw: float
  close_raw: float
  volume: float
  vwap_raw: float optional
```

Recommendation: use bars for Phase 1 bootstrapping only, because OHLCV supports realized-volatility proxies but not source and sink validation. Source: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

## Phase 2 event input

Recommended interface:

```text
BookEventRecord
  symbol: string
  ts_event: datetime
  event_type: "add" | "cancel" | "delete" | "execute_visible" | "execute_hidden" | "replace" | "halt" | "resume"
  order_id: string optional
  side: "bid" | "ask" | "unknown"
  price_raw: float optional
  price_tick: int optional
  size: float
```

Recommendation: Phase 2 should require event replay for source, cancellation, and execution estimation, because LOBSTER-style data exposes message files with event type, order id, size, price, and direction. Source: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

## Estimated state output

Recommended interface:

```text
TridentStateRecord
  symbol: string
  ts_event: datetime
  mid_px_raw: float
  mid_px_tick: float
  spread_ticks: float
  spread_bps: float
  depth_top: float
  imbalance_I: float
  k: float
  epsilon: float
  nu_t: float
  fragility: float
  R_m: float
  news_score_signed: float optional
  news_intensity: float optional
```

Recommendation: report `k`, `epsilon`, `nu_t`, and `R_m` with component fields, because the market Reynolds number is sensitive to depth floors, k floors, epsilon floors, and damping. Source: Cont, Kukanov, and Stoikov on OFI and depth sensitivity, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

## PDE grid state for Phase 2

Recommended interface:

```text
PriceGridState
  symbol: string
  ts_event: datetime
  price_tick_center: int array
  q_plus: float array
  q_minus: float array
  u_plus: float array optional
  u_minus: float array optional
  lambda_plus: float array optional
  lambda_minus: float array optional
  mu_plus: float array optional
  mu_minus: float array optional
  e_plus: float array optional
  e_minus: float array optional
  k: float array optional
  epsilon: float array optional
  nu_t: float array optional
```

Recommendation: store price-level arrays on a tick grid and track optional source and sink arrays separately, because conservation validation requires comparing integrated source and sink terms against event totals. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Patankar finite-volume reference, https://www.routledge.com/product/isbn/9780891165224

## Parameter interface

Recommended interface:

```text
EquationParameters
  C_mu: float
  epsilon_0: float
  k_0: float
  D_star: float
  gamma_u: float
  sigma_q: float
  sigma_k: float
  sigma_epsilon: float
  chi_P: float
  chi_nu: float
  C_u: float
  C_I: float
  C_c: float
  C_N: float
```

Required constraints:

- `C_mu >= 0`
- `epsilon_0 > 0`
- `k_0 > 0`
- `D_star > 0`
- `gamma_u >= 0`
- `sigma_q > 0`
- `sigma_k > 0`
- `sigma_epsilon > 0`
- `chi_P >= 0`
- `chi_nu >= 0`
- `C_u, C_I, C_c, C_N >= 0`

Recommendation: enforce these constraints at parameter-load time in later code, because nonnegative eddy viscosity, diffusion, production, and sink floors are required for unit consistency and stability. Source: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

## Handoff requirements

- Every state record must include enough metadata to recover the price coordinate and unit scale.
- Every feature must be computed point in time.
- Every sink must be capped by available depth in Phase 2.
- Every validation report must include the raw components of `R_m`, not just the final ratio.
- Every model comparison must include OFI or signed imbalance over depth as a baseline.

Recommendation: these handoff requirements should be treated as mandatory validation inputs, because they prevent unit ambiguity, future-data leakage, and unsupported claims beyond OFI and depth baselines. Sources: Cont, Kukanov, and Stoikov, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

