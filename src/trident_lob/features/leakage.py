"""Fail-closed leakage helpers for features and exogenous records."""

from __future__ import annotations

from collections.abc import Sequence

from trident_lob.data.schemas import (
    CalendarRecord,
    CanonicalDataRecord,
    NewsEventRecord,
)
from trident_lob.features.schemas import (
    FeatureRow,
    LeakageFinding,
    LeakageReason,
    LeakageReport,
    LeakageStatus,
)
from trident_lob.labels.schemas import ChronologicalSplitManifest


def build_leakage_report(
    feature_rows: Sequence[FeatureRow],
    *,
    report_id: str = "phase1c_leakage_report",
    split_manifest: ChronologicalSplitManifest | None = None,
    exogenous_records: Sequence[CanonicalDataRecord] = (),
    t_pred_ns: int | None = None,
) -> LeakageReport:
    findings: list[LeakageFinding] = []
    for row in feature_rows:
        if row.feature_available_at_max_ns > row.t_pred_ns:
            findings.append(
                LeakageFinding(
                    reason=LeakageReason.FEATURE_AVAILABLE_AFTER_PREDICTION,
                    symbol=row.symbol,
                    t_pred_ns=row.t_pred_ns,
                    detail="feature_available_at_max_ns exceeds t_pred_ns",
                )
            )
    if split_manifest is not None:
        minimum_embargo = (
            split_manifest.max_label_horizon_ns + split_manifest.max_feature_lookback_ns
        )
        if split_manifest.embargo_ns < minimum_embargo:
            findings.append(
                LeakageFinding(
                    reason=LeakageReason.SPLIT_EMBARGO_TOO_SHORT,
                    detail="split embargo is shorter than horizon plus lookback",
                )
            )
    if t_pred_ns is not None:
        findings.extend(_exogenous_findings(exogenous_records, t_pred_ns=t_pred_ns))
    max_available = (
        max(row.feature_available_at_max_ns for row in feature_rows)
        if feature_rows
        else None
    )
    return LeakageReport(
        report_id=report_id,
        status=LeakageStatus.FAIL if findings else LeakageStatus.PASS,
        checked_row_count=len(feature_rows),
        max_feature_available_at_ns=max_available,
        findings=tuple(findings),
    )


def _exogenous_findings(
    records: Sequence[CanonicalDataRecord],
    *,
    t_pred_ns: int,
) -> list[LeakageFinding]:
    findings: list[LeakageFinding] = []
    for record in records:
        if isinstance(record, NewsEventRecord):
            if record.available_at_ns > t_pred_ns:
                findings.append(
                    LeakageFinding(
                        reason=LeakageReason.NEWS_AVAILABLE_AFTER_PREDICTION,
                        symbol=record.symbol,
                        t_pred_ns=t_pred_ns,
                        detail=(
                            f"news event {record.event_id} unavailable at prediction"
                        ),
                    )
                )
            if record.source_published_at_ns > t_pred_ns:
                findings.append(
                    LeakageFinding(
                        reason=LeakageReason.NEWS_PUBLISHED_AFTER_PREDICTION,
                        symbol=record.symbol,
                        t_pred_ns=t_pred_ns,
                        detail=(
                            f"news event {record.event_id} published after prediction"
                        ),
                    )
                )
        if (
            isinstance(record, CalendarRecord)
            and record.actual_available_at_ns is not None
            and record.actual_available_at_ns > t_pred_ns
        ):
            findings.append(
                LeakageFinding(
                    reason=LeakageReason.CALENDAR_ACTUAL_NOT_AVAILABLE,
                    symbol=record.symbol,
                    t_pred_ns=t_pred_ns,
                    detail=f"calendar actual {record.calendar_id} unavailable",
                )
            )
    return findings
