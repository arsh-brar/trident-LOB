# Equation audit and dimensional analysis

## Scope

This Phase 0 audit reviews the TRIDENT-LOB equations for units, signs, positivity, stability, and market interpretation. It does not add production code, trading code, or any live-trading capability.

Primary recommendations are cited inline with URLs. The audit uses the model equations in `docs/TRIDENT_LOB_MODEL.md` as the object under review.

## Source basis

- Limit order book source, sink, and depth accounting should be tied to event-level add, cancel, delete, and execution messages, because reconstructed LOB data systems expose exactly those event categories and book snapshots. Source: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php
- Phase 1 can use L1 bars, trades, and top-of-book depth, while Phase 2 should use L2 or L3 event replay, because normalized market data schemas separate OHLCV, trades, MBP-1, MBP-10, and MBO by increasing book detail. Source: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas
- Order-flow imbalance over displayed depth is a sound baseline for price movement and should be the first empirical comparator for the TRIDENT Reynolds number, because Cont, Kukanov, and Stoikov find short-horizon price changes are mainly driven by order-flow imbalance with a slope inversely related to depth. Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822
- The latent interface and square-root impact pieces are plausible research analogues, because Donier, Bonart, Mastromatteo, and Bouchaud derive nonlinear market impact from a linear latent order book approximation. Source: https://arxiv.org/abs/1412.0141
- A hydrodynamic order-book limit is a plausible Phase 2 target, but it should not be claimed in Phase 1 from L1 data alone, because Gao and Deng establish fluid limits under a two-sided Markov order book model and test the approximation on liquid stocks. Source: https://arxiv.org/abs/1411.7502
- The k and epsilon closure should be treated as an analogy requiring calibration, because the standard k-epsilon model defines k, epsilon, production, and eddy viscosity in physical units that do not transfer automatically to price space. Source: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/
- Positivity and conservation should be built into later discretizations with finite-volume accounting and nonnegative source treatment, because finite-volume heat, mass, flow, and reaction methods are designed around physical conservation. Source: Patankar, Numerical Heat Transfer and Fluid Flow, https://www.routledge.com/product/isbn/9780891165224

## Base dimensions

Use the following base dimensions for the audit:

- `S`: shares or contracts.
- `P`: price coordinate unit.
- `T`: time.
- `B`: dimensionless news or signal score.

Phase 1 recommendation: use ticks for book-space geometry and basis points or log returns for cross-symbol return features. Phase 2 recommendation: use ticks for event replay and expose raw-price metadata for reconstruction. This keeps price-grid math aligned with exchange tick rules while keeping model features comparable across symbols. Sources: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes; Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

## Unit dictionary

| Quantity | Meaning | Unit |
| --- | --- | --- |
| `p` | price-space coordinate | `P` |
| `t` | time | `T` |
| `dp` | price-space grid width | `P` |
| `q_s(p,t)` | visible liquidity density for side `s` | `S / P` |
| `ell_s(p,t)` | latent liquidity density for side `s` | `S / P` |
| `Phi` | latent sell minus buy pressure | `S / P` |
| `P_t` | midprice interface | `P` |
| `u_s(p,t)` | quote-revision velocity in price space | `P / T` |
| `U` | mean transport velocity for turbulence variables | `P / T` |
| `D_0` | base price-placement diffusion | `P^2 / T` |
| `nu_0` | base quote viscosity in momentum analogue | `P^2 / T` |
| `nu_t` | market eddy diffusivity | `P^2 / T` |
| `k` | market turbulent energy analogue | `P^2 / T^2` |
| `epsilon` | market dissipation rate analogue | `P^2 / T^3` |
| `lambda_s` | new limit-order source density rate | `S / (P T)` |
| `mu_s` | cancellation hazard | `1 / T` |
| `e_s` | execution sink density rate | `S / (P T)` |
| `M_plus`, `M_minus` | aggressive market-order flow by side | `S / T` |
| `K_s` | queue-priority execution kernel over price | `1 / P` |
| `xi_s` | liquidity-density noise rate | `S / (P T)` before discretization |
| `Pi_s` | market pressure analogue | `P^2 S / (P T^2)` if `c_q^2 q_s` is velocity squared times density |
| `c_q^2` | liquidity pressure coefficient | `P^2 / T^2` |
| `c_k` | turbulence pressure coefficient | `S / P` if multiplying `k` |
| `q_star` | pressure regularizer | `S / P` |
| `gamma_u` | quote velocity damping | `1 / T` |
| `F_s` | quote-velocity forcing | `P / T^2` |
| `eta_s` | quote-velocity noise acceleration | `P / T^2` before discretization |
| `D_k` | k diffusion | `P^2 / T` |
| `D_epsilon` | epsilon diffusion | `P^2 / T` |
| `P_k` | k production | `P^2 / T^3` |
| `I` | aggressive flow imbalance | `S / T` |
| `D_top` | top-of-book depth | `S` |
| `D_star` | depth regularizer | `S` |
| `N_t` | exogenous news score | `B` |
| `chi_P` | price-interface noise scale | dimensionless if `nu_t` has `P^2 / T` |
| `L` | latent book slope near midprice | `S / P^2` |
| `Q` | meta-order size | `S` |
| `DeltaP` | impact displacement | `P` |
| `chi_nu` | impact-fragility coefficient | `T / P^2` if multiplying `nu_t` |

Recommendation: Phase 0 should freeze this unit dictionary before coding any feature builder, because mismatched units will otherwise leak directly into `nu_t`, `R_m`, and impact features. Source: OpenFOAM k-epsilon documentation for dimensional k, epsilon, and eddy viscosity, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

## Equation audit

### News forcing

Equation:

```text
N_i(t) = sum_j beta_source(j) * relevance(i,j) * sentiment(j) * novelty(j)
         * exp(-(t - tau_j) / tau_N) * 1[t >= tau_j]
```

Unit check: if all weights and scores are dimensionless, `N_i(t)` is dimensionless. `tau_N` must have unit `T`.

Sign check: `sentiment(j)` may be negative, so `N_i(t)` may be signed. Since `P_k` later uses `N_t^2`, sign information is lost in turbulence production. That is acceptable for volatility or fragility forcing, but directional news forcing must enter `F_s` or a separate drift feature if used.

Positivity: the exponential kernel is nonnegative. The signed score is not positive by design.

Stability: decayed event streams are causal when `1[t >= tau_j]` is enforced. The feature builder must not revise historical scores with later event knowledge.

Market interpretation: `N_i(t)^2` means news intensity, not direction. Recommendation: store both signed news score and squared intensity so direction and turbulence can be tested separately. Source: Databento schemas separate event timestamps and normalized market records, which supports point-in-time feature construction, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Open questions:

- How should source reliability and novelty be estimated without using future corrections?
- Should scheduled events use a pre-event anticipation kernel as well as a post-event decay kernel?

### Visible liquidity equation

Equation:

```text
partial_t q_s + partial_p(q_s * u_s)
=
partial_p [ (D_0 + nu_t / sigma_q) * partial_p q_s ]
+ lambda_s
- mu_s * q_s
- e_s
+ xi_s
```

Unit check:

- `partial_t q_s`: `S / (P T)`.
- `partial_p(q_s u_s)`: `(S / P * P / T) / P = S / (P T)`.
- diffusion term: `(P^2 / T * S / P^2) / P = S / (P T)`.
- `lambda_s`: `S / (P T)`.
- `mu_s q_s`: `S / (P T)`.
- `e_s`: `S / (P T)`.

Sign check: advection is conservative, diffusion smooths density when `D_0 + nu_t / sigma_q >= 0`, `lambda_s` adds liquidity, cancellation and execution remove liquidity. Signs are coherent.

Positivity: positivity is not automatic under explicit advection-diffusion with sinks and noise. Required constraints are `q_s >= 0`, `lambda_s >= 0`, `mu_s >= 0`, `e_s >= 0`, `D_0 >= 0`, `nu_t >= 0`, `sigma_q > 0`, and execution capped by available depth. Recommendation: Phase 2 discretization should use finite-volume cells with capped sinks and nonnegative reconstruction, because event-level LOB messages support exact add, cancel, and execution accounting. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Patankar finite-volume reference, https://www.routledge.com/product/isbn/9780891165224

Stability: for an explicit scheme, enforce an advection CFL bound roughly `dt <= C_a * dp / max(|u_s|)` and diffusion bound roughly `dt <= C_d * dp^2 / max(D_0 + nu_t / sigma_q)`. Capping sinks requires `dt * mu_s <= 1` and `dt * e_s_cell <= q_s_cell`. Recommendation: Phase 1 should avoid full PDE stepping and estimate stable aggregate features, because L1 data lacks the price-level source and sink granularity needed to verify this equation. Source: Databento schema hierarchy, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Market interpretation: this equation is a conservation law for visible resting depth over price. It is only fully observable with L2 or L3 replay, not bars alone. Source: LOBSTER reconstruction documentation, https://data.lobsterdata.com/info/DataStructure.php

Open questions:

- What boundary conditions represent the finite visible book window, zero flux at window edges, absorbing boundaries, or exchange price bands?
- Should cancellations by price level be modeled as hazards or as event impulses?
- How should hidden executions affect visible `e_s` when the book state does not change?

### Execution sink

Equation:

```text
e_plus(p,t) = M_plus(t) * K_plus(p; q_plus)
e_minus(p,t) = M_minus(t) * K_minus(p; q_minus)
```

Unit check: `M_s` has `S / T`; `K_s` must integrate to 1 over price and have unit `1 / P`; therefore `e_s` has `S / (P T)`.

Sign check: `M_s >= 0` and `K_s >= 0` imply `e_s >= 0`. Aggressive buys consume asks, aggressive sells consume bids, which is market-consistent.

Positivity: the sink can overconsume unless cell-level execution is capped by available depth. Recommendation: implement later event replay as execution deltas against displayed queues, because ITCH-style data reports executions against booked visible orders and does not symmetrically add a second event for the aggressor. Source: Nasdaq Data Link explanation of ITCH executions, https://help.data.nasdaq.com/article/999-in-nasdaq-totalview-itch-5-0-i-thought-there-should-be-two-order-execute-messages-for-a-match-number-however-there-is-only-one-order-execute-message-isnt-the-deal-supposed-to-go-both-buy-and-sell-ways

Stability: `K_s` should be compact near the best quote and normalized after masking unavailable depth. If no depth is available, execution should be clipped to zero rather than assigned to empty levels.

Market interpretation: `K_s` is a queue-priority model. It is not identifiable from L1 bars alone. Source: Databento MBO and MBP schema descriptions, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Open questions:

- Should `K_s` include price improvement, hidden liquidity, midpoint trades, or auction prints?
- Should marketable limit orders be included in `M_s` or handled separately?

### Quote momentum analogue

Equation:

```text
partial_t u_s + u_s * partial_p u_s
=
- 1 / (q_s + q_star) * partial_p Pi_s
+ partial_p [ (nu_0 + nu_t) * partial_p u_s ]
- gamma_u * u_s
+ F_s
+ eta_s
```

Unit check: left side is `P / T^2`. The viscous term has `(P^2 / T * 1 / T) / P = P / T^2`. Damping has `P / T^2`. For the pressure term to match, `Pi_s` must have units such that `partial_p Pi_s / q_s = P / T^2`. With `q_s` in `S / P`, `Pi_s` must have `S P / T^2`. This implies `c_q^2 q_s` is valid if `c_q^2` has `P^2 / T^2`, while `c_k k` is valid only if `c_k` has `S / P`.

Sign check: the pressure-gradient sign is physically plausible only if increasing pressure in the positive price direction pushes velocity toward lower prices. For asks and bids, this may need side-specific sign conventions because quote widening means asks move up while bids move down. Recommendation: define `u_plus > 0` as asks revising upward and `u_minus < 0` as bids revising downward in raw price space, then test symmetric widening separately from directional drift. Source: Cont, Kukanov, and Stoikov on order-flow imbalance and depth as directional price drivers, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

Positivity: this equation does not require `u_s` positivity. It requires `q_s + q_star > 0`, `nu_0 + nu_t >= 0`, and `gamma_u >= 0`.

Stability: nonlinear advection requires a CFL bound. Viscosity regularizes shear if nonnegative. The pressure denominator becomes unstable when `q_s` is near zero unless `q_star` is calibrated.

Market interpretation: quote momentum is a latent quote-revision field, not an actual physical velocity. It should be estimated as price-level depth migration in Phase 2 and omitted or proxied in Phase 1. Source: Gao and Deng on hydrodynamic order-book shape limits, https://arxiv.org/abs/1411.7502

Open questions:

- Should `Pi_plus` and `Pi_minus` share the same pressure coefficients?
- Should bid and ask equations be written in distance-from-mid coordinates to simplify widening signs?
- Is Burgers-like quote momentum empirically identifiable from event replay, or should it be a regularized latent state only?

### Turbulent flux closure

Equation:

```text
mean(q_s_prime * u_s_prime) ~= -nu_t * partial_p mean(q_s)
nu_t = C_mu * k^2 / (epsilon + epsilon_0)
```

Unit check: `mean(q_s_prime u_s_prime)` has `S / T`; `nu_t partial_p mean(q_s)` has `P^2 / T * S / P^2 = S / T`. `nu_t` has `P^2 / T` if `k` has `P^2 / T^2` and `epsilon` has `P^2 / T^3`.

Sign check: the negative gradient closure moves turbulent flux down the mean liquidity gradient, which is diffusive and stabilizing.

Positivity: `nu_t >= 0` requires `C_mu >= 0`, `k >= 0`, and `epsilon + epsilon_0 > 0`. Recommendation: use a positive floor for `k` and `epsilon` in any estimator and record when the floor is active, because k-epsilon models assume positive transported turbulence quantities and compute eddy viscosity from `k^2 / epsilon`. Sources: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/; OpenFOAM realizable k-epsilon documentation, https://doc.openfoam.com/2312/tools/processing/models/turbulence/ras/linear-evm/rtm/realizableKEpsilon/

Stability: `epsilon` near zero can produce explosive `nu_t`. The floor `epsilon_0` is required but changes the meaning of fragility. Recommendation: expose `epsilon_0` as a calibrated hyperparameter and report sensitivity. Source: OpenFOAM realizable k-epsilon documentation, https://doc.openfoam.com/2312/tools/processing/models/turbulence/ras/linear-evm/rtm/realizableKEpsilon/

Market interpretation: `nu_t` is best read as shock persistence or liquidity mixing, not literal fluid viscosity.

Open questions:

- Can `nu_t` be identified separately from `D_0` using L2 data?
- Should `C_mu` be constant, symbol-specific, or state-dependent?

### k equation

Equation:

```text
partial_t k + U * partial_p k
=
partial_p [ (D_k + nu_t / sigma_k) * partial_p k ]
+ P_k
- epsilon
+ zeta_k
```

Unit check: all deterministic terms have `P^2 / T^3` when `k` is `P^2 / T^2`, `U` is `P / T`, `D_k` and `nu_t` are `P^2 / T`, `P_k` is `P^2 / T^3`, and `epsilon` is `P^2 / T^3`.

Sign check: production adds k and dissipation removes k, matching the k-epsilon analogy. Source: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

Positivity: negative noise can drive `k < 0`. Recommendation: Phase 1 should estimate `k` from nonnegative realized variance or squared returns rather than directly simulating noisy k dynamics, because realized volatility proxies are naturally nonnegative and are feasible with bars or trades. Source: Databento OHLCV and trades schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Stability: explicit diffusion needs a diffusion time-step bound. Reaction terms need nonnegative source treatment and `epsilon` clipping so dissipation does not make k negative in one step.

Market interpretation: `k` is volatility intensity. In Phase 1, use a realized variance proxy over trailing windows. Do not call it true turbulence kinetic energy. Source: OpenFOAM k-epsilon unit definitions, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

Open questions:

- Which realized-volatility estimator should define `k` under irregular ticks and sparse quotes?
- Should `k` live in tick units or basis-point units for cross-symbol models?

### epsilon equation

Equation:

```text
partial_t epsilon + U * partial_p epsilon
=
partial_p [ (D_epsilon + nu_t / sigma_epsilon) * partial_p epsilon ]
+ C_epsilon1 * epsilon / (k + k_0) * P_k
- C_epsilon2 * epsilon^2 / (k + k_0)
+ zeta_epsilon
```

Unit check: all deterministic terms have `P^2 / T^4`. For example, `epsilon / k * P_k` gives `(1 / T) * (P^2 / T^3) = P^2 / T^4`, and `epsilon^2 / k` gives `P^2 / T^4`.

Sign check: production and nonlinear destruction match the k-epsilon analogy. Source: OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

Positivity: `epsilon` must remain positive or `nu_t` and fragility become undefined. Recommendation: estimate Phase 1 epsilon as a positive volatility decay or mean-reversion rate times `k`, not as an unconstrained regression output. Source: OpenFOAM realizable k-epsilon documentation, https://doc.openfoam.com/2312/tools/processing/models/turbulence/ras/linear-evm/rtm/realizableKEpsilon/

Stability: denominators require `k + k_0 > 0`. If `k` is small, the epsilon equation can become stiff. Later solvers should handle reaction terms implicitly or with positivity-preserving operator splitting.

Market interpretation: `epsilon` is a shock absorption or volatility decay capacity. It is not directly observable from L1 data and should be validated by whether `k^2 / epsilon` predicts persistent spread widening or local jumps out of sample.

Open questions:

- Should epsilon be estimated from decay of realized variance, spread normalization, depth replenishment, or all three?
- How should `k_0` be chosen across symbols and regimes?

### Turbulence production

Equation:

```text
P_k =
C_u * sum_s q_s * (partial_p u_s)^2
+ C_I * I^2 / (D_top + D_star)^2
+ C_c * |partial_t log(D_top)|^2
+ C_N * N_t^2
```

Unit check:

- `sum q_s (partial_p u_s)^2` has `(S / P) * (1 / T)^2 = S / (P T^2)`, so `C_u` must have `P^3 / (S T)`.
- `I^2 / depth^2` has `1 / T^2`, so `C_I` must have `P^2 / T`.
- `|partial_t log(D_top)|^2` has `1 / T^2`, so `C_c` must have `P^2 / T`.
- `N_t^2` is `B^2`, so `C_N` must have `P^2 / (T^3 B^2)`.

Sign check: all four production terms are nonnegative if coefficients are nonnegative.

Positivity: production is nonnegative by construction. `D_top + D_star` must be positive.

Stability: squared imbalance and squared depth-withdrawal terms can spike. Recommendation: winsorize or robust-scale Phase 1 proxies before modeling, and report raw diagnostics separately, because empirical LOB event series include irregularities and halts that must be checked before downstream analysis. Source: LOBSTER FAQ on irregularities and halts, https://lobsterdata.com/info/help_faq_general.php

Market interpretation:

- Quote shear means depth migration and queue instability.
- Aggressive imbalance means immediate pressure over available depth.
- Depth withdrawal means liquidity evaporation.
- News means external information intensity.

Recommendation: Phase 1 should start with the `I^2 / depth^2`, depth withdrawal, realized-volatility, and optional news terms, while deferring quote shear until L2 or L3 data exists. Sources: Cont, Kukanov, and Stoikov on OFI over depth, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822; Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Open questions:

- Should the imbalance term be signed elsewhere for direction?
- Should depth withdrawal use `log(D_top)` or bounded relative change to avoid zero-depth singularities?
- How should coefficients be constrained during estimation?

### Price interface equation

Equations:

```text
Phi(P_t,t) = 0

dP_t = - partial_t Phi(P_t,t) / partial_p Phi(P_t,t) * dt
       + sqrt(2 * chi_P * nu_t(P_t,t)) * dW_t
```

Unit check: `partial_t Phi / partial_p Phi` has `(S / (P T)) / (S / P^2) = P / T`; multiplying by `dt` gives `P`. `sqrt(nu_t) dW_t` gives `sqrt(P^2 / T) * sqrt(T) = P` if `chi_P` is dimensionless.

Sign check: the deterministic sign is mathematically correct from differentiating `Phi(P_t,t) = 0`: `dP/dt = -Phi_t / Phi_p`, provided `Phi_p != 0`.

Positivity: price itself need not be positive in transformed coordinates, but raw equity price must remain positive. Log-price coordinates avoid negative-price paths but complicate tick-grid execution.

Stability: if `partial_p Phi` is near zero, the interface velocity explodes. Recommendation: Phase 2 should require a minimum latent-slope threshold before using interface velocity as a prediction feature. Source: Donier et al. on linear latent order book impact, https://arxiv.org/abs/1412.0141

Market interpretation: the stochastic part makes price diffusion scale with local eddy diffusivity, which is plausible as a volatility proxy but must be tested against simpler realized-volatility baselines.

Open questions:

- How is `Phi` estimated from visible book data without assuming a latent book shape?
- Should `Phi_p` be constrained positive near the midprice?
- Should the stochastic term use local `nu_t`, realized variance, or both?

### Market impact equation

Equations:

```text
ell_plus(p) - ell_minus(p) ~= L * (p - P_t)
Q = integral_0^DeltaP L * x dx = 0.5 * L * DeltaP^2
DeltaP = sqrt(2Q / L)
L_eff = L / (1 + chi_nu * nu_t)
DeltaP ~= sqrt(2Q * (1 + chi_nu * nu_t) / L)
```

Unit check: `L` has `S / P^2`, so `L x dx` integrates to `S`. `2Q / L` has `P^2`. `chi_nu` must have `T / P^2` if multiplying `nu_t`.

Sign check: for buy meta-orders, `DeltaP >= 0` when `Q >= 0` and `L > 0`. For sells, use signed impact or apply the formula to magnitude and attach sign separately.

Positivity: require `Q >= 0`, `L > 0`, and `1 + chi_nu nu_t > 0`.

Stability: impact diverges when `L` approaches zero. Recommendation: cap or withhold impact estimates when latent slope is below a validated floor. Source: Donier et al. latent linear book and square-root impact framework, https://arxiv.org/abs/1412.0141

Market interpretation: the turbulence adjustment reduces usable liquidity when `nu_t` is high. This is a hypothesis, not an established result. Recommendation: test the claim as a conditional impact or spread-widening effect against OFI over depth before using it in any decision process. Source: Cont, Kukanov, and Stoikov OFI baseline, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

Open questions:

- Is `nu_t` the right fragility adjustment, or should `k^2 / epsilon` enter directly?
- Should `L` be estimated from visible slope, latent model fit, or short-horizon impact response?

### Market Reynolds number

Equation:

```text
R_m = ( |I| / (D_top + D_star) ) / ( epsilon / (k + k_0) + gamma_u )
```

Unit check: numerator has `(S / T) / S = 1 / T`. `epsilon / k` has `1 / T`; `gamma_u` has `1 / T`. Therefore `R_m` is dimensionless.

Sign check: numerator and denominator are nonnegative if floors and damping are positive. The crash-like condition is equivalent to `R_m > 1`.

Positivity: require `D_top + D_star > 0`, `k + k_0 > 0`, `epsilon >= 0`, and `gamma_u >= 0`.

Stability: `R_m` is sensitive to low depth, low k denominator choices, and low epsilon. Recommendation: report each component alongside `R_m` and run ablations against OFI and depth alone. Source: Cont, Kukanov, and Stoikov on OFI and depth, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

Market interpretation: `R_m` compares pressure arrival rate to dissipation and damping capacity. It is a dimensionless fragility score, not a proof of crash risk.

Open questions:

- Should `I` be OFI from book events, signed trade imbalance, or both?
- Should `D_top` use same-side depth, total top depth, or harmonic depth?
- Should thresholds be universal or symbol-specific?

### Verification equations

Order-book accounting:

```text
d/dt integral q_s dp = integral lambda_s dp
                       - integral mu_s q_s dp
                       - integral e_s dp
                       + boundary flux
```

Unit check: both sides have `S / T`. Signs are coherent. Recommendation: Phase 2 should reconcile integrated PDE source and sink terms to event replay totals per interval. Source: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

Nonnegative liquidity:

```text
q_s >= 0
lambda_s >= 0
mu_s >= 0
e_s >= 0
```

Recommendation: treat nonnegativity as a hard validation gate rather than a soft diagnostic, because displayed book sizes are nonnegative by data schema and event accounting. Source: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Symmetry sanity check:

```text
q_plus = q_minus
lambda_plus = lambda_minus
mu_plus = mu_minus
M_plus = M_minus
F_plus = F_minus
```

Recommendation: deterministic drift should be zero under symmetric conditions, but spread widening may still occur if both sides move away from midprice. Source: Cont, Kukanov, and Stoikov on imbalance as a directional price driver, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

Known-model limits:

- If `k = 0`, `nu_t = 0`, and quote velocity is ignored, the model becomes a stochastic source and sink order-book model.
- If latent book is linear near the midprice, the model recovers square-root impact.
- If only best bid and ask are retained, the model reduces toward OFI over depth.

Recommendation: these limits should become unit tests and research notebooks before any production feature work. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Cont, Kukanov, and Stoikov, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

## Nondimensional groups

Let `P0` be the price-space scale, `T0` the time scale, `Q0` the depth scale, `U0 = P0 / T0`, `K0 = P0^2 / T0^2`, and `E0 = P0^2 / T0^3`.

Recommended Phase 1 scales:

- `P0 = 1 tick` for book geometry.
- `T0 = 60 seconds` for minute-bar features.
- `Q0 = median top-of-book depth` over a trailing point-in-time window.
- `K0 = trailing realized variance in tick units per `T0`.

Recommendation: use trailing, point-in-time scales only, because future normalization would leak future data into features. Source: Databento timestamped schemas support point-in-time market records, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

Core dimensionless groups:

| Group | Formula | Interpretation |
| --- | --- | --- |
| Market Reynolds number | `R_m = (|I| / (D_top + D_star)) / (epsilon / (k + k_0) + gamma_u)` | pressure arrival rate over dissipation plus damping |
| Liquidity Peclet number | `Pe_q = |u| P0 / (D_0 + nu_t / sigma_q)` | quote transport over diffusion |
| Turbulence Peclet number | `Pe_k = |U| P0 / (D_k + nu_t / sigma_k)` | k transport over k diffusion |
| Diffusive Courant number | `Fo_q = (D_0 + nu_t / sigma_q) dt / dp^2` | explicit diffusion stability diagnostic |
| Advective Courant number | `Co_u = |u| dt / dp` | explicit advection stability diagnostic |
| Sink number | `Da_cancel = mu dt` | cancellation hazard per step |
| Execution depletion number | `Da_exec = e_cell dt / q_cell` | fraction of available cell depth consumed |
| Fragility ratio | `Fr_m = k^2 / (epsilon + epsilon_0)` | shock persistence proxy with units `P^2 / T` |
| Dimensionless eddy diffusivity | `Nu_m = nu_t / D_0` | turbulent diffusion over base diffusion |
| News production ratio | `Np = C_N N_t^2 / P_k` | share of k production attributed to news |

Recommendation: report `R_m`, `Pe_q`, `Co_u`, `Fo_q`, `Da_cancel`, and `Da_exec` together in Phase 2 solver diagnostics, because stability and interpretation cannot be separated for advection-diffusion-reaction systems. Source: Patankar finite-volume reference, https://www.routledge.com/product/isbn/9780891165224

## Main audit conclusions

1. The core liquidity equation is dimensionally coherent if `q_s` is a density in shares per price unit, `u_s` is price per time, `lambda_s` and `e_s` are density rates, and `nu_t` is price squared per time.
2. The k-epsilon analogy is dimensionally coherent in price space if `k` is price squared per time squared and `epsilon` is price squared per time cubed.
3. The pressure term requires explicit units for `c_q`, `c_k`, and `Pi_s`; this is the most important missing dimensional specification.
4. Phase 1 should not solve the PDE. It should compute point-in-time proxies for OFI, depth, realized volatility, volatility decay, fragility, and `R_m`, then compare them to simple baselines.
5. Phase 2 should move to event-level L2 or L3 replay with finite-volume accounting, capped sinks, and positivity checks.
6. Tick units are the right book-space coordinate for Phase 1 and Phase 2. Log returns or basis points are right output and cross-symbol feature coordinates, not the internal book grid.

Each conclusion is supported by the cited market-data schema, LOB reconstruction, k-epsilon, hydrodynamic-limit, latent-order-book, and OFI sources listed above.

