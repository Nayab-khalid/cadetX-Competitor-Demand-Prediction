# Task 4 – Skill Extraction & Feature Engineering By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

## 1. Method
Keyword/regex extraction against a **shared skill taxonomy** (`skill_taxonomy.json`), run over Task 3's `clean_text` field (the punctuation-aware cleaned text, matched *before* stopword removal so multi-word phrases like "machine learning" and "project management" stay intact).

Chosen over spaCy NER / embeddings because:
- The taxonomy is explicit and auditable — every match is traceable to a rule, which matters when the team has to align a **shared taxonomy across four companies'** datasets for fair comparison in Task 6.
- No training data or model download needed, so teammates can run this against their own company's cleaned CSV with zero setup differences.
- Regex handles the symbol-heavy tech tokens (`c++`, `c#`, `ci/cd`) that a plain bag-of-words / NER model tends to mangle.

## 2. Taxonomy (`skill_taxonomy.json`)
97 skills grouped into 9 categories: **Programming Languages, Data & Machine Learning, Cloud & Infrastructure, Databases, Web & Frameworks, Security, Business & Soft Skills, Hardware & Manufacturing, Education & Certifications.** Structure is `category -> skill_name -> [regex variants]`, designed to be dropped in unchanged against the other companies' cleaned datasets so skill counts stay directly comparable.

## 3. Outputs
| File | Shape | Contents |
|---|---|---|
| `extracted_skills.csv` | long | `job_id, skill, skill_category, job_category` — one row per (posting, skill) match |
| `skill_features.csv` | wide | `job_id` × 97 binary skill columns + 9 `cat_*_count` rollups + `total_skills_matched` + Company/Category/Location/posting_date |
| `skill_frequency.csv` | summary | `skill, skill_category, postings_mentioning, pct_of_postings`, sorted descending |
| `category_skill_counts.csv` | summary | job `Category` × `skill_category` mention counts, for the taxonomy-vs-role-category cross-tab |

## 4. Results (Google, 1,127 postings)
- 1,118 / 1,127 postings (99.2%) matched at least one taxonomy skill; avg **7.24 skills/posting**.
- Top matched skills: `bachelors_degree` (74.5%), `sales` (42.3%), `cross_functional_collaboration` (37.6%), `marketing` (34.6%), `strategic_planning` (30.4%), `stakeholder_management` (29.8%), `google_cloud` (24.1%), `computer_science_degree` (23.6%), `leadership` (23.2%), `consulting` (22.6%).
- Business/soft-skill terms dominate the top of the table because Google's postings span Sales, Program Management, Marketing, and Partnerships roles alongside engineering — this is itself a Task 5/6 signal (Google's hiring mix isn't purely technical) and is called out in the Task 9 insight report.

## Task 4 Outcome
Shared, reusable skill taxonomy built and applied end-to-end: **97 skills extracted across 1,127 postings** into long-format, wide-format, and summary feature tables, ready for Task 5 (trend analysis) and Task 6 (cross-company comparison).
