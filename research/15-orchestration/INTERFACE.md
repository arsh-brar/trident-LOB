# Orchestration Interface

Status: Phase 0 planning interface. This is not production code and does not authorize trading code.

## Task Record

Every future build task should include:

```text
task_id
phase
owner_agent
review_agent
objective
inputs_to_read
allowed_paths
forbidden_paths
expected_outputs
validation_commands
required_handoff
open_questions
stop_conditions
```

Recommendation: require `allowed_paths` and `forbidden_paths` because multiple agents may work in the same codebase and must not revert or modify unrelated edits. Source: [repository rules](../../AGENTS.md).

## Agent Handoff Record

Every completed task should produce:

```text
handoff_id
task_id
owner_agent
files_changed
interfaces_changed
validation_run
validation_passed
known_failures
follow_up_tasks
open_questions
blocked_live_trading_check
secret_check
future_data_check
```

Recommendation: handoffs should be append-only and factual. They should not hide failed checks, missing data, degraded bars-only behavior, or unresolved timestamp questions. Sources: [testing interface](../13-testing-validation-and-benchmarks/INTERFACE.md), [reproducibility interface](../14-reproducibility-and-experiment-tracking/INTERFACE.md).

## Review Record

Every review should return:

```text
review_id
task_id
reviewer
status = approve | request_changes | block
findings
validation_gates_checked
files_reviewed
residual_risk
```

Hard blockers include:

- Future data in features or preprocessing.
- Live broker endpoint, live credential path, or live-trading enable flag.
- Secret, paid data payload, or private account information in committed files.
- Missing availability metadata.
- Missing baseline comparison for model claims.
- Negative accepted liquidity, nonpositive accepted `epsilon`, or uncapped execution.
- Profitability claim without out-of-sample, transaction-cost-adjusted evidence.

Sources: [repository rules](../../AGENTS.md), [risk validation](../11-risk-controls-and-compliance/VALIDATION.md), [testing validation](../13-testing-validation-and-benchmarks/VALIDATION.md).

## Shared Interface Change Protocol

An agent may change a shared contract only when the task explicitly lists that contract. The handoff must name downstream agents affected, migration notes, and tests added or changed. Shared changes without tests should be blocked unless the task is Phase 0 documentation only.

Recommendation: shared contract changes should be small and reviewed by the owning downstream component because the system depends on swappable interfaces. Sources: [architecture decision](../12-python-architecture-and-stack/DECISION.md), [architecture interface](../12-python-architecture-and-stack/INTERFACE.md).

## Escalation Interface

Escalate to the orchestration owner when:

- A task needs files outside its allowed paths.
- A required planning document is missing.
- Two agents need incompatible changes to the same interface.
- A validation gate is ambiguous.
- A task requires network access, paid data, credentials, paper broker access, or any live-like endpoint.
- A result appears to support a profitability claim.

Recommendation: escalation should pause the risky action, not the whole project. Sources: [data validation](../06-data-requirements-and-vendors/VALIDATION.md), [risk decision](../11-risk-controls-and-compliance/DECISION.md).
