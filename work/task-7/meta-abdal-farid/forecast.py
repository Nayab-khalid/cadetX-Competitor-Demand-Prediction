"""
Task 7 — Demand Forecasting (META)
Member: Abdal Farid

Reads Task 5's weekly trend CSV, fits exponential smoothing (alpha=0.3),
runs an 8-week backtest, and forecasts 12 weeks ahead with an 80%
prediction interval. Writes:

  - meta_forecast_12week_<stamp>.csv
  - meta_forecast_12week_<stamp>.png

Run:
    python forecast.py
    python forecast.py --stamp 20260927
"""
import argparse
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

# --- Model / horizon config (matches the method note) ----------------------
ALPHA   = 0.3        # exponential smoothing parameter
HORIZON = 12         # weeks to forecast
HOLDOUT = 8          # weeks held out for the backtest
Z_80    = 1.282      # z-multiplier for an 80% prediction interval

# --- Plot colours -----------------------------------------------------------
HIST_COLOR = "#4A90E2"
FORE_COLOR = "#E74C3C"
BAND_COLOR = "#F5B7B1"


# ---------------------------------------------------------------------------
# CLI / input
# ---------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Task 7 — META demand forecast")
    p.add_argument("--input",  type=Path, default=None,
                   help="Task 5 weekly trend CSV")
    p.add_argument("--outdir", type=Path, default=HERE,
                   help="Where to write the two outputs")
    p.add_argument("--stamp",  default=date.today().strftime("%Y%m%d"),
                   help="Date stamp for output filenames (YYYYMMDD)")
    return p.parse_args()


def resolve_input(cli_path):
    if cli_path is not None:
        if Path(cli_path).exists():
            return Path(cli_path)
        raise SystemExit(f"--input not found: {cli_path}")

    t5 = HERE.parents[1] / "task-5" / "meta-abdal-farid"
    for pat in ("meta_trend_weekly_*.csv", "*trend_weekly*.csv", "*weekly*.csv"):
        cands = sorted(t5.glob(pat), reverse=True)
        if cands:
            return cands[0]
    # fallback: sibling of the script
    for p in sorted(HERE.glob("meta_trend_weekly_*.csv"), reverse=True):
        return p
    raise SystemExit(f"Could not find Task 5 weekly CSV under {t5}")


def load_weekly(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    if "week_start" not in df.columns or "velocity" not in df.columns:
        raise SystemExit(
            f"Expected 'week_start' and 'velocity' columns. "
            f"Got: {list(df.columns)}"
        )
    df["week_start"] = pd.to_datetime(df["week_start"])
    return df.sort_values("week_start").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def exp_smoothing(x, alpha):
    """Manual exponential smoothing: S[0] = x[0]; S[t] = a*x[t] + (1-a)*S[t-1]."""
    s = np.empty_like(x, dtype=float)
    s[0] = x[0]
    for t in range(1, len(x)):
        s[t] = alpha * x[t] + (1 - alpha) * s[t - 1]
    return s


def fit(train_x, alpha, z):
    smoothed  = exp_smoothing(train_x, alpha)
    residuals = train_x - smoothed

    point     = float(smoothed[-1])
    resid_std = float(residuals.std(ddof=1))     # pandas default

    lower = max(0.0, point - z * resid_std)
    upper = point + z * resid_std

    return {
        "smoothed":  smoothed,
        "residuals": residuals,
        "resid_std": resid_std,
        "point":     point,
        "lower":     lower,
        "upper":     upper,
    }


def backtest(train_x, test_x, alpha):
    """Flat forecast from the model fitted on train_x, evaluated on test_x."""
    f    = fit(train_x, alpha, Z_80)
    pred = np.full(len(test_x), f["point"], dtype=float)
    mae  = float(np.mean(np.abs(test_x - pred)))
    return pred, mae


# ---------------------------------------------------------------------------
# Output frames
# ---------------------------------------------------------------------------
def build_forecast_df(last_week_start, f, horizon):
    rows = []
    for i in range(1, horizon + 1):
        ws = last_week_start + pd.Timedelta(days=7 * i)
        rows.append({
            "week_start":        ws.date(),
            "iso_week":          ws.strftime("%G-W%V"),
            "forecast_point":    f["point"],
            "forecast_lower_80": f["lower"],
            "forecast_upper_80": f["upper"],
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
def plot_forecast(hist_df, forecast_df, split_date, outpath):
    fig, ax = plt.subplots(figsize=(16, 8))

    hx = hist_df["week_start"]
    hy = hist_df["velocity"].astype(float)

    # Historical line + soft fill
    ax.plot(hx, hy, color=HIST_COLOR, linewidth=1.6,
            marker="o", markersize=3.5,
            label="Actual postings (historical)")
    ax.fill_between(hx, 0, hy, color=HIST_COLOR, alpha=0.15)

    # Train / forecast split line
    ax.axvline(split_date, color="grey", linestyle="--", linewidth=1.4,
               label="Train/forecast split")

    # Forecast band + line
    fx = pd.to_datetime(forecast_df["week_start"])
    fy = forecast_df["forecast_point"]

    ax.fill_between(fx,
                    forecast_df["forecast_lower_80"],
                    forecast_df["forecast_upper_80"],
                    color=BAND_COLOR, alpha=0.55,
                    label="80% prediction interval")
    ax.plot(fx, fy, color=FORE_COLOR, linewidth=3,
            marker="s", markersize=6,
            label=f"Forecast (exp smoothing α={ALPHA})")

    # Data-quality warning (top-left)
    ax.text(0.01, 0.97,
            "⚠ Data Quality Warning:\n"
            "Snapshots dominate (Feb 2026: 58% of data). Forecast is unreliable.",
            transform=ax.transAxes, va="top", ha="left",
            fontsize=10, fontweight="bold", color="red",
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="lightyellow", edgecolor="red"))

    # Split annotation (top-right)
    ax.text(0.78, 0.90, "← Training Data  |  Forecast →",
            transform=ax.transAxes, ha="center", fontsize=10, color="grey",
            bbox=dict(boxstyle="round,pad=0.35",
                      facecolor="white", edgecolor="grey"))

    ax.set_title(
        "Meta: 12-Week Hiring Demand Forecast\n"
        "(September 2025 – August 2026 historical + 12-week forecast)",
        fontsize=13, fontweight="bold",
    )
    ax.set_xlabel("Week", fontsize=11)
    ax.set_ylabel("Postings per week", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(loc="upper right", fontsize=10)

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    args   = parse_args()
    infile = resolve_input(args.input)
    print(f"Reading: {infile}")

    df = load_weekly(infile)
    x  = df["velocity"].to_numpy(dtype=float)
    n  = len(x)

    if n <= HOLDOUT + 4:
        raise SystemExit(f"Not enough history: {n} rows, need > {HOLDOUT + 4}")

    train_x  = x[:-HOLDOUT]
    test_x   = x[-HOLDOUT:]
    train_df = df.iloc[:-HOLDOUT].copy()

    # Fit on the full training window
    f = fit(train_x, ALPHA, Z_80)

    # Backtests
    _, bt_mae = backtest(train_x, test_x, ALPHA)
    naive_pred = np.full_like(test_x, train_x[-1], dtype=float)
    naive_mae  = float(np.mean(np.abs(test_x - naive_pred)))

    print(f"  training weeks: {len(train_x)}   holdout weeks: {len(test_x)}")
    print(f"  point forecast: {f['point']:.6f}   "
          f"80% PI: [{f['lower']:.6f}, {f['upper']:.6f}]")
    print(f"  residual std:   {f['resid_std']:.6f}")
    print(f"  backtest MAE:   exp-smoothing={bt_mae:.4f}   naive={naive_mae:.4f}")

    # Forecast horizon
    last_week_start = df["week_start"].iloc[-1]
    forecast_df     = build_forecast_df(last_week_start, f, HORIZON)

    csv_path = args.outdir / f"meta_forecast_12week_{args.stamp}.csv"
    png_path = args.outdir / f"meta_forecast_12week_{args.stamp}.png"

    forecast_df.to_csv(csv_path, index=False)
    plot_forecast(df, forecast_df,
                  split_date=train_df["week_start"].iloc[-1],
                  outpath=png_path)

    print(f"\n✅ {csv_path.name}  ({len(forecast_df)} weeks)")
    print(f"✅ {png_path.name}")


if __name__ == "__main__":
    main()
