# Orchestration Options

Status: Phase 0 planning. No production code, trading code, broker routing, paid-data purchase, or profitability claim is authorized.

## Option A: Single Builder Agent

One future build agent implements the Phase 1 stack end to end.

Benefits:

- Lowest coordination overhead.
- Fewer handoff documents.
- One person maintains local consistency.

Risks:

- Too much surface area for one agent.
- Higher chance of hidden coupling between data, features, models, risk, and reporting.
- Harder to review timestamp safety and live-trading safety across the full system.

Assessment: reject as the default. The repository explicitly wants swappable components, and the research contracts split naturally by component. Sources: [repository rules](../../AGENTS.md), [architecture decision](../12-python-architecture-and-stack/DECISION.md).

## Option B: Research-Agent Mirroring

Create future coding agents that mirror research agents 00 through 14.

Benefits:

- Preserves research provenance.
- Easy to cite prior decisions.
- Each research theme gets a direct build owner.

Risks:

- Research topics do not map cleanly to code ownership.
- Several agents would want to edit the same feature, validation, and config files.
- Backtesting, risk, reporting, and tracking would be tightly coupled without clear package boundaries.

Assessment: reject as the default. The research phase is thematic. The build phase should be component-owned. Sources: [architecture interface](../12-python-architecture-and-stack/INTERFACE.md), [testing interface](../13-testing-validation-and-benchmarks/INTERFACE.md).

## Option C: Component-Owned Roster

Create future coding agents around package boundaries: contracts, data, event store, features, turbulence, price interface, prediction, backtest, risk, validation, reproducibility, and reports.

Benefits:

- Matches the swappable architecture requested in the repository rules.
- Gives each agent clear files and folders.
- Makes review easier because interfaces and tests become explicit handoffs.
- Keeps live-trading blocks centralized in risk, backtest, and validation gates.

Risks:

- Requires an orchestration file, task template, and handoff template.
- Requires review discipline when interfaces change.

Assessment: accept. This is the preferred build orchestration model. Sources: [repository rules](../../AGENTS.md), [architecture decision](../12-python-architecture-and-stack/DECISION.md), [risk decision](../11-risk-controls-and-compliance/DECISION.md).

## Option D: Validation-First Roster

Start with validation and reproducibility agents, then let implementation agents fill the gates.

Benefits:

- Strongest protection against leakage and live-trading violations.
- Matches the fail-closed guidance in testing and risk research.
- Forces fixtures and manifests before complex models.

Risks:

- May slow early prototyping if validation owners block all interface movement.
- Needs minimal contracts before tests can be useful.

Assessment: combine with Option C. The accepted plan should sequence contracts and validation before feature and model work, but still assign component owners. Sources: [testing validation](../13-testing-validation-and-benchmarks/VALIDATION.md), [reproducibility validation](../14-reproducibility-and-experiment-tracking/VALIDATION.md).

## Accepted Direction

Use Option C with Option D sequencing. Create component-owned coding agents, require every task to include validation and reproducibility outputs, and keep Phase 0 and Phase 1 live trading blocked. Sources: [TRIDENT model](../../docs/TRIDENT_LOB_MODEL.md), [repository rules](../../AGENTS.md), [risk validation](../11-risk-controls-and-compliance/VALIDATION.md).
