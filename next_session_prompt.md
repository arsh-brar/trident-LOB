# Next Session Prompt

Use this prompt to continue TRIDENT-LOB in the next Codex session.

```text
You are Codex working in /Users/arshbrar/Development/GitHub/trident_LOB.

Start by reading these required files before editing:

- AGENTS.md
- docs/TRIDENT_LOB_MODEL.md
- plans/INTERFACES.md
- plans/ORCHESTRATION.md
- plans/VALIDATION_GATES.md
- TASKS/done/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md
- TASKS/done/TASK-002-phase-1b-offline-data-and-event-store.md
- TASKS/in-progress/TASK-003-phase-1c-features-labels-and-splits.md

Current project state:

- Phase 0 research and planning are complete.
- TASK-001 Phase 1A scaffold is done and merged into main.
- TASK-002 Phase 1B offline data and event store is done and merged into main.
- The repository has a CPU-only Python 3.12 package scaffold, uv.lock, Ruff,
  mypy, pytest, pre-commit hooks, config skeletons, protocol boundaries, and
  safety guard tests.
- The repository now has provider-neutral offline data schemas, synthetic
  fixtures, event-batch manifests, local Parquet event-store registration and
  query methods, and data validation guards.
- The next task is TASK-003 Phase 1C features, labels, and splits.
- Live trading is blocked in Phase 0 and Phase 1.
- Do not add live broker endpoints, live credential paths, live order routers,
  live-trading flags, paid data payloads, API keys, broker secrets, private
  account information, future-data features, production model logic, or
  profitability claims.

Primary task:

Work on TASKS/in-progress/TASK-003-phase-1c-features-labels-and-splits.md.

The intended outcome is a point-in-time feature, label, split, and
leakage-report skeleton with:

- strict feature-row schemas with `feature_available_at_max_ns <= t_pred_ns`
  validation
- strict label-row schemas kept separate from features
- chronological split manifests with embargo metadata
- tiny offline feature and label builders using TASK-002 synthetic fixtures
- bars-only degraded mode flags for unavailable quote-dependent features
- leakage reports that fail closed on future data
- tests proving feature availability, label separation, split embargo,
  completed-bar eligibility, bars-only degraded mode, and no live-trading or
  broker-access surface

Required research context:

- research/08-feature-engineering-and-labels/DECISION.md
- research/08-feature-engineering-and-labels/INTERFACE.md
- research/08-feature-engineering-and-labels/VALIDATION.md
- research/07-news-and-exogenous-inputs/DECISION.md
- research/07-news-and-exogenous-inputs/INTERFACE.md
- research/07-news-and-exogenous-inputs/VALIDATION.md
- research/09-prediction-models-and-baselines/INTERFACE.md
- research/09-prediction-models-and-baselines/VALIDATION.md
- research/12-python-architecture-and-stack/INTERFACE.md
- research/13-testing-validation-and-benchmarks/VALIDATION.md
- research/14-reproducibility-and-experiment-tracking/INTERFACE.md

Validation expectation:

Run the validation commands named in the task when possible. If dependency
installation or network access is needed, request approval before proceeding.
If any validation cannot run, document why and what remains risky.
If bare `python` or `uv` is unavailable, use existing `.venv` equivalents and
document the exact commands that could not run. The last validated project
interpreter was `.venv/bin/python`, Python `3.12.13`.

Closeout:

Update the task status when appropriate and provide a handoff using
plans/AGENT_HANDOFF_TEMPLATE.md fields.
```

## Sources

- Project rules: [AGENTS.md](AGENTS.md)
- Model scope and no-live-trading note: [docs/TRIDENT_LOB_MODEL.md](docs/TRIDENT_LOB_MODEL.md)
- Orchestration and Phase 1C definition: [plans/ORCHESTRATION.md](plans/ORCHESTRATION.md)
- Interface contracts: [plans/INTERFACES.md](plans/INTERFACES.md)
- Validation gates: [plans/VALIDATION_GATES.md](plans/VALIDATION_GATES.md)
- Feature decision: [research/08-feature-engineering-and-labels/DECISION.md](research/08-feature-engineering-and-labels/DECISION.md)
- Feature validation: [research/08-feature-engineering-and-labels/VALIDATION.md](research/08-feature-engineering-and-labels/VALIDATION.md)
- News decision: [research/07-news-and-exogenous-inputs/DECISION.md](research/07-news-and-exogenous-inputs/DECISION.md)
- Architecture interface: [research/12-python-architecture-and-stack/INTERFACE.md](research/12-python-architecture-and-stack/INTERFACE.md)
