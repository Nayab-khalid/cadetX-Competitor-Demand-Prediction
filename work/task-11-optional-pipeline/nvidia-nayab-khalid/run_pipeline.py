#!/usr/bin/env python3
"""Optional Task: end-to-end pipeline for the NVIDIA workstream.

Chains every stage that produces a committed artefact:

    collect (Task 2) -> preprocess (Task 3) -> extract skills (Task 4)
                     -> trends (Task 5) -> compare (Task 6)
                     -> forecast (Task 7) -> similarity (Task 8)

Each stage is the task's own script, run unmodified in its own directory. Nothing is reimplemented
here, so the pipeline cannot drift away from what the tasks actually committed.

Design notes
------------
* **Collection is opt-in.** `--with-collection` re-downloads snapshots, which is slow and hits a
  third-party host. The default run starts from the committed raw dataset, so a routine run is
  fast and offline-safe.
* **Stages are skippable and resumable.** `--from` and `--only` let a failed run be restarted at
  the stage that failed rather than from the beginning.
* **A stage failure stops the pipeline** by default: Task 5 reading a half-written Task 3 output
  would produce numbers that look fine and are wrong. `--keep-going` overrides this deliberately.
* **Every run writes a manifest** recording which stages ran, how long each took, and the SHA-256
  of every output file, so two runs can be compared and a silent change in a third-party source
  shows up as a changed hash.

Usage:
    python run_pipeline.py                      # preprocess -> similarity, from committed data
    python run_pipeline.py --with-collection    # include the Task 2 download
    python run_pipeline.py --from trends        # resume from the trend stage
    python run_pipeline.py --only forecast      # a single stage
    python run_pipeline.py --dry-run            # print the plan and exit
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# stage name -> (working directory relative to repo root, script, description)
STAGES = [
    ("collect",    "work/task-2/nvidia-nayab-khalid",  "collect_nvidia.py",
     "Download weekly snapshots and build the raw dataset"),
    ("preprocess", "work/task-3/nvidia-nayab-khalid",  "preprocess_nvidia.py",
     "Normalise, parse title structure, tokenise"),
    ("skills",     "work/task-4/nvidia-nayab-khalid",  "extract_skills.py",
     "Match the shared taxonomy, build feature tables"),
    ("trends",     "work/task-5/nvidia-nayab-khalid",  "analyse_trends.py",
     "Weekly stock and flows, lifespan, category mix"),
    ("compare",    "work/task-6/nvidia-nayab-khalid",  "compare_companies.py",
     "Four-company comparison with the validity control"),
    ("forecast",   "work/task-7/nvidia-nayab-khalid",  "forecast_demand.py",
     "Backtest five models, forecast the shared horizon"),
    ("similarity", "work/task-8/nvidia-nayab-khalid",  "similarity.py",
     "Three similarity matrices and their disagreement"),
]
DEFAULT_SKIP = {"collect"}          # slow, network-bound, and rarely needs re-running


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def outputs_of(stage_dir: Path) -> dict[str, str]:
    """Hash every committed data and figure output under a stage directory."""
    out = {}
    for sub in ("data", "figures"):
        base = stage_dir / sub
        if not base.exists():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file() and f.suffix.lower() in {".csv", ".png", ".json"}:
                out[str(f.relative_to(ROOT)).replace("\\", "/")] = sha256(f)[:16]
    return out


def run_stage(name: str, rel_dir: str, script: str, python: str, keep_going: bool) -> dict:
    cwd = ROOT / rel_dir
    print(f"\n=== {name} : {script} ===", flush=True)
    started = time.time()
    proc = subprocess.run([python, script], cwd=cwd, capture_output=True, text=True)
    elapsed = round(time.time() - started, 1)
    tail = (proc.stdout or "").strip().splitlines()[-3:]
    for line in tail:
        print("   " + line)
    ok = proc.returncode == 0
    if not ok:
        print(f"   FAILED in {elapsed}s (exit {proc.returncode})")
        err = (proc.stderr or "").strip().splitlines()[-6:]
        for line in err:
            print("   ! " + line)
        if not keep_going:
            print("\nPipeline stopped. A later stage reading a half-written output would produce "
                  "numbers that look fine and are wrong. Re-run with --from " + name +
                  " once fixed, or --keep-going to override.")
    else:
        print(f"   ok in {elapsed}s")
    return {"stage": name, "script": script, "ok": ok, "seconds": elapsed,
            "returncode": proc.returncode, "outputs": outputs_of(cwd) if ok else {}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--with-collection", action="store_true",
                    help="include the Task 2 download stage (slow, hits a third-party host)")
    ap.add_argument("--from", dest="start", default=None, help="resume from this stage")
    ap.add_argument("--only", default=None, help="run a single stage")
    ap.add_argument("--keep-going", action="store_true", help="continue after a stage fails")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and exit")
    ap.add_argument("--python", default=sys.executable, help="interpreter to run the stages with")
    args = ap.parse_args()

    plan = [s for s in STAGES if args.with_collection or s[0] not in DEFAULT_SKIP]
    names = [s[0] for s in plan]
    if args.only:
        if args.only not in [s[0] for s in STAGES]:
            print(f"ERROR  unknown stage '{args.only}'. Known: {[s[0] for s in STAGES]}")
            return 2
        plan = [s for s in STAGES if s[0] == args.only]
    elif args.start:
        if args.start not in names:
            print(f"ERROR  cannot resume from '{args.start}'. Planned: {names}")
            return 2
        plan = plan[names.index(args.start):]

    print("CadetX NVIDIA pipeline")
    print(f"repo root : {ROOT}")
    print(f"python    : {args.python}")
    print(f"stages    : {' -> '.join(s[0] for s in plan)}")
    if not args.with_collection and not args.only:
        print("note      : collection skipped; starting from the committed raw dataset "
              "(use --with-collection to refresh it)")
    if args.dry_run:
        for n, d, s, desc in plan:
            print(f"  {n:<11} {d}/{s:<22} {desc}")
        return 0

    started = datetime.now(timezone.utc)
    results = []
    for name, rel_dir, script, _desc in plan:
        r = run_stage(name, rel_dir, script, args.python, args.keep_going)
        results.append(r)
        if not r["ok"] and not args.keep_going:
            break

    manifest = {
        "started_utc": started.isoformat(timespec="seconds"),
        "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_seconds": round(sum(r["seconds"] for r in results), 1),
        "python": args.python,
        "stages_planned": [s[0] for s in plan],
        "collection_included": bool(args.with_collection),
        "results": results,
    }
    mdir = Path(__file__).parent / "runs"
    mdir.mkdir(exist_ok=True)
    stamp = started.strftime("%Y%m%dT%H%M%SZ")
    (mdir / f"manifest_{stamp}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (Path(__file__).parent / "last_run.json").write_text(json.dumps(manifest, indent=2),
                                                         encoding="utf-8")

    ok = all(r["ok"] for r in results)
    n_out = sum(len(r["outputs"]) for r in results)
    print(f"\n{'PASSED' if ok else 'FAILED'} - {sum(r['ok'] for r in results)}/{len(results)} "
          f"stages, {manifest['total_seconds']}s, {n_out} output files hashed")
    print(f"manifest: runs/manifest_{stamp}.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
