# Research

## Scope

This Phase 0 research covers backtesting, paper trading, and execution simulation for TRIDENT-LOB. It does not approve production code, live trading code, live credentials, broker routing, or profitability claims. Phase 1 must remain CPU-only on the Mac M3 and must support simulation and paper order handling only. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://ecfr.io/Title-17/Section-240.15c3-5.

## Prior decisions to respect

Phase 1 should be a CPU-only research pipeline using bars, top-of-book quotes, trades when available, optional news, and simple baselines before complex models. The backtester should consume only point-in-time features and model outputs already available at the decision timestamp. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, https://arxiv.org/abs/1011.6402, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Backtest outputs should be treated as research evidence, not investment evidence, unless they are out-of-sample, transaction-cost-adjusted, and validated against simple baselines. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675.

Risk controls must reject live-trading code paths in Phase 0 and Phase 1. The system may produce signals, order intents, simulated fills, paper ledgers, and paper rejects, but no live broker endpoint or live enable flag. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Backtesting realism requirements

The backtester should be timestamp-driven and must never let a feature, prediction, quote, trade, halt state, corporate action, session state, or news event enter before its `available_at` timestamp. This is required because the repo prohibits future data and because backtest overfitting and look-ahead bias can make false strategies appear valid. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

The engine should model regular sessions, early closes, holidays, extended-hours eligibility, and symbol-level halts before order acceptance. This is required because U.S. equities have official session calendars, early closes, LULD mechanics, market-wide circuit breakers, and halt states that can make otherwise valid orders impossible to execute. Sources: https://www.nyse.com/markets/hours-calendars, https://www.nyse.com/markets/nyse/trading-info, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan.

The fill simulator should include spread crossing, fees, commissions, regulatory or venue fees when configured, latency, slippage, partial fills, no-fill cases, order expiry, cancels, replaces, rejects, and stale quote rejects. This is required because real and paper order life cycles include partial fills, rejected orders, no-fill cases, price movement, disconnections, and order status changes. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts.

The simulator should support both cash-only and margin-style ledgers, but Phase 1 should default to cash-only and long-only. Margin and short-sale simulation should be disabled unless a later validation gate supplies broker-specific rules, locate or borrow data, and current margin policy. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.sec.gov/investor/pubs/regsho.htm, https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210, https://www.finra.org/rules-guidance/key-topics/margin-accounts.

## Backtester families

Vectorized backtesting is best for fast screening of simple, bar-based signal rules and cost assumptions. It is not sufficient as the final Phase 1 backtester because vectorized engines can hide ordering, latency, partial-fill, halt, and reject logic unless those are explicitly represented. Sources: https://vectorbt.dev/api/portfolio/base/, https://vectorbt.dev/api/portfolio/enums/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Event-driven backtesting is best for TRIDENT-LOB because it can process feature availability, signal timestamps, order intents, quote updates, trades, session events, halts, rejects, and partial fills in chronological order. This matches the project need to respect event-time accounting and later L2 or L3 replay. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://data.lobsterdata.com/info/DataStructure.php, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.

Broker paper-trading APIs are best as a later reconciliation layer, not the first source of truth. Alpaca paper trading and IBKR PaperTrader are useful because they expose real paper order life cycles, but both are simulations with assumptions and limitations. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

## Research conclusion

Phase 1 should use a two-level design. The first level is a deterministic event-driven research backtester with pluggable cost, latency, slippage, fill, reject, session, halt, short-sale, and buying-power models. The second level is an optional paper adapter that sends only approved paper intents to paper endpoints and reconciles paper order events back into the same ledger schema. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/.

## Open questions

The 08 feature-engineering and 09 prediction-model DECISION files were not present when this document was written, so final signal and label contracts may need alignment after those agents publish decisions. Source: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/08-feature-engineering-and-labels/README.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/09-prediction-models-and-baselines/README.md.

The exact fee schedule, regulatory fees, margin rules, short-sale borrow fields, and paper broker choice are unresolved and should remain configuration decisions until a later validation gate. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.finra.org/rules-guidance/key-topics/margin-accounts, https://www.sec.gov/investor/pubs/regsho.htm.

The minimum realism required before paper trading is unresolved. A conservative gate is to require matching order-intent semantics, timestamp checks, simulated lifecycle tests, halt tests, cash tests, short-sale reject tests, and out-of-sample cost-adjusted reports before any paper API call. Sources: https://ecfr.io/Title-17/Section-240.15c3-5, https://docs.alpaca.markets/docs/trading/paper-trading/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.
