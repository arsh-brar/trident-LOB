# Reproducibility Options

## Data Versioning Options

Option A is manifest-only data versioning. Recommendation: Use this only for early synthetic fixtures and public toy data, because it is simple but lacks DVC's ability to connect data, code, and model versions through lightweight metadata. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://docs.github.com/ignore-files, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

Option B is DVC for data and model artifact metadata with local or external storage. Recommendation: Choose this as the target Phase 1 data-versioning path because DVC is designed to version data and models with Git metadata while storing large files outside Git. Sources: https://dvc.org/doc/use-cases/versioning-data-and-models, https://dvc.org/doc/user-guide/basic-concepts/dvc-project, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

Option C is Git LFS for data. Recommendation: Do not make Git LFS the primary data-versioning system because TRIDENT needs dataset manifests, pipelines, hashes, and paid-data exclusion policy, not just large-file transport. Sources: https://dvc.org/doc/user-guide, https://docs.github.com/repositories/working-with-files/managing-large-files/about-git-large-file-storage, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Experiment Tracking Options

Option A is plain CSV or JSON run logs. Recommendation: Use this only as an export format, because it is easy to inspect but weak for run comparison, artifact lineage, and model registry integration. Sources: https://mlflow.org/docs/latest/ml/tracking/, https://docs.python.org/3/library/json.html.

Option B is local MLflow. Recommendation: Choose this as the Phase 1 default because prior architecture work selected MLflow local tracking and MLflow records runs, params, metrics, artifacts, datasets, and UI comparisons without requiring a hosted service. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://mlflow.org/docs/latest/ml/tracking/.

Option C is Weights and Biases. Recommendation: Keep this optional and opt-in only, because Phase 1 should be local-first and should not depend on hosted tracking or cloud sync. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://docs.wandb.ai/models/support/run_wandb_offline/, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md.

## Seed Control Options

Option A is ad hoc seeds inside scripts. Recommendation: Reject this because it makes splits, models, synthetic fixtures, and reports hard to reproduce. Sources: https://docs.python.org/3/library/random.html#notes-on-reproducibility, https://scikit-learn.org/stable/common_pitfalls.html.

Option B is one `seed_root` with derived component seeds. Recommendation: Choose this because it gives a simple audit path while allowing separate deterministic streams for data splits, model fits, bootstrap tests, and notebooks. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://docs.python.org/3/library/random.html, https://scikit-learn.org/stable/common_pitfalls.html.

Option C is fully entropy-driven repeated runs. Recommendation: Use this only for robustness sweeps after deterministic single-run reproduction is available, because nondeterministic entropy is useful for stress testing but weak for replaying a specific result. Sources: https://numpy.org/doc/stable/reference/random/index.html, https://docs.python.org/3/library/random.html#notes-on-reproducibility.

## Config Management Options

Option A is hand-written YAML without schema validation. Recommendation: Use this only for early notes, because schema-free configs can silently accept misspelled fields and ambiguous types. Sources: https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/.

Option B is OmegaConf structured configs plus Pydantic Settings for environment-derived values. Recommendation: Choose this for Phase 1 because it matches the existing architecture decision, supports runtime validation, and keeps secrets out of committed config files. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://omegaconf.readthedocs.io/en/latest/structured_config.html, https://docs.pydantic.dev/latest/concepts/pydantic_settings/.

Option C is Hydra from day one. Recommendation: Defer this until multirun sweeps are required, because prior architecture decisions prefer OmegaConf first and Hydra later for sweep composition. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/.

## Report Generation Options

Option A is manual notebooks. Recommendation: Reject manual notebooks as final evidence because hidden state and untracked execution order make results difficult to audit. Sources: https://nbformat.readthedocs.io/en/latest/format_description.html, https://papermill.readthedocs.io/en/latest/usage-workflow.html.

Option B is parameterized notebooks executed by Papermill. Recommendation: Choose this for exploratory reproducible reports because Papermill supports parameterized notebook execution and stores executed outputs as artifacts. Sources: https://papermill.readthedocs.io/en/latest/, https://papermill.readthedocs.io/en/latest/usage-workflow.html, https://mlflow.org/docs/latest/ml/tracking/.

Option C is Jupyter Book or Quarto for compiled research reports. Recommendation: Use this later when multiple reports need a browsable research site with cached or frozen notebook outputs. Sources: https://jupyterbook.org/en/stable/content/execute.html, https://quarto.org/docs/projects/code-execution.html.

## Model Registry Options

Option A is filesystem model folders. Recommendation: Use this only for throwaway experiments because it does not provide enough lineage, tagging, or version comparison. Sources: https://mlflow.org/docs/latest/ml/model-registry/, https://mlflow.org/docs/latest/ml/tracking/.

Option B is MLflow Model Registry with local backend. Recommendation: Choose this for Phase 1 research lineage because it links model versions to producing runs, tags, aliases, annotations, and artifacts. Sources: https://mlflow.org/docs/latest/ml/model-registry/, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

Option C is a hosted registry. Recommendation: Reject this for Phase 1 default because the project is local-first, CPU-only, and must not require cloud credentials or hosted services. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md, https://mlflow.org/docs/latest/ml/model-registry/, https://docs.github.com/en/actions/concepts/security/secrets.

## Audit Log Options

Option A is console-only logs. Recommendation: Reject this as the audit record because console output is easy to lose and difficult to join with run metadata. Sources: https://docs.python.org/3/library/logging.html, https://mlflow.org/docs/latest/ml/tracking/.

Option B is JSONL run audit logs plus MLflow metadata. Recommendation: Choose this because JSONL logs are append-friendly and MLflow stores run metadata, metrics, artifacts, and dataset links. Sources: https://docs.python.org/3/library/logging.html, https://docs.python.org/3/library/json.html, https://mlflow.org/docs/latest/ml/tracking/.

Option C is database audit logging. Recommendation: Defer this until orchestration requires concurrent multi-user writes, because Phase 1 is local Mac M3 research and should stay simple. Sources: file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md, https://docs.python.org/3/library/sqlite3.html, https://mlflow.org/docs/latest/ml/tracking/.

## Open Questions

1. Should DVC remotes be local-only for Phase 1, or should the project later define a private encrypted remote for collaborators?
2. Should the MLflow backend be filesystem-only or SQLite for better local registry behavior?
3. Should report generation standardize on notebooks first or pure Markdown reports first?
