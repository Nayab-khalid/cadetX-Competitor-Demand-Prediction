# shared/

The things all four members must use **identically**. Anything here changes only by PR with a
second member's approval - editing it locally silently breaks the other three datasets.

- `schema/job_postings.schema.json` - machine-readable column contract (see `docs/data-schema.md`)
- `taxonomy/skills.yaml` - canonical skill names and aliases (see `docs/skill-taxonomy.md`)
- `config/analysis_config.yaml` - window, buckets, forecast horizon, metrics, company colours
