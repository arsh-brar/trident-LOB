# Phase 3 Paper-Trading Plan

Status: Phase 0 plan. Paper trading is not approved until Phase 1 offline gates pass and the user explicitly approves a Phase 3 task.

## Goal

Connect validated offline signals to a paper-only broker workflow that streams or replays quotes, trades, and optional news, produces predictions, emits paper order intents, applies risk controls, reconciles simulated and broker-paper fills, and produces audit reports. Sources: [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), [risk decision](../research/11-risk-controls-and-compliance/DECISION.md), https://docs.alpaca.markets/docs/trading/paper-trading/.

## Preconditions

- Phase 1 passes all leakage, baseline, cost, reproducibility, and risk gates.
- Paper broker credentials are stored outside the repo.
- Paper account mode is proven by configuration and connection tests.
- No live endpoint or live credential is reachable from the paper adapter.
- Manual approval exists for paper-only work.

Sources: [risk blockers](../research/11-risk-controls-and-compliance/LIVE_TRADING_BLOCKERS.md), [VALIDATION_GATES](VALIDATION_GATES.md), https://ecfr.io/Title-17/Section-240.15c3-5.

## Scope

Allowed:

- Paper-only quotes, trades, order intents, simulated fills, paper fills, rejects, cancels, and reconciliation logs.
- Risk checks before every paper intent.
- Conservative order-rate, exposure, price-collar, stale-data, halt, and model-health controls.
- Reports comparing offline event-driven simulation to paper-broker behavior.

Blocked:

- Live broker endpoints.
- Live credentials.
- Live order router.
- Margin or short-sale simulation unless separately approved for paper-only modeling.
- Profitability claims.

Sources: [risk decision](../research/11-risk-controls-and-compliance/DECISION.md), [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Definition Of Done

- Paper adapter proves paper-only mode.
- Dry-run ledger and paper-broker ledger reconcile.
- Risk manager rejects stale data, missing NBBO, halts, LULD states, excessive exposure, excessive orders, and model failures.
- Paper report includes slippage, rejects, partial fills, turnover, drawdown, and net metrics.
- Live trading remains blocked.

