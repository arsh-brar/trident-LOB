"""Strict label rows and chronological split manifests."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from trident_lob.data.schemas import StrictBoundaryModel


class DirectionLabel(StrEnum):
    DOWN = "down"
    FLAT = "flat"
    UP = "up"


class LabelNullReason(StrEnum):
    NONE = "none"
    MISSING_CURRENT_MID = "missing_current_mid"
    MISSING_FUTURE_OUTCOME = "missing_future_outcome"
    INVALID_HORIZON = "invalid_horizon"
    SESSION_INVALID = "session_invalid"


class LabelRow(StrictBoundaryModel):
    symbol: str
    t_pred_ns: int
    horizon_seconds: int
    label_available_at_min_ns: int | None
    label_version: str = "phase1c_skeleton_v1"
    y_return_log: float | None = None
    y_return_ticks: float | None = None
    y_return_bps: float | None = None
    y_dir_cost_aware: DirectionLabel | None = None
    y_spread_widen: bool | None = None
    y_local_jump: bool | None = None
    y_depth_deplete: bool | None = None
    y_fragility_persist: bool | None = None
    cost_ticks: float = 0.0
    buffer_ticks: float = 0.0
    null_reason: LabelNullReason = LabelNullReason.NONE

    @model_validator(mode="after")
    def validate_label_boundary(self) -> Self:
        if self.t_pred_ns < 0:
            raise ValueError("t_pred_ns must be nonnegative.")
        if self.horizon_seconds <= 0:
            raise ValueError("horizon_seconds must be positive.")
        if self.cost_ticks < 0 or self.buffer_ticks < 0:
            raise ValueError("label costs and buffers must be nonnegative.")
        label_values = (
            self.y_return_log,
            self.y_return_ticks,
            self.y_return_bps,
            self.y_dir_cost_aware,
            self.y_spread_widen,
            self.y_local_jump,
            self.y_depth_deplete,
            self.y_fragility_persist,
        )
        has_label = any(value is not None for value in label_values)
        if has_label and self.null_reason != LabelNullReason.NONE:
            raise ValueError("non-null labels must use null_reason=none.")
        if not has_label and self.null_reason == LabelNullReason.NONE:
            raise ValueError("null labels require a null_reason.")
        if has_label:
            if self.label_available_at_min_ns is None:
                raise ValueError("non-null labels require label availability.")
            if self.label_available_at_min_ns <= self.t_pred_ns:
                raise ValueError("labels must become available after t_pred_ns.")
        return self


class SplitWindow(StrictBoundaryModel):
    start_ns: int
    end_ns: int

    @model_validator(mode="after")
    def validate_window(self) -> Self:
        if self.start_ns < 0 or self.end_ns < 0:
            raise ValueError("split timestamps must be nonnegative.")
        if self.start_ns > self.end_ns:
            raise ValueError("split start must be before or equal to end.")
        return self


class ChronologicalSplitManifest(StrictBoundaryModel):
    dataset_id: str
    split_id: str
    symbol_universe: tuple[str, ...]
    train: SplitWindow
    validation: SplitWindow
    test: SplitWindow
    embargo_ns: int
    max_label_horizon_ns: int
    max_feature_lookback_ns: int
    held_out_symbols: tuple[str, ...] = Field(default_factory=tuple)
    created_at_ns: int
    split_policy: str = "chronological"

    @model_validator(mode="after")
    def validate_chronological_embargo(self) -> Self:
        if not self.symbol_universe:
            raise ValueError("symbol_universe must not be empty.")
        if self.split_policy != "chronological":
            raise ValueError("only chronological split policy is allowed.")
        for name, value in {
            "embargo_ns": self.embargo_ns,
            "max_label_horizon_ns": self.max_label_horizon_ns,
            "max_feature_lookback_ns": self.max_feature_lookback_ns,
            "created_at_ns": self.created_at_ns,
        }.items():
            if value < 0:
                raise ValueError(f"{name} must be nonnegative.")
        if self.train.end_ns + self.embargo_ns > self.validation.start_ns:
            raise ValueError("train to validation embargo is too short.")
        if self.validation.end_ns + self.embargo_ns > self.test.start_ns:
            raise ValueError("validation to test embargo is too short.")
        required = self.max_label_horizon_ns + self.max_feature_lookback_ns
        if self.embargo_ns < required:
            raise ValueError("embargo must cover max label horizon plus lookback.")
        return self
