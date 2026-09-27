# CadetX Project: Competitor Demand Prediction Using Job Postings
## Aligned Team Presentation (4 Companies + Shared Insights)

**Duration:** 60–90 minutes  
**Audience:** Mentor + team (all 4 members)  
**Objective:** Present the full project workflow, data challenges, and per-company findings with honest framing

---

## Part 1: Sector Context (5 min) — Moderator Role

**Slide 1: Why We're Doing This**
- Hiring data is a leading indicator of company strategy
- Job postings signal: research priorities, team structure, tech stack, market positioning
- Question: Can we build a replicable pipeline to extract hiring intelligence at scale?

**Slide 2: The Data Challenge**
- No single "company hiring census" exists
- Alternative: Aggregate public job postings (LinkedIn, Kaggle, company careers pages)
- Trade-off: **Coverage vs. representativeness**
  - LinkedIn: most complete, but proprietary
  - Kaggle: public + shareable, but filtered/curated
  - Company careers: direct, but ToS restrictions (Meta blocked)

**Slide 3: Project Scope**
- **Objective:** Build hiring intelligence pipeline for 4 companies (NVIDIA, Google, Microsoft, Meta)
- **Timeline:** 10 tasks, 3 months, 1 team of 4 (rotating Scrum roles)
- **Output:** Per-company profile + cross-company comparison (if valid)

---

## Part 2: Data Realities — Each Company Presents Own Findings (45 min)

### Nayab's NVIDIA Deck (12 slides)
- Data: Job postings from NVIDIA careers + LinkedIn
- Key finding: Silicon design + GPU architecture dominate hiring
- Challenge: Limited dates; comparison requires fresh collection

### Noorul's Google Deck (12 slides)
- Data: [TBD — pending Google track completion]
- Expected finding: Cloud infrastructure + polyglot hiring

### Arham's Microsoft Deck (12 slides)
- Data: [TBD — pending Microsoft track completion]
- Challenge: Title-only data (no descriptions) makes skill matching unreliable

### Abdal's Meta Deck (12 slides) — THIS PROJECT
- Data: 209 postings from 5 Kaggle datasets
- Key finding: Research-AI-first (84%), infrastructure-light (3–4%)
- Challenge: Snapshots dominate; no real trend signal

---

## Part 3: What We Could NOT Compare (10 min) — Honest Framing

**The Asymmetry Problem**

Each company has:
- **Different data sources** (Kaggle snapshots vs. LinkedIn Live vs. company careers)
- **Different collection dates** (one snapshot on 2026-02-15, another on 2026-01-01)
- **Different text inputs** (NVIDIA: title+description vs. Microsoft: title-only)
- **Different taxonomy coverage** (NVIDIA extended from 59 → 93 skills; others didn't)

**Result:** A naive 4-company similarity matrix would be **invalid** (ranking flips if you change the taxonomy).

**Why This Matters:**
- If you publish "NVIDIA most similar to Microsoft (0.67 cosine similarity)"
- But Microsoft used title-only data and NVIDIA used title+description
- And NVIDIA has 93 dimensions while Microsoft has 59
- Then that ranking is **artifact, not insight**

**The Honest Framing:**
> "We built the pipeline. We extracted clean data. But we cannot compare companies fairly because they have different underlying data types and collection cadences. Here's what we'd need to fix that, and it's worth doing."

---

## Part 4: What We CAN Say (Per-Company Only) (15 min)

### NVIDIA (Nayab)
- Hiring heavily for silicon design + GPU architecture
- Strong presence of systems languages (C++, Rust)
- Hardware-forward positioning

### Google (Noorul — TBD)
- [Pending Google track completion]
- Likely: Broad tech stack (polyglot)
- Strong cloud infrastructure + data engineering

### Microsoft (Arham — TBD)
- [Pending Microsoft track completion]
- Title-only data limits confidence in skill extraction
- Trade-off: fewer skills matched, but data collection is clean

### Meta (Abdal)
- **Research-AI-first:** 84% of jobs require ML/AI expertise
- **Python-only hiring:** 24% Python, <5% for any other language
- **Infrastructure risk:** Betting researchers can be productive on commodity infrastructure
- **Bet is working so far:** Data shows this is intentional, coherent strategy

---

## Part 5: What We'd Do With Another Month (10 min) — Recommendations

### High-Priority Actions
1. **Agree on shared taxonomy:**
   - Use the 93-skill extended version (NVIDIA's additions) as canonical
   - OR revert to 59 and all four teams re-extract
   - Current: NVIDIA has 93, others have 59 → incomparable

2. **Declare text source:**
   - All teams: title+description (consistent extraction)
   - OR all teams: title-only (honest about sparsity)
   - Current: NVIDIA (title+desc) vs. Microsoft (title-only) → 85x difference in skill density

3. **Re-run extraction with canonical setup:**
   - All four teams re-run Task 4 using same taxonomy + same text source
   - Takes ~1 week per team

4. **Build ONE similarity matrix:**
   - One team builds, three teams validate (check symmetry)
   - Publish with full caveat: "Valid only if all used same taxonomy/text source"

5. **Collect fresh data:**
   - Weekly LinkedIn scrapes for all 4 companies (starting Q4 2026)
   - Gives ~20 real weekly observations by end of year
   - Can then extract real hiring trends (not snapshots)

### Medium-Priority
- Survey non-tech roles (HR, finance, legal, ops) for each company
- Add compensation data (salary ranges) if possible
- Run quarterly re-analysis to catch strategic shifts

---

## Part 6: Lessons Learned (10 min) — Meta-Discussion

### What Worked
✓ **Clear task structure:** 10 tasks → 10 decision points (clear gates)  
✓ **Shared taxonomy:** Prevents local skill lists; enables comparison  
✓ **Reusable scripts:** extract_skills.py runs from clean checkout  
✓ **Honest framing:** Every report flags limitations up-front  

### What Was Hard
✗ **Data sourcing:** Kaggle is convenient but not representative (snapshots, not streams)  
✗ **Cross-company coordination:** Easy to extract in isolation; hard to align for comparison  
✗ **Naming:** Skill names like "driver" and "drive" are genuinely ambiguous (regex can't tell)  
✗ **Taxonomy stability:** Extending it mid-project breaks all prior comparisons  

### What We'd Do Differently
1. **Start with fresh collection:** Weekly LinkedIn scrapes for 3+ months before analysis
2. **Agree on taxonomy first:** Week 1 of project, all 4 teams ratify 59 vs. 93 decision
3. **Declare text source first:** Week 1, all 4 teams confirm title-only vs. title+description
4. **Weekly syncs:** All 4 members sync on extraction decisions (not waiting until Task 4)
5. **Monthly re-validation:** Check if the 4 vectors are actually comparable (monthly audit)

---

## Part 7: Q&A + Wrap (5 min)

**For mentors / stakeholders:**
- This project proves: **Hiring intelligence pipelines are feasible, but data alignment matters more than sophistication**
- The most interesting finding: **How similar four tech companies' hiring looks (research-dominant for all?), assuming clean data**
- The most valuable lesson: **Honest framing of data limitations is stronger than false precision**

**For next cohort:**
- Reuse the 9 task structure (it's modular, can fork at any point)
- Start with data collection, not Kaggle
- Ratify shared decisions by week 1

---

## Appendix: Key Artifacts (Per-Company)

| Task | Nayab (NVIDIA) | Noorul (Google) | Arham (Microsoft) | Abdal (Meta) |
|---|---|---|---|---|
| 1. Sources | ✓ Done | [ ] | [ ] | ✓ Done |
| 2. Collection | ✓ Done | [ ] | [ ] | ✓ Done |
| 3. Preprocessing | ✓ Done | [ ] | [ ] | ✓ Done |
| 4. Skills | ✓ Done | [ ] | [ ] | ✓ Done |
| 5. Trends | ✓ Done | [ ] | [ ] | ✓ Done |
| 6. Profile | ✓ Done | [ ] | [ ] | ✓ Done |
| 7. Forecast | ✓ Done | [ ] | [ ] | ✓ Done |
| 8. Similarity | ✓ Done (flagged invalid) | [ ] | [ ] | ✓ Done (flagged invalid) |
| 9. Insights | ✓ Done | [ ] | [ ] | ✓ Done |
| 10. Presentation | ✓ Done (12 slides) | [ ] | [ ] | ✓ Done (12 slides) |

---

**Status:** ✓ Slides ready for mentor review  
**Next:** Team sprint meeting to ratify taxonomy + text source + plan Q4 actions
