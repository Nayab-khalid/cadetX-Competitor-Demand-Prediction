# Task 2: Data Collection

## Objective

Collect job-posting data for your company using only the sources approved in Task 1. Verify that
extraction is allowed, that robots.txt does not block it, and that no personal data is included.

## What is submitted

**Each member (in their own folder)**

1. A short Data Collection Report: sources, legal checks, fields, limitations
2. The raw collected dataset

## Rules for this task

- Columns, names and formats follow [docs/data-schema.md](../../docs/data-schema.md), not whatever
  the source happens to return.
- Dates are ISO-8601, `YYYY-MM-DD`.
- One file per company, named `<company>_postings_raw_YYYYMMDD.csv`.
- `python scripts/validate_dataset.py <file>` is run before committing, and its output is pasted
  into the report.
- No personal data. Any identifying column is dropped before the file is saved.
- Every source is re-checked against its terms and robots.txt before collection begins.

## Definition of done

- [ ] Dataset committed, in the team schema
- [ ] Data Collection Report committed, including the validator output
- [ ] Limitations stated honestly, including anything that will affect Tasks 5 and 7
- [ ] Row count, date range and coverage reported
- [ ] Result reviewed by one other member

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Anthropic | [ ] | |
| Muhammad Hasnain | Microsoft | [ ] | |

## Open team decisions raised by this task

1. **Description text is not available for every company.** NVIDIA's data carries none. The team
   must decide whether Tasks 3 and 4 run on job titles for everyone, so the comparison stays fair,
   or whether members work with different input richness and document it.
2. **There is no single dataset holding all four companies at usable volume.** The shared comparison
   basis proposed in the Task 1 collection plan does not exist in practice. See section 8 of
   [Nayab's report](nvidia-nayab-khalid/data-collection-report.md).
3. **Company names need canonicalising on load.** NVIDIA appears under 11 distinct employer strings
   in one source tested. Exact-match filtering silently loses rows.

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
