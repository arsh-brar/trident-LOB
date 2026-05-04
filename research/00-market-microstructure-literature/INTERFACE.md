# Market Microstructure Interface Notes

## Purpose

This Phase 0 interface note describes research-facing contracts only. It does not define production code, live-trading code, broker adapters, or execution logic.

## Data Concepts

Recommendation: Keep bars, top-of-book quotes, depth snapshots, message-level events, trades, and news as separate conceptual inputs because they support different validation claims. Sources: Gould et al. LOB review, https://doi.org/10.1080/14697688.2013.803148; Nasdaq TotalView-ITCH specification, https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf; LOBSTER data structure, https://lobsterdata.com/info/DataStructure.php.

Required conceptual records:

| Record | Fields | Why it matters | Sources |
| --- | --- | --- | --- |
| Bar | symbol, timestamp, open, high, low, close, volume, vwap when available | Phase 1 fallback for returns, realized volatility, and volume-volatility facts | Cont stylized facts: https://doi.org/10.1080/713665670 |
| TopOfBookQuote | symbol, timestamp, bid_price, ask_price, bid_size, ask_size | Spread, top depth, OFI proxy, queue imbalance | Cont, Kukanov, Stoikov: https://arxiv.org/abs/1011.6402 |
| DepthSnapshot | symbol, timestamp, side, price_level, price, size | Visible liquidity field approximation | Gould et al.: https://doi.org/10.1080/14697688.2013.803148 |
| MessageEvent | symbol, timestamp, event_type, order_id when available, side, price, size | Source, sink, execution accounting and queue replay | Nasdaq TotalView-ITCH: https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf; LOBSTER: https://lobsterdata.com/info/DataStructure.php |
| Trade | symbol, timestamp, price, size, aggressor_side when available | Execution sink and signed trade imbalance | Cont, Kukanov, Stoikov: https://arxiv.org/abs/1011.6402 |
| NewsEvent | timestamp, symbol or market scope, source, relevance, sentiment, novelty, decay parameters | Exogenous forcing candidate, clearly separated from endogenous order flow | TRIDENT model specification: ../../docs/TRIDENT_LOB_MODEL.md |

## Feature Groups

Recommendation: Treat feature groups as swappable research modules so simple baselines and TRIDENT hypotheses can be evaluated independently. Sources: repo modularity policy in ../../AGENTS.md; zero-intelligence baseline support from Cont, Stoikov, Talreja, https://doi.org/10.1287/opre.1090.0780.

| Feature group | Inputs | Outputs | Literature role |
| --- | --- | --- | --- |
| SpreadDepthFeatures | top-of-book, depth snapshots | spread, midprice, top depth, depth imbalance | Core LOB state, https://doi.org/10.1080/14697688.2013.803148 |
| OFIFeatures | top-of-book quote changes | OFI, normalized OFI | Required short-horizon baseline, https://arxiv.org/abs/1011.6402 |
| SourceSinkFeatures | messages or depth deltas | limit arrival rate, cancellation rate, execution rate | Zero-intelligence and stochastic LOB baseline, https://doi.org/10.1287/opre.1090.0780 |
| QueueReactiveFeatures | messages, top queues | queue-conditioned event risks | Queue-reactive benchmark, https://arxiv.org/abs/1312.0563 |
| HawkesFeatures | timestamped events | excitation intensity, decay state, branching-like diagnostics | Event clustering benchmark, https://arxiv.org/abs/1502.04592 |
| LatentBookFeatures | trades, quotes, depth, impact windows | latent slope proxy, interface pressure proxy | Latent liquidity and impact benchmark, https://arxiv.org/abs/1412.0141 |
| TurbulenceFeatures | returns, OFI, depth, event rates, news | `k`, `epsilon`, `k^2 / epsilon`, market Reynolds proxy | Original TRIDENT hypothesis, ../../docs/TRIDENT_LOB_MODEL.md |

## Output Contracts

Recommendation: Every feature row should include `asof_timestamp`, `prediction_timestamp`, `symbol`, `horizon`, and `data_cutoff_timestamp` to prevent future data leakage. Source: repo no-future-data policy in ../../AGENTS.md; short-horizon OFI timing concern from Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402.

Research outputs:

| Output | Required fields | Notes |
| --- | --- | --- |
| FeatureFrame | symbol, asof_timestamp, horizon, feature_name columns, data_cutoff_timestamp | Must be computable without future data. |
| TargetFrame | symbol, asof_timestamp, horizon, target_name, target_value | Targets must begin after `asof_timestamp`. |
| ValidationReport | dataset_id, symbol_set, date_range, split_policy, metrics, leakage_checks, stylized_fact_checks | Must include baseline comparisons. |
| LiteratureTrace | decision_id, claim_type, source_url, affected_feature_or_test | Connects recommendations to sources. |

## Minimum Phase 1 Interface

Recommendation: Start with a small CPU-only interface using bars and top-of-book quotes, because these support spread, midprice returns, top depth, OFI, and realized volatility without requiring L3 reconstruction. Sources: Cont, Kukanov, Stoikov, https://arxiv.org/abs/1011.6402; Cont stylized facts, https://doi.org/10.1080/713665670; TRIDENT model specification, ../../docs/TRIDENT_LOB_MODEL.md.

Minimum Phase 1 inputs:

1. Bars.
2. Top-of-book quotes.
3. Trades if aggressor side is available or can be conservatively classified.
4. Optional timestamped news scores.

Minimum Phase 1 feature outputs:

1. Spread and midprice return.
2. OFI or OFI proxy.
3. Top-book depth and depth imbalance.
4. Realized volatility proxy for `k`.
5. Volatility or spread-recovery proxy for `epsilon`.
6. Fragility proxy `k^2 / epsilon`.
7. Optional news forcing state.

## Phase 2 Interface Extensions

Recommendation: Add L2/L3 replay only after Phase 1 baselines and leakage checks are stable, because event-level models require message data and careful queue accounting. Sources: Nasdaq TotalView-ITCH, https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf; LOBSTER data structure, https://lobsterdata.com/info/DataStructure.php; Huang, Lehalle, Rosenbaum, https://arxiv.org/abs/1312.0563.

Phase 2 additions:

1. Event replay adapter.
2. Queue state reconstruction.
3. Source, cancellation, and execution accounting.
4. Queue-reactive event model benchmark.
5. Hawkes event-clustering benchmark.
6. Impact-window builder for latent book tests.

## Non-Goals

1. No live trading.
2. No broker API integration.
3. No trading signal deployment.
4. No claim of profitability.
5. No production PDE solver in this research folder.

Sources for these boundaries: repo policy in ../../AGENTS.md; TRIDENT scope note in ../../docs/TRIDENT_LOB_MODEL.md.
