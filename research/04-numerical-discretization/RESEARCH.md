# Numerical Discretization Research

## Scope

This note is Phase 0 research only. It designs price-space and time discretization for TRIDENT-LOB and does not define production code, broker connectivity, live order routing, or trading logic. Live trading remains blocked by the repository rules and risk-control Wave 1 decision. Sources: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; risk decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md; SEC market access rule, https://ecfr.io/Title-17/Section-240.15c3-5.

Wave 1 decisions constrain the design. Internal book coordinate is ticks, Phase 1 is a CPU-only feature pipeline, full source and sink validation requires L2 or L3 data, and live trading is blocked. Sources: equation audit decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md; data decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md; Python stack decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Price Space

Use ticks as the computational price coordinate. A cell index `i` represents a one-tick price interval or occupied tick level, with `Delta_p = 1` tick by default. Raw price, tick size, symbol, venue, and timestamp remain metadata for reconstruction and reporting. Recommendation: keep the numerical grid in ticks because tick sizes define valid exchange price increments, and Wave 1 selected ticks as the internal coordinate. Sources: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Use side-specific fields on the same tick grid:

```text
q_plus[i, n]      ask liquidity, shares per tick
q_minus[i, n]     bid liquidity, shares per tick
u_plus[i, n]      ask quote velocity, ticks per second
u_minus[i, n]     bid quote velocity, ticks per second
k[i, n]           market turbulent energy proxy
epsilon[i, n]     dissipation proxy
nu_t[i, n]        eddy diffusivity
```

Recommendation: keep ask and bid fields side-specific rather than storing a signed single field, because the TRIDENT equations have side-specific sources, cancellations, executions, and quote velocities. Source: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

For finite-volume schemes, store cell averages of liquidity and turbulence fields. For finite-difference diagnostics, store nodal approximations only when conservation is not the target. Recommendation: make cell averages the primary representation for Phase 2 because finite-volume methods update cell integrals through boundary fluxes and are built for conservation laws. Source: LeVeque, Finite Volume Methods for Hyperbolic Problems, https://doi.org/10.1017/CBO9780511791253.

Boundary conditions should be conservative and explicit. The minimal Phase 2 boundary is zero outward diffusive flux at the far grid edges, capped advective outflow if quote velocity transports liquidity outside the modeled window, and no artificial source at boundaries. Recommendation: start with no-flux diffusion boundaries and audited advective outflow because book depth should change only through measured events, model sources, sinks, or documented boundary flux. Sources: TRIDENT accounting check, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; LeVeque finite-volume chapter, https://doi.org/10.1017/CBO9780511791253.005.

## Time

Use seconds as the physical time coordinate and retain event timestamps without lookahead. Phase 1 can operate on clock-time bars and top-of-book windows. Phase 2 should use event-time replay as the outer loop and optional PDE substeps between events. Recommendation: separate event timestamps from solver substeps because L2 or L3 message streams provide irregular event times, while explicit PDE updates require stability-limited timesteps. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Courant, Friedrichs, and Lewy stability condition, https://doi.org/10.1147/rd.112.0215.

For a clock interval from `t_n` to `t_{n+1}`, use:

```text
Delta_t_event = t_{n+1} - t_n
Delta_t_solver <= Delta_t_event
number_of_substeps = ceil(Delta_t_event / Delta_t_stable)
```

Recommendation: cap the solver timestep by the most restrictive active advection, diffusion, and reaction condition before every explicit update. Sources: CFL condition, https://doi.org/10.1147/rd.112.0215; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; positivity-preserving reaction-diffusion splitting, https://doi.org/10.1016/j.jcp.2021.110253.

## Method Comparison

Finite volume is the best primary method for a fuller TRIDENT solver. It conserves cell-integrated liquidity, exposes boundary fluxes, and matches the source-sink accounting check in the model specification. It also makes capped sinks natural because each cell has an available mass. Recommendation: use first-order monotone finite volume before any high-order method, then add limiters only after positivity and accounting tests pass. Sources: LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; Patankar, Numerical Heat Transfer and Fluid Flow, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224.

Finite difference is useful for diagnostics, prototype diffusion tests, and smooth latent-interface experiments, but it should not be the primary liquidity solver. It approximates derivatives directly and can be simpler to inspect, but it does not automatically preserve cell mass under source, sink, and boundary flux accounting. Recommendation: use finite difference only for non-conservative diagnostics or controlled synthetic tests in Phase 1. Sources: LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, https://doi.org/10.1137/1.9780898717839; LeVeque finite-volume comparison, https://doi.org/10.1017/CBO9780511791253.005.

Event-driven simulation is essential for order-book accounting. It updates book states at observed add, cancel, delete, execution, and halt messages, so it is the natural way to estimate empirical sources and sinks. It is not a PDE solver by itself, but it is the validation backbone for the PDE. Recommendation: make event replay the empirical truth layer for Phase 2 and the source of synthetic fixtures for Phase 1. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Cont, Stoikov, and Talreja stochastic LOB model, https://doi.org/10.1287/opre.1090.0780.

Stochastic differential equation integration is appropriate for the stochastic price interface and low-dimensional latent state experiments, not for the first liquidity-field solver. Euler-Maruyama is the minimal baseline for SDE experiments, but it needs positivity guards when applied to nonnegative variables such as liquidity, `k`, or `epsilon`. Recommendation: defer SDE integration of the price interface until deterministic accounting, positivity, and baseline feature checks pass. Sources: Kloeden and Platen, Numerical Solution of Stochastic Differential Equations, https://doi.org/10.1007/978-3-662-12616-5; Bayram, Partal, and Buyukoz, https://doi.org/10.1186/s13662-018-1466-5; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489.

Hybrid event-PDE schemes combine event replay with conservative PDE evolution between events. This is the most faithful long-term route for TRIDENT because observed events set sources and sinks, while finite volume evolves diffusion, quote transport, turbulence, and latent fields. Recommendation: use hybrid event-PDE only in Phase 2 after L2 or L3 data is available, because full source and sink validation is not identifiable from bars alone. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Gao and Deng hydrodynamic limit, https://arxiv.org/abs/1411.7502; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

## Positivity And Stability

Nonnegativity is a hard invariant:

```text
q_s[i] >= 0
lambda_s[i] >= 0
mu_s[i] >= 0
e_s[i] >= 0
k[i] >= 0
epsilon[i] > 0
nu_t[i] >= 0
```

Recommendation: reject any solver path that can produce negative liquidity without immediate correction and diagnostic failure, because book sizes, event quantities, and TRIDENT liquidity fields are nonnegative by construction. Sources: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

Execution sinks must be capped by available cell liquidity:

```text
realized_e_s[i] * Delta_t <= q_s[i]
q_s_next[i] = q_s[i] - realized_e_s[i] * Delta_t
```

Recommendation: implement execution as a capped sink in the numerical design and report any requested execution volume that cannot be matched to visible depth. Sources: TRIDENT execution sink check, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; LOBSTER event descriptions, https://data.lobsterdata.com/info/DataStructure.php.

For explicit advection in tick space, use a Courant bound:

```text
max_i abs(u_s[i]) * Delta_t / Delta_p <= C_adv
```

Use `C_adv <= 1` for first-order upwind finite volume. Recommendation: start with `C_adv = 0.5` in research runs and relax only after stability tests pass. Sources: CFL condition, https://doi.org/10.1147/rd.112.0215; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

For explicit diffusion, use the one-dimensional parabolic bound:

```text
max_i D_eff[i] * Delta_t / Delta_p^2 <= C_diff
D_eff = D_0 + nu_t / sigma_q
```

Use `C_diff <= 0.5` for a simple explicit centered diffusion update in one price dimension. Recommendation: use implicit or semi-implicit diffusion in Phase 2 if `nu_t` makes explicit substeps too small for CPU-only research. Sources: LeVeque finite-difference methods, https://doi.org/10.1137/1.9780898717839; Patankar finite-volume heat transfer, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224.

For linear cancellation sinks, explicit updates need:

```text
mu_s[i] * Delta_t <= C_react
```

Use `C_react <= 1` with capped sinks, or use an exact exponential sink update:

```text
q_s_next[i] = q_s[i] * exp(-mu_s[i] * Delta_t)
```

Recommendation: prefer exact or implicit positive reaction updates for cancellations and dissipation terms because reaction-diffusion systems can become stiff and positivity-preserving splitting is a known design goal. Sources: positivity-preserving operator splitting, https://doi.org/10.1016/j.jcp.2021.110253; Patankar source treatment, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224.

## Minimal Phase 1 Solver Path

Phase 1 should not solve the full PDE. It should build a CPU-only feature pipeline with tick-normalized grids, event or bar windows, top-of-book depth, spread, OFI, realized volatility proxy for `k`, decay proxy for `epsilon`, fragility `k^2 / (epsilon + epsilon_0)`, and optional news forcing. Recommendation: keep Phase 1 numerical work to feature construction, synthetic grid fixtures, and small deterministic accounting tests. Sources: market microstructure decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md; equation audit decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md; Cont, Kukanov, and Stoikov OFI, https://arxiv.org/abs/1011.6402.

The minimal Phase 1 numerical artifact is a research-only grid fixture that can:

1. Bin price levels into ticks.
2. Replay synthetic add, cancel, and execution events.
3. Cap sinks by available depth.
4. Compute diagnostic finite-volume fluxes on synthetic fields.
5. Verify positivity, conservation, symmetry, and known-model limits.

Recommendation: keep this artifact offline, local, deterministic by seed, and detached from any broker or live data endpoint. Sources: repository rules, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md; risk decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Fuller Phase 2 Solver Path

Phase 2 should use L2 or L3 event replay as the empirical driver and a finite-volume PDE core as the conservative numerical solver. The outer loop replays observed messages, estimates source and sink fields, advances PDE substeps between events, and audits state changes against book accounting. Recommendation: make finite volume plus event replay the default Phase 2 solver path. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Gao and Deng hydrodynamic limit, https://arxiv.org/abs/1411.7502; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

The Phase 2 path should add SDE interface integration only after the deterministic hybrid solver passes accounting tests. Recommendation: keep stochastic price-interface tests behind a separate validation gate because SDE noise can mask accounting errors and positivity failures. Sources: Kloeden and Platen SDE methods, https://doi.org/10.1007/978-3-662-12616-5; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489.

## Open Questions

1. Can `nu_t` be identified separately from base diffusion `D_0` using practical L2 data, or is L3 required?
2. Should the Phase 2 grid be centered on the midprice, fixed in raw tick coordinates, or use a moving window with conservative remapping?
3. What boundary condition best represents liquidity outside the observed book depth?
4. Should quote velocity `u_s` be estimated as explicit price-space transport, or should cancel-repost behavior be modeled as nonlocal source and sink terms?
5. How should hidden executions and hidden liquidity enter the execution sink when they are visible only as trade prints or partial book effects?
6. What timestep policy is fast enough for CPU-only Mac M3 research when event bursts make `Delta_t_event` extremely small?
7. Should positivity be enforced through conservative limiting, implicit reactions, logarithmic variables, or projection with diagnostic failure?

