# TRIDENT-LOB

TRIDENT-LOB is a Python research codebase for Turbulent Reaction-diffusion Interface Dynamics for Electronic Limit Order Books.

The project is in Phase 0: research, planning, interfaces, validation gates, data planning, and orchestration. It must not place live trades in Phase 0 or Phase 1.

## Current Structure

- `docs/`: model specification, glossary, and data ethics notes.
- `research/`: Phase 0 specialist research deliverables.
- `plans/`: synthesized master plan, orchestration, interfaces, data plan, risk register, and validation gates.
- `TASKS/`: future task queue folders.
- `experiments/`: future reproducible experiment notes and reports.

## Phase Path

1. Phase 0: research and planning only.
2. Phase 1: offline CPU-only Mac M3 research predictor with no live trading.
3. Phase 2: L2 or L3 order-book replay and source/sink validation.
4. Phase 3: paper trading only after offline gates pass and the user explicitly approves.
5. Phase 4: live-readiness review only after all gates pass and the user explicitly requests it.

## Required Reading For Future Agents

Before editing, read:

- `AGENTS.md`
- `docs/TRIDENT_LOB_MODEL.md`
- `plans/ORCHESTRATION.md`
- `plans/INTERFACES.md`
- `plans/VALIDATION_GATES.md`
- Relevant `research/*/DECISION.md`, `INTERFACE.md`, and `VALIDATION.md`

## Safety

Do not commit API keys, broker credentials, paid data, private account information, or live-trading code. Do not use future data in features or labels. Do not claim profitability without out-of-sample, transaction-cost-adjusted evidence.
