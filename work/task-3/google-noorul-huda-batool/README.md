# Task 3 – NLP Preprocessing & Method Selection By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset — Google + YouTube postings)

## 1. Input
`../job_skills.csv` — the raw dataset carried over from Task 2, 1,250 records, fields: `Company, Title, Category, Location, Responsibilities, Minimum Qualifications, Preferred Qualifications`.

## 2. Preprocessing Workflow (`preprocess.py`)
1. **Deduplication** — Task 2 identified 123 exact full-row duplicates in the raw dataset but intentionally left the raw file untouched. Task 3 is where they're dropped (`drop_duplicates()`), since carrying duplicates forward would double-count postings in every trend, forecast, and comparison table in later tasks. 1,250 → **1,127** unique postings.
2. **Stable IDs** — each surviving row gets a `job_id` (`JOB00000` …) so Task 4/5 outputs can be joined back to it.
3. **Missing values** — `Responsibilities` / `Minimum Qualifications` / `Preferred Qualifications` (14–15 nulls each, as flagged in Task 2 §7) filled with `""` rather than dropped; a posting is still usable for skill/category analysis without one section.
4. **Concatenation** — `Title + Responsibilities + Minimum Qualifications + Preferred Qualifications` merged into one `raw_text` document per posting.
5. **Text cleaning** (`basic_clean`) — lowercase, strip URLs/emails/newlines, remove punctuation *except* `+ # . / -` (kept so `c++`, `c#`, `node.js`, `ci/cd` survive as single tokens), collapse whitespace.
6. **Tokenize → stopword removal → lemmatize** — NLTK `word_tokenize`, English stopword list (with `c`, `r`, `go` explicitly kept — a generic filter would otherwise eat these valid short language names), `WordNetLemmatizer`.
7. **Simulated `posting_date`** — see Limitation below.

## 3. Output
`cleaned_job_postings.csv` — 1,127 rows × `job_id, Company, Title, clean_title, Category, Location, posting_date, posting_year_month, posting_date_is_simulated, Responsibilities, Minimum Qualifications, Preferred Qualifications, raw_text, clean_text, tokens, token_count`.

**Result:** 1,127/1,127 rows processed successfully, 0 empty `clean_text` rows, ~139 tokens/posting on average.

## 4. Method Choices & Why
- **NLTK over spaCy** — the dataset is small (1,127 rows post-dedup) and this task only needs tokenize/stopword/lemma; spaCy's fuller pipeline (POS/NER/parser) is reserved for optional NER-assisted skill extraction in Task 4 if needed.
- **Lemmatization, not stemming** — qualification text uses varied verb forms ("managing/manages/managed"); lemmatization keeps terms readable for the shared skill taxonomy used across the team's four companies in Task 4.
- **Punctuation partially retained** — a full punctuation strip turns `c++` → `c` and `node.js` → `node js`, corrupting skill matching downstream. The cleaning regex allowlists the characters that actually appear inside tech-skill tokens.

## 5. Limitation — Simulated `posting_date`
The Google Job Skills dataset (Kaggle, scraped from Google Careers, CC BY-NC-SA 4.0 — see Task 1) is a static snapshot with **no posting-date field**, and this gap was not caught in Task 1/2. Tasks 5 (Hiring Trend Analysis) and 7 (Demand Forecasting) require a time series, so this script generates a **seeded, reproducible synthetic `posting_date`** (uniform over Jan 2023–Dec 2024, with mild category-level skew so engineering/infra/data categories trend later) purely to demonstrate trend/forecasting methodology consistently. Every file that carries this column also carries `posting_date_is_simulated = True`, and this limitation is repeated in the Task 5, 7, and 9 write-ups. **It is not real hiring-velocity data** — a production version of this pipeline would use actual collection timestamps captured at scrape time.

## Task 3 Outcome
Preprocessing pipeline implemented and run end-to-end: **1,127 unique postings cleaned**, tokenized, and lemmatized, with a documented, reproducible synthetic date field added to unblock the time-series tasks later in the pipeline. Code and output are ready for Task 4 (Skill Extraction & Feature Engineering).
