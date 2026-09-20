# Automated Pipeline — NVIDIA

Member: Nayab Khalid | Company: NVIDIA | Optional Task | Date: 2026-09-20

## What it does

One command runs the entire NVIDIA workstream end to end:

```
collect (T2) → preprocess (T3) → skills (T4) → trends (T5) → compare (T6) → forecast (T7) → similarity (T8)
```

```bash
cd work/task-11-optional-pipeline/nvidia-nayab-khalid
python run_pipeline.py
```

**Verified run:** 6 of 6 stages passed in 244.5 seconds, 37 output files hashed.
(Collection excluded by default — see below.)

## Design decisions

**Each stage is the task's own script, run unmodified.** Nothing is reimplemented in the pipeline,
so it cannot drift away from what the tasks actually committed. If Task 5's script changes, the
pipeline picks the change up automatically.

**Collection is opt-in.** `--with-collection` re-downloads weekly snapshots, which is slow and hits
a third-party host. The default run starts from the committed raw dataset, so a routine run is fast
and works offline. Politeness to someone else's server is a design constraint, not an afterthought.

**A stage failure stops the pipeline.** Task 5 reading a half-written Task 3 output would produce
numbers that look plausible and are wrong. `--keep-going` overrides this, deliberately and
explicitly.

**Resumable.** `--from trends` restarts at the stage that failed; `--only forecast` runs one stage.

**Every run writes a manifest** — `runs/manifest_<timestamp>.json` — recording which stages ran,
how long each took, and the SHA-256 of every output file. Two runs can therefore be compared
directly, and a silent change in the third-party source shows up as a changed hash rather than as a
quietly different number in a report.

## Scheduling

[`.github/workflows/nvidia-pipeline.yml`](../../../.github/workflows/nvidia-pipeline.yml) runs it
every Monday at 06:00 UTC, before the weekly team meeting, and on manual dispatch.

**It does not commit results back to the repository.** An unattended commit would rewrite datasets
that other members' work depends on, and the Task 6 and Task 8 findings both turn on knowing
exactly which version of the data produced a number. Results are uploaded as build artefacts;
promoting a run to the repository stays a human decision.

The workflow also runs the dataset validator with `continue-on-error`, so the known
`job_description` failure is reported rather than hidden.

## Why this matters for Task 7

The forecast rests on 12 observations. Every weekly run adds one. Left scheduled, the pipeline
fixes the project's biggest weakness by simply continuing to run — which is a better argument for
automation than the time it saves.

## Commands

| Command | Does |
|---|---|
| `python run_pipeline.py` | preprocess → similarity, from committed data |
| `python run_pipeline.py --with-collection` | includes the download |
| `python run_pipeline.py --from trends` | resume after a failure |
| `python run_pipeline.py --only forecast` | one stage |
| `python run_pipeline.py --dry-run` | print the plan and exit |

## Limitations

1. **Not idempotent across source changes.** A re-run with `--with-collection` may produce
   different data, because the upstream source adds a snapshot daily. That is intended, and the
   manifest hashes make it visible.
2. **NVIDIA only.** The other three members' stages are not wired in; their scripts and layouts
   differ. Generalising this is a team task, not a solo one.
3. **No retry or backoff** on the download. A transient network failure fails the stage; the
   resume flag is the mitigation.
4. **The workflow has not been executed on GitHub Actions**, only locally. The first scheduled run
   will be the real test of the dependency list.
