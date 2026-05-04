# Options

## Option A: Full latent order book reconstruction from L2 or L3

Estimate visible cumulative depth by tick distance from the midprice, fit local slopes on both sides, and use event replay to estimate arrivals, cancellations, executions, and quote revisions.

Recommendation: Use this option for full TRIDENT verification, not Phase 1 default, because source and sink accounting requires L2 or L3 data. Sources: https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities.

Strengths:

- Closest to the reaction-diffusion model.
- Supports slope `L`, source terms, sink terms, queue depletion, and replenishment tests.
- Allows visible-depth tests against latent-liquidity assumptions.

Limits:

- Requires paid or academic L2/L3 data.
- More expensive and slower than Phase 1 CPU-only feature tests.
- Still does not reveal all hidden liquidity.

## Option B: Top-of-book interface proxy

Use best bid, best ask, quoted sizes, spread, OFI, signed trades if available, realized volatility, and TRIDENT turbulence proxies.

Recommendation: Choose this as the Phase 1 default when quotes are available, because OFI and top-book depth are literature-supported short-horizon price-pressure baselines and can run CPU-only on a Mac M3. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://academic.oup.com/jfec/article/12/1/47/816163.

Define:

```text
P_t = midprice in ticks
s_t = spread in ticks
D_h = harmonic_mean(best_bid_size, best_ask_size)
L_proxy = 2 * D_h / max(s_t, 1)
Phi_hat(p,t) = L_proxy * (p - P_t) - B_hat_t
```

Use:

```text
B_hat_t = a_1 * OFI_rate_t
        + a_2 * signed_trade_rate_t
        + a_3 * queue_imbalance_t
        + a_4 * news_score_t
```

Strengths:

- Uses point-in-time quote data.
- Aligns with Wave 1 Phase 1 data decisions.
- Can be compared directly against OFI and depth baselines.

Limits:

- `L_proxy` is not identified latent liquidity.
- No direct observation of depth away from best quote.
- No full source/sink validation.

## Option C: Bars-only impact proxy

Use OHLCV bars, returns, volume, volatility, optional signed volume proxy, and optional news. Estimate inverse-impact or liquidity-cost controls.

Recommendation: Allow this only as a weak fallback when quote data is absent, because bars can support realized-volatility and liquidity-cost proxies but cannot reconstruct the latent book or top-of-book queue pressure. Sources: https://doi.org/10.1111/j.1540-6261.2009.01469.x, https://lobsterdata.com/info/DataStructure.php.

Possible proxy:

```text
L_bar_proxy = rolling_robust_median(2 * abs(Q_proxy) / max(DeltaP_ticks^2, P_floor^2))
```

If no signed flow exists:

```text
illiquidity_proxy = abs(return) / dollar_volume
```

Strengths:

- Cheap and easy to compute.
- Useful for broad symbol screening.
- Fits CPU-only Phase 1 constraints.

Limits:

- Directional pressure is weak unless signed trades are available.
- Queue mechanics are missing.
- Latent liquidity slope is not identified.

## Option D: Structural reaction-diffusion calibration

Calibrate a diffusion-reaction latent book with replenishment, cancellation, diffusion, and market-order forcing.

Recommendation: Defer this option until after Phase 1 baselines pass, because the literature model is useful but Phase 1 should prefer simple baselines before complex models. Sources: https://arxiv.org/abs/1412.0141, https://doi.org/10.1080/14697680903373692.

Strengths:

- Best theoretical match to the model specification.
- Can generate impact trajectories for interrupted, reversed, or extended metaorders.
- Can be checked against no-manipulation constraints.

Limits:

- Needs stronger data and calibration discipline.
- Parameters may not be identifiable from bars or top-of-book quotes.
- Higher risk of overfitting.

## Option E: Hybrid empirical interface model

Estimate `Phi_hat` as a local feature map with `L_proxy` and `B_hat`, then test whether nonlinear impact and turbulence amplification improve out-of-sample prediction.

Recommendation: Use this as the Phase 1 research design, with Option B as the default data mode and Option C as fallback, because it preserves the TRIDENT interface idea while keeping the first implementation simple and falsifiable. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Core comparison:

```text
Baseline 1: DeltaP ~ OFI / depth
Baseline 2: DeltaP ~ spread + depth + volume + realized_volatility
TRIDENT 1: DeltaP ~ B_hat / L_proxy
TRIDENT 2: DeltaP ~ sqrt(abs(Q_proxy) / L_proxy)
TRIDENT 3: DeltaP ~ sqrt(abs(Q_proxy) / L_proxy) * turbulence_amplifier
```

## Open questions

Which symbols and horizons have enough top-of-book activity for stable `L_proxy`?

How should odd lots and hidden liquidity be handled when best quote sizes understate available liquidity?

Should `L_proxy` be learned as a calibrated scale multiplier per symbol, per spread regime, or per volatility regime?

Does the bars-only fallback create too much measurement error for useful interface tests?
