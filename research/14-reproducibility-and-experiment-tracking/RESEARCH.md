# Reproducibility And Experiment Tracking Research

## Scope

This is Phase 0 planning only. It defines reproducibility and experiment tracking policy for offline TRIDENT-LOB research on a CPU-only Apple Silicon Mac M3. It does not approve production code, live trading code, broker routing, paid-data commits, API-key commits, or profitability claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

The three planning files named in AGENTS.md, `plans/INTERFACES.md`, `plans/ORCHESTRATION.md`, and `plans/VALIDATION_GATES.md`, were not present during this research pass. The available decision files from research `00` through `07`, `11`, and `12` were read. The directories `08`, `09`, `10`, and `13` contained README files but no `DECISION.md` at the time of review. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Research Goals

Recommendation: Phase 1 should make every research result reproducible from a run manifest that identifies code version, dependency lock, config, seed plan, data version, feature version, model version, hardware profile, and report artifact. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://dvc.org/doc/use-cases/versioning-data-and-models, https://docs.astral.sh/uv/concepts/projects/sync/.

Recommendation: Reproducibility should be local-first and offline by default, because prior architecture decisions choose CPU-only Python on Mac M3 and MLflow local tracking over hosted tracking services for Phase 1. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://mlflow.org/docs/latest/ml/tracking/, https://docs.astral.sh/uv/concepts/projects/layout/.

Recommendation: The reproducibility layer should log enough metadata to reject future-data leakage and stale or unapproved model versions before any result is promoted from exploratory to candidate. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://scikit-learn.org/stable/common_pitfalls.html, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Data Versioning

Recommendation: Use DVC metadata for local data versioning and keep large datasets, paid data, broker exports, and vendor archives outside Git. Commit only lightweight DVC metadata, schema definitions, checksums, and synthetic fixtures that are allowed by license. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://dvc.org/doc/user-guide, https://docs.github.com/ignore-files, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Recommendation: Each dataset version should have a manifest with `dataset_id`, `source_name`, `source_url`, `license_or_entitlement`, `retrieved_at`, `available_at_cutoff`, `symbols`, `venue`, `calendar`, `time_range_utc_ns`, `schema_version`, `row_count`, `content_hash`, `dvc_hash`, and `paid_or_private` flags. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

Recommendation: Feature stores should reference immutable input dataset IDs and feature-builder config hashes rather than mutable file names alone. Sources: https://dvc.org/doc/user-guide/basic-concepts/dvc-project, https://mlflow.org/docs/latest/ml/tracking/, https://scikit-learn.org/stable/common_pitfalls.html.

## Experiment Tracking

Recommendation: Use local MLflow tracking for Phase 1 runs. Each run should log params, metrics, artifacts, dataset inputs, code version when available, dependency lock hash, config hash, seed root, hardware profile, and validation status. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Treat MLflow run IDs as audit references, not as permission to deploy models. A run can be `exploratory`, `candidate`, `rejected`, or `archived`, but Phase 1 must not include a live-trading stage or alias. Sources: https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Recommendation: Keep raw MLflow artifact stores local and ignored by Git, then export small run cards, validation summaries, and report manifests to versioned text or JSON files when they are safe to share. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://docs.github.com/ignore-files, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Seed Control

Recommendation: Every stochastic run should start from a single integer `seed_root`, then derive component seeds for splits, model initialization, bootstrap tests, synthetic fixtures, and notebook execution. Sources: https://docs.python.org/3/library/random.html, https://numpy.org/doc/stable/reference/random/index.html, https://scikit-learn.org/stable/common_pitfalls.html.

Recommendation: Use `numpy.random.default_rng(seed)` for NumPy randomness, set `random.seed(seed)` for Python standard-library randomness when used, set integer `random_state` values for scikit-learn estimators and splitters, and record `PYTHONHASHSEED` when deterministic hashing affects outputs. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://docs.python.org/3/library/random.html, https://scikit-learn.org/stable/common_pitfalls.html, https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED.

Recommendation: Deterministic claims should be limited to the same code, dependency lock, Python version, CPU architecture, input data, config, and seed plan, because numerical and stochastic libraries can change behavior across versions. Sources: https://docs.python.org/3/library/random.html#notes-on-reproducibility, https://numpy.org/doc/stable/reference/random/index.html, https://docs.astral.sh/uv/concepts/projects/sync/.

## Config Management

Recommendation: Use structured, typed configs with OmegaConf for Phase 1 composition and Pydantic Settings only for environment-derived runtime settings. Defer Hydra until multirun sweeps are needed. Sources: https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Config files must contain no secrets, no private broker account identifiers, and no paid data payloads. Configs may reference environment variable names, local secret keys, and local path placeholders. Sources: https://docs.pydantic.dev/latest/concepts/pydantic_settings/, https://docs.github.com/en/actions/concepts/security/secrets, https://docs.github.com/ignore-files, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Reports And Notebooks

Recommendation: Reports should be generated from tracked run manifests and parameterized notebooks or scripts, with all charts and tables traceable to dataset IDs, config hashes, and run IDs. Sources: https://papermill.readthedocs.io/en/latest/, https://jupyterbook.org/en/stable/content/execute.html, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: Notebooks should be reproducible research views, not the source of record for reusable logic. Notebook inputs should be parameterized, outputs should be regenerated during validation, and notebook metadata should record kernel and language information. Sources: https://papermill.readthedocs.io/en/latest/usage-workflow.html, https://nbformat.readthedocs.io/en/latest/format_description.html, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Reports must avoid profitability claims unless later validation gates require out-of-sample, transaction-cost-adjusted evidence and approve the claim. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Model Registry

Recommendation: Use MLflow Model Registry locally for research model lineage only. A registered model version should include the producing run ID, dataset ID, feature set ID, config hash, seed root, validation summary, and approval status. Sources: https://mlflow.org/docs/latest/ml/model-registry/, https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Recommendation: Model aliases should be limited to `exploratory`, `candidate`, `rejected`, and `archived` in Phase 1. Do not use `production`, `champion`, or `live` aliases during Phase 0 or Phase 1. Sources: https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Audit Logs

Recommendation: Each run should produce append-only JSONL audit events for run start, config resolution, data load, feature build, split creation, fit start, fit end, validation, report render, and model registration. Sources: https://docs.python.org/3/library/logging.html, https://mlflow.org/docs/latest/ml/tracking/, https://docs.python.org/3/library/json.html.

Recommendation: Audit events should include UTC timestamps, run ID, process ID, command, user-visible mode, dataset IDs, config hash, seed root, code version if available, and redacted credential references only. Sources: https://docs.python.org/3/library/logging.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, https://docs.github.com/en/actions/concepts/security/secrets.

## Open Questions

1. Should Phase 1 adopt DVC immediately, or start with plain manifests and add DVC when the first non-synthetic dataset arrives?
2. Should local MLflow use file storage only, or a SQLite backend store for registry behavior on Mac M3?
3. Which report renderer should become canonical for Phase 1: parameterized notebooks, Jupyter Book, or a Python-generated Markdown report?
4. What minimum metadata is required before a research model can be marked `candidate`?
5. How should collaborators share reproducible runs when paid data cannot be committed or redistributed?
