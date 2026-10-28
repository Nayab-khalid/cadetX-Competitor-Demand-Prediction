# Source Review: Microsoft

Member: Arham Malik
Task 1: Understanding Data Sources and Legal
Date: 2026-08-28

Summarised from `Task1_DataSources_Legal_Microsoft.docx` in this folder, which is the submitted
Task 1 report. That report is dated 2026-08-28 but does not record a separate date for each check,
so every check below is dated "by 2026-08-28". Where the report did not record evidence the
checklist asks for, such as a quoted Terms of Service clause, this file says so and does not fill
it in after the fact.

## Source 1

- Name: microsoft/SkillsExtractorCognitiveSearch, `deployment/microsoft_careers_sample.json`
- URL: https://github.com/microsoft/SkillsExtractorCognitiveSearch
- Type: GitHub
- Licence: MIT, Copyright (c) Microsoft Corporation

Checks:

- [x] Terms of Service read by 2026-08-28 - the repository's MIT licence governs reuse
- [x] robots.txt checked by 2026-08-28 - not applicable, the file is downloaded from a public repository and nothing is crawled
- [x] Extraction or download of the required data is permitted
- [x] Licence and attribution requirements understood - the copyright notice is kept, and the source is recorded in the `data_source` column of every row
- [x] Copyright position understood - Microsoft published the descriptions for recruitment and re-released them under MIT
- [ ] Contains no personal or sensitive data - **see correction below**

Terms of Service, relevant clause:

> MIT License, Copyright (c) Microsoft Corporation. Permits use, copying, modification and
> distribution, provided the copyright notice is retained.

robots.txt, relevant lines:

```
Not applicable - single file download from GitHub, no crawling.
```

Fields available: id, title, description, category, subCategory, state, targetLevel.

Limitations: no posting dates; Engineering roles only; 181 of 182 in Washington state; a sample
Microsoft published as demo data, not a census.

**Correction (2026-10-26).** The Task 1 and Task 2 reports both said all 182 records had been
inspected and held no contact details. That was wrong: three descriptions contain
`askstaff@microsoft.com`. The committed dataset now replaces them with `[EMAIL REDACTED]` - see
`../../task-2/microsoft-arham-malik/data-collection-note.md`. The box above stays unticked because it
describes the source, and the source does contain an address.

Verdict: approved, because Microsoft itself publishes it under a permissive licence and no scraping
is involved. Primary dataset, 182 postings with full description text.

## Source 2

- Name: Microsoft careers site
- URL: https://jobs.careers.microsoft.com
- Type: company career page
- Licence: proprietary

Checks:

- [ ] Terms of Service read - the report states no automated collection was made and that manual browsing is permitted, but quotes no clause
- [x] robots.txt checked by 2026-08-28 - a direct programmatic request to a live posting URL was refused with a robots-disallowed response
- [ ] Extraction or download of the required data is permitted - **no**, automated access is disallowed
- [x] Licence and attribution requirements understood
- [x] Copyright position understood
- [x] Contains no personal or sensitive data - not collected

Terms of Service, relevant clause:

> Not quoted in the Task 1 report.

robots.txt, relevant lines:

```
Not pasted in the Task 1 report. Recorded result: automated request to a live posting URL
refused, robots-disallowed.
```

Fields available: live postings with dates.

Limitations: automated access blocked.

Verdict: rejected for automated collection. Manual browsing only, for spot checks and verifying
job URLs. Under the team checklist, a disallowed careers path means the source is rejected.

## Source 3

- Name: Wayback Machine archives of Microsoft careers pages
- URL: https://web.archive.org
- Type: public archive
- Licence: public archive, research use

Checks:

- [ ] Terms of Service read - not recorded
- [ ] robots.txt checked - not recorded
- [ ] Extraction or download of the required data is permitted - not yet confirmed
- [ ] Licence and attribution requirements understood
- [ ] Copyright position understood
- [x] Contains no personal or sensitive data - archived public listings only

Terms of Service, relevant clause:

> Not recorded.

robots.txt, relevant lines:

```
Not recorded.
```

Fields available: historical snapshots of careers pages, which could recover approximate posting
dates.

Limitations: never attempted. Listed in the Task 1 report as a way to recover dates for Task 5.

Verdict: proposed, not yet used. The checks above must be completed before any collection.

## Source 4

- Name: LinkedIn Job Postings dataset (Hugging Face / Kaggle), 33,246 rows
- URL: not recorded in the Task 1 report
- Type: public dataset
- Licence: MIT

Checks:

- [x] Terms of Service read by 2026-08-28 - MIT-licensed dataset
- [x] robots.txt checked by 2026-08-28 - not applicable, dataset download
- [x] Extraction or download of the required data is permitted
- [x] Licence and attribution requirements understood
- [x] Copyright position understood
- [x] Contains no personal or sensitive data - not used

Terms of Service, relevant clause:

> MIT licence.

robots.txt, relevant lines:

```
Not applicable - dataset download.
```

Fields available: cross-market postings.

Limitations: verified to contain **zero** Microsoft-employer postings. The apparent matches were
consultancies hiring for Microsoft technologies.

Verdict: approved but not usable for Microsoft. Excluded from the Microsoft dataset.

## Source 5

- Name: LinkedIn Jobs (live site)
- URL: https://www.linkedin.com/jobs
- Type: company career page / job board
- Licence: proprietary

Checks:

- [x] Terms of Service read by 2026-08-28 - the report records that the ToS prohibits scraping; no clause quoted
- [ ] robots.txt checked - not recorded
- [ ] Extraction or download of the required data is permitted - **no**
- [x] Licence and attribution requirements understood
- [x] Copyright position understood
- [x] Contains no personal or sensitive data - not collected

Terms of Service, relevant clause:

> Not quoted in the Task 1 report. Recorded result: scraping prohibited.

robots.txt, relevant lines:

```
Not recorded.
```

Fields available: live postings.

Limitations: scraping prohibited.

Verdict: rejected for automated collection. Manual spot checks only.

## Recommendation

The source I will use in Task 2 for Microsoft, and the reason for choosing it:

Source 1, `microsoft/SkillsExtractorCognitiveSearch`. Microsoft runs its own careers platform
instead of a third-party applicant-tracking system with a public API, and that platform blocks
automated access. Microsoft's own GitHub organisation publishes 182 real postings under MIT as demo
data for an Azure skills-extraction project. That gives full description text through a channel
Microsoft itself opened, with no scraping and no licence ambiguity. Its known gaps are no posting
dates and an Engineering-only, Washington-heavy sample, which are carried into Task 2.
