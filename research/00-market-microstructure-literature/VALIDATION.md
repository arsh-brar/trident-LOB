# Market Microstructure Validation Plan

## Validation Principle

Recommendation: TRIDENT-LOB must first reproduce known microstructure and return stylized facts, then beat simple baselines out-of-sample on research metrics before any downstream trading interpretation is considered. Sources: Cont stylized facts, https://doi.org/10.1080/713665670; zero-intelligence baseline sources, https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio and https://doi.org/10.1287/opre.1090.0780; repo policy in ../../AGENTS.md.

## Required Baseline Tests

| Test | Pass condition | Why | Sources |
| --- | --- | --- | --- |
| Source-sink baseline | Simple arrival, cancellation, and execution controls are reported before TRIDENT variables | Prevents complex model claims without simple baselines | Smith et al.: https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio; Cont, Stoikov, Talreja: https://doi.org/10.1287/opre.1090.0780 |
| OFI baseline | OFI or an explicit OFI proxy is included in every short-horizon price model | OFI is a documented price-pressure variable | Cont, Kukanov, Stoikov: https://arxiv.org/abs/1011.6402 |
| Volatility baseline | Realized volatility features are included before `k` and `epsilon` are interpreted | Volatility clustering is a core stylized fact | Cont: https://doi.org/10.1080/713665670 |
| Square-root impact baseline | Impact tests compare against plain square-root impact | Latent-book impact should not be judged in isolation | Donier et al.: https://arxiv.org/abs/1412.0141; Toth et al.: https://doi.org/10.1103/PhysRevX.1.021006 |
| Hawkes benchmark | Event clustering is benchmarked with Hawkes features when event data exists | Hawkes processes are standard for clustered financial events | Bacry, Mastromatteo, Muzy: https://arxiv.org/abs/1502.04592 |

## Stylized-Fact Acceptance Tests

Recommendation: Simulated, replayed, or feature-generated outputs should be rejected as a market model if they fail basic stylized-fact checks. Source: Cont, https://doi.org/10.1080/713665670.

Required checks:

1. Raw return autocorrelation is weak relative to absolute or squared return dependence. Source: Cont, https://doi.org/10.1080/713665670.
2. Return distributions are heavy-tailed at short horizons. Source: Cont, https://doi.org/10.1080/713665670.
3. Absolute or squared returns show volatility clustering. Source: Cont, https://doi.org/10.1080/713665670.
4. Trading activity and volatility are positively related. Source: Cont, https://doi.org/10.1080/713665670.
5. Spread and depth respond to order arrival, cancellation, and execution rates. Source: Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.
6. Queue depletion and near-touch event probabilities depend on current queue state when event data is used. Source: Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563.
7. Event arrivals show clustering beyond an independent Poisson process when event data is used. Source: Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592.
8. Impact is concave in order size and compared with square-root scaling. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Toth et al., https://doi.org/10.1103/PhysRevX.1.021006.

## Leakage and Time-Split Checks

Recommendation: Every validation report must include explicit `data_cutoff_timestamp`, split windows, and target construction rules to show that no future data enters features. Sources: repo no-future-data policy in ../../AGENTS.md; backtest overfitting warning from Bailey et al., https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Required checks:

1. Feature timestamps are at or before the prediction timestamp.
2. Target windows start after the prediction timestamp.
3. Rolling statistics use only prior observations.
4. News events use publication timestamps, not later revision or article-processing timestamps.
5. Corporate-action adjustments, if used later, are applied consistently without future information.

## Incremental TRIDENT Tests

Recommendation: Evaluate `k`, `epsilon`, fragility, and market Reynolds proxies as incremental variables over OFI, spread, depth, and realized volatility. Sources for required controls: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402; Cont stylized facts, https://doi.org/10.1080/713665670.

Research questions:

1. Does `fragility = k^2 / epsilon` improve next-horizon return, direction, spread-widening, or jump-probability metrics?
2. Does fragility predict larger impact for the same order size, OFI, spread, and visible depth?
3. Does `epsilon` improve recovery forecasts after volatility or spread shocks?
4. Does news forcing improve shock-period calibration after controlling for endogenous event clustering?

## Event-Level Validation

Recommendation: L2 or L3 validation should verify event accounting before fitting queue-reactive, Hawkes, or latent-interface models. Sources: Nasdaq TotalView-ITCH specification, https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf; LOBSTER data structure, https://lobsterdata.com/info/DataStructure.php.

Required checks:

1. Added limit order shares, canceled shares, and executed shares reconcile to book depth changes.
2. Executions never consume more visible quantity than available at the reconstructed queue level.
3. Bid and ask side conventions are consistent across messages, trades, and book snapshots.
4. Event-time and clock-time aggregations are both reproducible.
5. Queue-reactive event probabilities are calibrated by queue-size bins.
6. Hawkes residual diagnostics are checked when Hawkes benchmarks are used.

## Impact Validation

Recommendation: Any TRIDENT impact result should compare against square-root impact and check for no-obvious-dynamic-arbitrage behavior in simulation. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Toth et al., https://doi.org/10.1103/PhysRevX.1.021006; Gatheral, https://doi.org/10.1080/14697680903373692.

Required checks:

1. Impact versus size is concave over tested size buckets.
2. Impact is larger when fragility is high only after controlling for spread, depth, OFI, volatility, and participation rate.
3. Post-impact relaxation or reversion is reported separately from peak impact.
4. Round-trip simulations do not mechanically generate positive expected gains from the impact model alone.

## Phase Gates

1. Phase 1 research may proceed when bar and top-of-book feature tests include baseline, leakage, and stylized-fact reports.
2. Phase 2 replay may proceed when event data adapters can reconcile source, sink, and execution accounting.
3. Paper-trading discussion may proceed only after validation gates exist outside this folder and no live-trading code is introduced here.

Sources for boundaries: repo policy in ../../AGENTS.md; TRIDENT scope note in ../../docs/TRIDENT_LOB_MODEL.md.
