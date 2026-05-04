# Reproducibility Interface

## Interface Role

The reproducibility interface connects data adapters, event stores, feature builders, turbulence estimators, price-interface estimators, prediction models, backtest research, report generation, and validation. It is metadata and workflow design only for Phase 0. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Recommendation: Every swappable component should accept a resolved config object, input data version IDs, a seed namespace, and a run context, then return output IDs and audit events. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://mlflow.org/docs/latest/ml/tracking/.

## Run Manifest Interface

Recommendation: The run manifest should be the top-level object for reproducing a result. It should be serializable as JSON and logged as an MLflow artifact. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://docs.python.org/3/library/json.html, https://dvc.org/doc/use-cases/versioning-data-and-models.

Required fields:

```text
run_id
experiment_name
created_at_utc
command
phase
mode
git_commit
git_dirty_allowed
python_version
platform
machine
cpu_brand
dependency_lock_hash
config_id
config_hash
seed_manifest_id
dataset_ids
feature_set_ids
model_id
report_ids
validation_status
audit_log_id
```

Recommendation: `phase` must be `phase_0` or `phase_1_research` for this project stage, and `mode` must not contain `live`, `broker`, or `production`. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md.

## Data Version Interface

Recommendation: Data version records should identify provenance, license constraints, paid or private status, point-in-time availability, schema, hashes, and DVC metadata. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://databento.com/docs/standards-and-conventions, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

Required fields:

```text
dataset_id
dataset_role
source_name
source_url
license_or_entitlement
paid_or_private
may_commit_payload
retrieved_at_utc
available_at_cutoff_utc
time_range_utc_ns
symbols
venue
calendar
schema_version
storage_uri
dvc_path
content_hash
row_count
redaction_status
```

Recommendation: `may_commit_payload` must be false for paid vendor data, broker exports, private account records, and anything containing API keys or credentials. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://docs.github.com/ignore-files, https://docs.github.com/en/actions/concepts/security/secrets.

## Config Interface

Recommendation: Config objects should be typed and split into data, features, turbulence, interface, model, validation, tracking, report, and risk sections. Sources: https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Required fields:

```text
config_id
config_hash
schema_version
data
features
turbulence
price_interface
model
validation
tracking
report
risk
```

Recommendation: Secret values must never appear in resolved configs. Resolved configs may contain only redacted values, environment variable names, or local secret reference IDs. Sources: https://docs.pydantic.dev/latest/concepts/pydantic_settings/, https://docs.github.com/en/actions/concepts/security/secrets, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Seed Manifest Interface

Recommendation: Use a seed manifest with one `seed_root` and named component seeds. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://docs.python.org/3/library/random.html#notes-on-reproducibility, https://scikit-learn.org/stable/common_pitfalls.html.

Required fields:

```text
seed_manifest_id
seed_root
python_random_seed
numpy_seed
split_seed
synthetic_fixture_seed
model_seed
bootstrap_seed
notebook_seed
pythonhashseed
```

Recommendation: Components should request seeds by name from the run context instead of creating unlogged randomness. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://scikit-learn.org/stable/common_pitfalls.html.

## Experiment Tracking Interface

Recommendation: The run context should wrap MLflow operations for logging params, metrics, artifacts, tags, data inputs, and model versions. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://mlflow.org/docs/latest/ml/model-registry/.

Minimum operations:

```text
start_run(experiment_name, run_manifest)
log_param(name, value)
log_metric(name, value, step)
log_artifact(path, artifact_role)
log_dataset(dataset_record)
log_validation(validation_record)
register_model(model_record)
end_run(status)
```

Recommendation: `register_model` must reject missing validation summaries, missing data versions, missing config hashes, missing seed manifests, and prohibited aliases. Sources: https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/11-risk-controls-and-compliance/DECISION.md, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Report Interface

Recommendation: Report generation should consume only run manifests and tracked artifacts, then produce Markdown, HTML, PDF, or executed notebook outputs with a report manifest. Sources: https://papermill.readthedocs.io/en/latest/usage-workflow.html, https://jupyterbook.org/en/stable/content/execute.html, https://mlflow.org/docs/latest/ml/tracking/.

Required report manifest fields:

```text
report_id
run_id
template_id
template_hash
input_artifact_ids
generated_at_utc
output_paths
output_hashes
contains_paid_data_excerpt
contains_private_account_info
contains_secret
validation_status
```

Recommendation: Report generation must fail if it would include API keys, broker credentials, private account information, paid data excerpts, or unsupported profitability claims. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://docs.github.com/en/actions/concepts/security/secrets, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253.

## Audit Log Interface

Recommendation: Audit logs should be append-only JSONL files with one event per line. Sources: https://docs.python.org/3/library/logging.html, https://docs.python.org/3/library/json.html, https://mlflow.org/docs/latest/ml/tracking/.

Required fields:

```text
event_id
event_time_utc
event_type
run_id
component
severity
message
input_ids
output_ids
config_hash
seed_root
redaction_status
```

Recommendation: Audit events should record enough identifiers to trace from a report table back to the producing run, model, feature set, and dataset. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://mlflow.org/docs/latest/ml/model-registry/, https://dvc.org/doc/use-cases/versioning-data-and-models.

## Open Questions

1. Should `git_commit` be optional until the repository metadata is available in every working copy?
2. Should `storage_uri` allow only local paths during Phase 1, or also private DVC remotes?
3. Should audit logs include full warning stack traces or compact error summaries by default?
