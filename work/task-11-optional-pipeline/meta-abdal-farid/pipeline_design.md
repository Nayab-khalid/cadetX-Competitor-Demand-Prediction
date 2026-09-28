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
