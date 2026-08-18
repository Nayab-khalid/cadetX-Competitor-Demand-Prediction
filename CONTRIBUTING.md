# Contributing

Read this before your first commit. These conventions exist so that four people working separately
produce work that can be combined.

## Where work goes

- Your submission for a task goes in `work/task-N/<your-folder>/`. Nowhere else.
- Team submissions for a task go in `work/task-N/team/`.
- Meeting minutes and weekly notes go in `minutes-of-meeting/sprint-N/`.
- Standards that everyone must follow are in `shared/`. Changing anything there must be agreed in a
  meeting first, because it affects the other three datasets.
- Do not edit another member's folder. Raise the issue in the weekly meeting instead.

## Naming

- Folders and files use lowercase letters and hyphens, with no spaces.
- Datasets: `<company>_<stage>_<YYYYMMDD>.csv`, for example `nvidia_postings_raw_20260901.csv`.
  Stages: `postings_raw`, `postings_clean`, `skills_long`, `skill_matrix`, `timeseries`, `forecast`.
- Figures: `<company>_<description>.png`.

## Git

- `main` must always work. Create a branch for your task, for example `task-1/nvidia`.
- Commit messages state the task and the company, for example
  `task-1(nvidia): add source review`.
- Open a pull request into `main` and ask one team member to review it.
- Commit regularly. Do not leave a whole task until the night before the deadline.

## Data

- Columns and formats follow [docs/data-schema.md](docs/data-schema.md).
- Run `python scripts/validate_dataset.py <file>` before committing any dataset. It must pass.
- No personal data, no credentials, no API keys.
- GitHub rejects files above 100 MB. If a dataset is large, commit a compressed file or a documented
  sample and state the full size in your report.

## Notebooks

- A notebook must run from top to bottom on a clean kernel before it is committed.
- Use relative paths only.
- Reusable code belongs in a `.py` file, not in a notebook.

## A task is complete when

1. Everything listed in the task README has been submitted.
2. Every item in the definition of done is ticked.
3. Your row in the task status table is updated.
4. The work is merged into `main`.

Only then does the Scrum Leader submit the repository URL in the CadetX portal.
