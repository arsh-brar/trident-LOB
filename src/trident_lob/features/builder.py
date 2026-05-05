"""Tiny offline feature builder for Phase 1C synthetic records."""

from __future__ import annotations

import math
from collections.abc import Sequence
from itertools import pairwise

from trident_lob.data.schemas import (
    BarRecord,
    CanonicalDataRecord,
    DataMode,
    MarketSide,
    QuoteRecord,
    TradeRecord,
)
from trident_lob.features.schemas import (
    FeatureFamily,
    FeatureQualityFlags,
    FeatureRow,
)

ONE_SECOND_NS = 1_000_000_000
ONE_MINUTE_NS = 60 * ONE_SECOND_NS
FIVE_MINUTES_NS = 5 * ONE_MINUTE_NS


class OfflineFeatureBuilder:
    """Builds conservative point-in-time rows from already validated records."""

    def __init__(
        self,
        *,
        tick_size: float = 0.01,
        max_feature_lookback_ns: int = FIVE_MINUTES_NS,
        feature_version: str = "phase1c_skeleton_v1",
    ) -> None:
        if tick_size <= 0:
            raise ValueError("tick_size must be positive.")
        self.tick_size = tick_size
        self.max_feature_lookback_ns = max_feature_lookback_ns
        self.feature_version = feature_version

    def build(
        self,
        records: Sequence[CanonicalDataRecord],
        *,
        prediction_times_ns: Sequence[int],
        symbol: str,
        data_mode: DataMode | None = None,
    ) -> list[FeatureRow]:
        return [
            self.build_one(
                records,
                t_pred_ns=t_pred_ns,
                symbol=symbol,
                data_mode=data_mode,
            )
            for t_pred_ns in prediction_times_ns
        ]

    def build_one(
        self,
        records: Sequence[CanonicalDataRecord],
        *,
        t_pred_ns: int,
        symbol: str,
        data_mode: DataMode | None = None,
    ) -> FeatureRow:
        bars = _eligible_bars(records, symbol=symbol, t_pred_ns=t_pred_ns)
        quotes = _eligible_quotes(records, symbol=symbol, t_pred_ns=t_pred_ns)
        trades = _eligible_trades(records, symbol=symbol, t_pred_ns=t_pred_ns)
        latest_bar = bars[-1] if bars else None
        latest_quote = quotes[-1] if quotes else None
        inferred_mode = data_mode or (DataMode.L1 if latest_quote else DataMode.BARS)
        if inferred_mode == DataMode.BARS:
            quotes = []
            trades = []
            latest_quote = None
        has_quotes = latest_quote is not None
        bars_only_degraded = inferred_mode == DataMode.BARS

        available_times = [0]
        if latest_bar is not None:
            available_times.append(latest_bar.available_at_ns)
        if latest_quote is not None:
            available_times.append(latest_quote.available_at_ns)
        available_times.extend(record.available_at_ns for record in trades)
        feature_available_at_max_ns = max(available_times)
        quality_flags = FeatureQualityFlags(
            has_bars=latest_bar is not None,
            has_quotes=has_quotes,
            has_trades=bool(trades),
            leakage_check_passed=feature_available_at_max_ns <= t_pred_ns,
            bars_only_degraded=bars_only_degraded,
        )
        common = {
            "symbol": symbol,
            "venue": _first_venue([latest_bar, latest_quote]),
            "t_pred_ns": t_pred_ns,
            "session_date": getattr(latest_bar, "asof_date", None),
            "tick_size": self.tick_size,
            "data_mode": inferred_mode,
            "max_feature_lookback_ns": self.max_feature_lookback_ns,
            "feature_available_at_max_ns": feature_available_at_max_ns,
            "feature_version": self.feature_version,
            "quality_flags": quality_flags,
            "feature_families": (
                FeatureFamily.ORDINARY_MICROSTRUCTURE,
                FeatureFamily.TECHNICAL_BASELINE,
            ),
        }

        technical = self._technical_features(bars, t_pred_ns=t_pred_ns)
        if not has_quotes or latest_quote is None:
            return FeatureRow.model_validate(
                {
                    **common,
                    **technical,
                    "unavailable_feature_reasons": (
                        "quote_dependent_features_unavailable",
                        "bars_only_degraded_mode",
                    ),
                }
            )

        microstructure = self._quote_features(quotes, trades, latest_quote)
        return FeatureRow.model_validate({**common, **technical, **microstructure})

    def _technical_features(
        self,
        bars: Sequence[BarRecord],
        *,
        t_pred_ns: int,
    ) -> dict[str, float | int | None]:
        latest_bar = bars[-1] if bars else None
        recent_bars = [
            bar
            for bar in bars
            if bar.event_end_ns >= t_pred_ns - self.max_feature_lookback_ns
        ]
        if latest_bar is None:
            return {
                "session_minute": None,
                "ret_lag_60s": None,
                "realized_vol_300s": None,
                "volume_300s": None,
                "dollar_volume_300s": None,
                "vwap_distance_60s": None,
                "range_hl_60s": None,
                "momentum_300s": None,
                "reversal_60s": None,
                "ma_gap_300s": None,
            }
        returns = [
            math.log(bar.close / bar.open)
            for bar in recent_bars
            if bar.open > 0 and bar.close > 0
        ]
        realized_vol = math.sqrt(sum(value * value for value in returns))
        volume = sum(bar.volume for bar in recent_bars)
        dollar_volume = sum(bar.volume * (bar.vwap or bar.close) for bar in recent_bars)
        average_close = sum(bar.close for bar in recent_bars) / len(recent_bars)
        ret_lag = math.log(latest_bar.close / latest_bar.open)
        return {
            "session_minute": int(
                (latest_bar.event_end_ns - latest_bar.event_start_ns) // ONE_MINUTE_NS
            ),
            "ret_lag_60s": ret_lag,
            "realized_vol_300s": realized_vol,
            "volume_300s": volume,
            "dollar_volume_300s": dollar_volume,
            "vwap_distance_60s": _difference_or_none(
                latest_bar.close,
                latest_bar.vwap,
            ),
            "range_hl_60s": latest_bar.high - latest_bar.low,
            "momentum_300s": math.log(latest_bar.close / recent_bars[0].open),
            "reversal_60s": -ret_lag,
            "ma_gap_300s": latest_bar.close - average_close,
        }

    def _quote_features(
        self,
        quotes: Sequence[QuoteRecord],
        trades: Sequence[TradeRecord],
        latest_quote: QuoteRecord,
    ) -> dict[str, float | int | None]:
        spread = latest_quote.ask_price - latest_quote.bid_price
        mid = (latest_quote.ask_price + latest_quote.bid_price) / 2.0
        spread_ticks = spread / self.tick_size
        prior_quote = quotes[-2] if len(quotes) >= 2 else None
        prior_mid = (
            (prior_quote.ask_price + prior_quote.bid_price) / 2.0
            if prior_quote is not None
            else None
        )
        signed_size = sum(
            trade.size
            if trade.aggressor_side == MarketSide.BUY
            else -trade.size
            if trade.aggressor_side == MarketSide.SELL
            else 0.0
            for trade in trades
        )
        total_size = sum(trade.size for trade in trades)
        return {
            "spread_ticks": spread_ticks,
            "spread_bps": spread / mid * 10_000.0,
            "mid_price": mid,
            "mid_ticks": mid / self.tick_size,
            "bid_size": latest_quote.bid_size,
            "ask_size": latest_quote.ask_size,
            "D_top": latest_quote.bid_size + latest_quote.ask_size,
            "D_top_harmonic": _harmonic_depth(
                latest_quote.bid_size,
                latest_quote.ask_size,
            ),
            "D_top_min": min(latest_quote.bid_size, latest_quote.ask_size),
            "queue_imbalance": _safe_divide(
                latest_quote.bid_size - latest_quote.ask_size,
                latest_quote.bid_size + latest_quote.ask_size,
            ),
            "OFI_60s": _ofi_60s(quotes),
            "signed_trade_imbalance_60s": (
                _safe_divide(signed_size, total_size) if total_size > 0 else None
            ),
            "trade_count_60s": len(trades),
            "quote_update_count_60s": len(quotes),
            "spread_change_60s": (
                spread - (prior_quote.ask_price - prior_quote.bid_price)
                if prior_quote is not None
                else None
            ),
            "trident_L_L1_proxy": _safe_divide(
                latest_quote.bid_size + latest_quote.ask_size,
                spread_ticks,
            ),
            "ret_lag_60s": _log_return_or_none(mid, prior_mid),
        }


def _eligible_bars(
    records: Sequence[CanonicalDataRecord],
    *,
    symbol: str,
    t_pred_ns: int,
) -> list[BarRecord]:
    bars = [
        record
        for record in records
        if isinstance(record, BarRecord)
        and record.symbol == symbol
        and record.event_end_ns <= t_pred_ns
        and record.available_at_ns <= t_pred_ns
    ]
    return sorted(
        bars,
        key=lambda record: (record.event_end_ns, record.available_at_ns),
    )


def _eligible_quotes(
    records: Sequence[CanonicalDataRecord],
    *,
    symbol: str,
    t_pred_ns: int,
) -> list[QuoteRecord]:
    quotes = [
        record
        for record in records
        if isinstance(record, QuoteRecord)
        and record.symbol == symbol
        and record.event_ts_ns <= t_pred_ns
        and record.available_at_ns <= t_pred_ns
    ]
    return sorted(
        quotes,
        key=lambda record: (record.event_ts_ns, record.available_at_ns),
    )


def _eligible_trades(
    records: Sequence[CanonicalDataRecord],
    *,
    symbol: str,
    t_pred_ns: int,
) -> list[TradeRecord]:
    trades = [
        record
        for record in records
        if isinstance(record, TradeRecord)
        and record.symbol == symbol
        and record.event_ts_ns <= t_pred_ns
        and record.available_at_ns <= t_pred_ns
        and record.event_ts_ns >= t_pred_ns - ONE_MINUTE_NS
    ]
    return sorted(
        trades,
        key=lambda record: (record.event_ts_ns, record.available_at_ns),
    )


def _ofi_60s(quotes: Sequence[QuoteRecord]) -> float | None:
    if len(quotes) < 2:
        return None
    total = 0.0
    for previous, current in pairwise(quotes):
        bid_component = (
            current.bid_size
            if current.bid_price >= previous.bid_price
            else -previous.bid_size
        )
        ask_component = (
            -current.ask_size
            if current.ask_price <= previous.ask_price
            else previous.ask_size
        )
        total += bid_component + ask_component
    return total


def _safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _difference_or_none(left: float, right: float | None) -> float | None:
    if right is None:
        return None
    return left - right


def _log_return_or_none(current: float, prior: float | None) -> float | None:
    if prior is None or prior <= 0:
        return None
    return math.log(current / prior)


def _harmonic_depth(bid_size: float, ask_size: float) -> float | None:
    if bid_size <= 0 or ask_size <= 0:
        return None
    return 2.0 / (1.0 / bid_size + 1.0 / ask_size)


def _first_venue(records: Sequence[BarRecord | QuoteRecord | None]) -> str | None:
    for record in records:
        if record is not None:
            return record.venue
    return None
