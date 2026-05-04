# Risk Control Options

Status: Phase 0 options only. No production code. No live trading.

## Decision Criteria

- Prefer controls that can be verified in backtests and paper trading before any broker integration because TRIDENT-LOB Phase 1 is scoped to simulation, backtesting, and paper trading: ../../docs/TRIDENT_LOB_MODEL.md
- Prefer pre-trade rejection over post-trade cleanup because SEC Rule 15c3-5 requires controls designed to prevent orders that exceed thresholds or appear erroneous before entry: https://ecfr.io/Title-17/Section-240.15c3-5
- Prefer broker-specific constraints as lower bounds, not upper bounds, because Regulation T and FINRA materials allow broker house requirements to be stricter than regulatory minimums: https://www.federalreserve.gov/frrs/regulations/section-22012-supplement-margin-requirements.htm and https://www.finra.org/rules-guidance/key-topics/margin-accounts
- Prefer conservative day-trading treatment until the selected broker confirms the effective implementation of SR-FINRA-2025-017, because the SEC approved the rule change on April 14, 2026 while FINRA public pages still show legacy PDT language: https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-finra-2025-017 and https://www.finra.org/rules-guidance/guidance/interps-4210

## Option A: Research-Only Ledger

Description: The system never constructs broker-ready orders. It records signals, hypothetical order intents, rejections, and simulated fills in a local research ledger.

Recommended for Phase 0 and early Phase 1 because it blocks live trading while allowing validation of features, timestamps, risk thresholds, and paper PnL accounting. This matches the model specification's simulation and backtesting scope: ../../docs/TRIDENT_LOB_MODEL.md

Benefits:

- Strongest live-trading block because no broker endpoint or credential path exists, consistent with repository hard rules: ../../AGENTS.md
- Easy replay and audit because every signal and risk decision can be logged before any external routing is introduced, consistent with SEC Rule 15c3-5 documentation and post-trade report principles: https://ecfr.io/Title-17/Section-240.15c3-5
- Reduces accidental margin and day-trading exposure because no real account can be touched, consistent with SEC and FINRA day-trading risk warnings: https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270

Costs:

- Paper assumptions may miss market impact, queue position, slippage, regulatory fees, and live fill behavior, which Alpaca explicitly lists as paper-trading limitations: https://docs.alpaca.markets/docs/trading/paper-trading/

## Option B: Broker Paper Adapter With Hard Dry-Run Default

Description: A future Phase 1 paper adapter can send orders only to a broker paper endpoint, with live endpoints unavailable at runtime.

Recommended only after Option A has passing timestamp, accounting, and rejection tests because broker paper environments can behave differently from live execution. Alpaca states paper trading is a simulation and not a substitute for real trading: https://docs.alpaca.markets/docs/trading/paper-trading/

Benefits:

- Tests broker API lifecycle, rejects, cancels, partial fills, and disconnections before live exposure, which Alpaca recommends because live-market algorithms can face unfilled orders, price spikes, network disconnects, and retries: https://docs.alpaca.markets/docs/trading/paper-trading/
- Allows API rate-limit validation against broker limits such as Alpaca's 200 requests per minute trading API throttle: https://alpaca.markets/support/usage-limit-api-calls
- Allows buying-power and order-state tests against broker paper rules, including open-order buying-power reduction and order lifecycle states: https://docs.alpaca.markets/docs/trading/orders/

Costs:

- Requires credential hygiene even for paper keys, so no keys should be committed and key loading should be externally configured under repository rules: ../../AGENTS.md
- Paper fills can overstate liquidity because Alpaca notes paper orders are not checked against NBBO quantities and paper trading does not model market impact or queue position: https://docs.alpaca.markets/docs/trading/paper-trading/

## Option C: Live-Ready Adapter Behind Governance Gate

Description: A later phase could add a broker adapter capable of live order routing, but only behind explicit human approvals, validation gates, broker review, and legal review.

Not recommended for Phase 0 or Phase 1. The project rules and model specification require live trading to be blocked until explicit validation gates, risk limits, and broker compliance checks are passed: ../../AGENTS.md and ../../docs/TRIDENT_LOB_MODEL.md

Benefits:

- Could eventually test small-real-money execution effects that paper trading does not simulate, such as market impact, information leakage, queue position, price improvement, regulatory fees, and dividends, which Alpaca identifies as paper gaps: https://docs.alpaca.markets/docs/trading/paper-trading/

Costs:

- Introduces real financial, margin, short-sale, operational, and compliance risk. SEC and FINRA warn day trading can cause large and immediate losses, margin losses beyond initial funds, and system-failure losses: https://www.sec.gov/about/reports-publications/investor-publications/day-trading-your-dollars-at-risk and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
- Requires broker-specific market access, margin, short-sale, LULD, account approval, and intraday margin compliance checks before use: https://ecfr.io/Title-17/Section-240.15c3-5, https://www.finra.org/rules-guidance/key-topics/margin-accounts, https://www.sec.gov/investor/pubs/regsho.htm, and https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan

## Recommended Option

Use Option A for Phase 0 and early Phase 1. Allow Option B only after validation tests prove that risk rejections, logging, data freshness checks, future-data guards, and paper ledger accounting work locally. Do not implement Option C in Phase 0 or Phase 1. This sequence follows the project model scope and uses pre-trade control principles from SEC Rule 15c3-5: ../../docs/TRIDENT_LOB_MODEL.md and https://ecfr.io/Title-17/Section-240.15c3-5
