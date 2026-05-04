# Phase 2 LOB Replay Plan

Status: Phase 0 plan. Phase 2 starts only after Phase 1 validation gates pass and data rights are settled.

## Goal

Build L2 or L3 event replay to estimate visible book fields, source terms, cancellation sinks, execution sinks, depth recovery, and fuller TRIDENT accounting. Sources: [model spec](../docs/TRIDENT_LOB_MODEL.md), [numerical decision](../research/04-numerical-discretization/DECISION.md), [calibration decision](../research/05-stochastic-processes-and-calibration/DECISION.md).

## Required Data

Use licensed L2 or L3 data with add, cancel, modify, execution, order-book states, accurate timestamps, halts, symbol mapping, corporate actions, and calendar metadata. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities, https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview.

## Solver Path

Recommendation: Use a hybrid event-PDE design. Event replay is the empirical truth layer. Finite-volume diagnostics evolve fields between event boundaries and audit source, sink, flux, positivity, stability, and known-model limits. Sources: [numerical decision](../research/04-numerical-discretization/DECISION.md), https://doi.org/10.1017/CBO9780511791253, https://arxiv.org/abs/1411.7502.

Do not build a production PDE solver until deterministic accounting, nonnegativity, symmetry, and convergence diagnostics pass. Sources: [numerical validation](../research/04-numerical-discretization/VALIDATION.md), [testing validation](../research/13-testing-validation-and-benchmarks/VALIDATION.md).

## Estimation Scope

- `q_plus`, `q_minus`: visible depth by tick level.
- `lambda_s`: limit-order arrival intensity by side, level, and state.
- `mu_s`: cancellation hazard by side, level, and state.
- `e_s`: execution sink capped by visible liquidity.
- `u_s`: quote-revision proxy from cancel-repost or depth migration evidence.
- `D_eff`: effective diffusion, with `D_0` and `nu_t` separation treated as open until evidence supports it.

Sources: [calibration decision](../research/05-stochastic-processes-and-calibration/DECISION.md), [equation audit](../research/01-equation-audit-and-dimensional-analysis/DECISION.md).

## Definition Of Done

- L2 or L3 license and storage policy are documented.
- Replay reconstructs nonnegative visible book states.
- Source, cancellation, execution, and boundary flux accounting reconciles within tolerance.
- Event order is deterministic and point-in-time.
- No hidden liquidity is invented to make accounting pass.
- No live trading code is introduced.

