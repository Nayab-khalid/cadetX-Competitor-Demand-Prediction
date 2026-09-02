# Data Collection Report - NVIDIA

Member: Nayab Khalid
Company: NVIDIA
Task 2: Data Collection
Date of collection: 2026-09-02

## Summary

1,745 distinct NVIDIA job postings were collected across 12 weekly observations, 2026-05-13 to
2026-09-02, from an openly licensed public dataset. The dataset supports the trend, comparison and
forecasting work in Tasks 5 to 7 well. It does **not** contain job description text, so the NLP
work in Tasks 3 and 4 must run on job titles and structured fields rather than full descriptions.

The plan written in Task 1 did not survive contact with the data. Both sources approved there were
tested and rejected, and the source actually used was found during collection. Section 2 records
what happened, because the reasoning matters more than the tidy answer.

| Item | Value |
|---|---|
| Distinct postings | 1,745 |
| Observation window | 2026-05-13 to 2026-09-02 (12 weekly observations) |
| Open roles per observation | 395 to 433, mean 416 |
| Postings opened / closed in window | 1,579 / 1,561 |
| Status at final observation | 413 active, 1,332 closed |
| Job description text | **0 of 1,745** |
| Validator result | FAILED, 2 errors, both on the missing `job_description` field |

## 1. Source used

| | |
|---|---|
| Dataset | Aramente/eu-tech-jobs |
| URL | https://huggingface.co/datasets/Aramente/eu-tech-jobs |
| Licence | **CC BY-4.0** (attribution required) |
| Publisher | Independent maintainer, published on Hugging Face |
| Origin of the NVIDIA rows | NVIDIA's public Workday careers feed, collected by the dataset maintainer |
| Company key | `nvidia-workday` |
| Coverage used | `snapshots/<date>/jobs.parquet`, sampled weekly |
| Accessed | 2026-09-02 |

The dataset publishes a daily snapshot of open roles for a curated list of technology employers,
with a companion `companies.parquet` describing each employer. NVIDIA is present as
`nvidia-workday`, described as a "Major Workday-hosted employer with EU offices".

## 2. Why the Task 1 sources were not used

Task 1 approved the Kaggle LinkedIn Job Postings dataset as the primary source and the Hugging Face
`lukebarousse/data_jobs` dataset as a cross-check. Both were tested at the start of Task 2 and both
failed, for reasons that were not visible from their dataset descriptions.

**Kaggle, LinkedIn Job Postings 2023-2024.** The dataset description says it covers 2023 and 2024,
which I read in Task 1 as a 24-month history. It is not. It is a single snapshot of about 124,000
LinkedIn postings captured over roughly four weeks. Filtered to NVIDIA it yields **11 postings**,
all first listed between 2026-03-15 and 2026-04-11 in the mirror examined. Eleven postings over four
weeks cannot support hiring-trend analysis or forecasting.

Tested by downloading the openly accessible mirror `MichaelYitzchak/LinkedInJobPostings`
(`postings.csv`, 517 MB uncompressed, 123,849 rows), which carries the same schema as the Kaggle
release plus a `company_name` column. The Kaggle account token was therefore never the obstacle;
the data itself is too thin for NVIDIA.

**Hugging Face, lukebarousse/data_jobs.** 785,741 rows, Apache-2.0, downloaded and inspected in
full. Filtered to NVIDIA it yields **271 postings** across 12 months of 2023, which is a usable
monthly series, but it carries no description text and covers only data-family roles: 93 software
engineer, 43 data scientist, 31 senior data engineer and so on. It represents a slice of NVIDIA's
hiring, not NVIDIA's hiring. It also proved unusable as the shared cross-company basis proposed in
the Task 1 plan, because Anthropic appears in it only 9 times against Google's 752 and Microsoft's
646.

A data-quality point worth carrying to the team from this test: NVIDIA appears there under 11
different employer strings, including `NVIDIA`, `Nvidia`, `NVIDIA Corporation`, and entity codes
such as `CN05 NVIDIA Shanghai WFOE` and `IN02 NVIDIA GraphicsPLtd,Pune`. Any member filtering on an
exact company name will silently lose rows.

**Sources also tested and rejected.** `edwarddgao/open-apply-jobs` (MIT, daily parquet from
Greenhouse, Ashby and Lever) is an excellent source with full descriptions, but contains no NVIDIA
data at all: NVIDIA publishes through Workday, and that dataset covers only those three applicant
tracking systems. It does carry OpenAI, Anthropic, Databricks and Snowflake, so it is worth raising
with the team for the members whose companies use those platforms.

## 3. Legal checks

| Check | Result |
|---|---|
| Licence of the dataset used | CC BY-4.0, confirmed 2026-09-02 via the dataset's card metadata |
| Attribution requirement | Recorded in the `source` column of every row and cited in this report |
| Automated access to NVIDIA's own site | Not performed. NVIDIA's Terms of Service section 3.2 prohibits it, as established in Task 1 |
| Personal data | None collected. No field in the source carries applicant or recruiter information |
| Validator PII scan | Clean. No email addresses or telephone numbers detected |
| Bypassing technical controls | None. All files were downloaded from the dataset's public HTTPS endpoints |

**Provenance, stated plainly.** The NVIDIA rows in this dataset originate from NVIDIA's Workday
feed, which NVIDIA's own Terms of Service prohibit *me* from collecting automatically. I did not
collect it; a third party did, and published the result under CC BY-4.0. Under the team rule agreed
in Task 1, section 7 of the legal rules, this is third-party derived data: it is used as a
documented secondary source, labelled as such in every output, and never presented as a first-party
collection. This is the same position the team took on the LinkedIn-derived datasets.

## 4. Method

The collection is reproducible by running [`collect_nvidia.py`](collect_nvidia.py). Three decisions
in it are worth stating.

**Snapshots, not diffs.** The dataset also ships daily diff files. They are not used. Across the
whole dataset the diff stream carries `new`, `removed` and `changed` events, but for NVIDIA it
carries only `new`: 8,797 `new` events for 2,029 distinct postings, the same posting re-announced up
to 18 times and never once marked removed. Flow figures derived from it would be fiction. The
snapshots are internally consistent, so first-seen and last-seen are derived from them instead.

**Weekly sampling.** 126 daily snapshots are available. Sampling every 7th day gives 19 candidate
observations and keeps the download near 350 MB rather than 2.4 GB, and weekly ISO buckets are
already the team standard in `shared/config/analysis_config.yaml`.

**Partial scrapes excluded.** 7 of the 19 sampled observations returned far fewer NVIDIA rows than
the rest and were excluded as failed collections on the source's side, not as real collapses in
hiring: 2026-04-29 (0 rows), 2026-05-27 (9), 2026-06-03 (9), 2026-05-06 (57), 2026-07-22 (66),
2026-07-15 (168) and 2026-06-17 (171), against a median of about 416. The rule applied is stated in
the script: exclude any observation below 60 per cent of the median. 12 observations remain.

Job identifiers were verified as stable before deriving flows: between the 2026-08-27 and
2026-09-02 snapshots, all 311 postings whose URL appears in both carry the same id in both, so
appearances and disappearances reflect real openings and closures rather than churning keys.

## 5. Files produced

| File | Rows | Size | Contents |
|---|---|---|---|
| `data/raw/nvidia_postings_raw_20260902.csv` | 1,745 | 753 KB | **The dataset.** One row per distinct posting, 25 columns, in the team schema |
| `collect_nvidia.py` | - | - | The collection script, re-runnable from a clean checkout |

There is deliberately **one** dataset file. An earlier draft also shipped a separate weekly series,
but that was an aggregate of this file at a different grain, and shipping two files invited the
question of which one is the submission. The weekly series is now generated on demand by the script
and is exactly reconstructable from the `observed_dates` column, verified observation by
observation across all 12 weeks.

The naive reconstruction does not work and the column exists because of it. Postings disappear and
reappear between observations, so treating `first_seen` to `last_seen` as a continuous open span
overcounts the stock: it gives 499 open roles on 2026-06-10 against a true 430. Storing the exact
observation dates on which each posting was present makes the series recoverable without error.

### Field coverage in the posting-level file

| Field | Populated | Note |
|---|---|---|
| `job_id`, `company_name`, `job_title`, `job_url` | 1,745 / 1,745 | Complete |
| `posting_date` | 1,745 / 1,745 | Proxy, see limitations |
| `location` | 1,745 / 1,745 | But 96 per cent are collapsed, see limitations |
| `job_category` | 878 / 1,745 | engineering 655, ml-ai 87, sales 35, research 26, ops 23 |
| `seniority_level` | 662 / 1,745 | senior 573, principal 32, junior 19, mid 18, exec 8, intern 7, staff 5 |
| `first_seen`, `last_seen`, `weeks_observed`, `job_status` | 1,745 / 1,745 | Derived by this script |
| `observed_dates` | 1,745 / 1,745 | JSON list of the exact observation dates the posting was present |
| **`job_description`** | **0 / 1,745** | The source carries none for NVIDIA |
| `tech_stack_tags`, `countries`, `salary_*`, `employment_type` | 0 / 1,745 | Empty in the source for NVIDIA |

### Weekly series

Generated from the dataset's `observed_dates` column.

| Observation | ISO week | Open roles | New | Closed | Net |
|---|---|---|---|---|---|
| 2026-05-13 | 2026-W20 | 395 | - | - | - |
| 2026-05-20 | 2026-W21 | 411 | 109 | 93 | +16 |
| 2026-06-10 | 2026-W24 | 430 | 266 | 247 | +19 |
| 2026-06-24 | 2026-W26 | 417 | 132 | 145 | -13 |
| 2026-07-01 | 2026-W27 | 403 | 88 | 102 | -14 |
| 2026-07-08 | 2026-W28 | 415 | 97 | 85 | +12 |
| 2026-07-29 | 2026-W31 | 419 | 297 | 293 | +4 |
| 2026-08-05 | 2026-W32 | 421 | 105 | 103 | +2 |
| 2026-08-12 | 2026-W33 | 419 | 115 | 117 | -2 |
| 2026-08-20 | 2026-W34 | 419 | 122 | 122 | 0 |
| 2026-08-27 | 2026-W35 | 433 | 146 | 132 | +14 |
| 2026-09-02 | 2026-W36 | 413 | 102 | 122 | -20 |

Gaps between observation dates are uneven because excluded weeks were dropped. The `new` and
`closed` columns count change since the previous **retained** observation, so the three intervals
spanning a dropped week cover more than seven days and are not directly comparable with the others.
This must be normalised per day before the series is used in Task 5.

## 6. Validation

```
python scripts/validate_dataset.py work/task-2/nvidia-nayab-khalid/data/raw/nvidia_postings_raw_20260902.csv

rows            1745
unique job_ids  1745
company_name    NVIDIA
date range      2026-05-13 to 2026-09-02  (5 months)

ERROR  1745 rows have an empty required field: job_description
ERROR  job_description shorter than 20 chars: row 1: 0 chars; ...

FAILED - 2 error(s), 0 warning(s).
```

The dataset fails the shared schema on one required field, `job_description`, because the source
does not carry it for NVIDIA. Per the schema rule the column is retained and left empty rather than
dropped. **This needs a team decision in the sprint meeting**: either the required-field rule is
relaxed for sources that cannot supply descriptions, or members without description text run a
reduced version of Tasks 3 and 4. It should not be resolved by quietly editing my file to pass.

Everything else passes: no duplicate identifiers, no empty identifiers, all dates ISO-8601, one
company per file, no personal data.

One fix was made to the shared validator during this task. Its phone-number heuristic matched the
bare string `tel`, so every NVIDIA job URL containing `Israel-Tel-Aviv` was reported as a suspected
telephone number. The pattern now requires word boundaries, and URL and identifier columns are
excluded from the phone scan. Verified in both directions afterwards: a fixture containing a real
email and a real telephone number is still caught, and the NVIDIA URLs no longer produce false
positives.

## 7. Limitations

These carry forward into every later task and must appear in the Task 9 report.

1. **No job description text.** The single most important limitation. Skill extraction in Task 4
   must work from job titles, which are short and contain far fewer skills than a description. The
   1,745 titles are real and usable, but a title-based skill profile is thinner than a
   description-based one, and comparisons against members who do have description text are not
   like-for-like.

2. **`posting_date` is a proxy.** NVIDIA's Workday feed exposes no posting date; `posted_at` is null
   on every NVIDIA row. The date used is the first weekly observation in which the posting appears.
   Postings already open on 2026-05-13 are left-censored: they appear to start that week regardless
   of how long they had been open. Duration and time-to-fill analysis is therefore not supported.

3. **Weekly resolution.** A posting opened and closed within one week is never observed. Turnover is
   understated by an unknown amount.

4. **Location is mostly collapsed.** 1,674 of 1,745 postings carry a placeholder such as
   "2 Locations" or "6 Locations" rather than named places; only 71 have a usable named location.
   Regional analysis is effectively unavailable for NVIDIA.

5. **European bias.** The source curates employers with EU offices and remote-EU hiring, so this is
   NVIDIA's European hiring, not global. Any comparison with a member whose source is global will
   overstate the difference in scale.

6. **Coverage of the observation window only.** 2026-05-13 to 2026-09-02 is under four months.
   Seasonality cannot be estimated, and a 12-week forecast horizon is being fitted on 12
   observations, which is thin. Task 7 must report wide intervals and lean on a naive baseline.

7. **Third-party derived.** As stated in section 3, this is not a first-party collection and its
   completeness against NVIDIA's actual Workday feed is unverified.

## 8. What I recommend for the team

1. **Ratify the description question in the sprint meeting.** Four members will not all have
   description text. Either Tasks 3 and 4 run on titles for everyone, so the comparison is fair, or
   the difference is documented and accepted.
2. **Reconsider the shared comparison basis.** The Task 1 plan proposed that all four members pull
   their company's rows from one common dataset. No dataset tested holds all four companies at usable
   volume. `edwarddgao/open-apply-jobs` covers Anthropic well and NVIDIA not at all; `data_jobs`
   covers Google and Microsoft well and Anthropic barely.
3. **Canonicalise company names on load.** NVIDIA appears under 11 distinct employer strings in one
   source. Every member should apply a name-matching rule rather than an exact match.
4. **Keep collecting weekly.** The snapshot source updates daily. Re-running the script each week
   extends the series and directly improves Task 7, which is currently short of observations.

## Attribution

Job posting data for NVIDIA is taken from the `Aramente/eu-tech-jobs` dataset, published on Hugging
Face under the Creative Commons Attribution 4.0 International licence. Datasets tested and not used
are credited in section 2: `arshkon/linkedin-job-postings` (CC BY-SA 4.0) via the
`MichaelYitzchak/LinkedInJobPostings` mirror, `lukebarousse/data_jobs` (Apache-2.0), and
`edwarddgao/open-apply-jobs` (MIT).
