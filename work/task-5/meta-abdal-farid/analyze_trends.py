"""
Task 5 — Hiring Trend Analysis (META)
Member: Abdal Farid

Reads the Task 3 cleaned postings CSV, aggregates postings by ISO week
and calendar month within the config window (Sept 2025 – Aug 2026),
zero-fills empty buckets, computes velocity / cumulative / rolling
averages and share-of-total, then writes:

  - meta_trend_weekly_<stamp>.csv   (ISO weeks, zero-filled)
  - meta_trend_monthly_<stamp>.csv  (calendar months, zero-filled)
  - meta_trend_analysis_<stamp>.png (2-panel figure)

Run:
    python analyze_trends.py
    python analyze_trends.py --input ../task-3/meta-abdal-farid/meta_cleaned_20260906.csv
"""
import argparse
from datetime import date
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

# --- Config window (matches shared/config/analysis_config.yaml v0.1.0) ---
CONFIG_START = "2025-09-01"
CONFIG_END   = "2026-08-31"

# Candidate column names for the posting date in the Task 3 cleaned CSV
DATE_COL_CANDIDATES = [
    "posting_date", "date_posted", "posted_date", "date", "created_at",
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Task 5 — META hiring trend analysis")
    p.add_argument("--input", type=Path, default=None,
                   help="Cleaned postings CSV (Task 3 output)")
    p.add_argument("--outdir", type=Path, default=HERE,
                   help="Where to write the three outputs (default: script folder)")
    p.add_argument("--stamp", default=date.today().strftime("%Y%m%d"),
                   help="Date stamp for output filenames (YYYYMMDD)")
    p.add_argument("--window-start", default=CONFIG_START)
    p.add_argument("--window-end",   default=CONFIG_END)
    return p.parse_args()


def resolve_input(cli_path):
    """Pick a default input CSV if --input is not given."""
    if cli_path is not None:
        if not Path(cli_path).exists():
            raise SystemExit(f"--input not found: {cli_path}")
        return Path(cli_path)

    candidates = [
        HERE.parents[1] / "task-3" / "meta-abdal-farid" / "meta_cleaned_20260906.csv",
        HERE.parent / "meta_cleaned_20260906.csv",
    ]
    # Any meta_cleaned_*.csv under task-3/
    try:
        candidates += sorted(
            (HERE.parents[1] / "task-3").rglob("meta_cleaned_*.csv"),
            reverse=True,
        )
    except Exception:
        pass

    for c in candidates:
        if c.exists():
            return c

    raise SystemExit(
        "Could not locate the cleaned CSV. Pass --input explicitly.\n"
        "Tried:\n  " + "\n  ".join(str(c) for c in candidates)
    )


def find_date_col(df):
    for c in DATE_COL_CANDIDATES:
        if c in df.columns:
            return c
    for c in df.columns:                      # fallback: any column with 'date'
        if "date" in c.lower():
            return c
    raise SystemExit(
        f"No date column found. Tried: {DATE_COL_CANDIDATES}. "
        f"Available: {list(df.columns)}"
    )


def load_postings(path, start, end):
    df = pd.read_csv(path)
    date_col = find_date_col(df)

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    if getattr(df[date_col].dt, "tz", None) is not None:
        df[date_col] = df[date_col].dt.tz_localize(None)
    df[date_col] = df[date_col].dt.normalize()   # drop time component

    df = df.dropna(subset=[date_col])
    df = df[(df[date_col] >= start) & (df[date_col] <= end)].copy()
    return df, date_col


# --------------------------------------------------------------------------
# Aggregations
# --------------------------------------------------------------------------
def weekly_table(df, date_col, start, end):
    df = df.copy()
    # Monday of each posting's week (ISO weeks start Monday)
    df["week_start"] = df[date_col] - pd.to_timedelta(df[date_col].dt.weekday, unit="D")
    # %G = ISO year, %V = ISO week number -> "2025-W36"
    df["iso_week"] = df[date_col].dt.strftime("%G-W%V")

    counts = (df.groupby(["iso_week", "week_start"])
                .size().rename("velocity").reset_index())

    # Full grid of every Monday in the window
    mondays = pd.date_range(start, end, freq="W-MON")
    grid = pd.DataFrame({
        "week_start": mondays,
        "iso_week":   mondays.strftime("%G-W%V"),
    })
    grid = grid.merge(counts, on=["iso_week", "week_start"], how="left")
    grid["velocity"]   = grid["velocity"].fillna(0).astype(int)
    grid = grid.sort_values("week_start").reset_index(drop=True)

    grid["cumulative"]          = grid["velocity"].cumsum()
    grid["velocity_rolling_4w"] = (grid["velocity"]
                                   .rolling(4, min_periods=1)
                                   .mean()
                                   .round(2))

    return grid[["iso_week", "week_start", "velocity",
                 "cumulative", "velocity_rolling_4w"]]


def monthly_table(df, date_col, start, end):
    df = df.copy()
    df["month_start"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    df["month"]       = df[date_col].dt.strftime("%Y-%m")

    counts = (df.groupby(["month", "month_start"])
                .size().rename("velocity").reset_index())

    months = pd.date_range(start, end, freq="MS")   # month-start
    grid = pd.DataFrame({
        "month_start": months,
        "month":       months.strftime("%Y-%m"),
    })
    grid = grid.merge(counts, on=["month", "month_start"], how="left")
    grid["velocity"] = grid["velocity"].fillna(0).astype(int)
    grid = grid.sort_values("month_start").reset_index(drop=True)

    grid["cumulative"] = grid["velocity"].cumsum()
    total = grid["velocity"].sum()
    grid["share_of_total"] = (
        (grid["velocity"] / total * 100).round(1) if total else 0.0
    )

    return grid[["month", "month_start", "velocity",
                 "cumulative", "share_of_total"]]


# --------------------------------------------------------------------------
# Plot
# --------------------------------------------------------------------------
def plot_all(weekly, monthly, outpath):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # ---- Top panel: weekly velocity + 4-week rolling average ----
    ax1.bar(weekly["week_start"], weekly["velocity"], width=5,
            color="#5B9BD5", label="Weekly velocity (new postings)")
    ax1.plot(weekly["week_start"], weekly["velocity_rolling_4w"],
             color="#ED7D31", linewidth=2.5, marker="o", markersize=4,
             label="4-week rolling average")
    ax1.set_title(
        "Meta: Hiring Velocity by Week (Sep 2025 – Aug 2026)\n"
        "Raw counts + 4-week rolling average",
        fontsize=12, fontweight="bold",
    )
    ax1.set_xlabel("Week")
    ax1.set_ylabel("Postings per week")
    ax1.grid(axis="y", alpha=0.3)
    ax1.legend(loc="upper right")

    # annotate Feb-2026 spike
    spike = weekly.loc[weekly["velocity"].idxmax()]
    ax1.annotate(
        "Feb 2026 snapshot spike",
        xy=(spike["week_start"], spike["velocity"]),
        xytext=(spike["week_start"] + pd.Timedelta(days=40),
                spike["velocity"] + 4),
        arrowprops=dict(arrowstyle="->", color="red"),
        color="red", fontsize=10, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.35),
    )

    # shade March 2026 data gap
    gap_start = pd.Timestamp("2026-03-01")
    gap_end   = pd.Timestamp("2026-04-01")
    ax1.axvspan(gap_start, gap_end, color="grey", alpha=0.15)
    ax1.text(gap_start + (gap_end - gap_start) / 2,
             ax1.get_ylim()[1] * 0.55,
             "Data gap\n(March 2026)",
             ha="center", color="grey", fontsize=10, fontweight="bold")

    # ---- Bottom panel: cumulative + monthly share ----
    ax2b = ax2.twinx()
    ax2.plot(monthly["month_start"], monthly["cumulative"],
             color="#2E75B6", linewidth=2.5, marker="o", markersize=5,
             label="Cumulative postings")
    ax2b.bar(monthly["month_start"], monthly["share_of_total"],
             width=20, color="#F4B183", alpha=0.7,
             label="Monthly share of total (%)")
    ax2.set_title("Meta: Cumulative Postings + Monthly Share",
                  fontsize=12, fontweight="bold")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Cumulative postings", color="#2E75B6")
    ax2b.set_ylabel("Monthly share of total (%)", color="#ED7D31")
    ax2.tick_params(axis="y",  labelcolor="#2E75B6")
    ax2b.tick_params(axis="y", labelcolor="#ED7D31")
    ax2.grid(axis="y", alpha=0.3)

    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper left")

    for ax in (ax1, ax2):
        for lbl in ax.get_xticklabels():
            lbl.set_rotation(45)
            lbl.set_ha("right")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    args   = parse_args()
    start  = pd.Timestamp(args.window_start)
    end    = pd.Timestamp(args.window_end)
    infile = resolve_input(args.input)

    print(f"Reading: {infile}")
    df, date_col = load_postings(infile, start, end)
    print(f"  rows in window: {len(df)}  (date column: {date_col})")

    weekly  = weekly_table(df, date_col, start, end)
    monthly = monthly_table(df, date_col, start, end)

    wk_path  = args.outdir / f"meta_trend_weekly_{args.stamp}.csv"
    mo_path  = args.outdir / f"meta_trend_monthly_{args.stamp}.csv"
    png_path = args.outdir / f"meta_trend_analysis_{args.stamp}.png"

    weekly.to_csv(wk_path, index=False)
    monthly.to_csv(mo_path, index=False)
    plot_all(weekly, monthly, png_path)

    print(f"✅ {wk_path.name}  ({len(weekly)} weeks, "
          f"{int(weekly['velocity'].sum())} postings)")
    print(f"✅ {mo_path.name}  ({len(monthly)} months)")
    print(f"✅ {png_path.name}")


if __name__ == "__main__":
    main()
