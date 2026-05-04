# Risk Controls Validation

Status: Phase 0 validation plan only. No production code. No live trading.

## Validation Principle

Risk controls must be tested before model quality claims and before any paper broker adapter. Pre-trade rejection, documented thresholds, access control, and post-decision logs are required because SEC Rule 15c3-5 describes those as core risk-management controls for market access: https://ecfr.io/Title-17/Section-240.15c3-5

## Unit-Level Validation

- Daily loss test: simulate losses crossing the max daily loss threshold and require `HALT_NEW_EXPOSURE` for all later intents that increase risk. This validates pre-set financial exposure controls under SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- Position size test: generate intents above max position notional and require rejection. This validates order size and capital threshold controls under SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- Symbol exposure test: generate same-symbol concentration above the configured cap and require rejection. This validates security-level thresholds under SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- Gross exposure test: generate portfolio exposure above the gross cap and require rejection. This validates aggregate credit and capital thresholds under SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- Order-rate test: generate more than 30 global paper intents per minute or more than 5 per symbol per minute and require rejection. This validates duplicative and short-window order controls under SEC Rule 15c3-5 and stays below Alpaca's 200 requests per minute throttle if Alpaca is used later: https://ecfr.io/Title-17/Section-240.15c3-5 and https://alpaca.markets/support/usage-limit-api-calls
- Price-collar test: generate orders outside approved collars, with missing NBBO, or during LULD states and require rejection. This validates erroneous-order and LULD-aware controls: https://ecfr.io/Title-17/Section-240.15c3-5 and https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan
- Model-failure test: generate NaN, infinity, stale model version, schema mismatch, missing calibration, and confidence outside bounds, then require rejection. This validates erroneous-order prevention under SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- Data-failure test: generate stale, out-of-order, duplicated, missing, and future-timestamped data, then require rejection. This validates repository no-future-data rules and system-failure controls: ../../AGENTS.md and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270
- Short-sale test: generate short intents without borrow availability or locate status and require rejection. This validates Regulation SHO locate modeling: https://www.sec.gov/investor/pubs/regsho.htm and https://ecfr.io/Title-17/Part-242/SubjectGroup-regulation-sho-regulation-of-short-sales
- Margin test: generate margin intents without explicit margin-simulation approval and require rejection. This validates Regulation T, FINRA margin, broker house-rule, and intraday margin readiness assumptions: https://www.federalreserve.gov/frrs/regulations/section-22012-supplement-margin-requirements.htm, https://www.finra.org/rules-guidance/key-topics/margin-accounts, and https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-finra-2025-017

## Integration Validation

- Backtest integration: replay historical data and prove every feature timestamp is less than or equal to the decision timestamp. This is required by the repository no-future-data rule and the model's timestamped event-stream design: ../../AGENTS.md and ../../docs/TRIDENT_LOB_MODEL.md
- Paper ledger integration: reconcile simulated cash, positions, realized PnL, unrealized PnL, fees, rejects, cancels, and fills after every event. This is required because the model specification requires order-book accounting checks and nonnegative liquidity or execution accounting: ../../docs/TRIDENT_LOB_MODEL.md
- Paper broker integration, later only: if Alpaca paper is used, compare local ledger state to broker paper order status streams and account snapshots. Alpaca recommends streaming updates for maintaining order state and documents paper-fill limitations: https://docs.alpaca.markets/docs/trading/orders/ and https://docs.alpaca.markets/docs/trading/paper-trading/
- Rate-limit integration: throttle all paper broker calls below documented broker limits and test 429 handling. Alpaca documents a 200 requests per minute account throttle: https://alpaca.markets/support/usage-limit-api-calls
- Halt and LULD integration: replay days with symbol halts, LULD pauses, and market-wide circuit breakers, then verify no new exposure during blocked states. LULD and market-wide circuit breakers are documented by FINRA and Investor.gov: https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan and https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/measures

## Compliance Checklist

Each item must pass before Phase 1 paper broker mode:

- No live broker endpoint exists in runtime config, because Phase 1 is simulation, backtesting, and paper trading only: ../../docs/TRIDENT_LOB_MODEL.md
- No live API key, broker credential, paid data credential, or private account data is committed, because repository rules prohibit committing credentials and private account information: ../../AGENTS.md
- Every feature has a source timestamp and data cutoff, because repository rules prohibit future data: ../../AGENTS.md
- Every recommendation and model report avoids profitability claims unless out-of-sample, transaction-cost-adjusted evidence exists, because repository rules prohibit unsupported profitability claims: ../../AGENTS.md
- Every risk decision produces an audit log, because SEC Rule 15c3-5 emphasizes documented controls and post-trade reports: https://ecfr.io/Title-17/Section-240.15c3-5
- Every rejected intent has a structured reason code, because documented controls need inspectable rejection behavior under SEC Rule 15c3-5: https://ecfr.io/Title-17/Section-240.15c3-5
- Margin simulation is disabled unless Regulation T, FINRA Rule 4210, selected broker house rules, and intraday margin implementation are configured and tested: https://www.federalreserve.gov/frrs/regulations/section-22012-supplement-margin-requirements.htm, https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210, and https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-finra-2025-017
- Short simulation is disabled unless borrow availability, locate status, close-out handling, and short marking fields are configured and tested: https://www.sec.gov/investor/pubs/regsho.htm and https://ecfr.io/Title-17/Part-242/SubjectGroup-regulation-sho-regulation-of-short-sales
- Day-trading and intraday margin logic handles both legacy PDT compatibility and the selected broker's current SR-FINRA-2025-017 implementation, because broker implementation may lag public regulatory approval: https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-finra-2025-017 and https://www.finra.org/rules-guidance/guidance/interps-4210
- Paper trading reports clearly state paper limitations, including market impact, information leakage, latency slippage, queue position, price improvement, regulatory fees, and dividends, because Alpaca identifies these as paper gaps: https://docs.alpaca.markets/docs/trading/paper-trading/

## Exit Criteria

Phase 1 paper broker mode may be considered only after all validation tests above pass for at least 20 independent replay days, including at least one high-volatility day, one halt or LULD scenario, one data-feed outage simulation, one model-failure simulation, and one broker-reject simulation. This recommendation is based on the need for documented financial, regulatory, and system-risk controls under SEC Rule 15c3-5 and day-trading risk warnings from FINRA: https://ecfr.io/Title-17/Section-240.15c3-5 and https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270

Live trading may not be considered from this validation file. Live trading remains blocked by LIVE_TRADING_BLOCKERS.md.
