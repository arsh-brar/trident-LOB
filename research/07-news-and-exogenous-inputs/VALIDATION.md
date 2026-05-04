# Validation

Date checked: 2026-05-04.

This validation plan is Phase 0 research design only. It does not validate live trading.

## Required Gates

Gate 1 is source provenance. Recommendation: every event must have provider, source URL or official source, event type, provider event ID or deterministic dedup key, and timestamp-quality metadata before it can enter `N_t`. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Gate 2 is timestamp normalization. Recommendation: every timestamp must be parsed to UTC nanoseconds and retain its original string or integer representation, because market data uses UTC nanosecond timestamps and news providers expose RFC3339 or offset-aware timestamps. Sources: https://databento.com/docs/standards-and-conventions, https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items.

Gate 3 is point-in-time eligibility. Recommendation: no event may contribute to a feature row unless `available_at <= t_pred` and `source_published_at <= t_pred`. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Gate 4 is scheduled-event separation. Recommendation: schedule knowledge, actual release values, revisions, transcripts, and post-release sentiment must be separate feature inputs with separate availability timestamps. Sources: https://massive.com/docs/rest/partners/benzinga/earnings, https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

Gate 5 is deduplication. Recommendation: duplicate and corrected events must be clustered before novelty and aggregation, because providers expose IDs, URLs, updated timestamps, and removed or corrected news semantics. Sources: https://docs.benzinga.com/api-reference/news-api/overview, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://massive.com/docs/rest/stocks/news?auth=signup.

Gate 6 is baseline comparison. Recommendation: compare full `N_t` against zero-news, event-count-only, calendar-only, and sentiment-free baselines before claiming usefulness. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://massive.com/docs/rest/stocks/news?auth=signup, https://www.bls.gov/schedule/news_release/.

## Test Cases

Future article test: create one article with `source_published_at` one second after `t_pred`. Expected result: the leakage gate rejects the event. Recommendation: this must be a hard failure because using news published after prediction time is lookahead bias. Sources: https://massive.com/docs/rest/stocks/news?auth=signup and file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Late provider update test: create one article published before `t_pred` but updated after `t_pred`. Expected result: the original eligible version may be used if stored, but the update fields may not be used before their `provider_updated_at`. Recommendation: event revisions must be versioned rather than overwritten. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items and https://docs.benzinga.com/api-reference/news-api/overview.

SEC bulk archive test: load an SEC filing from a nightly bulk file and ask for an intraday feature before dissemination. Expected result: reject or quarantine unless an intraday acceptance or dissemination timestamp proves availability. Recommendation: nightly bulk availability must not be treated as intraday availability. Source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Calendar actual test: create a CPI scheduled event at 8:30 AM ET and a prediction row at 8:29:59 AM ET. Expected result: pre-event risk may be used if `calendar_known_at <= t_pred`, but actual CPI values and surprise fields are rejected. Recommendation: scheduled knowledge and actual release data must use separate availability fields. Source: https://www.bls.gov/schedule/news_release/.

Earnings projection test: create an earnings date with projected status, then a confirmed update. Expected result: the projected date can be used only as projected schedule knowledge, and the confirmed status applies only after its update timestamp. Recommendation: confirmation status must be versioned because earnings providers distinguish projected from confirmed dates. Source: https://massive.com/docs/rest/partners/benzinga/earnings.

Duplicate burst test: create five headlines with the same URL or title cluster over ten minutes. Expected result: first eligible event has novelty near 1, later eligible duplicates have lower novelty, and future duplicates do not change past novelty. Recommendation: novelty must be computed using prior eligible cluster members only. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items and https://massive.com/docs/rest/stocks/news?auth=signup.

Timestamp conflict test: create an article where provider created time precedes source publication time or first-seen time by an impossible amount. Expected result: set a timestamp-quality warning and use the conservative maximum timestamp. Recommendation: timestamp conflicts must degrade quality rather than silently improve feature availability. Sources: https://docs.benzinga.com/api-reference/news-api/get-news-items and https://databento.com/docs/standards-and-conventions.

Macro official source test: compare a vendor macro calendar row against official BLS, BEA, Census, or FOMC calendars. Expected result: official schedule wins for scheduled time, while vendor data may add convenience metadata. Recommendation: official macro calendars should be the reference schedule for official releases. Sources: https://www.bls.gov/schedule/news_release/, https://www.bea.gov/news/schedule, https://www.census.gov/economic-indicators/calendar-listview.html, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

## Metrics

Recommendation: track coverage by event type, source, symbol, timestamp-quality class, and session because missing or low-quality events can create biased comparisons across symbols. Sources: https://massive.com/docs/rest/stocks/news?auth=signup, https://docs.benzinga.com/api-reference/news-api/get-news-items, https://www.sec.gov/search-filings/edgar-application-programming-interfaces.

Recommendation: track rejected events by reason code, especially publication after prediction, availability after prediction, missing timestamp, revision after prediction, and calendar unknown at prediction. Sources: https://databento.com/docs/standards-and-conventions, https://docs.benzinga.com/api-reference/news-api/get-news-items.

Recommendation: report feature distributions for `N_signed`, `N_energy`, `N_count`, `N_novel_count`, and scheduled risk by source type before any model fitting. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md and https://massive.com/docs/rest/stocks/news?auth=signup.

Recommendation: validate that `N_t` adds signal only through out-of-sample tests against literature-supported market microstructure baselines such as OFI, spread, depth, and realized volatility. Sources: https://arxiv.org/abs/1011.6402 and file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Open Questions

What timestamp-quality class is sufficient for 1-minute horizons?

How should removed news be handled when the removal arrives after the prediction timestamp?

Can article snippets or hashes support deduplication enough without storing full copyrighted article bodies?

Which official macro source should supply point-in-time actual values and revision histories?

How large should the embargo be around scheduled events when release time precision is only to the minute?
