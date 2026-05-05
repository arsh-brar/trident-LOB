"""Tiny offline label builder for one and five minute horizons."""

from __future__ import annotations

import math
from collections.abc import Sequence

from trident_lob.data.schemas import BarRecord, CanonicalDataRecord, QuoteRecord
from trident_lob.labels.schemas import DirectionLabel, LabelNullReason, LabelRow


class OfflineLabelBuilder:
    def __init__(
        self,
        *,
        tick_size: float = 0.01,
        cost_ticks: float = 1.0,
        buffer_ticks: float = 0.0,
        label_version: str = "phase1c_skeleton_v1",
    ) -> None:
        if tick_size <= 0:
            raise ValueError("tick_size must be positive.")
        if cost_ticks < 0 or buffer_ticks < 0:
            raise ValueError("cost_ticks and buffer_ticks must be nonnegative.")
        self.tick_size = tick_size
        self.cost_ticks = cost_ticks
        self.buffer_ticks = buffer_ticks
        self.label_version = label_version

    def build(
        self,
        records: Sequence[CanonicalDataRecord],
        *,
        prediction_times_ns: Sequence[int],
        symbol: str,
        horizon_seconds: Sequence[int] = (60, 300),
    ) -> list[LabelRow]:
        rows: list[LabelRow] = []
        for t_pred_ns in prediction_times_ns:
            for horizon in horizon_seconds:
                rows.append(
                    self.build_one(
                        records,
                        symbol=symbol,
                        t_pred_ns=t_pred_ns,
                        horizon_seconds=horizon,
                    )
                )
        return rows

    def build_one(
        self,
        records: Sequence[CanonicalDataRecord],
        *,
        symbol: str,
        t_pred_ns: int,
        horizon_seconds: int,
    ) -> LabelRow:
        if horizon_seconds <= 0:
            return _null_label(
                symbol=symbol,
                t_pred_ns=t_pred_ns,
                horizon_seconds=horizon_seconds,
                reason=LabelNullReason.INVALID_HORIZON,
                cost_ticks=self.cost_ticks,
                buffer_ticks=self.buffer_ticks,
                label_version=self.label_version,
            )
        current = _asof_mid(
            records,
            symbol=symbol,
            t_pred_ns=t_pred_ns,
            tick_size=self.tick_size,
        )
        if current is None:
            return _null_label(
                symbol=symbol,
                t_pred_ns=t_pred_ns,
                horizon_seconds=horizon_seconds,
                reason=LabelNullReason.MISSING_CURRENT_MID,
                cost_ticks=self.cost_ticks,
                buffer_ticks=self.buffer_ticks,
                label_version=self.label_version,
            )
        target_ns = t_pred_ns + horizon_seconds * 1_000_000_000
        future = _future_mid(
            records,
            symbol=symbol,
            target_ns=target_ns,
            tick_size=self.tick_size,
        )
        if future is None:
            return _null_label(
                symbol=symbol,
                t_pred_ns=t_pred_ns,
                horizon_seconds=horizon_seconds,
                reason=LabelNullReason.MISSING_FUTURE_OUTCOME,
                cost_ticks=self.cost_ticks,
                buffer_ticks=self.buffer_ticks,
                label_version=self.label_version,
            )
        return_ticks = (future.mid_price - current.mid_price) / self.tick_size
        neutral_band = self.cost_ticks + self.buffer_ticks
        direction = DirectionLabel.FLAT
        if return_ticks > neutral_band:
            direction = DirectionLabel.UP
        elif return_ticks < -neutral_band:
            direction = DirectionLabel.DOWN
        spread_widen = (
            future.spread_ticks is not None
            and current.spread_ticks is not None
            and future.spread_ticks > current.spread_ticks
        )
        return LabelRow(
            symbol=symbol,
            t_pred_ns=t_pred_ns,
            horizon_seconds=horizon_seconds,
            label_available_at_min_ns=future.available_at_ns,
            label_version=self.label_version,
            y_return_log=math.log(future.mid_price / current.mid_price),
            y_return_ticks=return_ticks,
            y_return_bps=(future.mid_price / current.mid_price - 1.0) * 10_000.0,
            y_dir_cost_aware=direction,
            y_spread_widen=spread_widen,
            y_local_jump=abs(return_ticks) > neutral_band * 2.0,
            y_depth_deplete=None,
            y_fragility_persist=None,
            cost_ticks=self.cost_ticks,
            buffer_ticks=self.buffer_ticks,
            null_reason=LabelNullReason.NONE,
        )


class _MidObservation:
    def __init__(
        self,
        *,
        mid_price: float,
        available_at_ns: int,
        event_ts_ns: int,
        spread_ticks: float | None,
    ) -> None:
        self.mid_price = mid_price
        self.available_at_ns = available_at_ns
        self.event_ts_ns = event_ts_ns
        self.spread_ticks = spread_ticks


def _asof_mid(
    records: Sequence[CanonicalDataRecord],
    *,
    symbol: str,
    t_pred_ns: int,
    tick_size: float,
) -> _MidObservation | None:
    observations: list[_MidObservation] = []
    for observation in _mid_observations(
        records,
        symbol=symbol,
        tick_size=tick_size,
    ):
        if observation.event_ts_ns > t_pred_ns:
            continue
        if observation.available_at_ns > t_pred_ns:
            continue
        observations.append(observation)
    return max(
        observations,
        key=lambda item: (item.event_ts_ns, item.available_at_ns),
        default=None,
    )


def _future_mid(
    records: Sequence[CanonicalDataRecord],
    *,
    symbol: str,
    target_ns: int,
    tick_size: float,
) -> _MidObservation | None:
    observations: list[_MidObservation] = []
    for observation in _mid_observations(
        records,
        symbol=symbol,
        tick_size=tick_size,
    ):
        if observation.event_ts_ns < target_ns:
            continue
        if observation.available_at_ns < target_ns:
            continue
        observations.append(observation)
    return min(
        observations,
        key=lambda item: (item.event_ts_ns, item.available_at_ns),
        default=None,
    )


def _mid_observations(
    records: Sequence[CanonicalDataRecord],
    *,
    symbol: str,
    tick_size: float,
) -> list[_MidObservation]:
    observations: list[_MidObservation] = []
    for record in records:
        if record.symbol != symbol:
            continue
        if isinstance(record, QuoteRecord):
            spread = record.ask_price - record.bid_price
            observations.append(
                _MidObservation(
                    mid_price=(record.ask_price + record.bid_price) / 2.0,
                    available_at_ns=record.available_at_ns,
                    event_ts_ns=record.event_ts_ns,
                    spread_ticks=spread / tick_size,
                )
            )
        if isinstance(record, BarRecord):
            observations.append(
                _MidObservation(
                    mid_price=record.close,
                    available_at_ns=record.available_at_ns,
                    event_ts_ns=record.event_end_ns,
                    spread_ticks=None,
                )
            )
    return observations


def _null_label(
    *,
    symbol: str,
    t_pred_ns: int,
    horizon_seconds: int,
    reason: LabelNullReason,
    cost_ticks: float,
    buffer_ticks: float,
    label_version: str,
) -> LabelRow:
    return LabelRow(
        symbol=symbol,
        t_pred_ns=t_pred_ns,
        horizon_seconds=horizon_seconds,
        label_available_at_min_ns=None,
        label_version=label_version,
        cost_ticks=cost_ticks,
        buffer_ticks=buffer_ticks,
        null_reason=reason,
    )
