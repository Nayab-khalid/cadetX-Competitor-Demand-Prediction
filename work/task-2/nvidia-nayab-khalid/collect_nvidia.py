#!/usr/bin/env python3
"""Task 2 collection script - NVIDIA job postings.

Source: Aramente/eu-tech-jobs on Hugging Face, licensed CC BY-4.0.
        https://huggingface.co/datasets/Aramente/eu-tech-jobs

The dataset publishes a daily snapshot of open roles for a curated list of technology
employers, including NVIDIA (company slug `nvidia-workday`, collected from NVIDIA's public
Workday feed by the dataset maintainer).

Design decisions, both recorded in the Data Collection Report:

1. The dataset also ships daily `diffs/`. They are NOT used. Across the whole dataset the diff
   stream carries `new`, `removed` and `changed` events, but for NVIDIA it carries only `new`:
   8,797 `new` events for 2,029 distinct postings, the same posting re-announced up to 18 times
   and never marked removed. Flows derived from it would be meaningless. Instead this script
   derives first_seen and last_seen from the snapshots themselves, which are consistent.

2. Snapshots are taken **weekly**, not daily. The team's shared analysis config uses ISO weekly
   buckets, and weekly sampling keeps the download to roughly 350 MB instead of 2.4 GB. Each
   snapshot is one observation of the stock of open roles.

3. NVIDIA's Workday feed exposes no posting date - `posted_at` is null on every NVIDIA row - so
   the first week a posting is observed is used as `posting_date`. It is a proxy, and postings
   already open at the first observation are left-censored. Both facts are reported.

Outputs, filtered to NVIDIA only:

  data/raw/nvidia_postings_raw_<YYYYMMDD>.csv       THE dataset: one row per distinct posting,
                                                   in the team schema
  data/derived/nvidia_weekly_series_<YYYYMMDD>.csv  an aggregate derived from it, kept for Task 5.
                                                   Not a second dataset - it can be rebuilt from
                                                   first_seen and last_seen in the file above.

Usage:  python collect_nvidia.py [--out-dir data/raw] [--work-dir .cache] [--every 7]
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

import pandas as pd

REPO = "https://huggingface.co/datasets/Aramente/eu-tech-jobs/resolve/main"
API = "https://huggingface.co/api/datasets/Aramente/eu-tech-jobs"
SLUG = "nvidia-workday"
COMPANY = "NVIDIA"

# Personal data must never reach the saved file - see the team legal rules.
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

# A snapshot whose NVIDIA count falls far below the median is a partial scrape, not a
# collapse in hiring. Such weeks are excluded from the series and reported.
PARTIAL_SCRAPE_RATIO = 0.6

SCHEMA = [
    "job_id", "company_name", "job_title", "job_description", "posting_date", "location",
    "job_url",
    "employment_type", "job_category", "seniority_level", "tech_stack_tags", "countries",
    "remote_policy", "salary_min", "salary_max", "salary_currency", "salary_period",
    "first_seen", "last_seen", "weeks_observed", "observed_dates", "job_status",
    "scraped_date",
    "company_industry", "source",
]


def fetch(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=240) as r, dest.open("wb") as fh:
        fh.write(r.read())
    return dest


def list_snapshot_dates() -> list[str]:
    with urllib.request.urlopen(API, timeout=90) as r:
        meta = json.load(r)
    dates = set()
    for s in meta.get("siblings", []):
        m = re.fullmatch(r"snapshots/(\d{4}-\d{2}-\d{2})/jobs\.parquet", s["rfilename"])
        if m:
            dates.add(m.group(1))
    return sorted(dates)


def pick_weekly(dates: list[str], every: int) -> list[str]:
    """Choose dates roughly `every` days apart, always keeping the first and the last."""
    parsed = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    chosen = [parsed[0]]
    for d in parsed[1:]:
        if (d - chosen[-1]).days >= every:
            chosen.append(d)
    if parsed[-1] not in chosen:
        chosen.append(parsed[-1])
    return [d.strftime("%Y-%m-%d") for d in chosen]


def redact(text: object) -> object:
    if not isinstance(text, str):
        return text
    return EMAIL_RE.sub("[email removed]", text)


def as_list_json(v: object) -> str:
    if v is None or isinstance(v, float):
        return ""
    if isinstance(v, str):
        return v
    try:
        return json.dumps([str(x) for x in v])
    except TypeError:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="data/raw")
    ap.add_argument("--work-dir", default=".cache")
    ap.add_argument("--every", type=int, default=7, help="days between snapshots")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache = Path(args.work_dir)
    stamp = date.today().strftime("%Y%m%d")

    print("1. listing daily snapshots")
    all_dates = list_snapshot_dates()
    dates = pick_weekly(all_dates, args.every)
    print(f"   {len(all_dates)} snapshots available, {all_dates[0]} to {all_dates[-1]}")
    print(f"   sampling {len(dates)} of them, roughly every {args.every} days")

    print("2. downloading and filtering to NVIDIA")
    frames = {}
    for i, d in enumerate(dates, 1):
        p = fetch(f"{REPO}/snapshots/{d}/jobs.parquet", cache / f"snap_{d}.parquet")
        df = pd.read_parquet(p)
        nv = df[df["company_slug"] == SLUG].copy()
        # The feed writes "" rather than null for fields it could not populate. Treat those as
        # missing so that coverage counts in the report are honest.
        for c in nv.columns:
            if nv[c].dtype == object:
                nv[c] = nv[c].map(lambda v: None if isinstance(v, str) and not v.strip() else v)
        frames[d] = nv
        print(f"   {i:>2}/{len(dates)}  {d}  {len(nv):>4} NVIDIA roles", flush=True)

    counts = pd.Series({d: len(f) for d, f in frames.items()})
    median = counts.median()
    partial = counts[counts < median * PARTIAL_SCRAPE_RATIO]
    if len(partial):
        print(f"\n   excluding {len(partial)} suspected partial scrape(s): "
              f"{', '.join(f'{d} ({n})' for d, n in partial.items())}")
        for d in partial.index:
            frames.pop(d)
    kept = sorted(frames)

    print("\n3. building the posting-level table")
    seen = []
    for d, f in frames.items():
        s = f[["id"]].copy()
        s["observed"] = d
        seen.append(s)
    seen = pd.concat(seen)
    life = seen.groupby("id")["observed"].agg(first_seen="min", last_seen="max",
                                              weeks_observed="nunique")
    # Exact presence, not just the span: postings can disappear and reappear between
    # observations, so first_seen..last_seen would overcount the open stock. Storing the
    # observation dates makes the weekly series exactly reconstructable from this one file.
    presence = seen.groupby("id")["observed"].agg(lambda v: json.dumps(sorted(set(v))))
    presence.name = "observed_dates"
    life = life.join(presence)

    # richest record per posting: the most recent snapshot it appeared in
    latest = pd.concat([f.assign(_obs=d) for d, f in frames.items()])
    latest = latest.sort_values("_obs").drop_duplicates("id", keep="last").set_index("id")
    df = latest.join(life)

    final_obs = kept[-1]
    out = pd.DataFrame(index=df.index)
    out["job_id"] = "nvidia_" + df.index.astype(str)
    out["company_name"] = COMPANY
    out["job_title"] = df["title"].astype(str).str.strip()
    out["job_description"] = df["description_md"].map(redact)
    out["posting_date"] = df["first_seen"]          # proxy: first week observed
    out["location"] = df["location"].fillna("").astype(str).str.strip()
    out["job_url"] = df["url"].astype(str)
    out["employment_type"] = ""
    out["job_category"] = df["role_family"].fillna("")
    out["seniority_level"] = df["seniority"].fillna("")
    out["tech_stack_tags"] = df["stack"].map(as_list_json)
    out["countries"] = df["countries"].map(as_list_json)
    out["remote_policy"] = df["remote_policy"].fillna("")
    for c in ("salary_min", "salary_max", "salary_currency", "salary_period"):
        out[c] = df[c].fillna("")
    out["first_seen"] = df["first_seen"]
    out["last_seen"] = df["last_seen"]
    out["weeks_observed"] = df["weeks_observed"]
    out["observed_dates"] = df["observed_dates"]
    out["job_status"] = (df["last_seen"] == final_obs).map({True: "active", False: "closed"})
    out["scraped_date"] = df["_obs"]
    out["company_industry"] = "Semiconductors and AI computing"
    out["source"] = "Aramente/eu-tech-jobs (CC BY-4.0), NVIDIA Workday feed"
    out = out[SCHEMA].sort_values(["posting_date", "job_id"]).reset_index(drop=True)

    postings_path = out_dir / f"nvidia_postings_raw_{stamp}.csv"
    out.to_csv(postings_path, index=False, encoding="utf-8")
    print(f"   wrote {postings_path}  ({len(out)} postings)")

    print("4. building the weekly series")
    rows = []
    prev: set[str] | None = None
    for d in kept:
        ids = set(frames[d]["id"])
        rows.append({
            "observation_date": d,
            "iso_week": datetime.strptime(d, "%Y-%m-%d").strftime("%G-W%V"),
            "open_roles": len(ids),
            "new_since_last": "" if prev is None else len(ids - prev),
            "closed_since_last": "" if prev is None else len(prev - ids),
            "net_change": "" if prev is None else len(ids) - len(prev),
        })
        prev = ids
    series = pd.DataFrame(rows)
    derived_dir = out_dir.parent / "derived"
    derived_dir.mkdir(parents=True, exist_ok=True)
    series_path = derived_dir / f"nvidia_weekly_series_{stamp}.csv"
    series.to_csv(series_path, index=False, encoding="utf-8")
    print(f"   wrote {series_path}  ({len(series)} observations)")

    print("\n--- summary for the Data Collection Report ---")
    print(f"observation window     {kept[0]} to {kept[-1]}  ({len(kept)} weekly observations)")
    print(f"distinct postings      {len(out)}")
    have_desc = out["job_description"].astype(str).str.len().gt(50).sum()
    print(f"with description text  {have_desc}  <-- the source carries none for NVIDIA")
    print(f"active / closed        {(out['job_status']=='active').sum()} / "
          f"{(out['job_status']=='closed').sum()}")
    print(f"open roles first/last  {series['open_roles'].iloc[0]} -> "
          f"{series['open_roles'].iloc[-1]}")
    for c in ("job_category", "seniority_level", "tech_stack_tags", "countries"):
        print(f"  {c:<16} populated on {out[c].astype(str).str.len().gt(2).sum():>5} of {len(out)}")
    print("\nweekly series:")
    print(series.to_string(index=False))
    print("\nseniority mix:\n" + out["seniority_level"].value_counts().to_string())
    print("\nrole families (top 10):\n" + out["job_category"].value_counts().head(10).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
