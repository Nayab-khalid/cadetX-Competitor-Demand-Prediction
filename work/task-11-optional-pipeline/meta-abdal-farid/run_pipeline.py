"""
META hiring-intelligence pipeline — Task 11
Member: Abdal Farid

Runs each task's committed script in order. Stops on first failure.
Writes a timestamped log to runs/<UTC-time>/pipeline.log.

Note: Task 2 (collect.py) and Task 4 (extract_skills.py) are not
included because those stages were performed interactively / via
notebooks, and only their outputs are committed. The pipeline re-runs
from Task 3 onwards, using the committed raw and extracted CSVs as
inputs. This is documented in pipeline_design.md.
"""
import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

STAGES = [
    ("Task 3  Preprocessing",     "work/task-3/meta-abdal-farid/preprocess.py",          []),
    ("Task 5  Trend analysis",    "work/task-5/meta-abdal-farid/analyze_trends.py",      []),
    ("Task 6  Comparison",        "work/task-6/meta-abdal-farid/compare_skills.py",      []),
    ("Task 7  Forecast",          "work/task-7/meta-abdal-farid/forecast.py",            []),
    ("Task 8  Similarity",        "work/task-8/meta-abdal-farid/similarity.py",          []),
    ("Task 9  Insights",          "work/task-9/meta-abdal-farid/generate_insights.py",   []),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--with-collection", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN — stages that would execute:")
        for label, script, _ in STAGES:
            print(f"  [{label}] -> {script}")
        return

    run_dir = (ROOT / "work/task-11-optional-pipeline/meta-abdal-farid/runs"
               / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "pipeline.log"

    def log(msg):
        line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
        print(line)
        with log_path.open("a") as f:
            f.write(line + "\n")

    log(f"Pipeline start — {len(STAGES)} stages")
    t0 = time.time()

    for label, script_rel, extra in STAGES:
        script = ROOT / script_rel
        cmd = [sys.executable, str(script), *extra]

        log(f"▶ {label}: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, cwd=ROOT)
            log(f"✅ {label} OK")
        except subprocess.CalledProcessError as e:
            log(f"❌ {label} FAILED (exit {e.returncode}) — aborting")
            sys.exit(1)
        except FileNotFoundError:
            log(f"❌ {label} script not found: {script}")
            sys.exit(1)

    log(f"🎉 Pipeline finished in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
