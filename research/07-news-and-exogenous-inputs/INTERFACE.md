# Interface

Date checked: 2026-05-04.

This is a Phase 0 interface contract. It is not production code.

## Inputs

The module consumes raw provider event records, official calendar records, and a prediction grid. Recommendation: adapters should preserve raw provider payloads or raw payload hashes plus parsed fields, because timestamp normalization and provider corrections must be auditable. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items, https://massive.com/docs/rest/stocks/news?auth=signup, https://databento.com/docs/standards-and-conventions.

Required logical inputs:

```text
events_raw
calendar_versions
symbol_master
prediction_grid
market_sessions
provider_config
```

Recommendation: `symbol_master` must support CIK, ticker, exchange, and provider symbol mappings before SEC filing relevance is used. Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces and https://databento.com/docs/standards-and-conventions.

## Canonical Event Schema

Each canonical event row has these fields:

```text
event_id
provider
provider_event_id
source_name
source_url
event_type
title
summary
language
source_published_at
provider_created_at
provider_updated_at
provider_removed_at
first_seen_at
available_at
scheduled_at
calendar_known_at
actual_available_at
native_timezone
timestamp_quality
symbols
primary_symbols
ciks
isins
cusips
topics
channels
importance
raw_sentiment_label
raw_sentiment_score
normalized_sentiment
raw_relevance_score
normalized_relevance
dedup_key
cluster_id
revision_id
payload_hash
raw_payload_ref
```

Recommendation: timestamps should be stored as UTC nanoseconds plus original strings where possible, because market data providers document nanosecond UTC timestamp semantics and news providers expose RFC3339 or offset-aware timestamp strings. Sources: https://databento.com/docs/standards-and-conventions, https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items.

Recommendation: `timestamp_quality` should record whether the feature uses publisher publication time, provider created time, provider updated time, local first-seen time, official release time, or an imputed conservative time. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

## Calendar Version Schema

Each scheduled event version has these fields:

```text
calendar_event_id
provider
official_source_url
event_type
event_name
scheduled_at
scheduled_timezone
period_covered
symbol
market_scope
confirmation_status
calendar_known_at
calendar_updated_at
actual_available_at
actual_value_ref
revision_id
payload_hash
```

Recommendation: schedule rows must be versioned because earnings providers expose projected and confirmed statuses, while official macro calendars can be updated. Sources: https://massive.com/docs/rest/partners/benzinga/earnings, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html.

## Feature Builder Contract

The feature builder accepts:

```text
prediction_grid:
  symbol
  t_pred
  horizon
  session_id

event_ledger:
  canonical events sorted by available_at

calendar_versions:
  scheduled event versions sorted by calendar_known_at
```

It returns:

```text
symbol
t_pred
horizon
N_signed
N_energy
N_count
N_novel_count
N_market_signed
N_market_energy
N_scheduled_risk
N_scheduled_risk_market
latest_event_available_at
event_count_by_type
timestamp_quality_flags
```

Recommendation: the feature builder must perform an as-of join using `available_at <= t_pred` for event releases and `calendar_known_at <= t_pred` for pre-event schedule features. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.bls.gov/schedule/news_release/.

Recommendation: the feature builder must reject rows where `source_published_at > t_pred`, even if the row appears in a historical file fetched later. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data.

## Deduplication Interface

The deduplication step accepts canonical events sorted by `available_at` and returns `dedup_key`, `cluster_id`, and `revision_id`. Recommendation: deduplication must be deterministic and must prefer provider IDs, source URLs, SEC accession numbers, and normalized hashes before approximate text similarity. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data.

## Sentiment Interface

The sentiment step accepts raw sentiment labels, raw sentiment scores, provider insight objects, event types, and optional local baseline scores. It returns `normalized_sentiment` in `[-1, 1]` and a `sentiment_method` field. Recommendation: all sentiment methods must be stored as metadata so provider sentiment, local sentiment, and neutral baselines can be compared without silent changes. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and https://www.alphavantage.co/documentation/.

## Relevance Interface

The relevance step accepts event symbols, primary symbols, CIKs, ISINs, CUSIPs, channels, topics, and symbol master mappings. It returns per-symbol relevance values in `[0, 1]`. Recommendation: `primary_symbols` should receive higher default relevance than secondary symbols, while macro events should use a market-wide relevance channel rather than forced company-specific tags. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.bls.gov/schedule/news_release/.

## Leakage Prevention Interface

The leakage gate returns pass, fail, or quarantine with a reason code:

```text
SOURCE_PUBLISHED_AFTER_PREDICTION
AVAILABLE_AFTER_PREDICTION
CALENDAR_UNKNOWN_AT_PREDICTION
ACTUAL_VALUE_NOT_AVAILABLE
TIMESTAMP_MISSING
TIMESTAMP_CONFLICT
REVISION_AFTER_PREDICTION
REMOVED_BEFORE_PREDICTION
```

Recommendation: failed or quarantined events must not contribute to `N_t`, because the repository forbids future data and provider documentation shows multiple timestamp concepts that can otherwise be confused. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Open Questions

Should raw article bodies be stored locally, or should the ledger store only hashes, summaries, and provider IDs?

What timestamp-quality threshold should be required before minute-level labels are allowed?

Should macro calendar records be represented once per market or expanded to every symbol during feature building?

How should provider-specific sentiment model version changes be detected?
