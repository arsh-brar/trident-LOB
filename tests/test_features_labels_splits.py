from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from trident_lob.data import DataMode, QuoteRecord, RecordType, SyntheticFixtureAdapter
from trident_lob.data.fixtures import BASE_TS_NS, ONE_MINUTE_NS, ONE_SECOND_NS
from trident_lob.features import (
    FeatureFamily,
    FeatureQualityFlags,
    FeatureRow,
    LeakageReason,
    OfflineFeatureBuilder,
    build_leakage_report,
)
from trident_lob.labels import (
    ChronologicalSplitManifest,
    DirectionLabel,
    OfflineLabelBuilder,
    SplitWindow,
    build_chronological_split_manifest,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_feature_row_schema_rejects_future_availability() -> None:
    with pytest.raises(ValidationError, match="feature_available_at_max_ns"):
        FeatureRow(
            symbol="TEST",
            t_pred_ns=10,
            feature_available_at_max_ns=11,
            max_feature_lookback_ns=0,
            data_mode=DataMode.L1,
            quality_flags=FeatureQualityFlags(has_quotes=True),
            feature_families=(FeatureFamily.ORDINARY_MICROSTRUCTURE,),
        )


def test_completed_bar_is_eligible_only_after_close_and_availability() -> None:
    adapter = SyntheticFixtureAdapter()
    bars = [
        record
        for record in adapter.market_records()
        if record.record_type == RecordType.BAR
    ]
    builder = OfflineFeatureBuilder()

    at_close = builder.build_one(
        bars,
        t_pred_ns=BASE_TS_NS + ONE_MINUTE_NS,
        symbol="TEST",
        data_mode=DataMode.BARS,
    )
    after_provider_availability = builder.build_one(
        bars,
        t_pred_ns=BASE_TS_NS + ONE_MINUTE_NS + ONE_SECOND_NS,
        symbol="TEST",
        data_mode=DataMode.BARS,
    )

    assert not at_close.quality_flags.has_bars
    assert after_provider_availability.quality_flags.has_bars
    assert after_provider_availability.volume_300s == 1_000.0


def test_bars_only_degraded_mode_nulls_quote_dependent_features() -> None:
    adapter = SyntheticFixtureAdapter()
    row = OfflineFeatureBuilder().build_one(
        adapter.market_records(),
        t_pred_ns=BASE_TS_NS + ONE_MINUTE_NS + ONE_SECOND_NS,
        symbol="TEST",
        data_mode=DataMode.BARS,
    )

    assert row.quality_flags.bars_only_degraded
    assert row.spread_ticks is None
    assert row.OFI_60s is None
    assert "quote_dependent_features_unavailable" in row.unavailable_feature_reasons


def test_label_builder_keeps_future_outcomes_separate_from_features() -> None:
    adapter = SyntheticFixtureAdapter()
    records = adapter.market_records()
    base_quote = next(record for record in records if isinstance(record, QuoteRecord))
    t_pred_ns = BASE_TS_NS + 10 * ONE_SECOND_NS
    future_one_minute = base_quote.model_copy(
        update={
            "event_ts_ns": t_pred_ns + ONE_MINUTE_NS,
            "available_at_ns": t_pred_ns + ONE_MINUTE_NS + ONE_SECOND_NS,
            "sequence": 10,
            "bid_price": 100.1,
            "ask_price": 100.2,
        }
    )
    future_five_minutes = base_quote.model_copy(
        update={
            "event_ts_ns": t_pred_ns + 5 * ONE_MINUTE_NS,
            "available_at_ns": t_pred_ns + 5 * ONE_MINUTE_NS + ONE_SECOND_NS,
            "sequence": 11,
            "bid_price": 100.2,
            "ask_price": 100.3,
        }
    )
    records = [*records, future_one_minute, future_five_minutes]

    feature_row = OfflineFeatureBuilder().build_one(
        records,
        t_pred_ns=t_pred_ns,
        symbol="TEST",
    )
    labels = OfflineLabelBuilder(buffer_ticks=0.5).build(
        records,
        prediction_times_ns=(t_pred_ns,),
        symbol="TEST",
    )

    assert all(not key.startswith("y_") for key in feature_row.model_dump())
    assert {label.horizon_seconds for label in labels} == {60, 300}
    assert all(label.y_dir_cost_aware == DirectionLabel.UP for label in labels)
    assert all(label.label_available_at_min_ns is not None for label in labels)


def test_label_builder_records_missing_future_outcomes() -> None:
    adapter = SyntheticFixtureAdapter()
    t_pred_ns = BASE_TS_NS + 10 * ONE_SECOND_NS

    label = OfflineLabelBuilder().build_one(
        adapter.market_records(),
        symbol="TEST",
        t_pred_ns=t_pred_ns,
        horizon_seconds=300,
    )

    assert label.y_return_ticks is None
    assert label.null_reason.value == "missing_future_outcome"


def test_chronological_split_manifest_enforces_embargo() -> None:
    timestamps = [BASE_TS_NS + i * 10 * ONE_MINUTE_NS for i in range(12)]
    manifest = build_chronological_split_manifest(
        dataset_id="synthetic:tiny",
        split_id="split-001",
        symbol_universe=("TEST",),
        timestamps_ns=timestamps,
        embargo_ns=10 * ONE_MINUTE_NS,
        max_label_horizon_ns=5 * ONE_MINUTE_NS,
        max_feature_lookback_ns=5 * ONE_MINUTE_NS,
        created_at_ns=BASE_TS_NS,
    )

    assert manifest.train.end_ns + manifest.embargo_ns <= manifest.validation.start_ns
    assert manifest.validation.end_ns + manifest.embargo_ns <= manifest.test.start_ns


def test_split_manifest_rejects_too_short_embargo() -> None:
    with pytest.raises(ValidationError, match="embargo"):
        ChronologicalSplitManifest(
            dataset_id="synthetic:tiny",
            split_id="bad-split",
            symbol_universe=("TEST",),
            train=SplitWindow(start_ns=0, end_ns=100),
            validation=SplitWindow(start_ns=200, end_ns=300),
            test=SplitWindow(start_ns=400, end_ns=500),
            embargo_ns=50,
            max_label_horizon_ns=100,
            max_feature_lookback_ns=100,
            created_at_ns=1,
        )


def test_leakage_report_fails_closed_for_mutated_future_feature() -> None:
    adapter = SyntheticFixtureAdapter()
    row = OfflineFeatureBuilder().build_one(
        adapter.market_records(),
        t_pred_ns=BASE_TS_NS + 10 * ONE_SECOND_NS,
        symbol="TEST",
    )
    leaked_row = row.model_copy(
        update={"feature_available_at_max_ns": row.t_pred_ns + ONE_SECOND_NS}
    )
    report = build_leakage_report([leaked_row])

    assert report.status.value == "fail"
    assert report.findings[0].reason == LeakageReason.FEATURE_AVAILABLE_AFTER_PREDICTION


def test_leakage_report_rejects_future_news_availability() -> None:
    adapter = SyntheticFixtureAdapter()
    report = build_leakage_report(
        [],
        exogenous_records=adapter.exogenous_records(),
        t_pred_ns=BASE_TS_NS + 7 * ONE_SECOND_NS,
    )
    reasons = {finding.reason for finding in report.findings}

    assert report.status.value == "fail"
    assert LeakageReason.NEWS_AVAILABLE_AFTER_PREDICTION in reasons
    assert LeakageReason.NEWS_PUBLISHED_AFTER_PREDICTION in reasons


def test_no_random_row_split_helper_is_exposed() -> None:
    import trident_lob.labels as labels

    assert not hasattr(labels, "build_random_row_split")
