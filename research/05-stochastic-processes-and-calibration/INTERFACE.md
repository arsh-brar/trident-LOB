# Calibration Interface

## Purpose

This interface describes Phase 0 contracts for future calibration components. It is not production code and does not authorize trading code. The future implementation should keep calibration swappable across direct counts, maximum likelihood, GMM, filters, and simulation-based methods. Sources: ../../AGENTS.md; ../12-python-architecture-and-stack/DECISION.md.

## Inputs

`BarFrame` contains point-in-time bars with symbol, timestamp, open, high, low, close, volume, and optional VWAP. It supports realized volatility and decay proxies only. Source: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

`L1QuoteFrame` contains best bid, best ask, bid size, ask size, timestamp, venue or feed identity, and sequence fields when available. It supports spread, top-book depth, OFI, quote-motion variance, and top-book replenishment or depletion proxies. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

`TradeFrame` contains timestamp, price, size, venue or feed identity, and trade direction when supplied or classified. It supports execution-flow proxies and OFI-style baselines, but it does not by itself identify full resting-book source and sink terms. Sources: Hasbrouck, https://doi.org/10.1111/j.1540-6261.1991.tb03749.x; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

`L2DepthEventFrame` contains timestamp, side, action, price, size, level, aggregate level sizes, and order counts when available. It supports visible depth fields and aggregate price-cell source and sink estimates when actions are present. Source: Databento MBP-10 documentation, https://databento.com/docs/schemas-and-data-formats/mbp-10.

`L3MessageFrame` contains timestamp, order ID, event type, side, price, size, and order lifecycle fields. It supports order-level source, cancellation, modification, execution, and queue-priority calibration. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

`CalendarFrame` contains session opens, closes, halts, early closes, and event windows. Calibration must use only data available at or before the calibration timestamp and must segment or reject abnormal market-state windows. Sources: NYSE calendars, https://www.nyse.com/markets/hours-calendars; repo no-future-data rule, ../../AGENTS.md.

## Outputs

`CalibrationEstimate` contains parameter name, symbol, side, tick cell or distance-from-mid bucket, time window, estimate, standard error or credible interval when available, sample count, source data level, method, and fit timestamp.

`TurbulenceStateEstimate` contains `k`, `epsilon`, `fragility`, `nu_t_proxy`, method, lookback window, units, floors, and uncertainty fields.

`EventIntensityEstimate` contains `lambda_s`, `mu_s`, `e_s`, optional Hawkes kernels, seasonality adjustment, state bins, and event counts.

`DiffusionEstimate` contains `D_effective`, optional `D_0`, optional `nu_t / sigma_q`, price-cell domain, residual accounting error, and identifiability notes.

`InterfaceEstimate` contains midprice response slope, OFI response, visible or latent liquidity slope proxy, spread-widening probability, jump probability, and calibration horizon.

`CalibrationReport` contains data coverage, parameter table, validation metrics, leakage checks, accounting checks, uncertainty, open questions, and sources.

## Required Methods

Every future calibrator should expose `fit(calibration_window)`, `estimate(as_of_time)`, `validate(validation_window)`, and `summarize()`. This supports point-in-time validation and avoids future-data leakage. Sources: repo policy, ../../AGENTS.md; Bailey et al., https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Every calibrator should report input data level as `bars`, `L1`, `L2`, or `L3`, because identifiability depends on data granularity. Source: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas.

Every event-level calibrator should preserve side, price in ticks, event type, sequence order, and timestamp precision. This is required for source, sink, execution, and queue accounting. Sources: ../01-equation-audit-and-dimensional-analysis/DECISION.md; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

Every calibration result should carry units. Required units are ticks for `p`, seconds for `t`, shares per tick for `q_s`, inverse seconds for `mu_s`, shares per tick per second for `lambda_s` and `e_s`, and tick-derived units for `k`, `epsilon`, and diffusion terms. Sources: ../01-equation-audit-and-dimensional-analysis/DECISION.md; OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

## Method Selection Rules

Use direct counts or maximum likelihood for event intensities when L2 or L3 action-labeled events are available. Sources: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780; Huang, Lehalle, and Rosenbaum, https://doi.org/10.1080/01621459.2014.982278.

Use GMM or rolling proxy estimators for Phase 1 bars and L1 quotes. Sources: Hansen, https://www.econometricsociety.org/publications/econometrica/1982/07/01/large-sample-properties-generalized-method-moments-estimators; Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418.

Use Kalman-style filters only for low-dimensional latent state estimates after proxy baselines are present. Sources: Kalman, https://doi.org/10.1115/1.3662552; Julier and Uhlmann, https://doi.org/10.1109/JPROC.2003.823141.

Use particle filters, neural state-space models, and score-based calibration only behind research interfaces, not as core Phase 1 dependencies. Sources: Doucet and Johansen, https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF.pdf; Krishnan, Shalit, and Sontag, https://arxiv.org/abs/1609.09869; Song et al., https://openreview.net/forum?id=PxTIG12RRHS; ../12-python-architecture-and-stack/DECISION.md.

## Open Questions

Should calibration reports store both tick-space estimates and basis-point normalized views?

Should event intensity bins be fixed by tick distance, queue percentile, or adaptive depth buckets?

Should uncertainty be reported as standard errors, bootstrap intervals, posterior intervals, or all available forms?

Should `epsilon` floors be global, symbol-specific, or regime-specific?
