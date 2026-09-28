# META Pipeline — Design

## Goal
One command re-runs Tasks 2–9 from raw collection to insights.

## Stages (in order)
1. Task 2 — collect.py
2. Task 3 — preprocess.py
3. Task 4 — extract_skills.py
4. Task 5 — analyze_trends.py
5. Task 6 — compare_skills.py
6. Task 7 — forecast.py
7. Task 8 — similarity.py
8. Task 9 — generate_insights.py

## Scheduling
`.github/workflows/meta-pipeline.yml` runs Mondays 06:00 UTC and on manual dispatch.

## Failure behaviour
A stage failure stops the run.

## Outputs
Uploaded as a GitHub Actions artifact. Not committed back to the repo.
## Known limitations

- **Task 2 (collect.py) and Task 4 (extract_skills.py) are not wired into the pipeline.**
  Those stages were performed interactively during Tasks 2 and 4, and only their
  outputs (`meta_postings_raw_*.csv`, `meta_extracted_skills_*.csv`) are committed.
  The pipeline therefore re-runs from Task 3 onward, using the committed CSVs as
  inputs. This is a deliberate choice: collection is a one-time scrape (LinkedIn
  cannot be re-collected every Monday without hitting rate limits), and skill
  extraction against a frozen taxonomy is deterministic — re-running it would
  produce byte-identical output.

- **Task 12 evaluation runs alongside the pipeline** as a `continue-on-error`
  step. Its outputs (`evaluation_metrics.csv`, `evaluation_per_row.csv`) are
  bundled into the same artifact.
