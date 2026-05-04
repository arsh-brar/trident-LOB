# Validation

## Validation stance

Recommendation: Validate TRIDENT turbulence variables as candidate research features, not as proven physics and not as trading rules. They must pass leakage checks, baseline comparisons, robustness checks, and falsifiable prediction tests before later engineering work depends on them. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://doi.org/10.1080/713665670, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Data validation

Recommendation: Require monotonic timestamps, no future features, valid tick size, nonnegative sizes, nonnegative `k`, positive `epsilon`, nonnegative `nu_t`, and explicit quality flags. Sources: https://databento.com/docs/knowledge-base/new-users/market-data-schemas, https://lobster-data.de/info/DataStructure.php, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

Recommendation: Validate all feature windows as closed on or before `decision_ts`. Recovery estimators for `epsilon` must use historical estimates of recovery behavior, not actual future recovery after the decision timestamp. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Recommendation: Validate L2 and L3 book fields against event accounting before using quote-shear or closure-residual estimators. Full source and sink tests require add, cancel, modify, execution, and book state records. Sources: https://lobster-data.de/info/DataStructure.php, https://databento.com/docs/schemas-and-data-formats, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

## Estimator validation

Recommendation: Test `k` estimators by comparing realized tick variance, quote-motion variance, and residual energy against next-horizon realized variance and jump outcomes. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418, https://arxiv.org/abs/1011.6402.

Recommendation: Test `epsilon` estimators by measuring whether higher `epsilon` predicts faster subsequent normalization of volatility, spread, and depth after comparable shocks. Sources: https://doi.org/10.1016/j.jedc.2015.09.012, https://doi.org/10.1088/1742-5468/aa7a3e.

Recommendation: Test `nu_t` only as a derived feature in Phase 1. Do not validate it as an independently identified market diffusivity until L2 or L3 gradients and flux proxies are available. Sources: https://www.openfoam.com/documentation/guides/v2112/doc/guide-turbulence-ras-realizable-k-epsilon.html, https://databento.com/docs/schemas-and-data-formats/mbp-10, https://lobster-data.de/info/DataStructure.php.

Recommendation: Test fragility in both raw and percentile form. Percentile form should be grouped by symbol, horizon, venue, and time-of-day bucket. Sources: https://doi.org/10.1080/713665670, https://doi.org/10.1111/1468-0262.00418.

## Baseline gates

Recommendation: Require TRIDENT features to beat or add statistically meaningful incremental signal over realized volatility for volatility and jump targets. Sources: https://www.nber.org/papers/w8160, https://doi.org/10.1111/1468-0262.00418.

Recommendation: Require TRIDENT features to beat or add incremental signal over GARCH forecasts for volatility clustering targets. Sources: https://doi.org/10.1016/0304-4076(86)90063-1, https://www.nber.org/papers/w8160.

Recommendation: Require comparison with stochastic volatility when latent-state modeling is introduced. TRIDENT must justify its added production and dissipation structure. Sources: https://doi.org/10.1198/073500102753410408, https://doi.org/10.2307/2297980.

Recommendation: Require OFI, spread, and depth controls in all short-horizon price-impact and direction tests. Sources: https://arxiv.org/abs/1011.6402, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Recommendation: Require VPIN-like controls for toxicity comparisons when trade signs and volume buckets are available. Sources: https://doi.org/10.1093/rfs/hhs053, https://pinstimation.com/reference/reference/vpin.html.

Recommendation: Require Hawkes intensity baselines when event-level streams are available. Sources: https://arxiv.org/abs/1502.04592, https://doi.org/10.1142/S2382626615500057.

## Falsification tests

Test 1: At fixed realized volatility, OFI, spread, depth, event intensity, and time-of-day controls, high fragility must predict higher next-horizon jump probability or spread widening. Failure condition: fragility has no stable out-of-sample incremental effect.

Test 2: At fixed signed flow and visible depth, high `nu_t` must predict larger realized impact. Failure condition: the effect disappears after OFI and depth controls.

Test 3: High `k` with high `epsilon` must recover faster than high `k` with low `epsilon` after comparable shocks. Failure condition: `epsilon` does not rank recovery speed out of sample.

Test 4: Production terms must specialize. Imbalance production should forecast directional pressure, withdrawal production should forecast liquidity loss, shear production should forecast quote-level migration, and news production should forecast externally synchronized bursts. Failure condition: production decomposition is interchangeable noise.

Sources for these tests: https://arxiv.org/abs/1011.6402, https://www.nber.org/papers/w8160, https://doi.org/10.1016/j.jedc.2015.09.012, https://arxiv.org/abs/1502.04592, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

## Robustness checks

Recommendation: Run walk-forward or blocked time splits by date, symbol, and regime. Do not shuffle event rows across time. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://doi.org/10.1080/713665670.

Recommendation: Test multiple horizons, including event-time, 1 minute, and 5 minute targets, but select horizons before final evaluation to reduce data-mining risk. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Recommendation: Report performance separately for normal regimes, liquidity-withdrawal regimes, scheduled-event windows, and high-volatility regimes. TRIDENT may be stress-specific, and pooled averages can hide that. Sources: https://doi.org/10.1080/713665670, https://doi.org/10.1016/j.jedc.2015.09.012.

Recommendation: Run ablations for each production term and for `k`, `epsilon`, and fragility separately. Sources: https://arxiv.org/abs/1011.6402, https://doi.org/10.1016/0304-4076(86)90063-1.

## Acceptance criteria

Recommendation: Accept Phase 1 turbulence proxies only if they are point-in-time safe, stable under reasonable parameter perturbations, nonnegative where required, and incrementally useful over the baseline stack for at least one predeclared target. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/, https://arxiv.org/abs/1011.6402.

Recommendation: Reject or quarantine a turbulence proxy if it depends on future recovery, revised data, unstable denominators, symbol-specific overfitting, or unexplainable sensitivity to `epsilon_0`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Open questions

What is the least leaky way to estimate `epsilon_decay` in real time?

Should `epsilon_floor` be a fixed tick-unit constant, a symbol percentile, or a function of quote frequency?

Should fragility be compared across symbols only through percentiles?

How should hidden liquidity be handled in withdrawal and impact tests?

Can Hawkes residuals help separate endogenous excitation from TRIDENT production?
