# Task 6 – Competitor Comparison By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

## 1. Scope note (important)
The team's full comparison framework is meant to run across **four companies**. This member's raw data (Task 1/2) is the Google Job Skills dataset, which only covers Google — but that dataset itself contains two `Company` values, **Google** and **YouTube** (a Google subsidiary), giving a genuine within-dataset comparison to demonstrate the framework on.

`compare.py` is written to **auto-merge teammates' data** the moment it's available: drop a teammate's Task 4 output (`cleaned_job_postings.csv`, `extracted_skills.csv`) into `competitor_data/<CompanyName>/`, and the script picks it up automatically and re-runs the same tables across all companies present — no code changes needed. As run here, no `competitor_data/` folder exists, so it reports "Google vs YouTube only" explicitly (see script stdout), which keeps the output honest about what it's actually comparing.

## 2. Comparison framework
| Table | What it compares |
|---|---|
| `company_overview.csv` | postings, distinct Categories, distinct Locations per company |
| `category_mix_by_company.csv` | % of postings per job Category, per company |
| `top_skills_by_company.csv` | top-15 taxonomy skills per company with % of postings |
| `skill_category_mix.csv` | tech-stack pattern — % of skill mentions per taxonomy category (Programming, Cloud & Infra, Data & ML, …), per company |
| `hiring_velocity_by_company.csv` | monthly postings per company on the simulated calendar (Task 3 limitation applies) |

Visuals in `visuals/`: `category_mix_by_company.png`, `skill_category_mix.png`, `hiring_velocity_by_company.png`.

## 3. How Google compares to YouTube (within-dataset)
- **Scale**: Google — 1,107 postings across 23 categories, 92 locations; YouTube — 20 postings across 10 categories, 8 locations. YouTube's postings in this dataset are a small slice, so its percentages are noisier (small-n caveat).
- **Skill-category mix is close** between the two: both lean Business & Soft Skills (~47–52%), Education & Certifications (~16–17%), Programming Languages (~14–16%) — consistent with YouTube operating as an integrated part of Google's hiring pipeline rather than a distinct tech stack.
- **Notable gap**: YouTube shows 0% Cloud & Infrastructure mentions vs Google's 7.2%, and a higher Data & ML share (8.5% vs 4.3%) — directionally consistent with YouTube's postings skewing toward media/content/data-product roles rather than core cloud-infra roles, though the small YouTube sample (20 postings) means this should be treated as a weak signal, not a confirmed strategic gap.

## 4. What a real 4-company comparison would add
Once teammates' `competitor_data/<Company>/` folders are populated, the same script directly yields: category-mix divergence (which competitor is over-indexed on which role type), skill-category "tech stack" comparison (who's hiring more for cloud/ML vs traditional infra), and hiring-velocity overlay (who's accelerating hiring faster) — the actual strategic-gap analysis the programme description asks for. This is flagged again in Task 9.

## Task 6 Outcome
A reusable, auto-merging competitor-comparison framework built and validated on Google vs YouTube; tables and visuals produced; ready to absorb the other three companies' data with zero code changes for the full team comparison.
