# TRIDENT-LOB Orchestration Plan

Status: Phase 0 orchestration. This plan does not authorize production code, live trading code, live broker endpoints, live credentials, paid-data commits, private account information, or profitability claims.

## Operating Rules

Live trading is blocked in Phase 0 and Phase 1. Future agents may build offline research workflows, validation fixtures, backtests, dry-run order-intent logs, and paper-ledger designs only when assigned. They must not add live broker endpoints, live credentials, live-trading enable flags, or production order routers. Sources: [TRIDENT model](../docs/TRIDENT_LOB_MODEL.md), [repository rules](../AGENTS.md), [risk decision](../research/11-risk-controls-and-compliance/DECISION.md).

Every future build agent must read `docs/TRIDENT_LOB_MODEL.md`, `AGENTS.md`, this file, and the relevant research `DECISION.md`, `INTERFACE.md`, and `VALIDATION.md` before editing. If `plans/INTERFACES.md` or `plans/VALIDATION_GATES.md` are later created, build agents must read them too. Source: [repository rules](../AGENTS.md).

All recommendations in generated documents must cite local research files or external URLs. Generated documents must not use em dashes. Source: [repository rules](../AGENTS.md).

## Coding Agent Roster

| Agent | Charter | Primary research inputs | Outputs owned | May modify | Must not touch |
| --- | --- | --- | --- | --- | --- |
| A0 Contracts And Config | Define shared protocols, Pydantic schemas, config sections, manifests, and package scaffolding. | [12 decision](../research/12-python-architecture-and-stack/DECISION.md), [14 interface](../research/14-reproducibility-and-experiment-tracking/INTERFACE.md) | `RunConfig`, manifests, protocol skeletons, config examples | `src/trident_lob/contracts`, `src/trident_lob/config`, tests for contracts, non-secret config examples | Data payloads, broker code, model implementations |
| A1 Data Adapters | Build provider-neutral offline data adapters and source metadata. | [06 decision](../research/06-data-requirements-and-vendors/DECISION.md), [07 interface](../research/07-news-and-exogenous-inputs/INTERFACE.md) | Normalized bar, quote, trade, depth, news, calendar, corporate-action records | `src/trident_lob/data`, adapter tests, fixture manifests | Live broker routing, paid data payloads, secrets |
| A2 Event Store | Build immutable local event storage and query interfaces. | [06 interface](../research/06-data-requirements-and-vendors/INTERFACE.md), [12 interface](../research/12-python-architecture-and-stack/INTERFACE.md) | Parquet partition conventions, raw payload hash references, event manifests | `src/trident_lob/events`, storage tests, fixture event batches | Feature logic, models, broker APIs |
| A3 Features And Labels | Build point-in-time features, labels, split manifests, and leakage reports. | [08 decision](../research/08-feature-engineering-and-labels/DECISION.md), [07 validation](../research/07-news-and-exogenous-inputs/VALIDATION.md) | Feature tables, label tables, split manifests, leakage report | `src/trident_lob/features`, `src/trident_lob/labels`, tests for leakage and labels | Model fitting, execution simulation, live endpoints |
| A4 Turbulence Estimator | Build Phase 1 proxies for `k`, `epsilon`, `nu_t`, fragility, production terms, and `R_m`. | [02 decision](../research/02-turbulence-closure-and-fragility/DECISION.md), [01 decision](../research/01-equation-audit-and-dimensional-analysis/DECISION.md) | Turbulence feature artifacts and diagnostics | `src/trident_lob/turbulence`, estimator tests | PDE solver claims, live trading, model promotion |
| A5 Price Interface Estimator | Build L1 and bars-only price-interface proxy estimators with quality flags. | [03 decision](../research/03-latent-order-book-and-price-interface/DECISION.md), [03 validation](../research/03-latent-order-book-and-price-interface/VALIDATION.md) | `L_proxy`, `B_proxy`, interface velocity, impact proxy diagnostics | `src/trident_lob/interface`, estimator tests | Broker intents, profitability claims |
| A6 Calibration And Numerical Fixtures | Build calibration reports, synthetic finite-volume diagnostics, and numerical invariants. | [04 decision](../research/04-numerical-discretization/DECISION.md), [05 validation](../research/05-stochastic-processes-and-calibration/VALIDATION.md) | Synthetic fixtures, accounting checks, unit checks, calibration reports | `src/trident_lob/calibration`, `src/trident_lob/numerics`, tests for invariants | Full PDE production solver, live trading |
| A7 Prediction Baselines | Build no-skill, linear, and bounded nonlinear offline prediction baselines. | [09 decision](../research/09-prediction-models-and-baselines/DECISION.md), [08 interface](../research/08-feature-engineering-and-labels/INTERFACE.md) | Model fit, prediction, diagnostics, ablation reports | `src/trident_lob/models`, model tests | Data ingestion, live signal deployment |
| A8 Backtesting | Build event-driven research backtester and conservative cost and fill simulation. | [10 decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), [09 interface](../research/09-prediction-models-and-baselines/INTERFACE.md) | Offline backtest reports, dry-run ledger events, cost reports | `src/trident_lob/backtest`, backtest tests | Live broker endpoints, live order routing |
| A9 Risk Controls | Build offline risk checks for simulated and paper-intent workflows. | [11 decision](../research/11-risk-controls-and-compliance/DECISION.md), [10 interface](../research/10-backtesting-paper-trading-and-execution/INTERFACE.md) | `RiskDecision`, reject reasons, kill-switch audit events | `src/trident_lob/risk`, risk tests | Model training, live approval paths |
| A10 Validation And Benchmarks | Build validation commands, fixtures, benchmark records, and fail-closed gates. | [13 decision](../research/13-testing-validation-and-benchmarks/DECISION.md), [04 validation](../research/04-numerical-discretization/VALIDATION.md) | Unit, property, numerical, data, backtest, integration, benchmark suites | `tests`, `benchmarks`, `src/trident_lob/validation` | Component implementations except test hooks |
| A11 Reproducibility And Tracking | Build local MLflow tracking, seed manifests, DVC metadata design, audit logs, and report manifests. | [14 decision](../research/14-reproducibility-and-experiment-tracking/DECISION.md), [12 decision](../research/12-python-architecture-and-stack/DECISION.md) | Run manifests, seed manifests, audit logs, local tracking wrappers | `src/trident_lob/tracking`, `experiments` metadata templates, reproducibility tests | Secrets, paid data payloads |
| A12 Reports | Build report generator for validation, model, backtest, and research summaries. | [13 interface](../research/13-testing-validation-and-benchmarks/INTERFACE.md), [14 interface](../research/14-reproducibility-and-experiment-tracking/INTERFACE.md) | Markdown, HTML, or notebook-backed research reports with citations | `src/trident_lob/reports`, report templates, report tests | Unsupported profitability claims, private data |
| A13 Orchestration Review | Maintain task queue, handoffs, review state, and phase-gate summaries. | [15 decision](../research/15-orchestration/DECISION.md), this file | Task records, handoff summaries, phase gate status | `plans`, `research/15-orchestration` | Production package files unless assigned |

## Handoff Protocol

Every agent must hand off with the fields in [agent handoff template](AGENT_HANDOFF_TEMPLATE.md). The handoff must list files changed, validation run, validation not run, open questions, interface changes, downstream agents affected, live-trading safety, secret safety, paid-data safety, and future-data safety.

Recommendation: handoffs should be append-only and factual so later agents can work with prior edits without reverting them. Source: [repository rules](../AGENTS.md).

## Task Queue Format

Use [task template](TASK_TEMPLATE.md) for every task. The queue can live in Markdown, YAML, or an issue tracker, but each record must include:

```text
task_id
phase
owner_agent
review_agent
priority
status
objective
required_reading
allowed_paths
forbidden_paths
inputs
outputs
validation_commands
review_gates
stop_conditions
sources
```

Tasks without explicit allowed paths should not start. Tasks that need network access, paid data, credentials, paper broker access, or shared-interface changes must name the need before work begins.

## Review Protocol

Reviewers lead with risks and blockers. A review must check timestamp eligibility, split discipline, unit and nonnegativity constraints, baseline comparisons, secret hygiene, paid-data hygiene, reproducibility metadata, and live-trading blocks.

Block completion when any of these are present:

- Feature uses data with `available_at` after prediction time.
- Random row split is used for time-series validation.
- Model report lacks no-skill, ordinary microstructure, or technical baselines.
- Negative accepted liquidity, negative accepted `k`, nonpositive accepted `epsilon`, negative `nu_t`, or uncapped execution appears.
- Live broker endpoint, live credential path, live order router, or live-trading flag appears.
- API key, broker credential, paid data payload, or private account information appears.
- Profitability is claimed without out-of-sample, transaction-cost-adjusted, slippage-stressed evidence.

Sources: [feature validation](../research/08-feature-engineering-and-labels/VALIDATION.md), [prediction validation](../research/09-prediction-models-and-baselines/VALIDATION.md), [risk validation](../research/11-risk-controls-and-compliance/VALIDATION.md), [testing validation](../research/13-testing-validation-and-benchmarks/VALIDATION.md).

## Escalation Rules

Escalate to A13 before continuing if:

- A task needs files outside its allowed paths.
- Another agent has changed the same shared interface.
- A required planning file is missing or inconsistent.
- A validation gate is unclear.
- A task needs paid data, network downloads, credentials, paper broker access, margin simulation, short-sale simulation, or live-like connectivity.
- A result could be interpreted as a profitability claim.

The default escalation outcome is to narrow scope, add a validation task, or document an open question. The default is never to bypass a hard safety gate.

## Prompt Template For Future Codex Build Agents

```text
You are TRIDENT-LOB <agent name>. Work only on <allowed paths>. Do not revert or modify edits made by others. This is Phase <phase>. Live trading is blocked in Phase 0 and Phase 1.

Read first:
- docs/TRIDENT_LOB_MODEL.md
- AGENTS.md
- plans/ORCHESTRATION.md
- <relevant research DECISION.md>
- <relevant research INTERFACE.md>
- <relevant research VALIDATION.md>

Objective:
<objective>

Inputs:
<inputs>

Outputs:
<outputs>

Forbidden:
<forbidden paths and behaviors>

Validation:
<commands and gates>

Stop and escalate if you need files outside scope, paid data, credentials, network access, paper broker access, live endpoints, or a shared-interface change not listed here.

At closeout, provide a handoff using plans/AGENT_HANDOFF_TEMPLATE.md fields.
```

## Phased Implementation Plan

### Phase 0: Planning And Contracts

Purpose: finish repository-level planning, consolidate interfaces, define validation gates, create task queue, and assign component ownership.

Allowed work: documentation, templates, interface sketches, validation plans, and synthetic fixture designs.

Blocked work: production package implementation, live trading code, broker routing, paid data purchase, secret handling, profitability claims.

Definition of done:

- Required Phase 0 deliverables exist and cite sources.
- Orchestration, task, and handoff templates exist.
- Missing repository-level interface and validation documents are either created by a future scoped task or recorded as open questions.
- Phase 1 tasks have owners, allowed paths, forbidden paths, validation commands, and review owners.

Sources: [repository rules](../AGENTS.md), [TRIDENT model](../docs/TRIDENT_LOB_MODEL.md).

### Phase 1A: Scaffolding And Validation Skeleton

Purpose: create CPU-only Python project scaffolding, dependency lock, component protocols, manifests, fixture structure, and initial validation commands.

Definition of done:

- Native arm64 Python 3.12 CPU-only environment is documented.
- `uv` lock exists.
- Core package skeleton follows swappable components.
- `ruff`, `mypy`, and `pytest` gates exist.
- No live endpoint, live credential, or trading router exists.

Sources: [architecture decision](../research/12-python-architecture-and-stack/DECISION.md), [stack validation](../research/12-python-architecture-and-stack/VALIDATION.md).

### Phase 1B: Offline Data And Event Store

Purpose: build provider-neutral offline records, local immutable event storage, data manifests, calendars, and small safe fixtures.

Definition of done:

- Bars, quotes, trades, depth, news, calendar, and corporate-action schemas include event and availability timestamps.
- Parquet round trips pass.
- Dataset manifests include source, license, delay class, and commit policy.
- Secret and paid-data checks pass.
- L2 or L3 claims are not made from bars or L1 fixtures.

Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), [data validation](../research/06-data-requirements-and-vendors/VALIDATION.md).

### Phase 1C: Features, Labels, And Splits

Purpose: build point-in-time feature rows, label rows, split manifests, and leakage reports.

Definition of done:

- `feature_available_at_max_ns <= t_pred_ns` passes for all accepted feature rows.
- Labels are separate from features and use declared horizons.
- Split manifests use chronological splits and embargo.
- Required ordinary microstructure, technical, TRIDENT proxy, and optional news feature contracts exist.
- Bars-only degraded mode is explicit.

Sources: [feature decision](../research/08-feature-engineering-and-labels/DECISION.md), [news validation](../research/07-news-and-exogenous-inputs/VALIDATION.md).

### Phase 1D: Estimators And Baselines

Purpose: build turbulence proxies, price-interface proxies, simple calibration reports, and no-skill, linear, and bounded nonlinear prediction baselines.

Definition of done:

- `k`, `epsilon`, `nu_t`, fragility, production terms, `R_m`, and L1 price-interface proxy include units and quality flags.
- OFI, spread, depth, realized volatility, time-of-day, and technical baselines are present.
- Logistic regression and ridge baselines run offline.
- TRIDENT features are reported only as incremental ablations.
- No model promotion or profitability claim is made.

Sources: [turbulence decision](../research/02-turbulence-closure-and-fragility/DECISION.md), [price-interface decision](../research/03-latent-order-book-and-price-interface/DECISION.md), [prediction decision](../research/09-prediction-models-and-baselines/DECISION.md).

### Phase 1E: Backtesting, Risk, And Dry-Run Ledger

Purpose: build event-driven research backtesting, conservative fill and cost simulation, risk checks, and dry-run ledger events.

Definition of done:

- Backtester processes inputs in chronological availability order.
- Costs include spread, slippage, fees when configured, turnover, drawdown, and net metrics.
- Cash-only, long-only is the default.
- Risk manager rejects stale data, model failures, halt states, LULD states, exposure breaches, short simulation, margin simulation, and live mode.
- Dry-run ledger reconciles cash, positions, orders, fees, and rejects.
- No paper broker API is required for Phase 1E completion.

Sources: [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), [risk validation](../research/11-risk-controls-and-compliance/VALIDATION.md).

### Phase 1F: Reproducibility, Reporting, And Benchmarks

Purpose: make each accepted run reproducible and reportable with local tracking, audit logs, seed manifests, and benchmarks.

Definition of done:

- Run manifests include dependency lock hash, config hash, seed manifest, dataset IDs, feature IDs, model ID, validation status, and audit log ID.
- Local MLflow tracking logs params, metrics, artifacts, data inputs, validation summaries, and reports.
- Reports cite data, configs, model IDs, validation status, and sources.
- Benchmarks record data shape, row counts, event counts, feature counts, wall time, and CPU context.
- Reports reject secrets, paid data excerpts, private account information, live-trading language, and unsupported profitability claims.

Sources: [reproducibility decision](../research/14-reproducibility-and-experiment-tracking/DECISION.md), [testing decision](../research/13-testing-validation-and-benchmarks/DECISION.md).

### Phase 2: L2 Or L3 Event Replay And Fuller TRIDENT Validation

Purpose: add serious L2 or L3 event replay, source and sink accounting, finite-volume diagnostics, and fuller price-grid validation after Phase 1 baselines and gates pass.

Definition of done:

- L2 or L3 data source is licensed, budgeted, and manifest-controlled.
- Replay reconstructs nonnegative visible book states.
- Adds, cancellations, modifications, executions, and boundary flux reconcile to depth changes.
- Finite-volume diagnostics pass positivity, accounting, stability, symmetry, known-model, and convergence gates.
- Full source-sink validation claims are based only on L2 or L3 evidence.
- Live trading remains unapproved unless a later phase creates and passes separate live-readiness gates.

Sources: [numerical decision](../research/04-numerical-discretization/DECISION.md), [calibration validation](../research/05-stochastic-processes-and-calibration/VALIDATION.md), [data decision](../research/06-data-requirements-and-vendors/DECISION.md).

## Open Questions

Should future agents split `plans/INTERFACES.md` into component-specific interface files after Phase 1 scaffolding begins?

Which `epsilon` estimator becomes default after the first Phase 1 validation run?

What sample-count and metric thresholds promote a model from diagnostic to accepted baseline?

What exact paper broker, if any, should be considered after internal simulator and risk gates pass?
