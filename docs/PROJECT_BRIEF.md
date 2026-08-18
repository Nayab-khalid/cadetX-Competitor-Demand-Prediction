# CadetX — Competitor Demand Prediction Using Job Postings
**NLP · Forecasting · Competitive Intelligence** — Virtual Work Experience programme brief.

Duration 3 months (flexible) · Team of 4 (Agile/Scrum, MS Teams) · 4 company specialists ·
10 tasks + 2 optional · Python / NLP / GitHub · Certificate + Reference Letter on completion.

## 1. Overview
Job postings are a *forward-looking* signal — they show plans, not past performance.
Build a system that predicts competitor demand and emerging tech trends from job-posting data
of major tech / AI / data companies: which teams are expanding, which technologies are being
adopted, what competitors plan, which skills will be in demand over the next 3–12 months.

**Problem:** companies lack a systematic, data-driven way to analyse competitor hiring patterns
and predict future demand.

**Goal:** a model that uses external job-posting data to forecast competitor demand, skill
trends and market direction.

**Business value:** forecast skill/tech/role demand · predict competitor product launches ·
spot emerging tech & market skill gaps · plan hiring and training · benchmark salaries ·
detect early expansion or slowdown.

**Users:** strategy teams, HR/talent, product managers, CEOs/CTOs, investors.

## 2. How the programme works
- One unified project with four perspectives, shared standards, full 3 months.
- Weekly MS Teams meeting: progress, challenges, alignment, next steps.
- One shared GitHub repo: data, code, notes, weekly reports, docs, meeting minutes.
- Cadence: one task per week, or one task per two weeks — the team sets its own deadlines.
- That week's Scrum Leader coordinates task distribution and ensures work is documented + uploaded.
- Members support each other on technical/analytical difficulties.

## 3. Team structure
Four data scientists; each picks **one unique company** and becomes its specialist.
All four datasets feed **one shared intelligence system**.

Worked example — sector Tech/AI/Data: Google · OpenAI · NVIDIA · Anthropic.

Choose from (examples, others welcome): Google, Microsoft, OpenAI, Snowflake, Databricks,
NVIDIA, Meta, Anthropic.

## 4. Rotating weekly roles
| Role | Responsibility |
|---|---|
| Scrum Leader | Runs the weekly Teams meeting, coordinates tasks, main point of contact, owns that week |
| Data Quality Lead | Datasets clean, consistent, validated across all four companies |
| Documentation Lead | Documentation, meeting minutes, project notes |
| Technical Lead | Code structure, technical decisions, implementation help |

All meeting outcomes (decisions, blockers, progress, next steps) go to the shared repo; each
member also uploads their own weekly notes.

## 5. Requirements before starting
1. Finalise team & company selection (a unique company each).
2. Create the shared GitHub workspace — all work lives here.
3. Fix a weekly MS Teams slot; attendance mandatory.
4. Assign the four rotating roles.
5. Agree task scheduling (weekly or biweekly) within the 3-month timeline.

## 6. The 10 tasks
Sequential — each builds on the last. Every task ends with an upload to the shared repo.

**01 — Understanding Data Sources & Legal.** Where job-posting data comes from (public datasets,
open-data portals, Kaggle, GitHub, company career pages) and the legal/ethical rules: Terms of
Service, robots.txt, public vs copyrighted data. Never collect personal or sensitive data.
*Team submits:* approved source list · documented understanding of legal requirements · shared
collection plan for Task 2.

**02 — Data Collection.** Collect your company's postings from legal, approved sources only;
verify extraction is allowed, robots.txt does not block, no personal data included.
*Each submits:* short Data Collection Report (sources, legal checks, fields, limitations) · raw dataset.

**03 — NLP Preprocessing & Method Selection.** Clean, structure and preprocess descriptions. Own
choice of methods/libraries, but align on a consistent quality bar so cross-company comparison stays fair.
*Each submits:* cleaned & preprocessed text · documented workflow + code in GitHub.

**04 — Skill Extraction & Feature Engineering.** Extract skills (keyword lists, regex, spaCy,
embeddings) and convert them to features — counts, categories, frequency trends. Align a **shared
skill taxonomy** across the four datasets.
*Each submits:* extracted-skills dataset & feature tables · note on methods.

**05 — Hiring Trend Analysis.** Aggregate by week/month, compute hiring velocity, identify
growth, decline, seasonal spikes. Align on a **shared time-series structure**.
*Each submits:* trend tables & visual summaries · note on key patterns.

**06 — Competitor Comparison.** Compare all four on skills, role categories, hiring velocity and
tech-stack patterns in a shared comparison framework; surface similarities, differences, strategic gaps.
*Each submits:* comparison tables & visuals · explanation of how their company compares.

**07 — Demand Forecasting.** Predict future hiring demand from the time series. Method is free
(moving averages, ARIMA, Prophet, deep learning) but align on a **shared forecast horizon**.
*Each submits:* forecast outputs & plots · brief explanation of the chosen model and why.

**08 — Company Similarity Scoring.** Similarity across skills, tech-stack tags, role categories
and trends — overlap scores, cosine similarity, TF-IDF, embeddings — within a shared framework.
*Each submits:* similarity tables & visuals (heatmaps / network graphs) · what drives the similarity.

**09 — Insight Generation & Reporting.** Turn analysis, comparisons and forecasts into actionable
insights on hiring patterns, skill demand, tech-stack trends and future demand. Shared reporting structure.
*Each submits:* concise insight report & visual summaries · explanation of the company's hiring
strategy and market position.

**10 — Final Presentation & Mentor Review.** Present the full workflow to the mentor and answer
questions on methods and results. Consistent slide format; finalise the repo — organised folders,
clean notebooks, updated READMEs.
*Team submits:* polished final presentation (per member + aligned storyline) · complete repo.

### Optional tasks (if time allows)
- **Automated Pipeline** — chain collection → preprocessing → skill extraction → trend analysis →
  forecasting into one scheduled end-to-end pipeline (Python scripts, cron, GitHub Actions, orchestrator).
  *Submit:* documented pipeline design & automation steps · final workflow in GitHub.
- **Fine-Tune a Skill Extraction Model** — fine-tune BERT/RoBERTa/spaCy on your descriptions and
  verified skill labels to improve precision and recall.
  *Submit:* fine-tuned model & evaluation metrics · note on the training process and gains.

## 7. Data & dataset schema
No dataset is provided — the team collects its own from legal, approved sources and documents
provenance and limitations. Legal & ethical first: Terms of Service, robots.txt, is extraction
allowed, public vs copyrighted. **Never collect personal or sensitive information.**

One row = one job posting; one column = one feature for NLP, analysis or forecasting.

### Required fields
| Field | Why it matters |
|---|---|
| `job_id` | Unique identifier for each posting |
| `company_name` | Needed for competitor comparison |
| `job_title` | Role classification, seniority detection |
| `job_description` | Main NLP input for skill extraction (full text) |
| `posting_date` | Hiring velocity, time-series forecasting, trend analysis |
| `location` | Regional hiring patterns; remote vs onsite |
| `job_url` | Traceability and validation |

### Recommended fields
`employment_type` (full-time/contract/internship) · `department` / `job_category` (Engineering,
AI, Data, Product) · `seniority_level` (Junior…Principal) · `extracted_skills` ·
`skill_categories` (Cloud, ML, DevOps…) · `tech_stack_tags` (AWS, Python, Kubernetes) ·
`cleaned_description` · `posting_month` / `posting_week` · `updated_at` / `scraped_date`
(reposted, stale vs fresh) · `job_status` (active/closed → urgency) · `salary_range` (when public) ·
`company_industry` / `sector` · `role_cluster_id` (NLP clustering) · `embedding_vector`
(Sentence-BERT) · `skill_frequency_vector` · `emerging_skill_flag` · `hiring_velocity_bucket`.

### Example rows (simplified)
| job_id | company_name | job_title | posting_date | job_description | extracted_skills | seniority | category | location |
|---|---|---|---|---|---|---|---|---|
| 001 | Google | ML Engineer | 2024-05-12 | full text… | ["Python","TensorFlow","GCP"] | Senior | AI/ML | London |
| 002 | Amazon | Data Engineer | 2024-05-10 | full text… | ["Spark","AWS","SQL"] | Mid | Data | Remote |
| 003 | Meta | LLM Researcher | 2024-05-08 | full text… | ["PyTorch","Transformers","RAG"] | Lead | AI Research | Dublin |

## 8. GitHub & submission
- One shared team repository is the backbone: data, code, notes, weekly reports, docs, minutes.
- The Scrum Leader uploads weekly meeting notes (decisions, blockers, progress, next steps).
- Each member also uploads their own weekly notes and contributions.
- At the end of each task the repo link is submitted in the CadetX portal.

## 9. Assessment (certificate, reference letter, job recommendation)
| Criterion | What is assessed |
|---|---|
| Consistency | Regular submissions, active participation across the 3 months |
| Specialist depth | Strong, well-documented analysis of your company |
| Legal & ethical rigour | Sources verified and documented; no personal or copyrighted data |
| Quality | Sound NLP, forecasting, clear visuals, useful insights |
| Collaboration | Active in the weekly Scrum and the rotating roles |
| Completeness | Finished, well-structured shared repo and polished final presentation |

## 10. How to select & start
1. Open Projects Selection in the CadetX student portal.
2. Read the brief and select **Competitor Demand Prediction**.
3. It is assigned and appears in your Projects area.
4. Form the team of four; each picks a unique company.
5. Set up the shared GitHub workspace, fix the weekly MS Teams slot, assign rotating roles.
6. Begin Task 1, then work through the 10 tasks, submitting the repo link as you go.
