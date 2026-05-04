"""Small immutable boundary records for the initial scaffold."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

DataMode = Literal["bars", "l1", "l2", "l3", "synthetic"]
ValidationStatus = Literal["pass", "fail", "warning", "not_run"]


@dataclass(frozen=True)
class ArtifactRef:
    artifact_id: str
    uri: str
    role: str
    content_hash: str | None = None


@dataclass(frozen=True)
class DataSliceSpec:
    symbols: tuple[str, ...]
    start_time_utc_ns: int
    end_time_utc_ns: int
    data_mode: DataMode = "synthetic"

    def __post_init__(self) -> None:
        if not self.symbols:
            raise ValueError("At least one symbol is required.")
        if self.start_time_utc_ns >= self.end_time_utc_ns:
            raise ValueError("Data slice start must be before end.")


@dataclass(frozen=True)
class DataBatch:
    slice_spec: DataSliceSpec
    manifest_id: str
    records_uri: str
    schema_version: str = "0.1"


@dataclass(frozen=True)
class FeatureFrame:
    artifact: ArtifactRef
    feature_available_at_max_ns: int
    row_count: int


@dataclass(frozen=True)
class LabelFrame:
    artifact: ArtifactRef
    max_label_horizon_ns: int
    row_count: int


@dataclass(frozen=True)
class TurbulenceFrame:
    artifact: ArtifactRef
    contains_k: bool = True
    contains_epsilon: bool = True


@dataclass(frozen=True)
class InterfaceFrame:
    artifact: ArtifactRef
    quality_flags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ModelArtifact:
    artifact: ArtifactRef
    validation_status: ValidationStatus = "not_run"


@dataclass(frozen=True)
class PredictionFrame:
    artifact: ArtifactRef
    row_count: int


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class ValidationReport:
    report_id: str
    status: ValidationStatus
    messages: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    phase: Literal["phase_1_research"]
    mode: Literal["offline_research", "dry_run"]
    dependency_lock_hash: str | None
    config_hash: str | None
    validation_status: ValidationStatus = "not_run"

    def __post_init__(self) -> None:
        blocked = {"production", "broker", "live"}
        if any(token in self.mode for token in blocked):
            raise ValueError("Run manifest mode is outside Phase 1 research scope.")
