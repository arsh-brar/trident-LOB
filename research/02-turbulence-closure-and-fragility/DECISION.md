# Decision

## Phase 1 turbulence decision

Recommendation: Phase 1 should implement a CPU-only turbulence feature pipeline, not a full turbulence PDE solver and not trading code. The pipeline should compute point-in-time proxies for `k`, `epsilon`, `nu_t`, fragility, and production terms, then evaluate them against baseline features and models. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://www.nber.org/papers/w8160.

## Chosen estimators

Recommendation: Use realized tick variance intensity as the default `k` estimator:

```text
k = sum(Delta mid_ticks^2) / window_seconds
```

Use quote-motion and residual-energy alternatives as research comparisons when quote data is available. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Recommendation: Use volatility decay as the default `epsilon` estimator:

```text
epsilon = max(lambda_decay * k, epsilon_floor)
```

Use spread recovery, depth recovery, and closure residual alternatives as data permits. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

Recommendation: Compute `nu_t` only as a derived closure:

```text
nu_t = C_mu * k^2 / (epsilon + epsilon_0)
```

Do not claim independent identification of `nu_t` until L2 or L3 data supports book gradients and flux tests. Sources: https://www.openfoam.com/documentation/guides/v2112/doc/guide-turbulence-ras-realizable-k-epsilon.html, https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobster-data.de/info/DataStructure.php.

Recommendation: Define fragility as:

```text
fragility = k^2 / (epsilon + epsilon_0)
```

Report raw, clipped, and within-symbol percentile versions. Percentiles should be grouped by horizon and time-of-day bucket to reduce seasonality artifacts. Sources: https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1080/713665670.

## Production terms

Recommendation: Include imbalance production in Phase 1:

```text
P_imbalance = C_I * I^2 / (D_top + D_star)^2
```

This is the first production term because OFI and depth are strong, observable microstructure controls. Sources: https://arxiv.org/abs/1011.6402, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Recommendation: Include withdrawal production in Phase 1 when top depth is available:

```text
P_withdrawal = C_c * abs(Delta log(D_top + D_star) / Delta t)^2
```

This captures rapid visible-liquidity loss and should be tested against spread and depth recovery. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e.

Recommendation: Defer quote-shear production to L2 or L3:

```text
P_shear = C_u * sum_s sum_l q_s(l,t) * [Delta_p u_s(l,t)]^2
```

This term needs multiple price levels and quote-revision velocities. Sources: https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobster-data.de/info/DataStructure.php, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

Recommendation: Keep news production optional:

```text
P_news = C_N * N_t^2
```

It requires timestamped, point-in-time news and scheduled-event data. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://www.nyse.com/markets/hours-calendars.

## Baseline decision

Recommendation: The required baseline stack is realized volatility, GARCH, stochastic volatility, OFI and depth, VPIN-like flow toxicity, and Hawkes intensity when event data is available. TRIDENT variables must be evaluated as incremental features over those baselines. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1016/0304-4076(86)90063-1, https://doi.org/10.1198/073500102753410408, https://arxiv.org/abs/1011.6402, https://doi.org/10.1093/rfs/hhs053, https://arxiv.org/abs/1502.04592.

## Unique TRIDENT claims to test

Recommendation: Accept TRIDENT turbulence closure only if at least one falsifiable prediction survives leakage checks, time splits, transaction-cost-aware backtest analysis if used later, and baseline comparison. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://doi.org/10.1080/713665670, https://arxiv.org/abs/1011.6402.

Falsifiable prediction 1: At fixed realized volatility, OFI, spread, depth, time of day, and event intensity, high fragility predicts higher next-horizon jump probability and spread widening.

Falsifiable prediction 2: At fixed order-flow imbalance and depth, high `nu_t` predicts larger realized impact for the same signed flow.

Falsifiable prediction 3: High `k` with high `epsilon` predicts faster recovery than high `k` with low `epsilon`.

Falsifiable prediction 4: Production decomposition predicts stress type: imbalance production predicts directional pressure, withdrawal production predicts liquidity loss, shear production predicts quote-level migration, and news production predicts externally synchronized bursts.

## Non-decisions

This decision does not approve live trading, broker routing, paid data purchase, production ingestion, or profitability claims.

This decision does not choose universal thresholds for fragility or market Reynolds number. Thresholds must be learned and validated by symbol, horizon, venue, and regime.

This decision does not claim that market turbulence variables are physical fluid variables. They are empirical analogues.

## Open questions

Can `epsilon` estimated from L1 volatility decay survive comparison with depth-recovery and spread-recovery estimators?

Can `nu_t` add predictive signal after controlling for realized volatility and OFI, or is it just a nonlinear transform of them?

How stable are `C_mu`, `epsilon_0`, and production coefficients across symbols and horizons?

Can news production be separated from Hawkes-like endogenous excitation?

Are TRIDENT variables useful in ordinary regimes, or only around shocks and liquidity withdrawal?
