# TASK-001: Phase 1A Scaffolding And Validation Skeleton

## Task Header

```text
task_id: TASK-001
phase: Phase 1A
owner_agent: A0 Contracts And Config
review_agent: A10 Validation And Benchmarks
priority: high
status: review
```

## Objective

Create the initial CPU-only Python project scaffold and validation skeleton for TRIDENT-LOB. The task should replace the placeholder packaging file with a real `pyproject.toml`, create the first `src/trident_lob` package structure, add shared protocols and config skeletons, and wire up local quality gates without adding trading logic.

## Required Reading

Always read:

- `docs/TRIDENT_LOB_MODEL.md`
- `AGENTS.md`
- `plans/ORCHESTRATION.md`
- `plans/INTERFACES.md`
- `plans/VALIDATION_GATES.md`

Task-specific research:

- `research/12-python-architecture-and-stack/DECISION.md`
- `research/12-python-architecture-and-stack/INTERFACE.md`
- `research/12-python-architecture-and-stack/VALIDATION.md`
- `research/13-testing-validation-and-benchmarks/DECISION.md`
- `research/13-testing-validation-and-benchmarks/INTERFACE.md`
- `research/13-testing-validation-and-benchmarks/VALIDATION.md`
- `research/14-reproducibility-and-experiment-tracking/DECISION.md`
- `research/14-reproducibility-and-experiment-tracking/INTERFACE.md`
- `research/14-reproducibility-and-experiment-tracking/VALIDATION.md`

## Allowed Paths

The agent may modify only:

- `pyproject.toml.placeholder`
- `pyproject.toml`
- `uv.lock`
- `.pre-commit-config.yaml`
- `src/trident_lob/`
- `tests/`
- `configs/`
- `benchmarks/`
- `data/README.md`
- `data/manifests/README.md`
- `experiments/README.md`
- `experiments/run_manifests/README.md`
- `reports/README.md`
- `reports/generated/README.md`
- `models/README.md`
- `models/registry/README.md`
- `TASKS/in-progress/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md`

## Forbidden Paths

The agent must not modify:

- `research/`
- `plans/` except by explicit user request
- `docs/TRIDENT_LOB_MODEL.md`
- `AGENTS.md`
- `.gitignore` unless a generated local artifact requires a narrow ignore update
- any paid data payload
- any secret file
- any live broker or live trading integration

## Inputs

- Phase 0 plans and research documents.
- Existing `.gitignore`.
- Existing `pyproject.toml.placeholder`.
- No market data payloads.
- No API keys.
- No broker credentials.

## Outputs

Required outputs:

- `pyproject.toml` with project metadata, Python version target, dependencies, optional dependency groups, pytest, Ruff, and mypy configuration.
- Remove or clearly retire `pyproject.toml.placeholder` only if the real `pyproject.toml` replaces it.
- `src/trident_lob/__init__.py`.
- Initial package folders from the architecture decision, at minimum `contracts`, `config`, `validation`, and `cli`.
- Protocol or type skeletons for swappable components without implementation-heavy business logic.
- Pydantic or dataclass config skeletons for non-secret settings.
- Minimal CLI placeholder that cannot place trades.
- Minimal tests for import, package metadata if practical, no live-trading guard strings, and config construction.
- Pre-commit configuration for Ruff, mypy, and pytest-compatible local checks when practical.
- README placeholders for new top-level artifact folders if created.

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

If `uv` is not installed or network access is needed to create the lock file, stop and request approval before installing or downloading dependencies.

## Required Handoff

At closeout, fill the fields from `plans/AGENT_HANDOFF_TEMPLATE.md` in the final response or a linked handoff file. Include:

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
- Live broker endpoint, live credential path, live order router, or live-trading flag appears.
- API key, broker credential, paid data payload, or private account information appears.
- Negative accepted liquidity, nonpositive accepted `epsilon`, or uncapped execution appears.
- Model work lacks no-skill, ordinary microstructure, and technical baselines.
- Profitability is claimed without out-of-sample, transaction-cost-adjusted evidence.
- Core dependencies require GPU or non-Mac-M3-only execution.
- Tests or package skeleton imply live trading is available.

## Stop Conditions

Stop and escalate if the task needs:

- network access for dependency download
- paid data
- credentials
- paper broker access
- files outside allowed paths
- a shared-interface change not named in this task
- a license decision
- live-like connectivity

## Sources

- `AGENTS.md`
- `docs/TRIDENT_LOB_MODEL.md`
- `plans/ORCHESTRATION.md`
- `plans/INTERFACES.md`
- `plans/VALIDATION_GATES.md`
- `research/12-python-architecture-and-stack/DECISION.md`
- `research/12-python-architecture-and-stack/INTERFACE.md`
- `research/12-python-architecture-and-stack/VALIDATION.md`
- `research/13-testing-validation-and-benchmarks/DECISION.md`
- `research/14-reproducibility-and-experiment-tracking/DECISION.md`
- Python packaging guide: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- uv project workflow: https://docs.astral.sh/uv/concepts/projects/sync/
- pytest docs: https://docs.pytest.org/en/stable/getting-started.html
- Ruff docs: https://docs.astral.sh/ruff/
- mypy docs: https://mypy.readthedocs.io/en/latest/getting_started.html
- pre-commit docs: https://pre-commit.com/

## Implementation Notes

Status updated to `review` after adding the initial Phase 1A scaffold. Validation
ran with `uv` from a temporary tool environment, `UV_CACHE_DIR` under
`/private/tmp`, and the locked project Python 3.12 environment.
