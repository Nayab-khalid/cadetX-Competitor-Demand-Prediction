# Task 6: Competitor Comparison — Meta Skill Profile

Member: Abdal Farid
Date: 2026-09-26

## Executive summary

Meta's skill profile is **heavily concentrated on applied AI/ML research and product work**, specifically large language models, recommendation systems, and generative AI. The company hires almost no infrastructure or data-engineering specialists, indicating a strategic decision to build AI/ML as a product-facing capability, not as a platform/ops discipline.

**Coverage:** 66 of 93 taxonomy skills matched (71.0%). Meta's profile is incomplete relative to the full taxonomy, which includes infrastructure, data engineering, and silicon design specializations that Meta postings largely omit.

**No cross-company comparison is attempted in this task** — per the brief's open decisions, the four-way comparison is currently invalid (different taxonomies, different input text, different time windows). This note documents Meta alone.

---

## Meta's hiring profile by skill tier

| Tier | Count | Coverage (% of postings) | Examples |
|---|---|---|---|
| **Core** (20%+) | 4 | 30–31% each | LLMs (30.6%), Recommender Systems (30.1%), Generative AI (27.8%), Python (23.9%) |
| **Specialist** (10–20%) | 5 | 10–20% each | Machine Learning (19.6%), Performance Engineering (18.2%), SQL (15.8%), A/B Testing (11.5%), Statistics (10.5%) |
| **Niche** (5–10%) | 11 | 5–10% each | Computer Vision, AI Safety, Cybersecurity, Robotics, RL, Agentic AI, etc. |
| **Rare** (<5%) | 46 | <5% each | Everything else (HPC, CUDA, Compilers, Storage Systems, Silicon Design, etc.) |

**Interpretation:**
- **Core skills are research domains, not infrastructure** — LLMs, recommendations, generative AI are not operational systems skills; they are research specializations.
- **Python, not DevOps** — the only programming language at "Core" tier is Python (ML/data), not C++, Rust, or Go (which appear 2%, 0.5%, 3.8% respectively).
- **Performance engineering is valued, but not ops** — Performance Engineering is at 18.2%, but Site Reliability is only 5.7%, and DevOps/CI-CD are barely present (<1–2%).

---

## Meta's hiring by category

| Category | Postings | % of postings | Distinct skills | Interpretation |
|---|---|---|---|---|
| **research_domains** | 175 | 83.7% | 18 | **Meta is a research-hiring machine.** LLMs, Generative AI, Recommender Systems, Computer Vision, RL, Agentic AI — 83.7% of Meta jobs touch at least one research domain. |
| **languages** | 63 | 30.1% | 7 | Python dominates (23.9%), SQL is secondary (15.8%), C/C++ are minimal (1–2%). Focus on high-level data/ML languages, not systems languages. |
| **hardware_systems** | 46 | 22.0% | 12 | Performance engineering and datacenter systems dominate (5.7–18.2% each). CUDA, Embedded Systems, Computer Architecture are rare (<1–2%). **Not GPU programming, not embedded work.** |
| **analytics_bi** | 31 | 14.8% | 4 | A/B Testing (11.5%) and Statistics (10.5%) indicate product validation culture; Tableau/Power BI minimal (1–2%). **Analytics is product work, not reporting.** |
| **product_process** | 31 | 14.8% | 5 | Technical Leadership, Research Publication, TPM, Business Development — scattered, no single skill dominates. |
| **mlops_devops** | 29 | 13.9% | 5 | Cybersecurity (7.2%) and Site Reliability (5.7%) are present but not core. CI/CD, test automation minimal. **MLOps/DevOps is weak relative to research.** |
| **ml_frameworks** | 13 | 6.2% | 4 | PyTorch (5.7%) > TensorFlow (2.4%) ≈ JAX (2.0%). **Surprisingly low.** Fewer than 1 in 16 Meta jobs mention a specific ML framework by name. |
| **cloud_infra** | 9 | 4.3% | 2 | Cloud Infrastructure and Docker at 3.8–4.3%. **Meta's cloud/container skills are nearly absent.** (Likely expected — Meta builds its own infrastructure.) |
| **data_engineering** | 6 | 2.9% | 2 | Apache Spark, ETL barely present. **Data engineering is almost entirely absent.** |
| **silicon_design** | 6 | 2.9% | 7 | All rare (<1% each). No silicon hiring in this dataset. |

---

## Meta's strategic positioning

### What Meta prioritizes
1. **Applied AI research over infrastructure** — 3 of 4 core skills (LLMs, Recommendations, Generative AI) are research domains.
2. **Python-based development** — the only language at scale, indicating a ML-centric tech stack.
3. **Product analytics and experimentation** — A/B Testing (11.5%) and Statistics (10.5%) as Specialist-tier skills.
4. **Performance-conscious but not systems-focused** — Performance Engineering is present, but CUDA, HPC, kernel development are rare.

### What Meta de-emphasizes
1. **Infrastructure and operations** — Cloud Infrastructure (4.3%), Data Engineering (2.9%), silicon design (2.9%), DevOps (<2%).
2. **Specific ML frameworks** — Only 6.2% of postings mention PyTorch/TensorFlow/JAX by name, suggesting the company prefers to hire researchers who can learn any framework.
3. **Polyglot programming** — C++, Java, Go, Rust are all <5%, indicating a Python-first hiring strategy.
4. **Data pipeline engineering** — Apache Spark, ETL, Kafka are nearly absent despite being typical Big Tech infrastructure skills.

### Implication
**Meta is hiring for AI research + AI product work, not infrastructure or platform engineering.** The job market concentration on research domains, combined with weak infrastructure signals, suggests Meta's organizational structure has:
- Strong research teams (FAIR, MSL teams visible in postings)
- AI product teams (recommendations, generative features)
- Possibly outsourced or in-sourced infrastructure (hence few cloud/DevOps postings)

---

## Taxonomy coverage and gaps

### What the taxonomy covers well
- **Research domains** (18 skills): LLMs, Generative AI, Computer Vision, Robotics, RL, Agentic AI, RAG, RLHF, NLP, Recommender Systems, Deep Learning, Machine Learning, etc. → All matched, most at scale.
- **Core languages** (7 skills matched of 10 available): Python, SQL, Java, Go, Rust, R, JavaScript. C++ and C matched but weakly.

### What the taxonomy covers poorly (gap)
- **Cloud infrastructure** (2 skills matched of 2 available): Only "Cloud Infrastructure" and "Docker" show up; AWS, Azure, GCP, Kubernetes all below 5%.
- **Data engineering** (2 skills matched of 7 available): Only Spark and ETL; Kafka, Airflow, Snowflake, dbt, Databricks absent.
- **Silicon design** (7 skills in taxonomy, 0–1% each): No hiring visible. Meta doesn't appear to hire chip designers in this dataset.
- **ML frameworks** (4 skills matched of 8): PyTorch visible (5.7%), but ONNX, TensorRT, Triton Inference Server absent. Oddly weak given Meta's AI focus.

### Candidate terms for potential extension
The top candidate terms mined in Task 4 are mostly corporate boilerplate (`social`, `shape`, `strategy`, `design`, `learning`, `analytics`), but a few signal **real gaps:**
- **analytics** (131 mentions) — "analytics" as a standalone discipline, not A/B Testing specifically
- **augmented/virtual/immersive** (103–115 mentions) — AR/VR/Reality Labs work, not covered by current taxonomy
- **design** (124 mentions) — likely "design thinking," "product design," not technical design; not taxonomy material

---

## Method: normalized, comparison-ready structure

All tables and visuals follow the shared framework (`shared/config/analysis_config.yaml`):
- **Normalisation:** All results are share-of-postings (%), never raw counts, so Meta's 209 postings can later be fairly compared to any other company's total.
- **Data source:** Title + description (full text per Task 3 cleanup), not title-only. This is a stated choice per the open decision "titles or descriptions, decided once."
- **Taxonomy:** 93 skills (post-extension) from `shared/taxonomy/skills.yaml` v0.1.0.
- **Matcher:** Regex-based canonical matching with blocklist, negative-context rules, and single-occurrence-per-skill per task 4.

---

## Data caveats — why Meta's numbers are not directly comparable across companies (yet)

1. **Data collection artifact (Task 5):** Meta's 209 postings are a mixed bag of 5 Kaggle snapshots, with 57.8% concentrated in Feb 2026. This is **stock** (snapshot of open jobs at a moment), not **flow** (arrivals over time). NVIDIA has the same issue; Google and Microsoft's date coverage is unknown.

2. **Input text richness:** Meta has full job descriptions (206/209 rows). Other companies may have title-only data. Microsoft's open decision notes it gets 0.08 skills/posting from title vs. 6.84 from description — an 85x difference. If Google or Microsoft used title-only matching, their skill counts cannot be directly compared to Meta's.

3. **Duplicate inflation:** 63% of Meta's 209 rows are duplicate/repost duplicates (flagged in Task 2). Raw counts are inflated. Deduplication would reduce Meta's 209 to ~112 distinct postings, which would cut all skills' % values by ~50%.

4. **Taxonomy extension timing:** NVIDIA extended the taxonomy with 34 new skills (silicon_design, specialisations, etc.) *after* extracting. If Google and Microsoft extracted against the original 59-skill taxonomy before the extension, their scores are not comparable to NVIDIA's or Meta's.

5. **No cross-company time series:** Meta's data spans Jan 2024–June 2026 (with a 16-month gap). NVIDIA's is 2026-only. Google has no dates. Microsoft's date column is empty. A "hiring trend comparison" over time is not possible.

---

## Why this task is incomplete (per the brief's open decisions)

The brief explicitly flags: **"The four-way comparison is not currently valid."** Reasons:

1. **Everyone needs to extend the taxonomy for their own company**, then re-run Task 4 extraction. Otherwise NVIDIA's apparent richness (72% coverage) is just "Nayab extended the taxonomy," not "NVIDIA hires differently."

2. **Decide on title vs. description before any cross-company work.** Meta used both; Microsoft gets 85x more skills from description than title. If Google used title-only, it's not comparable.

3. **Inventory all data collection methods.** This note assumes everyone has full descriptions. If they don't, raw coverage % is meaningless.

This task (Task 6) should have been "hold until Tasks 1-5 are consistent across the team." Submitting it now documents Meta's internal profile only, not a comparison.

---

## Deliverables

- `meta_comparison_skill_tiers_20260926.csv` — All 66 matched skills, ranked by % coverage, with tier assignment (Core/Specialist/Niche/Rare)
- `meta_comparison_category_deep_dive_20260926.csv` — Category breakdown with top 3 skills per category, counts, percentages
- `meta_comparison_skill_profile_20260926.png` — 4-panel visualization: top 20 skills (horizontal bar), category distribution (vertical bar), tier pie chart, coverage concentration (bar)

---

## Next steps (recommendation for the team)

1. **Google, Microsoft, Anthropic: extend Task 4 for your companies.** Find skills/terms that are frequent in your postings but not in the taxonomy, propose additions.
2. **Consensus on title vs. description:** Does the team standardize on title+description (Meta, NVIDIA's choice), or title-only? If different, note it in Task 6 explicitly.
3. **Inventory data collection:** Dates, text fields available, whether data is stock (snapshot) or flow (continuous). Only then do cross-company comparisons make sense.
4. **Re-run Task 6** once steps 1–3 are done.

Until then, this note stands: **Meta is research-heavy, infrastructure-light, Python-first.** It's a data point about one company's hiring, not yet a comparison.
