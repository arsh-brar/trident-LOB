# Decision

## Chosen coordinate system

Phase 1 decision: use ticks as the internal book-space coordinate, with basis points and log returns as normalized feature and target views.

Phase 2 decision: continue using ticks for event replay and finite-volume price cells, with raw price retained as required metadata for reconstruction and reporting.

Recommendation rationale: ticks align with exchange price increments and order-book levels, while basis points and log returns support cross-symbol comparison. Sources: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes; Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

## Chosen units

Use the following canonical units:

- `p`: ticks.
- `t`: seconds.
- `q_s`: shares per tick.
- `u_s`: ticks per second.
- `D_0`, `nu_0`, `nu_t`, `D_k`, `D_epsilon`: ticks squared per second.
- `k`: ticks squared per second squared.
- `epsilon`: ticks squared per second cubed.
- `lambda_s`: shares per tick per second.
- `mu_s`: inverse seconds.
- `e_s`: shares per tick per second.
- `M_s`: shares per second.
- `K_s`: inverse ticks.
- `L`: shares per tick squared.
- `Q`: shares.
- `DeltaP`: ticks.

Recommendation rationale: these units make the liquidity equation, k equation, epsilon equation, eddy diffusivity, impact equation, and market Reynolds number dimensionally consistent. Source: OpenFOAM k-epsilon documentation for k, epsilon, production, and eddy viscosity dimensional relationships, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

## Phase 1 implementation decision

Do not solve the full PDE in Phase 1. Build a CPU-only Python research feature pipeline that computes point-in-time proxies:

- spread in ticks and basis points.
- top-of-book depth.
- OFI or signed trade imbalance proxy.
- realized volatility proxy for `k`.
- volatility decay or shock-absorption proxy for `epsilon`.
- fragility proxy `k^2 / (epsilon + epsilon_0)`.
- market Reynolds number `R_m`.
- optional news intensity `N_t^2` and signed news score.

Recommendation rationale: L1, trades, and bars support these features, while full source and sink estimation requires L2 or L3 event replay. Sources: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

## Phase 2 implementation decision

Use L2 or L3 event replay to estimate `q_plus`, `q_minus`, `lambda_s`, `mu_s`, `e_s`, and price-level transport. Use finite-volume accounting with capped sinks and nonnegative cell states.

Recommendation rationale: event-level data exposes add, cancel, delete, and execution updates needed to verify the source and sink terms, and finite-volume methods are the natural conservation framework for advection-diffusion-reaction equations. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Patankar, Numerical Heat Transfer and Fluid Flow, https://www.routledge.com/product/isbn/9780891165224

## Market Reynolds number decision

Use the following Phase 1 market Reynolds number:

```text
R_m = (abs(I) / (D_top + D_star)) / (epsilon / (k + k_0) + gamma_u)
```

where:

- `I` is signed aggressive imbalance or OFI proxy in shares per second.
- `D_top` is top-of-book depth in shares.
- `D_star` is a positive depth floor in shares.
- `k` is realized variance intensity in tick units.
- `epsilon` is positive volatility decay capacity in tick units.
- `k_0` is a positive floor.
- `gamma_u` is quote damping in inverse seconds.

Recommendation rationale: this formula is dimensionless and compares pressure arrival rate against absorption capacity. It should be validated against OFI and depth baselines before use in model decisions. Source: Cont, Kukanov, and Stoikov on OFI and depth, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

## Nonnegativity decision

Treat nonnegativity as a hard gate:

- `q_s >= 0`
- `lambda_s >= 0`
- `mu_s >= 0`
- `e_s >= 0`
- `k >= 0`
- `epsilon > 0`
- `nu_t >= 0`
- `D_0 >= 0`

Recommendation rationale: market-data book sizes and event quantities are nonnegative, and k-epsilon eddy viscosity requires positive `k` and `epsilon` to avoid undefined or unstable diffusivity. Sources: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

## Open questions

- Should bid and ask quote velocities be modeled in raw price direction or in distance-from-mid coordinates?
- Can `nu_t` be identified separately from base diffusion `D_0` with practical L2 data?
- Should `epsilon` be estimated from volatility decay, depth replenishment, spread recovery, or a joint state model?
- Should `R_m` thresholds be universal, symbol-specific, or regime-specific?
- How should hidden liquidity and hidden executions enter `e_s` and `K_s`?
- Should news direction enter only `F_s`, while `N_t^2` enters `P_k`?

