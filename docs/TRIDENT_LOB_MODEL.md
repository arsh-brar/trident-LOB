# TRIDENT-LOB Model Specification

## Purpose

TRIDENT-LOB means Turbulent Reaction-diffusion Interface Dynamics for Electronic Limit Order Books.

The model treats the limit order book as a two-sided reactive liquidity field in price space. Resting bids and asks are mass-like fields. New limit orders are sources. Cancellations are sinks. Market orders are reactive sinks. Price is a moving interface between latent buy pressure and latent sell pressure. Volatility and liquidity fragility are represented through a turbulence-closure-like pair of variables, market turbulent energy `k` and dissipation `epsilon`.

This document is meant to be placed in the project directory before the research and coding phases begin.

## Important scope note

This model is a research model, not a guaranteed trading system. The first implementation should be used for simulation, backtesting, and paper trading. Live trading should be blocked by explicit validation gates, risk limits, and broker compliance checks.

## Does news enter the model?

Yes. News enters as an exogenous forcing term `N_t` that changes over the day. In the model, news is not a one-time variable. It is a timestamped event stream with decay, symbol relevance, sentiment, novelty, and market-wide impact.

A practical symbol-specific news forcing term can be:

```text
N_i(t) = sum_j beta_source(j) * relevance(i,j) * sentiment(j) * novelty(j)
         * exp(-(t - tau_j) / tau_N) * 1[t >= tau_j]
```

where:

- `i` is the stock symbol.
- `j` is a news event.
- `tau_j` is the publication timestamp.
- `beta_source(j)` is a source reliability weight.
- `relevance(i,j)` measures whether the event matters for the symbol.
- `sentiment(j)` can be positive, negative, or neutral.
- `novelty(j)` downweights repeated versions of the same story.
- `tau_N` is the decay time scale.

The model should support at least three exogenous streams:

1. Symbol-specific news, such as earnings, analyst actions, legal events, product news, and SEC filings.
2. Market-wide news, such as inflation, rates, Fed speeches, jobs data, and geopolitical shocks.
3. Scheduled events, such as earnings calendar, economic calendar, FOMC calendar, and options expiry.

The first version can use a simple news score, but the architecture should allow a better event encoder later.

## State variables

Use price `p` as the spatial coordinate and time `t` as the time coordinate.

### Visible order book fields

```text
q_plus(p,t)  = sell-side ask liquidity density
q_minus(p,t) = buy-side bid liquidity density
```

These are visible resting orders, ideally from Level 2 or Level 3 data.

### Quote transport velocities

```text
u_plus(p,t)  = ask-side quote-revision velocity in price space
u_minus(p,t) = bid-side quote-revision velocity in price space
```

These represent liquidity migrating through price space by canceling and reposting.

### Latent order book fields

```text
ell_plus(p,t)  = latent sell intention
ell_minus(p,t) = latent buy intention
Phi(p,t)       = ell_plus(p,t) - ell_minus(p,t)
```

The midprice is the moving interface where latent buy and sell pressure balance:

```text
Phi(P_t,t) = 0
```

### Turbulence variables

```text
k(p,t)       = market turbulent kinetic energy
epsilon(p,t) = market turbulence dissipation rate
nu_t(p,t)    = market eddy diffusivity
```

Use:

```text
nu_t = C_mu * k^2 / (epsilon + epsilon_0)
```

Interpretation:

```text
volatility intensity        ~= k
market dissipation capacity ~= epsilon
market fragility            ~= k^2 / epsilon
```

High `k` with high `epsilon` means an active but resilient market. High `k` with low `epsilon` means a fragile market where shocks persist and liquidity can vanish.

## Core liquidity equation

For each side `s in {plus, minus}`:

```text
partial_t q_s + partial_p(q_s * u_s)
=
partial_p [ (D_0 + nu_t / sigma_q) * partial_p q_s ]
+ lambda_s
- mu_s * q_s
- e_s
+ xi_s
```

Terms:

- `lambda_s`: new limit order source.
- `mu_s * q_s`: cancellation sink.
- `e_s`: execution sink from market orders consuming resting liquidity.
- `D_0`: base diffusion in price placement.
- `nu_t / sigma_q`: turbulent diffusion of liquidity.
- `xi_s`: stochastic order-flow noise.

This equation must preserve nonnegative liquidity. The numerical implementation must cap executions by available depth.

## Execution sink

Aggressive buy flow consumes ask liquidity:

```text
e_plus(p,t) = M_plus(t) * K_plus(p; q_plus)
```

Aggressive sell flow consumes bid liquidity:

```text
e_minus(p,t) = M_minus(t) * K_minus(p; q_minus)
```

where:

```text
M_plus(t)  = aggressive buy market order flow
M_minus(t) = aggressive sell market order flow
```

and `K_plus`, `K_minus` are queue-priority kernels concentrated near the best ask and best bid.

## Quote momentum analogue

For each side `s`:

```text
partial_t u_s + u_s * partial_p u_s
=
- 1 / (q_s + q_star) * partial_p Pi_s
+ partial_p [ (nu_0 + nu_t) * partial_p u_s ]
- gamma_u * u_s
+ F_s
+ eta_s
```

Market pressure:

```text
Pi_s = c_q^2 * q_s + c_k * k
```

Interpretation:

- `c_q^2 * q_s`: crowding pressure from too much liquidity at a price.
- `c_k * k`: uncertainty pressure that causes quotes to widen, cancel, or move.
- `nu_0 + nu_t`: effective liquidity viscosity.
- `gamma_u`: damping from arbitrage, market-making, and mean reversion.
- `F_s`: forcing from imbalance, news, inventory pressure, and cross-asset signals.
- `eta_s`: stochastic forcing.

## Turbulence closure

After decomposing mean and fluctuations:

```text
u_s = mean(u_s) + u_s_prime
q_s = mean(q_s) + q_s_prime
```

an averaged liquidity equation produces an unclosed turbulent flux:

```text
mean(q_s_prime * u_s_prime)
```

Use a gradient closure:

```text
mean(q_s_prime * u_s_prime) ~= -nu_t * partial_p mean(q_s)
```

with:

```text
nu_t = C_mu * k^2 / (epsilon + epsilon_0)
```

### k equation

```text
partial_t k + U * partial_p k
=
partial_p [ (D_k + nu_t / sigma_k) * partial_p k ]
+ P_k
- epsilon
+ zeta_k
```

### epsilon equation

```text
partial_t epsilon + U * partial_p epsilon
=
partial_p [ (D_epsilon + nu_t / sigma_epsilon) * partial_p epsilon ]
+ C_epsilon1 * epsilon / (k + k_0) * P_k
- C_epsilon2 * epsilon^2 / (k + k_0)
+ zeta_epsilon
```

### Turbulence production

```text
P_k =
C_u * sum_s q_s * (partial_p u_s)^2
+ C_I * I^2 / (D_top + D_star)^2
+ C_c * |partial_t log(D_top)|^2
+ C_N * N_t^2
```

where:

```text
I     = M_plus - M_minus
D_top = top-of-book depth
N_t   = exogenous news or information shock
```

The production terms represent quote shear, aggressive order-flow imbalance, liquidity withdrawal, and news shocks.

## Price interface equation

The midprice `P_t` is the zero crossing of latent buy and sell pressure:

```text
Phi(P_t,t) = 0
```

Differentiating the interface condition gives:

```text
dP_t = - partial_t Phi(P_t,t) / partial_p Phi(P_t,t) * dt
       + sqrt(2 * chi_P * nu_t(P_t,t)) * dW_t
```

The deterministic part moves with latent liquidity imbalance. The stochastic part scales with local market eddy diffusivity.

## Market impact prediction

Near the midprice, assume the latent imbalance is linear:

```text
ell_plus(p) - ell_minus(p) ~= L * (p - P_t)
```

A buy meta-order of size `Q` consumes liquidity from `P_t` to `P_t + DeltaP`:

```text
Q = integral_0^DeltaP L * x dx = 0.5 * L * DeltaP^2
```

So:

```text
DeltaP = sqrt(2Q / L)
```

TRIDENT-LOB adds turbulence by reducing effective usable liquidity:

```text
L_eff = L / (1 + chi_nu * nu_t)
```

Therefore:

```text
DeltaP ~= sqrt( 2Q * (1 + chi_nu * nu_t) / L )
```

Key testable claim:

```text
For the same Q and visible depth, impact should be larger when k^2 / epsilon is high.
```

## Market Reynolds number

Define:

```text
R_m = ( |I| / (D_top + D_star) ) / ( epsilon / (k + k_0) + gamma_u )
```

Interpretation:

- `R_m << 1`: laminar market, imbalance is absorbed.
- `R_m ~= 1`: transitional market, spread widens and volatility bursts.
- `R_m >> 1`: liquidity vacuum, executions consume the book faster than liquidity replenishes.

Crash-like local jump condition:

```text
|I| > (D_top + D_star) * ( epsilon / (k + k_0) + gamma_u )
```

## Verification checks

### Check 1: Order-book accounting

Integrate the liquidity equation over price:

```text
d/dt integral q_s dp = integral lambda_s dp
                       - integral mu_s q_s dp
                       - integral e_s dp
                       + boundary flux
```

This must match event-level accounting.

### Check 2: Nonnegative liquidity

The implementation must enforce:

```text
q_s(p,t) >= 0
lambda_s >= 0
mu_s >= 0
e_s >= 0
```

Executions must never consume more shares than available.

### Check 3: Symmetry sanity check

If both sides are symmetric:

```text
q_plus = q_minus
lambda_plus = lambda_minus
mu_plus = mu_minus
M_plus = M_minus
F_plus = F_minus
```

then expected deterministic price drift should be zero.

### Check 4: Known-model limits

- If `k = 0`, `nu_t = 0`, and quote velocity is ignored, the model reduces to a stochastic source/sink order-book model.
- If the latent book is linear near the midprice, the model recovers square-root impact.
- If only best bid and best ask are retained, the model reduces toward order-flow imbalance over depth models.

## Phase 1 implementation target

The first implementation should not attempt the full PDE/SPDE immediately. It should build a minimal prediction engine that estimates simplified TRIDENT state variables from available data.

Suggested Phase 1 inputs:

```text
bars: open, high, low, close, volume, vwap
quotes: best bid, best ask, bid size, ask size
tape: trades with side classification if available
news: timestamped symbol and market news scores, optional at first
```

Suggested Phase 1 features:

```text
spread
midprice return
order-flow imbalance proxy
top-book depth proxy
realized volatility proxy for k
volatility decay proxy for epsilon
fragility = k^2 / epsilon
news forcing N_t
market Reynolds number R_m
```

Suggested Phase 1 targets:

```text
next 1-minute direction
next 5-minute direction
next 1-minute return
next 5-minute return
probability of spread widening
probability of local jump
```

Suggested Phase 1 model options:

```text
baseline: logistic regression or ridge regression
strong tabular baseline: LightGBM or XGBoost
physics-informed model: differentiable state-space model or neural ODE later
```

The first goal is not to prove the PDE. The first goal is to test whether TRIDENT-derived features improve out-of-sample prediction and paper-trading performance against simple baselines.

## Phase 2 implementation target

Phase 2 should add Level 2 or Level 3 event replay:

```text
new limit order events
cancellation events
market order executions
queue position updates
order-book reconstruction
source and sink estimation
fuller q_plus and q_minus fields across price levels
```

This is where TRIDENT becomes an actual reaction-diffusion order-book model instead of a feature-generation model.

## Data needs

### Minimum viable data

Use this for early coding and architecture tests:

- Minute bars for many stocks.
- Top-of-book quote stream if available.
- Trades if available.
- News stream or delayed news archive if available.

This is enough for a Phase 1 feature model, but not enough to verify the full source/sink PDE.

### Serious model-validation data

Use this to test the actual TRIDENT intuition:

- Level 2 market depth, ideally at least 10 levels.
- Level 3 message data if possible.
- Market order, limit order, and cancellation events.
- Nanosecond or microsecond timestamps if possible.
- Corporate actions and symbol mapping.
- Trading halts and exchange status.
- News and scheduled-event timestamps.

### Practical data recommendation

For US equities, serious order-book data is usually paid. Free or cheap data can get the code and Phase 1 predictor started, but validating the source/sink model usually requires paid L2 or L3 data.

Reasonable path:

1. Start with free or low-cost minute bars and top-of-book quotes for code structure.
2. Add paper trading with no real money.
3. Buy a small amount of historical L2/L3 data for a few liquid symbols and a few days.
4. Only then scale to larger datasets.

## References

These references are starting points for the research agents. They should be verified and expanded during Phase 0.

- Cont, Kukanov, Stoikov, The Price Impact of Order Book Events, arXiv:1011.6402.
- Donier, Bonart, Mastromatteo, Bouchaud, A fully consistent, minimal model for non-linear market impact, arXiv:1412.0141.
- Gao and Deng, Hydrodynamic Limit of Order Book Dynamics, arXiv:1411.7502.
- Huang and Polak, LOBSTER: Limit Order Book Reconstruction System, SSRN 1977207.
- Databento equities and Nasdaq TotalView-ITCH documentation.
- LOBSTER data documentation.
- Alpaca market data and paper trading documentation.
- FINRA intraday margin and day trading rule documentation.
