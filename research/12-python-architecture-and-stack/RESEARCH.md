# Python Architecture And Stack Research

## Scope

This Phase 0 note recommends a Python stack for TRIDENT-LOB Phase 1 research on a local Mac with Apple Silicon M3. It does not introduce production code, trading code, broker integration, or claims of profitability. The model document requires a modular Python research architecture for a turbulent reaction-diffusion limit order book model with swappable data, feature, estimator, model, backtest, paper-trading, risk, and report components [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md). The repository rules require CPU-only Phase 1 execution on Apple Silicon M3, no future data in features, no live trading, simple baselines before complex models, citations for recommendations, and no profitability claims without out-of-sample transaction-cost-adjusted evidence [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

The expected Phase 1 environment should therefore optimize for reproducible local CPU execution, deterministic research runs, easy replacement of modules, and well documented interfaces rather than cloud scale or low latency deployment [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [Apple Silicon documentation](https://developer.apple.com/documentation/apple-silicon).

## Platform Findings

Use native arm64 Python on macOS, not an Intel translated environment, because Apple recommends native Apple Silicon binaries where possible and notes that Rosetta translation is a compatibility bridge rather than the target state [Apple Silicon documentation](https://developer.apple.com/documentation/apple-silicon), [Rosetta support note](https://support.apple.com/en-us/102527), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Use Python 3.12 as the Phase 1 target unless repository-wide coordination later chooses otherwise. It is new enough for current scientific tooling and within PyTorch's current macOS recommendation window while avoiding the newest interpreter edge for compiled research packages [PyTorch local install](https://docs.pytorch.org/get-started/locally/), [scikit-learn install](https://scikit-learn.org/stable/install.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Use a project-level dependency manager and lock file. `uv` is a good default because NumPy and SciPy both document project-based workflows with `uv`, and `uv` documents managed project dependencies, environments, lockfiles, and `uv run` execution [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install), [uv PyPI](https://pypi.org/pypi/uv), [Python dependency groups](https://packaging.python.org/en/latest/specifications/dependency-groups/).

## DataFrame And Query Layer

Recommend Polars as the primary DataFrame engine for feature construction and event-window transformations. Polars recommends its lazy API for most cases because deferred execution enables optimizer benefits, and Polars can scan Parquet lazily [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/), [Polars Parquet](https://docs.pola.rs/user-guide/io/parquet/), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Keep pandas as an interoperability dependency rather than the main compute surface. pandas remains the common exchange format across scikit-learn and many finance data tools, and pandas documents Parquet and PyArrow support, but the main pipeline should avoid pandas-only assumptions [pandas user guide](https://pandas.pydata.org/docs/user_guide/), [pandas read_parquet](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html), [scikit-learn install](https://scikit-learn.org/stable/install.html).

Recommend DuckDB as the local analytical event-store/query layer over Parquet. DuckDB's Python API can query Parquet directly, ingest pandas, Polars, and Arrow objects, and return results to Polars, pandas, Arrow, NumPy, and PyTorch formats [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview), [DuckDB data ingestion](https://duckdb.org/docs/stable/clients/python/data_ingestion), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Recommend Parquet as the canonical research data file format with PyArrow-compatible schemas. Apache Parquet is column-oriented and designed for efficient storage and retrieval, DuckDB and Polars both support direct Parquet reads, and pandas supports Parquet through PyArrow by default when available [Apache Parquet overview](https://parquet.apache.org/docs/overview/), [DuckDB data ingestion](https://duckdb.org/docs/stable/clients/python/data_ingestion), [Polars Parquet](https://docs.pola.rs/user-guide/io/parquet/), [pandas read_parquet](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html).

## Numerical And ML Layer

Recommend NumPy as the base array ABI and SciPy for numerical estimation, optimization, interpolation, sparse operations, and scientific routines. Both projects document standard installation paths and are the stable foundation for Python scientific computing on local machines [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Do not make JAX a Phase 1 core dependency. JAX supports CPU-only macOS Apple ARM wheels, but its Apple GPU support is experimental and not needed for a CPU-only local research baseline [JAX install](https://docs.jax.dev/en/latest/installation.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Do not make PyTorch a Phase 1 core dependency. PyTorch supports macOS and CPU installation, and its MPS backend targets Apple GPU acceleration, but Phase 1 explicitly requires CPU-only operation and simple baselines first [PyTorch local install](https://docs.pytorch.org/get-started/locally/), [PyTorch MPS backend](https://docs.pytorch.org/docs/2.9/notes/mps.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Recommend scikit-learn as the baseline modeling framework. scikit-learn provides stable installation paths on macOS, integrates with NumPy and SciPy, and supports simple baselines before complex models [scikit-learn install](https://scikit-learn.org/stable/install.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Recommend XGBoost as the optional gradient boosting dependency if boosted trees are needed after baseline gates pass. XGBoost documents prebuilt wheels for macOS including Apple Silicon and a minimal CPU-only installation path, while LightGBM on macOS has historically required OpenMP runtime setup for Apple Clang builds [XGBoost install](https://xgboost.readthedocs.io/en/release_3.0.0/install.html), [LightGBM install](https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html), [LightGBM PyPI](https://pypi.org/project/lightgbm/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

## Config, Validation, And Tracking

Recommend Pydantic v2 for runtime schema validation of configs, event manifests, data contracts, and model parameter objects. Pydantic documents strict mode at the field, model, and validation-call level, which is useful for preventing accidental coercion in research data contracts [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Recommend OmegaConf for Phase 1 config composition, with Hydra deferred until command-line multirun sweeps become necessary. OmegaConf supports structured configs with runtime type safety and static type checker support; Hydra adds powerful composition and override workflows that are useful later but heavier for early modular baselines [OmegaConf structured configs](https://omegaconf.readthedocs.io/en/latest/structured_config.html), [Hydra composition](https://hydra.cc/docs/1.2/tutorials/basic/your_first_app/composition/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Recommend MLflow local tracking over Weights and Biases for Phase 1. MLflow Tracking records runs, metrics, parameters, artifacts, datasets, and local UI results, while W&B can run offline but is still oriented around later cloud sync and account workflows [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/), [W&B offline](https://docs.wandb.ai/models/ref/cli/wandb-offline), [W&B offline support](https://docs.wandb.ai/models/support/run_wandb_offline/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

## Developer Tooling

Recommend pytest for tests because it supports concise assertions, standard discovery, fixtures such as `tmp_path`, and floating point comparison helpers useful for numerical research validation [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Recommend Ruff for linting and formatting because it provides both `ruff check` and `ruff format`, is documented as a fast replacement for several Python linting and formatting tools, and supports `pyproject.toml` configuration [Ruff docs](https://docs.astral.sh/ruff/), [Ruff linter](https://docs.astral.sh/ruff/linter/), [Ruff formatter](https://docs.astral.sh/ruff/formatter/).

Recommend mypy for gradual static type checking of swappable component interfaces. mypy documents static checking without running code and can be introduced gradually to prevent regressions in protocol contracts [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html), [mypy docs](https://mypy.readthedocs.io/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Recommend pre-commit for local quality gates before commits. pre-commit documents a repository-level `.pre-commit-config.yaml`, installable hooks, and `pre-commit run --all-files` for manual verification [pre-commit docs](https://pre-commit.com/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Recommend Typer for the research CLI, backed by Click. Typer is based on Python type hints, supports command trees, automatic help, and completion; Click is the stable composable CLI toolkit underneath and documents arbitrary nesting plus generated help pages [Typer PyPI](https://pypi.org/pypi/typer/), [Click docs](https://click.palletsprojects.com/en/stable/why/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

