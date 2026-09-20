#!/usr/bin/env python3
"""Task 5 hiring trend analysis - NVIDIA job postings.

Input :  work/task-3/.../nvidia_postings_clean_<stamp>.csv   (postings + observed_dates)
         work/task-4/.../nvidia_skills_long_<stamp>.csv      (skills per posting)
Output:  data/trends/nvidia_weekly_trend_<stamp>.csv         the main trend table
         data/trends/nvidia_category_mix_<stamp>.csv         skill category x observation
         data/trends/nvidia_lifespan_<stamp>.csv             how long postings stay open
         figures/*.png                                        four figures

Method
------
Three properties of the Task 2 data decide how this is computed:

1. **The observation gaps are uneven.** 7, 21, 14, 7, 7, 21, 7, 7, 8, 7 and 6 days, because seven
   partial scrapes were excluded. Counting arrivals per observation would make the weeks that
   follow a gap look like hiring spikes. Every flow is therefore reported **per day**, and the
   per-observation counts are kept beside them so the normalisation is visible rather than hidden.

2. **The stock is observed, the flows are derived.** Open roles on a date is a direct count from
   that day's snapshot. New and closed are set differences between consecutive snapshots, so they
   inherit any gap in between. Where the two disagree, the stock is the more trustworthy series.

3. **Both ends are censored.** Postings already open at the first observation are stamped with that
   date (395 of 1,745), so arrivals in the first period are not arrivals. Postings still open at
   the last observation have no end date. The first period is dropped from flow analysis, and
   lifespans are split into completed and still-open rather than averaged together.

Usage:  python analyse_trends.py
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---- design tokens: the validated categorical palette, light mode (see dataviz/palette.md)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dcdcd8"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_2, "text.color": INK,
    "xtick.color": INK_2, "ytick.color": INK_2, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
})


def style(ax, title, ylabel):
    ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=12)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(axis="y", alpha=0.9)
    ax.tick_params(length=0)
    return ax


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean", default=None)
    ap.add_argument("--skills", default=None)
    args = ap.parse_args()

    clean_p = Path(args.clean) if args.clean else sorted(
        Path("../../task-3/nvidia-nayab-khalid/data/processed").glob("nvidia_postings_clean_*.csv"))[-1]
    skills_p = Path(args.skills) if args.skills else sorted(
        Path("../../task-4/nvidia-nayab-khalid/data/features").glob("nvidia_skills_long_*.csv"))[-1]
    stamp = re.search(r"(\d{8})", clean_p.name).group(1)

    out = Path("data/trends"); out.mkdir(parents=True, exist_ok=True)
    figs = Path("figures"); figs.mkdir(parents=True, exist_ok=True)

    print(f"1. reading {clean_p.name} and {skills_p.name}")
    df = pd.read_csv(clean_p)
    skills = pd.read_csv(skills_p)
    df["obs"] = df.observed_dates.map(json.loads)
    observations = sorted({o for lst in df.obs for o in lst})
    print(f"   {len(df)} postings | {len(observations)} observations "
          f"{observations[0]} to {observations[-1]}")

    # ------------------------------------------------------------------ the trend table
    print("2. building the weekly trend table")
    present = {o: set(df.job_id[df.obs.map(lambda l, o=o: o in l)]) for o in observations}
    rows, prev = [], None
    for i, o in enumerate(observations):
        ids = present[o]
        gap = (date.fromisoformat(o) - date.fromisoformat(observations[i - 1])).days if i else None
        new = len(ids - prev) if prev is not None else None
        closed = len(prev - ids) if prev is not None else None
        rows.append({
            "observation_date": o,
            "iso_week": date.fromisoformat(o).strftime("%G-W%V"),
            "days_since_previous": gap,
            "open_roles": len(ids),
            "new_postings": new,
            "closed_postings": closed,
            "net_change": (len(ids) - len(prev)) if prev is not None else None,
            "new_per_day": round(new / gap, 2) if new is not None else None,
            "closed_per_day": round(closed / gap, 2) if closed is not None else None,
            "net_per_day": round((new - closed) / gap, 2) if new is not None else None,
        })
        prev = ids
    trend = pd.DataFrame(rows)
    # Rolling mean over the flow series only; the first period is censored, so it is excluded.
    trend["new_per_day_rolling3"] = trend.new_per_day.rolling(3, min_periods=2).mean().round(2)
    trend.to_csv(out / f"nvidia_weekly_trend_{stamp}.csv", index=False, encoding="utf-8")
    print(f"   wrote {out / f'nvidia_weekly_trend_{stamp}.csv'}")

    flow = trend.dropna(subset=["new_per_day"]).copy()

    # ------------------------------------------------------------------ category mix
    print("3. building the skill category mix over time")
    first_seen = df.set_index("job_id").posting_date
    skills = skills.copy()
    skills["observation"] = skills.job_id.map(first_seen)
    top_cats = skills.skill_category.value_counts().head(5).index.tolist()
    skills["cat"] = np.where(skills.skill_category.isin(top_cats), skills.skill_category, "other")
    mix = (skills.groupby(["observation", "cat"]).size().unstack(fill_value=0)
           .reindex(observations, fill_value=0))
    order = top_cats + ["other"]
    mix = mix[[c for c in order if c in mix.columns]]
    mix_share = mix.div(mix.sum(axis=1).replace(0, np.nan), axis=0).round(4)
    mix.to_csv(out / f"nvidia_category_mix_{stamp}.csv", encoding="utf-8")
    print(f"   wrote {out / f'nvidia_category_mix_{stamp}.csv'}")

    # ------------------------------------------------------------------ lifespan
    print("4. measuring how long postings stay open")
    d = df.copy()
    d["first"] = pd.to_datetime(d.first_seen)
    d["last"] = pd.to_datetime(d.last_seen)
    d["span_days"] = (d["last"] - d["first"]).dt.days
    completed = d[(d.job_status == "closed") & (d.posting_date != observations[0])]
    still_open = d[d.job_status == "active"]
    buckets = [0, 7, 14, 28, 56, 999]
    labels = ["<= 1 week", "1-2 weeks", "2-4 weeks", "4-8 weeks", "8+ weeks"]
    life = (pd.cut(completed.span_days, bins=buckets, labels=labels, right=True,
                   include_lowest=True).value_counts().reindex(labels).rename("postings")
            .reset_index())
    life.columns = ["bucket", "postings"]          # the index column is named by the source series
    life["share"] = (life.postings / life.postings.sum()).round(3)
    life.to_csv(out / f"nvidia_lifespan_{stamp}.csv", index=False, encoding="utf-8")
    print(f"   wrote {out / f'nvidia_lifespan_{stamp}.csv'}")

    # ================================================================== figures
    print("5. drawing figures")
    # True date positions, not an evenly spaced index: the gaps run from 6 to 21 days, and
    # spacing them equally would misrepresent the time axis.
    xdates = [date.fromisoformat(o) for o in observations]
    x = matplotlib.dates.date2num(xdates)
    labels_x = [d.strftime("%d %b") for d in xdates]

    # -- 1. open roles: one series, so no legend; the title names it
    fig, ax = plt.subplots(figsize=(9, 4.0))
    ax.plot(x, trend.open_roles, color=SERIES[0], linewidth=2, marker="o", markersize=6,
            markeredgecolor=SURFACE, markeredgewidth=1.5)
    style(ax, "NVIDIA open roles per observation", "open roles")
    ax.set_xticks(x); ax.set_xticklabels(labels_x, rotation=45, ha="right", fontsize=8)
    # Focused range, not zero-based: the series sits in a 38-role band and a zero baseline would
    # flatten it to a straight line. The axis start is stated on the chart so it cannot mislead.
    lo, hi = trend.open_roles.min(), trend.open_roles.max()
    ax.set_ylim(lo - 25, hi + 22)
    for i in (0, int(trend.open_roles.idxmax()), len(trend) - 1):
        ax.annotate(f"{trend.open_roles[i]}", (x[i], trend.open_roles[i]),
                    textcoords="offset points", xytext=(0, 11), ha="center", fontsize=9,
                    color=INK, fontweight="bold")
    ax.axhline(trend.open_roles.mean(), color=INK_2, linewidth=1, linestyle=(0, (4, 3)), alpha=0.7)
    ax.annotate(f"mean {trend.open_roles.mean():.0f}", (x[0], trend.open_roles.mean()),
                textcoords="offset points", xytext=(6, 6), ha="left", fontsize=8, color=INK_2)
    ax.annotate("y-axis starts at %d, not zero; the full range is %d to %d"
                % (lo - 25, lo, hi), xy=(0, -0.30), xycoords="axes fraction",
                fontsize=7.5, color=INK_2)
    fig.tight_layout(); fig.savefig(figs / "fig1_open_roles.png", dpi=200); plt.close(fig)

    # -- 2. flows per day: two series, legend + direct labels
    fig, ax = plt.subplots(figsize=(9, 4.0))
    fdates = [date.fromisoformat(o) for o in flow.observation_date]
    fx = matplotlib.dates.date2num(fdates)
    ax.plot(fx, flow.new_per_day, color=SERIES[0], linewidth=2, marker="o", markersize=6,
            markeredgecolor=SURFACE, markeredgewidth=1.5, label="new per day")
    ax.plot(fx, flow.closed_per_day, color=SERIES[1], linewidth=2, marker="s", markersize=6,
            markeredgecolor=SURFACE, markeredgewidth=1.5, label="closed per day")
    style(ax, "Hiring velocity: postings opened and closed per day", "postings per day")
    ax.set_xticks(fx)
    ax.set_xticklabels([d.strftime("%d %b") for d in fdates], rotation=45, ha="right", fontsize=8)
    ax.annotate("new", (fx[-1], flow.new_per_day.iloc[-1]), textcoords="offset points",
                xytext=(8, 0), color=SERIES[0], fontsize=9, fontweight="bold", va="center")
    ax.annotate("closed", (fx[-1], flow.closed_per_day.iloc[-1]), textcoords="offset points",
                xytext=(8, 0), color=SERIES[1], fontsize=9, fontweight="bold", va="center")
    ax.legend(frameon=False, loc="upper left", fontsize=9, labelcolor=INK_2)
    ax.set_xlim(fx[0] - 4, fx[-1] + 10)
    fig.tight_layout(); fig.savefig(figs / "fig2_velocity.png", dpi=200); plt.close(fig)

    # -- 3. category mix. Plotted as SHARE, not counts: raw counts are dominated by the censored
    #       first observation and by the two 21-day gaps, so a count chart would show the sampling
    #       pattern rather than the hiring mix. The censored observation is dropped outright.
    mix_plot = mix_share.drop(index=observations[0]).dropna(how="all") * 100
    fig, ax = plt.subplots(figsize=(9, 4.4))
    bottom = np.zeros(len(mix_plot))
    bx = np.arange(len(mix_plot))
    for i, c in enumerate(mix_plot.columns):
        vals = mix_plot[c].values
        ax.bar(bx, vals, bottom=bottom, color=SERIES[i % len(SERIES)],
               width=0.74, edgecolor=SURFACE, linewidth=2, label=c)
        for xi, (v, b) in enumerate(zip(vals, bottom)):
            if v >= 8:                                    # label only segments big enough to read
                ax.text(xi, b + v / 2, f"{v:.0f}", ha="center", va="center", fontsize=7.5,
                        color="white", fontweight="bold")
        bottom += vals
    style(ax, "Skill mix by category, share of mentions at each observation", "share of mentions (%)")
    ax.set_xticks(bx)
    ax.set_xticklabels([date.fromisoformat(o).strftime("%d %b") for o in mix_plot.index],
                       rotation=45, ha="right", fontsize=8)
    ax.legend(frameon=False, ncol=6, fontsize=8.5, loc="upper center",
              bbox_to_anchor=(0.5, -0.24), labelcolor=INK_2, handlelength=1.4,
              columnspacing=1.4)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    fig.tight_layout(); fig.savefig(figs / "fig3_category_mix.png", dpi=200); plt.close(fig)

    # -- 4. lifespan distribution
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.bar(life.bucket, life.postings, color=SERIES[0], width=0.6)
    style(ax, "How long a posting stayed open, completed postings only", "postings")
    for xi, v in enumerate(life.postings):
        ax.text(xi, v + life.postings.max() * 0.03, f"{int(v)}", ha="center", fontsize=9,
                color=INK, fontweight="bold")
    ax.set_ylim(0, life.postings.max() * 1.2)
    ax.tick_params(axis="x", labelsize=9)
    fig.tight_layout(); fig.savefig(figs / "fig4_lifespan.png", dpi=200); plt.close(fig)
    print(f"   wrote 4 figures to {figs}/")

    # ================================================================== summary
    print("\n--- summary for the trend note ---")
    print(f"observations            {len(trend)}  ({observations[0]} to {observations[-1]})")
    print(f"open roles              min {trend.open_roles.min()} max {trend.open_roles.max()} "
          f"mean {trend.open_roles.mean():.0f}")
    print(f"net change over window  {trend.open_roles.iloc[-1] - trend.open_roles.iloc[0]:+d} "
          f"({(trend.open_roles.iloc[-1]/trend.open_roles.iloc[0]-1)*100:+.1f}%)")
    print(f"new per day             min {flow.new_per_day.min():.1f} max {flow.new_per_day.max():.1f} "
          f"mean {flow.new_per_day.mean():.1f}")
    print(f"closed per day          min {flow.closed_per_day.min():.1f} max {flow.closed_per_day.max():.1f} "
          f"mean {flow.closed_per_day.mean():.1f}")
    slope = np.polyfit(np.arange(len(flow)), flow.new_per_day, 1)[0]
    print(f"trend in new/day        {slope:+.3f} per observation")
    print(f"\nlifespan (completed, n={int(life.postings.sum())}):\n{life.to_string(index=False)}")
    print(f"median completed span   {completed.span_days.median():.0f} days")
    print(f"still open at the end   {len(still_open)} postings, right-censored")
    print(f"\ntrend table:\n{trend.to_string(index=False)}")
    print(f"\ncategory share at first and last observation:")
    print(mix_share.iloc[[0, -1]].T.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
