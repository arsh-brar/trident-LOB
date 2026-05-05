"""Chronological split manifest builder."""

from __future__ import annotations

from collections.abc import Sequence

from trident_lob.labels.schemas import ChronologicalSplitManifest, SplitWindow


def build_chronological_split_manifest(
    *,
    dataset_id: str,
    split_id: str,
    symbol_universe: Sequence[str],
    timestamps_ns: Sequence[int],
    embargo_ns: int,
    max_label_horizon_ns: int,
    max_feature_lookback_ns: int,
    created_at_ns: int,
    held_out_symbols: Sequence[str] = (),
) -> ChronologicalSplitManifest:
    timestamps = sorted(set(timestamps_ns))
    if len(timestamps) < 5:
        raise ValueError("at least five distinct timestamps are required.")
    train_stop_index = max(0, int(len(timestamps) * 0.6) - 1)
    train_start = timestamps[0]
    train_end = timestamps[train_stop_index]
    validation_candidates = [
        value for value in timestamps if value >= train_end + embargo_ns
    ]
    if len(validation_candidates) < 2:
        raise ValueError("not enough timestamps after train embargo.")
    validation_start = validation_candidates[0]
    validation_stop_index = max(0, int(len(validation_candidates) * 0.5) - 1)
    validation_end = validation_candidates[validation_stop_index]
    test_candidates = [
        value for value in timestamps if value >= validation_end + embargo_ns
    ]
    if not test_candidates:
        raise ValueError("not enough timestamps after validation embargo.")
    return ChronologicalSplitManifest(
        dataset_id=dataset_id,
        split_id=split_id,
        symbol_universe=tuple(symbol_universe),
        train=SplitWindow(start_ns=train_start, end_ns=train_end),
        validation=SplitWindow(start_ns=validation_start, end_ns=validation_end),
        test=SplitWindow(start_ns=test_candidates[0], end_ns=timestamps[-1]),
        embargo_ns=embargo_ns,
        max_label_horizon_ns=max_label_horizon_ns,
        max_feature_lookback_ns=max_feature_lookback_ns,
        held_out_symbols=tuple(held_out_symbols),
        created_at_ns=created_at_ns,
    )
