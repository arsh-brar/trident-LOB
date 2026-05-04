# Options

## Option A: Vectorized research backtester

A vectorized backtester computes positions, returns, costs, and metrics from arrays or DataFrames. It is attractive for early Phase 1 screening because it is fast, CPU-friendly, and simple to run across symbols and parameter grids. Sources: https://vectorbt.dev/api/portfolio/base/, https://numpy.org/install/, https://docs.pola.rs/user-guide/concepts/lazy-api/.

Use this option only for first-pass bar-based diagnostics, baseline checks, and sensitivity analysis. Do not use it as the final execution simulator because partial fills, latency, order queueing, session gates, halts, and rejects are easier to audit in an event-driven loop. Sources: https://vectorbt.dev/api/portfolio/base/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Strengths: simple, fast, repeatable, and useful for coarse transaction-cost sweeps. Sources: https://vectorbt.dev/api/portfolio/base/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675.

Weaknesses: weaker lifecycle realism, weaker ordering semantics, and higher risk that a strategy accidentally uses same-bar or future information if timestamps are not enforced separately. Sources: https://vectorbt.dev/api/portfolio/enums/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Option B: Event-driven research backtester

An event-driven backtester processes market events, feature snapshots, model predictions, risk checks, order intents, simulated exchange responses, fills, cancels, rejects, and portfolio updates in chronological order. This should be the default TRIDENT-LOB Phase 1 design. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts, https://data.lobsterdata.com/info/DataStructure.php.

Use this option as the main research engine because it can enforce `available_at <= decision_time`, session state, halts, LULD gates, stale NBBO rejection, order latency, partial fills, and cash or margin constraints. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://www.nyse.com/markets/hours-calendars, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan, https://docs.alpaca.markets/docs/trading/orders/.

Strengths: realistic order lifecycle, clean audit trail, natural compatibility with later L2 or L3 replay, and clear integration with risk controls. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://data.lobsterdata.com/info/DataStructure.php, https://ecfr.io/Title-17/Section-240.15c3-5.

Weaknesses: slower than vectorized screening and more work to implement. The design should stay modular and CPU-only to match Phase 1 architecture decisions. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://numpy.org/install/.

## Option C: Broker paper-trading API adapter

A broker paper adapter submits approved paper orders to a simulated broker endpoint and reconciles broker statuses back into the research ledger. It is useful only after the internal event-driven backtester passes validation. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/.

Alpaca paper trading is the lowest-friction Phase 1 candidate because the paper environment is free, uses a paper endpoint, exposes order status, and is already part of the repository data-vendor decisions. It should still be treated as a simulation because Alpaca states that paper trading differs from real trading and does not account for all market impact, information leakage, fill, liquidity, and data-source differences. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md, https://docs.alpaca.markets/docs/trading/paper-trading/, https://docs.alpaca.markets/docs/trading/orders/.

IBKR PaperTrader is a stronger later comparison for broker-style behavior because it supports many instruments and order types through TWS API, but it adds desktop or gateway complexity and its paper simulator has documented limitations such as top-of-book fill simulation and different behavior for some order types. Sources: https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm, https://api.ibkr.com/en/trading/tws.php.

Strengths: exposes real paper API status behavior, authentication handling, outages, rejects, order lifecycle events, and reconciliation issues before any live review. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/.

Weaknesses: still simulated, broker-specific, dependent on external credentials and connectivity, and not suitable as the first backtest truth source. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

## Option D: External backtesting framework

Backtrader, Zipline, and QuantConnect LEAN offer useful reference designs for slippage, fills, costs, and order models. They should inform TRIDENT-LOB interfaces, but Phase 1 should not depend on a large external engine unless it fits the chosen Python stack and timestamp contract. Sources: https://www.backtrader.com/docu/slippage/slippage/, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.

Use external frameworks as source material and test comparators, not as a required dependency. TRIDENT-LOB needs a provider-neutral event schema, TRIDENT feature ledger, and paper-only guardrails that are project-specific. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Recommendation

Choose Option B as the Phase 1 primary design, with Option A as a fast pre-screen and Option C as a gated paper reconciliation layer. Defer Option D to reference and comparison use. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts, https://vectorbt.dev/api/portfolio/base/, https://docs.alpaca.markets/docs/trading/paper-trading/.

## Open questions

Which broker paper API should be the first adapter, Alpaca or IBKR, depends on credential availability, market-data entitlement, and whether the Phase 1 scope needs only U.S. equities or broader instruments. Sources: https://docs.alpaca.markets/docs/market-data-faq, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/.

The exact external framework comparison set is unresolved. Backtrader, Zipline, and LEAN are enough for design references, but the project may not need to install them. Sources: https://www.backtrader.com/docu/slippage/slippage/, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.
