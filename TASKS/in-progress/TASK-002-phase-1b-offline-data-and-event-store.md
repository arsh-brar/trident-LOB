# TASK-002: Phase 1B Offline Data And Event Store

## Task Header

```text
task_id: TASK-002
phase: Phase 1B
owner_agent: A1 Data Adapters and A2 Event Store
review_agent: A10 Validation And Benchmarks
priority: high
status: in_progress
```

## Objective

Build the first provider-neutral offline data and event-store skeleton for
TRIDENT-LOB. The task should add canonical record schemas, dataset manifests,
safe synthetic fixtures, local immutable event-store interfaces, and validation
guards without downloading market data, adding credentials, adding broker access,
or implementing trading logic.

## Required Reading

Always read:

- `AGENTS.md`
- `docs/TRIDENT_LOB_MODEL.md`
- `plans/INTERFACES.md`
- `plans/ORCHESTRATION.md`
- `plans/VALIDATION_GATES.md`
- `TASKS/done/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md`

Task-specific research:

- `research/06-data-requirements-and-vendors/DECISION.md`
- `research/06-data-requirements-and-vendors/INTERFACE.md`
- `research/06-data-requirements-and-vendors/VALIDATION.md`
- `research/07-news-and-exogenous-inputs/DECISION.md`
- `research/07-news-and-exogenous-inputs/INTERFACE.md`
- `research/07-news-and-exogenous-inputs/VALIDATION.md`
- `research/12-python-architecture-and-stack/INTERFACE.md`
- `research/13-testing-validation-and-benchmarks/VALIDATION.md`
- `research/14-reproducibility-and-experiment-tracking/INTERFACE.md`

## Allowed Paths

The agent may modify only:

- `src/trident_lob/data/`
- `src/trident_lob/events/`
- `src/trident_lob/contracts/`
- `src/trident_lob/config/`
- `src/trident_lob/validation/`
- `tests/`
- `configs/`
- `data/README.md`
- `data/manifests/README.md`
- `data/manifests/`
- `TASKS/in-progress/TASK-002-phase-1b-offline-data-and-event-store.md`

## Forbidden Paths

The agent must not modify:

- `research/`
- `plans/`
- `docs/TRIDENT_LOB_MODEL.md`
- `AGENTS.md`
- `pyproject.toml` unless a missing already-approved dependency blocks the task
- `uv.lock` unless `pyproject.toml` is explicitly and narrowly changed
- any paid data payload
- any raw vendor archive
- any secret file
- any live broker or live trading integration
- `src/trident_lob/features/`
- `src/trident_lob/models/`
- `src/trident_lob/backtest/`
- `src/trident_lob/paper/`
- `src/trident_lob/risk/`

## Inputs

- Phase 1A package scaffold and contracts.
- No market data payloads.
- No API keys.
- No broker credentials.
- Synthetic records created inside tests or tiny committed fixtures only.

## Outputs

Required outputs:

- Canonical record schemas for at least bars, quotes, trades, depth, news,
  calendar, and corporate actions.
- Dataset or event-batch manifest schemas with provider, source, license class,
  delay class, timestamp range, row count, content hash or payload hash reference,
  `secret_free`, `paid_payload_free`, and `may_commit_payload` fields.
- Offline-only synthetic fixture adapter or fixture builder that produces tiny
  safe records with event and availability timestamps.
- Local event-store skeleton with immutable registration and query interfaces.
  A minimal Parquet round trip is preferred if it can use existing dependencies.
- Validation guards for timestamp ordering, `available_at <= decision time`
  checks where applicable, negative prices or sizes, crossed quotes, unknown
  license class, paid payload safety, and secret safety.
- Tests proving imports, schema construction, invalid fixture rejection,
  manifest safety, event-store registration or round trip, and no live broker
  or live-trading surface.
- Task closeout notes appended to this task file when ready for review.

## Validation Commands

```text
command: python -c "import platform; print(platform.machine())"
purpose: verify native Apple Silicon architecture when run locally
required: yes
```

```text
command: python -c "import sys; print(sys.version)"
purpose: verify Python version visibility
required: yes
```

```text
command: uv sync --locked
purpose: install from lock file without changing dependencies
required: no
```

```text
command: uv run pytest
purpose: run test suite
required: yes if uv environment is available
```

```text
command: uv run ruff check .
purpose: lint repository
required: yes if uv environment is available
```

```text
command: uv run ruff format --check .
purpose: verify formatting
required: yes if uv environment is available
```

```text
command: uv run mypy src
purpose: run static type checks
required: yes if uv environment is available
```

If `uv` is not installed or network access is needed to create or update the
lock file, stop and request approval before installing or downloading
dependencies.

## Required Handoff

At closeout, fill the fields from `plans/AGENT_HANDOFF_TEMPLATE.md` in the final
response or a linked handoff file. Include:

- files changed
- validation run
- validation not run
- open questions
- interface changes
- downstream agents affected
- live-trading safety
- secret safety
- paid-data safety
- future-data safety

## Review Gates

Block completion if any of these apply:

- Future data enters features, preprocessing, labels, validation, or reports.
- A record lacks event time or availability time where required.
- Random row splitting or model training enters this data task.
- Live broker endpoint, live credential path, live order router, or
  live-trading flag appears.
- API key, broker credential, paid data payload, raw vendor archive, or private
  account information appears.
- L2 or L3 structural claims are made from bars, L1, or synthetic fixtures.
- Negative prices, negative sizes, crossed quotes, impossible timestamp ordering,
  unknown license class, or paid-payload commit flags are accepted silently.
- Production model logic, backtesting logic, paper broker implementation, or
  trading logic enters the scaffold.
- Profitability is claimed without out-of-sample, transaction-cost-adjusted
  evidence.

## Stop Conditions

Stop and escalate if the task needs:

- network access for dependency download or data download
- paid data
- credentials
- paper broker access
- files outside allowed paths
- a shared-interface change not named in this task
- a license decision
- live-like connectivity
- storing full copyrighted article bodies or paid vendor payloads

## Sources

- `AGENTS.md`
- `docs/TRIDENT_LOB_MODEL.md`
- `plans/ORCHESTRATION.md`
- `plans/INTERFACES.md`
- `plans/VALIDATION_GATES.md`
- `research/06-data-requirements-and-vendors/DECISION.md`
- `research/06-data-requirements-and-vendors/INTERFACE.md`
- `research/06-data-requirements-and-vendors/VALIDATION.md`
- `research/07-news-and-exogenous-inputs/DECISION.md`
- `research/07-news-and-exogenous-inputs/INTERFACE.md`
- `research/07-news-and-exogenous-inputs/VALIDATION.md`
- `research/12-python-architecture-and-stack/INTERFACE.md`
- `research/13-testing-validation-and-benchmarks/VALIDATION.md`
- `research/14-reproducibility-and-experiment-tracking/INTERFACE.md`
- Databento standards: https://databento.com/docs/standards-and-conventions
- Apache Parquet overview: https://parquet.apache.org/docs/overview/
- Polars Parquet docs: https://docs.pola.rs/user-guide/io/parquet/
- DuckDB Python API: https://duckdb.org/docs/stable/clients/python/overview
- Pydantic strict mode: https://docs.pydantic.dev/latest/concepts/strict_mode/
