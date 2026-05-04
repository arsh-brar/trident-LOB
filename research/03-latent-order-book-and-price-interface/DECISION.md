# Decision

## Phase 1 decision

Use a hybrid empirical price-interface model for Phase 1. The default data mode is top-of-book quotes plus trades when available. Bars-only mode is allowed as a fallback, but all bars-only latent-liquidity outputs must be labeled nonstructural proxies.

Recommendation: Choose the top-of-book interface proxy for Phase 1 because it is CPU-only, uses point-in-time data, respects the Wave 1 decision that full source/sink validation needs L2/L3, and compares directly with OFI and depth baselines. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://academic.oup.com/jfec/article/12/1/47/816163, https://lobsterdata.com/info/DataStructure.php.

## Accepted definitions

Use ticks as the internal price coordinate.

```text
P_t = midprice in ticks
Phi(p,t) = ell_plus(p,t) - ell_minus(p,t)
Phi(P_t,t) = 0
L_t = partial_p Phi(P_t,t)
```

Recommendation: Keep `Phi(P_t,t) = 0` as the central price-interface definition because it matches the TRIDENT model and the latent order book reaction-diffusion literature. Sources: https://arxiv.org/abs/1412.0141, https://doi.org/10.1080/14697688.2015.1040056.

Near the interface:

```text
Phi_hat(p,t) = L_hat_t * (p - P_t) - B_hat_t
```

The implied one-step movement equation is:

```text
Delta P_hat_{t,h} = h * R_hat_{t,h} / (L_hat_t + L_floor)
```

where:

```text
R_hat_{t,h} ~= - partial_t Phi(P_t,t)
```

For metaorder-style impact tests:

```text
I_hat(Q,t) = sign(Q) * sqrt(2 * abs(Q) / (L_hat_t + L_floor))
```

Recommendation: Use the linear interface equation for short-horizon directional prediction and the square-root equation for impact-scaling validation, because both follow from a locally linear latent book but answer different empirical questions. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://arxiv.org/abs/1412.0141.

## Phase 1 approximation for L

With top-of-book quotes:

```text
D_h = harmonic_mean(best_bid_size, best_ask_size)
s   = max(spread_ticks, 1)
L_hat_t = 2 * D_h / s
```

Recommendation: Use this as `L_L1_proxy`, not as identified latent liquidity, because top-of-book quotes do not show depth away from the best quote or hidden liquidity. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

With bars only:

```text
L_hat_t = rolling robust inverse-impact proxy
```

A possible form is:

```text
L_hat_t = median_window(2 * abs(Q_proxy) / max(DeltaP_ticks^2, P_floor^2))
```

Recommendation: Use bars-only `L_hat_t` only as a liquidity-control feature and never as a latent book estimate, because bars do not contain bid queue size, ask queue size, queue depletion, or quote updates. Sources: https://doi.org/10.1111/j.1540-6261.2009.01469.x, https://lobsterdata.com/info/DataStructure.php.

## Phase 1 approximation for Phi

With top-of-book quotes:

```text
B_hat_t = a_1 * OFI_rate_t
        + a_2 * signed_trade_rate_t
        + a_3 * queue_imbalance_t
        + a_4 * news_score_t
```

With bars only:

```text
B_hat_t = a_1 * signed_volume_proxy_t
        + a_2 * return_state_t
        + a_3 * volume_shock_t
        + a_4 * news_score_t
```

Recommendation: Fit `B_hat_t` only with features available at or before decision time, because the repo forbids future data and financial backtests are highly exposed to leakage and overfitting. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822.

## Turbulence-amplified impact decision

Test turbulence as an impact amplifier:

```text
F_t = k_t^2 / (epsilon_t + epsilon_0)
I_hat(Q,t,F) = sign(Q) * sqrt(2 * abs(Q) / (L_hat_t + L_floor))
               * (1 + theta_F * zscore(F_t))
```

Recommendation: Accept turbulence-amplified impact only if `theta_F > 0` is stable out of sample and improves prediction over OFI, spread, depth, volume, and realized-volatility controls. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Rejected for Phase 1

Reject full PDE solving in Phase 1. Recommendation: Defer full reaction-diffusion calibration until L2 or L3 data is available and simpler baselines are established. Sources: https://arxiv.org/abs/1412.0141, https://lobsterdata.com/info/DataStructure.php.

Reject live trading and live-trading enable flags. Recommendation: Keep this work research-only because the project hard rules and Wave 1 risk decision block live trading. Sources: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270, https://ecfr.io/Title-17/Section-240.15c3-5.

## Open questions

Should the top-of-book `L_L1_proxy` use harmonic mean depth, minimum depth, or side-specific depth based on the predicted move direction?

Should `Phi_hat` be calibrated globally, per symbol, or per symbol-regime?

How much of measured square-root impact is mechanical liquidity versus information in the trade sign?

Does turbulence amplification survive after controlling for spread widening and depth withdrawal?

What minimum quote quality is required before the interface proxy is trusted?
