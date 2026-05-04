"""Tiny offline-only synthetic fixtures for schema and store validation."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence

from trident_lob.data.schemas import (
    BarRecord,
    BookSide,
    CalendarEventType,
    CalendarRecord,
    CanonicalDataRecord,
    CorporateActionRecord,
    CorporateActionType,
    DataMode,
    DelayClass,
    DepthAction,
    DepthRecord,
    DepthType,
    EventBatchManifest,
    LicenseClass,
    NewsEventRecord,
    QuoteRecord,
    RecordType,
    SuitabilityLabel,
    TradeRecord,
    canonical_record_to_row,
)

BASE_TS_NS = 1_735_689_600_000_000_000
ONE_SECOND_NS = 1_000_000_000
ONE_MINUTE_NS = 60 * ONE_SECOND_NS


def content_hash_for_records(records: Sequence[CanonicalDataRecord]) -> str:
    rows = [canonical_record_to_row(record) for record in records]
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


class SyntheticFixtureAdapter:
    """Offline fixture builder that never reaches external services."""

    provider = "synthetic"
    dataset = "tiny_phase1_fixture"
    venue = "XTEST"
    feed = "synthetic"
    source = "synthetic_fixture"
    source_url = "file://synthetic-fixture"

    def market_records(self) -> list[CanonicalDataRecord]:
        return [
            BarRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + ONE_MINUTE_NS,
                available_at_ns=BASE_TS_NS + ONE_MINUTE_NS + ONE_SECOND_NS,
                source=self.source,
                interval="1m",
                event_start_ns=BASE_TS_NS,
                event_end_ns=BASE_TS_NS + ONE_MINUTE_NS,
                open=100.0,
                high=101.0,
                low=99.5,
                close=100.5,
                volume=1_000.0,
                vwap=100.25,
                trade_count=10,
            ),
            QuoteRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + 2 * ONE_SECOND_NS,
                available_at_ns=BASE_TS_NS + 3 * ONE_SECOND_NS,
                source=self.source,
                sequence=1,
                bid_price=100.0,
                bid_size=50.0,
                ask_price=100.1,
                ask_size=60.0,
            ),
            TradeRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + 4 * ONE_SECOND_NS,
                available_at_ns=BASE_TS_NS + 5 * ONE_SECOND_NS,
                source=self.source,
                sequence=2,
                trade_id="T-1",
                price=100.05,
                size=25.0,
            ),
            DepthRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + 6 * ONE_SECOND_NS,
                available_at_ns=BASE_TS_NS + 7 * ONE_SECOND_NS,
                source=self.source,
                sequence=3,
                side=BookSide.BID,
                price=99.9,
                size=40.0,
                level=1,
                depth_type=DepthType.SYNTHETIC,
                action=DepthAction.SNAPSHOT,
                order_count=2,
            ),
        ]

    def exogenous_records(self) -> list[CanonicalDataRecord]:
        return [
            NewsEventRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + 8 * ONE_SECOND_NS,
                available_at_ns=BASE_TS_NS + 9 * ONE_SECOND_NS,
                source=self.source,
                event_id="NEWS-1",
                source_name="Synthetic Research Fixture",
                source_url=self.source_url,
                event_type="news_article",
                title="Synthetic neutral research headline",
                summary="Tiny safe fixture summary.",
                source_published_at_ns=BASE_TS_NS + 8 * ONE_SECOND_NS,
                first_seen_at_ns=BASE_TS_NS + 9 * ONE_SECOND_NS,
                symbols=("TEST",),
                normalized_sentiment=0.0,
                normalized_relevance=1.0,
                novelty_group="synthetic-neutral",
            ),
            CalendarRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + 10 * ONE_MINUTE_NS,
                available_at_ns=BASE_TS_NS,
                source=self.source,
                calendar_id="SESSION-1",
                session_date="2025-01-01",
                event_type=CalendarEventType.MARKET_SESSION,
                event_name="Synthetic regular session",
                scheduled_at_ns=BASE_TS_NS + 10 * ONE_MINUTE_NS,
                calendar_known_at_ns=BASE_TS_NS,
                open_ts_ns=BASE_TS_NS,
                close_ts_ns=BASE_TS_NS + 390 * ONE_MINUTE_NS,
            ),
            CorporateActionRecord(
                provider=self.provider,
                dataset=self.dataset,
                symbol="TEST",
                venue=self.venue,
                feed=self.feed,
                event_ts_ns=BASE_TS_NS + 86_400 * ONE_SECOND_NS,
                available_at_ns=BASE_TS_NS,
                source=self.source,
                action_id="CA-1",
                effective_date="2025-01-02",
                effective_ts_ns=BASE_TS_NS + 86_400 * ONE_SECOND_NS,
                action_type=CorporateActionType.SPLIT,
                split_ratio=1.0,
                source_url=self.source_url,
                asof_date="2025-01-01",
            ),
        ]

    def all_records(self) -> list[CanonicalDataRecord]:
        return [*self.market_records(), *self.exogenous_records()]

    def manifest_for(
        self,
        records: Sequence[CanonicalDataRecord],
        *,
        batch_id: str = "synthetic-batch-001",
        record_type: RecordType = RecordType.QUOTE,
    ) -> EventBatchManifest:
        timestamps = [record.event_ts_ns for record in records]
        return EventBatchManifest(
            dataset_id=f"{self.provider}:{self.dataset}:{batch_id}",
            batch_id=batch_id,
            provider=self.provider,
            dataset=self.dataset,
            source=self.source,
            source_url=self.source_url,
            license_class=LicenseClass.ENGINEERING_FIXTURE,
            delay_class=DelayClass.SYNTHETIC,
            data_mode=DataMode.SYNTHETIC,
            timestamp_start_ns=min(timestamps),
            timestamp_end_ns=max(timestamps),
            row_count=len(records),
            content_hash=content_hash_for_records(records),
            secret_free=True,
            paid_payload_free=True,
            may_commit_payload=True,
            redistribution_allowed=True,
            suitability_labels=(
                SuitabilityLabel.ENGINEERING_FIXTURE,
                SuitabilityLabel.PHASE1_RESEARCH,
                SuitabilityLabel.NOT_FOR_LIVE_TRADING,
            ),
            record_type=record_type,
        )
