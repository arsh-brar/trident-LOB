# Data Validation Plan

Date checked: 2026-05-04.

This document defines validation gates for research data only. It does not permit live trading.

## Gate 1: Source And License Inventory

Pass criteria:

1. Every dataset has `provider`, `dataset`, `license_class`, `entitlement`, `delay_class`, `redistribution_allowed`, and `source_url`.
2. Paid data and credentials are not committed.
3. The run manifest records the vendor plan and date checked.

Recommendation: block ingestion if the license class is unknown, because Databento, Nasdaq, LOBSTER, IBKR, Alpaca, and Massive each differentiate plans, entitlements, or usage rights. Sources: https://databento.com/pricing, https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview, https://lobsterdata.com/info/AccessOptions.php, https://www.interactivebrokers.com/en/pricing/market-data-pricing.php?menu=A, https://alpaca.markets/data, https://massive.com/pricing?product=stocks.

## Gate 2: Timestamp And Ordering

Pass criteria:

1. Each record has a UTC event timestamp and ingestion timestamp.
2. L2/L3 streams preserve sequence or update IDs.
3. Timestamps are never rounded before storage.
4. Provider timestamp semantics are documented.

Recommendation: reject L2/L3 replay if a sequence gap is detected. Binance requires restart when a diff-depth update has `U` greater than local update ID plus 1, and Nasdaq TotalView help notes identical timestamps can require tracking numbers. Sources: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams, https://help.data.nasdaq.com/article/957-how-is-the-tracking-number-under-the-nasdaq-totalview-itch-feed-used.

Recommendation: store timestamp precision metadata because Databento provides nanosecond fields, LOBSTER timestamps vary from millisecond to nanosecond depending on period, and Kraken book timestamps have microsecond precision but are not unique across price levels. Sources: https://databento.com/equities, https://lobsterdata.com/info/DataStructure.php, https://docs.kraken.com/api/docs/websocket-v1/book/.

## Gate 3: Calendar And Session Integrity

Pass criteria:

1. No bar, quote, trade, or order event is used outside the validated session unless explicitly marked premarket, after-hours, overnight, or 24/7 crypto.
2. Early closes and holidays are represented.
3. Calendar source is versioned in the run manifest.

Recommendation: use official exchange calendars as authority and `exchange_calendars` only as a local helper. Sources: https://www.nyse.com/markets/hours-calendars, https://pypi.org/project/exchange-calendars/.

## Gate 4: Corporate Action Integrity

Pass criteria:

1. Raw prices are preserved.
2. Adjusted prices include adjustment policy and as-of date.
3. Splits, dividends, ticker changes, and symbol mappings are point-in-time.

Recommendation: never mix adjusted and unadjusted data in one feature table. Massive states stock flat files are unadjusted, while adjusted data can be requested via REST or applied manually from splits. Alpaca documents symbol rename behavior and an `asof` parameter for historical endpoints. Sources: https://massive.com/docs/flat-files/stocks/overview?assetClass=stocks&license=personal&name=stocks_basic, https://docs.alpaca.markets/docs/market-data-faq.

## Gate 5: Feed Coverage And Delay Disclosure

Pass criteria:

1. Every feature row includes feed coverage: IEX-only, SIP, direct prop feed, broker non-consolidated, crypto venue, or reconstructed.
2. Every feature row includes delay class: real-time, delayed, end-of-day, historical archive, or replay.
3. Backtests cannot compare models across different feed coverage without explicit stratification.

Recommendation: do not combine Alpaca IEX-only and SIP data as if they are equivalent. Alpaca shows IEX is a single exchange and SIP covers consolidated US exchanges with materially different trade counts and volumes. Sources: https://docs.alpaca.markets/docs/historical-stock-data-1, https://docs.alpaca.markets/docs/market-data-faq.

Recommendation: label IBKR free Cboe One/IEX data as non-consolidated. IBKR states free streaming US stock and ETF data from Cboe One and IEX is non-consolidated. Source: https://www.interactivebrokers.com/en/pricing/market-data-pricing.php?menu=A.

## Gate 6: Order Book Accounting

Pass criteria:

1. L2/L3 replay must reconstruct nonnegative book sizes.
2. Executions cannot consume more displayed size than available within the chosen data semantics.
3. Add, cancel, modify, execute, clear, and halt events are counted separately.
4. Reconstructed top-of-book from depth must match quote records when both are available.

Recommendation: use LOBSTER or Databento MBO as the accounting reference for source/sink validation because both preserve event-level order book semantics. Sources: https://lobsterdata.com/info/DataStructure.php, https://lobsterdata.com/info/HowDoesItWork.php, https://databento.com/equities.

## Gate 7: Rate Limit And Budget Control

Pass criteria:

1. Every adapter has a token-bucket or vendor-specific pacing policy.
2. Paid data adapters require a maximum dollar budget per run.
3. Historical batch requests estimate cost before download where the provider supports it.
4. Broker API historical requests obey pacing limits.

Recommendation: Databento requests should use its cost estimation and budget monitoring before large downloads. Sources: https://databento.com/equities, https://databento.com/pricing.

Recommendation: IBKR historical ingestion must be throttled because IBKR documents 50 simultaneous historical requests and pacing violations above 60 requests within 10 minutes. Source: https://interactivebrokers.github.io/tws-api/historical_limitations.html.

Recommendation: crypto websocket adapters must enforce exchange-specific limits before connection. Binance documents 5 incoming messages/sec and 1,024 streams/connection, Coinbase documents websocket request and subscription limits, and Kraken documents public REST rate guidance. Sources: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams, https://docs.cdp.coinbase.com/exchange/websocket-feed/rate-limits, https://support.kraken.com/hc/en-us/articles/206548367-what-are-the-API-rate-limits-.

## Gate 8: No Future Data

Pass criteria:

1. Feature builders can only use records with `event_ts_utc <= decision_ts_utc`.
2. Corporate action adjustments must be as-of controlled.
3. News must use publication timestamp, not scrape or ingestion timestamp, unless ingestion lag is explicitly modeled.
4. Calendar closures must be known as of the run date for historical simulation.

Recommendation: point-in-time `asof` handling must be a first-class interface field because Alpaca documents symbol rename behavior where latest and historical endpoints differ. Source: https://docs.alpaca.markets/docs/market-data-faq.

## Gate 9: Mac M3 Secret Hygiene

Pass criteria:

1. No secret values in git status, logs, notebooks, test fixtures, or markdown.
2. `.env.example` contains variable names only.
3. Runtime credentials are read from macOS Keychain, a password manager CLI, or environment variables.
4. Paper and live credentials are separate.

Recommendation: store secrets outside the repository using macOS Keychain or a password manager CLI, and never write paid data credentials into project files. Sources: https://support.apple.com/guide/keychain-access/welcome/mac, https://developer.1password.com/docs/cli, https://www.tiingo.com/kb/article/where-to-find-your-tiingo-api-token/.

## Gate 10: Suitability Labels

Pass criteria:

Each dataset is labeled as one or more of:

`engineering_fixture`, `phase1_research`, `paper_trading`, `serious_l2_validation`, `full_l3_verification`, `not_for_live_trading`.

Recommendation: only LOBSTER, Databento MBO, or direct Nasdaq TotalView-ITCH-style data should receive `full_l3_verification`. Sources: https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities, https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview.
