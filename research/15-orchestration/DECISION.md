# Orchestration Decision

Status: Phase 0 decision. This does not authorize production code, live trading code, live broker endpoints, live credentials, paid-data commits, or profitability claims.

## Decision

Use a component-owned orchestration model for future Phase 1 build agents. Each agent receives a narrow charter, fixed input documents, explicit file ownership, forbidden files, validation commands, handoff notes, and review gates. This matches the modular architecture required by the repository and the selected Python stack. Sources: [repository rules](../../AGENTS.md), [architecture decision](../12-python-architecture-and-stack/DECISION.md), [architecture interface](../12-python-architecture-and-stack/INTERFACE.md).

## Accepted Roster Shape

The future build roster should include agents for contracts and config, data adapters, event store, features and labels, turbulence estimates, price-interface estimates, calibration and numerical fixtures, prediction baselines, backtesting, risk controls, validation and benchmarks, reproducibility and tracking, reports, and orchestration review.

Recommendation: assign each future coding task to exactly one primary owner and one reviewer. Shared interfaces may be edited only when the task names the interface and includes downstream handoff notes. Sources: [testing decision](../13-testing-validation-and-benchmarks/DECISION.md), [reproducibility decision](../14-reproducibility-and-experiment-tracking/DECISION.md).

## Phase Boundary

Phase 0 is documentation and planning only. Phase 1 is offline, CPU-only research implementation on Mac M3. Phase 1 may include simulation, backtesting, and dry-run paper-ledger design, but live trading remains blocked. No Phase 1 task may add live broker endpoints, live credentials, live enable flags, or production order routing. Sources: [TRIDENT model](../../docs/TRIDENT_LOB_MODEL.md), [risk decision](../11-risk-controls-and-compliance/DECISION.md), [backtesting decision](../10-backtesting-paper-trading-and-execution/DECISION.md).

## Required Build Order

1. Contracts, config schemas, manifests, fixture strategy, and validation gates.
2. Provider-neutral data records and local event store.
3. Point-in-time feature and label builder.
4. Turbulence and price-interface proxy estimators.
5. Baseline prediction models and model diagnostics.
6. Event-driven research backtester with dry-run ledger and risk checks.
7. Reproducible reports, MLflow tracking, audit logs, and benchmarks.

Recommendation: do not start model fitting before feature leakage gates and split manifests exist. Sources: [feature validation](../08-feature-engineering-and-labels/VALIDATION.md), [prediction validation](../09-prediction-models-and-baselines/VALIDATION.md).

## Required Review Gates

Block a task if it introduces future data, missing availability metadata, random row splits, negative liquidity or rates, uncapped execution, missing simple baselines, unsupported profitability claims, secrets, paid data payloads, live endpoints, live credentials, or live-trading flags. Sources: [testing validation](../13-testing-validation-and-benchmarks/VALIDATION.md), [risk validation](../11-risk-controls-and-compliance/VALIDATION.md), [data validation](../06-data-requirements-and-vendors/VALIDATION.md).

## Non-Decisions

This decision does not choose a data vendor, buy paid data, select a broker, approve paper API use, approve margin, approve short selling, approve a full PDE solver, or promote any model.

## Open Questions

The orchestration plan still needs future companion files for consolidated interfaces and validation gates if the project wants to satisfy the current `AGENTS.md` read list with repository-level documents. Sources: [repository rules](../../AGENTS.md).

The exact package paths will be finalized when the first Phase 1 scaffolding task is approved. The planning recommendation is to follow the `src/trident_lob` layout in the architecture decision. Source: [architecture decision](../12-python-architecture-and-stack/DECISION.md).
