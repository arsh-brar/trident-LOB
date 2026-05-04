# Python Stack Options

## Decision Criteria

Phase 1 choices should be native on Apple Silicon M3, CPU-only, reproducible, modular, and friendly to out-of-sample validation without future-data leakage [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [Apple Silicon documentation](https://developer.apple.com/documentation/apple-silicon).

## DataFrame Engine

| Option | Fit | Recommendation |
| --- | --- | --- |
| Polars | Strong for lazy scans, vectorized transforms, and Parquet-heavy research workflows [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/), [Polars Parquet](https://docs.pola.rs/user-guide/io/parquet/) | Use as primary feature and event transform engine, because TRIDENT needs efficient event-window and price-grid operations on local CPU [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md). |
| pandas | Strong ecosystem compatibility and broad user familiarity [pandas user guide](https://pandas.pydata.org/docs/user_guide/), [pandas read_parquet](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html) | Keep as compatibility layer for package APIs and reports, not as the default compute engine, because Phase 1 should avoid pandas-only pipeline assumptions [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |

## Arrays, Numerical Kernels, And ML Frameworks

| Option | Fit | Recommendation |
| --- | --- | --- |
| NumPy | Base numerical array library with straightforward installation [NumPy install](https://numpy.org/install/) | Use as the core array representation at interfaces, because many scientific Python packages interoperate through NumPy [SciPy install](https://scipy.org/install). |
| SciPy | Scientific algorithms, optimization, sparse matrices, and numerical routines [SciPy install](https://scipy.org/install) | Use for turbulence and interface estimation routines where standard numerical methods are enough [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md). |
| JAX | CPU macOS Apple ARM wheels exist, but Apple GPU is experimental [JAX install](https://docs.jax.dev/en/latest/installation.html) | Do not use in Phase 1 core, because CPU-only simple baselines are the requirement and JIT complexity should wait for a proven numerical bottleneck [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| PyTorch | macOS install is supported, and MPS exists for Apple GPU acceleration [PyTorch local install](https://docs.pytorch.org/get-started/locally/), [PyTorch MPS backend](https://docs.pytorch.org/docs/2.9/notes/mps.html) | Do not use in Phase 1 core, because GPU acceleration is out of scope and deep learning should wait until simple baselines and validation gates are established [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |

## Model Baselines And Boosted Trees

| Option | Fit | Recommendation |
| --- | --- | --- |
| scikit-learn | Stable macOS installation, common baseline estimators, and NumPy/SciPy integration [scikit-learn install](https://scikit-learn.org/stable/install.html) | Use first for baselines, pipelines, calibration, and validation tooling [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| LightGBM | Fast gradient boosting, but macOS setup may involve OpenMP runtime or Homebrew packages [LightGBM install](https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html), [LightGBM PyPI](https://pypi.org/project/lightgbm/) | Keep optional and secondary, because Phase 1 should minimize non-Python system dependency friction on Mac M3 [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| XGBoost | Documents prebuilt Python wheels for macOS including Apple Silicon and a minimal CPU-only install path [XGBoost install](https://xgboost.readthedocs.io/en/release_3.0.0/install.html) | Prefer over LightGBM if boosted trees are needed after simple baselines pass validation, because it fits local CPU-only Apple Silicon more cleanly [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |

## Storage And Query

| Option | Fit | Recommendation |
| --- | --- | --- |
| Parquet | Column-oriented storage designed for efficient storage and retrieval [Apache Parquet overview](https://parquet.apache.org/docs/overview/) | Use as canonical file format for event slices, feature matrices, labels, and validation splits [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md). |
| DuckDB | Queries local Parquet directly and interoperates with Polars, pandas, Arrow, NumPy, and PyTorch outputs [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview), [DuckDB data ingestion](https://duckdb.org/docs/stable/clients/python/data_ingestion) | Use as local query and event-store engine for Phase 1, because it keeps research SQL close to files without a server [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |

## Config, Schemas, And Experiments

| Option | Fit | Recommendation |
| --- | --- | --- |
| Pydantic | Strict runtime validation for model and field values [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) | Use for external data contracts, run manifests, validated config objects, and artifact metadata [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md). |
| OmegaConf | Structured configs with runtime type safety and static type checker support [OmegaConf structured configs](https://omegaconf.readthedocs.io/en/latest/structured_config.html) | Use for Phase 1 composition of modular research configs, with Pydantic validating boundary objects [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| Hydra | Powerful config composition and command-line overrides [Hydra composition](https://hydra.cc/docs/1.2/tutorials/basic/your_first_app/composition/) | Defer until experiments need multirun sweeps or more elaborate config groups, because early Phase 1 needs fewer moving parts [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| MLflow | Local run tracking, parameters, metrics, artifacts, datasets, and UI [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/) | Use for Phase 1 tracking because it works locally and avoids cloud account coupling [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| Weights and Biases | Offline mode can save runs locally and sync later [W&B offline](https://docs.wandb.ai/models/ref/cli/wandb-offline), [W&B offline support](https://docs.wandb.ai/models/support/run_wandb_offline/) | Keep optional only, because Phase 1 should not require hosted experiment infrastructure [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |

## Tooling And CLI

| Option | Fit | Recommendation |
| --- | --- | --- |
| pytest | Standard discovery, fixtures, assertion introspection, and approximate comparisons [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html) | Use for unit, contract, numerical, leakage, and smoke tests [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md). |
| Ruff | Single fast linter and formatter with `ruff check` and `ruff format` [Ruff docs](https://docs.astral.sh/ruff/), [Ruff linter](https://docs.astral.sh/ruff/linter/), [Ruff formatter](https://docs.astral.sh/ruff/formatter/) | Use instead of separate Black, isort, pyflakes, and pycodestyle tools [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| mypy | Static type checking without executing code [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html) | Use gradually on shared interfaces first, then widen as the codebase stabilizes [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| pre-commit | Local hook orchestration and manual `run --all-files` verification [pre-commit docs](https://pre-commit.com/) | Use to run Ruff, mypy, and lightweight pytest gates before commits [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md). |
| Typer | Type-hint based CLI framework with automatic help and command trees [Typer PyPI](https://pypi.org/pypi/typer/) | Use for the research command interface because it matches typed Python components [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html). |
| Click | Stable composable CLI toolkit with nesting and generated help [Click docs](https://click.palletsprojects.com/en/stable/why/) | Treat as Typer's foundation and fallback for lower-level CLI behavior [Typer PyPI](https://pypi.org/pypi/typer/). |

