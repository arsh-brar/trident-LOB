# Stack Validation Plan

## Environment Validation

Verify the Phase 1 environment is native Apple Silicon arm64, Python 3.12, and CPU-only. This follows the repository rule for Mac Apple Silicon M3 CPU-only execution and Apple's guidance to target native Apple Silicon binaries [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [Apple Silicon documentation](https://developer.apple.com/documentation/apple-silicon), [Rosetta support note](https://support.apple.com/en-us/102527).

Required checks:

```text
python -c "import platform; print(platform.machine())"
python -c "import sys; print(sys.version)"
python -c "import torch; print(torch.cuda.is_available())"  # only if torch is installed in optional group
```

Accept only `arm64` for the machine check and no required GPU dependency for core Phase 1 runs [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [PyTorch local install](https://docs.pytorch.org/get-started/locally/), [JAX install](https://docs.jax.dev/en/latest/installation.html).

## Dependency Validation

Require a reproducible project lock file and separate dependency groups for core, dev, optional boosted-tree, optional deep-learning, notebooks, and docs. This aligns with documented project-based workflows and dependency groups [uv PyPI](https://pypi.org/pypi/uv), [Python dependency groups](https://packaging.python.org/en/latest/specifications/dependency-groups/), [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install).

Run import smoke tests for the core stack: Polars, pandas, NumPy, SciPy, scikit-learn, DuckDB, Pydantic, OmegaConf, MLflow, pytest, Ruff, mypy, Typer, and Click. These imports validate the selected documented packages without exercising live trading or networked services [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/), [pandas user guide](https://pandas.pydata.org/docs/user_guide/), [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview), [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/), [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/), [Typer PyPI](https://pypi.org/pypi/typer/).

## Data Validation

Validate that every persisted event, feature, label, prediction, and report artifact has a manifest with symbol, venue if available, timestamp range, schema version, source identifier, and split identifier. This supports no-future-data checks and traceability for the TRIDENT event-stream model [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/).

Validate Parquet round trips through Polars, DuckDB, and pandas compatibility paths. This is required because Parquet is the recommended canonical format and the stack intentionally mixes Polars, DuckDB, pandas, and Arrow-compatible tools [Apache Parquet overview](https://parquet.apache.org/docs/overview/), [Polars Parquet](https://docs.pola.rs/user-guide/io/parquet/), [DuckDB data ingestion](https://duckdb.org/docs/stable/clients/python/data_ingestion), [pandas read_parquet](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html).

## Leakage Validation

Require tests that fail when a feature row uses an event timestamp greater than the prediction timestamp or label cutoff. This directly enforces the project rule against future data [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html).

Require split manifests that define train, validation, and test windows by time, not random row shuffling, because limit order book events and news forcing are time-indexed processes [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [scikit-learn install](https://scikit-learn.org/stable/install.html).

## Numerical Validation

Require deterministic numerical smoke tests for turbulence fields, nonnegative liquidity constraints, execution capping by available depth, and finite `k`, `epsilon`, and fragility values. These checks map to the TRIDENT liquidity equations and turbulence closure [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install), [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html).

Use pytest approximate comparisons for floating point tolerances and small synthetic fixtures before real market data tests. This keeps Phase 1 simple and auditable [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

## Model Validation

Require scikit-learn baseline models before XGBoost or other complex models. Any optional boosted-tree result must be compared against naive, linear, and tree baselines on the same out-of-sample split with transaction costs included before any research conclusion is written [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [scikit-learn install](https://scikit-learn.org/stable/install.html), [XGBoost install](https://xgboost.readthedocs.io/en/release_3.0.0/install.html).

Track every run with MLflow local metadata: code version if available, config hash, split manifest, data manifest, parameters, metrics, and artifacts. MLflow documents run tracking, metrics, parameters, artifacts, datasets, and a local UI [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

## Tooling Gates

Require `ruff check`, `ruff format --check`, `mypy`, and `pytest` as local quality gates before merging Phase 1 implementation changes. Ruff documents lint and format commands, mypy documents static type checking, and pytest documents discovery and assertion workflows [Ruff linter](https://docs.astral.sh/ruff/linter/), [Ruff formatter](https://docs.astral.sh/ruff/formatter/), [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html), [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html).

Use pre-commit to run the fast checks locally and keep heavier numerical tests available as explicit commands. pre-commit documents repository hooks and manual `pre-commit run --all-files` execution [pre-commit docs](https://pre-commit.com/), [Ruff docs](https://docs.astral.sh/ruff/), [mypy docs](https://mypy.readthedocs.io/).

## Stop Conditions

Stop a Phase 1 run if it requires live credentials, broker access, live order submission, future-data features, cloud-only experiment tracking, non-native architecture, GPU-only acceleration, or unvalidated profitability claims. These conditions come directly from the project rules and model scope note [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [W&B offline support](https://docs.wandb.ai/models/support/run_wandb_offline/).

