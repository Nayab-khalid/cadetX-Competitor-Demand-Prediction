# Optional Task 11 – Automated Pipeline By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

## Design
`run_pipeline.py` sequences the already-built and independently-documented Task 3–9 scripts into one end-to-end run: **NLP Preprocessing → Skill Extraction → Trend Analysis → Competitor Comparison → Demand Forecasting → Similarity Scoring → Insight Dashboard regeneration.** It does not duplicate any task's logic — it calls each task's own script (`subprocess.run`, correct working directory per stage) exactly as documented in that task's README, and stops on the first non-zero exit code so a broken stage never lets stale/inconsistent output flow downstream.

`--from N` lets a stage be resumed without rerunning earlier ones (e.g. `--from 7` after only touching the forecasting script).

## Automation
Three ways to run this on a schedule, all pointed at the same script:
1. **Cron** (Linux/macOS): `0 3 * * 1  cd /path/to/repo/Optional_Automated_Pipeline && python run_pipeline.py` — weekly, Monday 03:00.
2. **Windows Task Scheduler**: a weekly trigger running `python run_pipeline.py` from this folder.
3. **GitHub Actions** (`../.github/workflows/pipeline.yml`) — runs weekly (`cron: "0 3 * * 1"`) and on manual dispatch, installs the Python + NLTK dependencies fresh, runs the full pipeline, and uploads every stage's CSV/PNG output as a downloadable workflow artifact (so results are inspectable without pushing generated files back into the repo).

## Validated
Ran end-to-end in this workspace: **31.3s total** (Task 3: 8.6s, Task 4: 4.3s, Task 5: 4.2s, Task 6: 2.8s, Task 7: 4.3s, Task 8: 4.1s, Task 9: 3.0s), reproducing identical output to running each task individually.

## Task 11 Outcome
A single orchestrator chains Tasks 3–9 into one reproducible run, with cron/Task-Scheduler instructions and a working GitHub Actions workflow for scheduled, artifact-producing runs — the automated-pipeline deliverable for this track.
