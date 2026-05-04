# Options

Date checked: 2026-05-04.

This document compares Phase 0 options for the `N_t` module. All options are research-only. None authorizes production ingestion, live alerts, live trading, or profitability claims.

## Option A: Official Sources Only

This option uses SEC EDGAR for filings and official BLS, BEA, Census, and Federal Reserve calendars for macro events. Recommendation: keep this option as the minimum compliance and leakage baseline because official sources define the release schedule and dissemination semantics for filings and macro releases. Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

Benefits are clear provenance, no news vendor lock-in, and strong auditability. Recommendation: use official sources for scheduled macro events even if a vendor mirror is added later, because official release calendars give the primary release date and time. Sources: https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html.

Limits are weak company news coverage, no built-in sentiment, and sparse intraday market-moving headlines outside SEC filings. Recommendation: do not rely on official-only sources for symbol-specific news studies that claim to measure intraday headline reaction. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and https://docs.benzinga.com/api-reference/news-api/overview.

## Option B: Low-Friction Provider-Neutral News Baseline

This option adds Massive stock news and Alpha Vantage `NEWS_SENTIMENT` to the official-source baseline. Recommendation: use this option for early Phase 1 experiments because Massive provides article IDs, ticker filters, publication timestamps, publisher metadata, and optional insights, while Alpha Vantage provides simple news sentiment and earnings calendar endpoints. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and https://www.alphavantage.co/documentation/.

Benefits are easy implementation, source URLs, ticker association, publication timestamps, and sentiment inputs. Recommendation: normalize all provider sentiment into a local schema instead of trusting a single provider score, because providers expose different sentiment and insight semantics. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and https://www.alphavantage.co/documentation/.

Limits are uncertain low-latency archival fidelity and possible lack of correction metadata. Recommendation: do not use this option for claims about sub-second or minute-level news reaction unless the provider archive includes auditable `available_at`, created, updated, or first-seen metadata. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items and https://databento.com/docs/standards-and-conventions.

## Option C: Event-Grade Commercial Archive

This option uses Benzinga Newsfeed plus Massive Benzinga earnings, while still keeping official SEC and macro calendars. Recommendation: prefer this option for serious intraday news research when budget allows because Benzinga exposes ticker, primary ticker, ISIN, CUSIP, channel, topic, importance, created, updated, `publishedSince`, `updatedSince`, and removed or corrected news mechanics. Sources: https://docs.benzinga.com/api-reference/news-api/overview, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://massive.com/docs/rest/partners/benzinga/earnings.

Benefits are better event lifecycle support, richer filtering, corrections, and earnings metadata. Recommendation: store event versions when using this option because updates and removed news can change the apparent information set after the original publication. Sources: https://docs.benzinga.com/api-reference/news-api/overview and https://docs.benzinga.com/api-reference/news-api/get-news-items.

Limits are paid data cost, licensing constraints, and possible redistribution restrictions. Recommendation: commit only schemas and `.env.example` style placeholders, never API keys or paid data extracts, because provider access is credentialed and project policy blocks private account information in the repository. Sources: https://docs.benzinga.com/introduction/introduction and file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Option D: Calendar-Only Event Risk

This option excludes article news and filings from first-pass features, and uses only earnings dates, FOMC dates, BLS releases, BEA releases, and Census releases. Recommendation: keep this option as a negative-control baseline because scheduled event windows can be known before release and are easier to validate for leakage. Sources: https://massive.com/docs/rest/partners/benzinga/earnings, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html.

Benefits are strong point-in-time semantics and low storage needs. Recommendation: separate pre-event risk features from post-event actual surprise features, because actual release values are not available before the release timestamp. Sources: https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html.

Limits are no unscheduled news coverage. Recommendation: do not treat calendar-only `N_t` as a full proxy for exogenous information shocks, because the TRIDENT model explicitly includes symbol-specific news and market-wide shocks beyond scheduled events. Source: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

## Recommendation

Choose Option B for Phase 1 interface design and early experiments, while designing the event schema so Option C can replace it without changing downstream feature builders. Source: https://massive.com/docs/rest/stocks/news?auth=signup, https://www.alphavantage.co/documentation/, https://docs.benzinga.com/api-reference/news-api/overview.

Use Option A official calendars as mandatory reference sources for SEC and macro events, even when vendors provide mirrored calendars. Source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

Keep Option D as a validation baseline to test whether text sentiment and novelty add value beyond known scheduled event risk. Source: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md and https://www.bls.gov/schedule/news_release/.

## Open Questions

Which vendor can provide the most audit-friendly historical `first_seen_at` or created timestamp at acceptable cost?

Will Massive's insight fields be stable enough for longitudinal studies across provider model changes?

Can Alpha Vantage news sentiment be used reproducibly for historical backtests with sufficient rate limits?

What paid-data license terms apply to storing raw article bodies, snippets, or derived embeddings?
