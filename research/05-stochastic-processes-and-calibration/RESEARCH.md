# Stochastic Processes And Calibration Research

## Scope

This is Phase 0 research only. It does not authorize production code, broker connectivity, live orders, or profitability claims. Phase 1 remains a CPU-only Python feature pipeline on the local Mac M3. Internal book coordinates are ticks. Full source and sink validation requires L2 or L3 data. Live trading remains blocked by the repository policy and the Wave 1 risk decision. Sources: ../../AGENTS.md, ../../docs/TRIDENT_LOB_MODEL.md, ../00-market-microstructure-literature/DECISION.md, ../01-equation-audit-and-dimensional-analysis/DECISION.md, ../06-data-requirements-and-vendors/DECISION.md, ../11-risk-controls-and-compliance/DECISION.md, ../12-python-architecture-and-stack/DECISION.md.

## Objects To Calibrate

TRIDENT separates visible liquidity, event flows, transport, diffusion, latent interface motion, and turbulence proxies. The calibration target should therefore be a staged family of models, not one monolithic estimator.

The source term `lambda_s(p,t)` is the arrival rate or intensity of new visible limit liquidity on side `s` at tick coordinate `p`. Event-level calibration should count add events by side, price cell, state bin, and time. This follows stochastic LOB models that estimate order-flow rates from high-frequency order book observations and queue-reactive models that condition event intensities on the current book state. Sources: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780; Huang, Lehalle, and Rosenbaum, https://doi.org/10.1080/01621459.2014.982278.

The cancellation sink `mu_s(p,t) q_s(p,t)` is the depletion rate from visible cancellations and deletes. Event-level calibration should estimate either a cancellation intensity per resting share or a direct cancellation hazard by price cell and queue state. This is identifiable from event messages with cancel or delete actions and becomes confounded when only aggregate depth changes are observed. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

The execution sink `e_s(p,t)` is the marketable order flow that consumes resting liquidity. Event-level calibration should separate trades and fills from cancels, cap consumption by available cell depth, and estimate a queue-priority kernel `K_s` concentrated near the best quote. Order-flow imbalance is the required simple baseline because short-horizon price changes are strongly linked to signed supply and demand at the best quotes. Sources: Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

The diffusion terms `D_0` and `nu_t / sigma_q` summarize local spreading, smoothing, and turbulent redistribution of visible liquidity across tick cells. In Phase 1 these should be proxies only. In Phase 2 they can be estimated from L2 or L3 replay by comparing net flux across neighboring tick cells after accounting for adds, cancels, and executions. Finite-volume accounting is the correct conceptual framework because the liquidity equation is a conservation law with reaction terms. Sources: Patankar, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224; TRIDENT model specification, ../../docs/TRIDENT_LOB_MODEL.md.

The turbulence terms `k`, `epsilon`, and `nu_t = C_mu k^2 / (epsilon + epsilon_0)` should be treated as latent state variables or feature proxies before they are treated as physically identified fields. Phase 1 can estimate `k` from realized variance or quote-motion variance and `epsilon` from volatility decay, spread recovery, or depth recovery. Realized volatility has a formal connection to quadratic variation, but high-frequency microstructure noise affects naive realized variance estimators. Sources: Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418; Zhang, Mykland, and Ait-Sahalia, https://doi.org/10.1198/016214505000000169.

The price interface parameters should be calibrated only as predictive or descriptive latent-state parameters in Phase 1. L1 data supports midprice motion, spread widening probability, and OFI response. L2 and L3 data are needed to estimate the slope of latent or visible liquidity near the interface with less confounding. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

## Candidate Stochastic Process Families

Independent or conditionally independent Poisson processes are the first event-intensity baseline for limit arrivals, cancellations, and executions. They are simple, auditable, and consistent with the baseline stochastic order-book literature. Source: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780.

State-dependent Markov queue models are the preferred Phase 2 baseline when replayed book state is available. They estimate event rates conditional on queue sizes, spread, distance from mid, and constant-reference-price regimes. Source: Huang, Lehalle, and Rosenbaum, https://doi.org/10.1080/01621459.2014.982278.

Hawkes processes are the preferred event-clustering benchmark once event timestamps are reliable and dense enough. They can model self-excitation and cross-excitation among add, cancel, and trade events, but they should not be the Phase 1 default for bars because bars discard the timing information that Hawkes likelihoods need. Sources: Bacry, Mastromatteo, and Muzy, https://arxiv.org/abs/1502.04592; Abergel and Jedidi, https://doi.org/10.1137/15M1011469.

Diffusion and state-space approximations are appropriate for `k`, `epsilon`, latent interface motion, and smoothed liquidity states. Maximum likelihood for discretely observed diffusions can be useful when transition densities are approximated, but Phase 1 should use low-dimensional proxies before full latent diffusion estimation. Source: Ait-Sahalia, https://doi.org/10.1111/1468-0262.00274.

Bayesian filtering, particle filtering, and particle MCMC are appropriate when hidden states matter and likelihoods are nonlinear or non-Gaussian. These methods are research options for turbulence and latent-interface estimation, not Phase 1 dependencies. Sources: Sarkka and Svensson, https://doi.org/10.1017/9781108917407; Doucet and Johansen, https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF.pdf; Andrieu, Doucet, and Holenstein, https://academic.oup.com/jrsssb/article/72/3/269/7076437.

Neural state-space models and score-based calibration are later research options only. They can approximate nonlinear state transitions and posterior distributions, but they add training complexity, compute cost, and validation burden. They should wait until simple baselines, likelihood estimators, and moment estimators fail on out-of-sample validation. Sources: Krishnan, Shalit, and Sontag, https://arxiv.org/abs/1609.09869; Hyvarinen, https://jmlr.csail.mit.edu/papers/v6/hyvarinen05a.html; Song et al., https://openreview.net/forum?id=PxTIG12RRHS.

## Data Identifiability

Bars identify only coarse proxies. They can support realized volatility, volatility decay, volume, return, range, and VWAP-based features. They do not identify source, cancellation, execution, queue priority, or price-level diffusion terms. This means bars can calibrate Phase 1 `k` and `epsilon` proxies, but they cannot validate the full reaction-diffusion source and sink model. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418.

L1 quotes identify top-of-book spread, midprice, best bid and ask sizes, top-book depth, and OFI-style pressure. They can estimate net top-book replenishment and depletion, but they cannot cleanly separate new limit orders from cancellations and executions without trade prints and event labels. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

L2 depth identifies visible depth by price level and can support aggregate price-cell source and sink estimates when event actions are included. It can estimate depth recovery, local depth shocks, and aggregate diffusion proxies across the observed levels. It cannot fully identify individual queue position, hidden liquidity, or order-level cancellation hazards. Sources: Databento MBP-10 documentation, https://databento.com/docs/schemas-and-data-formats/mbp-10; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

L3 messages are the strongest source for source, sink, execution, cancellation, and queue-priority calibration because order IDs and event types let replay reconstruct order lifecycles. Even L3 does not reveal all hidden liquidity or off-venue pressure, so validation must keep residual uncertainty. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

## Open Questions

Which `epsilon` proxy is most stable: volatility half-life, spread recovery, depth recovery, or a joint latent-state decay rate?

Can `D_0` and turbulent diffusion `nu_t / sigma_q` be separately identified from practical L2 replay, or are they only jointly identifiable?

Does `k^2 / epsilon` add signal after controlling for realized volatility, spread, depth, OFI, and event intensity?

How much L3 history is needed for stable cancellation hazards by side, tick distance, and queue state?

How should hidden liquidity, midpoint executions, auctions, halts, and fragmented venues enter residual terms?

Can exogenous news forcing be separated from endogenous self-excitation in event flow?
