# Market Microstructure Options

## Option A: Source-Sink Baseline

Model visible liquidity with simple limit order arrivals, cancellations, and executions, using spread, depth, and realized volatility as controls.

Recommendation: Implement this as the first benchmark because zero-intelligence and stochastic LOB models show that simple order submission, cancellation, and execution mechanisms can reproduce important spread and depth behavior. Sources: Smith et al., https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio; Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.

Pros:

- Simple and CPU-friendly for Apple Silicon M3.
- Compatible with bars, top-of-book quotes, and event-level data.
- Gives a conservative baseline before claiming value from turbulence variables.

Cons:

- Misses event clustering unless extended.
- Does not directly represent latent liquidity.
- May underfit stress regimes where cancellation and execution intensities change quickly.

## Option B: Queue-Reactive Event Layer

Estimate event probabilities as functions of best bid and best ask queue sizes, spread, and recent event state.

Recommendation: Use this as the main Phase 2 queue baseline when event data exists, because queue-reactive models condition event intensities on queue state and are empirically aligned with LOB mechanics. Source: Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563.

Pros:

- Strong microstructure fit near the touch.
- Maps cleanly to depletion risk and short-horizon price moves.
- Works with shallow L2 and full L3 replay.

Cons:

- Needs higher-quality event data than bars.
- Does not by itself explain latent liquidity or impact concavity.
- Calibration can be symbol and regime dependent.

## Option C: OFI-Centered Phase 1 Feature Model

Use OFI, spread, top-book depth, realized volatility, and TRIDENT fragility variables as Phase 1 features for next-horizon prediction tasks.

Recommendation: Make OFI a required baseline feature before judging TRIDENT-specific variables, because OFI is a documented short-horizon price-change explanatory variable. Source: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402.

Pros:

- Practical with top-of-book data.
- Easy to compare against logistic regression, ridge regression, and gradient-boosted baselines.
- Directly tests whether `k`, `epsilon`, and `k^2 / epsilon` add incremental signal.

Cons:

- OFI proxies from bars are weaker than quote-derived OFI.
- Does not estimate full source and sink terms.
- Feature results must be out-of-sample and transaction-cost-aware before any trading interpretation.

## Option D: Hawkes Event-Clustering Layer

Fit self-exciting and cross-exciting point processes for limit orders, cancellations, market orders, quote changes, and news shocks.

Recommendation: Treat Hawkes models as a Phase 2 benchmark for clustered event flow, because finance event data often exhibits self-excitation and cross-excitation. Sources: Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592; Bowsher, https://doi.org/10.1016/j.jeconom.2006.11.007.

Pros:

- Explicit model for clustered activity.
- Natural bridge to shock decay and endogenous activity.
- Can benchmark TRIDENT turbulence production terms.

Cons:

- Event-level calibration can be computationally heavier.
- Kernel choice and stationarity assumptions matter.
- May be excessive for Phase 1 CPU-only work.

## Option E: Latent Order Book Interface

Estimate an unobserved latent buy-sell pressure field and define midprice as the interface where latent imbalance crosses zero.

Recommendation: Keep this as the conceptual spine of TRIDENT but initially estimate only coarse proxies, because latent liquidity is not directly observed and should be validated through impact and reversal behavior. Source: Donier et al., https://arxiv.org/abs/1412.0141.

Pros:

- Closest match to the TRIDENT model specification.
- Supports square-root impact logic.
- Separates displayed liquidity from true market intention.

Cons:

- Requires careful identifiability assumptions.
- Easy to overfit with flexible state estimates.
- Needs impact and replay validation before being trusted.

## Option F: Turbulence-Closure Feature Layer

Estimate `k` from realized volatility or event intensity, estimate `epsilon` from volatility decay or resilience, and use `k^2 / epsilon` as fragility.

Recommendation: Use this as the first original TRIDENT contribution, but test it only as an incremental feature over source-sink, OFI, and volatility baselines. Sources for required baselines and stylized facts: Cont, https://doi.org/10.1080/713665670; Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402; Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.

Pros:

- CPU-friendly in Phase 1.
- Directly operationalizes the TRIDENT hypothesis.
- Can be evaluated with simple out-of-sample tests.

Cons:

- Turbulence analogy is original and uncertain in this domain.
- Proxy choice for `epsilon` may dominate results.
- Needs stress-regime validation to avoid spurious signal.

## Recommended Phase 0 Ordering

1. Source-sink and OFI baselines first, because simple baselines are required by repo policy and supported by zero-intelligence and OFI literature. Sources: Smith et al., https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio; Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402.
2. Add TRIDENT `k`, `epsilon`, and fragility proxies next, because the research question is whether they improve out-of-sample behavior over known microstructure variables. Sources: Cont stylized facts, https://doi.org/10.1080/713665670; TRIDENT model specification, ../../docs/TRIDENT_LOB_MODEL.md.
3. Add queue-reactive and Hawkes benchmarks only when L2 or L3 event data is available, because they require event-state information that bars cannot provide reliably. Sources: Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563; Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592.
4. Validate latent-interface and impact claims against square-root impact before using them in any simulated execution study. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Toth et al., https://doi.org/10.1103/PhysRevX.1.021006; Gatheral, https://doi.org/10.1080/14697680903373692.
