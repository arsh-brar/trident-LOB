# TRIDENT-LOB Risk Register

Status: Phase 0 risk register. This is not legal, financial, or trading advice.

| ID | Risk | Severity | Phase | Mitigation | Sources |
| --- | --- | --- | --- | --- | --- |
| R1 | Future data leakage makes results invalid. | Critical | 1 | Enforce `available_at <= t_pred`, chronological splits, embargo, and leakage tests. | [feature validation](../research/08-feature-engineering-and-labels/VALIDATION.md), https://scikit-learn.org/stable/common_pitfalls.html |
| R2 | Backtest overfitting creates false confidence. | Critical | 1 | Require simple baselines, walk-forward validation, held-out tests, and no profitability claim. | [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 |
| R3 | TRIDENT proxies are mistaken for structural proof. | High | 1 | Label bars-only and L1 proxies as nonstructural, require L2/L3 for source/sink validation. | [turbulence decision](../research/02-turbulence-closure-and-fragility/DECISION.md), [data decision](../research/06-data-requirements-and-vendors/DECISION.md) |
| R4 | Paid data or credentials are committed. | Critical | All | Use `.env.example`, Keychain or password manager, DVC metadata, and secret scans. | [data plan](DATA_PLAN.md), https://docs.github.com/ignore-files |
| R5 | Live trading slips into Phase 0 or Phase 1. | Critical | 0, 1 | Block live endpoints, live credentials, live router, and live-trading flags. | [risk blockers](../research/11-risk-controls-and-compliance/LIVE_TRADING_BLOCKERS.md), https://ecfr.io/Title-17/Section-240.15c3-5 |
| R6 | Execution simulator overstates fill quality. | High | 1 | Use conservative fills, spread, slippage, latency, partial-fill caps, and rejects. | [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts |
| R7 | News features leak revisions or later publication. | High | 1 | Use `available_at`, first-seen timestamps, separate scheduled and actual events, and point-in-time novelty. | [news decision](../research/07-news-and-exogenous-inputs/DECISION.md), https://www.sec.gov/search-filings/edgar-application-programming-interfaces |
| R8 | Nonnegative liquidity or `epsilon` constraints fail. | High | 2 | Require positivity-preserving updates, capped execution sinks, and numerical validation. | [numerical decision](../research/04-numerical-discretization/DECISION.md), https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/ |
| R9 | Mac M3 performance blocks local iteration. | Medium | 1 | Use Polars, DuckDB, Parquet, NumPy/SciPy, scikit-learn, and benchmark reports. | [architecture decision](../research/12-python-architecture-and-stack/DECISION.md), [testing decision](../research/13-testing-validation-and-benchmarks/DECISION.md) |
| R10 | Paper broker behavior differs from simulator. | Medium | 3 | Reconcile paper fills, rejects, cancels, and latency against internal ledger. | [paper plan](PHASE_3_PAPER_TRADING.md), https://docs.alpaca.markets/docs/trading/paper-trading/ |

## Global Controls

- Stop work if a task needs credentials, paid data, paper broker access, live-like connectivity, or files outside scope without explicit approval.
- Do not claim profitability without out-of-sample, transaction-cost-adjusted, slippage-stressed evidence.
- Prefer simple baselines before complex models.
- Record open questions rather than guessing.

Sources: [repository rules](../AGENTS.md), [orchestration plan](ORCHESTRATION.md), [risk decision](../research/11-risk-controls-and-compliance/DECISION.md).

