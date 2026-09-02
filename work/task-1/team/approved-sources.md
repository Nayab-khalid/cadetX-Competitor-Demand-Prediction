# Approved Data Sources

Reviewed on: 2026-08-18
Agreed by the team on: YYYY-MM-DD (to be confirmed in the sprint 1 meeting)

A source appears in the approved list only after the checklist in
[docs/legal-checklist.md](../../../docs/legal-checklist.md) has been completed and dated. Every
robots.txt line quoted below was read on the date shown and must be re-checked before Task 2
collection begins.

## Summary

| # | Source | Type | Verdict | Used by |
|---|---|---|---|---|
| S1 | NVIDIA External Career Site (Workday) | Company career site | Rejected, Terms of Service prohibit automated access | - |
| S2 | Microsoft Careers | Company career site | Provisional, robots.txt permits, terms not yet read | Muhammad Hasnain |
| S3 | Greenhouse Job Board API (Anthropic) | Public documented API | Approved | Arham Malik |
| S4 | Google Careers | Company career site | Rejected for systematic collection | - |
| S5 | Kaggle: LinkedIn Job Postings 2023-2024 | Public dataset, CC BY-SA 4.0 | Approved | Nayab Khalid (primary), Noorul Huda Batool (primary), all (cross-check) |
| S6 | Hugging Face: lukebarousse/data_jobs | Public dataset, Apache-2.0 | Approved, backup only | All |
| S7 | Adzuna API | Commercial API | Rejected | - |
| S8 | Cedefop Skills-OVATE | EU aggregated statistics | Approved, context only | All |

## S1. NVIDIA External Career Site (Workday)

- URL: `https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite`
- Type: first-party company career site, hosted on Workday
- robots.txt checked: 2026-08-18 at `https://nvidia.wd5.myworkdayjobs.com/robots.txt`

```
Sitemap: https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/siteMap.xml

User-agent: *
Allow: /NVIDIAExternalCareerSite/
Disallow: /talentcommunity/
Disallow: /refreshFacet/
```

- `https://www.nvidia.com/robots.txt` checked 2026-08-18: `Allow: /` for all user agents, with a
  content signal permitting search and AI crawling. The careers section is not disallowed.
- Personal data: job postings only. No applicant or recruiter data is exposed on the allowed path.

**Terms of Service, read 2026-08-18** at `https://www.nvidia.com/en-us/about-nvidia/terms-of-service/`:

- Section 3.2, Use Restrictions, prohibits using any robot, spider, scraper, crawler, data mining
  tool or other automatic device or methodology to access, acquire, copy or monitor the site, and
  prohibits reproducing or circumventing the site's navigational structure by automated means.
- Section 3.1, License Grant, permits downloading a single copy of materials for personal,
  non-commercial internal use only.

- **Verdict: rejected for automated collection.** robots.txt permits crawling the career-site path,
  but the Terms of Service prohibit the automated tools that Task 2 would require. Where the two
  disagree, the Terms of Service govern. Manual reading of the public careers page, with aggregate
  observations only and no bulk copying, remains permitted and is used as a current-state check.
  NVIDIA posting data is taken from S5 instead. Full reasoning is in Nayab Khalid's source review.

## S2. Microsoft Careers

- URL: `https://apply.careers.microsoft.com` (`https://jobs.careers.microsoft.com` returns
  HTTP 301 to this host, confirmed 2026-08-18)
- Type: first-party company career site
- robots.txt checked: 2026-08-18 at `https://apply.careers.microsoft.com/robots.txt`

```
User-agent: *
Disallow: /
Allow: /$
Allow: /careers
Allow: /api/apply
Allow: /api/pcsx
Allow: /candidate/login
Allow: /login
Allow: /events/candidate
Allow: /events/open
Allow: /api/events
Allow: /careerhub/explore/jobs
Allow: /api/career_hub
Allow: /static/gen
Allow: /gen
```

- The site is disallowed by default. Only the explicitly allowed paths may be requested, and of
  those only `/careers`, `/careerhub/explore/jobs` and `/api/career_hub` are relevant to this
  project.
- `/api/apply`, `/candidate/login` and `/login` are allowed by robots.txt but are **out of scope by
  team decision**: they relate to applications and accounts, and touching them risks personal data.
- **Outstanding check:** Microsoft's Terms of Use have not yet been read. The NVIDIA review showed
  that a permissive robots.txt can sit alongside terms that prohibit automated access, and the terms
  govern. This source is not confirmed until the owning member has read and dated them.
- **Verdict: provisional.** Permitted by robots.txt for `/careers`, `/careerhub/explore/jobs` and
  `/api/career_hub`, subject to the Terms of Use check above.

## S3. Greenhouse Job Board API (Anthropic)

- Endpoint: `https://boards-api.greenhouse.io/v1/boards/anthropic/jobs`
  (add `?content=true` to return the full job description)
- Documentation: `https://developers.greenhouse.io/job-board.html`
- Type: public, documented, unauthenticated API operated by the applicant tracking system that
  Anthropic uses to publish its own vacancies. This is the same API that powers the careers page.
- Checked 2026-08-18: the endpoint returns a JSON `jobs` array. Fields observed on a job object:
  `id`, `internal_job_id`, `requisition_id`, `title`, `location`, `absolute_url`, `company_name`,
  `updated_at`, `first_published`, `application_deadline`, `language`, `metadata`,
  `data_compliance`.
- robots.txt checked 2026-08-18 at `https://job-boards.greenhouse.io/robots.txt`: every directive
  in the file is commented out, so no crawl restriction is declared.
- `https://www.anthropic.com/robots.txt` checked 2026-08-18: `User-Agent: *` with `Allow: /`.
- Personal data: none. The response describes vacancies, not people.
- **Verdict: approved.** This is the strongest source in the set: first-party, structured, no
  extraction required, and it supplies `first_published`, which gives a genuine posting date.

## S4. Google Careers

- URL: `https://www.google.com/about/careers/applications/jobs/results`
- robots.txt checked: 2026-08-18 at `https://www.google.com/robots.txt`. The following lines apply:

```
Disallow: /about/careers/applications/candidate-prep
Disallow: /about/careers/applications/connect-with-a-googler
Disallow: /about/careers/applications/jobs/results?page=
Disallow: /about/careers/applications/jobs/results/?page=
Disallow: /about/careers/applications/jobs/results?*&page=
Disallow: /about/careers/applications/jobs/results/?*&page=
Disallow: /about/careers/applications-a/jobs/results
```

- The paginated results listing is disallowed. Because pagination is the only way to enumerate the
  full set of vacancies, systematic collection from this site cannot be done within robots.txt.
- **Verdict: rejected for systematic collection.** Google job-posting data will be taken from the
  approved public datasets (S5, S6) instead. This decision and its consequence for comparability
  are recorded in the collection plan.

## S5. Kaggle: LinkedIn Job Postings (2023-2024)

- URL: `https://www.kaggle.com/datasets/arshkon/linkedin-job-postings`
- Licence: **CC BY-SA 4.0** (confirmed 2026-08-18). Attribution and share-alike are required.
- Size: approximately 531 MB across multiple CSV files; over 124,000 postings from 2023 and 2024.
- Contents: job postings with title, description, salary, location, work type and application URL,
  plus separate company and benefit files.
- **Caveat, and it matters:** the data originates from LinkedIn, whose User Agreement prohibits
  automated collection. The CC BY-SA licence was applied by the uploader, not by LinkedIn. The team
  did not collect this data and is not bound by an agreement it never entered, but the provenance is
  not clean.
- Controls applied: used as a **secondary and historical source only**, never as the sole basis for
  a company's analysis; filtered to the four companies in scope; any column that could identify a
  person is dropped on load; Kaggle and the dataset author are credited; derived outputs are shared
  under the same licence.
- **Verdict: approved as a secondary source** under the controls above.

## S6. Hugging Face: lukebarousse/data_jobs

- URL: `https://huggingface.co/datasets/lukebarousse/data_jobs`
- Licence: **Apache-2.0** (confirmed 2026-08-18).
- Size: approximately 786,000 rows covering 2023, aggregated from several job boards.
- Columns include `job_title`, `company_name`, `job_location`, `job_posted_date`, `job_skills`,
  `salary_year_avg`, `job_schedule_type`.
- Limitation: it carries extracted skills rather than the full job description text, so it cannot be
  the input to the NLP work in Task 3 and Task 4. It is useful as a volume and skill benchmark.
- **Verdict: approved as a backup and benchmarking source only.**

## S7. Adzuna API

- URL: `https://developer.adzuna.com`
- Free tier: 1,000 calls per month.
- Restriction found on 2026-08-18: academic use is permitted only for a 14-day trial to validate
  coverage and quality. Ongoing research use, including aggregated vacancy counts and average
  salaries, requires written consent. Displayed listings must carry an Adzuna attribution label.
- **Verdict: rejected.** A three-month project cannot run on a 14-day trial, and the team has no
  written consent. If a member wants to use it, consent must be obtained in writing first and this
  entry updated.

## S8. Cedefop Skills-OVATE

- URL: `https://www.cedefop.europa.eu/en/tools/skills-online-vacancies`
- Type: EU institution tool analysing online job advertisements across 28 European countries, using
  ISCO-08, NACE Rev. 2, NUTS-2 and ESCO classifications, updated quarterly.
- Limitation: it publishes aggregated indicators for occupations, skills and regions, not individual
  company postings, so it cannot support company-level comparison.
- **Verdict: approved as background and sector context only.** Useful in Task 9 to place the four
  companies against the wider European skill demand picture.

## Rejected sources

| Source | Reason for rejection |
|---|---|
| NVIDIA External Career Site, automated collection | Terms of Service section 3.2 prohibits robots, scrapers, crawlers and data mining tools, despite a permissive robots.txt |
| Google Careers, systematic collection | robots.txt disallows the paginated results listing |
| Adzuna API | Academic use limited to a 14-day trial; ongoing research needs written consent |
| Any LinkedIn, Indeed or Glassdoor collection by the team | Their terms prohibit automated collection. Data derived from them is used only through an openly licensed third-party dataset, and only as a secondary source |

## Conditions attached to approved sources

| Source | Condition |
|---|---|
| S1 NVIDIA | No automated requests of any kind. Manual reading of the public careers page only, aggregate observations, no bulk copying |
| S2 Microsoft | Terms of Use must be read and dated before collection. Requests limited to `/careers`, `/careerhub/explore/jobs`, `/api/career_hub`; no application or login endpoints |
| S3 Greenhouse | Reasonable request rate; public job board endpoints only |
| S5 Kaggle | Attribution to Kaggle and the dataset author; share-alike on derived outputs; secondary use only |
| S6 Hugging Face | Attribution; not used as NLP input because it lacks description text |
| S8 Cedefop | Cited as the source of any aggregate figure quoted |

## Re-check requirement

robots.txt and terms can change. Every source is re-checked at the start of Task 2 and again before
the final submission in Task 10. If a source becomes restricted, collection from it stops and the
decision is recorded in the meeting minutes.
