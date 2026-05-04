# Calibration Validation

## Validation Principles

Calibration must be point-in-time. Training windows must end before validation windows begin, and no feature may use future data. This is a hard repository rule. Sources: ../../AGENTS.md; Bailey et al., https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Calibration must start with simple baselines and show incremental value before complex methods are used. This follows the repository rule and the Wave 1 market microstructure decision. Sources: ../../AGENTS.md; ../00-market-microstructure-literature/DECISION.md.

Calibration must report data granularity. Bars, L1, L2, and L3 support different parameter claims, so validation cannot treat all estimates as structurally identified. Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

## Accounting Checks

For L2 or L3 replay, validate source and sink accounting by comparing observed depth change in each tick cell to adds minus cancels minus executions plus boundary movement. This directly tests the integrated liquidity equation. Sources: ../../docs/TRIDENT_LOB_MODEL.md; Patankar, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224.

Executions must never consume more visible shares than available in the replayed book cell. Any calibration that implies negative depth fails validation. Sources: ../../docs/TRIDENT_LOB_MODEL.md; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

Estimated `lambda_s`, `mu_s`, `e_s`, `k`, `epsilon`, `D_0`, and `nu_t` must respect nonnegativity and unit checks. Sources: ../01-equation-audit-and-dimensional-analysis/DECISION.md; OpenFOAM k-epsilon documentation, https://doc.openfoam.com/2212/tools/processing/models/turbulence/ras/linear-evm/rtm/kEpsilon/.

## Statistical Checks

Direct event-rate estimates should be validated by out-of-sample log likelihood, calibration plots by event type, and residual event-count diagnostics by side, tick distance, time of day, and queue state. Sources: Cont, Stoikov, and Talreja, https://doi.org/10.1287/opre.1090.0780; Huang, Lehalle, and Rosenbaum, https://doi.org/10.1080/01621459.2014.982278.

Hawkes models should be validated only on event-level data with timestamp quality checks, branching ratio stability, residual diagnostics, and comparison to independent or state-dependent Poisson baselines. Sources: Bacry, Mastromatteo, and Muzy, https://arxiv.org/abs/1502.04592; Abergel and Jedidi, https://doi.org/10.1137/15M1011469.

GMM estimates should report chosen moments, weighting method, moment errors, robust uncertainty, and out-of-sample moment stability. Source: Hansen, https://www.econometricsociety.org/publications/econometrica/1982/07/01/large-sample-properties-generalized-method-moments-estimators.

Realized-volatility-derived `k` estimates should be checked against sampling-frequency sensitivity and microstructure noise. Sources: Andersen, Bollerslev, Diebold, and Labys, https://doi.org/10.1111/1468-0262.00418; Zhang, Mykland, and Ait-Sahalia, https://doi.org/10.1198/016214505000000169.

Filtered `k`, `epsilon`, and interface states should be compared to rolling proxy baselines before acceptance. Kalman-style filters should include innovation diagnostics, while particle filters should include effective sample size and resampling diagnostics. Sources: Sarkka and Svensson, https://doi.org/10.1017/9781108917407; Doucet and Johansen, https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF.pdf.

## Prediction Checks

A calibrated parameter should not be promoted merely because it fits in sample. It must improve at least one predeclared out-of-sample task after controlling for spread, depth, OFI, realized volatility, and volume. Sources: ../../AGENTS.md; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402; Bailey et al., https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Candidate tasks are next 1-minute return, next 5-minute return, direction, spread widening, local jump, depth recovery, and impact conditional on visible depth and order-flow imbalance. Sources: ../../docs/TRIDENT_LOB_MODEL.md; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

The turbulence claim should be validated as an incremental claim: for the same OFI, spread, visible depth, and realized volatility, higher `k^2 / epsilon` should predict greater impact, greater jump probability, or weaker depth recovery. Sources: ../../docs/TRIDENT_LOB_MODEL.md; Donier et al., https://arxiv.org/abs/1412.0141.

## Data-Level Validation Matrix

| Data level | Valid calibration claims | Invalid or weak claims |
|---|---|---|
| Bars | realized variance proxy for `k`, coarse `epsilon` decay, volume and return moments | source, cancellation, execution, queue kernel, structural diffusion |
| L1 quotes | spread, depth, OFI, top-book depletion and recovery proxies | full price-level source and sink separation, queue position |
| L2 depth | visible depth field, aggregate price-cell rates, depth recovery, effective diffusion proxy | order-level queue hazards, hidden liquidity |
| L3 messages | source, cancellation, execution, queue-priority kernel, event accounting | hidden liquidity, off-venue latent intentions |

Sources: Databento schema documentation, https://databento.com/docs/knowledge-base/new-users/market-data-schemas; Databento MBP-10 documentation, https://databento.com/docs/schemas-and-data-formats/mbp-10; LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php.

## Failure Conditions

Fail validation if any estimate uses future data, produces negative liquidity or negative rate parameters, relies on bars while claiming source or sink identification, omits OFI and simple volatility baselines, or claims profitability. Sources: ../../AGENTS.md; ../../docs/TRIDENT_LOB_MODEL.md; Cont, Kukanov, and Stoikov, https://arxiv.org/abs/1011.6402.

Fail validation if live trading code, live broker endpoints, live credential paths, or live enable flags appear in the calibration work. Sources: ../../AGENTS.md; ../11-risk-controls-and-compliance/DECISION.md.

## Open Questions

Which out-of-sample horizons should be mandatory for calibration acceptance?

Should validation use calendar time, event time, volume time, or all three?

What level of moment mismatch is acceptable before a parameter is marked unusable?

How should uncertainty from data censoring, hidden liquidity, and venue fragmentation be reported?

Should turbulence validation require stress-window performance or full-sample performance?
