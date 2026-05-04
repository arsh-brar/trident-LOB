# Numerical Discretization Options

## Evaluation Criteria

The discretization must preserve nonnegative liquidity, expose source-sink accounting, respect tick-space units, support CPU-only Phase 1 research, and allow a fuller L2 or L3 event-driven solver in Phase 2. Recommendation: reject any option that cannot audit book mass or prevent negative `q_s`, `k`, and `epsilon`. Sources: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; equation audit decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md; positivity-preserving reaction-diffusion splitting, https://doi.org/10.1016/j.jcp.2021.110253.

## Option A: Finite Volume

Finite volume stores cell averages over tick cells and updates them with numerical fluxes plus sources and sinks. It is a natural match for the liquidity equation because the model includes advection, diffusion, sources, cancellations, executions, stochastic forcing, and boundary flux checks.

Recommendation: choose finite volume as the primary Phase 2 PDE method. It is conservative, makes boundary flux explicit, and aligns with the TRIDENT accounting identity. Sources: LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; TRIDENT accounting checks, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Strengths:

- Conserves liquidity up to sources, sinks, and boundary flux.
- Supports capped execution sinks by cell.
- Works naturally on a tick grid.
- Can start with monotone first-order upwind and add limiters later.

Weaknesses:

- More implementation detail than finite difference.
- Requires careful source-term treatment for positivity.
- Explicit diffusion can force small timesteps when `nu_t` is large.

Best phase: Phase 2 as the fuller solver. Phase 1 only for synthetic diagnostics.

## Option B: Finite Difference

Finite difference approximates derivatives of the liquidity, velocity, turbulence, or latent-interface fields. It is simple for diffusion diagnostics and smooth latent fields but weaker for source-sink book accounting.

Recommendation: use finite difference only for Phase 1 diagnostics, synthetic smooth-field tests, and possibly latent-interface experiments where conservation is not the primary invariant. Sources: LeVeque finite-difference methods, https://doi.org/10.1137/1.9780898717839; LeVeque finite-volume comparison, https://doi.org/10.1017/CBO9780511791253.005.

Strengths:

- Simple formulas and easy inspection.
- Useful for controlled diffusion and interface tests.
- Good teaching and sanity-check tool.

Weaknesses:

- Conservation is not automatic.
- Positivity can fail under explicit reaction and diffusion updates.
- Boundary flux accounting is less direct than finite volume.

Best phase: Phase 1 diagnostics only.

## Option C: Event-Driven Simulation

Event-driven simulation replays limit order, cancellation, deletion, execution, and halt events. It updates the book exactly at observed timestamps and is the empirical source of `lambda_s`, `mu_s`, and `e_s`.

Recommendation: use event-driven replay as the empirical accounting layer and validation backbone whenever L2 or L3 data is available. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Cont, Stoikov, and Talreja stochastic LOB model, https://doi.org/10.1287/opre.1090.0780.

Strengths:

- Matches the native market-data event structure.
- Gives direct accounting for adds, cancels, deletes, executions, and halts.
- Avoids artificial clock-time interpolation during replay.

Weaknesses:

- Does not solve diffusion or quote-transport PDE terms by itself.
- Requires L2 or L3 data for full source-sink validation.
- Can be expensive during event bursts without careful batching.

Best phase: Phase 1 fixtures and Phase 2 empirical replay.

## Option D: Stochastic Differential Equation Integration

SDE integration is relevant for the stochastic price interface and low-dimensional latent state models. Euler-Maruyama is the minimal method for SDE experiments, and Milstein or implicit methods can be considered later for stronger convergence or stiffness.

Recommendation: do not use SDE integration as the first liquidity solver. Use it later for the stochastic price interface after deterministic accounting passes. Sources: Kloeden and Platen, https://doi.org/10.1007/978-3-662-12616-5; Bayram, Partal, and Buyukoz, https://doi.org/10.1186/s13662-018-1466-5; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489.

Strengths:

- Directly represents stochastic interface noise.
- Useful for Monte Carlo stress tests.
- Matches the TRIDENT stochastic interface term.

Weaknesses:

- Random noise can obscure deterministic accounting defects.
- Standard Euler-Maruyama does not preserve positivity for arbitrary nonnegative states.
- Calibration is not identifiable from bars alone.

Best phase: Phase 2 or later research extension.

## Option E: Hybrid Event-PDE Scheme

A hybrid event-PDE scheme replays observed order-book events and advances a finite-volume PDE state between event timestamps. Events provide empirical sources and sinks. PDE substeps evolve diffusion, quote transport, turbulence, and latent liquidity.

Recommendation: select hybrid event-PDE as the fuller Phase 2 architecture, with finite volume as the PDE core and event replay as the data driver. Sources: Gao and Deng hydrodynamic limit, https://arxiv.org/abs/1411.7502; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

Strengths:

- Best match to TRIDENT's event sources and PDE dynamics.
- Allows accounting checks at every event boundary.
- Can support deterministic PDE, stochastic interface, and synthetic stress tests.

Weaknesses:

- Most complex option.
- Requires L2 or L3 data for serious validation.
- Needs strict timestep, remapping, and positivity gates.

Best phase: Phase 2.

## Comparison

| Option | Conservation | Positivity path | Data need | Phase 1 fit | Phase 2 fit |
| --- | --- | --- | --- | --- | --- |
| Finite volume | Strong | Monotone fluxes, capped sinks, positive splitting | Synthetic or L2/L3 | Medium | Strong |
| Finite difference | Weak to medium | Small timesteps or projection | Synthetic | Medium | Weak |
| Event-driven simulation | Strong for observed events | Direct nonnegative event sizes and caps | L2/L3 for full use | Strong for fixtures | Strong |
| SDE integration | Not for field mass | Special positive schemes or guarded states | Calibrated state data | Weak | Medium |
| Hybrid event-PDE | Strong if audited | Finite volume plus positive reaction updates | L2/L3 | Weak | Strong |

Recommendation: use a two-stage plan. Phase 1 should use event-style fixtures, tick grids, feature windows, and small finite-volume diagnostics. Phase 2 should use hybrid event-PDE with finite volume as the conservative PDE core. Sources: market microstructure decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md; data decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

## Open Questions

1. Should Phase 2 use one-tick cells only, or allow coarser cells away from the midprice?
2. Should high-order finite volume be considered after monotone first-order tests pass, or is first order enough for research interpretability?
3. Is a moving grid worth the complexity if it requires conservative remapping around the midprice?
4. Can SDE interface noise be separated empirically from ordinary volatility and spread effects?

