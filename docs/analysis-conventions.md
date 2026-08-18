# Analysis conventions

Proposed defaults. **Ratify or change them in the Week 1 meeting**, then treat them as fixed -
`shared/config/analysis_config.yaml` is the machine-readable copy that code should read.

## Time series (Task 5)

- Buckets: ISO week (`2026-W34`) **and** calendar month (`2026-08`). Produce both.
- Window: the same start and end date for all four companies - set it to the widest range that all
  four datasets actually cover, and state it.
- Empty periods are **zero**, not missing.
- Hiring velocity = number of new postings per bucket. Rolling velocity = 4-week rolling mean.
- Growth rate = period-over-period percentage change on the rolling series, not the raw series.

## Comparison (Task 6)

- Never compare raw counts across companies. Use share of that company's postings, or postings per
  1,000 postings. Say which in every axis label.
- Role categories come from one agreed mapping, stored in `work/task-6/team/`.

## Forecasting (Task 7)

- Horizon: 12 weeks (3 months) ahead.
- Holdout: the final 8 weeks of the shared window.
- Metric: MAE and MAPE, both reported.
- Always include a naive baseline (last value carried forward, and seasonal naive).
- Report a prediction interval, not just a point estimate.

## Similarity (Task 8)

- Feature space: canonical skill share vectors from Task 4, TF-IDF weighted.
- Metric: cosine similarity. One canonical 4x4 matrix, produced by one owner, validated by the rest.

## Figures

- One chart per message; title states the finding, not the variable.
- Always label axes with the unit, including the normalisation.
- Same colour per company across every chart in the project - agree the four colours in Week 1 and
  put them in `shared/config/analysis_config.yaml`.
- Readable in greyscale; no red/green as the only distinction.
- Save as PNG at 150 dpi minimum into the task's `outputs/figures/`.

## Reproducibility

- Set and record a random seed wherever one is used.
- Relative paths only.
- State library versions in your method note.
