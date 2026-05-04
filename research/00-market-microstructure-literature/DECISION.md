# Market Microstructure Decision

## Decision

TRIDENT-LOB Phase 1 should start as a CPU-only feature and validation framework, not as a full PDE solver and not as trading code. The first empirical stack should combine simple source-sink controls, OFI, spread, top-book depth, realized volatility, and TRIDENT turbulence proxies. Recommendation: use simple and literature-supported baselines before testing original turbulence variables. Sources: Smith et al., https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio; Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402; Cont stylized facts, https://doi.org/10.1080/713665670.

## Literature-Supported Pieces

1. Visible LOB event accounting should distinguish limit order arrivals, cancellations, executions, queue state, spread, and depth. Source: Gould et al., https://doi.org/10.1080/14697688.2013.803148.
2. A simple stochastic source-sink LOB model is a valid baseline. Sources: Smith et al., https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio; Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.
3. Queue state should influence short-horizon event intensities when event-level data is available. Source: Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563.
4. OFI should be included as a required short-horizon price-pressure baseline. Source: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402.
5. Market events can cluster and excite future events, making Hawkes models useful benchmarks for event-level replay. Sources: Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592; Bowsher, https://doi.org/10.1016/j.jeconom.2006.11.007; Large, https://doi.org/10.1016/j.finmar.2006.09.001.
6. Latent liquidity is a plausible modeling layer and square-root impact is a required impact benchmark. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Toth et al., https://doi.org/10.1103/PhysRevX.1.021006.
7. Simulated or replayed output should reproduce stylized facts including fat tails, volatility clustering, weak raw-return autocorrelation, and activity-volatility relationships. Source: Cont, https://doi.org/10.1080/713665670.

## Original TRIDENT Hypotheses

1. `k` can be interpreted as market turbulent energy and estimated from realized volatility, event intensity, or quote-motion variance.
2. `epsilon` can be interpreted as dissipation or resilience and estimated from volatility decay, spread recovery, or depth recovery.
3. `k^2 / epsilon` is a fragility variable that should predict larger impact or higher jump probability for the same OFI and visible depth.
4. A market Reynolds number can summarize whether imbalance is absorbed or amplified by weak dissipation.
5. News forcing can enter as an exogenous production term for `k`, with source reliability, relevance, sentiment, novelty, and decay.

These are original research claims from the TRIDENT model specification, not established facts. They should be tested only as incremental explanatory variables over literature baselines. Source for TRIDENT specification: ../../docs/TRIDENT_LOB_MODEL.md. Sources for the baselines that must be controlled: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402; Cont, https://doi.org/10.1080/713665670; Donier et al., https://arxiv.org/abs/1412.0141.

## Accepted Phase 1 Shape

Recommendation: Phase 1 should estimate simplified state variables from bars, top-of-book quotes, trades when available, and optional news, then compare models on out-of-sample prediction tasks. Source: TRIDENT model specification, ../../docs/TRIDENT_LOB_MODEL.md; OFI baseline source: https://arxiv.org/abs/1011.6402.

Recommendation: Phase 1 should avoid full event-intensity Hawkes calibration unless event data is available, because Hawkes models are event-stream models and bars lose much of the required timing structure. Source: Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592.

Recommendation: No profitability or deployment claim should be made from Phase 1 feature tests. Any later trading interpretation requires out-of-sample, transaction-cost-adjusted evidence and validation gates. Sources: repo policy in ../../AGENTS.md; backtest overfitting warning from Bailey et al., https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253; market-impact constraints from Gatheral, https://doi.org/10.1080/14697680903373692.

## Open Questions

1. Which `epsilon` proxy is most defensible: volatility decay, spread recovery, depth replenishment, or a fitted resilience parameter?
2. Does `k^2 / epsilon` add signal after controlling for realized volatility, spread, depth, OFI, and event intensity?
3. Is the turbulence analogy useful outside stress regimes, or only during liquidity withdrawal and volatility bursts?
4. How should exogenous news be separated from endogenous Hawkes-like event excitation?
5. Can latent-interface estimates be identified with top-of-book data, or is L2/L3 data required?
6. What horizon best matches the TRIDENT state variables: event time, 1 minute, 5 minutes, or adaptive liquidity time?

## Decision Guardrails

Recommendation: Treat TRIDENT variables as candidate features until they pass stylized-fact validation, baseline comparison, and leakage checks. Sources: Cont stylized facts, https://doi.org/10.1080/713665670; OFI baseline, https://arxiv.org/abs/1011.6402.

Boundary: Do not write live-trading code in this phase. Source: repo policy in ../../AGENTS.md.
