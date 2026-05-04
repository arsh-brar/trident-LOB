# Data Vendor Options

Date checked: 2026-05-04.

## Option A: Free Phase 1 Scaffold

Use Alpaca Free for IEX trades, quotes, bars, snapshots, corporate actions, and 30 websocket symbols; use Massive Basic for free EOD, reference, corporate actions, technical indicators, and minute aggregates; use public crypto exchange order books as local replay fixtures.

Cost: $0/month for listed vendor tiers, excluding storage and compute. Alpaca Free lists $0/mo, 200 API calls/min, IEX, 7+ years history, and 30 websocket symbols. Massive Basic lists $0/mo, 5 calls/min, 2 years history, EOD, reference, corporate actions, and minute aggregates. Binance, Coinbase, and Kraken expose public order book market data with rate limits. Sources: https://alpaca.markets/data, https://massive.com/pricing?product=stocks, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams, https://docs.cdp.coinbase.com/exchange/websocket-feed/rate-limits, https://docs.kraken.com/api/docs/websocket-v1/book/.

Pros: cheapest, enough to build adapters, event store contracts, baselines, no paid data handling, CPU-only friendly.

Cons: Alpaca Free is IEX-only for live equities, Massive Basic is limited to 5 calls/min, crypto market structure is not US equity market structure, and there is no full US equity L2/L3 source/sink validation.

Recommendation: choose this only for Phase 0 and very early Phase 1 interface work, and label all results as engineering checks rather than evidence for TRIDENT market microstructure claims. Sources: https://docs.alpaca.markets/docs/historical-stock-data-1, https://docs.alpaca.markets/docs/market-data-faq, https://massive.com/pricing?product=stocks.

## Option B: Low-Cost Consolidated Phase 1

Use Alpaca Algo Trader Plus or Massive Advanced for consolidated recent US equity quotes/trades plus bars, and use official exchange calendar validation with `exchange_calendars`.

Cost: Alpaca Algo Trader Plus is listed at $99/mo with all US exchanges, unlimited API calls, unlimited websocket symbols, and 7+ years history. Massive Advanced is listed at $199/mo with real-time data, trades, quotes, 20+ years history, corporate actions, and financials/ratios. Sources: https://alpaca.markets/data, https://massive.com/pricing?product=stocks.

Pros: enough for credible Phase 1 top-of-book features, backtests over historical bars and trades, paper-trading feed alignment, and corporate action handling.

Cons: still not L2/L3. Cannot estimate cancellation sinks or queue composition directly.

Recommendation: use this option if the immediate goal is a serious Phase 1 predictor with spread, midprice, top-book depth, trade flow, and corporate actions, but keep TRIDENT PDE/source-sink verification out of scope. Sources: https://alpaca.markets/data, https://massive.com/docs/flat-files/stocks/overview?assetClass=stocks&license=personal&name=stocks_basic.

## Option C: Paid Historical L2/L3 Research Slice

Use Databento usage-based historical data for Nasdaq TotalView-ITCH or other direct equity feeds. Pull only a few symbols and days in MBO, MBP-10, MBP-1, trades, definitions, and imbalance schemas.

Cost: Databento lists pay-as-you-go historical pricing, $125 signup credits, US equities historical from $0.40/GB, and Standard at $199/mo. Databento pricing examples show Nasdaq TotalView-ITCH MBO, MBP-1, TBBO, and trades can fit meaningful sample windows into signup credits. Sources: https://databento.com/equities, https://databento.com/pricing.

Pros: best self-service route for high-fidelity paid research. Provides L3 MBO, L2 MBP-10, L1 MBP-1/TBBO, trades, definitions, imbalances, and nanosecond timestamps.

Cons: requires paid account and licensing workflow. Data volume can grow quickly and must be budget-limited.

Recommendation: make this the default paid source for a serious TRIDENT Phase 2 pilot if LOBSTER academic access is not available. Sources: https://databento.com/equities, https://databento.com/pricing.

## Option D: LOBSTER Academic Deep Dive

Use LOBSTER if the project has eligible academic access. Pull NASDAQ symbols, event messages, and reconstructed order books at selected depth levels.

Cost: LOBSTER academic flat rate is listed at 4,798 EUR/year excluding VAT, with 10 accounts, 1,000 GB server storage, up to 200 price levels, no restrictions on tickers, requests, or periods. Source: https://lobsterdata.com/info/AccessOptions.php.

Pros: purpose-built for limit order book research, clear CSV message/orderbook structure, order IDs, event types, up to nanosecond timestamps depending on period, and full NASDAQ stock universe coverage.

Cons: academic licensing conditions, NASDAQ-only scope, not real-time, and no built-in news/corporate actions.

Recommendation: use LOBSTER as the cheapest serious source/sink dataset if eligible, then supplement with a separate corporate action and news source. Sources: https://lobsterdata.com/info/WhatIsLOBSTER.php, https://lobsterdata.com/info/DataStructure.php, https://lobsterdata.com/info/AccessOptions.php.

## Option E: Broker Feed For Paper Trading

Use Alpaca or IBKR for paper-trading feed alignment and broker adapter experiments, while keeping research archives separate.

Cost: Alpaca Free or Algo Trader Plus pricing is public. IBKR provides free non-consolidated real-time streaming data from Cboe One and IEX for US-listed stocks and ETFs, delayed data where available, and paid exchange subscriptions such as US Equity and Options Add-On Streaming Bundle at $4.50 non-pro and Cboe BZX L2 at $8 non-pro. Sources: https://alpaca.markets/data, https://www.interactivebrokers.com/en/pricing/market-data-pricing.php?menu=A.

Pros: paper-trading realism, operational integration, account and order event handling.

Cons: broker APIs have pacing limits, entitlements, non-display restrictions, and are not specialized historical research archives. IBKR historical API pacing includes no more than 60 requests within 10 minutes and 50 simultaneous historical requests. Sources: https://interactivebrokers.github.io/tws-api/historical_limitations.html, https://interactivebrokers.github.io/tws-api/market_data_type.html.

Recommendation: use broker feeds only after the research event schema is stable, and never use broker feed behavior as proof of TRIDENT profitability or full source/sink correctness. Sources: https://www.interactivebrokers.com/campus/ibkr-api-page/market-data-subscriptions/, https://docs.alpaca.markets/docs/market-data-faq.

## Option F: Public Crypto Order Book Sandbox

Use Binance, Coinbase Exchange, and Kraken public order books to test event store throughput, sequence handling, L2 reconstruction, and book validation.

Cost: free public market data, subject to exchange limits. Binance REST depth supports up to 5,000 entries, websocket diff depth updates at 1000ms or 100ms, and websocket limits include 5 incoming messages/sec and 1,024 streams/connection. Coinbase Exchange websocket limits include 8 requests/sec/IP, bursts to 20, and 10 subscriptions per product/channel unless paid. Kraken websocket book supports 10, 25, 100, 500, and 1,000 depth levels. Sources: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams, https://docs.cdp.coinbase.com/exchange/websocket-feed/rate-limits, https://docs.kraken.com/api/docs/websocket-v1/book/.

Pros: free L2-like depth engineering and 24/7 data. Useful for CPU-only Mac M3 replay and correctness tests.

Cons: not US equities, no NMS, different matching rules, different fees, and no corporate actions.

Recommendation: use crypto only as an engineering sandbox, not as final TRIDENT equity validation. Sources: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams, https://docs.kraken.com/api/docs/websocket-v1/book/.
