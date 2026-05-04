# TRIDENT-LOB Data Plan

Status: Phase 0 data plan. This plan does not approve paid data purchases or credential storage in the repository.

## 1. Free-Start Path

Build adapters, schemas, fixtures, bars, L1-style features, calendar joins, corporate action handling, and baseline models using Alpaca Free, Massive Basic aggregates and reference data, SEC EDGAR APIs, official macro calendars, and public crypto L2 fixtures. This is enough for Phase 1 engineering and feature validation, not full TRIDENT source/sink verification. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), https://alpaca.markets/data, https://massive.com/pricing?product=stocks, https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams.

## 2. Low-Cost Path

For serious Phase 1 evaluation, add one paid top-of-book or historical market data source such as Alpaca Algo Trader Plus, Massive Advanced, or Databento usage-based TBBO, MBP-1, and trades for fixed windows. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), https://alpaca.markets/data, https://massive.com/pricing?product=stocks, https://databento.com/pricing.

## 3. Serious L2 Or L3 Validation Path

Use LOBSTER if academic access is available. Otherwise use Databento MBO or MBP-10 for a small paid pilot. Direct Nasdaq TotalView is a later institutional path. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), https://lobsterdata.com/info/AccessOptions.php, https://lobsterdata.com/info/DataStructure.php, https://databento.com/equities, https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview.

## 4. Live Data Path For Paper Trading

Paper trading needs paper-only broker credentials, live or delayed data entitlements understood by provider terms, and explicit separation from live-trading credentials. Broker feeds should be sanity-check and paper-workflow sources, not primary research archives. Sources: [backtesting decision](../research/10-backtesting-paper-trading-and-execution/DECISION.md), [risk decision](../research/11-risk-controls-and-compliance/DECISION.md), https://docs.alpaca.markets/docs/trading/paper-trading/, https://interactivebrokers.github.io/tws-api/market_data_type.html.

## 5. News Data Path

Start with SEC EDGAR, official macro calendars, Massive stock news, and Alpha Vantage news sentiment. Upgrade later to Benzinga Newsfeed or Massive Benzinga earnings if point-in-time availability metadata and licensing support the use case. Sources: [news decision](../research/07-news-and-exogenous-inputs/DECISION.md), https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.bls.gov/schedule/news_release/, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.alphavantage.co/documentation/, https://docs.benzinga.com/api-reference/news-api/overview.

## 6. Licensing Restrictions

Every data source must be tagged as free, delayed, real-time, paid, research-only, paper-trading-suitable, or live-trading-suitable. Paid raw data, broker exports, private account data, and provider credentials must not be committed. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), [reproducibility decision](../research/14-reproducibility-and-experiment-tracking/DECISION.md), https://docs.github.com/ignore-files.

## 7. Storage Layout

```text
data/
  README.md
  manifests/
  raw/
  interim/
  processed/
  external/
  fixtures/
```

Use Parquet as canonical local storage and DuckDB for query. Store DVC metadata and dataset manifests when allowed. Do not commit large raw data, paid payloads, or secrets. Sources: [architecture decision](../research/12-python-architecture-and-stack/DECISION.md), [reproducibility decision](../research/14-reproducibility-and-experiment-tracking/DECISION.md), https://parquet.apache.org/docs/overview/, https://duckdb.org/docs/stable/clients/python/overview, https://dvc.org/doc/use-cases/versioning-data-and-models.

## 8. Estimated Storage Needs

Free-start fixtures should stay below 1 GB. Phase 1 bars, trades, and L1 quotes for a small symbol set can range from a few GB to tens of GB depending on tick frequency and history. L2 and L3 pilots can grow to tens or hundreds of GB quickly, so they require explicit manifest and DVC policy before purchase. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), [reproducibility decision](../research/14-reproducibility-and-experiment-tracking/DECISION.md).

## 9. API-Key Security Policy

Use macOS Keychain, a password manager CLI, or environment variables loaded outside the repo. Commit only `.env.example` and secret reference names. Segregate research, paper, and any future live credentials. Block live credentials in Phase 0 and Phase 1. Sources: [data decision](../research/06-data-requirements-and-vendors/DECISION.md), [risk blockers](../research/11-risk-controls-and-compliance/LIVE_TRADING_BLOCKERS.md), https://support.apple.com/guide/keychain-access/welcome/mac, https://developer.1password.com/docs/cli.

