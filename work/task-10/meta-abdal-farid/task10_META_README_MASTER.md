# Meta: Competitor Demand Prediction Using Job Postings

**CadetX Internship Project** — Tasks 1–9  
**Member:** Abdal Farid  
**Company:** Meta  
**Date:** 2026-09-27  

---

## Project Overview

This repository contains a complete hiring intelligence analysis for Meta, using 209 job postings from 5 Kaggle datasets (2024–2026). The project proceeds through 9 sequential tasks:

1. **Task 1:** Legal source review and ToS compliance
2. **Task 2:** Data collection, schema validation, and deduplication
3. **Task 3:** NLP preprocessing (boilerplate removal, date unification)
4. **Task 4:** Canonical skill extraction using shared taxonomy
5. **Task 5:** Hiring trend analysis (weekly/monthly velocity, forecast window)
6. **Task 6:** Company skill profile and strategic positioning
7. **Task 7:** Demand forecasting (12-week horizon with prediction intervals)
8. **Task 8:** Similarity framework and cross-company comparison prerequisites
9. **Task 9:** Executive insight report and strategic recommendations

Each task produces:
- **Data artifacts** (CSV files, cleaned postings, extracted features)
- **Analysis scripts** (re-runnable Python)
- **Method notes** (explaining choices, limitations, caveats)
- **Visualizations** (PNG charts for reports)

---

## Quick Start

### Reproducing the Entire Analysis

```bash
# 1. Clone the repository
git clone <repo_url>
cd work/meta-abdal-farid

# 2. Install dependencies
pip install pandas numpy scikit-learn PyYAML matplotlib seaborn

# 3. Run Task 4 extraction (the core analysis)
python task-4/extract_skills.py \
  task-3/meta_cleaned_20260906.csv \
  shared/taxonomy/skills.yaml \
  task-4/output/

# 4. All other tasks are analysis/reporting; scripts are documented in their folders
```

### Viewing Key Outputs

| What | Where | Format |
|---|---|---|
| **Executive summary** | task-9/ | `meta_insight_report_20260927.md` + PNG |
| **Skill profile** | task-6/ | CSV + visualization PNG |
| **Top findings** | task-9/meta_insight_report_20260927.md | Markdown report |
| **Full presentation** | slides/ | 12-slide deck (markdown source) |

---

## Folder Structure

```
work/meta-abdal-farid/
├── README.md (this file)
│
├── task-1/
│   ├── README.md
│   ├── source-review.md
│   └── META_Task1.md
│
├── task-2/
│   ├── README.md
│   ├── META_Task2_DataCollectionReport.md
│   └── meta_postings_raw_20260906.csv (209 rows, raw)
│
├── task-3/
│   ├── README.md
│   ├── preprocessing_note.md
│   ├── preprocess.py (re-runnable)
│   ├── meta_cleaned_20260906.csv (209 rows, cleaned)
│   └── meta_cleaning_log_20260906.csv
│
├── task-4/
│   ├── README.md
│   ├── method_note.md
│   ├── extract_skills.py (re-runnable from clean checkout)
│   ├── skills_updated_20260926.yaml (taxonomy with Meta's corrections)
│   ├── meta_extracted_skills_20260926.csv
│   ├── meta_feature_skill_frequency_20260926.csv
│   ├── meta_feature_category_frequency_20260926.csv
│   ├── meta_feature_monthly_skill_trend_20260926.csv
│   ├── meta_taxonomy_candidates_20260926.csv
│   └── meta_comparison_skill_tiers_20260926.csv
│
├── task-5/
│   ├── README.md
│   ├── method_note.md
│   ├── meta_trend_weekly_20260926.csv
│   ├── meta_trend_monthly_20260926.csv
│   └── meta_trend_analysis_20260926.png
│
├── task-6/
│   ├── README.md
│   ├── method_note.md
│   ├── meta_comparison_category_deep_dive_20260926.csv
│   ├── meta_comparison_skill_profile_20260926.png
│   └── meta_comparison_skill_tiers_20260926.csv
│
├── task-7/
│   ├── README.md
│   ├── method_note.md
│   ├── meta_forecast_12week_20260927.csv
│   ├── meta_forecast_12week_20260927.png
│   ├── meta_forecast_train_20260927.csv
│   └── meta_forecast_test_20260927.csv
│
├── task-8/
│   ├── README.md
│   ├── method_note.md
│   ├── meta_skill_vector_20260927.csv
│   ├── meta_similarity_hypothetical_20260927.csv
│   ├── meta_similarity_skill_space_20260927.png
│   ├── meta_similarity_matrix_hypothetical_20260927.png
│   └── meta_similarity_sparsity_issue_20260927.png
│
├── task-9/
│   ├── README.md
│   ├── meta_insight_report_20260927.md (MAIN REPORT)
│   └── meta_insight_executive_summary_20260927.png
│
└── slides/
    ├── README.md
    ├── meta_presentation_20260927.md (markdown source, 12 slides)
    └── [PowerPoint version if created from markdown]
```

---

## Key Findings (Summary)

### Meta's Hiring Profile
- **Research-dominated:** 84% of jobs require ML/AI research expertise
- **Python-first:** Only language at >20% adoption; C++/Go/Rust <5% combined
- **Infrastructure-light:** Cloud hiring 4%, data engineering 3%
- **Top 3 skills:** LLMs (30.6%), Recommender Systems (30.1%), Generative AI (27.8%)

### Strategic Bet
Meta is betting: **"Top AI researchers on commodity infrastructure = sustainable advantage"**
- If true: Leads in AI/LLM capabilities, faster shipping
- If false: Infrastructure debt compounds, researcher productivity drops

### Data Quality
- 209 postings from 5 Kaggle snapshots (not continuous stream)
- 63% are duplicates (true n ≈ 112)
- Feb 2026 has 58% of data (single snapshot, not hiring signal)
- **Cannot forecast trends** (time series is artifact-dominated)
- **Cannot compare companies yet** (different taxonomies, text sources)

### Next Steps
1. Collect fresh data (weekly LinkedIn scrapes, starting Q4 2026)
2. Ratify shared taxonomy (59 vs. 93 skills)
3. Declare text source (title vs. title+description)
4. Re-run all teams' Task 4 extraction with canonical setup
5. Build valid 4-way similarity matrix
6. Re-run this analysis quarterly (watch for strategic shifts)

---

## Data Quality Caveats

### What We Know (High Confidence)
✓ Meta hires heavily for AI/ML research  
✓ Python is the primary development language  
✓ Infrastructure/DevOps hiring is minimal  
✓ Organizational structure is research-dominant  

### What We DON'T Know (Low Confidence)
✗ Meta's absolute hiring volume (sample, not census)  
✗ Year-over-year hiring growth (time series too gapped)  
✗ Future hiring trends (forecast unreliable due to sparse data)  
✗ How Meta compares to NVIDIA/Google/Microsoft (4-way comparison not valid yet)  

### Critical Issues
1. **Kaggle snapshot bias:** 5 one-time uploads, not continuous collection
2. **Duplicate inflation:** 63% of rows are reposts; all percentages are scaled up
3. **Selection bias:** "AI jobs" dataset omits non-AI roles (HR, finance, legal, ops)
4. **Missing seniority:** Cannot break down junior vs. senior roles
5. **No compensation:** Cannot infer salary/market positioning

**Do not use this analysis for budget forecasts or staffing plans without addressing these issues.**

---

## Running Individual Tasks

Each task is independent but depends on outputs from prior tasks:

### Task 2: Data Collection
```bash
# Input: 5 Kaggle CSV files (must be downloaded separately)
# Output: meta_postings_raw_20260906.csv
# Method: Documented in task-2/README.md
```

### Task 3: Preprocessing
```bash
# Input: meta_postings_raw_20260906.csv (Task 2 output)
# Output: meta_cleaned_20260906.csv
# Run: python task-3/preprocess.py meta_postings_raw_20260906.csv meta_cleaned_20260906.csv meta_cleaning_log_20260906.csv
```

### Task 4: Skill Extraction (re-runnable from clean checkout)
```bash
# Input: meta_cleaned_20260906.csv (Task 3), shared/taxonomy/skills.yaml
# Output: meta_extracted_skills_20260926.csv and feature tables
# Run: python task-4/extract_skills.py <cleaned_csv> <taxonomy_yaml> <outdir>
# Verified: Runs cleanly from /tmp/ (clean checkout)
```

### Tasks 5–9: Analysis (not re-runnable; depends on Task 4 outputs)
```bash
# Each task reads CSVs from prior tasks and generates reports/visualizations
# Documented in individual task READMEs
```

---

## Methodology Notes

### Skill Extraction (Task 4)
- **Input text:** Job title + cleaned job description (not title-only)
- **Taxonomy:** 93 canonical skills (shared across all teams)
- **Matching:** Regex with word-boundary rules and negative-context filters
- **Validation:** Hand-checked 20 random postings; 90% accuracy
- **Output:** Long-format skill mentions + aggregated frequency tables

### Trend Analysis (Task 5)
- **Bucketing:** ISO weeks (Monday start) + calendar months
- **Window:** Sept 1, 2025 – Aug 31, 2026 (per shared config)
- **Zero-fill:** Empty periods filled with 0 (no NaNs)
- **Velocity:** Count of new postings per bucket (not normalized)
- **Caveats:** Data is snapshots (stock), not arrivals (flow); Feb 2026 spike is artifact

### Similarity Framework (Task 8)
- **Feature space:** 93 skills, normalized by share-of-postings
- **Distance metric:** Cosine similarity (0.0–1.0)
- **Status:** Framework designed but not applied to 4-way comparison (currently invalid per brief's open decisions)

---

## Artifacts & Attribution

All CSV files, PNG visualizations, and method notes are tagged with creation date (20260926–20260927). This ensures:
- Clean versioning (no overwrite risk)
- Traceability (every file has a timestamp)
- Auditability (can trace back to specific analysis run)

All findings cite their source artifacts:
- "Meta hires 84% in research domains" → task-6/meta_comparison_category_deep_dive_20260926.csv
- "LLMs appear in 30.6% of postings" → task-4/meta_feature_skill_frequency_20260926.csv
- "Feb 2026 has 57.8% of data" → task-5/meta_trend_monthly_20260926.csv

---

## Shared Taxonomy & Extensions

Meta's Task 4 identified **two canonical skill aliases that should be removed** from the shared taxonomy:

1. **"drive" from Autonomous Vehicles** — 100% false positives (matched generic corporate verb)
2. **"driver" from Kernel & Drivers** — 100% false positives (single repeated boilerplate)

Both documented in `task-4/skills_updated_20260926.yaml` with dated comments. **These changes require team ratification before publishing.**

---

## Presenting This Work

### For Strategy/HR Leadership
**Use:** Task 9 insight report + Slide 11 of the 12-slide deck  
**Time:** 10–15 minutes  
**Takeaway:** Meta is AI-research-first; watch for infrastructure risk  

### For Data Science Mentor
**Use:** 12-slide deck + individual task method notes  
**Time:** 30–45 minutes  
**Takeaway:** How to build hiring intelligence pipelines; data asymmetry breaks naive comparisons  

### For Team Debrief
**Use:** Team storyline presentation (separate file) + all four companies' decks  
**Time:** 60–90 minutes  
**Takeaway:** Why cross-company comparison is blocked and what's needed to unblock it  

---

## Dependencies & Environment

### Python Packages
```
pandas 3.0.2
numpy 1.26.0
scikit-learn 1.3.2
PyYAML 6.0.3
matplotlib 3.8.4
seaborn 0.13.0
```

### Installation
```bash
pip install pandas numpy scikit-learn PyYAML matplotlib seaborn
```

### Versions Used
- Python 3.12.3
- Verified on: Ubuntu 24 LTS

---

## Contact & Attribution

**Analyst:** Abdal Farid  
**Project:** CadetX Internship, Meta Track  
**Completion Date:** 2026-09-27  
**Status:** ✓ Tasks 1–9 complete  

**For questions on:**
- Data sources → Task 1 method note
- Data quality → Task 2 report
- Preprocessing → Task 3 method note
- Skill extraction → Task 4 method note (includes taxonomy changes)
- Trends → Task 5 method note
- Strategic profile → Task 6 method note
- Forecast → Task 7 method note (flagged as unreliable)
- Similarity → Task 8 method note (includes why 4-way is blocked)
- Insights → Task 9 insight report

---

## License & Attribution

All Kaggle data is used under the license specified at source (CC, MIT, ODC-By). See Task 1 source review for details.

Code (Python scripts) is provided as-is for educational and research purposes.

Reports and analyses are part of the CadetX internship project and should be attributed as: "Abdal Farid, CadetX Internship, Meta Track, 2026."

---

**Last updated:** 2026-09-27  
**Status:** ✓ All 9 tasks complete, ready for mentor review
