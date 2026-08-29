# Source Review: Meta

Member: Abdal Farid
Task 1: Understanding Data Sources and Legal
Date: 2026-08-29

Complete one block for every source considered. The full question list is in
`docs/legal-checklist.md`. A source can only be proposed for approval once every box is ticked and
every check is dated.

## Source 1

- Name: Meta Careers (official company careers page)
- URL: https://www.metacareers.com
- Type: company career page
- Licence: none stated — all content copyright Meta Platforms, Inc.

Checks:

- [x] Terms of Service read on 2026-08-28
- [x] robots.txt checked on 2026-08-29  
- [ ] Extraction or download of the required data is permitted
- [x] Licence and attribution requirements understood
- [x] Copyright position understood
- [x] Contains no personal or sensitive data

Terms of Service, relevant clause:

> Meta's terms prohibit collecting content or information from its platforms using automated means (bots, scrapers, crawlers) without Meta's prior written permission. Meta has also actively pursued legal action against parties scraping its properties (e.g. *Meta Platforms, Inc. v. Bright Data Ltd.*, N.D. Cal., ruling Jan 23 2024).

Robots.txt, relevant lines:
# Notice: Collection of data on Facebook through automated means is
# prohibited unless you have express written permission from Facebook
# and may only be conducted for the limited purpose contained in said
# permission.
# See: http://www.facebook.com/apps/site_scraping_tos_terms.php

User-agent: facebookexternalhit
Allow: *

User-agent: meta-externalads
Allow: *

User-agent: *
Disallow: /*cursor=
Disallow: /*fb_comment_id=
Disallow: /ajax/
Disallow: /tealium/
Disallow: /intern/
Disallow: /internal/
Disallow: /login/
Disallow: /oidc/callback/
Disallow: /*.php
Disallow: /signup/
Disallow: /resume/

Fields available:

Job title, job description, location, team/org, posting URL — visible on-page, but not offered as a bulk download or API.

Limitations:

No official export/API; ToS prohibits automated collection without permission.

Verdict:
 **rejected**, because Meta's Terms of Service prohibit automated collection without prior permission. This is why Meta job data was instead sourced from licensed third-party datasets (see Source 2).

## Source 2

- Name: Combined Kaggle Job Postings Datasets (5 datasets, filtered for Meta/Facebook only)
- URL: see sub-sources below
- Type: Kaggle dataset (combined)
- Licence: mixed — see sub-sources below; each dataset published for open download on Kaggle

Sub-sources:

1. **LinkedIn Job Postings (2023–2024)** — https://www.kaggle.com/datasets/arshkon/linkedin-job-postings — Licence: **CC BY-SA 4.0 (confirmed)**
2. **LinkedIn Jobs and Skills (2024)** — https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024 — Licence: **ODC Attribution License / ODC-By (confirmed)**
3. **AI Job Market Global 2026** — https://www.kaggle.com/datasets/atharvasoundankar/ai-job-market-global-2026 — Licence: **CC BY-NC-SA 4.0 (confirmed)** — Non-Commercial clause; acceptable for this educational/research project, flagged since it restricts commercial use
4. **AI & ML Job Postings — LinkedIn & Indeed (2025)** — https://www.kaggle.com/datasets/ankit0017/ai-and-ml-job-postings-linkedin-and-indeed-2025 — Licence: **CC BY 4.0 (confirmed)**
5. **Job Listing Dataset** — https://www.kaggle.com/datasets/sweetymahale/job-listing-dataset — Licence: **MIT (confirmed)**

Checks:

- [x] Terms of Service read on 2026-08-29 for all 5 sub-sources (license confirmed directly on each dataset page)
- [x] robots.txt checked (not applicable to any — all accessed via Kaggle's own download mechanism, not direct scraping)
- [x] Extraction or download of the required data is permitted (Kaggle datasets are published for download by design)
- [x] Licence and attribution requirements understood for all 5 (CC BY-SA, ODC-By, CC BY-NC-SA, CC BY, and MIT — all require attribution to original authors; CC BY-NC-SA additionally restricts commercial use)
- [x] Copyright position understood (underlying postings are LinkedIn/Indeed/employer content; each dataset is a third-party compilation, not original Meta content)
- [x] Contains no personal or sensitive data (job posting fields only — title, company, salary, description; no candidate names/emails)

Fields available:

Job title, company name, location, salary range/min/max, job description, skills, posting date, work type, experience level — merged and standardised across all 5 sources into one dataset.

Limitations:
Combined 209 raw Meta/Facebook-matched rows across all 5 sources; after removing genuine duplicate postings (same title, company, and description appearing in more than one source), **112 unique postings** remain.

Date coverage spans **January 2024 to June 2026**, but with a significant gap between **September 2024 and August 2025**  
limits continuous month-by-month trend analysis for that period.

Column structure varies across the 5 sources (different field names for the same data); fields were merged into a single consistent schema.

Salary/skills fields are only partially populated (not every source includes them).

Verdict: 
**approved**. All 5 licenses confirmed directly on their Kaggle dataset pages (CC BY-SA 4.0, ODC-By, CC BY-NC-SA 4.0, CC BY 4.0, MIT). All are open licenses permitting reuse for research/educational purposes with attribution; note sub-source 3 (CC BY-NC-SA 4.0) restricts commercial use specifically. All 5 avoid the automated-collection restriction identified in Source 1, since data was obtained via Kaggle's own publish/download mechanism rather than by scraping Meta directly.

## Recommendation

The source I will use in Task 2 for Meta: the combined, deduplicated Kaggle dataset described in Source 2 (112 unique Meta postings, Jan 2024–Jun 2026). Source 1 (Meta's own careers page) was rejected due to its Terms of Service prohibiting automated collection without permission.