# Research

Date checked: 2026-05-04.

This note designs the Phase 0 news and exogenous input module for TRIDENT-LOB. It is research planning only. It does not create production ingestion, live alerts, broker integration, live trading code, or any profitability claim.

The model needs a point-in-time exogenous forcing stream `N_t`, not a static news column. The model specification defines news as timestamped events with source reliability, symbol relevance, sentiment, novelty, and decay. Phase 1 should keep this CPU-only and provider-neutral, because Phase 1 has already been constrained to local feature pipelines and simple baselines before complex models. Source: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md and https://numpy.org/install/.

## Source Survey

Massive, formerly Polygon.io, exposes stock news through `/v2/reference/news`, with ticker filters, `published_utc` filters, article IDs, publisher metadata, tickers, and optional insights. Recommendation: use this as the first commercial-news adapter candidate because the endpoint has explicit publication timestamps in RFC3339 UTC, ticker associations, unique IDs, source URLs, and sentiment-related insight fields. Source: https://massive.com/docs/rest/stocks/news?auth=signup.

Benzinga exposes a Newsfeed API with filters by tickers, ISINs, CUSIPs, channels, topics, date ranges, `updatedSince`, `publishedSince`, importance, created timestamps, updated timestamps, and removed or corrected news. Recommendation: use Benzinga as the richer event-news candidate when low-latency corrections, primary ticker filters, and importance metadata matter. Source: https://docs.benzinga.com/api-reference/news-api/overview and https://docs.benzinga.com/api-reference/news-api/get-news-items.

Alpha Vantage exposes `NEWS_SENTIMENT` with ticker, topic, `time_from`, `time_to`, sort, and limit parameters, and it also exposes `EARNINGS_CALENDAR` for expected earnings in 3, 6, or 12 month horizons. Recommendation: use Alpha Vantage only as a lightweight baseline source for Phase 1 experiments, because it is simple to query but less explicit about provider ingestion and correction timestamps than event-focused feeds. Source: https://www.alphavantage.co/documentation/.

SEC EDGAR exposes company submissions and XBRL APIs through `data.sec.gov`, with no API key requirement. The SEC says the JSON structures are updated throughout the day as submissions are disseminated, with typical submissions API processing delay below one second, and bulk archives are republished nightly. Recommendation: treat SEC filings as an official exogenous source with filing acceptance and dissemination semantics, and never use nightly bulk archive availability as if it were intraday availability. Source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

SEC automated access has fair access constraints. The SEC lists a current maximum request rate of 10 requests per second and asks scripted users to declare a user agent. Recommendation: any future SEC adapter must be rate-limited, identify itself, and store raw filing metadata for audit. Source: https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data.

Earnings calendars are revisions-prone. Massive's Benzinga earnings endpoint includes scheduled or reported date, UTC time, confirmation status, last updated timestamp, estimates, actuals, and surprise fields. Recommendation: model earnings calendar rows as versioned scheduled events, not immutable truth, because the provider distinguishes projected from confirmed dates and exposes `last_updated`. Source: https://massive.com/docs/rest/partners/benzinga/earnings.

Nasdaq's public earnings calendar states that earnings dates can be algorithm-derived from historical reporting dates and provided by Zacks. Recommendation: do not treat projected earnings dates as confirmed corporate disclosures unless a press release, SEC filing, or provider confirmation flag supports that status. Source: https://www.nasdaq.com/market-activity/quotes/earnings.

Macro calendars should come from official calendars first. BLS publishes release calendars with Eastern Time release times and an online calendar feed. Recommendation: use official BLS scheduled release times for CPI, Employment Situation, PPI, JOLTS, import and export prices, productivity, and related labor releases before using a vendor mirror. Source: https://www.bls.gov/schedule/news_release/.

BEA publishes an official release schedule with date and time fields for GDP, personal income and outlays, international trade, international transactions, and related releases. Recommendation: use BEA's official schedule for BEA-managed macro events and store release time in Eastern Time plus normalized UTC. Source: https://www.bea.gov/news/schedule.

The Census Bureau publishes an official economic indicator release schedule with release date, time, period covered, and event IDs. Recommendation: use Census as the official source for retail sales, durable goods, construction spending, housing starts, new residential sales, wholesale trade, and related Census economic indicators. Source: https://www.census.gov/economic-indicators/calendar-listview.html.

The Federal Reserve publishes FOMC meeting calendars, statements, implementation notes, press conferences, minutes, and projection material links. Recommendation: store FOMC meetings as scheduled market-wide events and store statements, minutes, projection materials, and press conferences as distinct release events. Source: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

Databento documents event timestamps `ts_event`, receive timestamps `ts_recv`, live outgoing timestamps `ts_out`, and timestamp deltas, all in nanoseconds since Unix epoch, with UTC defaults. Recommendation: align market data and news features to a common UTC nanosecond timeline while retaining each source's native timestamp fields. Source: https://databento.com/docs/standards-and-conventions.

Databento also warns that normalization can truncate or discard timestamps and can introduce data issues. Recommendation: store raw provider payloads or raw metadata hashes for news and calendar events so timestamp loss can be audited later. Source: https://databento.com/docs/standards-and-conventions.

## Point-In-Time Semantics

The canonical rule is simple: an event may influence a feature at prediction timestamp `t_pred` only if the module can prove the event was available at or before `t_pred`. Recommendation: compute `N_t` with `available_at <= t_pred` and reject any event with `source_published_at > t_pred`, because the repository forbids future data and providers expose publication, created, updated, or dissemination timestamps for this purpose. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

For articles, `source_published_at` is the publisher publication timestamp when provided, `provider_created_at` is the provider's created timestamp, `provider_updated_at` is the correction or update timestamp, and `first_seen_at` is the first local observation time. Recommendation: use `available_at = max(source_published_at, provider_created_at, first_seen_at)` when all fields exist, and otherwise use the most conservative available timestamp. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and https://docs.benzinga.com/api-reference/news-api/get-news-items.

For SEC filings, `source_published_at` should be the EDGAR acceptance or dissemination timestamp when available from the filing metadata, and `first_seen_at` should be the local poll time. Recommendation: if a historical SEC source lacks intraday availability metadata, use it only for daily or coarser studies, or apply a conservative availability delay that makes the feature unusable before the next known dissemination window. Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces and https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data.

For scheduled events, `scheduled_at` is the planned release time, `calendar_known_at` is when this schedule record was first available, and `actual_available_at` is when the actual release or result became available. Recommendation: pre-event features may use only schedule data with `calendar_known_at <= t_pred`, while actual values, surprises, transcripts, filings, and post-release sentiment require `actual_available_at <= t_pred`. Sources: https://massive.com/docs/rest/partners/benzinga/earnings, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html.

## N_t Design

Use two related features. `N_signed_i(t)` carries directional information. `N_energy_i(t)` carries shock intensity for the `C_N * N_t^2` turbulence production term. Recommendation: preserve both signed and squared news forcing, because the TRIDENT model uses `N_t^2` in turbulence production while directional news can still enter side-specific forcing `F_s`. Source: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

The Phase 1 formula should be:

```text
N_signed_i(t) =
  sum_j beta_source(j) * relevance(i,j) * sentiment(i,j) * novelty(j,t)
  * decay_j(t) * 1[available_at(j) <= t]

N_energy_i(t) =
  sum_j abs(beta_source(j) * relevance(i,j) * sentiment_or_intensity(j)
  * novelty(j,t)) * decay_j(t) * 1[available_at(j) <= t]
```

Recommendation: do not include an event in either sum unless `available_at(j) <= t` and `source_published_at(j) <= t`, because publication after the prediction timestamp is a direct lookahead bias. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Relevance should start with provider ticker tags, primary ticker flags, SEC CIK-to-ticker mapping, and official calendar category mapping. Recommendation: do not infer tradable symbol relevance from free text alone in Phase 1 unless the inferred mapping is stored with confidence and audited against provider tags. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Sentiment should start as a bounded numeric feature in `[-1, 1]`, with neutral equal to `0`. Recommendation: accept provider sentiment or insight fields as raw inputs, but store the provider name, provider model label, and normalized value so later models can compare provider sentiment against a local CPU-only baseline. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and https://www.alphavantage.co/documentation/.

Novelty should be computed only from events already available before `t`. Recommendation: cluster duplicates by provider ID, source URL, accession number, normalized title, normalized body hash, and near-time text similarity, then set novelty to `1 / (1 + prior_cluster_count)` or a monotone decreasing cluster weight. Sources: https://docs.benzinga.com/api-reference/news-api/overview, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data.

Decay should use simple kernels first. Recommendation: use exponential decay with configurable half-lives by source type, and include a rectangular scheduled-event window for pre-event risk, because the project requires simple baselines before complex models. Sources: https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

## Open Questions

What is the most defensible provider for point-in-time historical news archives at Phase 1 budget?

How should delayed provider updates be represented when `created`, `updated`, and publisher publication times disagree?

Can provider sentiment add signal after controlling for realized volatility, spread, depth, OFI, and event intensity?

How should macro surprise values be joined without using revised economic data that was not available at the prediction timestamp?

What half-life grid best separates intraday shock reaction from slow sector repricing?

Can article novelty be validated without storing copyrighted full article bodies?
