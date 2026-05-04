# Orchestration Validation

Status: Phase 0 validation plan. This validates coordination documents only. It does not validate production code, broker routing, paper API use, live trading, or profitability.

## Required Checks

Gate 1: scope check. The orchestration deliverables must stay in `research/15-orchestration` and the named files in `plans`. Source: [repository rules](../../AGENTS.md).

Gate 2: source check. Recommendations must cite local research documents or external URLs. Source: [repository rules](../../AGENTS.md).

Gate 3: live-trading block. The documents must state that live trading is blocked in Phase 0 and Phase 1. Sources: [TRIDENT model](../../docs/TRIDENT_LOB_MODEL.md), [risk decision](../11-risk-controls-and-compliance/DECISION.md).

Gate 4: roster completeness. `plans/ORCHESTRATION.md` must define coding agent roster, charters, inputs, outputs, allowed paths, forbidden paths, handoff protocol, task queue format, review protocol, escalation rules, prompt templates, phased plan, and definition of done for every phase.

Gate 5: handoff completeness. `plans/AGENT_HANDOFF_TEMPLATE.md` must capture changed files, validation, handoff notes, open questions, live-trading safety, secret safety, and future-data safety.

Gate 6: task completeness. `plans/TASK_TEMPLATE.md` must capture objective, inputs, allowed paths, forbidden paths, outputs, validation commands, review owner, and stop conditions.

Gate 7: no em dash. Generated documents should avoid em dashes to satisfy repository document rules. Source: [repository rules](../../AGENTS.md).

## Failure Conditions

Fail orchestration validation if a document permits live trading in Phase 0 or Phase 1, omits timestamp safety, omits baseline discipline, omits validation ownership, contains unsupported profitability language, lacks sources for recommendations, or assigns broad unbounded file ownership.

Sources: [feature validation](../08-feature-engineering-and-labels/VALIDATION.md), [prediction validation](../09-prediction-models-and-baselines/VALIDATION.md), [risk validation](../11-risk-controls-and-compliance/VALIDATION.md), [testing validation](../13-testing-validation-and-benchmarks/VALIDATION.md).

## Manual Review Checklist

- The roster maps to swappable architecture components.
- Shared files have explicit owners.
- Agents cannot modify live trading paths because no such paths are allowed in Phase 0 or Phase 1.
- Every future build prompt tells the agent what to read first.
- Every phase has a definition of done.
- Open questions are explicit and do not weaken hard gates.

## Open Questions

Should future validation create repository-level `plans/INTERFACES.md` and `plans/VALIDATION_GATES.md` so the `AGENTS.md` read list resolves to consolidated files?

Should task queue records be stored as Markdown, YAML, or issue tracker items once implementation begins?
