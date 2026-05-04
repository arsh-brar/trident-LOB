# Data Vendor Decision

Date checked: 2026-05-04.

## Decision

Adopt a two-stage data plan.

1. Phase 1 default: build provider-neutral interfaces using Alpaca Free plus Massive Basic and public crypto order book fixtures. This is enough for CPU-only Mac M3 development of adapters, event schemas, bars, top-book features, calendar handling, corporate action joins, and baseline models. Sources: https://alpaca.markets/data, https://massive.com/pricing?product=stocks, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams.

2. Phase 1 serious evaluation: add one paid top-of-book source, either Alpaca Algo Trader Plus at $99/mo or Massive Advanced at $199/mo, or Databento usage-based MBP-1/TBBO/trades for fixed historical windows. Sources: https://alpaca.markets/data, https://massive.com/pricing?product=stocks, https://databento.com/equities, https://databento.com/pricing.

3. Full TRIDENT verification: use LOBSTER if academic access is available, otherwise use Databento MBO/MBP-10/definitions/imbalance for a small paid pilot. Sources: https://lobsterdata.com/info/AccessOptions.php, https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities, https://databento.com/pricing.

## Why

Free data can build the system, but it cannot verify the turbulent reaction-diffusion source/sink model. Alpaca Free is IEX-only for live equities, and Massive Basic is limited to free aggregate/reference use. Full source/sink estimation requires L2/L3 order-book data with add, cancel, modify, and execution events. Sources: https://docs.alpaca.markets/docs/historical-stock-data-1, https://docs.alpaca.markets/docs/market-data-faq, https://massive.com/pricing?product=stocks, https://lobsterdata.com/info/HowDoesItWork.php.

Databento is the preferred commercial research source because it lists L3 MBO, L2 MBP-10, L1 MBP-1/TBBO, trades, OHLCV, definitions, corporate actions, imbalances, usage-based pricing, $125 signup credits, and nanosecond timestamp fields. Sources: https://databento.com/equities, https://databento.com/pricing.

LOBSTER is the preferred academic source because it is designed around NASDAQ Historical TotalView-ITCH, provides message and orderbook CSVs, supports up to 200 levels, and lists flat-rate academic pricing. Sources: https://lobsterdata.com/info/WhatIsLOBSTER.php, https://lobsterdata.com/info/DataStructure.php, https://lobsterdata.com/info/AccessOptions.php.

Broker feeds should remain paper-trading and sanity-check sources, not primary archives, because they are entitlement-driven and paced. IBKR explicitly notes delayed/live/frozen data modes and historical request pacing. Sources: https://interactivebrokers.github.io/tws-api/market_data_type.html, https://interactivebrokers.github.io/tws-api/historical_limitations.html.

## Answers

What can be built free: the modular data adapter, event store contracts, synthetic fixtures, crypto L2 reconstruction, US equity bars and IEX top-book features, corporate action plumbing, and baseline models. This is not enough for source/sink validation. Sources: https://alpaca.markets/data, https://massive.com/pricing?product=stocks, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams.

What requires paid data: current consolidated SIP quotes and trades, full-market historical quotes/trades at scale, L2 equity depth, L3 message data, direct Nasdaq TotalView-ITCH, and serious news archives. Sources: https://docs.alpaca.markets/docs/market-data-faq, https://databento.com/equities, https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview.

Cheapest serious source/sink dataset: LOBSTER academic flat rate if eligible. If not, Databento usage-based MBO sample windows are the practical self-service choice. Sources: https://lobsterdata.com/info/AccessOptions.php, https://databento.com/pricing.

Enough data for Phase 1: bars, top-of-book quotes, trades, corporate actions, and official calendars are enough for simplified TRIDENT features, but not the full PDE/source-sink model. Sources: https://docs.alpaca.markets/docs/historical-stock-data-1, https://databento.com/equities, https://www.nyse.com/markets/hours-calendars.

Data required for full TRIDENT verification: L3 order messages, order IDs, add/cancel/modify/execution types, L2/L3 reconstructed book states, accurate event timestamps, halts, imbalances, corporate actions, symbol mapping, and news/scheduled event timestamps. Sources: https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities, https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview.

Credential storage on Mac M3: use macOS Keychain or a password manager CLI, keep secrets outside the repository, commit only `.env.example`, segregate paper and live credentials, and block live-trading credentials in Phase 0. Sources: https://support.apple.com/guide/keychain-access/welcome/mac, https://developer.1password.com/docs/cli, https://www.tiingo.com/kb/article/where-to-find-your-tiingo-api-token/.

## Non-Decision

No live-trading source is approved. No production ingestion is approved. No paid credential is requested. No claim about profitability is made.
