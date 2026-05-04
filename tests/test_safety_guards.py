from __future__ import annotations

from pathlib import Path

import pytest

from trident_lob.config import DataConfig, RunConfig, ValidationConfig
from trident_lob.validation import assert_phase1_safe_config

REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNED_PATHS = [
    REPO_ROOT / "src",
    REPO_ROOT / "configs",
    REPO_ROOT / "benchmarks",
]


def iter_scaffold_text() -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for base_path in SCANNED_PATHS:
        if not base_path.exists():
            continue
        for path in base_path.rglob("*"):
            if path.is_file() and path.suffix in {
                ".py",
                ".toml",
                ".yaml",
                ".yml",
                ".md",
            }:
                files.append((path, path.read_text(encoding="utf-8")))
    return files


def test_config_rejects_paid_payloads() -> None:
    with pytest.raises(ValueError, match="paid data"):
        DataConfig(paid_payload_free=False)


def test_config_rejects_random_row_split() -> None:
    with pytest.raises(ValueError, match="Random row splits"):
        ValidationConfig(allow_random_row_split=True)


def test_phase1_guard_accepts_default_config() -> None:
    assert_phase1_safe_config(RunConfig.default())


def test_data_config_rejects_mutated_secret_flag() -> None:
    with pytest.raises(ValueError, match="secrets"):
        DataConfig(secret_free=False)


def test_scaffold_has_no_live_service_terms() -> None:
    prohibited_terms = (
        "al" + "paca",
        "bin" + "ance",
        "coin" + "base",
        "interactive" + "brokers",
        "kra" + "ken",
        "api" + "_key",
        "secret" + "_key",
        "order" + "_router",
        "order" + "_url",
    )
    hits: list[str] = []
    for path, text in iter_scaffold_text():
        lowered = text.lower()
        for term in prohibited_terms:
            if term in lowered:
                hits.append(f"{path.relative_to(REPO_ROOT)} contains {term}")
    assert hits == []
