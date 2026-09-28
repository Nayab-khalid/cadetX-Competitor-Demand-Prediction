"""
META hiring-intelligence pipeline — Task 11
Member: Abdal Farid
"""
import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

STAGES = [
    ("Task 2  Collection",        "work/task-2/meta-abdal-farid/collect.py",            []),
    ("Task 3  Preprocessing",     "work/task-3/meta-abdal-farid/preprocess.py",          []),
    ("Task 4  Skill extraction",  "work/task-4/meta-abdal-farid/extract_skills.py",      []),
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
               / datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "pipeline.log"

    def log(msg):
        line = f"[{datetime.utcnow().isoformat()}] {msg}"
        print(line)
        with log_path.open("a") as f:
            f.write(line + "\n")

    log(f"Pipeline start — {len(STAGES)} stages")
    t0 = time.time()

    for label, script_rel, extra in STAGES:
        script = ROOT / script_rel
        cmd = [sys.executable, str(script), *extra]

        if args.with_collection and "collect" in script.name:
            cmd.append("--with-collection")

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
