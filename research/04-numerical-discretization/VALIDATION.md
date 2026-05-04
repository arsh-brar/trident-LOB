# Numerical Discretization Validation

## Validation Position

Numerical validation is required before any future solver can be trusted as a research component. It does not approve live trading, production execution, or profitability claims. Recommendation: treat every numerical output as research-only until it passes invariant, accounting, stability, and out-of-sample model gates. Sources: repository rules, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md; TRIDENT verification checks, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; Bailey et al. backtest overfitting warning, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Gate 1: Positivity

Acceptance criteria:

```text
min(q_plus) >= 0
min(q_minus) >= 0
min(k) >= 0
min(epsilon) > 0
min(nu_t) >= 0
all realized execution sinks <= available cell liquidity
```

Recommendation: fail the step if any accepted state violates positivity or if a sink consumes more liquidity than available. Sources: TRIDENT nonnegative liquidity check, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; positivity-preserving reaction-diffusion splitting, https://doi.org/10.1016/j.jcp.2021.110253.

## Gate 2: Source-Sink Accounting

For each side:

```text
mass_after - mass_before
= source_mass - realized_sink_mass + boundary_flux + stochastic_mass_delta
```

The residual must be within a configured numerical tolerance on synthetic tests and must be reported on empirical replay. Recommendation: require event-level accounting before validating the full source-sink PDE, because adds, cancels, deletes, and executions are only directly observable in L2 or L3 event data. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; data decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

## Gate 3: Stability Margins

For every explicit update, report:

```text
adv_margin = max_i abs(u_s[i]) * Delta_t / Delta_p
diff_margin = max_i D_eff[i] * Delta_t / Delta_p^2
react_margin = max_i mu_s[i] * Delta_t
```

Acceptance criteria:

```text
adv_margin <= C_adv
diff_margin <= C_diff
react_margin <= C_react
```

Recommendation: fail explicit steps that exceed configured stability margins and subcycle rather than silently accepting unstable updates. Sources: CFL condition, https://doi.org/10.1147/rd.112.0215; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; LeVeque finite-difference methods, https://doi.org/10.1137/1.9780898717839.

## Gate 4: Reaction Treatment

Linear cancellations and dissipation must remain positive under the chosen timestep. Exact exponential or implicit positive updates are preferred when rates are large. Recommendation: require a dedicated reaction validation case with high `mu_s`, high `epsilon` dissipation, and large source impulses before any Phase 2 solver is accepted. Sources: positivity-preserving operator splitting, https://doi.org/10.1016/j.jcp.2021.110253; Patankar source treatment, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224.

## Gate 5: Symmetry

Construct symmetric synthetic books:

```text
q_plus = q_minus
lambda_plus = lambda_minus
mu_plus = mu_minus
M_plus = M_minus
F_plus = F_minus
```

Acceptance criteria: deterministic price drift is zero within tolerance, total side masses remain symmetric within tolerance, and no side-specific numerical bias appears. Recommendation: keep this as a required regression test because TRIDENT defines symmetry as a sanity check. Source: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

## Gate 6: Known-Model Limits

Required limits:

1. With `k = 0` and `nu_t = 0`, the liquidity update reduces to a source-sink order-book model.
2. With only best bid and best ask retained, diagnostics reduce toward OFI over depth.
3. With a linear latent book near the interface, impact follows the square-root form before turbulence adjustment.

Recommendation: validate these limits before testing original TRIDENT turbulence hypotheses. Sources: TRIDENT known-model limits, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; Cont, Kukanov, and Stoikov OFI, https://arxiv.org/abs/1011.6402; Donier et al. latent liquidity and square-root impact, https://arxiv.org/abs/1412.0141.

## Gate 7: Grid And Timestep Convergence

Synthetic smooth-field tests should be run at multiple time steps and grid widths where possible:

```text
Delta_p = 1, 2, 4 ticks for coarse diagnostic comparisons
Delta_t = base, base / 2, base / 4 for timestep sensitivity
```

Acceptance criteria: stable qualitative behavior, decreasing residuals on smooth synthetic cases, and no new positivity violations under refinement. Recommendation: require convergence diagnostics before using a finite-volume solver for Phase 2 research claims. Sources: LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253; LeVeque finite-difference methods, https://doi.org/10.1137/1.9780898717839.

## Gate 8: Event Replay Consistency

On L2 or L3 samples, replayed visible book depth must match vendor-provided snapshots within documented tolerances. Recommendation: validate replay against vendor snapshots before estimating PDE source and sink fields. Sources: LOBSTER message and orderbook file structure, https://data.lobsterdata.com/info/DataStructure.php; Databento equities schemas, https://databento.com/equities.

## Gate 9: Stochastic Interface Sanity

For SDE interface experiments, use fixed seeds, report Monte Carlo error, and compare deterministic and stochastic runs. Acceptance criteria: stochastic noise cannot repair deterministic accounting failures, and interface samples must remain consistent with configured volatility scale. Recommendation: keep SDE integration behind a separate validation gate. Sources: Kloeden and Platen, https://doi.org/10.1007/978-3-662-12616-5; Bayram, Partal, and Buyukoz, https://doi.org/10.1186/s13662-018-1466-5; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489.

## Gate 10: Phase And Safety Boundaries

Phase 1 acceptance means only that feature construction, fixtures, and diagnostic invariants work locally on CPU. It does not validate full TRIDENT PDE dynamics. Phase 2 acceptance requires L2 or L3 replay, source-sink accounting, and finite-volume validation. Recommendation: do not claim full source-sink validation from bars, top-of-book quotes alone, or synthetic fixtures. Sources: data decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

## Open Questions

1. What tolerance should be used for mass residuals when empirical feeds include hidden liquidity or out-of-range levels?
2. What grid-convergence criterion is meaningful on a one-tick natural grid?
3. How should stochastic order-flow noise be separated from deterministic event replay residuals?
4. What validation fixture should represent market halts and reopenings?
5. Should severe volatility periods use stricter stability constants than ordinary periods?

