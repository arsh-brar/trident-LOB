"""Protocol boundaries for swappable Phase 1 components."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Protocol

from trident_lob.config import RunConfig
from trident_lob.contracts.types import (
    ArtifactRef,
    DataBatch,
    DataSliceSpec,
    FeatureFrame,
    InterfaceFrame,
    LabelFrame,
    ModelArtifact,
    PredictionFrame,
    RiskDecision,
    RunManifest,
    TurbulenceFrame,
    ValidationReport,
)
from trident_lob.data.schemas import CanonicalDataRecord, EventBatchManifest, RecordType


class DataAdapter(Protocol):
    def describe_available_slices(self) -> list[DataSliceSpec]: ...

    def load(self, request: DataSliceSpec) -> DataBatch: ...


class EventStore(Protocol):
    def write(self, batch: DataBatch, manifest: RunManifest) -> ArtifactRef: ...

    def scan(self, query: DataSliceSpec) -> Iterable[Mapping[str, object]]: ...


class OfflineEventStore(Protocol):
    def register_batch(
        self,
        records: Sequence[CanonicalDataRecord],
        manifest: EventBatchManifest,
    ) -> ArtifactRef: ...

    def query_events(
        self,
        *,
        record_type: RecordType | None = None,
        symbol: str | None = None,
        start_ns: int | None = None,
        end_ns: int | None = None,
    ) -> object: ...


class FeatureBuilder(Protocol):
    def build(
        self, records: Iterable[Mapping[str, object]], clock_ns: int
    ) -> FeatureFrame: ...


class LabelBuilder(Protocol):
    def build(
        self,
        records: Iterable[Mapping[str, object]],
        horizons_ns: tuple[int, ...],
        costs: Mapping[str, float],
    ) -> LabelFrame: ...


class TurbulenceEstimator(Protocol):
    def transform(self, features: FeatureFrame) -> TurbulenceFrame: ...


class PriceInterfaceEstimator(Protocol):
    def transform(self, features: FeatureFrame) -> InterfaceFrame: ...


class PredictionModel(Protocol):
    def fit(
        self,
        train_frame: FeatureFrame,
        validation_frame: FeatureFrame,
        config: RunConfig,
    ) -> ModelArtifact: ...

    def predict(self, feature_frame: FeatureFrame) -> PredictionFrame: ...


class Backtester(Protocol):
    def run(
        self,
        predictions: PredictionFrame,
        market_events: Iterable[Mapping[str, object]],
        config: RunConfig,
    ) -> ValidationReport: ...


class RiskManager(Protocol):
    def evaluate(
        self,
        intent: Mapping[str, object],
        state: Mapping[str, object],
    ) -> RiskDecision: ...


class ReportGenerator(Protocol):
    def render(self, run_manifest: RunManifest) -> ArtifactRef: ...
