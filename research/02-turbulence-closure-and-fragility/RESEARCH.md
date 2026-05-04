# Research

## Scope

This is Phase 0 research for turbulence closure and fragility. It does not propose production code, live trading, broker integration, or profitability claims. The Phase 1 shape is a CPU-only feature pipeline with ticks as the internal book coordinate. Full source and sink validation needs L2 or L3 data. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Can k, epsilon, and nu_t be estimated from market data?

Recommendation: Treat `k` as an observable proxy for local market turbulent energy, not as a physical kinetic energy quantity. Estimate it from realized tick variance, quote-revision variance, or residual volatility after simple microstructure controls, because realized volatility is a model-free high-frequency variance estimator and OFI plus depth are known short-horizon price-pressure controls. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418, https://arxiv.org/abs/1011.6402.

Recommendation: Treat `epsilon` as an observable proxy for dissipation or shock absorption, not as a directly measured physical dissipation rate. Estimate it from post-shock decay of `k`, spread recovery, depth recovery, or the residual needed to balance a simplified `k` equation, because limit order book resiliency is commonly studied through recovery after liquidity shocks. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

Recommendation: Compute `nu_t = C_mu k^2 / (epsilon + epsilon_0)` as a derived eddy-diffusivity closure in Phase 1, not as a separately identified parameter. The k-epsilon closure defines turbulent viscosity from `k` and `epsilon`, while market data without L2 or L3 book gradients cannot identify both base diffusion and turbulent diffusion. Sources: https://www.openfoam.com/documentation/guides/v2112/doc/guide-turbulence-ras-realizable-k-epsilon.html, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://lobster-data.de/info/DataStructure.php.

Recommendation: Do not claim that market `k`, `epsilon`, or `nu_t` are physically equivalent to fluid turbulence. Use the analogy as an empirical closure hypothesis that must beat GARCH, stochastic volatility, realized volatility, OFI, VPIN-like, and Hawkes baselines out of sample. Sources: https://doi.org/10.1016/0045-7825(74)90029-2, https://doi.org/10.1016/0304-4076(86)90063-1, https://doi.org/10.1198/073500102753410408, https://doi.org/10.1093/rfs/hhs053, https://arxiv.org/abs/1502.04592.

## Proposed k estimators

Recommendation: Use realized tick variance intensity as the default Phase 1 `k` estimator:

```text
k_rv(t, h) = sum_{i in window(t,h)} [Delta mid_ticks_i]^2 / h
```

This uses ticks squared per second squared when tick moves are divided by event or wall-clock time. It is simple, CPU-only, and point-in-time if the window ends at decision time. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md.

Recommendation: Add a quote-motion `k` estimator when top-of-book or depth data is available:

```text
k_quote(t, h) = 0.5 * weighted_var(u_bid, u_ask)
```

where quote velocities are measured in ticks per second and weights can use visible depth. This better matches the model's quote momentum variables than trade-only realized volatility. Sources: https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobster-data.de/info/DataStructure.php, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Recommendation: Add a residual-energy `k` estimator for research comparison:

```text
k_resid(t, h) = variance(residual return after OFI, spread, depth, and seasonality controls)
```

This asks whether TRIDENT captures unexplained turbulence after the strongest simple microstructure controls. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1080/713665670.

## Proposed epsilon estimators

Recommendation: Use a decay-rate estimator as the default Phase 1 `epsilon` proxy. Detect local shocks in `k`, fit a one-sided exponential decay over future-free windows that end at the current timestamp, and set:

```text
epsilon_decay(t) = max(lambda_decay(t) * k(t), epsilon_floor)
```

This makes high dissipation correspond to fast volatility decay and low dissipation correspond to persistence. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e, https://doi.org/10.1111/1468-0262.00418.

Recommendation: Use depth and spread recovery estimators as L1 or L2 alternatives:

```text
epsilon_depth(t) = k(t) / tau_depth_recovery(t)
epsilon_spread(t) = k(t) / tau_spread_recovery(t)
```

where recovery time is the trailing estimate of how quickly top depth refills or spread returns after shocks. This aligns `epsilon` with order book resiliency rather than return volatility alone. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Recommendation: Use a closure-residual estimator only when L2 or L3 data is available:

```text
epsilon_balance = positive_part(P_k + diffusion_proxy - Delta k / Delta t)
```

This is closer to the model equation, but it needs price-level fields, gradients, and event accounting, which are not available from bars alone. Sources: https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://databento.com/docs/schemas-and-data-formats, https://lobster-data.de/info/DataStructure.php.

## Fragility

Recommendation: Define Phase 1 fragility as:

```text
fragility(t) = k(t)^2 / (epsilon(t) + epsilon_0)
```

and report a normalized percentile within symbol, venue, time-of-day bucket, and horizon. Raw values are unit-sensitive, while percentiles make stress comparisons more stable across symbols. Sources: https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://doi.org/10.1111/1468-0262.00418, https://arxiv.org/abs/1011.6402.

Recommendation: Track depth-adjusted fragility as a secondary feature:

```text
depth_fragility(t) = fragility(t) / (D_top(t) + D_star)
```

because the same turbulence state should matter more when visible depth is thin. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1016/j.jedc.2015.09.012.

## Turbulence production terms

Recommendation: Estimate imbalance production with:

```text
P_imbalance = C_I * I^2 / (D_top + D_star)^2
```

where `I` is signed aggressive imbalance or OFI proxy. This is the most practical Phase 1 production term because OFI and depth are observable from top-of-book data. Sources: https://arxiv.org/abs/1011.6402, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Recommendation: Estimate liquidity withdrawal production with:

```text
P_withdrawal = C_c * abs(Delta log(D_top + D_star) / Delta t)^2
```

or, with L3 data, from cancellation intensity near the touch. This maps sudden depth loss into turbulence production and should be tested against resiliency baselines. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://lobster-data.de/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats.

Recommendation: Estimate quote-shear production only with L2 or L3 data:

```text
P_shear = C_u * sum_s sum_l q_s(l,t) * [Delta_p u_s(l,t)]^2
```

This is closest to the turbulence analogy but needs multiple price levels and quote revision velocities. Sources: https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobster-data.de/info/DataStructure.php.

Recommendation: Estimate news production as:

```text
P_news = C_N * N_t^2
```

when timestamped news, scheduled events, relevance, sentiment, and novelty scores are available. Keep it optional in Phase 1 because the data vendor decision has not approved a primary news archive. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, https://www.nyse.com/markets/hours-calendars.

## Baseline comparison

Recommendation: Compare TRIDENT `k` against realized volatility first. Realized volatility is the closest nonparametric benchmark and should be difficult to beat for volatility measurement. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418.

Recommendation: Compare TRIDENT `k` and `epsilon` against GARCH because GARCH directly models volatility clustering with a small parametric recursion. TRIDENT should be rejected for Phase 1 prediction if it adds no incremental signal beyond GARCH and realized volatility. Sources: https://doi.org/10.1016/0304-4076(86)90063-1, https://www.nber.org/papers/w8160.

Recommendation: Compare against stochastic volatility models as latent-state volatility baselines. Stochastic volatility is conceptually closer to TRIDENT than GARCH because volatility is an unobserved state, but TRIDENT is unique only if its dissipation and production terms add microstructure structure beyond a latent variance process. Sources: https://doi.org/10.2307/2297980, https://doi.org/10.1198/073500102753410408, https://academic.oup.com/book/51972.

Recommendation: Compare against VPIN-like flow toxicity because fragility should overlap with toxic order-flow imbalance but should not reduce to it. TRIDENT is useful only if `k^2 / epsilon` predicts jumps, spread widening, or impact after controlling for VPIN-like measures. Sources: https://doi.org/10.1093/rfs/hhs053, https://pinstimation.com/reference/reference/vpin.html.

Recommendation: Compare against Hawkes intensity models when event-level data is available. Hawkes models capture endogenous event clustering; TRIDENT production terms must add useful information about absorption and fragility rather than merely rediscovering self-excitation. Sources: https://arxiv.org/abs/1502.04592, https://doi.org/10.1142/S2382626615500057.

## Falsifiable predictions unique to TRIDENT

Prediction 1: For the same realized volatility, OFI, spread, and top-of-book depth, higher `k^2 / epsilon` predicts a higher probability of local jumps and spread widening over the next short horizon. This is unique because realized volatility and GARCH do not separate turbulent energy from dissipation. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1016/0304-4076(86)90063-1, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Prediction 2: For the same signed aggressive imbalance and depth, higher `nu_t` predicts larger price impact. This is unique because OFI models condition impact mainly on imbalance and depth, while TRIDENT adds eddy diffusivity as a usable-liquidity reducer. Sources: https://arxiv.org/abs/1011.6402, https://arxiv.org/abs/1412.0141, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Prediction 3: After a shock, markets with high `k` and high `epsilon` should revert spread and depth faster than markets with high `k` and low `epsilon`. This is unique because raw realized volatility treats both states as similarly volatile. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e, https://doi.org/10.1111/1468-0262.00418.

Prediction 4: A production decomposition should identify different stress types. Imbalance-driven production should precede directional moves, withdrawal production should precede spread widening and depth loss, quote-shear production should precede level migration, and news production should precede cross-symbol volatility bursts. Sources: https://arxiv.org/abs/1011.6402, https://arxiv.org/abs/1502.04592, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

## Open questions

The largest uncertainty is whether `epsilon` can be estimated robustly from L1 data. Depth and spread recovery are plausible, but they may measure market maker behavior, exchange rules, or time-of-day seasonality more than dissipation.

It is unclear whether `nu_t` can be identified separately from base diffusion without L2 or L3 price-level gradients. Phase 1 should report it as a derived proxy.

It is unclear whether fragility is a universal variable or symbol-specific. Normalized percentiles may be required before cross-symbol comparison.

It is unclear whether news production can be separated from endogenous Hawkes-like event excitation without high-quality timestamped news and event-stream data.

It is unclear whether TRIDENT variables will add signal outside stress regimes. They may be useful only during liquidity withdrawal, volatility bursts, and scheduled-event windows.
