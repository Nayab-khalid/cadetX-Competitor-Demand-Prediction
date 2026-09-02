# Legal and Ethical Rules

Written on: 2026-08-18
Agreed by the team on: YYYY-MM-DD (to be confirmed in the sprint 1 meeting)

These rules apply to every member for the whole project. They are the team's answer to the Task 1
requirement for a clear understanding of the legal requirements.

## 1. Permitted sources

Data is collected only from the sources listed as approved in
[approved-sources.md](approved-sources.md). A new source may be used only after the checklist in
[docs/legal-checklist.md](../../../docs/legal-checklist.md) has been completed, dated, and agreed by
the team in a meeting.

The order of preference is:

1. A first-party public API published by the company or its applicant tracking system.
2. The company's own career site, where robots.txt permits the paths required.
3. An openly licensed public dataset with a stated licence.
4. Nothing else.

## 2. Terms of Service

The Terms of Service of every source are read before any data is collected. The member records the
date they were read and the section that governs automated access, research use or redistribution.
Where terms are ambiguous, the source is treated as not permitted.

Terms that restrict use are respected even when the data is technically reachable. The Adzuna API
was rejected on exactly this basis: the data is available, but ongoing academic use requires written
consent that the team does not have.

## 3. robots.txt

The robots.txt file of every host is read before collection, and the applicable `User-agent`,
`Allow` and `Disallow` lines are quoted with the date of the check in the member's source review.

- A `Disallow` on a path the team needs means the source is not used for that purpose. Google
  Careers was rejected for systematic collection for this reason.
- Where a site disallows everything by default and allows named paths, only those named paths are
  requested. Microsoft Careers is handled this way.
- **Where robots.txt and the Terms of Service disagree, the Terms of Service govern.** robots.txt is
  an instruction to crawlers; the terms are the contractual position. NVIDIA is the worked example:
  its careers host allows the career-site path in robots.txt, while section 3.2 of its Terms of
  Service prohibits robots, scrapers, crawlers and data mining tools. The site is therefore not used
  for automated collection. Checking robots.txt alone is not sufficient for any source.
- Being allowed by robots.txt is not on its own a reason to request something. Application and login
  endpoints are excluded by team decision even where robots.txt permits them.
- robots.txt is re-checked at the start of Task 2 and before the Task 10 submission.

## 4. No bypassing technical controls

The team does not bypass logins, paywalls, rate limits, CAPTCHAs or bot protection, and does not
misrepresent itself through user-agent spoofing. Requests are made at a slow, polite rate. If a
source blocks or throttles the team, collection stops rather than being worked around.

## 5. Personal and sensitive data

No personal or sensitive data is collected, stored, processed or committed at any point.

This includes names, email addresses, telephone numbers, recruiter or hiring-manager identities,
applicant information, and any free-text content that identifies an individual. Only company-level
job-posting information is collected.

Controls:

- Any column that could identify a person is dropped at the point of loading, before the file is
  saved.
- `python scripts/validate_dataset.py <file>` is run on every dataset before it is committed. It
  scans every cell for email addresses and telephone numbers and fails the file if it finds any.
- If personal data is discovered in a committed file, it is removed immediately, the commit history
  is corrected, and the incident is recorded in the meeting minutes.

## 6. Copyright and licensing

Factual fields such as job title, posting date, location and employer are recorded and analysed
freely. Full job description text is treated as protected expression:

- It is used as an input to analysis, and the outputs the team publishes are derived features,
  counts, trends and forecasts, not reproductions of the source text.
- This repository is not used to republish full description text as a dataset release. Where a
  member must commit description text to make their work reproducible, they commit the smallest set
  needed and state the source and licence in their Data Collection Report.
- Licence conditions are honoured. The Kaggle dataset is CC BY-SA 4.0, so it requires attribution
  and share-alike on anything derived from it. The Hugging Face dataset is Apache-2.0 and requires
  attribution.

## 7. Data derived from third parties

Some public datasets are derived from platforms whose own terms prohibit collection, such as
LinkedIn. The team did not collect that data and is not party to those terms, but the provenance is
not clean. Such datasets are therefore:

- used as a secondary or historical source only, never as the only basis for a company's analysis;
- filtered to the four companies in scope on load;
- clearly labelled as third-party derived in every report and chart that uses them.

## 8. Provenance and record keeping

For every dataset the member records the source, the exact URL, the access date, the collection
method and the licence, in their Data Collection Report in Task 2. Any figure that appears in a
report or a slide must be traceable back to a file in this repository.

## 9. Changes during the project

If the terms or robots.txt of a source change during the project, use of that source stops
immediately, the affected work is reviewed, and the decision is recorded in the meeting minutes for
that sprint.

## 10. Responsibility

Each member is responsible for the legality of their own collection. The Data Quality Lead of the
week checks that every committed dataset passes the validator and that the source reviews are
complete and dated. Uncertainty is raised in the weekly meeting rather than resolved privately.

Agreed by: Nayab Khalid, Noorul Huda Batool, Arham Malik, Abdal Farid
