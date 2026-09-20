# Optional Task: Automated Pipeline

## Objective

Connect collection, preprocessing, skill extraction, trend analysis and forecasting into one scheduled, end-to-end pipeline.

## What is submitted

**Each member (in their own folder)**

1. Documented pipeline design and automation steps
2. The final workflow in GitHub

## Rules for this task

- Stages are the tasks' own scripts, run unmodified, so the pipeline cannot drift from what was committed.
- A stage failure stops the run by default.

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

## State

**Working and verified: 6 of 6 stages in 244.5 seconds, 37 output files hashed.**

```bash
cd work/task-11-optional-pipeline/nvidia-nayab-khalid
python run_pipeline.py
```

Scheduled weekly by
[.github/workflows/nvidia-pipeline.yml](../../.github/workflows/nvidia-pipeline.yml). It uploads
artefacts and deliberately does **not** commit results back: an unattended commit would rewrite
datasets that other members depend on.

NVIDIA only. Wiring in the other three members' stages is a team task, since their scripts and
layouts differ.

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
