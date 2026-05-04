# Decision

## Primary decision

Build Phase 1 around an event-driven research backtester with pluggable execution simulation. The engine must process timestamped inputs in chronological order and must reject any feature, prediction, news event, quote, trade, session state, or halt state whose `available_at` is after the decision timestamp. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Use vectorized backtesting only as a fast diagnostic layer for simple baseline screens and cost sweeps. Do not promote a vectorized result to paper trading unless the same strategy passes the event-driven simulator with identical timestamp rules, costs, risk limits, and session rules. Sources: https://vectorbt.dev/api/portfolio/base/, https://vectorbt.dev/api/portfolio/enums/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.

Add broker paper-trading APIs only after the internal event-driven simulator passes validation. Paper adapters may submit paper orders and reconcile paper order events, but they must not expose live endpoints, live credentials, or live-trading flags in Phase 1. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/.

## Execution simulation decision

The simulator must model order acceptance, queueing, latency, order expiry, cancel, replace, reject, fill, and partial-fill events. It must record every lifecycle transition as an immutable ledger event. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

Marketable buys should cross the ask plus configured slippage and marketable sells should cross the bid minus configured slippage when quote data is available. If only trade bars are available, fills must be labeled bars-only and use conservative assumptions. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/supported-models/equity-model, https://www.backtrader.com/docu/slippage/slippage/, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html.

Limit orders should fill only when the historical quote or trade evidence proves the limit was marketable after latency. Queue priority should be conservative unless L3 queue data is available. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html, https://data.lobsterdata.com/info/DataStructure.php.

Partial fills should be capped by visible size, volume participation, or a configurable conservative fill model. The simulator must not consume more historical liquidity than is available under the selected data mode. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html.

Latency must be represented as an interval between intent time, release time, broker receipt time if paper, market eligibility time, and fill evaluation time. The fill model must evaluate quotes and trades at or after the latency-adjusted time, never before. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/supported-models, https://docs.alpaca.markets/docs/trading/paper-trading/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Session and halt decision

The session model must include regular trading hours, holidays, early closes, extended-hours eligibility, and queued orders outside eligible sessions. Sources: https://www.nyse.com/markets/hours-calendars, https://docs.alpaca.markets/docs/trading/orders/.

The halt model must reject or suspend new simulated exposure when the symbol is halted, paused, in an LULD state, missing NBBO, or affected by a market-wide circuit breaker. Sources: https://www.nyse.com/markets/nyse/trading-info, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan, https://docs.alpaca.markets/docs/market-data-faq.

## Cost and constraints decision

Every report must show gross performance, net performance after configured commissions and fees, spread cost, slippage, reject counts, partial-fill counts, turnover, exposure, drawdown, and capacity diagnostics. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675.

Cash-only, long-only simulation is the default Phase 1 account type. Margin, leverage, and short-sale simulation are disabled by default and require explicit paper-only approval plus current rules for margin, short sale locates, and broker house constraints. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.sec.gov/investor/pubs/regsho.htm, https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210, https://www.finra.org/rules-guidance/key-topics/margin-accounts.

The risk manager must run before the simulated execution venue and before any paper adapter. It must reject orders that breach cash, position, gross exposure, symbol exposure, order-rate, price-collar, stale-data, halt, or model-health limits. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5.

## Paper trading path

The strict path is research signal, vectorized diagnostic if useful, event-driven backtest, walk-forward out-of-sample evaluation, transaction-cost-adjusted report, validation gate, paper account dry run, paper API adapter, paper reconciliation report, and manual review. No step in this path permits live trading in Phase 1. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://docs.alpaca.markets/docs/trading/paper-trading/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

The first paper adapter should target Alpaca paper only if credentials are available outside the repo and the account is configured as paper-only. IBKR PaperTrader should remain a later comparison because it requires TWS or Gateway setup and has simulator-specific limitations. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

## Non-decisions

This decision does not approve live trading, live broker endpoints, live-trading credentials, margin use, short selling, paid data purchase, production ingestion, or profitability claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Open questions

The default numerical values for latency, spread padding, slippage, volume participation, and reject probabilities remain unsettled and should be calibrated by data mode, symbol liquidity, session, and broker paper comparison. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/supported-models, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html.

The project still needs final feature and prediction-model DECISION files from research/08 and research/09 before the backtester can freeze its signal and label contract. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/08-feature-engineering-and-labels/README.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/09-prediction-models-and-baselines/README.md.

The correct paper broker for Phase 1 remains open until credential availability, data entitlements, supported symbols, and account restrictions are known. Sources: https://docs.alpaca.markets/docs/market-data-faq, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/.
