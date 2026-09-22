# Task 5 – Hiring Trend Analysis By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

> **Limitation carried from Task 3:** `posting_date` is a seeded, reproducible **simulated** field — the Google Job Skills dataset has no real posting-date column. Every table/chart below demonstrates the trend-analysis *methodology* (monthly aggregation, rolling velocity, growth-rate comparison, seasonality) on a synthetic 2023–2024 calendar. Absolute numbers are not real Google hiring activity; the shape of the method is what should be reused once real timestamps are available.

## 1. Time-series structure
Monthly (`year_month`, `YYYY-MM`) — chosen as the shared granularity across the team's four companies (weekly is too noisy for ~1,100-row datasets; quarterly hides skill-level shifts).

## 2. Method
- **Hiring velocity** = postings/month + 3-month rolling average (`monthly_postings.csv`, `visuals/overall_hiring_trend.png`).
- **Category trend** = postings/month per job `Category` (`category_monthly_trend.csv`, `visuals/category_trend.png`).
- **Skill trend** = mentions/month for the top 15 taxonomy skills from Task 4 (`skill_monthly_trend.csv`, `visuals/top_skills_trend.png`).
- **Seasonality** = postings pooled by calendar month name, plus a Category × Month heatmap (`seasonal_month_of_year.csv`, `visuals/seasonal_heatmap.png`).
- **Growth/decline** = first-half-of-window vs second-half-of-window counts per category (min. 15 total postings) and per skill (min. 10 total mentions), both floors chosen to filter out growth-% swings driven by tiny sample noise (e.g. 0→3 postings reads as "+300%" but is meaningless volume), ranked by % growth (`growth_summary.csv`).

## 3. Key patterns observed
- Average **47 postings/month** across the simulated 2023-01 → 2024-12 window.
- **Growing categories** (first half → second half, ≥15 total postings): Technical Solutions (37→64, +73%), Partnerships (23→31, +35%) — the only two categories that clear the volume floor with positive growth; everything else in the top-5-by-count list (People Operations, Program Management, Product & Customer Support) is flat-to-slightly-down, consistent with the mild linear trend built into the simulated calendar in Task 3 (see that file's limitation note) rather than a dramatic shift.
- **Fastest-growing skills** (≥10 total mentions): `data_mining`, `virtualization`, `ruby`, `rest_api`, `mobile_development`.
- **Declining categories**: Manufacturing & Supply Chain, Administrative, Legal & Government Relations, Finance, Sales Operations.
- Because the synthetic calendar encodes only a simple linear category-level trend (not real calendar seasonality like hiring freezes or fiscal-year cycles), the seasonal heatmap should be read as a demonstration of the technique rather than a real seasonal signal — this caveat is repeated in the Task 9 report.

## Task 5 Outcome
Full trend-analysis pipeline built and run: monthly hiring velocity, category/skill trend tables, a seasonality view, and a first-half-vs-second-half growth ranking, with matching visual summaries in `visuals/`. Ready to feed Task 6 (Competitor Comparison) and Task 7 (Demand Forecasting).
