# Risk Controls Decision

Status: Phase 0 decision. This does not authorize live trading.

## Decision

TRIDENT-LOB will use a research-only risk-control design for Phase 0 and Phase 1. The system may produce signals, local order intents, rejects, simulated fills, and paper ledgers, but it must not contain a live broker endpoint, live credential path, live order router, or live-trading enable flag during Phase 0 or Phase 1. This follows the repository hard rules and the model specification's statement that the first implementation should be simulation, backtesting, and paper trading with live trading blocked by validation gates: ../../AGENTS.md and ../../docs/TRIDENT_LOB_MODEL.md

## Required Phase 1 Defaults

- `mode`: `DRY_RUN` by default and required for all Phase 1 runs. Dry-run mode may log hypothetical order intents but must not submit real orders. This follows the project scope and FINRA's warning that day trading can create large immediate losses: ../../docs/TRIDENT_LOB_MODEL.md and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
- `live_trading_enabled`: prohibited in Phase 0 and Phase 1. Any code path that could send live orders must fail closed because SEC Rule 15c3-5 emphasizes controlled access and pre-trade risk controls for market-access systems: https://ecfr.io/Title-17/Section-240.15c3-5
- `max_daily_loss`: stop generating new paper exposure at the lesser of 1 percent of paper equity or 2 times the 20-day median simulated daily loss. This is an internal conservative threshold chosen to satisfy pre-set financial exposure control principles and day-trading risk warnings: https://ecfr.io/Title-17/Section-240.15c3-5 and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
- `max_position_notional`: cap each paper position at the lesser of 2 percent of paper equity, 5 percent of the symbol's average 1-minute dollar volume, or the approved symbol cap. This creates symbol-specific pre-set capital thresholds consistent with SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- `max_symbol_exposure`: cap each symbol at 5 percent of total paper gross exposure. This is a symbol-level risk threshold consistent with SEC Rule 15c3-5's sector, security, or other threshold language: https://ecfr.io/Title-17/Section-240.15c3-5
- `max_gross_exposure`: cap total paper gross exposure at 25 percent of paper equity unless a later validation gate lowers the limit. Conservative leverage is required because SEC and FINRA warn margin and day trading can generate severe losses: https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
- `max_orders_per_minute`: cap global paper order intents at 30 per minute and per-symbol paper order intents at 5 per minute. This is below Alpaca's documented 200 requests per minute throttle and supports erroneous or duplicative order controls under SEC Rule 15c3-5: https://alpaca.markets/support/usage-limit-api-calls and https://ecfr.io/Title-17/Section-240.15c3-5
- `price_collar`: reject paper intents outside a configurable NBBO-based collar and reject all intents when NBBO is stale or absent. This supports erroneous-order protection and LULD-aware price discipline: https://ecfr.io/Title-17/Section-240.15c3-5 and https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan
- `short_sales`: disabled by default. Short simulation requires explicit paper approval, borrow availability fields, locate status fields, and Reg SHO modeling because Regulation SHO requires locate and documentation before short sales: https://www.sec.gov/investor/pubs/regsho.htm and https://ecfr.io/Title-17/Part-242/SubjectGroup-regulation-sho-regulation-of-short-sales
- `margin`: disabled by default. Margin simulation requires Regulation T, FINRA Rule 4210, selected broker house rules, and intraday margin handling because margin requirements come from federal regulation, FINRA rules, and broker requirements: https://www.federalreserve.gov/frrs/regulations/section-22012-supplement-margin-requirements.htm, https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210, and https://www.finra.org/rules-guidance/key-topics/margin-accounts

## Kill Switches

The system must halt new paper exposure and log the cause when any condition below occurs:

- Daily loss threshold breached, because pre-set financial thresholds are required for market-access style controls: https://ecfr.io/Title-17/Section-240.15c3-5
- Single-symbol, gross, or order-rate threshold breached, because SEC Rule 15c3-5 calls for capital, price, size, and duplicative-order controls: https://ecfr.io/Title-17/Section-240.15c3-5
- Model returns NaN, infinity, stale version, unapproved version, schema mismatch, or impossible confidence, because erroneous-order protection requires failing closed: https://ecfr.io/Title-17/Section-240.15c3-5
- Data feed is stale, out of order, duplicated beyond tolerance, missing NBBO, missing halt status, or timestamped after the decision time, because the repository prohibits future data and FINRA warns system failures can cause losses: ../../AGENTS.md and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
- Symbol is halted, paused, in LULD limit state, or market-wide circuit breaker state is active, because LULD and circuit breaker mechanics can prevent normal execution: https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan and https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/measures
- Broker paper API returns repeated rejects, throttles, disconnects, or inconsistent order lifecycle states, because Alpaca warns algorithms can encounter unfilled orders, price spikes, network disconnects, and retries in live-market operation: https://docs.alpaca.markets/docs/trading/paper-trading/
- Manual operator halt is requested, because SEC Rule 15c3-5 requires access control and documented supervisory procedures: https://ecfr.io/Title-17/Section-240.15c3-5

## Manual Approvals

Manual approval is required for all transitions between research ledger, paper broker, and any future live-readiness review. Manual approval is also required for changes to max daily loss, max position size, max gross exposure, max orders per minute, short-sale simulation, margin simulation, data vendor changes, and model promotion. This follows FINRA's day-trading approval-procedure concept and SEC Rule 15c3-5 access-control principles: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2130 and https://ecfr.io/Title-17/Section-240.15c3-5

## Non-Decision

This decision does not select a broker, approve margin, approve short selling, approve live trading, claim profitability, or provide legal interpretation. Live trading remains blocked until every hard condition in LIVE_TRADING_BLOCKERS.md is satisfied. SEC and FINRA investor materials warn against claims of easy profits and describe day trading as highly risky: https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
