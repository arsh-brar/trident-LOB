# Decision

Date checked: 2026-05-04.

## Decision

Build a Phase 1 design for a provider-neutral `N_t` event ledger and feature builder. Do not build production ingestion, live alerts, broker hooks, or live trading code. Recommendation: treat news and exogenous inputs as offline research features that feed the existing CPU-only Phase 1 pipeline. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md and https://numpy.org/install/.

The selected Phase 1 default is official SEC and macro calendars plus Massive stock news and Alpha Vantage news sentiment as low-friction research adapters. Recommendation: design the schema to upgrade later to Benzinga Newsfeed and Massive Benzinga earnings without changing downstream feature contracts. Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.alphavantage.co/documentation/, https://docs.benzinga.com/api-reference/news-api/overview, https://massive.com/docs/rest/partners/benzinga/earnings.

## Timestamp Decision

All timestamps must be normalized to UTC nanoseconds, with original provider timestamp strings preserved. Recommendation: use UTC nanoseconds as the canonical join key because Databento market data timestamps are nanoseconds since Unix epoch and UTC by default, while news providers expose UTC or offset-aware publication fields. Sources: https://databento.com/docs/standards-and-conventions, https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items.

Every event row must carry these point-in-time fields when available:

```text
source_published_at
provider_created_at
provider_updated_at
provider_removed_at
first_seen_at
available_at
scheduled_at
calendar_known_at
actual_available_at
```

Recommendation: compute features from `available_at`, not from retrieval date or article date alone, because publication, provider creation, provider update, and local first observation can differ. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

The hard leakage rule is:

```text
event_is_eligible(t_pred) =
  available_at <= t_pred
  and source_published_at <= t_pred
  and not removed_before_or_at(t_pred)
```

Recommendation: explicitly reject any news article, SEC filing, macro actual, earnings actual, transcript, or revised calendar row that was published after the prediction timestamp. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

## Event Types

Use these canonical event types:

```text
news_article
press_release
sec_filing
earnings_scheduled
earnings_reported
earnings_transcript
macro_scheduled
macro_released
fed_statement
fed_minutes
fed_projection
market_holiday_or_closure
```

Recommendation: store scheduled and released versions as separate events because pre-event schedule knowledge and post-event actual information become available at different times. Sources: https://massive.com/docs/rest/partners/benzinga/earnings, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

## Relevance Decision

Symbol relevance starts with provider ticker tags, primary ticker flags, SEC CIK and ticker mappings, and explicit calendar category mappings. Recommendation: use provider tags and official identifiers before text inference, because Massive and Benzinga expose ticker associations and the SEC submissions API includes company metadata with exchanges and ticker symbols. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Market-wide macro relevance should map to `SPY`, index futures proxies, broad ETF groups, rates-sensitive sectors, and all symbols as a separate market forcing term, but only as research metadata. Recommendation: keep market-wide forcing separate from symbol-specific forcing so macro releases do not masquerade as company news. Sources: https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

## Sentiment Decision

Sentiment is a normalized float in `[-1, 1]`, with provider sentiment stored separately from normalized sentiment. Recommendation: Phase 1 should use provider sentiment only as a raw input and should include neutral and event-count baselines, because provider-specific sentiment methods can differ and the project requires simple baselines first. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://www.alphavantage.co/documentation/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

SEC filings and macro scheduled events should default to neutral sentiment unless a validated parser or actual surprise field is available point-in-time. Recommendation: do not infer positive or negative direction from filing type or scheduled release existence alone in Phase 1. Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule.

## Deduplication And Novelty Decision

Deduplication must run before novelty and before feature aggregation. Recommendation: use a stable dedup key in this order: provider event ID, SEC accession number, canonical article URL, normalized title hash, normalized title plus source plus publication-time bucket, and optional text-similarity cluster. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data.

Novelty must be point-in-time. Recommendation: compute novelty from only prior eligible events in the same cluster, for example `novelty_j(t) = 1 / (1 + count_prior_cluster_events_available_before_t)`, so future duplicate articles cannot downweight an earlier event. Sources: https://docs.benzinga.com/api-reference/news-api/overview and https://docs.benzinga.com/api-reference/news-api/get-news-items.

## Decay Decision

Use exponential decay as the first kernel:

```text
decay_j(t) = exp(-log(2) * age_seconds(j,t) / half_life_seconds(source_type))
```

Recommendation: fit or grid-search half-lives by source type, starting with short intraday half-lives for breaking news and longer windows for filings and scheduled macro events. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.bls.gov/schedule/news_release/.

Scheduled events need a separate anticipation kernel:

```text
pre_event_risk(t) = 1[calendar_known_at <= t < scheduled_at]
  * exp(-time_to_event_seconds / anticipation_half_life_seconds)
```

Recommendation: use anticipation only for schedule knowledge and use actual release information only after `actual_available_at <= t`. Sources: https://massive.com/docs/rest/partners/benzinga/earnings, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html.

## N_t Decision

Phase 1 should output:

```text
N_signed_i(t)
N_energy_i(t)
N_count_i(t)
N_novel_count_i(t)
N_market_signed(t)
N_market_energy(t)
N_scheduled_risk_i(t)
N_scheduled_risk_market(t)
```

Recommendation: compare `N_t` features against count-only and calendar-only baselines before claiming any benefit from sentiment, relevance, novelty, or decay. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.bls.gov/schedule/news_release/.

## Non-Decision

No live trading is approved. No broker endpoint is approved. No paid data purchase is approved. No production ingestion is approved. No profitability claim is made.

## Open Questions

Which provider exposes the best historical first-seen timestamp for article availability?

Should `available_at` include a fixed vendor latency buffer when historical archives lack local first-seen logs?

How should corrected or removed articles affect historical features when a correction arrives after the prediction timestamp?

Which source-type half-lives are stable across symbols and market regimes?

How should macro surprise values be sourced point-in-time without using later revisions?
