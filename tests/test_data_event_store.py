from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from trident_lob.data import (
    DataMode,
    DelayClass,
    EventBatchManifest,
    LicenseClass,
    QuoteRecord,
    RecordType,
    SyntheticFixtureAdapter,
)
from trident_lob.events import EventStoreError, LocalParquetEventStore
from trident_lob.validation import (
    GuardViolation,
    assert_manifest_commit_safe,
    assert_monotone_event_time,
    assert_records_available_by,
)


def test_synthetic_fixture_builds_all_required_record_types() -> None:
    adapter = SyntheticFixtureAdapter()
    record_types = {record.record_type for record in adapter.all_records()}

    assert record_types == {
        RecordType.BAR,
        RecordType.QUOTE,
        RecordType.TRADE,
        RecordType.DEPTH,
        RecordType.NEWS,
        RecordType.CALENDAR,
        RecordType.CORPORATE_ACTION,
    }


def test_quote_schema_rejects_crossed_quote() -> None:
    adapter = SyntheticFixtureAdapter()
    good_quote = next(
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.QUOTE
    )
    quote_values = good_quote.model_dump()
    quote_values["bid_price"] = 101.0
    quote_values["ask_price"] = 100.0

    with pytest.raises(ValidationError, match="bid_price"):
        QuoteRecord.model_validate(quote_values)


def test_trade_schema_rejects_negative_size() -> None:
    with pytest.raises(ValidationError, match="size"):
        QuoteRecord(
            provider="synthetic",
            dataset="tiny_phase1_fixture",
            symbol="TEST",
            venue="XTEST",
            feed="synthetic",
            event_ts_ns=1,
            available_at_ns=2,
            source="synthetic_fixture",
            bid_price=100.0,
            bid_size=-1.0,
            ask_price=100.1,
            ask_size=1.0,
        )


def test_manifest_rejects_paid_payload_commit() -> None:
    with pytest.raises(ValidationError, match="paid payloads"):
        EventBatchManifest(
            dataset_id="paid:test",
            batch_id="batch",
            provider="paid-provider",
            dataset="restricted",
            source="restricted",
            source_url="file://restricted",
            license_class=LicenseClass.PAID,
            delay_class=DelayClass.HISTORICAL_ARCHIVE,
            data_mode=DataMode.BARS,
            timestamp_start_ns=1,
            timestamp_end_ns=2,
            row_count=1,
            content_hash="abc",
            secret_free=True,
            paid_payload_free=True,
            may_commit_payload=True,
            redistribution_allowed=True,
            record_type=RecordType.BAR,
        )


def test_manifest_rejects_unknown_license_class() -> None:
    with pytest.raises(ValidationError, match="license_class"):
        EventBatchManifest.model_validate(
            {
                "dataset_id": "unknown:test",
                "batch_id": "batch",
                "provider": "unknown",
                "dataset": "unknown",
                "source": "unknown",
                "source_url": "file://unknown",
                "license_class": "mystery",
                "delay_class": "synthetic",
                "data_mode": "synthetic",
                "timestamp_start_ns": 1,
                "timestamp_end_ns": 2,
                "row_count": 1,
                "content_hash": "abc",
                "record_type": "bar",
            }
        )


def test_availability_guard_rejects_unavailable_record() -> None:
    adapter = SyntheticFixtureAdapter()
    records = adapter.market_records()
    with pytest.raises(GuardViolation, match="unavailable"):
        assert_records_available_by(records, decision_ts_ns=1)


def test_monotone_event_guard_rejects_out_of_order_records() -> None:
    adapter = SyntheticFixtureAdapter()
    records = list(reversed(adapter.market_records()))
    with pytest.raises(GuardViolation, match="ordered"):
        assert_monotone_event_time(records)


def test_manifest_commit_guard_accepts_synthetic_manifest() -> None:
    adapter = SyntheticFixtureAdapter()
    records = [
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.QUOTE
    ]
    manifest = adapter.manifest_for(records, record_type=RecordType.QUOTE)

    assert_manifest_commit_safe(manifest)


def test_local_parquet_event_store_round_trip(tmp_path: Path) -> None:
    adapter = SyntheticFixtureAdapter()
    records = [
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.QUOTE
    ]
    manifest = adapter.manifest_for(records, record_type=RecordType.QUOTE)
    store = LocalParquetEventStore(tmp_path)

    artifact = store.register_batch(records, manifest)
    result = store.query_events(record_type=RecordType.QUOTE, symbol="TEST")

    assert artifact.content_hash == manifest.content_hash
    assert result.height == 1
    assert result.select("symbol").item() == "TEST"
    assert result.select("bid_price").item() == 100.0


def test_event_store_rejects_mismatched_manifest_hash(tmp_path: Path) -> None:
    adapter = SyntheticFixtureAdapter()
    records = [
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.QUOTE
    ]
    manifest = adapter.manifest_for(records, record_type=RecordType.QUOTE).model_copy(
        update={"content_hash": "not-the-record-hash"}
    )
    store = LocalParquetEventStore(tmp_path)

    with pytest.raises(GuardViolation, match="content_hash"):
        store.register_batch(records, manifest)


def test_event_store_rejects_out_of_order_batch(tmp_path: Path) -> None:
    adapter = SyntheticFixtureAdapter()
    first_quote = next(
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.QUOTE
    )
    later_quote = first_quote.model_copy(
        update={
            "event_ts_ns": first_quote.event_ts_ns + 10,
            "available_at_ns": first_quote.available_at_ns + 10,
            "sequence": 2,
        }
    )
    records = [later_quote, first_quote]
    manifest = adapter.manifest_for(records, record_type=RecordType.QUOTE)
    store = LocalParquetEventStore(tmp_path)

    with pytest.raises(GuardViolation, match="ordered"):
        store.register_batch(records, manifest)


def test_event_store_registration_is_immutable(tmp_path: Path) -> None:
    adapter = SyntheticFixtureAdapter()
    records = [
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.QUOTE
    ]
    manifest = adapter.manifest_for(records, record_type=RecordType.QUOTE)
    store = LocalParquetEventStore(tmp_path)

    store.register_batch(records, manifest)
    with pytest.raises(EventStoreError, match="already registered"):
        store.register_batch(records, manifest)
