# Research

## Scope

This Phase 0 note covers latent order book theory, reaction-diffusion market impact, the TRIDENT price interface, and Phase 1 approximations when only bars or top-of-book quotes are available. It does not authorize production code, paper trading code, or live trading code.

## Literature summary

Latent order book models treat supply and demand intentions as fields around the current price, not only as visible displayed depth. The key empirical and theoretical point is that average latent liquidity is small near the current price and grows away from it, producing a V-shaped supply-demand profile. Recommendation: TRIDENT should model latent sell minus latent buy pressure as a locally linear field near the midprice, because this is the minimal structure used to explain nonlinear impact and the square-root law. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://doi.org/10.1080/14697688.2015.1040056.

The Donier, Bonart, Mastromatteo, and Bouchaud model uses a latent order book inspired by diffusion-reaction dynamics. Latent intentions diffuse in price, are reassessed or cancelled, and are replenished away from the price. The transaction price is the interface where latent buy and sell pressure balance. Recommendation: TRIDENT should keep the price interface definition `Phi(P_t,t) = 0`, because it matches the model specification and the reaction-diffusion latent order book literature. Sources: https://arxiv.org/abs/1412.0141, https://doi.org/10.1080/14697688.2015.1040056.

Square-root impact follows when the latent book is locally linear. If the net executed signed quantity is `Q` and local latent liquidity slope is `L`, then the mechanical displacement needed to absorb the order scales as:

```text
Delta P ~= sign(Q) * sqrt(2 * abs(Q) / L)
```

This is a static interface approximation. It is not a profitability claim. Recommendation: TRIDENT validation should treat square-root impact as a required benchmark, not as a discovered result. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://arxiv.org/abs/1412.0141.

At short horizons, top-of-book order flow imbalance is a strong baseline. Cont, Kukanov, and Stoikov show that short-interval price changes are mainly driven by order flow imbalance at the best bid and ask, with a coefficient inversely related to market depth. Recommendation: Phase 1 price-interface tests must compare every latent-liquidity proxy against OFI, spread, depth, and realized volatility baselines. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://academic.oup.com/jfec/article/12/1/47/816163.

Impact models also need no-manipulation discipline. Gatheral shows that impact shape and impact decay cannot be chosen independently under no-dynamic-arbitrage constraints. Recommendation: TRIDENT should avoid calibrating a transient impact kernel that allows profitable round trips in simulation, even in research-only tests. Sources: https://doi.org/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1292353.

## TRIDENT interpretation

Use the model specification variables:

```text
ell_plus(p,t)  = latent sell intention
ell_minus(p,t) = latent buy intention
Phi(p,t)       = ell_plus(p,t) - ell_minus(p,t)
Phi(P_t,t)     = 0
```

Near the interface:

```text
Phi(p,t) ~= L_t * (p - P_t)
L_t = partial_p Phi(P_t,t)
```

Use ticks as the internal price coordinate, following the Wave 1 dimensional decision. Recommendation: `P_t`, `p`, and `Delta P` should be measured internally in ticks, with returns and basis points used only as normalized reporting views. Sources: https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

The interface movement equation follows by differentiating `Phi(P_t,t) = 0`:

```text
0 = partial_t Phi(P_t,t) + dot(P_t) * partial_p Phi(P_t,t)
dot(P_t) = - partial_t Phi(P_t,t) / L_t
```

For a finite horizon `h`, Phase 1 should use:

```text
Delta P_{t,h} = h * R_hat_{t,h} / (L_hat_t + L_floor) + error
R_hat_{t,h} ~= - partial_t Phi(P_t,t)
```

`R_hat` is a signed interface-pressure proxy from point-in-time features. With top-of-book data, it should be driven by OFI rate, signed trade imbalance if available, spread, depth, and turbulence features. With bars only, it should be clearly labeled as a weak proxy because the sign and queue mechanics are not identified.

## Latent liquidity slope L

`L` has units shares per tick squared. With L2 or L3 data, estimate it from cumulative visible depth around the midprice:

```text
C_ask(x) = sum visible ask shares from 1 to x ticks above mid
C_bid(x) = sum visible bid shares from 1 to x ticks below mid
C_side(x) ~= 0.5 * L_side * x^2
L = robust_average(L_ask, L_bid)
```

Recommendation: Full `L` validation should use L2 or L3 order-book data because estimating a slope requires depth away from the best quote, and full source/sink validation requires add, cancel, modify, and execution events. Sources: https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities.

With top-of-book only, estimate a proxy:

```text
D_h = harmonic_mean(best_bid_size, best_ask_size)
s   = spread_ticks
L_L1_proxy = 2 * D_h / max(s, 1)
```

This treats the best queue as one tick of density located roughly `s / 2` ticks from the mid. Recommendation: Phase 1 may use `L_L1_proxy` only as a point-in-time fragility feature and must not call it identified latent liquidity. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

With bars only, do not estimate structural `L`. Use a rolling inverse-impact proxy only for exploratory controls:

```text
L_bar_proxy = robust_median(2 * abs(signed_volume_proxy) / max(DeltaP_ticks^2, P_floor^2))
```

If trade signs are unavailable, replace this with a liquidity-cost proxy such as absolute return per dollar volume and mark it nonstructural. Recommendation: bars-only Phase 1 should use bar impact proxies as controls, not as `L`, because bars do not expose queue depth, quote revisions, or source/sink events. Sources: https://doi.org/10.1111/j.1540-6261.2009.01469.x, https://lobsterdata.com/info/DataStructure.php.

## Interface function Phi

For Phase 0, define `Phi` as a local function rather than a full reconstructed field:

```text
Phi_hat(p,t) = L_hat_t * (p - P_t) - B_hat_t
```

`B_hat_t` is a signed pressure offset. Positive `B_hat_t` shifts the zero interface upward when buy pressure dominates. A simple Phase 1 top-of-book form is:

```text
B_hat_t = a_1 * OFI_rate_t
        + a_2 * signed_trade_rate_t
        + a_3 * imbalance_t
        + a_4 * news_score_t
```

Only variables observed at or before `t` are allowed. Recommendation: `Phi_hat` should be estimated as a predictive feature map with strict point-in-time windows, because the repository forbids future data and OFI is already a strong short-horizon baseline. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

For bars only, use:

```text
B_hat_t = a_1 * signed_volume_proxy_t
        + a_2 * return_reversal_or_momentum_t
        + a_3 * news_score_t
```

Recommendation: bars-only `Phi_hat` should be treated as an interface-pressure approximation, not a latent order book reconstruction. Sources: https://doi.org/10.1111/j.1540-6261.2009.01469.x, https://arxiv.org/abs/1412.0141.

## Turbulence-amplified impact

TRIDENT adds market turbulent energy `k`, dissipation `epsilon`, and fragility:

```text
F_t = k_t^2 / (epsilon_t + epsilon_0)
```

Use turbulence as an amplifier of impact after controlling for standard liquidity:

```text
Impact(Q,t) = sign(Q) * sqrt(2 * abs(Q) / (L_hat_t + L_floor))
              * (1 + theta_F * standardized(F_t))
```

An equivalent form is an effective slope:

```text
L_eff_t = (L_hat_t + L_floor) / (1 + theta_F * standardized(F_t))^2
```

Recommendation: Phase 1 should test turbulence amplification only as incremental explanatory power over OFI, spread, depth, volume, and realized volatility. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822.

## Open questions

Can top-of-book depth provide a stable enough `L_L1_proxy` across symbols with different lot sizes, spreads, and tick constraints?

Does the square-root impact law hold in the chosen Phase 1 universe after normalizing by volatility, volume, and participation rate?

Can `k^2 / epsilon` add explanatory power after realized volatility, spread, depth, OFI, and event intensity are already included?

Should `Phi_hat` be estimated separately for upward and downward moves to capture bid-ask asymmetry?

Can bars-only signed volume proxies be trusted for symbols with high off-exchange volume or wide spreads?

What horizon best matches the interface approximation: one bar, several bars, event time, or adaptive liquidity time?
