"""Point-in-time feature records and leakage report schemas."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from trident_lob.data.schemas import DataMode, StrictBoundaryModel


class FeatureFamily(StrEnum):
    ORDINARY_MICROSTRUCTURE = "ordinary_microstructure"
    TECHNICAL_BASELINE = "technical_baseline"
    TRIDENT_PROXY = "trident_proxy"
    NEWS = "news"


class LeakageStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"


class LeakageReason(StrEnum):
    FEATURE_AVAILABLE_AFTER_PREDICTION = "feature_available_after_prediction"
    NEWS_AVAILABLE_AFTER_PREDICTION = "news_available_after_prediction"
    NEWS_PUBLISHED_AFTER_PREDICTION = "news_published_after_prediction"
    CALENDAR_ACTUAL_NOT_AVAILABLE = "calendar_actual_not_available"
    SPLIT_EMBARGO_TOO_SHORT = "split_embargo_too_short"
    MISSING_AVAILABILITY_METADATA = "missing_availability_metadata"


class FeatureQualityFlags(StrictBoundaryModel):
    has_bars: bool = False
    has_quotes: bool = False
    has_trades: bool = False
    has_news: bool = False
    is_regular_session: bool = True
    is_halted: bool = False
    is_luld_state: bool = False
    is_stale_quote: bool = False
    has_crossed_or_locked_quote: bool = False
    leakage_check_passed: bool = True
    bars_only_degraded: bool = False


class FeatureRow(StrictBoundaryModel):
    symbol: str
    t_pred_ns: int
    feature_available_at_max_ns: int
    max_feature_lookback_ns: int
    data_mode: DataMode
    quality_flags: FeatureQualityFlags
    feature_families: tuple[FeatureFamily, ...]
    feature_version: str = "phase1c_skeleton_v1"
    venue: str | None = None
    session_date: str | None = None
    tick_size: float = 0.01
    currency: str = "USD"
    unavailable_feature_reasons: tuple[str, ...] = Field(default_factory=tuple)
    spread_ticks: float | None = None
    spread_bps: float | None = None
    mid_price: float | None = None
    mid_ticks: float | None = None
    bid_size: float | None = None
    ask_size: float | None = None
    D_top: float | None = None
    D_top_harmonic: float | None = None
    D_top_min: float | None = None
    queue_imbalance: float | None = None
    OFI_60s: float | None = None
    signed_trade_imbalance_60s: float | None = None
    trade_count_60s: int | None = None
    quote_update_count_60s: int | None = None
    spread_change_60s: float | None = None
    session_minute: int | None = None
    ret_lag_60s: float | None = None
    realized_vol_300s: float | None = None
    volume_300s: float | None = None
    dollar_volume_300s: float | None = None
    vwap_distance_60s: float | None = None
    range_hl_60s: float | None = None
    momentum_300s: float | None = None
    reversal_60s: float | None = None
    ma_gap_300s: float | None = None
    trident_k_60s: float | None = None
    trident_epsilon_60s: float | None = None
    trident_nu_t_60s: float | None = None
    trident_fragility_60s: float | None = None
    trident_R_m_60s: float | None = None
    trident_P_imbalance_60s: float | None = None
    trident_P_withdrawal_60s: float | None = None
    trident_L_L1_proxy: float | None = None

    @model_validator(mode="after")
    def validate_point_in_time_and_degraded_mode(self) -> Self:
        if self.t_pred_ns < 0 or self.feature_available_at_max_ns < 0:
            raise ValueError("feature timestamps must be nonnegative UTC nanoseconds.")
        if self.max_feature_lookback_ns < 0:
            raise ValueError("max_feature_lookback_ns must be nonnegative.")
        if self.feature_available_at_max_ns > self.t_pred_ns:
            raise ValueError("feature_available_at_max_ns must be <= t_pred_ns.")
        if self.tick_size <= 0:
            raise ValueError("tick_size must be positive.")
        if self.data_mode == DataMode.BARS or self.quality_flags.bars_only_degraded:
            quote_values = (
                self.spread_ticks,
                self.spread_bps,
                self.bid_size,
                self.ask_size,
                self.D_top,
                self.queue_imbalance,
                self.OFI_60s,
                self.trident_L_L1_proxy,
            )
            if any(value is not None for value in quote_values):
                raise ValueError(
                    "bars-only rows must not contain observed quote features."
                )
        nonnegative_fields = {
            "spread_ticks": self.spread_ticks,
            "spread_bps": self.spread_bps,
            "bid_size": self.bid_size,
            "ask_size": self.ask_size,
            "D_top": self.D_top,
            "D_top_harmonic": self.D_top_harmonic,
            "D_top_min": self.D_top_min,
            "realized_vol_300s": self.realized_vol_300s,
            "volume_300s": self.volume_300s,
            "dollar_volume_300s": self.dollar_volume_300s,
            "trident_k_60s": self.trident_k_60s,
            "trident_nu_t_60s": self.trident_nu_t_60s,
            "trident_fragility_60s": self.trident_fragility_60s,
        }
        for name, value in nonnegative_fields.items():
            if value is not None and value < 0:
                raise ValueError(f"{name} must be nonnegative.")
        if self.trident_epsilon_60s is not None and self.trident_epsilon_60s <= 0:
            raise ValueError("trident_epsilon_60s must be positive.")
        return self


class LeakageFinding(StrictBoundaryModel):
    reason: LeakageReason
    symbol: str | None = None
    t_pred_ns: int | None = None
    detail: str


class LeakageReport(StrictBoundaryModel):
    report_id: str
    status: LeakageStatus
    checked_row_count: int
    max_feature_available_at_ns: int | None = None
    findings: tuple[LeakageFinding, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def validate_fail_closed_status(self) -> Self:
        if self.findings and self.status != LeakageStatus.FAIL:
            raise ValueError("leakage reports with findings must fail.")
        if not self.findings and self.status != LeakageStatus.PASS:
            raise ValueError("leakage reports without findings must pass.")
        return self
