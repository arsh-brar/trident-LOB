"""Fail-closed guards for the initial Phase 1 scaffold."""

from __future__ import annotations

from trident_lob.config import RunConfig


class GuardViolation(ValueError):
    """Raised when a config or manifest violates Phase 1 safety scope."""


def assert_phase1_safe_config(config: RunConfig) -> None:
    if config.mode.phase != "phase_1_research":
        raise GuardViolation("Only phase_1_research is allowed in this scaffold.")
    if config.mode.execution_mode not in {"offline_research", "dry_run"}:
        raise GuardViolation("Unsupported execution mode for Phase 1A.")
    if not config.data.secret_free:
        raise GuardViolation("Config is not secret-free.")
    if not config.data.paid_payload_free:
        raise GuardViolation("Config is not paid-payload-free.")
    if config.validation.allow_random_row_split:
        raise GuardViolation("Random row split is blocked for time-series validation.")
    if config.risk.allow_short or config.risk.allow_margin:
        raise GuardViolation("Short and margin simulation are blocked in Phase 1A.")
