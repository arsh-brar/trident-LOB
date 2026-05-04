# AGENTS.md for TRIDENT-LOB

## Project identity

This repository builds TRIDENT-LOB, a Python research codebase for a turbulent reaction-diffusion limit order book model.

## Hard rules

- Do not place live trades.
- Do not write live-trading code unless a later explicit task requests it and validation gates have passed.
- Do not commit API keys, broker credentials, paid data, or private account information.
- Do not use future data in any feature.
- Do not claim profitability without out-of-sample, transaction-cost-adjusted evidence.
- Prefer simple baselines before complex models.
- Every recommendation must cite sources.
- No em dashes in generated documents.

## Development environment

Primary development is on a MacBook with Apple Silicon M3. Phase 1 must run CPU-only on this machine.

## Phase 1 coding preference

Use Python first. Keep the architecture modular. Make every major component swappable:

- data adapter
- event store
- feature builder
- turbulence estimator
- price-interface estimator
- prediction model
- backtester
- paper-trading adapter
- risk manager
- report generator

## Required behavior

Before editing files, read:

```text
docs/TRIDENT_LOB_MODEL.md
plans/INTERFACES.md
plans/ORCHESTRATION.md
plans/VALIDATION_GATES.md
```

If any of these files do not exist, ask the orchestration process to create them or work only on the assigned Phase 0 planning task.
