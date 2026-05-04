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
- TASKS/in-progress/TASK-002-phase-1b-offline-data-and-event-store.md

Current project state:

- Phase 0 research and planning are complete.
- TASK-001 Phase 1A scaffold is done and merged into main.
- The repository has a CPU-only Python 3.12 package scaffold, uv.lock, Ruff,
  mypy, pytest, pre-commit hooks, config skeletons, protocol boundaries, and
  safety guard tests.
- The next task is TASK-002 Phase 1B offline data and event store.
- Live trading is blocked in Phase 0 and Phase 1.
- Do not add live broker endpoints, live credential paths, live order routers,
  live-trading flags, paid data payloads, API keys, broker secrets, private
  account information, future-data features, production model logic, or
  profitability claims.

Primary task:

Work on TASKS/in-progress/TASK-002-phase-1b-offline-data-and-event-store.md.

The intended outcome is a provider-neutral offline data and event-store
skeleton with:

- canonical market, news, calendar, and corporate-action record schemas
- dataset and event-batch manifest schemas with license and commit-safety flags
- offline-only synthetic fixture adapter for tiny safe records
- immutable local event-store skeleton using Parquet-oriented interfaces
- validation guards for timestamp ordering, availability timestamps, negative
  prices or sizes, crossed quotes, secret safety, and paid-payload safety
- tests proving schema construction, invalid fixture rejection, manifest safety,
  import health, and no live-trading or broker-access surface

Required research context:

- research/06-data-requirements-and-vendors/DECISION.md
- research/06-data-requirements-and-vendors/INTERFACE.md
- research/06-data-requirements-and-vendors/VALIDATION.md
- research/07-news-and-exogenous-inputs/DECISION.md
- research/07-news-and-exogenous-inputs/INTERFACE.md
- research/07-news-and-exogenous-inputs/VALIDATION.md
- research/12-python-architecture-and-stack/INTERFACE.md
- research/13-testing-validation-and-benchmarks/VALIDATION.md
- research/14-reproducibility-and-experiment-tracking/INTERFACE.md

Validation expectation:

Run the validation commands named in the task when possible. If dependency
installation or network access is needed, request approval before proceeding.
If any validation cannot run, document why and what remains risky.

Closeout:

Update the task status when appropriate and provide a handoff using
plans/AGENT_HANDOFF_TEMPLATE.md fields.
```

## Sources

- Project rules: [AGENTS.md](AGENTS.md)
- Model scope and no-live-trading note: [docs/TRIDENT_LOB_MODEL.md](docs/TRIDENT_LOB_MODEL.md)
- Orchestration and Phase 1B definition: [plans/ORCHESTRATION.md](plans/ORCHESTRATION.md)
- Interface contracts: [plans/INTERFACES.md](plans/INTERFACES.md)
- Validation gates: [plans/VALIDATION_GATES.md](plans/VALIDATION_GATES.md)
- Data decision: [research/06-data-requirements-and-vendors/DECISION.md](research/06-data-requirements-and-vendors/DECISION.md)
- Data validation: [research/06-data-requirements-and-vendors/VALIDATION.md](research/06-data-requirements-and-vendors/VALIDATION.md)
- News decision: [research/07-news-and-exogenous-inputs/DECISION.md](research/07-news-and-exogenous-inputs/DECISION.md)
- Architecture interface: [research/12-python-architecture-and-stack/INTERFACE.md](research/12-python-architecture-and-stack/INTERFACE.md)
