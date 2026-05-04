"""Data validation guards for Phase 1 offline records and manifests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from trident_lob.data.schemas import (
    CanonicalDataRecord,
    DatasetManifest,
    EventBatchManifest,
    LicenseClass,
    QuoteRecord,
)
from trident_lob.validation.gates import GuardViolation

SECRET_MARKERS = (
    "secret",
    "credential",
    "token",
    "password",
    "bearer ",
    "private key",
)


def assert_records_available_by(
    records: Sequence[CanonicalDataRecord],
    decision_ts_ns: int,
) -> None:
    for record in records:
        if record.available_at_ns > decision_ts_ns:
            raise GuardViolation(
                f"{record.record_type} record is unavailable at decision time."
            )


def assert_monotone_event_time(records: Sequence[CanonicalDataRecord]) -> None:
    previous: int | None = None
    for record in records:
        if previous is not None and record.event_ts_ns < previous:
            raise GuardViolation("records are not ordered by event_ts_ns.")
        previous = record.event_ts_ns


def assert_no_crossed_quotes(records: Sequence[CanonicalDataRecord]) -> None:
    for record in records:
        if isinstance(record, QuoteRecord) and record.bid_price >= record.ask_price:
            raise GuardViolation("crossed or locked quote was accepted.")


def assert_manifest_commit_safe(
    manifest: DatasetManifest | EventBatchManifest,
) -> None:
    if manifest.license_class == LicenseClass.PAID and manifest.may_commit_payload:
        raise GuardViolation("paid payloads may not be committed.")
    if not manifest.secret_free:
        raise GuardViolation("manifest is not secret-free.")
    if not manifest.paid_payload_free:
        raise GuardViolation("manifest is not paid-payload-free.")
    if manifest.may_commit_payload and not manifest.redistribution_allowed:
        raise GuardViolation("committed payloads require redistribution allowance.")


def assert_secret_free_mapping(values: Mapping[str, Any]) -> None:
    hits: list[str] = []
    for key, value in values.items():
        value_text = str(value).lower()
        if any(marker in value_text for marker in SECRET_MARKERS):
            hits.append(str(key))
    if hits:
        raise GuardViolation(f"possible secret-bearing fields: {', '.join(hits)}")


def validate_event_batch(
    records: Sequence[CanonicalDataRecord],
    manifest: EventBatchManifest,
) -> None:
    if len(records) != manifest.row_count:
        raise GuardViolation("manifest row_count does not match records.")
    if any(record.record_type != manifest.record_type for record in records):
        raise GuardViolation("manifest record_type does not match records.")
    if records:
        min_ts = min(record.event_ts_ns for record in records)
        max_ts = max(record.event_ts_ns for record in records)
        if manifest.timestamp_start_ns != min_ts or manifest.timestamp_end_ns != max_ts:
            raise GuardViolation("manifest timestamp range does not match records.")
    assert_no_crossed_quotes(records)
    assert_manifest_commit_safe(manifest)
