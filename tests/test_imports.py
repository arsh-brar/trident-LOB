from __future__ import annotations

import importlib.metadata

import trident_lob
from trident_lob.cli.app import main
from trident_lob.config import RunConfig


def test_package_imports() -> None:
    assert trident_lob.__version__ == "0.1.0"


def test_project_metadata_name_when_installed() -> None:
    try:
        metadata_version = importlib.metadata.version("trident-lob")
    except importlib.metadata.PackageNotFoundError:
        metadata_version = trident_lob.__version__
    assert metadata_version == trident_lob.__version__


def test_cli_placeholder_runs_without_routing() -> None:
    assert main(["validate"]) == 0


def test_default_config_constructs() -> None:
    config = RunConfig.default()
    assert config.mode.phase == "phase_1_research"
    assert config.mode.execution_mode == "offline_research"
    assert config.data.secret_free is True
    assert config.data.paid_payload_free is True
