# Source Review: NVIDIA

Member: Nayab Khalid
Company: NVIDIA
Task 1: Understanding Data Sources and Legal
Date of review: 2026-08-18

## Summary

Four candidate sources were reviewed for NVIDIA job-posting data. The finding that decided the
outcome is that **NVIDIA's own Terms of Service prohibit automated extraction from its site, even
though the careers host's robots.txt permits crawling of the career-site path**. Where robots.txt
and the Terms of Service disagree, the Terms of Service govern, so the career site cannot be used
for automated collection.

| # | Source | Licence or terms | Verdict |
|---|---|---|---|
| 1 | NVIDIA External Career Site (Workday) | NVIDIA ToS section 3.2 prohibits automated tools | Rejected for automated collection |
| 2 | Kaggle: LinkedIn Job Postings 2023-2024 | CC BY-SA 4.0 | **Approved, primary source** |
| 3 | Hugging Face: lukebarousse/data_jobs | Apache-2.0 | Approved, benchmark and backup |
| 4 | Adzuna API | Academic use limited to a 14-day trial | Rejected |

Primary source for Task 2: **Source 2**, filtered to NVIDIA, with Source 3 as a cross-check and
manual, non-automated observation of the live careers page as a current-state sanity check.

---

## Source 1: NVIDIA External Career Site (Workday)

- Name: NVIDIA External Career Site
- URL: `https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite`
- Landing page: `https://www.nvidia.com/en-us/about-nvidia/careers/`
- Type: first-party company career site, hosted on Workday
- Licence: none offered. Site content is proprietary.

### Checks

- [x] Terms of Service read on 2026-08-18
- [x] robots.txt checked on 2026-08-18 (both hosts)
- [ ] Extraction or download of the required data is permitted — **no**
- [x] Licence and attribution requirements understood
- [x] Copyright position understood
- [x] Contains no personal or sensitive data

### robots.txt evidence

`https://nvidia.wd5.myworkdayjobs.com/robots.txt`, read 2026-08-18:

```
Sitemap: https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/siteMap.xml

User-agent: *
Allow: /NVIDIAExternalCareerSite/
Disallow: /talentcommunity/
Disallow: /refreshFacet/
```

`https://www.nvidia.com/robots.txt`, read 2026-08-18: a single `User-agent: *` block with `Allow: /`,
and a content signal permitting search and AI crawling. Nothing disallows the careers section.

On robots.txt alone, the career-site path would be permitted.

### Terms of Service evidence

`https://www.nvidia.com/en-us/about-nvidia/terms-of-service/`, read 2026-08-18.

- **Section 3.2, Use Restrictions**, prohibits using any robot, spider, scraper, crawler, data
  mining tool or other automatic device or methodology to access, acquire, copy or monitor the site.
  It also prohibits reproducing or circumventing the site's navigational structure by automated
  means or an equivalent manual process, and prohibits placing an unreasonable load on the site's
  infrastructure.
- **Section 3.1, License Grant**, permits downloading a single copy of materials for personal,
  non-commercial internal use only. It does not authorise redistribution.
- **Section 4, Ownership**, confirms NVIDIA retains its intellectual property rights and that no
  further licence is implied.

(Summarised, not quoted at length. Section references are given so the clauses can be checked.)

### Assessment

A permissive robots.txt is a crawling instruction, not a grant of permission. The Terms of Service
are the contractual position, and they prohibit exactly the activity Task 2 would require. The
career site is therefore rejected for automated collection.

Two secondary points, recorded for completeness:

- The career site is served from `nvidia.wd5.myworkdayjobs.com`, a Workday-operated host rather than
  `nvidia.com`. Whether the nvidia.com terms formally extend to that host is arguable. The team's
  rule is that where the position is arguable, the source is treated as not permitted.
- Section 3.1 does permit a person to download a single copy of materials for personal,
  non-commercial internal use. Reading the live careers page manually and recording aggregate
  observations, such as how many AI and hardware roles are open in a given week, stays within that
  permission and involves no automated tool. This is used only as a sanity check, not as the dataset.

### Verdict

**Rejected for automated collection.** Manual, non-automated observation of the public careers page
is retained as a current-state validation step, with no bulk copying and no automated requests.

---

## Source 2: Kaggle, LinkedIn Job Postings (2023-2024)

- Name: LinkedIn Job Postings (2023 - 2024), published by Arsh Koneru
- URL: `https://www.kaggle.com/datasets/arshkon/linkedin-job-postings`
- Type: public dataset on an open dataset platform
- Licence: **CC BY-SA 4.0**, confirmed 2026-08-18. Attribution and share-alike required.

### Checks

- [ ] Kaggle Terms of Use read — **outstanding.** The terms page could not be retrieved on
      2026-08-18. To be read and dated before collection begins in Task 2.
- [x] Dataset licence confirmed on 2026-08-18
- [x] Download of the data is permitted under the stated licence
- [x] Licence and attribution requirements understood
- [x] Copyright position understood
- [ ] Contains no personal or sensitive data — **to be verified on the actual files**

### What the dataset contains

- Approximately 531 MB across several CSV files, covering more than 124,000 postings from 2023
  and 2024.
- Posting-level fields include title, description, location, work type, salary and application URL.
  Separate files carry company details and benefits.
- NVIDIA rows are extracted by filtering on company name. The row count available for NVIDIA is not
  yet known and is the first thing to establish in Task 2.

### Provenance concern

The data originates from LinkedIn, whose User Agreement prohibits automated collection. The CC BY-SA
licence was applied by the uploader, not by LinkedIn. I did not collect this data and am not party
to LinkedIn's agreement, but the provenance is not clean and I will not present it as if it were.

Controls I will apply:

- The dataset is described in every report and chart as third-party derived, with its licence stated.
- Kaggle and the dataset author are credited; anything I derive from it is shared under CC BY-SA 4.0.
- Only NVIDIA rows are retained. Everything else is discarded on load.
- Any field that could identify a person is dropped before the file is saved, and the file is run
  through `python scripts/validate_dataset.py` before it is committed.

### Limitations

- The data covers 2023 and 2024. Relative to this project in 2026 it is historical, so it supports
  trend analysis, method validation and long-run comparison, but it is not evidence about NVIDIA's
  current hiring.
- Coverage depends on what was captured from LinkedIn at the time, so it is a sample of NVIDIA's
  postings, not a complete record.
- The full description text is present, which is what makes it usable for the NLP work in Task 3 and
  Task 4. No other approved source gives me that.

### Verdict

**Approved as the primary source for NVIDIA**, subject to reading the Kaggle Terms of Use and
confirming the absence of personal data in the actual files, both before Task 2 collection.

---

## Source 3: Hugging Face, lukebarousse/data_jobs

- URL: `https://huggingface.co/datasets/lukebarousse/data_jobs`
- Type: public dataset
- Licence: **Apache-2.0**, confirmed 2026-08-18. Attribution required.

### Checks

- [x] Licence confirmed on 2026-08-18
- [x] Download permitted under the licence
- [x] Attribution requirement understood
- [ ] Contains no personal or sensitive data — to be verified on the files

### Assessment

Approximately 786,000 rows covering 2023, aggregated from several job boards. Fields include job
title, company name, location, posted date, salary and extracted skills.

The limitation that decides its role: it carries **extracted skills rather than full description
text**, so it cannot be the input to my NLP preprocessing in Task 3 or my own skill extraction in
Task 4. Using it as the primary source would mean inheriting somebody else's skill extraction and
having nothing of my own to evaluate.

### Verdict

**Approved as a benchmark and backup source.** Its value is as an independent check on my Task 4
skill extraction: if my extracted skills for NVIDIA roles diverge sharply from this dataset's, that
is a signal to re-examine my method.

---

## Source 4: Adzuna API

- URL: `https://developer.adzuna.com`
- Type: commercial job-search API with a free developer tier
- Terms reviewed: 2026-08-18

### Assessment

The free tier allows 1,000 calls per month. Academic use is permitted only for a 14-day trial
period, to validate coverage and quality. Continued use for research, including aggregated vacancy
counts and average salaries, requires written consent. Displayed listings must carry an Adzuna
attribution label.

A three-month project cannot be run on a 14-day trial, and I have no written consent.

### Verdict

**Rejected.** If the team later wants this source, written consent must be obtained first and this
review updated.

---

## Sources not pursued

| Source | Reason |
|---|---|
| LinkedIn, Indeed, Glassdoor collected directly | Their terms prohibit automated collection. Their data reaches this project only through an openly licensed third-party dataset, as a documented secondary source |
| Google Careers, Microsoft Careers | Not my company. Reviewed by the members who own them |
| Cedefop Skills-OVATE | Publishes aggregated European indicators, not company-level postings. Useful as sector context in Task 9, not as a source for NVIDIA |

---

## Approved sources and download links

Everything downstream in Tasks 2 to 9 comes from the two datasets below.

| Source | Link | Licence | Role |
|---|---|---|---|
| Kaggle: LinkedIn Job Postings 2023-2024 | https://www.kaggle.com/datasets/arshkon/linkedin-job-postings | CC BY-SA 4.0 | Primary, filtered to NVIDIA rows |
| Hugging Face: lukebarousse/data_jobs | https://huggingface.co/datasets/lukebarousse/data_jobs | Apache-2.0 | Cross-check on skill extraction |
| NVIDIA careers page | https://www.nvidia.com/en-us/about-nvidia/careers/ | Read manually under ToS 3.1 | Current-state sanity check only |

### Downloading the primary dataset

```bash
pip install kaggle
kaggle datasets download -d arshkon/linkedin-job-postings
```

Place the `kaggle.json` API token in `%USERPROFILE%\.kaggle\` first, then unzip into
`work/task-2/nvidia-nayab-khalid/data/raw/`. The archive holds a main postings file plus company
and benefit lookup files; exact file names and row counts are recorded in the Task 2 Data
Collection Report after download rather than assumed here.

### Downloading the cross-check dataset

Single file: https://huggingface.co/datasets/lukebarousse/data_jobs/resolve/main/data_jobs.csv

```python
import pandas as pd
url = "https://huggingface.co/datasets/lukebarousse/data_jobs/resolve/main/data_jobs.csv"
df = pd.read_csv(url)
nvidia = df[df["company_name"].str.contains("NVIDIA", case=False, na=False)]
```

### Two checks that must close before downloading

1. Kaggle's Terms of Use (https://www.kaggle.com/terms) could not be retrieved on 2026-08-18. Read
   and date them before collection begins.
2. Verify the absence of personal data column by column on the downloaded files, then confirm with
   `python scripts/validate_dataset.py`.

---

## Recommendation for Task 2

**Primary source:** Kaggle LinkedIn Job Postings (2023-2024), CC BY-SA 4.0, filtered to NVIDIA.
It is the only approved source that gives me full job description text, which the NLP work in
Tasks 3 and 4 depends on, and it gives real posting dates across 24 months, which the trend analysis
in Task 5 and the forecasting in Task 7 depend on.

**Cross-check:** Hugging Face `lukebarousse/data_jobs`, filtered to NVIDIA, to validate my skill
extraction against an independently produced skill list.

**Current-state check:** manual observation of the public NVIDIA careers page, recording aggregate
counts only, with no automated requests and no bulk copying. This is used to comment on whether the
historical picture still looks representative, and is clearly labelled as a manual observation.

**Before collecting, I will:**

1. Read and date the Kaggle Terms of Use.
2. Re-check both robots.txt files and the NVIDIA Terms of Service, and record the dates.
3. Confirm the NVIDIA row count and date coverage in the dataset, and report it honestly even if it
   is smaller than expected.
4. Inspect the columns for personal data and drop anything identifying before saving.
5. Run `python scripts/validate_dataset.py` on the extracted file and commit the output with my Data
   Collection Report.

**Known limitation to carry into Task 9:** my NVIDIA data is historical and third-party derived,
because NVIDIA's own terms rule out collecting from the primary source. Any statement I make about
NVIDIA's hiring is a statement about 2023 and 2024, not about today, and I will say so rather than
let a chart imply otherwise.
