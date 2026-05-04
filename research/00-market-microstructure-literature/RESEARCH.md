# Market Microstructure Literature Review

## Scope

This Phase 0 review covers empirical and modeling literature relevant to TRIDENT-LOB: visible limit order book dynamics, zero-intelligence order flow, queue-reactive models, order-flow imbalance, Hawkes processes, latent order books, market impact, volatility clustering, and stylized facts. The goal is to identify what the model should reproduce before any production code, trading code, or profitability claims are considered.

## Literature Map

| Area | Core idea | TRIDENT-LOB relevance | Sources |
| --- | --- | --- | --- |
| Limit order book surveys | LOBs are event-driven systems with limit orders, cancellations, executions, queue priority, spread dynamics, and depth profiles. | Use as the domain map for event types, state variables, and validation vocabulary. | Gould et al. review: https://doi.org/10.1080/14697688.2013.803148 |
| Zero-intelligence LOB models | Order placement, cancellation, and market orders can produce realistic spread and depth regularities even without strategic agents. | Baseline source, sink, and execution model for Phase 1 and Phase 2 comparisons. | Smith et al.: https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio, Cont, Stoikov, Talreja: https://doi.org/10.1287/opre.1090.0780 |
| Queue-reactive models | Event intensities depend on current queue sizes near the best bid and ask. | Best near-term empirical bridge from top-of-book state to stochastic event rates. | Huang, Lehalle, Rosenbaum: https://arxiv.org/abs/1312.0563 |
| Order-flow imbalance | Changes in best bid and ask sizes and prices summarize short-horizon supply-demand pressure. | Direct Phase 1 proxy for imbalance forcing and price-interface drift. | Cont, Kukanov, Stoikov: https://arxiv.org/abs/1011.6402 |
| Hawkes processes | Market events cluster in time and can excite future events of same or different types. | Candidate model for clustered order arrivals, cancellations, trades, and shock decay. | Bacry, Mastromatteo, Muzy: https://arxiv.org/abs/1502.04592, Bowsher: https://doi.org/10.1016/j.jeconom.2006.11.007, Large: https://doi.org/10.1016/j.finmar.2006.09.001 |
| Latent order book | Visible depth is only part of market intention. A latent supply-demand field can explain square-root impact. | Direct precedent for TRIDENT's latent interface and effective liquidity slope. | Donier et al.: https://arxiv.org/abs/1412.0141 |
| Market impact | Impact is concave and often approximated by square-root scaling for meta-orders. No-dynamic-arbitrage constrains admissible impact models. | TRIDENT's turbulence-adjusted impact claim should be tested against square-root impact and no-arbitrage constraints. | Toth et al.: https://doi.org/10.1103/PhysRevX.1.021006, Gatheral: https://doi.org/10.1080/14697680903373692 |
| Volatility clustering and stylized facts | Returns have weak linear autocorrelation, fat tails, clustered volatility, volume-volatility dependence, and long-memory-like absolute returns. | Required empirical acceptance tests for simulated and replayed TRIDENT outputs. | Cont: https://doi.org/10.1080/713665670 |
| Empirical order-book facts | LOB depth, placement, cancellation, and trade signs have heavy-tailed and persistent behavior. | Phase 2 should validate order-level event distributions, not only price targets. | Bouchaud, Mezard, Potters: https://doi.org/10.1088/1469-7688/2/4/301 |
| Event data formats | L2 and L3 data expose different levels of queue and order identity detail. | Interface design should separate top-of-book, depth, and message-level adapters. | LOBSTER documentation: https://lobsterdata.com/info/DataStructure.php, Nasdaq TotalView-ITCH: https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf, Databento schemas: https://databento.com/docs/schemas-and-data-formats |

## Detailed Findings

### Limit order book models

The LOB literature treats the book as a high-frequency queueing system in price-time priority. Reviews emphasize that a usable LOB model must describe order submissions, cancellations, executions, spread, depth, queue priority, price changes, and event-time versus clock-time sampling. Recommendation: TRIDENT-LOB should keep event accounting and price-grid accounting separate so Phase 1 can work with bars and top-of-book data while Phase 2 can replay L2 or L3 events. Source: Gould et al., https://doi.org/10.1080/14697688.2013.803148.

### Zero-intelligence models

Zero-intelligence models show that simple Poisson-like order submissions, cancellations, and market orders can generate nontrivial spreads and depth profiles. This matters because it gives TRIDENT a hard baseline: a turbulent closure should add explanatory value beyond source, sink, and execution rates. Recommendation: Phase 1 reports should compare TRIDENT features against a zero-intelligence or source-sink baseline before adding complex learned components. Sources: Smith et al., https://www.santafe.edu/research/results/working-papers/statistical-theory-of-the-continuous-double-auctio; Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.

### Queue-reactive models

Queue-reactive models condition event intensities on current queue sizes, especially at the best bid and ask. They are a strong fit for top-of-book and shallow-depth Phase 1 because they do not require a full latent field to estimate near-term event risk. Recommendation: TRIDENT's first event-intensity layer should include queue-size conditioned baselines for market order, limit order, and cancellation risks when such data exists. Source: Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563.

### Order-flow imbalance

Order-flow imbalance, or OFI, summarizes changes in bid and ask prices and sizes into a signed pressure variable. Cont, Kukanov, and Stoikov find OFI explains short-horizon price changes better than trade imbalance alone. Recommendation: Phase 1 must include OFI as a required baseline feature and should test whether `fragility = k^2 / epsilon` adds incremental out-of-sample explanatory power over OFI and spread-depth controls. Source: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402.

### Hawkes processes

Hawkes processes model self-excitation and cross-excitation in event streams, which is useful for clustered trades, cancellations, quote changes, and volatility bursts. Recommendation: Hawkes or marked Hawkes features should be considered a Phase 2 benchmark for clustered source, sink, and execution events, but not a Phase 1 dependency unless event-level data is available. Sources: Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592; Bowsher, https://doi.org/10.1016/j.jeconom.2006.11.007; Large, https://doi.org/10.1016/j.finmar.2006.09.001.

### Latent order book models

Latent order book models separate unobserved trading intentions from visible displayed liquidity. Donier et al. derive a locally linear latent book and square-root impact under a minimal model. Recommendation: TRIDENT's latent interface should be treated as a hypothesis-constrained state estimate, not as directly observed truth, and should be validated through impact, spread, and reversal behavior. Source: Donier et al., https://arxiv.org/abs/1412.0141.

### Market impact

The square-root impact law is a strong empirical and theoretical reference point, while no-dynamic-arbitrage arguments constrain impact models that would otherwise create mechanical price manipulation. Recommendation: TRIDENT's turbulence-adjusted impact formula should be evaluated against a plain square-root impact baseline and checked for no-obvious-dynamic-arbitrage behavior in simulation before any paper-trading adapter is enabled. Sources: Toth et al., https://doi.org/10.1103/PhysRevX.1.021006; Gatheral, https://doi.org/10.1080/14697680903373692.

### Volatility clustering

Stylized facts establish that asset returns have fat tails, weak raw-return autocorrelation, volatility clustering, leverage effects in some markets, and volume-volatility relationships. Recommendation: TRIDENT synthetic or replay outputs should pass stylized-fact checks before being used for downstream prediction claims. Source: Cont, https://doi.org/10.1080/713665670.

## Empirical Facts TRIDENT-LOB Must Reproduce

1. Weak linear autocorrelation of raw returns at liquid-market horizons, with stronger dependence in absolute or squared returns. Source: Cont, https://doi.org/10.1080/713665670.
2. Heavy-tailed return distributions at short horizons, with tails that become less extreme as the horizon increases. Source: Cont, https://doi.org/10.1080/713665670.
3. Volatility clustering, where high-volatility periods tend to follow high-volatility periods. Source: Cont, https://doi.org/10.1080/713665670.
4. Positive relationship between trading activity, volume, and volatility. Source: Cont, https://doi.org/10.1080/713665670.
5. Bid-ask spread and depth should vary with order arrival, cancellation, and execution rates. Source: Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.
6. OFI should explain a meaningful part of short-horizon price changes in event-time or short clock-time windows. Source: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402.
7. Event arrivals should show clustering and excitation beyond independent Poisson arrivals, especially around active periods. Sources: Bacry, Mastromatteo, Muzy, https://arxiv.org/abs/1502.04592; Bowsher, https://doi.org/10.1016/j.jeconom.2006.11.007.
8. Queue size at the best bid and ask should affect probabilities of depletion, price moves, cancellations, and new limit order placement. Source: Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563.
9. Market impact should be concave in meta-order size and benchmarked against square-root impact. Sources: Donier et al., https://arxiv.org/abs/1412.0141; Toth et al., https://doi.org/10.1103/PhysRevX.1.021006.
10. Visible depth alone should not be treated as full available liquidity because latent liquidity and hidden intention matter. Source: Donier et al., https://arxiv.org/abs/1412.0141.

## Data Implications

Recommendation: Phase 1 can start with bars, top-of-book quotes, trades, and delayed news scores because TRIDENT's first simplified features can be estimated from spread, midprice returns, top-book depth, OFI proxies, realized volatility, and news forcing. Sources: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402; TRIDENT model specification, ../../docs/TRIDENT_LOB_MODEL.md.

Recommendation: Phase 2 should use L2 or L3 data for source, sink, queue, and execution accounting. Message-level feeds such as Nasdaq TotalView-ITCH and normalized MBO/MBP schemas support this type of validation better than bars alone. Sources: Nasdaq TotalView-ITCH, https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf; Databento schemas, https://databento.com/docs/schemas-and-data-formats; LOBSTER data structure, https://lobsterdata.com/info/DataStructure.php.

## Phase 0 Boundaries

This document makes no live-trading recommendation, includes no trading code, and makes no profitability claim. All model claims above are research hypotheses or literature-supported validation requirements.
