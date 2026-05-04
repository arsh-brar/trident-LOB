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
- TASKS/in-progress/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md

Current project state:

- Phase 0 research and planning are complete.
- The repository has been initialized and pushed to https://github.com/arsh-brar/trident-LOB.git.
- The next task is Phase 1A scaffolding and validation skeleton.
- Live trading is blocked in Phase 0 and Phase 1.
- Do not add live broker endpoints, live credential paths, live order routers, live-trading flags, paid data payloads, API keys, broker secrets, or private account information.

Primary task:

Work on TASKS/in-progress/TASK-001-phase-1a-scaffolding-and-validation-skeleton.md.

The intended outcome is a CPU-only Mac M3 compatible Python project scaffold with:

- a real pyproject.toml replacing pyproject.toml.placeholder
- uv-compatible dependency groups
- src/trident_lob package skeleton
- initial protocol and config modules
- pytest, Ruff, mypy, and pre-commit configuration
- minimal tests proving imports and safety guards
- no production trading logic
- no paper broker adapter implementation beyond a safe placeholder if the task allows it

Required research context:

- research/12-python-architecture-and-stack/DECISION.md
- research/12-python-architecture-and-stack/INTERFACE.md
- research/12-python-architecture-and-stack/VALIDATION.md
- research/13-testing-validation-and-benchmarks/DECISION.md
- research/13-testing-validation-and-benchmarks/VALIDATION.md
- research/14-reproducibility-and-experiment-tracking/DECISION.md

Validation expectation:

Run the validation commands named in the task when possible. If dependency installation or network access is needed, request approval before proceeding. If any validation cannot run, document why and what remains risky.

Closeout:

Update the task status when appropriate and provide a handoff using plans/AGENT_HANDOFF_TEMPLATE.md fields.
```

## Sources

- Project rules: [AGENTS.md](AGENTS.md)
- Model scope and no-live-trading note: [docs/TRIDENT_LOB_MODEL.md](docs/TRIDENT_LOB_MODEL.md)
- Orchestration and Phase 1A definition: [plans/ORCHESTRATION.md](plans/ORCHESTRATION.md)
- Interface contracts: [plans/INTERFACES.md](plans/INTERFACES.md)
- Validation gates: [plans/VALIDATION_GATES.md](plans/VALIDATION_GATES.md)
- Stack decision: [research/12-python-architecture-and-stack/DECISION.md](research/12-python-architecture-and-stack/DECISION.md)
- Testing decision: [research/13-testing-validation-and-benchmarks/DECISION.md](research/13-testing-validation-and-benchmarks/DECISION.md)
