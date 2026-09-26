# Task 3: NLP Preprocessing Note — Meta

Member: Abdal Farid
Date: 2026-09-06

## Method choice

For this stage, cleaning is done with **plain Python + regex + pandas**, not a heavier NLP library (spaCy/NLTK). Reasoning:

- Task 3's job is text *cleaning and structuring*, not linguistic analysis — tokenisation, lemmatisation, and skill extraction are Task 4's job, done on top of `cleaned_description`.
- The actual noise in this dataset (checked by inspecting the raw text directly, not assumed) was: repeated company boilerplate (EEO/accommodation disclaimers), salary text embedded inline in some rows, and no HTML tags or raw URLs. A rules-based pass handles all of that precisely and predictably, which matters for a dataset multiple team members will later join on `cleaned_description` fairness — a heavier library would add processing variance without solving a problem this data actually has.
- No dependency beyond pandas keeps the script runnable top-to-bottom from a clean checkout with no extra installs.

## Pipeline steps (in order, per row)

1. **Missing-source check** — if `job_description` is empty/NaN, the row is kept, `cleaned_description` is set to null, and it's logged as `missing_source`. Row is never dropped.
2. **HTML tag / URL stripping** — regex removal of any `<...>` tags or `http(s)://` links (none were found in this dataset, but the step runs for every row regardless, for repeatability).
3. **Boilerplate block removal** — two known, verified patterns are stripped:
   - Meta's standard ADA/accommodation-request paragraph (ends in `accommodations-ext@fb.com` / `@meta.com`)
   - Meta's Equal Employment Opportunity disclaimer paragraph
4. **Embedded salary text removal** — inline strings like `"$177,000/year to $247,000/year + bonus + equity + benefits"` are stripped from the description text (salary is already captured structurally in the `salary_range` column from Task 2; leaving it duplicated in free text would skew any later text-based analysis).
5. **Whitespace normalisation** — collapses repeated whitespace/newlines to single spaces, trims ends.
6. Every step records **which patterns actually matched**, per row, in the removal log — nothing is stripped silently.

## Rows in / rows out reconciliation

| | Count |
|---|---|
| Rows in | 209 |
| Rows out | 209 |
| Rows dropped | **0** |
| Status: `cleaned` | 206 |
| Status: `missing_source` (no `job_description` to clean; row kept, `cleaned_description` = null) | 3 |
| Status: `empty_after_cleaning` (text existed but reduced to nothing) | 0 |

No rows were dropped at any point. The full per-row log (`job_id`, status, which cleaning rules fired, raw/cleaned character length) is committed as `meta_cleaning_log_20260906.csv`.

## Boilerplate removal, quantified

- 111 of 206 non-missing rows had at least one boilerplate/salary pattern removed.
- Typical removal size: **1,000–1,500 characters** per affected row (verified by comparing raw vs. cleaned length directly — e.g. one row went from 5,378 → 3,913 characters, entirely from removing the EEO + accommodation + salary blocks).
- 95 rows had no boilerplate matches and passed through with whitespace normalisation only.

## Hand validation

A stratified sample of 6 rows was manually inspected end-to-end (raw text vs. cleaned text, in full, not just the first N characters):

- **3 rows with boilerplate matches** (`meta_00180`, `meta_00106`, `meta_00095`) — confirmed the EEO/accommodation/salary blocks were correctly removed from the end of the text, and that the cleaned text still ends on a real, meaningful content sentence (not mid-sentence truncation). No over-removal of legitimate role-description content was found.
- **2 rows with no matches** (`meta_00123`, `meta_00036`) — confirmed cleaned text is identical to raw text (modulo whitespace normalisation), i.e. the pipeline correctly leaves already-clean postings alone rather than altering them unnecessarily.
- **1 missing-source row** (`meta_00203`) — confirmed it is retained in the output with `cleaned_description` = null and correctly logged as `missing_source`, not silently dropped.

**What this caught:** the pipeline reliably identifies and removes Meta's two standard boilerplate paragraphs and inline salary text without damaging real job-description content, and correctly distinguishes "nothing to clean" from "cleaned to empty" from "no source text at all" — three different states that matter differently for Task 4's skill extraction.

**What it does not attempt:** deeper NLP normalisation (lowercasing, stopword removal, lemmatisation) is deliberately left for Task 4, since different skill-extraction approaches (keyword match vs. embeddings) want different levels of normalisation, and doing it here would remove that choice from Task 4.

## Limitations

- Boilerplate patterns were built by inspecting Meta's actual postings and may not generalise to other companies' boilerplate wording — this is expected and fine, since each member is cleaning their own company's text, but it's worth the team confirming in Task 6 that "cleaned" means a comparable level of noise removal across companies, not necessarily identical rules.
- `cleaned_description` is null for the 3 rows with no source description — any Task 4 skill-extraction step will need to explicitly handle nulls (e.g. fall back to `job_title` only, or exclude from text-based metrics while keeping the row for count-based metrics).
- Salary text was deliberately removed from the description rather than merely flagged, since Task 2 already captures salary structurally in `salary_range` — if a future task wants raw salary phrasing, it is only available in the raw (pre-Task-3) dataset, not here.

## Library versions

- Python 3.12.3
- pandas 3.0.2
- Standard library `re` (regex) — no version, built in

## Code

Committed as `preprocess.py`. Runs top to bottom from a clean checkout with:

```
python preprocess.py meta_postings_raw_20260906.csv meta_cleaned_20260906.csv meta_cleaning_log_20260906.csv
```

Only dependency is `pandas` (already required by earlier tasks). No other setup needed.
