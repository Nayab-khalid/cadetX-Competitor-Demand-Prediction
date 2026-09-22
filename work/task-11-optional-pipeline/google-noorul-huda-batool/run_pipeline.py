"""
Optional Task - Automated Pipeline
Author: Noor Ul Huda | Company track: Google

Chains Tasks 3-9 into one scheduled, end-to-end run: NLP preprocessing ->
skill extraction -> trend analysis -> competitor comparison -> forecasting ->
similarity scoring -> insight/dashboard regeneration. Each stage is the exact
script already used (and documented) in its own Task folder -- this file
does not duplicate their logic, it only sequences them and stops on the
first failure so a broken stage never silently produces stale downstream
output.

Usage:
  python run_pipeline.py            # run all stages
  python run_pipeline.py --from 5   # resume from Task 5 (skip earlier stages)

Scheduling:
  - Cron (Linux/mac): 0 3 * * 1  cd /path/to/repo/Optional_Automated_Pipeline && python run_pipeline.py
  - Windows Task Scheduler: run `python run_pipeline.py` weekly from this folder.
  - GitHub Actions: see ../.github/workflows/pipeline.yml (runs on a weekly
    schedule and on manual dispatch; artifacts from each task's output are
    uploaded so a run's results are downloadable even without pushing back
    to the repo).
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STAGES = [
    (3, "Task3_NLP_Preprocessing", "preprocess.py"),
    (4, "Task4_Skill_Extraction_Feature_Engineering", "skill_extraction.py"),
    (5, "Task5_Hiring_Trend_Analysis", "trend_analysis.py"),
    (6, "Task6_Competitor_Comparison", "compare.py"),
    (7, "Task7_Demand_Forecasting", "forecasting.py"),
    (8, "Task8_Company_Similarity_Scoring", "similarity_scoring.py"),
    (9, "Task9_Insight_Generation_Reporting", "generate_dashboard.py"),
]


def run_stage(task_num: int, folder: str, script: str) -> float:
    cwd = ROOT / folder
    print(f"\n{'=' * 60}\nTask {task_num}: {folder}/{script}\n{'=' * 60}")
    start = time.time()
    result = subprocess.run([sys.executable, script], cwd=cwd)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"\nSTAGE FAILED: Task {task_num} ({folder}/{script}) exited with code {result.returncode}.")
        print("Pipeline stopped -- fix the failing stage before rerunning (downstream stages were not run, so no stale output was produced).")
        sys.exit(result.returncode)
    print(f"Task {task_num} completed in {elapsed:.1f}s")
    return elapsed


def main():
    parser = argparse.ArgumentParser(description="Run the Task 3-9 pipeline end to end.")
    parser.add_argument("--from", dest="from_task", type=int, default=3, help="Resume from this task number (default: 3, i.e. run everything)")
    args = parser.parse_args()

    pipeline_start = time.time()
    run_stages = [s for s in STAGES if s[0] >= args.from_task]
    if not run_stages:
        print(f"No stages match --from {args.from_task} (valid range: 3-9)")
        sys.exit(1)

    print(f"Running Google hiring-intelligence pipeline: Task {run_stages[0][0]} -> Task {run_stages[-1][0]}")
    timings = {}
    for task_num, folder, script in run_stages:
        timings[task_num] = run_stage(task_num, folder, script)

    total = time.time() - pipeline_start
    print(f"\n{'=' * 60}\nPIPELINE COMPLETE in {total:.1f}s\n{'=' * 60}")
    for task_num, elapsed in timings.items():
        print(f"  Task {task_num}: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
