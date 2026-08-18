# Data Collection Plan for Task 2

Agreed by the team on: YYYY-MM-DD

## Assignments

| Member | Company | Approved source to be used | Expected fields | Target volume |
|---|---|---|---|---|
| Nayab Khalid | NVIDIA | | | |
| Noorul Huda Batool | Google | | | |
| Arham Malik | Anthropic | | | |
| Muhammad Hasnain | Microsoft | | | |

## Shared standards

- Fields, column names and formats follow `docs/data-schema.md`.
- Dates are recorded as YYYY-MM-DD.
- One file per company, named `<company>_postings_raw_YYYYMMDD.csv`.
- Every dataset is checked with `python scripts/validate_dataset.py <file>` before it is committed.

## Collection period

The same date range is used by all four members, so the trend analysis in Task 5 is comparable.

Agreed range: YYYY-MM-DD to YYYY-MM-DD

## Risks

| Risk | Affected member | Mitigation |
|---|---|---|
| Source does not permit extraction | | Use an approved alternative |
| Too few postings available | | Widen the date range or add a second approved source |
| Missing posting dates | | Record as a limitation in the Data Collection Report |

## Deadline

To be agreed in the sprint 1 meeting.
