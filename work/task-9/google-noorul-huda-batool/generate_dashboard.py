"""
Task 9 - Insight Generation & Reporting
Author: Noor Ul Huda | Company track: Google

Builds one executive-summary dashboard image pulling from Tasks 4-8 output,
to accompany insight_report.md.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Google Hiring Intelligence — Executive Dashboard (Noor Ul Huda)", fontsize=15, fontweight="bold")

# 1) overall hiring trend
monthly = pd.read_csv("../Task5_Hiring_Trend_Analysis/monthly_postings.csv")
ax = axes[0, 0]
ax.plot(monthly["year_month"], monthly["postings"], marker="o", ms=3)
ax.set_title("Monthly Postings (simulated calendar)")
ax.tick_params(axis="x", rotation=90, labelsize=6)

# 2) top skills
freq = pd.read_csv("../Task4_Skill_Extraction_Feature_Engineering/skill_frequency.csv").head(10)
ax = axes[0, 1]
ax.barh(freq["skill"][::-1], freq["pct_of_postings"][::-1], color="#4285F4")
ax.set_title("Top 10 Skills (% of postings)")
ax.tick_params(axis="y", labelsize=7)

# 3) category mix
cat_counts = pd.read_csv("../Task3_NLP_Preprocessing/cleaned_job_postings.csv")["Category"].value_counts().head(8)
ax = axes[0, 2]
ax.barh(cat_counts.index[::-1], cat_counts.values[::-1], color="#34A853")
ax.set_title("Top 8 Job Categories (postings)")
ax.tick_params(axis="y", labelsize=7)

# 4) forecast
fc = pd.read_csv("../Task7_Demand_Forecasting/forecast_overall.csv")
hist = monthly.tail(6)
ax = axes[1, 0]
ax.plot(hist["year_month"], hist["postings"], marker="o", label="Recent actual", color="#4285F4")
ax.plot(fc["year_month"], fc["forecast_postings"], marker="o", linestyle="--", label="6-mo forecast", color="#EA4335")
ax.set_title("Demand Forecast (next 6 months)")
ax.tick_params(axis="x", rotation=45, labelsize=7)
ax.legend(fontsize=7)

# 5) company similarity (Google vs YouTube)
sim = pd.read_csv("../Task8_Company_Similarity_Scoring/similarity_cosine_skill_profile.csv", index_col=0)
ax = axes[1, 1]
im = ax.imshow(sim.values, cmap="viridis", vmin=0, vmax=1)
ax.set_xticks(range(len(sim.columns))); ax.set_xticklabels(sim.columns, fontsize=8)
ax.set_yticks(range(len(sim.index))); ax.set_yticklabels(sim.index, fontsize=8)
for i in range(len(sim.index)):
    for j in range(len(sim.columns)):
        ax.text(j, i, f"{sim.values[i,j]:.2f}", ha="center", va="center", color="white", fontsize=9)
ax.set_title("Tech-Stack Similarity (cosine)")

# 6) growth signals
growth = pd.read_csv("../Task5_Hiring_Trend_Analysis/growth_summary.csv")
top_growth = growth.sort_values("growth_pct", ascending=False).head(8)
ax = axes[1, 2]
colors = ["#34A853" if s == "category" else "#FBBC05" for s in top_growth["signal_type"]]
ax.barh(top_growth["name"][::-1], top_growth["growth_pct"][::-1], color=colors[::-1])
ax.set_title("Top Growth Signals (category=green, skill=yellow)")
ax.tick_params(axis="y", labelsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("executive_dashboard.png", dpi=150)
print("Saved -> executive_dashboard.png")
