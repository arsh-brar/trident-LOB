# Validation

## Required gates

Gate 1 is file and mode safety. Phase 1 must have no live broker endpoint, no live credentials, no live mode flag, no order router to a production account, and no code path that places real trades. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5.

Gate 2 is timestamp safety. Every market event, feature, prediction, news event, session state, halt state, and corporate action must satisfy `available_at <= decision_time` before it can influence an order intent. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Gate 3 is session safety. Orders must be accepted only in eligible sessions, with regular sessions, early closes, holidays, extended-hours eligibility, and queued order behavior represented explicitly. Sources: https://www.nyse.com/markets/hours-calendars, https://docs.alpaca.markets/docs/trading/orders/.

Gate 4 is halt safety. New simulated exposure must be rejected when symbol halts, LULD states, missing NBBO, stale quotes, or market-wide circuit breaker states make execution invalid. Sources: https://www.nyse.com/markets/nyse/trading-info, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan, https://docs.alpaca.markets/docs/market-data-faq.

Gate 5 is accounting safety. Cash, positions, open orders, reserved buying power, fees, realized PnL, unrealized PnL, and exposure must reconcile after every execution event. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.

Gate 6 is fill realism. The simulator must test no-fill, full-fill, partial-fill, stale-data reject, price-collar reject, limit-not-reached, market-crossing, volume-cap, latency-adjusted, and halt-reject scenarios. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://www.backtrader.com/docu/slippage/slippage/, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html.

Gate 7 is cost realism. Every strategy report must include net-of-cost performance, spread cost, slippage cost, commissions and fees when configured, turnover, capacity, and sensitivity to worse costs. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/supported-models, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675.

Gate 8 is constraints safety. Cash-only, long-only must be the default. Short-sale and margin scenarios must reject by default and must pass separate rule-aware simulations before any paper enablement. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.sec.gov/investor/pubs/regsho.htm, https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210.

Gate 9 is out-of-sample discipline. No paper run should be approved from an in-sample backtest alone. The report must include walk-forward or other time-respecting splits, baseline comparison, parameter-count disclosure, and no profitability claim. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675.

Gate 10 is paper reconciliation. Before paper API use, the internal simulator must pass deterministic replay tests. After paper API use, paper fills, rejects, cancels, positions, cash, and broker-reported account state must reconcile to the internal ledger or produce a documented break. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

## Required test fixtures

Use a normal session fixture with liquid quotes and trades to verify basic market and limit order behavior. Sources: https://www.nyse.com/markets/hours-calendars, https://docs.alpaca.markets/docs/trading/orders/.

Use an early-close and holiday fixture to verify that orders do not execute in closed sessions and that eligible queued orders are handled explicitly. Sources: https://www.nyse.com/markets/hours-calendars, https://docs.alpaca.markets/docs/trading/orders/.

Use a halt and LULD fixture to verify reject or suspend behavior. Sources: https://www.nyse.com/markets/nyse/trading-info, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan.

Use a stale quote fixture and an out-of-order event fixture to verify data freshness rejects and monotonic replay. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://docs.alpaca.markets/docs/market-data-faq.

Use a partial-fill fixture with limited quote size or volume cap to verify remaining quantity, average fill price, and reserved cash behavior. Sources: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts, https://zipline.ml4trading.io/_modules/zipline/finance/slippage.html.

Use a rejected short-sale fixture and rejected margin fixture to verify Phase 1 defaults. Sources: https://www.sec.gov/investor/pubs/regsho.htm, https://www.finra.org/rules-guidance/key-topics/margin-accounts.

## Promotion path

Stage 0 is offline research backtest with deterministic fixtures and no broker credentials. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Stage 1 is broader historical replay with out-of-sample splits, baseline comparison, and transaction-cost sensitivity. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675.

Stage 2 is paper dry run that creates order intents and ledger events without submitting to a broker paper API. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://ecfr.io/Title-17/Section-240.15c3-5.

Stage 3 is paper API submission to an explicitly paper-only account, with paper credentials stored outside the repository and no live endpoint available. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://support.apple.com/guide/keychain-access/welcome/mac.

Stage 4 is paper reconciliation and manual review. Live trading remains blocked in Phase 1 regardless of paper results. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Failure conditions

Fail validation if a test detects future data, same-bar fill ambiguity that was not made conservative, missing session state, missing halt state, negative cash in cash mode, negative positions in long-only mode, live endpoint strings, live credential names, unknown model version, nonfinite prediction, unreconciled paper account state, or any report that claims profitability without out-of-sample net evidence. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://ecfr.io/Title-17/Section-240.15c3-5, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Open questions

The exact threshold for acceptable simulator-to-paper fill divergence is open and should be broker-specific. Sources: https://docs.alpaca.markets/docs/trading/paper-trading/, https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm.

The exact validation horizon and sample size for paper trading promotion are open because they depend on final feature and prediction-model decisions. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/08-feature-engineering-and-labels/README.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/09-prediction-models-and-baselines/README.md.

The exact transaction fee model is open until a broker, venue, and asset universe are selected. Sources: https://docs.alpaca.markets/docs/trading/orders/, https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts.
