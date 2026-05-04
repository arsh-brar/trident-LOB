# Agent Handoff Template

Status: Phase 0 template. Do not include secrets, paid data payloads, private account information, live broker endpoints, or live-trading instructions.

## Handoff Header

```text
handoff_id:
task_id:
phase:
owner_agent:
review_agent:
date_utc:
```

## Summary

State what changed in direct prose.

## Files Changed

```text
path:
change_type: added | modified | deleted
reason:
```

## Inputs Read

List the required project and research documents read before editing.

## Interfaces Changed

```text
interface_name:
change:
downstream_agents_affected:
migration_notes:
```

## Validation

```text
commands_run:
passed:
failed:
not_run:
reason_not_run:
```

## Safety Checks

```text
future_data_check: pass | fail | not_applicable
secret_check: pass | fail | not_applicable
paid_data_check: pass | fail | not_applicable
live_trading_block_check: pass | fail | not_applicable
profitability_claim_check: pass | fail | not_applicable
```

## Known Issues

List known failures, degraded modes, missing data, unresolved timestamp questions, or validation gaps.

## Follow-Up Tasks

```text
task:
owner_agent:
priority:
blocking:
```

## Open Questions

List uncertainty explicitly. Do not turn open questions into permissions.

## Sources

Cite local research docs as relative paths and external recommendations as URLs.
