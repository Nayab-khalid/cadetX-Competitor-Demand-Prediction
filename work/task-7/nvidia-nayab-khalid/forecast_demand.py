#!/usr/bin/env python3
"""Task 7 demand forecasting - NVIDIA hiring demand.

Input :  work/task-5/.../nvidia_weekly_trend_<stamp>.csv
Output:  data/forecasts/*.csv, figures/*.png

What is being forecast, and the honest constraint
-------------------------------------------------
Two series come out of Task 5:

  open_roles   the stock of open postings, 12 observations, directly counted
  new_per_day  the arrival rate, 11 intervals, derived and gap-normalised

The team's shared config sets a 12-week forecast horizon. **The NVIDIA series has 12 observations.**
Forecasting a horizon as long as the entire history is not a modelling problem, it is a
data problem, and no choice of model fixes it. So this task does three things instead of pretending
otherwise:

1. Fits five simple models and backtests them properly, rather than fitting one complex model that
   cannot be evaluated. With 12 points, ARIMA order selection or Prophet's seasonality terms would
   be fitting noise; both need more data than exists here.
2. Reports the naive baseline alongside every model, because on a short flat series the naive
   forecast is genuinely hard to beat and a model that loses to it should be said to have lost.
3. Produces prediction intervals from backtest residuals, widening with horizon, and reports the
   12-week interval honestly even where it is uninformatively wide.

Usage:  python forecast_demand.py
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

ROOT = Path(__file__).resolve().parents[3]
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdcd8"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
HORIZON_WEEKS = 12          # from shared/config/analysis_config.yaml
HOLDOUT = 4                 # observations held back for backtesting

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_2, "text.color": INK,
    "xtick.color": INK_2, "ytick.color": INK_2, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
})


def style(ax, title, ylabel=""):
    ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(axis="y", alpha=0.9)
    ax.tick_params(length=0)
    return ax


# ------------------------------------------------------------------ the models
def f_naive(train, h):
    return np.repeat(train[-1], h)


def f_mean3(train, h):
    return np.repeat(np.mean(train[-3:]), h)


def f_drift(train, h):
    if len(train) < 2:
        return f_naive(train, h)
    slope = (train[-1] - train[0]) / (len(train) - 1)
    return train[-1] + slope * np.arange(1, h + 1)


def f_ses(train, h):
    try:
        return SimpleExpSmoothing(np.asarray(train, float),
                                  initialization_method="estimated").fit().forecast(h)
    except Exception:
        return f_naive(train, h)


def f_holt(train, h):
    try:
        return ExponentialSmoothing(np.asarray(train, float), trend="add", seasonal=None,
                                    initialization_method="estimated").fit().forecast(h)
    except Exception:
        return f_drift(train, h)


MODELS = {"Naive (last value)": f_naive, "Mean of last 3": f_mean3, "Drift": f_drift,
          "Simple exponential smoothing": f_ses, "Holt linear trend": f_holt}


def backtest(series: np.ndarray, holdout: int) -> pd.DataFrame:
    """Expanding-origin one-step-ahead backtest over the final `holdout` observations."""
    rows = []
    for name, fn in MODELS.items():
        errs = []
        for i in range(len(series) - holdout, len(series)):
            pred = fn(series[:i], 1)[0]
            errs.append(pred - series[i])
        errs = np.array(errs, float)
        actual = series[-holdout:]
        rows.append({"model": name,
                     "MAE": round(np.mean(np.abs(errs)), 2),
                     "MAPE_pct": round(np.mean(np.abs(errs / actual)) * 100, 2),
                     "bias": round(np.mean(errs), 2),
                     "residual_sd": round(np.std(errs, ddof=0), 2)})
    return pd.DataFrame(rows).sort_values("MAE").reset_index(drop=True)


def forecast_series(series, dates, label, unit, figs, out, fname_stem, weekly_step=7):
    print(f"\n--- {label} ---")
    s = np.asarray(series, float)
    bt = backtest(s, HOLDOUT)
    print(bt.to_string(index=False))
    best = bt.iloc[0]
    fn = MODELS[best.model]
    point = fn(s, HORIZON_WEEKS)

    # Interval from backtest residual spread, widened with the square root of the horizon.
    sd = max(best.residual_sd, 1e-9)
    z = 1.2816                                           # 80%, matching the shared config
    steps = np.arange(1, HORIZON_WEEKS + 1)
    half = z * sd * np.sqrt(steps)
    last = dates[-1]
    fdates = [last + timedelta(days=int(weekly_step * i)) for i in steps]

    fc = pd.DataFrame({"date": [d.isoformat() for d in fdates],
                       "weeks_ahead": steps,
                       "forecast": point.round(2),
                       "lower_80": (point - half).round(2),
                       "upper_80": (point + half).round(2)})
    fc.to_csv(out / f"{fname_stem}_forecast.csv", index=False, encoding="utf-8")
    bt.to_csv(out / f"{fname_stem}_backtest.csv", index=False, encoding="utf-8")
    print(f"chosen: {best.model} | 12-week point {point[-1]:.1f} "
          f"[{point[-1] - half[-1]:.1f}, {point[-1] + half[-1]:.1f}]")

    fig, ax = plt.subplots(figsize=(9, 4.2))
    hx = matplotlib.dates.date2num(dates)
    fx = matplotlib.dates.date2num(fdates)
    ax.plot(hx, s, color=SERIES[0], linewidth=2, marker="o", markersize=5,
            markeredgecolor=SURFACE, markeredgewidth=1.2, label="observed")
    ax.plot(np.r_[hx[-1], fx], np.r_[s[-1], point], color=SERIES[1], linewidth=2,
            linestyle=(0, (5, 3)), marker="o", markersize=4, label=f"forecast ({best.model})")
    ax.fill_between(fx, point - half, point + half, color=SERIES[1], alpha=0.16,
                    linewidth=0, label="80% interval")
    style(ax, f"{label}: observed and 12-week forecast", unit)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK_2, loc="upper left")
    ax.axvline(hx[-1], color=INK_2, linewidth=0.8, linestyle=(0, (2, 3)), alpha=0.6)
    ax.annotate("forecast starts", (hx[-1], ax.get_ylim()[1]), textcoords="offset points",
                xytext=(4, -12), fontsize=7.5, color=INK_2)
    # The axis holds date2num values, so it must be told it is a date axis or the ticks render
    # as raw ordinals (20600, 20625, ...).
    ax.xaxis_date()
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b"))
    for lbl in ax.get_xticklabels():
        lbl.set_rotation(45); lbl.set_ha("right"); lbl.set_fontsize(8)
    fig.tight_layout(); fig.savefig(figs / f"{fname_stem}_forecast.png", dpi=200); plt.close(fig)
    return bt, fc, best


def main() -> int:
    out = Path("data/forecasts"); out.mkdir(parents=True, exist_ok=True)
    figs = Path("figures"); figs.mkdir(parents=True, exist_ok=True)

    src = sorted((ROOT / "work/task-5/nvidia-nayab-khalid/data/trends")
                 .glob("nvidia_weekly_trend_*.csv"))[-1]
    print(f"1. reading {src.name}")
    t = pd.read_csv(src)
    dates = [date.fromisoformat(d) for d in t.observation_date]
    print(f"   {len(t)} observations, {dates[0]} to {dates[-1]}")
    print(f"   horizon {HORIZON_WEEKS} weeks against {len(t)} observations of history")

    bt1, fc1, best1 = forecast_series(t.open_roles.values, dates, "Open roles",
                                      "open roles", figs, out, "open_roles")

    flow = t.dropna(subset=["new_per_day"])
    fdates = [date.fromisoformat(d) for d in flow.observation_date]
    bt2, fc2, best2 = forecast_series(flow.new_per_day.values, fdates, "New postings per day",
                                      "postings per day", figs, out, "new_per_day")

    # ---- model comparison figure, open roles
    fig, ax = plt.subplots(figsize=(9, 3.6))
    b = bt1.sort_values("MAE", ascending=True)
    y = np.arange(len(b))
    cols = [SERIES[2] if m == best1.model else SERIES[0] for m in b.model]
    ax.barh(y, b.MAE, color=cols, height=0.6)
    ax.set_yticks(y); ax.set_yticklabels(b.model, fontsize=8.5)
    ax.invert_yaxis()
    for yi, v in enumerate(b.MAE):
        ax.text(v + 0.25, yi, f"{v:.2f}", va="center", fontsize=8.5, color=INK, fontweight="bold")
    style(ax, "Backtest error on the last 4 observations, open roles", "")
    ax.set_xlabel("mean absolute error (open roles)", fontsize=8.5)
    ax.grid(axis="x", alpha=0.9); ax.grid(axis="y", visible=False)
    ax.set_xlim(0, b.MAE.max() * 1.25)
    fig.tight_layout(); fig.savefig(figs / "backtest_open_roles.png", dpi=200); plt.close(fig)

    summary = pd.DataFrame({
        "series": ["open_roles", "new_per_day"],
        "observations": [len(t), len(flow)],
        "chosen_model": [best1.model, best2.model],
        "backtest_MAE": [best1.MAE, best2.MAE],
        "backtest_MAPE_pct": [best1.MAPE_pct, best2.MAPE_pct],
        "naive_MAE": [bt1[bt1.model.str.startswith("Naive")].MAE.iloc[0],
                      bt2[bt2.model.str.startswith("Naive")].MAE.iloc[0]],
        "forecast_12w": [fc1.forecast.iloc[-1], fc2.forecast.iloc[-1]],
        "lower_80_12w": [fc1.lower_80.iloc[-1], fc2.lower_80.iloc[-1]],
        "upper_80_12w": [fc1.upper_80.iloc[-1], fc2.upper_80.iloc[-1]],
    })
    summary.to_csv(out / "forecast_summary.csv", index=False, encoding="utf-8")
    print("\n--- summary ---")
    print(summary.to_string(index=False))
    print("\n4-week view (more defensible than 12):")
    print(fc1[fc1.weeks_ahead <= 4].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
