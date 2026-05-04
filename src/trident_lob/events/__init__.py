"""Local offline event-store interfaces."""

from trident_lob.events.store import EventStoreError, LocalParquetEventStore

__all__ = ["EventStoreError", "LocalParquetEventStore"]
