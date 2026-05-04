# Numerical Discretization Decision

## Decision

Use ticks as the numerical price coordinate and seconds as the time coordinate. Store raw price, tick size, venue, and symbol metadata alongside the grid. Recommendation: keep `Delta_p = 1` tick for the default internal grid because exchange tick sizes define valid price increments and Wave 1 selected ticks as the canonical coordinate. Sources: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes; equation audit decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md.

Phase 1 will not solve the full TRIDENT PDE. It will use a CPU-only feature and validation pipeline with tick-normalized price levels, event-style fixtures, finite-volume diagnostic checks on synthetic fields, and no live trading. Recommendation: Phase 1 should estimate features and test invariants, not build a production solver or broker path. Sources: market microstructure decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md; Python stack decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md; risk decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Phase 2 should use a hybrid event-PDE solver. Event replay provides empirical sources and sinks from L2 or L3 data. A finite-volume PDE core evolves liquidity, diffusion, quote transport, turbulence, and latent fields between event boundaries. Recommendation: select finite volume as the primary PDE discretization for Phase 2 because it conserves cell mass through numerical fluxes and supports book-accounting audits. Sources: LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Gao and Deng hydrodynamic limit, https://arxiv.org/abs/1411.7502.

## Rejected As Primary Paths

Finite difference is rejected as the primary liquidity solver because it approximates derivatives directly and does not naturally expose the source-sink and boundary-flux accounting required by TRIDENT. Recommendation: use finite difference only for diagnostics and synthetic smooth-field tests. Sources: LeVeque finite-difference methods, https://doi.org/10.1137/1.9780898717839; LeVeque finite-volume chapter, https://doi.org/10.1017/CBO9780511791253.005.

Pure event-driven simulation is rejected as the only solver because it cannot represent diffusion, quote transport, turbulence closure, or latent-interface PDE terms without an added field evolution step. Recommendation: use event replay as the empirical truth layer, not as a replacement for the fuller PDE design. Sources: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780; TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Pure SDE integration is rejected as the first solver because it is aimed at stochastic interface and low-dimensional state dynamics, not conservative liquidity-field accounting. Recommendation: defer SDE interface integration until deterministic finite-volume accounting passes. Sources: Kloeden and Platen, https://doi.org/10.1007/978-3-662-12616-5; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489.

## Positivity Decision

Nonnegativity is a hard gate for every future solver path:

```text
q_s >= 0
lambda_s >= 0
mu_s >= 0
e_s >= 0
k >= 0
epsilon > 0
nu_t >= 0
```

Recommendation: a step that produces negative liquidity, negative `k`, nonpositive `epsilon`, or negative `nu_t` must fail validation unless a documented positivity-preserving limiter or implicit positive reaction update fixes it before the state is accepted. Sources: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/; positivity-preserving reaction-diffusion splitting, https://doi.org/10.1016/j.jcp.2021.110253.

Execution sinks must be capped by available visible depth in each affected cell. Recommendation: never allow `e_s[i] * Delta_t > q_s[i]`; report unmatched requested execution as a diagnostic rather than borrowing liquidity from the future or another cell. Sources: TRIDENT execution sink definition, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; LOBSTER event accounting, https://data.lobsterdata.com/info/DataStructure.php.

## Stability Decision

Any explicit future PDE update must satisfy all active timestep limits:

```text
max_i abs(u_s[i]) * Delta_t / Delta_p <= C_adv
max_i D_eff[i] * Delta_t / Delta_p^2 <= C_diff
max_i mu_s[i] * Delta_t <= C_react
D_eff = D_0 + nu_t / sigma_q
```

Recommendation: start with `C_adv = 0.5`, `C_diff = 0.5`, and `C_react = 1.0` for research diagnostics, with exact or implicit positive reaction updates preferred when reactions are stiff. Sources: CFL condition, https://doi.org/10.1147/rd.112.0215; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; positivity-preserving reaction-diffusion splitting, https://doi.org/10.1016/j.jcp.2021.110253.

If explicit diffusion forces too many substeps, Phase 2 should use semi-implicit or implicit diffusion while keeping advection and event sinks audited. Recommendation: prefer stable implicit diffusion over relaxing positivity or timestep constraints. Sources: Patankar, Numerical Heat Transfer and Fluid Flow, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224; LeVeque finite-difference methods, https://doi.org/10.1137/1.9780898717839.

## Minimal Phase 1 Path

The minimal Phase 1 path is:

1. Build tick-indexed research fixtures from bars, top-of-book quotes, trades if available, and synthetic L2-like events.
2. Compute spread, top-book depth, OFI or signed imbalance proxy, realized volatility proxy for `k`, decay proxy for `epsilon`, fragility, and market Reynolds number.
3. Run synthetic finite-volume accounting checks without solving the full PDE.
4. Validate no future data, nonnegative states, capped sinks, symmetry, and known-model limits.

Recommendation: stop Phase 1 at feature and invariant validation unless a later planning gate approves a solver implementation task. Sources: TRIDENT Phase 1 target, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; Cont, Kukanov, and Stoikov OFI, https://arxiv.org/abs/1011.6402; Bailey et al. backtest overfitting warning, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Fuller Phase 2 Path

The fuller Phase 2 path is:

1. Ingest L2 or L3 event messages with add, cancel, delete, execution, and halt semantics.
2. Reconstruct `q_plus` and `q_minus` across tick levels.
3. Estimate `lambda_s`, `mu_s`, and `e_s` from event replay.
4. Advance finite-volume advection-diffusion-reaction substeps between event boundaries.
5. Use positive reaction updates and capped execution sinks.
6. Add stochastic interface integration only after deterministic accounting passes.
7. Validate against event accounting, nonnegativity, symmetry, known-model limits, and grid convergence.

Recommendation: require L2 or L3 data before claiming full TRIDENT source-sink validation. Sources: data decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Databento equities schemas, https://databento.com/equities.

## Non-Decision

No production solver is approved. No live trading, live broker integration, or live-trading code is approved. No profitability claim is made. Sources: repository rules, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md; risk decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Open Questions

1. Should Phase 2 use a fixed raw tick grid or a moving grid centered on midprice?
2. Should quote transport be modeled as local advection or as nonlocal cancel-repost source and sink pairs?
3. What is the most defensible positivity-preserving treatment for the `epsilon` equation?
4. Can practical L2 data distinguish turbulent diffusion from unobserved replenishment?
5. How should hidden liquidity and hidden executions be represented without violating accounting?

