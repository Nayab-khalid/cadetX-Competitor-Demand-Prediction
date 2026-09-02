# Data Collection Plan for Task 2

Written on: 2026-08-18
Agreed by the team on: YYYY-MM-DD (to be confirmed in the sprint 1 meeting)

## 1. Assignments

| Member | Company | Primary source | Access method | Secondary source |
|---|---|---|---|---|
| Nayab Khalid | NVIDIA | Aramente/eu-tech-jobs (CC BY-4.0), filtered to NVIDIA | Weekly snapshot download | Manual observation of the live careers page |
| Noorul Huda Batool | Google | _to be filled in by the owner_ | | |
| Arham Malik | Microsoft | S2 Microsoft Careers, subject to reading the Terms of Use first | Allowed paths `/careers`, `/careerhub/explore/jobs`, `/api/career_hub` | |
| Abdal Farid | Meta | _to be filled in by the owner_ | | |

Two companies cannot be collected from their own career sites:

- **Google**, because robots.txt disallows the paginated job results listing, so systematic
  collection is not permitted (S4).
- **NVIDIA**, because section 3.2 of NVIDIA's Terms of Service prohibits robots, scrapers, crawlers
  and data mining tools, even though the careers host's robots.txt permits the career-site path.
  Terms of Service take precedence over robots.txt (S1).

Both therefore planned to use the openly licensed Kaggle dataset as their primary source.
**Superseded for NVIDIA:** that dataset was tested in Task 2 and yields only 11 NVIDIA postings over a four-week window, so it was rejected and replaced by Aramente/eu-tech-jobs. See `work/task-2/nvidia-nayab-khalid/data-collection-report.md`, section 2. Microsoft remains
provisional until its Terms of Use have been read, and Anthropic is unaffected because the
Greenhouse Job Board API is published for public use.

## 2. The timing problem, and how the team handles it

A company career site shows the roles that are **open today**. It does not show a history of
postings. Three consequences follow, and every member must plan for them.

**a. A single snapshot cannot produce a time series.** Counting today's open roles gives one data
point, not the weekly series that Task 5 and Task 7 need.

**b. Posting dates inside a single snapshot are biased.** Roles posted months ago that have already
been filled are no longer listed, so the further back you look inside one snapshot, the fewer
postings you see. This is survivorship bias, and it looks exactly like a genuine hiring increase.
Any chart built from a single snapshot's posting dates must say so.

**c. Therefore the team collects forward, weekly.**

| Series | How it is built | Covers | Used for |
|---|---|---|---|
| Live weekly snapshot series | Every member collects their company's open roles on the same day each week and appends the rows with a `scraped_date` | 2026-08-25 onwards, approximately 11 to 12 weekly points by Task 7 | Primary series for hiring velocity, trends and forecasting |
| Posting-date history from the first snapshot | The posting dates present in the first collection | Roughly the preceding months, source dependent | Context only, always labelled as affected by survivorship bias |
| Historical monthly series | S5 Kaggle dataset filtered to the four companies | 2023 and 2024 | Validating the forecasting method on a longer series, and long-run comparison |

The three series are kept in separate files and are never concatenated into one column. The Kaggle
history is two years old relative to this project, so it supports method validation and long-run
context, not a claim about current demand.

**This applies differently to each member.** Arham (Greenhouse API) and Muhammad (Microsoft Careers)
can build the live weekly snapshot series, and Arham additionally has `first_published`, a genuine
publication timestamp. Nayab (NVIDIA) and Noorul Huda (Google) are working from the Kaggle dataset,
so their series is the historical monthly one covering 2023 and 2024, and they have no live series
to collect. Their trend and forecasting work is therefore a statement about 2023 and 2024, and every
chart they produce must say so. This asymmetry is a limitation of the project, not something to be
smoothed over in Task 6.

## 3. Collection schedule

Applies to the members with a live source, Arham (Anthropic) and Muhammad (Microsoft).

- Collection day: every Monday, starting Monday 2026-08-24, through the week of 2026-11-09.
- Each weekly collection is saved as its own file and appended to the member's cumulative dataset.
- A missed week is recorded as a gap in the Data Collection Report. It is never back-filled with an
  estimate.
- The Data Quality Lead of the week confirms in the meeting that all four members collected.

## 4. Shared standards

- Fields, names, order and formats follow [docs/data-schema.md](../../../docs/data-schema.md).
- `posting_date` is ISO-8601 `YYYY-MM-DD`. Relative dates such as "posted 30+ days ago" are not
  usable as a posting date; where a source only gives a relative date, the field is left empty and
  the limitation is recorded.
- `scraped_date` is mandatory for every row, because the weekly snapshot design depends on it.
- `job_id` is prefixed with the company, for example `nvidia_00123`, and is stable across weekly
  snapshots so that a repeated posting can be recognised.
- One file per company per stage, named `<company>_postings_raw_YYYYMMDD.csv`.
- Reposted roles are kept, not deduplicated, and flagged. Reposting is a real hiring signal.
- Every file passes `python scripts/validate_dataset.py <file>` before it is committed.

## 5. Field mapping to check before collecting

Each member confirms which schema fields their source actually provides, and records the gaps.

| Schema field | Microsoft Careers | Greenhouse API | Kaggle dataset |
|---|---|---|---|
| job_id | to confirm | `id` | to confirm |
| job_title | yes | `title` | yes |
| job_description | to confirm | with `?content=true` | yes |
| posting_date | to confirm | `first_published` | yes |
| location | yes | `location.name` | yes |
| job_url | yes | `absolute_url` | yes |

The Greenhouse API is the only source confirmed on 2026-08-18 to provide a genuine publication
timestamp. Members using the other sources must establish in Task 2 what date their source gives and
state it plainly.

## 6. Comparability risk

The four companies are not being collected from the same kind of source. One is a public API, two
are career sites, one is a third-party dataset. Volumes and field coverage will differ for reasons
that have nothing to do with hiring behaviour.

Controls:

- Every comparison in Task 6 and Task 8 is normalised as a share of that company's own postings, or
  per 1,000 postings. Raw counts are never compared across companies.
- All four members also extract their company's rows from the same Kaggle dataset. That gives one
  like-for-like cross-check where all four came from a single source.
- The source of every figure is stated in the chart or table.
- The limitation is written into the Task 9 report rather than left for the mentor to find.

## 7. Collection window for analysis

| Series | Start | End |
|---|---|---|
| Live weekly snapshots | 2026-08-24 | 2026-11-09 |
| Historical monthly | 2023-01-01 | 2024-12-31 |

The final window is confirmed in the sprint 2 meeting, once every member knows what their source
actually returns. It is then written into `shared/config/analysis_config.yaml` and not changed.

## 8. Risks

| Risk | Affected | Mitigation |
|---|---|---|
| Source returns too few postings for a time series | Anthropic, smallest of the four | Keep weekly snapshots running for the full project; report counts honestly rather than padding them |
| Career site is JavaScript-driven and hard to read | Microsoft | Use the published sitemap and the allowed API paths; if the allowed paths are insufficient, fall back to the Kaggle dataset and record the change |
| Source provides only relative posting dates | Microsoft | Leave `posting_date` empty, rely on `scraped_date` and the weekly snapshot design |
| Terms of Service prohibit automated access despite a permissive robots.txt | NVIDIA, and possibly Microsoft | Read the terms before collecting, not after; fall back to an openly licensed dataset and record the decision |
| robots.txt or terms change mid-project | All | Re-check at the start of Task 2 and before Task 10; stop and minute the decision |
| Kaggle dataset is two years old | Google especially | Use it for history and validation, not as evidence of current demand; state this in every chart that uses it |
| A member misses a collection week | All | Record the gap; the Data Quality Lead checks collection in the weekly meeting |

## 9. Deliverables for Task 2

Each member submits:

1. A Data Collection Report covering sources, legal checks, fields, method and limitations.
2. The raw dataset, schema compliant and validator clean.
3. Their company's rows extracted from the Kaggle cross-check dataset.

## 10. Deadline

To be agreed in the sprint 1 meeting. Suggested: Task 2 submitted by the end of sprint 3, so that
three weekly snapshots exist before the preprocessing work begins in Task 3.
