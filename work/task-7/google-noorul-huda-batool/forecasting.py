"""
Task 7 - Demand Forecasting
Author: Noor Ul Huda | Company track: Google

NOTE: forecasts are built on the SIMULATED posting_date calendar (see Task 3
limitation) -- they demonstrate the forecasting methodology, not a real
prediction of Google's future hiring. Swap in real time-stamped data and the
same code produces a real forecast.

Method: Holt's linear exponential smoothing (trend, no seasonal component).
Chosen over ARIMA because the series is short (24 monthly points) -- ARIMA
order selection (p,d,q) is unstable/overfits with that little data, while
Holt's method needs only a level+trend fit and is robust at this length.
Chosen over Prophet to avoid an extra heavy dependency for a 24-point series
where its seasonality/holiday machinery isn't needed.

Shared forecast horizon (aligned with the team): 6 months ahead.

Inputs:
  ../Task5_Hiring_Trend_Analysis/monthly_postings.csv
  ../Task5_Hiring_Trend_Analysis/category_monthly_trend.csv
  ../Task5_Hiring_Trend_Analysis/growth_summary.csv
  ../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv
  ../Task3_NLP_Preprocessing/cleaned_job_postings.csv
  (skill monthly series are recomputed here from extracted_skills.csv rather than
  read from Task 5's skill_monthly_trend.csv, since that file only carries the
  top-15 *globally* most-mentioned skills -- the fastest-*growing* skills picked
  from growth_summary.csv are often not in that top-15 by raw volume.)

Outputs:
  forecast_overall.csv
  forecast_by_category.csv   (top 3 growing categories from Task 5)
  forecast_by_skill.csv      (top 3 growing skills from Task 5)
  visuals/*.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

os.makedirs("visuals", exist_ok=True)

HORIZON = 6


def forecast_series(series: pd.Series, horizon: int = HORIZON):
    """Fit Holt's linear trend model; return (fitted, forecast) as pd.Series indexed by month."""
    series = series.asfreq("M", fill_value=0)
    model = ExponentialSmoothing(series, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated")
    fit = model.fit(optimized=True)
    fc = fit.forecast(horizon)
    fc = fc.clip(lower=0)
    return fit.fittedvalues, fc


def plot_forecast(actual, fitted, forecast, title, path):
    plt.figure(figsize=(10, 5))
    plt.plot(actual.index.astype(str), actual.values, marker="o", label="Actual")
    plt.plot(forecast.index.astype(str), forecast.values, marker="o", linestyle="--", color="red", label=f"Forecast (+{HORIZON}mo)")
    plt.xticks(rotation=90, fontsize=7)
    plt.title(title)
    plt.ylabel("Postings")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main():
    monthly = pd.read_csv("../Task5_Hiring_Trend_Analysis/monthly_postings.csv")
    monthly["year_month"] = pd.PeriodIndex(monthly["year_month"], freq="M")
    overall = monthly.set_index("year_month")["postings"]

    fitted, fc_overall = forecast_series(overall)
    out_overall = pd.DataFrame({
        "year_month": fc_overall.index.astype(str),
        "forecast_postings": fc_overall.values.round(1),
    })
    out_overall.to_csv("forecast_overall.csv", index=False)
    plot_forecast(overall, fitted, fc_overall, "Google — Overall Hiring Demand Forecast (Holt's linear trend)", "visuals/forecast_overall.png")

    growth = pd.read_csv("../Task5_Hiring_Trend_Analysis/growth_summary.csv")
    cat_monthly = pd.read_csv("../Task5_Hiring_Trend_Analysis/category_monthly_trend.csv")
    cat_monthly["year_month"] = pd.PeriodIndex(cat_monthly["year_month"], freq="M")

    cleaned = pd.read_csv("../Task3_NLP_Preprocessing/cleaned_job_postings.csv", parse_dates=["posting_date"])
    extracted = pd.read_csv("../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv")
    extracted = extracted.merge(cleaned[["job_id", "posting_date"]], on="job_id", how="left")
    extracted["posting_date"] = pd.to_datetime(extracted["posting_date"])
    extracted["year_month"] = extracted["posting_date"].dt.to_period("M")

    top_categories = growth[growth["signal_type"] == "category"].nlargest(3, "growth_pct")["name"].tolist()
    cat_forecast_rows = []
    for cat in top_categories:
        sub = cat_monthly[cat_monthly["Category"] == cat].set_index("year_month")["postings"]
        sub = sub.reindex(pd.period_range(overall.index.min(), overall.index.max(), freq="M"), fill_value=0)
        if sub.sum() < 8:
            continue  # too sparse to forecast meaningfully
        _, fc = forecast_series(sub)
        for ym, val in fc.items():
            cat_forecast_rows.append({"Category": cat, "year_month": str(ym), "forecast_postings": round(val, 1)})
    pd.DataFrame(cat_forecast_rows).to_csv("forecast_by_category.csv", index=False)

    top_skills = growth[growth["signal_type"] == "skill"].nlargest(3, "growth_pct")["name"].tolist()
    skill_monthly_all = extracted.groupby(["year_month", "skill"]).size().rename("mentions").reset_index()
    skill_forecast_rows = []
    for sk in top_skills:
        sub = skill_monthly_all[skill_monthly_all["skill"] == sk].set_index("year_month")["mentions"]
        sub = sub.reindex(pd.period_range(overall.index.min(), overall.index.max(), freq="M"), fill_value=0)
        if sub.sum() < 8:
            continue
        _, fc = forecast_series(sub)
        for ym, val in fc.items():
            skill_forecast_rows.append({"skill": sk, "year_month": str(ym), "forecast_mentions": round(val, 1)})
    pd.DataFrame(skill_forecast_rows).to_csv("forecast_by_skill.csv", index=False)

    plt.figure(figsize=(10, 5))
    for cat in top_categories:
        sub = cat_monthly[cat_monthly["Category"] == cat].set_index("year_month")["postings"]
        sub = sub.reindex(pd.period_range(overall.index.min(), overall.index.max(), freq="M"), fill_value=0)
        if sub.sum() < 8:
            continue
        plt.plot(sub.index.astype(str), sub.values, marker=".", label=f"{cat} (actual)")
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Google — Actuals for Top Growing Categories (forecast horizon: +6mo, see forecast_by_category.csv)")
    plt.ylabel("Postings")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("visuals/forecast_by_category.png", dpi=150)
    plt.close()

    print("=== Task 7 Summary ===")
    print(f"Forecast horizon: {HORIZON} months")
    print("\nOverall postings forecast:")
    print(out_overall.to_string(index=False))
    print(f"\nCategories forecasted: {top_categories}")
    print(f"Skills forecasted: {top_skills}")


if __name__ == "__main__":
    main()
