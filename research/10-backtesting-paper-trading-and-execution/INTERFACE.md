# Interface

## Component boundary

The Phase 1 backtesting package should expose swappable interfaces for data, features, predictions, risk, execution simulation, portfolio accounting, paper adapters, and reports. This follows the repository preference for modular components and the Python architecture decision. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Required input records

`MarketEvent` should include `event_id`, `symbol`, `event_type`, `event_ts`, `available_at`, `source`, `sequence`, `bid_px`, `ask_px`, `bid_sz`, `ask_sz`, `trade_px`, `trade_sz`, `bar_ohlcv`, `halt_state`, `session_state`, and raw provider metadata when available. The backtester should reject events with missing or nonmonotonic timestamps unless the data adapter has a documented repair rule. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://data.lobsterdata.com/info/DataStructure.php, https://docs.alpaca.markets/docs/market-data-faq.

`FeatureSnapshot` should include `feature_ts`, `available_at`, `symbol`, `horizon`, `feature_version`, `feature_values`, and `source_event_cutoff`. Feature snapshots must be eligible only when `available_at <= decision_time`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

`PredictionSnapshot` should include `prediction_ts`, `available_at`, `symbol`, `horizon`, `model_id`, `model_version`, `training_cutoff`, `prediction`, `confidence`, and `diagnostics`. The risk manager should reject stale, unknown, NaN, infinite, or unapproved model outputs. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5.

## Order intent contract

`OrderIntent` should include `intent_id`, `strategy_id`, `symbol`, `side`, `quantity`, `order_type`, `limit_price`, `stop_price`, `time_in_force`, `extended_hours`, `decision_time`, `release_time`, `max_latency_ms`, `account_type`, `allow_short`, `allow_margin`, `reason_code`, and `risk_context_id`. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.quantconnect.com/docs/v2/writing-algorithms/live-trading/trading-and-orders.

The allowed Phase 1 sides are buy, sell, and sell_to_close for long-only cash mode. Short sell and buy_to_cover should exist only as rejected paper-simulation states unless a later gate enables short-sale simulation. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.sec.gov/investor/pubs/regsho.htm.

The allowed Phase 1 order types should be market and limit for internal simulation. Stop, stop-limit, market-on-open, market-on-close, bracket, and trailing-stop orders should be deferred until the simulator passes simple lifecycle tests. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/supported-models/equity-model.

## Risk check contract

`RiskDecision` should include `intent_id`, `accepted`, `reject_code`, `reject_message`, `checked_at`, `cash_available`, `buying_power`, `position_before`, `position_after_if_filled`, `gross_exposure_after_if_filled`, `symbol_exposure_after_if_filled`, `price_collar`, `session_state`, `halt_state`, and `data_freshness_state`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5, https://docs.alpaca.markets/docs/trading/orders/.

Risk checks must run before simulated venue acceptance and before paper API submission. Sources: https://ecfr.io/Title-17/Section-240.15c3-5, https://docs.alpaca.markets/docs/trading/orders/.

## Execution event contract

`ExecutionEvent` should include `order_id`, `intent_id`, `event_type`, `event_ts`, `available_at`, `status`, `filled_qty`, `remaining_qty`, `fill_price`, `fees`, `spread_cost`, `slippage_cost`, `venue`, `liquidity_flag`, `reject_code`, `latency_ms`, `source`, and raw broker or simulator payload. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

Execution events should be append-only and deterministic for a fixed random seed, input event set, and simulator configuration. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://docs.python.org/3/library/random.html.

## Fill model contract

`FillModel` should expose `simulate(order, market_state, portfolio_state, config) -> list[ExecutionEvent]`. Implementations should include no_fill, immediate_crossing, quote_aware_limit, volume_participation, and L2_replay when data is available. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html, https://data.lobsterdata.com/info/DataStructure.php.

`CostModel` should expose `estimate(order, fill, market_state, config) -> CostBreakdown` with commissions, fees, spread cost, slippage, borrow cost if enabled, margin interest if enabled, and total cost. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

`LatencyModel` should expose `eligible_time(order, config) -> timestamp` and should support fixed, distributional, and replayed paper latency modes. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/supported-models, https://docs.alpaca.markets/docs/trading/paper-trading/.

## Portfolio ledger contract

`PortfolioState` should include cash, settled cash if modeled, positions, average price, realized PnL, unrealized PnL, fees, gross exposure, net exposure, symbol exposure, open orders, reserved buying power, and margin state if enabled. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.

The ledger should reserve cash or buying power for open orders and release it only on fill, cancel, expiry, or reject according to the selected account model. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.finra.org/rules-guidance/key-topics/margin-accounts.

## Paper adapter contract

`PaperTradingAdapter` should expose `submit_paper_order`, `cancel_paper_order`, `stream_paper_events`, `get_paper_account`, `get_paper_positions`, and `reconcile_paper_ledger`. The interface must not include live endpoints or live mode flags in Phase 1. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Paper adapters must write broker payloads into the same execution-event schema used by the simulator so reports can compare simulated fills against paper fills. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

## Report contract

`BacktestReport` should include data coverage, timestamp eligibility checks, session coverage, halt handling, gross returns, net returns, costs, turnover, drawdown, exposure, fill quality, reject reasons, partial-fill rate, no-fill rate, latency assumptions, slippage assumptions, paper reconciliation if present, and open validation failures. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Open questions

The exact Python protocol names and package locations should be aligned with the future repo package layout after Phase 0 orchestration creates the missing `plans/INTERFACES.md`. Source: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

The exact fields needed for borrow availability, locate status, and margin interest should remain open until a broker and data vendor are selected. Sources: https://www.sec.gov/investor/pubs/regsho.htm, https://www.finra.org/rules-guidance/key-topics/margin-accounts, https://docs.alpaca.markets/docs/trading/orders/.
