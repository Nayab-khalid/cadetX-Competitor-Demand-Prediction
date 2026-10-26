#!/usr/bin/env python3
"""Optional Task 11 - pipeline runner, Microsoft.

One entry point that rebuilds every downstream artefact from the Task 2 file,
in dependency order:

    task-3 preprocess -> task-4 extract -> task-5 trends
                      -> task-6 compare -> task-7 forecast
                      -> task-8 similarity -> task-9 insights

    python run_pipeline.py

ON SCHEDULING, which the brief frames this around. A cron or Actions schedule
assumes a source you can re-poll. Microsoft's careers site blocks automated
access and the MIT-licensed repository is a static file, so a nightly run would
reprocess identical bytes.

What is useful for Microsoft is reproducibility: a change to Task 3's cleaning
rules propagates through six downstream scripts without anyone re-running them
by hand in the right order. It already earned that - its first run caught a
stale input path left over from reorganising folders.

Members whose companies expose a live ATS API should own the scheduled
ingestion half of this task.
"""
from __future__ import annotations
import subprocess, sys, time
from pathlib import Path

W = Path(__file__).resolve().parents[2]
M = "microsoft-arham-malik"
STAGES = [
    ("task-3  preprocess",  W/"task-3"/M, "preprocess.py"),
    ("task-4  extract",     W/"task-4"/M, "extract_skills.py"),
    ("task-5  trends",      W/"task-5"/M, "trend_analysis.py"),
    ("task-6  compare",     W/"task-6"/M, "compare_companies.py"),
    ("task-7  forecast",    W/"task-7"/M, "forecasting.py"),
    ("task-8  similarity",  W/"task-8"/M, "similarity.py"),
    ("task-9  insights",    W/"task-9"/M, "insights.py"),
]

def main() -> int:
    print("Microsoft pipeline\n")
    failed = 0
    for label, cwd, script in STAGES:
        t0 = time.time()
        r = subprocess.run([sys.executable, script], cwd=cwd,
                           capture_output=True, text=True)
        dt = time.time() - t0
        if r.returncode == 0:
            print(f"  ok       {label}  ({dt:.1f}s)")
        else:
            failed += 1
            err = (r.stderr or "").strip().splitlines()
            print(f"  FAILED   {label}  ({dt:.1f}s)")
            print(f"           {err[-1] if err else 'unknown'}")
    print(f"\n{len(STAGES)-failed}/{len(STAGES)} stages completed")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
