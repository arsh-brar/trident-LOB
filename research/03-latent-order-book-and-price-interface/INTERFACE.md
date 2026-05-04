# Interface

## Component role

The price-interface estimator converts point-in-time market features into latent-liquidity and interface-pressure proxies. It is a research component for Phase 1. It does not place orders, route orders, create broker intents, or claim profitability.

Recommendation: Keep the estimator swappable behind a small interface because the project architecture requires modular estimators and Phase 1 should compare simple baselines before complex models. Sources: https://numpy.org/install/, https://scikit-learn.org/stable/install.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822.

## Inputs

Required point-in-time fields:

```text
symbol
timestamp
mid_ticks
spread_ticks
best_bid_size
best_ask_size
```

Optional point-in-time fields:

```text
ofi
signed_trade_volume
bar_volume
bar_return_ticks
realized_volatility_ticks
k
epsilon
news_score
halt_or_bad_data_flag
```

Recommendation: All inputs must be timestamped and joined as of the decision time, because future data is prohibited and look-ahead leakage invalidates predictive tests. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

## Outputs

The estimator returns research features:

```text
symbol
timestamp
mid_ticks
L_proxy
L_proxy_kind
B_proxy
Phi_at_mid
interface_velocity_proxy
sqrt_impact_proxy
turbulence_amplifier
fragility
quality_flags
```

Definitions:

```text
L_proxy_kind in {"l1_top_book", "bar_inverse_impact", "l2_visible_depth"}
Phi_at_mid = -B_proxy
interface_velocity_proxy = B_proxy / (L_proxy + L_floor)
sqrt_impact_proxy = sign(Q_proxy) * sqrt(2 * abs(Q_proxy) / (L_proxy + L_floor))
fragility = k^2 / (epsilon + epsilon_0)
turbulence_amplifier = 1 + theta_F * zscore(fragility)
```

Recommendation: Output `L_proxy_kind` and `quality_flags` with every row so downstream validation cannot confuse top-of-book or bars-only proxies with identified latent liquidity. Sources: https://lobsterdata.com/info/DataStructure.php, https://doi.org/10.1111/j.1540-6261.2009.01469.x.

## Top-of-book estimator contract

Use:

```text
D_h = harmonic_mean(best_bid_size, best_ask_size)
L_proxy = 2 * D_h / max(spread_ticks, 1)
queue_imbalance = (best_bid_size - best_ask_size)
                  / (best_bid_size + best_ask_size + depth_floor)
B_proxy = fitted_or_configured_linear_score(
    ofi_rate,
    signed_trade_rate,
    queue_imbalance,
    news_score
)
```

Recommendation: The top-of-book estimator must include OFI as a baseline feature when quote updates are available, because OFI is an established driver of short-horizon price changes. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://academic.oup.com/jfec/article/12/1/47/816163.

## Bars-only estimator contract

Use:

```text
Q_proxy = signed_volume_proxy if available else volume_shock_proxy
L_proxy = rolling_median(2 * abs(Q_proxy) / max(DeltaP_ticks^2, P_floor^2))
B_proxy = fitted_or_configured_linear_score(
    signed_volume_proxy,
    return_state,
    volume_shock,
    news_score
)
```

Required flags:

```text
quality_flags includes "bars_only"
quality_flags includes "latent_liquidity_not_identified"
```

Recommendation: Bars-only mode must expose explicit quality flags because bar data can estimate liquidity costs but cannot observe queue pressure or source/sink mechanics. Sources: https://doi.org/10.1111/j.1540-6261.2009.01469.x, https://lobsterdata.com/info/DataStructure.php.

## L2 or L3 validation estimator contract

Use visible cumulative depth:

```text
C_ask(x) ~= 0.5 * L_ask * x^2
C_bid(x) ~= 0.5 * L_bid * x^2
L_proxy = robust_average(L_ask, L_bid)
```

Recommendation: L2 or L3 mode should be a validation path rather than the Phase 1 default, because Phase 1 is a CPU-only feature pipeline and full event replay belongs after baseline gates. Sources: https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities.

## Quality gates

Return missing or invalid outputs when:

```text
spread_ticks <= 0
best_bid_size < 0
best_ask_size < 0
mid_ticks is missing
timestamp is stale
halt_or_bad_data_flag is true
L_proxy is not finite
epsilon <= 0 when fragility is requested
```

Recommendation: Fail closed on impossible or stale market data because erroneous market-data states invalidate research signals and later risk controls must reject stale or missing NBBO. Sources: https://ecfr.io/Title-17/Section-240.15c3-5, https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan.

## Open questions

Should side-specific `L_proxy_up` and `L_proxy_down` be returned instead of one symmetric slope?

Should `B_proxy` be a fitted coefficient model, a normalized index, or both?

Should turbulence amplification be computed inside this component or in a downstream impact validator?

How should quote-size odd lots be included if the data vendor reports them separately?
