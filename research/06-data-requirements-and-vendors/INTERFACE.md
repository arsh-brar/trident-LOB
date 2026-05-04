# Data Interface Requirements

Date checked: 2026-05-04.

This is a Phase 0 interface plan, not production code.

## Provider-Neutral Records

Recommendation: every data adapter should emit normalized records with raw vendor payload retained separately for audit. This is necessary because providers differ on timestamps, adjustment behavior, depth semantics, and entitlements. Sources: https://databento.com/equities, https://docs.alpaca.markets/docs/market-data-faq, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams.

### BarRecord

Required fields: `provider`, `dataset`, `symbol`, `venue`, `feed`, `start_ts_utc`, `end_ts_utc`, `timeframe`, `open`, `high`, `low`, `close`, `volume`, `vwap`, `trade_count`, `adjustment_policy`, `asof_date`, `ingested_at_utc`, `source_url`.

Notes: Alpaca minute bars use the left side of the interval, and SIP trade timestamps are truncated to the minute for minute bars. Source: https://docs.alpaca.markets/docs/market-data-faq.

### TradeRecord

Required fields: `provider`, `dataset`, `symbol`, `venue`, `feed`, `event_ts_utc`, `receive_ts_utc`, `exchange_ts_utc`, `sequence`, `trade_id`, `price`, `size`, `conditions`, `aggressor_side`, `is_correction`, `raw_payload_ref`.

Notes: aggressor side may be direct, absent, or inferred. Databento states SIP data does not provide buyer/seller initiation while direct prop feeds can provide it. Source: https://databento.com/equities.

### QuoteRecord

Required fields: `provider`, `dataset`, `symbol`, `venue`, `feed`, `event_ts_utc`, `receive_ts_utc`, `sequence`, `bid_price`, `bid_size`, `ask_price`, `ask_size`, `bid_exchange`, `ask_exchange`, `is_nbbo`, `delay_class`, `raw_payload_ref`.

Notes: feed and delay class are mandatory because Alpaca IEX and SIP can differ materially, and IBKR distinguishes live, frozen, delayed, and delayed frozen market data. Sources: https://docs.alpaca.markets/docs/historical-stock-data-1, https://interactivebrokers.github.io/tws-api/market_data_type.html.

### DepthRecord

Required fields: `provider`, `dataset`, `symbol`, `venue`, `feed`, `event_ts_utc`, `receive_ts_utc`, `sequence`, `side`, `price`, `size`, `level`, `depth_type`, `action`, `order_count`, `checksum`, `raw_payload_ref`.

Notes: `depth_type` values should include `mbp_1`, `mbp_10`, `l2_snapshot`, `l2_delta`, `mbo`, and `lobster_orderbook`. Databento uses MBP-1, MBP-10, and MBO schemas. Binance has snapshot plus diff depth update semantics. Sources: https://databento.com/equities, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams.

### OrderEventRecord

Required fields: `provider`, `dataset`, `symbol`, `venue`, `event_ts_utc`, `receive_ts_utc`, `sequence`, `order_id`, `event_type`, `side`, `price`, `size`, `visible`, `match_id`, `reason`, `raw_payload_ref`.

Notes: this is the key record for source/sink verification. LOBSTER message files include time, event type, order ID, size, price, and direction. Databento MBO includes order ID and action fields. Sources: https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities.

### CorporateActionRecord

Required fields: `provider`, `symbol`, `effective_date`, `action_type`, `split_ratio`, `cash_amount`, `currency`, `raw_symbol`, `new_symbol`, `source_url`, `ingested_at_utc`.

Notes: historical backtests must either store raw prices plus adjustment metadata or store adjusted prices with the adjustment policy. Massive flat files are unadjusted, with adjusted retrieval available through REST or manual split endpoint use. Source: https://massive.com/docs/flat-files/stocks/overview?assetClass=stocks&license=personal&name=stocks_basic.

### NewsEventRecord

Required fields: `provider`, `story_id`, `published_ts_utc`, `received_ts_utc`, `symbols`, `source_name`, `headline`, `url`, `summary`, `sentiment`, `relevance`, `novelty_group`, `market_wide_flag`, `raw_payload_ref`.

Notes: news must be timestamped and point-in-time. The TRIDENT model treats news as an exogenous forcing stream `N_t`.

### CalendarRecord

Required fields: `calendar_id`, `session_date`, `open_ts_utc`, `close_ts_utc`, `is_open`, `is_early_close`, `holiday_name`, `source_url`, `verified_at_utc`.

Notes: use official NYSE/Nasdaq schedules as the authority and local libraries as helpers. Sources: https://www.nyse.com/markets/hours-calendars, https://pypi.org/project/exchange-calendars/.

## Adapter Capabilities

Each provider adapter must declare:

`supports_bars`, `supports_trades`, `supports_quotes`, `supports_l2`, `supports_l3`, `supports_news`, `supports_corporate_actions`, `supports_calendar`, `historical_supported`, `streaming_supported`, `paper_trading_supported`, `live_trading_supported`.

Each adapter must also declare:

`min_timestamp_precision`, `timestamp_semantics`, `delay_class`, `venue_coverage`, `rate_limit_policy`, `license_class`, `redistribution_allowed`, `requires_paid_entitlement`, `credential_names`.

Recommendation: adapters should refuse to run if a requested feature requires paid entitlements that are not present in config. Sources: https://docs.alpaca.markets/docs/market-data-faq, https://www.interactivebrokers.com/campus/ibkr-api-page/market-data-subscriptions/, https://databento.com/pricing.

## Storage Interfaces

Recommendation: store normalized data partitioned by `provider`, `dataset`, `symbol`, `date`, and `record_type`, and store raw payloads separately by content hash. This supports auditability and avoids mixing adjusted and unadjusted data. Sources: https://massive.com/docs/flat-files/stocks/overview?assetClass=stocks&license=personal&name=stocks_basic, https://databento.com/equities.

Recommendation: L2/L3 event stores must preserve sequence numbers and support replay from snapshot plus deltas. Binance documents a strict snapshot plus buffered diff-depth procedure, and LOBSTER orderbook rows are driven by message rows. Sources: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams, https://lobsterdata.com/info/DataStructure.php.

## Credential Interface

Required environment variable names:

`TRIDENT_ALPACA_KEY_ID`, `TRIDENT_ALPACA_SECRET_KEY`, `TRIDENT_DATABENTO_API_KEY`, `TRIDENT_MASSIVE_API_KEY`, `TRIDENT_TIINGO_API_KEY`, `TRIDENT_FINNHUB_API_KEY`, `TRIDENT_IBKR_ACCOUNT_ALIAS`.

Recommendation: do not define live broker order credentials for Phase 0. If later phases need them, use separate variable names with `LIVE` in the name and validation gates that block use by default. Sources: https://support.apple.com/guide/keychain-access/welcome/mac, https://developer.1password.com/docs/cli, https://alpaca.markets/data.
