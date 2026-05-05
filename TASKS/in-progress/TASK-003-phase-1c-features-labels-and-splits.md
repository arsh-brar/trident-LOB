# TASK-003: Phase 1C Features, Labels, And Splits

## Task Header

```text
task_id: TASK-003
phase: Phase 1C
owner_agent: A3 Features And Labels
review_agent: A10 Validation And Benchmarks
priority: high
status: review
```

## Objective

Build the first point-in-time feature, label, split, and leakage-report skeleton
for TRIDENT-LOB. The task should use the provider-neutral offline records and
event-store outputs from TASK-002, create strict feature and label boundary
schemas, implement tiny synthetic fixture builders, and add fail-closed leakage
validation without adding model training, backtesting, paper-broker code, or
trading logic.

## Required Reading

Always read:

- `AGENTS.md`
- `docs/TRIDENT_LOB_MODEL.md`
- `plans/INTERFACES.md`
- `plans/ORCHESTRATION.md`
- `plans/VALIDATION_GATES.md`
- `TASKS/done/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md`
- `TASKS/done/TASK-002-phase-1b-offline-data-and-event-store.md`

Task-specific research:

- `research/08-feature-engineering-and-labels/DECISION.md`
- `research/08-feature-engineering-and-labels/INTERFACE.md`
- `research/08-feature-engineering-and-labels/VALIDATION.md`
- `research/07-news-and-exogenous-inputs/DECISION.md`
- `research/07-news-and-exogenous-inputs/INTERFACE.md`
- `research/07-news-and-exogenous-inputs/VALIDATION.md`
- `research/09-prediction-models-and-baselines/INTERFACE.md`
- `research/09-prediction-models-and-baselines/VALIDATION.md`
- `research/12-python-architecture-and-stack/INTERFACE.md`
- `research/13-testing-validation-and-benchmarks/VALIDATION.md`
- `research/14-reproducibility-and-experiment-tracking/INTERFACE.md`

## Allowed Paths

The agent may modify only:

- `src/trident_lob/features/`
- `src/trident_lob/labels/`
- `src/trident_lob/contracts/`
- `src/trident_lob/config/`
- `src/trident_lob/validation/`
- `tests/`
- `configs/`
- `benchmarks/`
- `reports/README.md`
- `reports/generated/README.md`
- `TASKS/in-progress/TASK-003-phase-1c-features-labels-and-splits.md`

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
- `src/trident_lob/data/` except for reading existing TASK-002 schemas and
  fixtures
- `src/trident_lob/events/` except for reading existing TASK-002 store
  interfaces
- `src/trident_lob/models/`
- `src/trident_lob/backtest/`
- `src/trident_lob/paper/`
- `src/trident_lob/risk/`

## Inputs

- Phase 1A package scaffold, contracts, config, and validation skeleton.
- Phase 1B provider-neutral data schemas, synthetic fixtures, event-batch
  manifests, and local event-store skeleton.
- No market data downloads.
- No API keys.
- No broker credentials.
- Synthetic records created inside tests or tiny committed fixtures only.

## Outputs

Required outputs:

- Strict feature-row schemas with `symbol`, `t_pred_ns`,
  `feature_available_at_max_ns`, `max_feature_lookback_ns`, `data_mode`,
  quality flags, and feature-family metadata.
- Strict label-row schemas with `symbol`, `t_pred_ns`, `horizon_seconds`,
  `label_available_at_min_ns`, return labels, cost-aware direction labels,
  stress labels, cost ticks, buffer ticks, and null reason codes.
- Split-manifest schemas with chronological train, validation, and test
  windows, embargo length, maximum label horizon, maximum feature lookback, and
  optional held-out symbols.
- A tiny offline feature builder that can create ordinary microstructure and
  technical baseline rows from TASK-002 synthetic bars, quotes, and trades.
- A tiny offline label builder for 1 minute and 5 minute horizons that keeps
  labels separate from features and records missing or invalid future outcomes.
- Leakage-report helpers that fail when
  `feature_available_at_max_ns > t_pred_ns`, when news or calendar actuals are
  used before availability, or when split embargo is too short.
- Bars-only degraded mode flags for quote-dependent features that are null when
  quotes are not present.
- Tests proving schema construction, invalid leakage rejection, completed-bar
  eligibility, label separation from features, chronological split and embargo
  behavior, bars-only degraded mode, no random row split helper, and no live
  broker or live-trading surface.
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

If `python` or `uv` is not on the shell path, use the existing `.venv`
equivalents and document the exact commands that could not run. The project
interpreter used in TASK-002 was `.venv/bin/python`, Python `3.12.13`, matching
the project `>=3.12,<3.13` requirement.

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

- Any accepted feature row has `feature_available_at_max_ns > t_pred_ns`.
- Completed-bar features use bars whose close time or provider availability
  time is after `t_pred_ns`.
- Quote, trade, news, SEC filing, macro, calendar actual, or corporate-action
  revision data enters a feature before its availability timestamp.
- Labels are stored in the same structure as feature columns in a way that a
  feature builder can consume future outcomes.
- Split manifests use random row splitting or omit required chronological
  train, validation, test, and embargo metadata.
- Embargo is shorter than `max_label_horizon_ns + max_feature_lookback_ns`.
- Bars-only data emits quote-only or L2/L3 structural features as observed
  values instead of null or degraded-mode flags.
- Negative accepted `k`, nonpositive accepted `epsilon`, negative `nu_t`,
  negative depth, or negative cost values are accepted silently.
- Live broker endpoint, live credential path, live order router, or
  live-trading flag appears.
- API key, broker credential, paid data payload, raw vendor archive, or private
  account information appears.
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
- implementing model training, backtesting, or trading behavior

## Sources

- `AGENTS.md`
- `docs/TRIDENT_LOB_MODEL.md`
- `plans/ORCHESTRATION.md`
- `plans/INTERFACES.md`
- `plans/VALIDATION_GATES.md`
- `TASKS/done/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md`
- `TASKS/done/TASK-002-phase-1b-offline-data-and-event-store.md`
- `research/08-feature-engineering-and-labels/DECISION.md`
- `research/08-feature-engineering-and-labels/INTERFACE.md`
- `research/08-feature-engineering-and-labels/VALIDATION.md`
- `research/07-news-and-exogenous-inputs/DECISION.md`
- `research/07-news-and-exogenous-inputs/INTERFACE.md`
- `research/07-news-and-exogenous-inputs/VALIDATION.md`
- `research/09-prediction-models-and-baselines/INTERFACE.md`
- `research/09-prediction-models-and-baselines/VALIDATION.md`
- `research/12-python-architecture-and-stack/INTERFACE.md`
- `research/13-testing-validation-and-benchmarks/VALIDATION.md`
- `research/14-reproducibility-and-experiment-tracking/INTERFACE.md`
- scikit-learn time-series split docs:
  https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- scikit-learn common pitfalls:
  https://scikit-learn.org/stable/common_pitfalls.html
- Apache Parquet overview: https://parquet.apache.org/docs/overview/
- Polars lazy API: https://docs.pola.rs/user-guide/concepts/lazy-api/
- DuckDB Python API: https://duckdb.org/docs/stable/clients/python/overview

## Implementation Notes

Status updated to `review` on 2026-05-05 after adding the Phase 1C feature,
label, split, and leakage-report skeleton.

Added:

- Strict `FeatureRow`, `FeatureQualityFlags`, leakage finding, and leakage
  report schemas with fail-closed availability checks.
- Tiny offline feature builder for completed-bar technical features and
  L1 top-of-book ordinary microstructure features from TASK-002 synthetic
  records.
- Bars-only degraded mode that keeps quote-dependent values null and records
  explicit unavailable-feature reasons.
- Strict `LabelRow` schemas kept separate from feature rows, with 60 second
  and 300 second label builder support, cost-aware direction labels, stress
  label placeholders, costs, buffers, and null reason codes.
- Chronological split manifest schemas and a fixed chronological split builder
  with embargo metadata.
- Leakage report helpers that fail for future feature availability, future news
  availability or publication, calendar actuals unavailable at prediction time,
  and insufficient split embargo.
- Tests for feature availability, completed-bar eligibility, label separation,
  chronological split embargo, bars-only degradation, future-news rejection,
  missing future labels, no random row split helper, and the existing safety
  surface scan.

Validation run:

- `.venv/bin/python -c "import platform; print(platform.machine())"`: `arm64`.
- `.venv/bin/python -c "import sys; print(sys.version)"`: Python `3.12.13`.
- `.venv/bin/python -m pytest`: passed, 31 tests.
- `.venv/bin/ruff check .`: passed.
- `.venv/bin/ruff format --check .`: passed.
- `.venv/bin/mypy src`: passed.
- `rg -n "alpaca|binance|coinbase|interactive brokers|kraken|api_key|secret_key|order_router|order_url|live_trading|broker" src configs benchmarks tests`:
  found only existing safety-blocking guard literals and the split-string safety
  test fixture, not endpoints, credential paths, order routers, or enable flags.

Validation not run:

- Exact bare `python -c ...` commands were not available because `python` is not
  on the shell path.
- `uv sync --locked` and exact `uv run ...` commands were not available because
  `uv` is not on the shell path.

Safety review:

- No live broker endpoints, live credential paths, live order routers,
  live-trading flags, paid data payloads, raw vendor archives, secrets, private
  account information, production model logic, backtesting logic, paper broker
  implementation, trading logic, or profitability claims were added.
- Feature rows fail closed when source availability exceeds prediction time.
- Labels remain separate from features and intentionally record future outcome
  availability only in label rows.
