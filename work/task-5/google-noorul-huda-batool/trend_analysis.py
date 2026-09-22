"""
Task 5 - Hiring Trend Analysis
Author: Noor Ul Huda | Company track: Google

NOTE: posting_date in the input files is a SIMULATED field (see Task 3 README /
Limitation section) — the Google Job Skills dataset has no real posting-date
field. Monthly counts here demonstrate the trend-analysis methodology on a
reproducible synthetic calendar; they are not real Google hiring velocity.

Inputs:
  ../Task3_NLP_Preprocessing/cleaned_job_postings.csv
  ../Task4_Skill_Extraction_Feature_Engineering/skill_features.csv
  ../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv

Outputs (tables):
  monthly_postings.csv          overall postings per month + 3-mo rolling avg + MoM growth %
  category_monthly_trend.csv    postings per Category per month
  skill_monthly_trend.csv       mentions per skill per month (top 15 skills only)
  seasonal_month_of_year.csv    postings aggregated by calendar month (seasonality view)
  growth_summary.csv            first-half vs second-half comparison -> growing/declining categories & skills

Outputs (visuals, in ./visuals):
  overall_hiring_trend.png, category_trend.png, top_skills_trend.png, seasonal_heatmap.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("visuals", exist_ok=True)
plt.rcParams["figure.autolayout"] = True

TOP_N_SKILLS = 15


def main():
    df = pd.read_csv("../Task3_NLP_Preprocessing/cleaned_job_postings.csv", parse_dates=["posting_date"])
    skills = pd.read_csv("../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv")
    skills = skills.merge(df[["job_id", "posting_date"]], on="job_id", how="left")
    skills["posting_date"] = pd.to_datetime(skills["posting_date"])
    skills["year_month"] = skills["posting_date"].dt.to_period("M")

    df["year_month"] = df["posting_date"].dt.to_period("M")

    # 1) overall monthly postings + hiring velocity
    monthly = df.groupby("year_month").size().rename("postings").to_frame()
    monthly = monthly.asfreq("M", fill_value=0).reset_index()
    monthly["year_month"] = monthly["year_month"].astype(str)
    monthly["rolling_3mo_avg"] = monthly["postings"].rolling(3, min_periods=1).mean().round(2)
    monthly["mom_growth_pct"] = monthly["postings"].pct_change().mul(100).round(1)
    monthly.to_csv("monthly_postings.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(monthly["year_month"], monthly["postings"], marker="o", label="Postings/month")
    plt.plot(monthly["year_month"], monthly["rolling_3mo_avg"], linestyle="--", label="3-mo rolling avg (hiring velocity)")
    plt.xticks(rotation=90)
    plt.title("Google — Overall Hiring Trend (simulated calendar, see Task 3 limitation)")
    plt.xlabel("Month")
    plt.ylabel("Postings")
    plt.legend()
    plt.savefig("visuals/overall_hiring_trend.png", dpi=150)
    plt.close()

    # 2) category monthly trend
    cat_monthly = df.groupby(["year_month", "Category"]).size().rename("postings").reset_index()
    cat_monthly["year_month"] = cat_monthly["year_month"].astype(str)
    cat_monthly.to_csv("category_monthly_trend.csv", index=False)

    top_categories = df["Category"].value_counts().head(6).index.tolist()
    plt.figure(figsize=(11, 6))
    for cat in top_categories:
        sub = cat_monthly[cat_monthly["Category"] == cat]
        plt.plot(sub["year_month"], sub["postings"], marker=".", label=cat)
    plt.xticks(rotation=90)
    plt.title("Google — Monthly Postings by Top 6 Job Categories")
    plt.xlabel("Month")
    plt.ylabel("Postings")
    plt.legend(fontsize=8)
    plt.savefig("visuals/category_trend.png", dpi=150)
    plt.close()

    # 3) skill monthly trend (top skills overall)
    top_skills = skills["skill"].value_counts().head(TOP_N_SKILLS).index.tolist()
    skill_monthly = (
        skills[skills["skill"].isin(top_skills)]
        .groupby(["year_month", "skill"]).size().rename("mentions").reset_index()
    )
    skill_monthly["year_month"] = skill_monthly["year_month"].astype(str)
    skill_monthly.to_csv("skill_monthly_trend.csv", index=False)

    plt.figure(figsize=(11, 6))
    for sk in top_skills[:8]:
        sub = skill_monthly[skill_monthly["skill"] == sk]
        plt.plot(sub["year_month"], sub["mentions"], marker=".", label=sk)
    plt.xticks(rotation=90)
    plt.title("Google — Monthly Mentions, Top 8 Skills")
    plt.xlabel("Month")
    plt.ylabel("Mentions")
    plt.legend(fontsize=8)
    plt.savefig("visuals/top_skills_trend.png", dpi=150)
    plt.close()

    # 4) seasonality by calendar month (month-of-year), pooling both years
    df["month_name"] = df["posting_date"].dt.month_name()
    month_order = ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"]
    seasonal = df.groupby("month_name").size().reindex(month_order).rename("postings").reset_index()
    seasonal.to_csv("seasonal_month_of_year.csv", index=False)

    pivot = df.pivot_table(index="Category", columns="month_name", values="job_id", aggfunc="count", fill_value=0)
    pivot = pivot.reindex(columns=month_order, fill_value=0)
    plt.figure(figsize=(12, 7))
    plt.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    plt.colorbar(label="Postings")
    plt.xticks(range(len(month_order)), month_order, rotation=90)
    plt.yticks(range(len(pivot.index)), pivot.index, fontsize=7)
    plt.title("Google — Seasonal Heatmap: Category x Calendar Month")
    plt.savefig("visuals/seasonal_heatmap.png", dpi=150)
    plt.close()

    # 5) growth summary: first half vs second half of the window
    midpoint = df["posting_date"].min() + (df["posting_date"].max() - df["posting_date"].min()) / 2
    df["half"] = df["posting_date"].apply(lambda d: "first_half" if d < midpoint else "second_half")
    cat_half = df.groupby(["Category", "half"]).size().unstack(fill_value=0)
    for c in ["first_half", "second_half"]:
        if c not in cat_half.columns:
            cat_half[c] = 0
    cat_half["growth_pct"] = ((cat_half["second_half"] - cat_half["first_half"]) / cat_half["first_half"].replace(0, 1) * 100).round(1)
    cat_half = cat_half[cat_half["first_half"] + cat_half["second_half"] >= 15]  # ignore tiny-count noise
    cat_half = cat_half.sort_values("growth_pct", ascending=False).reset_index()
    cat_half.insert(0, "signal_type", "category")
    cat_half = cat_half.rename(columns={"Category": "name"})

    skills_h = skills.merge(df[["job_id", "half"]], on="job_id", how="left")
    skill_half = skills_h.groupby(["skill", "half"]).size().unstack(fill_value=0)
    for c in ["first_half", "second_half"]:
        if c not in skill_half.columns:
            skill_half[c] = 0
    skill_half["growth_pct"] = ((skill_half["second_half"] - skill_half["first_half"]) / skill_half["first_half"].replace(0, 1) * 100).round(1)
    skill_half = skill_half[skill_half["first_half"] + skill_half["second_half"] >= 10]  # ignore tiny-count noise
    skill_half = skill_half.sort_values("growth_pct", ascending=False).reset_index()
    skill_half.insert(0, "signal_type", "skill")
    skill_half = skill_half.rename(columns={"skill": "name"})

    growth_summary = pd.concat([cat_half, skill_half], ignore_index=True)
    growth_summary.to_csv("growth_summary.csv", index=False)

    print("=== Task 5 Summary ===")
    print(f"Months covered: {monthly['year_month'].min()} -> {monthly['year_month'].max()}")
    print(f"Avg postings/month: {monthly['postings'].mean():.1f}")
    print("\nTop 5 growing categories (first half -> second half):")
    print(cat_half.head(5)[["name", "first_half", "second_half", "growth_pct"]].to_string(index=False))
    print("\nTop 5 growing skills (min 10 total mentions):")
    print(skill_half.head(5)[["name", "first_half", "second_half", "growth_pct"]].to_string(index=False))
    print("\nTop 5 declining categories:")
    print(cat_half.tail(5)[["name", "first_half", "second_half", "growth_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
