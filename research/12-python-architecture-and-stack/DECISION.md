# Python Architecture And Stack Decision

## Recommended Phase 1 Stack

Use native arm64 Python 3.12 on macOS with a project lock file managed by `uv`. This satisfies the local Mac Apple Silicon M3 requirement while aligning with documented project-based install workflows for NumPy and SciPy [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [Apple Silicon documentation](https://developer.apple.com/documentation/apple-silicon), [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install), [uv PyPI](https://pypi.org/pypi/uv).

Use Polars as the primary DataFrame engine, pandas only for compatibility, DuckDB as the local query layer, and Parquet as the canonical file format. This fits TRIDENT's event-stream, price-grid, and feature-window workload while staying local and CPU-only [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [Polars lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/), [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview), [Apache Parquet overview](https://parquet.apache.org/docs/overview/), [pandas user guide](https://pandas.pydata.org/docs/user_guide/).

Use NumPy and SciPy as the numerical core. Do not make JAX or PyTorch core Phase 1 dependencies, because the project requires CPU-only local execution and simple baselines before complex models [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [NumPy install](https://numpy.org/install/), [SciPy install](https://scipy.org/install), [JAX install](https://docs.jax.dev/en/latest/installation.html), [PyTorch local install](https://docs.pytorch.org/get-started/locally/).

Use scikit-learn for first-pass models and validation baselines. Add XGBoost as an optional dependency only after baseline gates require boosted trees. Keep LightGBM secondary because macOS setup can involve OpenMP runtime friction [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [scikit-learn install](https://scikit-learn.org/stable/install.html), [XGBoost install](https://xgboost.readthedocs.io/en/release_3.0.0/install.html), [LightGBM install](https://lightgbm.readthedocs.io/en/stable/Installation-Guide.html).

Use Pydantic for strict external data and config validation, OmegaConf for initial config composition, and defer Hydra until multirun sweeps are needed. This keeps modularity without overloading the first implementation [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/), [OmegaConf structured configs](https://omegaconf.readthedocs.io/en/latest/structured_config.html), [Hydra composition](https://hydra.cc/docs/1.2/tutorials/basic/your_first_app/composition/), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md).

Use MLflow local tracking for runs, metrics, parameters, artifacts, and datasets. Keep Weights and Biases optional and opt-in only, because Phase 1 should not depend on a hosted service [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/), [W&B offline](https://docs.wandb.ai/models/ref/cli/wandb-offline), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Use pytest, Ruff, mypy, and pre-commit as the minimum quality toolchain. This gives unit and contract tests, formatting, linting, gradual type checking, and local hooks [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), [Ruff docs](https://docs.astral.sh/ruff/), [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html), [pre-commit docs](https://pre-commit.com/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Use Typer for the research CLI, with Click as the stable underlying CLI foundation. The CLI should expose offline research workflows such as ingest, build-features, estimate-turbulence, fit-baseline, backtest, validate, and report, without live trading commands in Phase 1 [Typer PyPI](https://pypi.org/pypi/typer/), [Click docs](https://click.palletsprojects.com/en/stable/why/), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

## Proposed Package Layout

The production package should eventually use a `src/` layout with swappable components that mirror the project architecture preferences [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [TRIDENT model](file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md), [Python pyproject guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml?trk=public_post_comment-text).

```text
trident_lob/
  __init__.py
  cli/
    app.py
    commands/
  config/
    schemas.py
    defaults/
  contracts/
    protocols.py
    types.py
  data/
    adapters/
    catalog.py
    parquet_io.py
  events/
    store.py
    schemas.py
  features/
    builders/
    windows.py
  turbulence/
    estimators/
    closure.py
  interface/
    estimators/
    price_interface.py
  models/
    baselines/
    boosted/
  backtest/
    engine.py
    costs.py
    metrics.py
  paper/
    adapter.py
  risk/
    manager.py
  reports/
    generator.py
  validation/
    leakage.py
    splits.py
    gates.py
  tracking/
    mlflow.py
```

The layout keeps data adapters, event stores, feature builders, turbulence estimators, price-interface estimators, prediction models, backtester, paper-trading adapter, risk manager, and report generator replaceable through protocols rather than concrete imports [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [mypy getting started](https://mypy.readthedocs.io/en/latest/getting_started.html), [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/).

## Dependency Policy

Pin direct dependencies through `pyproject.toml` plus a committed lock file. Use dependency groups for `dev`, `ml`, `docs`, and `notebooks` so Phase 1 core installs stay small [Python dependency groups](https://packaging.python.org/en/latest/specifications/dependency-groups/), [uv PyPI](https://pypi.org/pypi/uv), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Keep core dependencies to packages that have documented macOS and Apple Silicon or pure Python support. Mark heavier ML dependencies such as XGBoost, PyTorch, and JAX as optional groups, not core dependencies [XGBoost install](https://xgboost.readthedocs.io/en/release_3.0.0/install.html), [PyTorch local install](https://docs.pytorch.org/get-started/locally/), [JAX install](https://docs.jax.dev/en/latest/installation.html), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

Prefer binary wheels and avoid source builds for Phase 1 unless a validation need justifies the maintenance cost. This is consistent with SciPy's recommendation to use binaries where available and with the Apple Silicon native execution target [SciPy build docs](https://docs.scipy.org/doc/scipy/building/index.html), [Apple Silicon documentation](https://developer.apple.com/documentation/apple-silicon), [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md).

No dependency may require broker credentials, paid data keys, cloud sync, or live-trading capabilities for core tests. This follows the repository rules and keeps Phase 1 research offline and auditable [AGENTS](file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md), [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/), [W&B offline](https://docs.wandb.ai/models/support/run_wandb_offline/).

