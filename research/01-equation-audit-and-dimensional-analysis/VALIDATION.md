# Validation

## Phase 0 validation gates

### Gate 1: dimensional consistency

Pass criteria:

- `q_s` is shares per tick.
- `u_s` is ticks per second.
- `D_0`, `nu_0`, `nu_t`, `D_k`, and `D_epsilon` are ticks squared per second.
- `k` is ticks squared per second squared.
- `epsilon` is ticks squared per second cubed.
- `lambda_s` and `e_s` are shares per tick per second.
- `mu_s` and `gamma_u` are inverse seconds.
- `R_m` is dimensionless.

Recommendation: no Phase 1 implementation should start until these units are encoded in research configuration or documentation, because the k-epsilon analogy depends on dimensional consistency among `k`, `epsilon`, and `nu_t`. Source: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

### Gate 2: coordinate consistency

Pass criteria:

- Internal book coordinates are ticks.
- Raw price is retained as metadata.
- Basis points or log returns are used only for normalized features and targets.
- Tick size is point-in-time metadata.

Recommendation: reject any Phase 1 feature file that mixes raw price, ticks, and basis points without explicit conversion metadata. Source: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes

### Gate 3: nonnegativity constraints

Pass criteria:

- `q_s >= 0`
- `lambda_s >= 0`
- `mu_s >= 0`
- `e_s >= 0`
- `k >= 0`
- `epsilon > 0`
- `nu_t >= 0`
- `D_0 >= 0`

Recommendation: treat violations as hard errors in later validation, because order-book sizes are nonnegative and eddy viscosity is undefined when epsilon is nonpositive. Sources: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; OpenFOAM realizable k-epsilon documentation, https://doc.openfoam.com/2312/tools/processing/models/turbulence/ras/linear-evm/rtm/realizableKEpsilon/

### Gate 4: accounting consistency

Pass criteria:

```text
change in integrated q_s
= integrated source
- integrated cancellation
- integrated execution
+ boundary flux
```

Recommendation: require this gate for Phase 2 event replay, because reconstructed LOB datasets provide message and orderbook files that can reconcile event updates with book states. Source: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

### Gate 5: no future data

Pass criteria:

- All rolling scales use trailing windows only.
- News features use `1[t >= tau_j]`.
- Normalization parameters are fit only on training windows.
- Validation windows occur strictly after training windows.

Recommendation: block any feature that uses future normalization or revised event values without point-in-time timestamps, because future information would invalidate out-of-sample claims. Source: Databento schemas expose event timestamps needed for point-in-time records, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

## Equation-specific validation

### Liquidity equation

Checks:

- Integrated source and sink accounting matches event totals in Phase 2.
- Sink terms never consume more than available depth.
- Diffusion coefficient `D_0 + nu_t / sigma_q` is nonnegative.
- Symmetric bid and ask inputs produce zero deterministic directional drift.

Recommendation: implement this with finite-volume accounting in Phase 2, because the equation is a conservation law with sources and sinks. Source: Patankar finite-volume reference, https://www.routledge.com/product/isbn/9780891165224

### Execution kernel

Checks:

- `K_s >= 0`.
- `sum K_s dp = 1` over available executable cells.
- `e_s dt <= q_s` per cell after depth masking.
- Aggressive buys consume asks and aggressive sells consume bids.

Recommendation: validate execution against event replay rather than bar aggregates, because ITCH-style executions reduce booked visible orders and do not include a paired aggressor book event. Source: Nasdaq Data Link ITCH execution explanation, https://help.data.nasdaq.com/article/999-in-nasdaq-totalview-itch-5-0-i-thought-there-should-be-two-order-execute-messages-for-a-match-number-however-there-is-only-one-order-execute-message-isnt-the-deal-supposed-to-go-both-buy-and-sell-ways

### Quote momentum

Checks:

- `q_s + q_star > 0`.
- `nu_0 + nu_t >= 0`.
- `gamma_u >= 0`.
- Sign convention for bid and ask quote revisions is declared.
- Pressure units satisfy the acceleration equation.

Recommendation: do not require quote momentum in Phase 1, because L1 data cannot identify price-level quote-revision velocity. Source: Databento schema hierarchy from L1 through L3, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

### k and epsilon

Checks:

- `k >= 0`.
- `epsilon > 0`.
- `epsilon_0 > 0`.
- `k_0 > 0`.
- `nu_t = C_mu k^2 / (epsilon + epsilon_0) >= 0`.
- `P_k >= 0` when production coefficients are nonnegative.

Recommendation: Phase 1 should estimate `k` from realized variance and epsilon from positive decay or absorption proxies, because direct stochastic simulation can violate positivity without specialized numerics. Source: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

### Price interface

Checks:

- `Phi(P_t,t) = 0` is bracketed by opposite signs in the latent book.
- `partial_p Phi` is above a minimum absolute slope threshold.
- Stochastic increment variance is nonnegative.
- Impact sign is attached separately for buy and sell meta-orders.

Recommendation: validate the latent interface only after enough book-depth data exists, because the latent-order-book assumption is a model restriction and not directly observed in L1 data. Source: Donier et al. latent-order-book impact model, https://arxiv.org/abs/1412.0141

### Market Reynolds number

Checks:

- Numerator `abs(I) / (D_top + D_star)` has inverse-second units.
- Denominator `epsilon / (k + k_0) + gamma_u` has inverse-second units.
- `R_m` is finite and nonnegative.
- Component ablations are reported: `I`, `D_top`, `k`, `epsilon`, `gamma_u`, and floors.
- Predictive tests compare `R_m` against OFI over depth.

Recommendation: do not interpret `R_m > 1` as a crash prediction until it beats OFI and depth baselines out of sample with transaction-cost-aware evaluation where relevant. Source: Cont, Kukanov, and Stoikov on OFI and depth, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

## Stability diagnostics for Phase 2

Required diagnostics:

```text
Co_u = max(|u|) dt / dp
Fo_q = max(D_0 + nu_t / sigma_q) dt / dp^2
Fo_k = max(D_k + nu_t / sigma_k) dt / dp^2
Da_cancel = max(mu_s) dt
Da_exec = max(e_cell dt / q_cell)
```

Recommendation: report these diagnostics for every PDE replay experiment, because advection, diffusion, cancellation, and execution can each independently break stability or positivity. Source: Patankar finite-volume reference, https://www.routledge.com/product/isbn/9780891165224

## Market interpretation tests

Minimum tests:

- Symmetric book test: balanced sides should produce zero deterministic price drift.
- Depth depletion test: higher `abs(I) / depth` should increase predicted movement or spread-widening risk.
- Fragility test: for the same imbalance and depth, higher `k^2 / epsilon` should predict more persistent volatility or spread widening.
- News intensity test: `N_t^2` should predict volatility or spread effects separately from signed news direction.
- Impact test: larger `nu_t` or fragility should increase conditional impact only if the effect survives OFI and depth controls.

Recommendation: these tests should be run against simple baselines before complex models, because OFI and depth are already strong short-horizon microstructure predictors. Source: Cont, Kukanov, and Stoikov, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

## Open questions

- What is the most stable point-in-time estimator for epsilon from L1 data?
- Should volatility decay be measured in ticks, basis points, or both?
- How should the model handle locked or crossed books in raw data?
- Should halts and auction periods be excluded, modeled separately, or treated as boundary states?
- Can hidden executions be used to infer latent liquidity without contaminating visible-depth accounting?
- What thresholds define acceptable finite-volume residuals in Phase 2?

