"""Provider-neutral data records and manifests for offline Phase 1 research."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RecordType(StrEnum):
    BAR = "bar"
    QUOTE = "quote"
    TRADE = "trade"
    DEPTH = "depth"
    NEWS = "news"
    CALENDAR = "calendar"
    CORPORATE_ACTION = "corporate_action"


class DelayClass(StrEnum):
    SYNTHETIC = "synthetic"
    REPLAY = "replay"
    HISTORICAL_ARCHIVE = "historical_archive"
    DELAYED = "delayed"
    END_OF_DAY = "end_of_day"
    REAL_TIME = "real_time"


class LicenseClass(StrEnum):
    FREE = "free"
    DELAYED = "delayed"
    PAID = "paid"
    RESEARCH_ONLY = "research-only"
    PAPER_TRADING_SUITABLE = "paper-trading-suitable"
    ENGINEERING_FIXTURE = "engineering_fixture"


class DataMode(StrEnum):
    BARS = "bars"
    L1 = "l1"
    L2 = "l2"
    L3 = "l3"
    SYNTHETIC = "synthetic"


class SuitabilityLabel(StrEnum):
    ENGINEERING_FIXTURE = "engineering_fixture"
    PHASE1_RESEARCH = "phase1_research"
    PAPER_TRADING = "paper_trading"
    SERIOUS_L2_VALIDATION = "serious_l2_validation"
    FULL_L3_VERIFICATION = "full_l3_verification"
    NOT_FOR_LIVE_TRADING = "not_for_live_trading"


class MarketSide(StrEnum):
    BUY = "buy"
    SELL = "sell"
    UNKNOWN = "unknown"


class BookSide(StrEnum):
    BID = "bid"
    ASK = "ask"


class DepthType(StrEnum):
    MBP_1 = "mbp_1"
    MBP_10 = "mbp_10"
    L2_SNAPSHOT = "l2_snapshot"
    L2_DELTA = "l2_delta"
    MBO = "mbo"
    SYNTHETIC = "synthetic"


class DepthAction(StrEnum):
    SNAPSHOT = "snapshot"
    ADD = "add"
    MODIFY = "modify"
    CANCEL = "cancel"
    CLEAR = "clear"


class CorporateActionType(StrEnum):
    SPLIT = "split"
    DIVIDEND = "dividend"
    SYMBOL_CHANGE = "symbol_change"
    OTHER = "other"


class CalendarEventType(StrEnum):
    MARKET_SESSION = "market_session"
    EARLY_CLOSE = "early_close"
    HOLIDAY = "holiday"
    MACRO_SCHEDULED = "macro_scheduled"
    EARNINGS_SCHEDULED = "earnings_scheduled"


class TimestampQuality(StrEnum):
    EXACT_UTC_NS = "exact_utc_ns"
    PROVIDER_UTC = "provider_utc"
    OFFICIAL_SCHEDULE = "official_schedule"
    CONSERVATIVE_IMPUTED = "conservative_imputed"


class StrictBoundaryModel(BaseModel):
    """Strict external boundary model used for records and manifests."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


def _ensure_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive.")


def _ensure_nonnegative(name: str, value: float | int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be nonnegative.")


class CanonicalRecord(StrictBoundaryModel):
    record_type: RecordType
    provider: str
    dataset: str
    symbol: str
    venue: str
    feed: str
    event_ts_ns: int
    available_at_ns: int
    source: str
    raw_payload_ref: str | None = None
    payload_hash: str | None = None

    @model_validator(mode="after")
    def validate_common_timestamps(self) -> Self:
        if self.event_ts_ns < 0 or self.available_at_ns < 0:
            raise ValueError("timestamps must be nonnegative UTC nanoseconds.")
        return self


class BarRecord(CanonicalRecord):
    record_type: RecordType = RecordType.BAR
    interval: str
    event_start_ns: int
    event_end_ns: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float | None = None
    trade_count: int | None = None
    adjustment_policy: str = "raw"
    asof_date: str | None = None

    @model_validator(mode="after")
    def validate_bar(self) -> Self:
        if self.event_start_ns >= self.event_end_ns:
            raise ValueError("bar start must be before bar end.")
        if self.event_ts_ns != self.event_end_ns:
            raise ValueError("bar event_ts_ns must equal event_end_ns.")
        if self.available_at_ns < self.event_end_ns:
            raise ValueError("bar available_at_ns must be at or after event_end_ns.")
        for name, value in {
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
        }.items():
            _ensure_positive(name, value)
        _ensure_nonnegative("volume", self.volume)
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("bar low is inconsistent with OHLC values.")
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("bar high is inconsistent with OHLC values.")
        if self.vwap is not None:
            _ensure_positive("vwap", self.vwap)
        if self.trade_count is not None:
            _ensure_nonnegative("trade_count", self.trade_count)
        return self


class QuoteRecord(CanonicalRecord):
    record_type: RecordType = RecordType.QUOTE
    sequence: int | None = None
    bid_price: float
    bid_size: float
    ask_price: float
    ask_size: float
    bid_exchange: str | None = None
    ask_exchange: str | None = None
    is_nbbo: bool = False
    delay_class: DelayClass = DelayClass.SYNTHETIC

    @model_validator(mode="after")
    def validate_quote(self) -> Self:
        if self.available_at_ns < self.event_ts_ns:
            raise ValueError("quote availability cannot precede event time.")
        _ensure_positive("bid_price", self.bid_price)
        _ensure_positive("ask_price", self.ask_price)
        _ensure_nonnegative("bid_size", self.bid_size)
        _ensure_nonnegative("ask_size", self.ask_size)
        if self.bid_price >= self.ask_price:
            raise ValueError("bid_price must be less than ask_price.")
        if self.sequence is not None:
            _ensure_nonnegative("sequence", self.sequence)
        return self


class TradeRecord(CanonicalRecord):
    record_type: RecordType = RecordType.TRADE
    sequence: int | None = None
    trade_id: str
    price: float
    size: float
    aggressor_side: MarketSide = MarketSide.UNKNOWN
    conditions: tuple[str, ...] = ()
    is_correction: bool = False

    @model_validator(mode="after")
    def validate_trade(self) -> Self:
        if self.available_at_ns < self.event_ts_ns:
            raise ValueError("trade availability cannot precede event time.")
        _ensure_positive("price", self.price)
        _ensure_positive("size", self.size)
        if self.sequence is not None:
            _ensure_nonnegative("sequence", self.sequence)
        return self


class DepthRecord(CanonicalRecord):
    record_type: RecordType = RecordType.DEPTH
    sequence: int
    side: BookSide
    price: float
    size: float
    level: int
    depth_type: DepthType = DepthType.SYNTHETIC
    action: DepthAction = DepthAction.SNAPSHOT
    order_count: int | None = None
    checksum: str | None = None

    @model_validator(mode="after")
    def validate_depth(self) -> Self:
        if self.available_at_ns < self.event_ts_ns:
            raise ValueError("depth availability cannot precede event time.")
        _ensure_nonnegative("sequence", self.sequence)
        _ensure_positive("price", self.price)
        _ensure_nonnegative("size", self.size)
        if self.level < 1:
            raise ValueError("level must be at least 1.")
        if self.order_count is not None:
            _ensure_nonnegative("order_count", self.order_count)
        return self


class NewsEventRecord(CanonicalRecord):
    record_type: RecordType = RecordType.NEWS
    event_id: str
    provider_event_id: str | None = None
    source_name: str
    source_url: str
    event_type: str
    title: str
    summary: str | None = None
    language: str = "en"
    source_published_at_ns: int
    provider_created_at_ns: int | None = None
    provider_updated_at_ns: int | None = None
    provider_removed_at_ns: int | None = None
    first_seen_at_ns: int
    symbols: tuple[str, ...]
    primary_symbols: tuple[str, ...] = ()
    topics: tuple[str, ...] = ()
    normalized_sentiment: float = 0.0
    normalized_relevance: float = 1.0
    novelty_group: str | None = None
    market_wide: bool = False
    timestamp_quality: TimestampQuality = TimestampQuality.EXACT_UTC_NS

    @field_validator("symbols")
    @classmethod
    def validate_symbols(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if not value:
            raise ValueError("news symbols must not be empty.")
        return value

    @model_validator(mode="after")
    def validate_news(self) -> Self:
        if self.event_ts_ns != self.source_published_at_ns:
            raise ValueError("news event_ts_ns must equal source_published_at_ns.")
        if self.first_seen_at_ns < self.source_published_at_ns:
            raise ValueError("first_seen_at_ns must be at or after publication time.")
        if self.available_at_ns < self.first_seen_at_ns:
            raise ValueError("available_at_ns must be at or after first_seen_at_ns.")
        if not -1.0 <= self.normalized_sentiment <= 1.0:
            raise ValueError("normalized_sentiment must be in [-1, 1].")
        if not 0.0 <= self.normalized_relevance <= 1.0:
            raise ValueError("normalized_relevance must be in [0, 1].")
        return self


class CalendarRecord(CanonicalRecord):
    record_type: RecordType = RecordType.CALENDAR
    calendar_id: str
    session_date: str
    event_type: CalendarEventType
    event_name: str
    scheduled_at_ns: int
    calendar_known_at_ns: int
    open_ts_ns: int | None = None
    close_ts_ns: int | None = None
    actual_available_at_ns: int | None = None
    is_open: bool = True
    is_early_close: bool = False
    holiday_name: str | None = None
    timestamp_quality: TimestampQuality = TimestampQuality.OFFICIAL_SCHEDULE

    @model_validator(mode="after")
    def validate_calendar(self) -> Self:
        if self.event_ts_ns != self.scheduled_at_ns:
            raise ValueError("calendar event_ts_ns must equal scheduled_at_ns.")
        if self.available_at_ns < self.calendar_known_at_ns:
            raise ValueError(
                "available_at_ns must be at or after calendar_known_at_ns."
            )
        if self.open_ts_ns is not None and self.close_ts_ns is not None:
            if self.open_ts_ns >= self.close_ts_ns:
                raise ValueError("session open must be before close.")
        if self.actual_available_at_ns is not None:
            if self.actual_available_at_ns < self.scheduled_at_ns:
                raise ValueError("actual availability cannot precede scheduled time.")
        return self


class CorporateActionRecord(CanonicalRecord):
    record_type: RecordType = RecordType.CORPORATE_ACTION
    action_id: str
    effective_date: str
    effective_ts_ns: int
    action_type: CorporateActionType
    split_ratio: float | None = None
    cash_amount: float | None = None
    currency: str | None = None
    raw_symbol: str | None = None
    new_symbol: str | None = None
    source_url: str
    asof_date: str

    @model_validator(mode="after")
    def validate_corporate_action(self) -> Self:
        if self.event_ts_ns != self.effective_ts_ns:
            raise ValueError("corporate action event_ts_ns must equal effective_ts_ns.")
        if self.split_ratio is not None:
            _ensure_positive("split_ratio", self.split_ratio)
        if self.cash_amount is not None:
            _ensure_nonnegative("cash_amount", self.cash_amount)
        return self


MarketDataRecord = BarRecord | QuoteRecord | TradeRecord | DepthRecord
CanonicalDataRecord = (
    BarRecord
    | QuoteRecord
    | TradeRecord
    | DepthRecord
    | NewsEventRecord
    | CalendarRecord
    | CorporateActionRecord
)


class DatasetManifest(StrictBoundaryModel):
    dataset_id: str
    provider: str
    dataset: str
    source: str
    source_url: str
    license_class: LicenseClass
    delay_class: DelayClass
    data_mode: DataMode
    timestamp_start_ns: int
    timestamp_end_ns: int
    row_count: int
    content_hash: str
    payload_hash_ref: str | None = None
    secret_free: bool = True
    paid_payload_free: bool = True
    may_commit_payload: bool = False
    redistribution_allowed: bool = False
    suitability_labels: tuple[SuitabilityLabel, ...] = Field(
        default=(
            SuitabilityLabel.ENGINEERING_FIXTURE,
            SuitabilityLabel.NOT_FOR_LIVE_TRADING,
        )
    )
    schema_version: str = "0.1"

    @model_validator(mode="after")
    def validate_manifest_safety(self) -> Self:
        if self.timestamp_start_ns > self.timestamp_end_ns:
            raise ValueError("manifest timestamp range is invalid.")
        _ensure_nonnegative("row_count", self.row_count)
        if not self.secret_free:
            raise ValueError("manifest is not secret-free.")
        if not self.paid_payload_free:
            raise ValueError("manifest is not paid-payload-free.")
        if self.license_class is LicenseClass.PAID and self.may_commit_payload:
            raise ValueError("paid payloads may not be committed.")
        if self.may_commit_payload and not self.redistribution_allowed:
            raise ValueError("committed payloads require redistribution allowance.")
        return self


class EventBatchManifest(DatasetManifest):
    batch_id: str
    record_type: RecordType
    partition_keys: tuple[str, ...] = ("provider", "dataset", "symbol", "record_type")
    storage_uri: str | None = None


def canonical_record_to_row(record: CanonicalDataRecord) -> dict[str, Any]:
    return record.model_dump(mode="json")
