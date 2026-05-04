# Validation

## Purpose

Validation must determine whether the latent-liquidity and interface proxies add useful, non-leaky explanatory power over standard market microstructure baselines. It must not claim profitability and must not authorize live trading.

Recommendation: Treat every result as research-only until it passes out-of-sample validation, transaction-cost-aware interpretation, and later project validation gates. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://doi.org/10.1080/14697680903373692.

## Data validation

Check:

```text
timestamps are monotonic per symbol
features use only data available at or before prediction time
spread_ticks > 0
best sizes are nonnegative
mid_ticks is finite
no target column is used in feature construction
halted or bad-data intervals are excluded or flagged
```

Recommendation: Make leakage checks a hard gate because future data is prohibited and leakage can dominate high-frequency validation. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

## Baseline tests

Run baseline models before TRIDENT-specific features:

```text
DeltaP_{t,h} ~ OFI_t / depth_t
DeltaP_{t,h} ~ spread_t + depth_t + volume_t + realized_volatility_t
abs(DeltaP_{t,h}) ~ volume_t + realized_volatility_t + spread_t
```

Recommendation: Require OFI, spread, depth, and realized volatility baselines before testing `Phi_hat`, because OFI and depth explain short-horizon price moves in existing literature. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://academic.oup.com/jfec/article/12/1/47/816163.

## Square-root impact test

Use signed volume or metaorder proxy buckets. For each symbol, horizon, and regime:

```text
I_h(Q) = median(sign(Q) * DeltaP_{t,h} | bucket(abs(Q)))
```

Fit:

```text
abs(I_h(Q)) = A * abs(Q)^delta
```

Pass criteria:

```text
delta is closer to 0.5 than to 1.0 out of sample
A decreases when L_proxy increases
sign agreement is better than a naive zero-impact model
results are stable across train and test windows
```

Recommendation: Test square-root impact as a scaling law with out-of-sample buckets, not as a trading signal, because the latent order book literature explains impact concavity but does not imply profitable prediction. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://arxiv.org/abs/1412.0141.

## L proxy validation

Top-of-book mode:

```text
L_L1_proxy = 2 * harmonic_mean(best_bid_size, best_ask_size) / max(spread_ticks, 1)
```

Tests:

```text
higher L_L1_proxy predicts lower absolute impact for the same signed pressure
higher L_L1_proxy reduces fitted OFI coefficient magnitude
L_L1_proxy is stable enough by symbol and time of day
```

Recommendation: Validate `L_L1_proxy` only by monotonic impact reduction and incremental predictive value, because top-of-book data cannot identify the full latent liquidity slope. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://lobsterdata.com/info/DataStructure.php.

Bars-only mode:

```text
L_bar_proxy = rolling inverse-impact proxy
```

Tests:

```text
L_bar_proxy predicts lower next-period absolute return per unit volume
L_bar_proxy does not use the target return window
L_bar_proxy is less trusted than top-of-book L_L1_proxy
```

Recommendation: Treat bars-only validation as low-confidence screening because daily or bar-level liquidity proxies estimate trading costs indirectly and do not expose queues. Sources: https://doi.org/10.1111/j.1540-6261.2009.01469.x, https://lobsterdata.com/info/DataStructure.php.

## Phi validation

Estimate:

```text
Phi_hat(p,t) = L_hat_t * (p - P_t) - B_hat_t
interface_velocity_proxy = B_hat_t / (L_hat_t + L_floor)
```

Tests:

```text
interface_velocity_proxy predicts signed DeltaP_{t,h}
Phi features improve directional log loss or regression error over baselines
coefficients have stable signs across walk-forward splits
performance survives symbol, day, and volatility-regime splits
```

Recommendation: Accept `Phi_hat` only if it improves out-of-sample metrics after OFI, spread, depth, volume, and realized volatility are included. Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Turbulence-amplified impact test

Define:

```text
F_t = k_t^2 / (epsilon_t + epsilon_0)
base_impact = sign(Q_t) * sqrt(2 * abs(Q_t) / (L_hat_t + L_floor))
amplified_impact = base_impact * (1 + theta_F * zscore(F_t))
```

Run nested comparisons:

```text
Model A: impact ~ base_impact
Model B: impact ~ base_impact + realized_volatility
Model C: impact ~ base_impact + realized_volatility + F_t
Model D: impact ~ base_impact * F_t + realized_volatility + spread + depth + OFI
```

Pass criteria:

```text
theta_F > 0 in walk-forward test windows
interaction improves out-of-sample error or likelihood
effect remains after spread and depth controls
effect is strongest during high fragility regimes
no single crisis day drives the result
```

Recommendation: Require turbulence amplification to beat realized-volatility and depth-withdrawal controls before treating it as a TRIDENT result, because `k^2 / epsilon` is an original hypothesis rather than established market microstructure fact. Sources: https://doi.org/10.1103/PhysRevX.1.021006, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1712822.

## Robustness tests

Run:

```text
walk-forward splits
symbol-held-out splits
day-held-out splits
time-of-day controls
spread-regime splits
volatility-regime splits
permutation tests for feature timing
round-trip impact sanity checks
```

Recommendation: Include round-trip impact sanity checks because transient impact models can violate no-dynamic-arbitrage if impact shape and decay are inconsistent. Sources: https://doi.org/10.1080/14697680903373692, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1292353.

## Open questions

What participation-rate proxy should be used when only bars are available?

How should fragmented parent orders be inferred without broker metaorder labels?

Should square-root impact be tested in event time, clock time, or volume time?

What minimum out-of-sample improvement is enough to keep turbulence-amplified impact in Phase 1?

How should hidden liquidity and off-exchange trades be flagged in equity data?
