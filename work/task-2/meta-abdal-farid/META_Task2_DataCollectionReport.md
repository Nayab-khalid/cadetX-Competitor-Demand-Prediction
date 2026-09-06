# Data Collection Report: Meta

Member: Abdal Farid
Task 2: Data Collection
Date: 2026-09-06

## Sources used

Full legal review is in `META_Task1.md` (Task 1 doc). Summary:

- **Meta's own careers page (metacareers.com)** — considered and **rejected**. Meta's Terms of Service prohibit automated data collection without prior written permission; `robots.txt` also disallows several relevant paths (`/login/`, `/internal/`, `/resume/`, etc.).
- **5 licensed Kaggle datasets**, combined and filtered for Meta/Facebook postings only:
  1. LinkedIn Job Postings (2023–2024) — `arshkon/linkedin-job-postings` — CC BY-SA 4.0
  2. LinkedIn Jobs and Skills (2024) — `asaniczka/1-3m-linkedin-jobs-and-skills-2024` — ODC Attribution License (ODC-By)
  3. AI Job Market Global 2026 — `atharvasoundankar/ai-job-market-global-2026` — CC BY-NC-SA 4.0 (non-commercial clause — acceptable for this educational project)
  4. AI & ML Job Postings — LinkedIn & Indeed (2025) — `ankit0017/ai-and-ml-job-postings-linkedin-and-indeed-2025` — CC BY 4.0
  5. Job Listing Dataset — `sweetymahale/job-listing-dataset` — MIT

All 5 sources' licences and terms were re-checked on 2026-09-06, immediately before this collection pass, confirming permission for reuse in an educational/research context with attribution.

## Legal checks

- Licence read and confirmed for all 5 Kaggle sources (screenshots taken from each dataset page).
- `robots.txt` not applicable to the Kaggle sources — data obtained via Kaggle's own publish/download mechanism, not by scraping the original job boards directly.
- Meta's own `robots.txt` and ToS were re-checked; still the reason its own site is excluded as a direct source.
- No personal or candidate-identifying data included. One borderline item checked explicitly: `job_description` text contains Meta's standard boilerplate ADA-accommodation contact line (`accommodations-ext@meta.com` / `accommodations-ext@fb.com`) in 85 of 209 rows — this is Meta's own generic company mailbox, not an individual's or recruiter's personal email, and is treated as acceptable under the "no personal data" rule. Flagged here for reviewer visibility rather than silently left in.
- No phone numbers or personal names detected in any field (checked programmatically).

## Collection and schema-mapping method

1. Downloaded all 5 Kaggle datasets and filtered each to Meta/Facebook rows only, using exact-name matching with a regex fallback and an explicit blocklist to exclude lookalike company names (e.g. "Metasys", "Imetalx", "Meta4") — this directly addresses the team's open question about company-name canonicalisation.
2. Combined the 5 filtered files: **209 raw matched rows**.
3. Mapped all fields into the shared schema (`docs/data-schema.md`):
   - `company_name` canonicalised to exactly one value: `Meta` (source data mixed "Meta" and "Facebook" — both mapped to the single canonical value per the schema's alignment-lock rule).
   - `posting_date` converted to strict ISO-8601 `YYYY-MM-DD` (source dates were a mix of text dates and Unix millisecond timestamps).
   - `posting_week` / `posting_month` derived from `posting_date`.
   - `job_id` assigned as `meta_00001`–`meta_00209`.
   - Recommended fields populated where the source data supported them: `employment_type`, `seniority_level`, `salary_range`, `extracted_skills` (as JSON list), `scraped_date`.
4. **Duplicates were not removed.** Per the schema rule ("reposts are real signal — keep them, but flag them"), a boolean `is_duplicate_posting` column was added instead, flagging rows that share an identical `job_title` + `job_description` with another row in the file. **131 of 209 rows are flagged.**
5. Kept raw — no text cleaning or normalisation applied to `job_description`; that is explicitly scoped to Task 3.

## Validator output

`python scripts/validate_dataset.py meta_postings_raw_20260906.csv`

```
TODO: run this script yourself once you have repo access and paste its real output here before committing. I do not have access to your repo's scripts/ folder and cannot run it for you.
```

## Fields available

Required (schema-complete): `job_id, company_name, job_title, job_description, posting_date, location, job_url`
Recommended (partial, source-dependent): `employment_type, seniority_level, salary_range, extracted_skills, company_industry, scraped_date, posting_week, posting_month`
Extra (not in shared schema, kept for transparency): `is_duplicate_posting`

## Row count, date range, coverage

- **209 rows** (raw, not deduplicated — see duplicate-flagging note above)
- Date range: **2024-01-13 to 2026-06-21**
- Missing values in required fields: `job_description` missing in 3 rows, `posting_date` missing in 4 rows, `job_url` missing in 132 rows (roughly two of the five source datasets did not provide a posting URL field)
- `is_duplicate_posting = True` for 131 rows — likely the same postings appearing across more than one of the 5 merged source datasets

## Limitations (including effects on Tasks 5 and 7)

- **Date coverage gap:** a significant gap exists between September 2024 and August 2025, with data otherwise concentrated in two dense clusters (April 2024, February 2026). This will affect **Task 5 (trend analysis)** and **Task 7 (forecasting)** — continuous month-by-month trend lines across the gap will not be meaningful; recommend treating the two clusters as separate comparison snapshots, or the team sourcing a supplementary dataset to cover the gap period.
- **`job_url` missing for 132/209 rows** — limits traceability/validation for roughly two-thirds of postings.
- **High duplicate-flag rate (131/209, ~63%)** — the real number of *distinct* postings is closer to 112; this affects any row-count-based velocity metric in Task 5, which should likely be computed on de-duplicated counts even though raw rows are kept here.
- **`job_description` availability is not universal** — 3 rows have none. This is a smaller gap than what NVIDIA's dataset apparently has (per the team's open decision #1); worth the team aligning on whether Tasks 3–4 run on title-only text for fairness, or document differing input richness per company.
- Sub-source #3 (CC BY-NC-SA 4.0) restricts commercial use of that portion of the data — noted for the team, not a blocker for this educational project.

## Deliverable

Raw collected dataset: `meta_postings_raw_20260906.csv` (209 rows, schema-compliant column names/order, ISO-8601 dates, UTF-8, duplicates flagged not removed).
