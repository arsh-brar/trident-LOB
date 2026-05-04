# Reproducibility Validation

## Validation Purpose

This document defines gates for reproducibility and experiment tracking. It is Phase 0 planning only and does not approve production code, live trading code, broker routing, paid-data commits, private credential commits, or profitability claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

Recommendation: A research result should not be considered reproducible until it can be rerun from a manifest on Mac M3 with matching dependency lock, config hash, data version IDs, seed root, validation metrics, and report checksums within documented tolerances. Sources: https://docs.astral.sh/uv/concepts/projects/sync/, https://mlflow.org/docs/latest/ml/tracking/, https://dvc.org/doc/use-cases/versioning-data-and-models.

## Gate 1: Repository And Dependency Reproduction

Recommendation: Validate that `uv sync --locked` succeeds before any run is accepted as reproducible. Sources: https://docs.astral.sh/uv/concepts/projects/sync/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Record Python version, platform, machine architecture, dependency lock hash, and CPU-only status in every accepted run. Sources: https://docs.python.org/3/library/platform.html, https://docs.astral.sh/uv/concepts/projects/sync/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Failure conditions:

```text
missing dependency lock
lock hash mismatch
untracked dependency override
non-CPU required dependency in Phase 1 core
missing environment summary
```

## Gate 2: Data Version And Leakage Reproduction

Recommendation: Validate every input dataset against its manifest, DVC metadata if present, content hash, schema version, point-in-time availability, license or entitlement, and commit policy. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md.

Recommendation: Fail validation if a feature, label, report, or notebook uses data with `available_at` after the prediction timestamp. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/07-news-and-exogenous-inputs/DECISION.md, https://scikit-learn.org/stable/common_pitfalls.html.

Failure conditions:

```text
missing dataset manifest
content hash mismatch
schema mismatch
future data detected
paid payload marked committable
private broker export marked committable
unknown license or entitlement
```

## Gate 3: Config And Secret Safety

Recommendation: Validate resolved configs against structured schemas and reject unknown fields, type mismatches, secret-looking values, private account identifiers, and paid data payloads. Sources: https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, https://docs.github.com/en/actions/concepts/security/secrets.

Recommendation: Store only `.env.example`, environment variable names, and local secret reference IDs in committed config or report artifacts. Sources: https://docs.github.com/ignore-files, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Failure conditions:

```text
resolved config contains an API key
resolved config contains broker credentials
resolved config contains private account information
resolved config contains paid data rows
unknown config field
config hash missing
```

## Gate 4: Seed And Determinism

Recommendation: Validate that every stochastic run has a seed manifest and that Python, NumPy, scikit-learn, splitters, bootstraps, synthetic fixtures, and notebooks use named seeds. Sources: https://docs.python.org/3/library/random.html#notes-on-reproducibility, https://numpy.org/doc/stable/reference/random/index.html, https://scikit-learn.org/stable/common_pitfalls.html.

Recommendation: Re-run a deterministic smoke test twice on the same Mac M3 environment and require matching split IDs, model parameters when deterministic, validation metrics, and report hashes within tolerances. Sources: https://docs.python.org/3/library/random.html#notes-on-reproducibility, https://numpy.org/doc/stable/reference/random/index.html, https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED.

Failure conditions:

```text
missing seed_root
unlogged random_state
PYTHONHASHSEED omitted when hash order affects output
two deterministic reruns produce different split IDs
two deterministic reruns exceed metric tolerance
```

## Gate 5: Experiment Tracking Completeness

Recommendation: Require each accepted run to log params, metrics, artifacts, data inputs, resolved config, seed manifest, validation summary, and audit log to local MLflow. Sources: https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Reject any run whose MLflow tags or artifacts imply live trading, broker routing, production deployment, or profitability without approved validation evidence. Sources: https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

Failure conditions:

```text
missing MLflow run ID
missing run manifest
missing validation summary
missing audit log artifact
prohibited live or production tag
profitability claim without approved evidence
```

## Gate 6: Model Registry

Recommendation: Validate that registered models include run ID, dataset IDs, feature IDs, config hash, seed manifest, validation status, and safe alias. Sources: https://mlflow.org/docs/latest/ml/model-registry/, https://mlflow.org/docs/latest/ml/tracking/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

Recommendation: Reject registry aliases outside `exploratory`, `candidate`, `rejected`, and `archived` during Phase 0 and Phase 1. Sources: https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Failure conditions:

```text
missing producing run
missing validation summary
missing data version
missing config hash
missing seed manifest
prohibited alias
```

## Gate 7: Reports And Notebooks

Recommendation: Validate reports by re-rendering from the run manifest and comparing output hashes, numeric tables, chart data, and declared source IDs. Sources: https://papermill.readthedocs.io/en/latest/usage-workflow.html, https://jupyterbook.org/en/stable/content/execute.html, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: Reject notebooks or reports that contain secrets, private account information, paid data excerpts, unapproved live-trading language, or unsupported profitability claims. Sources: https://nbformat.readthedocs.io/en/latest/format_description.html, https://docs.github.com/en/actions/concepts/security/secrets, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Failure conditions:

```text
notebook cannot execute from clean kernel
report cannot render from run manifest
report hash mismatch outside tolerance
secret detected
paid data excerpt detected
private broker information detected
unsupported profitability claim
```

## Gate 8: Audit Logs

Recommendation: Validate JSONL audit logs for required event types, monotonic UTC timestamps per process, run ID consistency, config hash consistency, seed root consistency, and redaction status. Sources: https://docs.python.org/3/library/logging.html, https://docs.python.org/3/library/json.html, https://mlflow.org/docs/latest/ml/tracking/.

Recommendation: Keep audit logs append-only and log them as MLflow artifacts for each run. Sources: https://docs.python.org/3/library/logging.html, https://mlflow.org/docs/latest/ml/tracking/.

Failure conditions:

```text
audit log missing
invalid JSONL
missing required event
run ID mismatch
unredacted secret
timestamp after report generation for prerequisite event
```

## Open Questions

1. What numeric tolerances should be allowed for floating-point reruns on the same Mac M3?
2. Should chart image hashes be exact, or should validation compare underlying chart data only?
3. Should secret scanning be a required pre-commit hook or a validation command only?
4. Which validation gates become required before a model can move from `exploratory` to `candidate`?
