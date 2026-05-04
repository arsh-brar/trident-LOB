"""Immutable local Parquet-oriented event-store skeleton."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

import polars as pl

from trident_lob.contracts.types import ArtifactRef
from trident_lob.data.schemas import (
    CanonicalDataRecord,
    EventBatchManifest,
    RecordType,
    canonical_record_to_row,
)
from trident_lob.validation.data import validate_event_batch


class EventStoreError(ValueError):
    """Raised when local event-store invariants are violated."""


class LocalParquetEventStore:
    """Append-only local store for validated offline event batches."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def register_batch(
        self,
        records: Sequence[CanonicalDataRecord],
        manifest: EventBatchManifest,
    ) -> ArtifactRef:
        validate_event_batch(records, manifest)
        batch_dir = self._batch_dir(manifest)
        data_path = batch_dir / "records.parquet"
        manifest_path = batch_dir / "manifest.json"
        if batch_dir.exists():
            raise EventStoreError(
                f"event batch already registered: {manifest.batch_id}"
            )

        batch_dir.mkdir(parents=True, exist_ok=False)
        rows = [canonical_record_to_row(record) for record in records]
        pl.DataFrame(rows).write_parquet(data_path)
        stored_manifest = manifest.model_copy(update={"storage_uri": str(data_path)})
        manifest_path.write_text(
            json.dumps(
                stored_manifest.model_dump(mode="json"), indent=2, sort_keys=True
            ),
            encoding="utf-8",
        )
        return ArtifactRef(
            artifact_id=manifest.batch_id,
            uri=str(data_path),
            role=f"event_batch:{manifest.record_type.value}",
            content_hash=manifest.content_hash,
        )

    def query_events(
        self,
        *,
        record_type: RecordType | None = None,
        symbol: str | None = None,
        start_ns: int | None = None,
        end_ns: int | None = None,
    ) -> pl.DataFrame:
        paths = sorted((self.root / "events").glob("*/*/*/*/records.parquet"))
        if record_type is not None:
            paths = [path for path in paths if path.parts[-5] == record_type.value]
        if not paths:
            return pl.DataFrame()

        frames = [pl.read_parquet(path) for path in paths]
        frame = pl.concat(frames, how="diagonal_relaxed")
        if symbol is not None and "symbol" in frame.columns:
            frame = frame.filter(pl.col("symbol") == symbol)
        if start_ns is not None and "event_ts_ns" in frame.columns:
            frame = frame.filter(pl.col("event_ts_ns") >= start_ns)
        if end_ns is not None and "event_ts_ns" in frame.columns:
            frame = frame.filter(pl.col("event_ts_ns") <= end_ns)
        if "event_ts_ns" in frame.columns:
            frame = frame.sort("event_ts_ns")
        return frame

    def _batch_dir(self, manifest: EventBatchManifest) -> Path:
        return (
            self.root
            / "events"
            / manifest.record_type.value
            / manifest.provider
            / manifest.dataset
            / manifest.batch_id
        )
