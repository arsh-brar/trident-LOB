# Task Template

Status: Phase 0 template. This template is for future build or planning tasks. It does not authorize live trading.

## Task Header

```text
task_id:
phase:
owner_agent:
review_agent:
priority:
status: queued | in_progress | blocked | review | done
```

## Objective

State the concrete outcome.

## Required Reading

Always include:

- `docs/TRIDENT_LOB_MODEL.md`
- `AGENTS.md`
- `plans/ORCHESTRATION.md`
- The relevant research `DECISION.md`, `INTERFACE.md`, and `VALIDATION.md`

## Allowed Paths

List exact files and folders the agent may modify.

## Forbidden Paths

List files and folders the agent must not touch. Include unrelated agents' work.

## Inputs

List data fixtures, manifests, configs, or prior outputs the agent may read.

## Outputs

List files, docs, tests, manifests, or reports the task must produce.

## Validation Commands

```text
command:
purpose:
required: yes | no
```

## Required Handoff

The agent must fill `plans/AGENT_HANDOFF_TEMPLATE.md` content in the task closeout or linked handoff file.

## Review Gates

Block completion if any of these apply:

- Future data enters features, preprocessing, labels, validation, or reports.
- Live broker endpoint, live credential path, live order router, or live-trading flag appears.
- API key, broker credential, paid data payload, or private account information appears.
- Negative accepted liquidity, nonpositive accepted `epsilon`, or uncapped execution appears.
- Model work lacks no-skill, ordinary microstructure, and technical baselines.
- Profitability is claimed without out-of-sample, transaction-cost-adjusted evidence.

## Stop Conditions

Stop and escalate if the task needs network access, paid data, credentials, paper broker access, files outside allowed paths, or a change to shared interfaces not named in this task.

## Sources

Cite local research docs as relative paths and external recommendations as URLs.
