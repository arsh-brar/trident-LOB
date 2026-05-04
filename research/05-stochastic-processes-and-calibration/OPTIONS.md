# Calibration Options

## Option A: Direct Counts And Maximum Likelihood

Estimate arrival, cancellation, and execution rates by counting events in time, side, price-cell, and state bins. Fit Poisson, multinomial, survival, or simple Hawkes likelihoods when event timestamps are available.

Strengths: simple, auditable, CPU-friendly, and aligned with stochastic LOB baselines. It gives direct estimates for `lambda_s`, `mu_s`, and `e_s` when L2 or L3 event labels exist. Sources: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780; Huang, Lehalle, and Rosenbaum, https://doi.org/10.1080/01621459.2014.982278.

Weaknesses: event-label quality matters, seasonality must be handled, and bars cannot support this beyond coarse volume or volatility proxies. Hawkes likelihoods also become fragile if timestamps are batched, censored, or too coarse. Sources: Bacry, Mastromatteo, and Muzy, https://arxiv.org/abs/1502.04592; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Best use: Phase 1 should use direct counts only for available bars, quotes, and trades. Phase 2 should use event-level maximum likelihood as the primary calibration method for source, cancellation, and execution terms. Sources: ../../docs/TRIDENT_LOB_MODEL.md; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

## Option B: Generalized Method Of Moments

Estimate parameters by matching moments such as mean event rates, cancellation fractions, depth recovery half-life, realized variance, OFI response slope, spread-widening frequency, impact curves, and stylized facts.

Strengths: useful when likelihoods are misspecified or partially observed. It can combine bars, L1 quotes, trades, and L2 aggregates without pretending all hidden events are observed. Sources: Hansen, https://www.econometricsociety.org/publications/econometrica/1982/07/01/large-sample-properties-generalized-method-moments-estimators; Cont stylized facts, https://doi.org/10.1080/713665670.

Weaknesses: moment choice is subjective, weak identification is possible, and uncertainty estimates need robust time-series treatment. It cannot recover source and sink event mechanics from bars alone. Sources: Hansen, https://www.econometricsociety.org/publications/econometrica/1982/07/01/large-sample-properties-generalized-method-moments-estimators; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Best use: Phase 1 should use moment matching for `k`, `epsilon`, fragility, OFI response, and simple interface response. Phase 2 can use GMM as a robustness check against likelihood estimates. Sources: Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

## Option C: Bayesian Filtering

Represent `k`, `epsilon`, latent imbalance, and price-interface state as hidden variables. Update posterior state estimates as bars, quotes, trades, or events arrive.

Strengths: principled uncertainty representation, works with missing data, and naturally separates latent states from noisy observations. Sources: Sarkka and Svensson, https://doi.org/10.1017/9781108917407; Kalman, https://doi.org/10.1115/1.3662552.

Weaknesses: model design matters, priors can dominate short samples, and full Bayesian estimation may be too heavy for Phase 1. Source: Sarkka and Svensson, https://doi.org/10.1017/9781108917407.

Best use: keep as a Phase 1 research design for turbulence and interface state, but implement only after simple rolling and exponentially weighted proxies are validated. Sources: ../../AGENTS.md; ../../docs/TRIDENT_LOB_MODEL.md.

## Option D: Particle Filters And Particle MCMC

Use sequential Monte Carlo for nonlinear, non-Gaussian latent states, then use particle MCMC or related methods for parameter uncertainty.

Strengths: flexible for nonlinear `k`, `epsilon`, `nu_t`, and latent interface dynamics. It can handle non-Gaussian observation noise and regime changes better than linear Gaussian filters. Sources: Doucet and Johansen, https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF.pdf; Andrieu, Doucet, and Holenstein, https://academic.oup.com/jrsssb/article/72/3/269/7076437.

Weaknesses: computational cost, particle degeneracy, tuning burden, and difficult reproducibility. It is not the right first step for a CPU-only Phase 1 feature pipeline. Sources: Doucet and Johansen, https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF.pdf; ../12-python-architecture-and-stack/DECISION.md.

Best use: later calibration studies on short L2 or L3 windows where uncertainty in turbulence and interface states is central. Source: Sarkka and Svensson, https://doi.org/10.1017/9781108917407.

## Option E: Kalman-Style Approximations

Use linear Kalman, extended Kalman, unscented Kalman, or Gaussian assumed-density filters for low-dimensional latent state estimates.

Strengths: faster than particle methods, CPU-friendly, and suitable for online-style research features. They are a practical bridge between rolling proxies and full nonlinear filtering. Sources: Kalman, https://doi.org/10.1115/1.3662552; Julier and Uhlmann, https://doi.org/10.1109/JPROC.2003.823141.

Weaknesses: Gaussian assumptions and local linearization can fail during jumps, halts, crossed markets, and liquidity vacuums. Source: Julier and Uhlmann, https://doi.org/10.1109/JPROC.2003.823141.

Best use: Phase 1 candidate for `k`, `epsilon`, and price-interface proxies after rolling baselines. Keep it low-dimensional and deterministic enough for reproducible CPU tests. Sources: ../12-python-architecture-and-stack/DECISION.md; Sarkka and Svensson, https://doi.org/10.1017/9781108917407.

## Option F: Neural State-Space Models

Use neural networks for transition and emission functions in a latent state-space model.

Strengths: can fit nonlinear transition dynamics that are hard to write by hand, including interactions among OFI, spread, depth, news, and turbulence proxies. Source: Krishnan, Shalit, and Sontag, https://arxiv.org/abs/1609.09869.

Weaknesses: high overfitting risk, more compute, harder interpretation, and greater leakage and validation burden. This conflicts with the Phase 1 preference for simple baselines first. Sources: ../../AGENTS.md; Bailey et al., https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Best use: do not use in Phase 1 core. Revisit only after simple baselines and physics-derived features pass out-of-sample validation. Sources: ../00-market-microstructure-literature/DECISION.md; ../12-python-architecture-and-stack/DECISION.md.

## Option G: Score-Based Calibration

Use score matching, diffusion models, or score-based simulation-based inference to learn gradients of log densities or posteriors over latent states and parameters.

Strengths: can target complex high-dimensional distributions when likelihoods are unavailable or expensive. Sources: Hyvarinen, https://jmlr.csail.mit.edu/papers/v6/hyvarinen05a.html; Song et al., https://openreview.net/forum?id=PxTIG12RRHS.

Weaknesses: not naturally aligned with Phase 1 CPU-only simple baselines, requires careful simulator design, and can be difficult to validate economically. Sources: ../../AGENTS.md; Song et al., https://openreview.net/forum?id=PxTIG12RRHS.

Best use: later research on synthetic SPDE or event-replay calibration, not initial empirical calibration. Sources: Hyvarinen, https://jmlr.csail.mit.edu/papers/v6/hyvarinen05a.html; ../12-python-architecture-and-stack/DECISION.md.

## Option Comparison

| Method | Best parameters | Minimum data | Phase 1 fit | Main risk |
|---|---|---:|---|---|
| Direct counts and MLE | `lambda_s`, `mu_s`, `e_s`, Hawkes kernels | L2/L3 events | partial | event labels and seasonality |
| GMM | `k`, `epsilon`, OFI response, interface response | bars or L1 | strong | weak identification |
| Bayesian filtering | latent `k`, `epsilon`, interface state | bars or L1 | later | prior and model dependence |
| Particle filters | nonlinear latent states | L1/L2/L3 | later | compute and degeneracy |
| Kalman-style approximations | low-dimensional latent proxies | bars or L1 | later | Gaussian approximation failure |
| Neural state-space models | nonlinear transitions | large L1/L2/L3 | no | overfitting and opacity |
| Score-based calibration | high-dimensional posterior or simulator calibration | large simulation or L2/L3 | no | validation burden |

## Open Questions

Which moments should be mandatory for the first GMM calibration report?

Can event-level MLE and GMM agree on `mu_s` and `e_s` in real L2 or L3 samples?

What minimum sample length is needed for stable Hawkes cross-excitation estimates?

Are Kalman-style `epsilon` estimates more stable than direct volatility-decay proxies?

Can score-based calibration produce interpretable uncertainty for TRIDENT parameters, or only useful simulation diagnostics?
