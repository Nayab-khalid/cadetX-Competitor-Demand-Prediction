# Task 2 Data Collection Note - Microsoft (REVISED)

Member: Arham Malik (Microsoft) | Revised: 2026-10-26

## Why this revises the earlier submission

The dataset committed previously fails `scripts/validate_dataset.py`:

    ERROR  PERSONAL DATA - email addresses found: row 47, row 67, row 114

Three job descriptions contain `askstaff@microsoft.com`. `docs/data-schema.md`
is explicit: never collect an email, "not even in a spare column - it fails the
ethics criterion outright."

**The earlier report stated that no contact information was present. That was
wrong.** It claimed all 182 records had been inspected; the check was not
thorough enough to catch an address inside description text.

It also did not follow `docs/data-schema.md`, alignment lock #1, in three ways:
raw numeric `job_id` instead of the `microsoft_00001` form, semicolon-separated
strings where the schema asks for JSON lists, and required columns not in the
documented order.

`conform_to_team_schema.py` fixes all of it. Addresses are replaced with
`[EMAIL REDACTED]` rather than deleted silently, so a reviewer can see that a
redaction happened. The validator now passes on everything except
`posting_date`.

## Source

| | |
|---|---|
| Repository | github.com/microsoft/SkillsExtractorCognitiveSearch |
| File | `deployment/microsoft_careers_sample.json` |
| Publisher | Microsoft Corporation |
| Licence | MIT |
| Records | 182 |

Microsoft's careers site disallows automated access - a direct programmatic
request to a live posting URL was refused. No public dataset of Microsoft
postings was found: a 33,246-row LinkedIn dataset was tested and contained zero
Microsoft-employer postings, the apparent matches being consultancies hiring for
Microsoft technologies.

Microsoft publishes these 182 postings itself, under MIT, as sample data for an
Azure skills-extraction demo. No scraping, no licence ambiguity.

## Fields

| Required field | Status |
|---|---|
| job_id | complete, `microsoft_00001` form |
| company_name | complete |
| job_title | complete |
| job_description | complete, mean 3,941 chars, no truncation |
| posting_date | **empty - not in source** |
| location | state level only |
| job_url | reconstructed from the source id |

`source_job_id` is retained because Microsoft requisition IDs are sequential,
which Task 5 uses as an ordinal time axis.

## Limitations

- **No posting dates.** Constrains Tasks 5 and 7. Team-wide: Nayab's Task 6 note
  records that no cross-company time series is possible regardless.
- **Engineering only.** All 182 are engineering roles.
- **181 of 182 are Washington state.** No regional analysis.
- **A sample, not a census.** Volumes are not market share.
- **Job URLs are reconstructed** from ids and were not validated, because the
  careers site blocks automated requests.

## Validator

    $ python scripts/validate_dataset.py work/task-2/microsoft-arham-malik/microsoft_postings_raw_20261026.csv
    rows            182
    unique job_ids  182
    company_name    Microsoft
    ERROR  182 rows have an empty required field: posting_date

The remaining error cannot be fixed from this source. Flagged for the meeting
rather than worked around.
