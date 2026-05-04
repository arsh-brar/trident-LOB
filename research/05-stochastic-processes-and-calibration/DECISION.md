# Stochastic Processes And Calibration Decision

## Decision

Phase 1 calibration will use simple, CPU-only, point-in-time estimators and moment checks. It will not attempt the full TRIDENT SPDE, production code, live trading code, or neural calibration. This follows the Wave 1 decisions that Phase 1 is a feature pipeline, internal coordinates are ticks, full source and sink validation needs L2 or L3, and live trading is blocked. Sources: ../../AGENTS.md, ../../docs/TRIDENT_LOB_MODEL.md, ../00-market-microstructure-literature/DECISION.md, ../01-equation-audit-and-dimensional-analysis/DECISION.md, ../06-data-requirements-and-vendors/DECISION.md, ../11-risk-controls-and-compliance/DECISION.md.

Use generalized method of moments and rolling or exponentially weighted estimators for Phase 1 turbulence proxies. Estimate `k` from realized variance or quote-motion variance, estimate `epsilon` from volatility decay, spread recovery, or depth recovery, and report fragility as `k^2 / (epsilon + epsilon_0)`. This is the most defensible Phase 1 choice because bars and L1 quotes support volatility and recovery proxies but do not identify full source and sink mechanics. Sources: Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418; Zhang, Mykland, and Ait-Sahalia, https://doi.org/10.1198/016214505000000169; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Use direct event accounting and maximum likelihood as the Phase 2 primary method for `lambda_s`, `mu_s`, `e_s`, and queue-priority kernels when L2 or L3 events are available. Counts and likelihoods should be conditioned on side, tick distance, time of day, spread, depth, and queue state. This follows stochastic order-book and queue-reactive calibration practice. Sources: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780; Huang, Lehalle, and Rosenbaum, https://doi.org/10.1080/01621459.2014.982278.

Use Hawkes models only as an event-level benchmark after reliable event timestamps are available. Do not fit Hawkes models to bars as a primary estimator because bars discard event timing and cross-excitation information. Sources: Bacry, Mastromatteo, and Muzy, https://arxiv.org/abs/1502.04592; Abergel and Jedidi, https://doi.org/10.1137/15M1011469.

Use Kalman-style filters only as a later Phase 1 refinement for low-dimensional `k`, `epsilon`, and price-interface state. Use particle filters, particle MCMC, neural state-space models, and score-based calibration only as research extensions after baseline validation. This respects the simple-baseline rule and the CPU-only Phase 1 stack decision. Sources: Kalman, https://doi.org/10.1115/1.3662552; Julier and Uhlmann, https://doi.org/10.1109/JPROC.2003.823141; Doucet and Johansen, https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF.pdf; Krishnan, Shalit, and Sontag, https://arxiv.org/abs/1609.09869; Hyvarinen, https://jmlr.csail.mit.edu/papers/v6/hyvarinen05a.html; Song et al., https://openreview.net/forum?id=PxTIG12RRHS; ../12-python-architecture-and-stack/DECISION.md.

## Parameter Identifiability Decision

Bars can learn only coarse `k`, `epsilon`, volume, return, and impact-response proxies. They cannot learn `lambda_s`, `mu_s`, `e_s`, `K_s`, `u_s`, `D_0`, or `nu_t` as structural book parameters. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418.

L1 quotes can learn top-of-book spread, depth, OFI, quote-motion variance, top-book depletion and replenishment proxies, and simple price-interface response. They cannot cleanly separate new limit orders, cancellations, and executions without trade prints and event labels. Sources: Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

L2 depth can learn visible `q_plus`, `q_minus`, depth recovery, aggregate price-cell shocks, and partial source or sink rates when event actions are present. It cannot fully learn queue position or order-level cancellation hazards. Sources: Databento MBP-10 documentation, https://databento.com/docs/schemas-and-data-formats/mbp-10; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

L3 messages can learn the strongest versions of `lambda_s`, `mu_s`, `e_s`, `K_s`, queue position, and event-level accounting. It still cannot fully learn hidden liquidity or off-book latent intentions. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

## Non-Decision

This decision does not select a data vendor, approve paid data, approve production ingestion, approve paper trading, approve live trading, or claim profitability. Sources: ../../AGENTS.md; ../06-data-requirements-and-vendors/DECISION.md; ../11-risk-controls-and-compliance/DECISION.md.

## Open Questions

Which `epsilon` proxy should become the default: volatility decay, spread recovery, depth recovery, or a filtered latent decay rate?

Can `D_0` and `nu_t / sigma_q` be separated empirically, or should Phase 2 estimate only an effective diffusion?

How much out-of-sample improvement is required before turbulence variables become required features?

What event-time binning preserves enough information for Hawkes calibration while staying CPU-friendly?

How should exogenous news forcing enter a calibration report without leaking future information?
