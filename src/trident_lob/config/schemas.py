"""Dataclass config skeletons for Phase 1 offline research."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Phase = Literal["phase_1_research"]
ExecutionMode = Literal["offline_research", "dry_run"]
DataMode = Literal["bars", "l1", "l2", "l3", "synthetic"]
LicenseClass = Literal[
    "free",
    "delayed",
    "real-time",
    "paid",
    "research-only",
    "paper-trading-suitable",
]
SplitPolicy = Literal["chronological", "walk_forward"]


@dataclass(frozen=True)
class ModeConfig:
    """Execution mode guard for Phase 1 research runs."""

    phase: Phase = "phase_1_research"
    execution_mode: ExecutionMode = "offline_research"

    def __post_init__(self) -> None:
        blocked = {"production", "broker", "live"}
        if self.phase != "phase_1_research":
            raise ValueError("Phase 1A config only allows phase_1_research.")
        if any(token in self.execution_mode for token in blocked):
            raise ValueError("Execution mode is outside Phase 1A safety scope.")


@dataclass(frozen=True)
class DataConfig:
    data_mode: DataMode = "synthetic"
    license_class: LicenseClass = "free"
    paid_payload_free: bool = True
    secret_free: bool = True

    def __post_init__(self) -> None:
        if not self.paid_payload_free:
            raise ValueError("Committed configs must not include paid data payloads.")
        if not self.secret_free:
            raise ValueError("Committed configs must not include secrets.")


@dataclass(frozen=True)
class ValidationConfig:
    split_policy: SplitPolicy = "chronological"
    require_availability_check: bool = True
    allow_random_row_split: bool = False

    def __post_init__(self) -> None:
        if self.allow_random_row_split:
            raise ValueError("Random row splits are not valid for Phase 1 time series.")


@dataclass(frozen=True)
class TrackingConfig:
    tracking_uri: str = "experiments/mlruns"
    registry_aliases: tuple[str, ...] = (
        "exploratory",
        "candidate",
        "rejected",
        "archived",
    )

    def __post_init__(self) -> None:
        blocked_aliases = {"production", "broker", "champion", "live"}
        if blocked_aliases.intersection(self.registry_aliases):
            raise ValueError(
                "Registry aliases must stay within Phase 1 research scope."
            )


@dataclass(frozen=True)
class RiskConfig:
    max_research_drawdown_fraction: float = 0.05
    allow_short: bool = False
    allow_margin: bool = False

    def __post_init__(self) -> None:
        if self.max_research_drawdown_fraction <= 0:
            raise ValueError("Max research drawdown fraction must be positive.")
        if self.allow_short or self.allow_margin:
            raise ValueError("Short and margin simulation are outside Phase 1A scope.")


@dataclass(frozen=True)
class RunConfig:
    schema_version: str = "0.1"
    mode: ModeConfig = field(default_factory=ModeConfig)
    data: DataConfig = field(default_factory=DataConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)

    @classmethod
    def default(cls) -> RunConfig:
        return cls()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
