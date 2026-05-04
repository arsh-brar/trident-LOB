# Options

## Option A: Minimal L1 proxy closure

Recommendation: Use Option A as the default Phase 1 starting point. Estimate `k` from realized tick variance, `epsilon` from trailing volatility decay or spread recovery, `fragility = k^2 / (epsilon + epsilon_0)`, and imbalance production from OFI over depth. This option fits the CPU-only feature pipeline and can run on bars, trades, and top-of-book quotes. Sources: https://www.nber.org/papers/w8160, https://arxiv.org/abs/1011.6402, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Strengths: It is simple, point-in-time, cheap to compute, and testable against strong baselines.

Weaknesses: It cannot validate full source and sink terms, cannot estimate quote shear across price levels, and cannot identify `nu_t` separately from the closure formula.

Use when: Phase 1 needs an auditable first feature set on Mac M3 CPU.

## Option B: L2 depth-field closure

Recommendation: Use Option B for serious model validation after a small L2 sample is available. Estimate price-level depth fields, quote velocities, withdrawal production, and partial quote-shear production across visible levels. Sources: https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobster-data.de/info/DataStructure.php, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

Strengths: It moves closer to the actual TRIDENT closure because `q_s(p,t)` and price-level gradients become observable over the top levels.

Weaknesses: L2 aggregates orders by price and may not fully separate adds, cancels, modifies, hidden executions, and queue priority.

Use when: The research needs to test whether quote shear and depth withdrawal explain future spread, depth, and price impact beyond L1 features.

## Option C: L3 event-replay closure

Recommendation: Use Option C only for full source, sink, and closure validation. Estimate event-level `lambda_s`, cancellation sinks, execution sinks, queue updates, price-level fields, and closure residuals from reconstructed book events. Sources: https://lobster-data.de/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

Strengths: It is the only option that can test the reaction-diffusion accounting identities directly.

Weaknesses: It is paid or access-constrained for US equities, more complex, and outside the first lightweight Phase 1 path.

Use when: The project needs to determine whether TRIDENT is a real order-book field model rather than a feature analogy.

## Option D: State-space turbulence closure

Recommendation: Defer Option D until Options A and B produce incremental evidence. A state-space model could estimate latent `k`, `epsilon`, production coefficients, and observation noise jointly, but this adds complexity before the simple baselines are exhausted. Sources: https://doi.org/10.1198/073500102753410408, https://doi.org/10.2307/2297980, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Strengths: It handles noisy observations and latent states in a coherent statistical model.

Weaknesses: It is slower, harder to validate, and risks fitting the turbulence analogy instead of testing it.

Use when: A simple feature pipeline shows stable incremental signal and the project needs parameter uncertainty.

## Option E: Hawkes-first event model

Recommendation: Treat Hawkes models as benchmarks, not the primary Phase 1 turbulence estimator. Hawkes intensity models are excellent for event clustering, but they do not by themselves define dissipation, eddy diffusivity, or fragility. Sources: https://arxiv.org/abs/1502.04592, https://doi.org/10.1142/S2382626615500057, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md.

Strengths: It is a strong event-stream benchmark for clustered market orders, limit orders, and cancellations.

Weaknesses: It needs event data and may explain stress as excitation without measuring absorption capacity.

Use when: L2 or L3 event streams are available and TRIDENT production terms need a serious endogenous-clustering competitor.

## Comparison

Recommendation: Select Option A for Phase 1, prepare interfaces compatible with Options B and C, and defer Options D and E to validation stages. This respects CPU-only development, simple baselines first, and the Wave 1 decision that full source and sink validation needs L2 or L3. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/01-equation-audit-and-dimensional-analysis/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.
