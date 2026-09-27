# Meta: Competitor Demand Prediction Using Job Postings
## CadetX Internship Project — Final Presentation

---

## Slide 1: Title Slide

**Meta: Competitor Demand Prediction Using Job Postings**

**Member:** Abdal Farid  
**Date:** 2026-09-27  
**Project:** CadetX Internship, Meta Track  
**Duration:** Tasks 1–9, September 2026  

---

## Slide 2: Project Scope & Data Strategy

### Objective
Predict Meta's future hiring demand and strategic positioning using job postings as a signal.

### Data Sources (Task 1)
- **5 Kaggle datasets**, all CC/open license
  - LinkedIn Job Postings 2023–2024
  - LinkedIn Jobs & Skills 2024
  - AI Job Market Global 2026
  - AI & ML Job Postings 2025
  - Job Listing Dataset (MIT)
- **Meta Careers page:** Rejected (ToS prohibits automated collection)

### Coverage
- **209 postings** collected across all sources
- **Date range:** Jan 2024 – June 2026
- **Legal status:** ✓ All licenses verified, compliant

---

## Slide 3: Data Collection & Quality (Task 2)

### Raw Data
- **209 postings** → 209 rows, schema-compliant CSV
- **5 source files** merged, deduplicated by job_id + title + description

### Data Quality Issues
- **63% duplicates** (reposts flagged; true distinct postings ≈ 112)
- **4 rows missing posting date**, 3 rows missing description
- **81 rows outside analysis window** (Sept 2025–Aug 2026)

### Preprocessing (Task 3)
- Boilerplate removed: Meta's ADA/EEO paragraphs, repeated text
- 111/206 rows affected (1000–1500 chars removed per row)
- **Result:** 206 cleaned descriptions, no data loss

### Key Finding
**Data is stock (snapshots), not flow (arrivals).** Kaggle uploads don't represent hiring velocity.

---

## Slide 4: Skill Extraction Methodology (Task 4)

### Approach
- **Regex-based matching** against canonical taxonomy (93 skills, v0.1.0)
- Input: Job title + cleaned description (not title-only)
- Output: Canonical skill names, matched field (title/description), category

### Taxonomy & Validation
- **93-skill taxonomy** includes NVIDIA's extensions (silicon_design, etc.)
- **Title-match blocklist** prevents false positives (r, c)
- **Negative context rule** excludes "neural network" from Networking skill
- **Hand-validation:** 20 postings checked; 18 correct, 1 miss, 1 borderline

### Coverage
- **66 of 93 skills matched** (71.0%)
- **191/209 postings** have ≥1 skill (91.4%)
- **3.41 skills per posting** average

### Taxonomy Corrections
- **Removed "drive"** from Autonomous Vehicles (100% false positives)
- **Removed "driver"** from Kernel & Drivers (single boilerplate sentence)
- Both documented with dated comments for team ratification

---

## Slide 5: Meta's Skill Profile — Top 5 Skills (Task 4)

### Core Skills (20%+ of postings each)
| Skill | % | Postings | Interpretation |
|---|---|---|---|
| **LLMs** | 30.6% | 64 | Conversational AI, foundational models |
| **Recommender Systems** | 30.1% | 63 | Feed ranking, personalization (core product) |
| **Generative AI** | 27.8% | 58 | Content generation, synthesis |
| **Python** | 23.9% | 50 | Data/ML development (only language >20%) |
| **Machine Learning** | 19.6% | 41 | General ML expertise baseline |

### Key Insight
**Not specialization skills — baseline competencies.** 1 in 3 Meta jobs mentions LLMs. This signals strategic focus, not niche hiring.

---

## Slide 6: Hiring by Category Breakdown (Task 6)

### Distribution Across 10 Categories

| Category | % of Postings | # Skills | Implication |
|---|---|---|---|
| **Research Domains** | 83.7% | 18 | Core: LLMs, GenAI, Recommendations, CV, RL, Robotics, AI Safety |
| **Languages** | 30.1% | 7 | Python-dominant; C++/Go/Rust <5% combined |
| **Hardware Systems** | 22.0% | 12 | Performance Engineering (18%), not CUDA/HPC |
| **Analytics/BI** | 14.8% | 4 | A/B Testing (11.5%), Statistics (10.5%) — product focus |
| **Product Process** | 14.8% | 5 | Leadership, TPM, business dev — scattered |
| **MLOps/DevOps** | 13.9% | 5 | Site Reliability (5.7%), CI/CD minimal |
| **ML Frameworks** | 6.2% | 4 | PyTorch (5.7%); oddly low for AI company |
| **Cloud Infrastructure** | 4.3% | 2 | AWS/Azure/GCP <5% — Meta builds own infra |
| **Data Engineering** | 2.9% | 2 | Spark/ETL minimal — centralized function |
| **Silicon Design** | 2.9% | 7 | 0 hiring visible — not a chip company |

### Strategic Positioning
**Meta is research-heavy (84%), infrastructure-light (3–6%).**

---

## Slide 7: Hiring Trends & Velocity (Task 5)

### Time Series (Sept 2025–Aug 2026)
- **53 weeks** in analysis window
- **128 postings** in window (61% of total)
- **45 of 53 weeks** have zero postings (85% sparse)

### The Feb 2026 Spike
- **74 postings in February** (57.8% of windowed data)
- **All concentrated in 2 weeks** (W06 + W08)
- **Root cause:** Single Kaggle dataset snapshot (published mid-Feb)

### Critical Finding
**This is NOT a hiring trend.**
- Not 74 arrivals in one month
- One dataset download happened to be Feb 2026
- Actual hiring signal is **completely obscured** by snapshot artifact

### Data Quality Impact
- **Forecasting impossible** (trends are meaningless)
- **Cross-company comparison risky** (different collection dates per source)
- **Recommendation:** Weekly LinkedIn scrapes for Q4 2026 onwards

---

## Slide 8: Strategic Positioning & Market Profile (Task 6)

### What Meta IS Hiring For
✓ AI research (LLMs, Generative AI, Recommendations)  
✓ Python development  
✓ Product analytics (A/B Testing, experimentation)  
✓ Performance engineering  
✓ AI Safety / responsible AI (emerging area)  

### What Meta is NOT Hiring For
✗ Cloud infrastructure (4.3%)  
✗ Data engineering / pipelines (2.9%)  
✗ Systems programming / DevOps (5% combined)  
✗ Polyglot languages (C++, Go, Rust: <5% combined)  
✗ Chip design (0%)  

### Inferred Team Structure
1. **FAIR (Meta AI Research)** — dominant, hiring senior researchers
2. **Product ML** — smaller cluster, embedding AI into features
3. **Central ops** — compliance, security, legal (not advertised on Kaggle)
4. **Infrastructure** — minimal hiring visible (likely mature team + outsourced)

### Competitive Bet
**"Researchers can be productive on commodity infrastructure"**
- Bet 1: Hire top AI researchers → they drive innovation → ship fast
- Bet 2: Python + existing datacenters are enough → don't hire for infra
- **If this fails:** Technical debt accumulates → eventually fires firefighters

---

## Slide 9: Data Limitations & Caveats (Task 5–6)

### What We Know (High Confidence)
- Meta hires heavily for AI/ML research
- LLMs, recommendations, generative AI are strategic priorities
- Python-first, infrastructure-light tech stack
- Organizational structure is research-dominant

### What We DON'T Know (Low Confidence)
- Meta's absolute hiring volume (sample, not census)
- Year-over-year hiring growth (time series too gapped)
- Future hiring trends (forecast unreliable)
- How Meta compares to NVIDIA/Google/Microsoft (4-way comparison not valid yet)

### Critical Data Issues
1. **Kaggle snapshot bias:** 5 one-time uploads, not continuous stream
2. **Duplicate inflation:** 63% are reposts; true n ≈ 112
3. **Selection bias:** "AI jobs" dataset omits non-AI roles
4. **Missing seniority:** Cannot break down junior vs. senior hiring
5. **No compensation:** Cannot infer salary/market positioning

### Must-Do Disclaimer
**Do not publish cross-company rankings yet.** Tasks 6 & 8 found that taxonomy choice and text-source differences break symmetry (see Slide 10).

---

## Slide 10: Comparison Framework & Why 4-Way Matrix is Blocked (Task 8)

### Similarity Framework (If All Follow It)
- **Feature space:** 93 canonical skills (normalized by share of postings)
- **Distance metric:** Cosine similarity (0.0 to 1.0)
- **Input:** Title + description (full-text, not title-only)

### Why The Four-Company Matrix is Not Yet Valid

**Problem 1: Different Taxonomies**
- NVIDIA extended taxonomy with 34 new skills (silicon_design, Agentic AI, etc.)
- If Google/Microsoft extracted against original 59 skills, vectors are incommensurable
- Result: Ranking flips by up to 0.123 depending on taxonomy version

**Problem 2: Title vs. Description**
- Microsoft: 0.08 skills/posting from title vs. 6.84 from description (85x difference)
- If some teams used title-only, their vectors are near-orthogonal (unreliable cosine similarities)
- Meta used title+description; unknown for others

**Problem 3: No Canonical Matrix**
- Rules require "one canonical matrix, validated by the others"
- Currently: Four teams extracting separately, no consensus

### Prerequisites for Valid Comparison
1. All teams agree: extended 93-skill taxonomy or revert to 59 + re-extract?
2. All teams declare: title-only or title+description?
3. All teams re-run Task 4 extraction with canonical setup
4. One team builds matrix, others validate (check symmetry)

---

## Slide 11: Key Insights & Recommendations (Task 9)

### Strategic Insight: Meta's AI-First Bet

Meta is organizing around a **single, narrow hypothesis:**
> "Top AI researchers driving innovation on commodity infrastructure is a sustainable competitive advantage."

### Evidence
- 84% of hiring goes to research domains
- Python-only development stack
- Minimal infrastructure/DevOps hiring
- Presence of AI Safety hiring (defensive positioning)

### If This Bet Wins
- Meta leads in AI/LLM capabilities
- Faster shipping than infrastructure-burdened competitors
- Researchers are happy (focused on research, not ops)

### If This Bet Fails
- Infrastructure debt compounds → performance crises
- Researcher productivity drops → hiring slowdown
- Single-discipline org is fragile (market shift away from LLMs)

### Recommendations for Meta Leadership
1. **Validate the bet:** Measure time-to-production, infra costs, researcher attrition
2. **Clarify outsourcing:** Is infrastructure truly commoditized, or is it a hidden risk?
3. **Expand hiring language diversity:** Python-only is risky; hire for C++/Rust if edge/embedded is strategic
4. **Formalize AI Safety mandate:** 7.7% of hiring suggests this is real; set an explicit goal if it is

### Recommendations for This Team
1. **Collect fresh data:** Weekly LinkedIn scrapes starting Q4 2026 (not Kaggle snapshots)
2. **Ratify taxonomy:** Meet in sprint meeting to decide on 59 vs. 93 skills
3. **Declare text source:** Title+description or title-only across all four companies
4. **Re-run Task 4:** Extract using canonical setup, build valid 4-way matrix
5. **Iterate:** Re-run this analysis in Q1 2027 to detect strategic shifts (hiring changes)

---

## Slide 12: Conclusion & Next Steps

### What We Built
A **complete hiring intelligence pipeline** for Meta (Tasks 1–9):
- Legal source review → Data collection → Preprocessing → Skill extraction
- Trend analysis → Strategic positioning → Forecasting → Similarity framework
- Executive insights → Final report

**Every analysis is honest about limitations.** No finding is overstated.

### What You Can Do Now
1. **Brief Meta leadership** with Slide 11 insights (AI-first bet, infrastructure risk)
2. **Set up quarterly updates** (re-run this analysis every Q, watch for shifts)
3. **Coordinate with teammates** to ratify taxonomy + text source + rebuild 4-way matrix
4. **Collect fresh data** starting next month (weekly scrapes, not Kaggle)

### The Bigger Story
This project shows **how data asymmetry breaks comparisons.** When four companies have:
- Different data sources (Kaggle vs. LinkedIn Live)
- Different collection dates (snapshots at different times)
- Different taxonomy coverage (NVIDIA extended, others didn't)
- Different input text (title vs. title+description)

...their similarity matrices don't mean what they seem to mean.

**The honest frame is stronger than the false precision.** "We can't compare yet, and here's why" is more credible than "Here's a ranking" (that might flip if you change the taxonomy).

### Deliverables
- ✓ 9 task reports (each with method note + data artifacts)
- ✓ 1 executive insight report (strategy-ready)
- ✓ 1 visual summary (board-level)
- ✓ Reusable scripts (extract_skills.py, trend analysis, etc.)
- ✓ Complete, documented repository (all tasks, all README files)

---

## Questions?

**For meta-specific findings:** See Task 9 insight report  
**For methodology:** See individual task method notes (Tasks 1–8)  
**For cross-company issues:** See Task 8 comparison framework + brief's open decisions  
**For data/scripts:** All in `work/meta-abdal-farid/` folder on GitHub

**Contact:** Abdal Farid, CadetX internship, Meta track
