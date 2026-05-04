# Orchestration Research

Status: Phase 0 planning. This file does not authorize production code, live trading code, broker routing, paid-data commits, private credential commits, or profitability claims.

## Scope

This research synthesizes the model specification, repository rules, and research agents 00 through 14 into an orchestration plan for future build agents. The immediate goal is coordination, not implementation.

Core sources: [TRIDENT model](../../docs/TRIDENT_LOB_MODEL.md), [repository rules](../../AGENTS.md), [market microstructure decision](../00-market-microstructure-literature/DECISION.md), [architecture decision](../12-python-architecture-and-stack/DECISION.md), [testing decision](../13-testing-validation-and-benchmarks/DECISION.md), and [reproducibility decision](../14-reproducibility-and-experiment-tracking/DECISION.md).

## Synthesis

TRIDENT-LOB Phase 1 should be an offline, CPU-only Python research system on Mac M3. It should estimate simplified TRIDENT state proxies from bars, top-of-book quotes, trades when available, and optional point-in-time news. It should not solve the full PDE, place live trades, create live broker paths, or claim profitability. Sources: [TRIDENT model](../../docs/TRIDENT_LOB_MODEL.md), [market microstructure decision](../00-market-microstructure-literature/DECISION.md), [risk decision](../11-risk-controls-and-compliance/DECISION.md).

The architecture must keep major components swappable: data adapter, event store, feature builder, turbulence estimator, price-interface estimator, prediction model, backtester, paper-trading adapter, risk manager, and report generator. The selected stack is Python 3.12, `uv`, Polars, DuckDB, Parquet, NumPy, SciPy, scikit-learn, Pydantic, OmegaConf, MLflow, pytest, Ruff, mypy, pre-commit, Typer, and Click. Sources: [repository rules](../../AGENTS.md), [architecture decision](../12-python-architecture-and-stack/DECISION.md), [architecture interface](../12-python-architecture-and-stack/INTERFACE.md).

The most important cross-agent constraint is timestamp safety. Every market event, feature, news event, calendar row, corporate action, prediction, and validation record needs availability metadata. Features may use only data available at or before the prediction timestamp. Labels intentionally use future outcomes, but they must be stored separately from features and guarded by split and embargo rules. Sources: [feature decision](../08-feature-engineering-and-labels/DECISION.md), [news decision](../07-news-and-exogenous-inputs/DECISION.md), [prediction interface](../09-prediction-models-and-baselines/INTERFACE.md).

The second cross-agent constraint is structural humility. Bars and L1 quotes support Phase 1 proxies for `k`, `epsilon`, fragility, market Reynolds number, OFI, spread, depth, and L1 price-interface liquidity. They do not identify full source, cancellation, execution, queue, diffusion, or latent liquidity parameters. Full TRIDENT source and sink validation requires L2 or L3 replay. Sources: [calibration validation](../05-stochastic-processes-and-calibration/VALIDATION.md), [data decision](../06-data-requirements-and-vendors/DECISION.md), [numerical decision](../04-numerical-discretization/DECISION.md).

The third cross-agent constraint is baseline discipline. TRIDENT variables must be tested as incremental features over ordinary microstructure, technical, volatility, OFI, depth, and no-skill baselines. Complex models are deferred until simple baselines and leakage gates pass. Sources: [market validation](../00-market-microstructure-literature/VALIDATION.md), [prediction decision](../09-prediction-models-and-baselines/DECISION.md), [feature validation](../08-feature-engineering-and-labels/VALIDATION.md).

## Dependencies Between Workstreams

Data and calendar contracts precede feature building. Feature building precedes turbulence estimation, price-interface estimation, model fitting, and backtesting. Validation and reproducibility are not final polish. They must be built beside each workstream from the beginning. Sources: [data interface](../06-data-requirements-and-vendors/INTERFACE.md), [feature interface](../08-feature-engineering-and-labels/INTERFACE.md), [testing interface](../13-testing-validation-and-benchmarks/INTERFACE.md), [reproducibility interface](../14-reproducibility-and-experiment-tracking/INTERFACE.md).

Risk controls must sit between predictions and any simulated or paper order intent. Phase 0 and Phase 1 must not expose live endpoints, live credentials, live routing, or live enable flags. The default mode is `DRY_RUN`. Sources: [risk decision](../11-risk-controls-and-compliance/DECISION.md), [backtesting decision](../10-backtesting-paper-trading-and-execution/DECISION.md), [SEC Rule 15c3-5](https://ecfr.io/Title-17/Section-240.15c3-5).

## Recommended Orchestration Shape

Use a component-owned roster, not isolated research-topic ownership. Future coding agents should own narrow package areas and test artifacts. Every task must state allowed files, forbidden files, inputs to read, outputs to produce, validation commands, and handoff notes. This reduces collisions and keeps future agents inside the modular architecture selected by the research phase. Sources: [repository rules](../../AGENTS.md), [architecture decision](../12-python-architecture-and-stack/DECISION.md), [testing validation](../13-testing-validation-and-benchmarks/VALIDATION.md).

Use append-only handoffs. A build agent should summarize what it changed, what it did not touch, which gates passed, which gates failed, and which open questions remain. It must not revert another agent's edits. Source: [repository rules](../../AGENTS.md).

Use fail-closed review. Reviewers should block work on future data, missing availability metadata, live-trading paths, secret exposure, negative liquidity or rates, uncapped execution, missing baselines, unsupported profitability claims, and missing reproducibility metadata. Sources: [risk validation](../11-risk-controls-and-compliance/VALIDATION.md), [testing validation](../13-testing-validation-and-benchmarks/VALIDATION.md), [reproducibility validation](../14-reproducibility-and-experiment-tracking/VALIDATION.md).

## Open Questions

The exact contents of future `plans/INTERFACES.md` and `plans/VALIDATION_GATES.md` remain open because this task was scoped to `plans/ORCHESTRATION.md`, `plans/AGENT_HANDOFF_TEMPLATE.md`, and `plans/TASK_TEMPLATE.md`.

The default `epsilon` estimator remains unsettled. Candidate methods are volatility decay, spread recovery, depth recovery, and filtered latent decay. Sources: [turbulence decision](../02-turbulence-closure-and-fragility/DECISION.md), [calibration decision](../05-stochastic-processes-and-calibration/DECISION.md).

The minimum sample counts and thresholds for model promotion, calibration quality, and stress labels remain open. Sources: [feature validation](../08-feature-engineering-and-labels/VALIDATION.md), [prediction validation](../09-prediction-models-and-baselines/VALIDATION.md), [testing decision](../13-testing-validation-and-benchmarks/DECISION.md).

The exact paper broker, if any, remains open. Live trading remains blocked in Phase 0 and Phase 1 regardless of this choice. Sources: [data decision](../06-data-requirements-and-vendors/DECISION.md), [backtesting decision](../10-backtesting-paper-trading-and-execution/DECISION.md), [risk decision](../11-risk-controls-and-compliance/DECISION.md).
