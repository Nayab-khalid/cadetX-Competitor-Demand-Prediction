# Task 10 – Final Presentation & Mentor Review By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

## Contents
- `Google_Hiring_Intelligence_Final_Presentation.pptx` — 12-slide final deck covering the problem, pipeline (Tasks 1–9), data/legal foundation and its date-field limitation, NLP/skill-extraction results, hiring trends, competitor comparison, demand forecast, similarity scoring, Google's inferred hiring strategy, and limitations/next steps.
- `build_deck.js` — the pptxgenjs script that generates the deck (all chart data sourced from the actual Task 4–8 output CSVs). Rerun with `npm install && node build_deck.js` after installing Node dependencies (`node_modules/` is gitignored).

## Slide flow
1. Title
2. Problem & business value
3. End-to-end pipeline (Tasks 1–9)
4. Data source & legal foundation, incl. the simulated-date limitation
5. NLP preprocessing & skill extraction results
6. Hiring trend analysis
7. Competitor comparison (Google vs YouTube)
8. Demand forecast (6-month horizon)
9. Company similarity scoring
10. Google's hiring strategy & position
11. Limitations & next steps (incl. the optional Tasks 11–12)
12. Thank you / Q&A

## QA performed
- `validate.py` schema/relationship/content-type check — **passed**.
- `markitdown` content dump checked for missing content and leftover placeholder text — **none found**.
- Manual coordinate/layout review for text overflow and spacing (no LibreOffice available in this environment to render slide images, so this substituted for pixel-level visual QA).

## GitHub workspace structure
The repository root now contains, alongside this presentation and the original Task 1/2 deliverables:

```
Google Task 1 .docx
Task 2.pdf
job_skills.csv
Task3_NLP_Preprocessing/        (script, README, cleaned dataset)
Task4_Skill_Extraction_Feature_Engineering/  (taxonomy, script, README, feature tables)
Task5_Hiring_Trend_Analysis/    (script, README, trend tables, visuals/)
Task6_Competitor_Comparison/    (script, README, comparison tables, visuals/)
Task7_Demand_Forecasting/       (script, README, forecast tables, visuals/)
Task8_Company_Similarity_Scoring/ (script, README, similarity tables, visuals/)
Task9_Insight_Generation_Reporting/ (insight_report.md, dashboard image, script)
Task10_Final_Presentation/      (this folder)
Optional_Automated_Pipeline/    (Task 11)
Optional_FineTune_Skill_Extraction/ (Task 12)
```

Every task folder has its own `README.md` documenting method, inputs/outputs, results, and (where relevant) limitations, so each folder is self-contained for a reviewer who opens it directly.

## Task 10 Outcome
Final presentation built, validated, and documented; the GitHub workspace is organized into one self-contained, README'd folder per task, ready to push.
