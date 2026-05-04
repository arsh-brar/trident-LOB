# Options

## Coordinate choices

### Option A: raw price

Raw price uses dollars or native instrument price units as `p`.

Pros:

- It maps directly to exchange-reported prices and vendor schemas. Source: Databento documents price fields in normalized market-data records, https://databento.com/docs/knowledge-base/new-users/market-data-schemas
- It preserves natural interpretation for impact in dollars or cents.

Cons:

- It is not naturally comparable across symbols with different price levels.
- It makes grid spacing symbol-dependent when tick sizes vary.

Recommendation: keep raw price as metadata and reconstruction input, but do not use it as the main internal Phase 1 feature coordinate. Source: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes

### Option B: ticks

Ticks use `x = (p - reference_price) / tick_size` as the local book coordinate.

Pros:

- It aligns book geometry with exchange minimum price increments. Source: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes
- It makes queue levels and price-grid diffusion easier to audit.
- It maps naturally to L2 and L3 order-book reconstruction.

Cons:

- Tick value can change by symbol, regime, and rule. The feature builder must store the tick-size source.
- Tick units are not sufficient for cross-symbol return targets.

Recommendation: use ticks as the Phase 1 and Phase 2 internal book-space coordinate, with point-in-time tick-size metadata. Sources: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes; Databento instrument definitions and schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

### Option C: log price

Log price uses `x = log(p)`.

Pros:

- Returns are additive and approximately scale-free.
- Positive raw prices map to all real numbers.

Cons:

- Exchange books do not live on an equal log-price grid.
- Execution queues and tick-level depth must be transformed back to raw ticks for accounting.

Recommendation: use log returns for targets and volatility features, but not as the primary order-book grid. Source: Cont, Kukanov, and Stoikov emphasize OFI and displayed depth at best bid and ask, which are book-level rather than log-grid objects, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

### Option D: basis points

Basis points use normalized price changes, usually `10000 * DeltaP / P_ref`.

Pros:

- They are intuitive for cross-symbol spread and return comparison.
- They are compatible with Phase 1 bar and quote features.

Cons:

- They blur discrete tick and queue mechanics.
- They require a reference price and can be noisy for very low-price symbols.

Recommendation: use basis points for cross-symbol reporting, spread features, and model targets, but keep tick units for book geometry. Source: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes

## Liquidity-density options

### Option A: shares per tick

Define `q_s` as shares per tick. Then `dp = 1 tick`, `u_s` is ticks per second, `D_0` and `nu_t` are ticks squared per second, `k` is ticks squared per second squared, and `epsilon` is ticks squared per second cubed.

Recommendation: use shares per tick for Phase 1 top-book proxies and Phase 2 grid cells, because LOBSTER and normalized market-data schemas expose sizes at price levels and event updates by price level. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

### Option B: shares per dollar

Define `q_s` as shares per dollar or native price unit.

Recommendation: keep this as a derived reporting view only, because it is more awkward for finite-volume event replay on a discrete tick grid. Source: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes

### Option C: notional per tick

Define `q_s` as dollars notional per tick.

Recommendation: do not use this as the primary Phase 1 unit, because execution sinks and market-order sizes are naturally shares or contracts in event data, while notional can be derived later for reporting. Source: LOBSTER event fields include size and price separately, https://data.lobsterdata.com/info/DataStructure.php

## Turbulence-state options

### Option A: price-space k and epsilon

Use `k` as tick squared per second squared and `epsilon` as tick squared per second cubed.

Recommendation: choose this for internal TRIDENT consistency because it makes `nu_t = C_mu k^2 / epsilon` have units of tick squared per second, matching the diffusion terms. Source: OpenFOAM k-epsilon documentation for the physical dimensional relationship among k, epsilon, and eddy viscosity, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/

### Option B: return-space k and epsilon

Use `k` as squared return per second squared and `epsilon` as squared return per second cubed.

Recommendation: allow this only as a normalized reporting feature, because book replay, depth density, and execution kernels require a tick-space grid. Sources: Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

## Modeling options

### Option A: Phase 1 feature proxy model

Compute features such as spread, depth, OFI proxy, realized volatility proxy for `k`, volatility decay proxy for `epsilon`, fragility, and market Reynolds number.

Recommendation: choose this for Phase 1 because L1, trade, and bar data support the inputs and because OFI over depth is a strong simple baseline. Sources: Cont, Kukanov, and Stoikov, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822; Databento schemas, https://databento.com/docs/knowledge-base/new-users/market-data-schemas

### Option B: Full PDE or SPDE solver

Estimate full price-level fields and solve the coupled TRIDENT equations.

Recommendation: defer this to Phase 2 after event replay exists, because the source, cancellation, and execution terms are not observable from bars alone. Source: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php

### Option C: Latent interface model only

Estimate latent slope `L`, impact, and interface motion without full visible book dynamics.

Recommendation: keep this as a research branch, not the main Phase 1 path, because latent-order-book square-root impact is a useful limit but does not replace visible order-flow baselines. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Cont, Kukanov, and Stoikov, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822

