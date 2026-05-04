# Reproducibility And Experiment Tracking Decision

Status: Phase 0 decision. This does not authorize production code, live trading code, paid-data commits, private credential commits, broker routing, or profitability claims.

## Decision

TRIDENT-LOB Phase 1 will use a local-first reproducibility stack on Mac M3: `uv` lock files for dependencies, DVC metadata for data versioning, local MLflow for experiment tracking and model lineage, OmegaConf structured configs with Pydantic Settings for environment-derived settings, explicit seed manifests, parameterized reports, reproducible notebooks, local model registry metadata, and append-only JSONL audit logs. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://docs.astral.sh/uv/concepts/projects/sync/, https://dvc.org/doc/use-cases/versioning-data-and-models, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: The canonical reproduction unit is a run manifest, not an informal notebook or a folder name. The manifest must identify code version if available, dependency lock hash, command, config hash, seed root, data version IDs, feature version IDs, model version ID, report artifact IDs, validation status, and audit-log path. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://dvc.org/doc/use-cases/versioning-data-and-models, https://docs.astral.sh/uv/concepts/projects/sync/.

## Reproduction Structure For Mac M3

Recommendation: A Phase 1 result should be reproducible on Mac M3 with this structure:

```text
configs/
  defaults/
  experiments/
data/
  README.md
  manifests/
experiments/
  mlruns/
  audit/
  run_manifests/
models/
  registry/
notebooks/
  templates/
reports/
  generated/
```

The large local directories `data/raw`, `data/interim`, `data/processed`, `experiments/mlruns`, and private model artifacts should be ignored by Git or tracked only through DVC metadata when allowed. Sources: https://docs.github.com/ignore-files, https://dvc.org/doc/user-guide/basic-concepts/dvc-project, https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Recommendation: The standard reproduction command shape should be:

```text
uv sync --locked
PYTHONHASHSEED=<seed_root> uv run trident-lob run --config <config_id> --seed <seed_root>
uv run trident-lob report --run-id <mlflow_run_id>
uv run trident-lob validate --run-id <mlflow_run_id>
```

This command shape is a Phase 0 interface decision only, not production code. Sources: https://docs.astral.sh/uv/concepts/projects/sync/, https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: A reproduced result should pass only when the generated manifest matches the expected dependency lock hash, config hash, dataset IDs, feature IDs, seed root, validation status, and report checksums. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://mlflow.org/docs/latest/ml/tracking/, https://docs.python.org/3/library/hashlib.html.

## Data Versioning Decision

Recommendation: Use DVC metadata plus dataset manifests as the Phase 1 data versioning design. Do not commit API keys, broker credentials, private account exports, paid data payloads, or private vendor archives. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://docs.github.com/ignore-files, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

Recommendation: Synthetic fixtures and tiny public sample data may be committed only if license and provenance are clear. Paid data and broker exports may be referenced by manifest and DVC metadata but must remain outside Git. Sources: https://docs.github.com/ignore-files, https://dvc.org/doc/user-guide, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Recommendation: Every dataset manifest must include point-in-time availability fields so that features can be rebuilt without future data. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://databento.com/docs/standards-and-conventions.

## Experiment Tracking Decision

Recommendation: Use local MLflow as the default experiment tracker. Each run must log parameters, metrics, validation outcomes, artifacts, data inputs, resolved config, seed manifest, and environment summary. Sources: https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Export small, shareable run summaries from MLflow to `experiments/run_manifests` or `reports/generated` when they contain no secrets, paid data, or private account details. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://docs.github.com/ignore-files, https://docs.github.com/en/actions/concepts/security/secrets.

## Seed Control Decision

Recommendation: Every run must have a `seed_root` and a seed manifest that derives named child seeds for splits, synthetic fixtures, models, bootstraps, and notebooks. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://docs.python.org/3/library/random.html#notes-on-reproducibility, https://scikit-learn.org/stable/common_pitfalls.html.

Recommendation: Phase 1 should use deterministic seed settings before running repeated-randomness robustness checks. Robustness sweeps may use multiple seed roots, but each individual run must still be replayable. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://scikit-learn.org/stable/common_pitfalls.html.

## Config Management Decision

Recommendation: Use OmegaConf structured configs for experiment composition, with Pydantic Settings for values loaded from environment variables or secret directories. Commit only non-secret defaults and examples. Sources: https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Defer Hydra until multirun sweeps are required, then use it only for offline research sweeps with explicit run manifests. Sources: https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Report And Notebook Decision

Recommendation: Use parameterized notebooks or script-backed Markdown reports as reproducible report views. Reports must be generated from run manifests and must cite dataset IDs, config hashes, model IDs, run IDs, and validation status. Sources: https://papermill.readthedocs.io/en/latest/usage-workflow.html, https://jupyterbook.org/en/stable/content/execute.html, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: Notebooks may be committed as templates or executed reports only when outputs are safe, small, and do not contain paid data excerpts, private account information, API keys, or broker credentials. Sources: https://nbformat.readthedocs.io/en/latest/format_description.html, https://docs.github.com/ignore-files, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Model Registry Decision

Recommendation: Use MLflow Model Registry locally for research lineage. Register only models that have run manifests, validation summaries, data version IDs, config hashes, seed manifests, and no live-trading approval. Sources: https://mlflow.org/docs/latest/ml/model-registry/, https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Recommendation: Phase 1 aliases are limited to `exploratory`, `candidate`, `rejected`, and `archived`. Any `production`, `live`, `broker`, or `champion` alias is rejected during Phase 0 and Phase 1. Sources: https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Audit Log Decision

Recommendation: Every run should emit JSONL audit logs and log the audit file as an MLflow artifact. The JSONL file should include run lifecycle events, config resolution, data inputs, feature outputs, split creation, fit lifecycle, validation, report rendering, model registration, warnings, and failures. Sources: https://docs.python.org/3/library/logging.html, https://docs.python.org/3/library/json.html, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: Audit logs must redact secrets and must store only secret reference names or environment variable names. Sources: https://docs.github.com/en/actions/concepts/security/secrets, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Non-Decision

This decision does not approve live trading, live broker integration, paid data purchase, production ingestion, hosted experiment tracking, cloud artifact storage, or profitability claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270.

## Open Questions

1. Should local MLflow use a SQLite backend for registry behavior, or is filesystem tracking enough for the first Phase 1 implementation?
2. Should DVC be introduced before the first paid or large dataset arrives, or only after synthetic fixture validation?
3. Should reproduced reports be required to match image checksums exactly, or only table outputs and numeric metrics?
4. How should collaborators exchange manifests for paid data that cannot be redistributed?
5. What validation status should be required before a model becomes `candidate`?
