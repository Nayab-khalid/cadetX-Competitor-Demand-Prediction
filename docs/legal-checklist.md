# Legal & ethical checklist

Complete this for **every** source before it goes on the approved list in Task 1. Copy the block
into your `source-review.md`, fill it in, and date the checks - an undated check is not a check.

## Per-source checklist

- [ ] **Terms of Service read.** Quote the clause that permits or forbids automated access,
      redistribution, or research use. Link + date.
- [ ] **robots.txt checked** at `https://<domain>/robots.txt`. Paste the `User-agent` and `Disallow`
      lines that apply. Date the check.
- [ ] **Extraction permitted** for the specific paths you will use. If robots.txt disallows the
      careers path, the source is rejected - no exceptions, no workarounds.
- [ ] **Licence identified.** CC-BY, CC0, ODbL, proprietary, "public but copyrighted"? Note the
      attribution requirement.
- [ ] **Copyright position understood.** Facts (dates, titles, locations) are generally not
      copyrightable; the full description text often is. Prefer extracted features to wholesale
      republication of long descriptions.
- [ ] **No personal data.** Confirm the fields you keep contain no names, emails, phone numbers,
      recruiter identities or anything else that identifies a person.
- [ ] **Rate limits / politeness** respected where any request is made at all.
- [ ] **Provenance recorded** - exact URL, access date, and how the data was obtained.

## Preference order for sources

1. Published open datasets with a clear licence (open-data portals, Kaggle datasets with a stated
   licence, government/statistical releases).
2. Official APIs with terms that permit research use.
3. Company career pages **only** where the ToS and robots.txt clearly allow it.

If in doubt, the answer is no - pick a different source and say so in your report.

## Source register

Maintained by the team in `work/task-1/team/approved-sources.md`.

| Source | Licence | robots.txt OK (date) | ToS OK (date) | Personal data | Verdict | Used by |
|---|---|---|---|---|---|---|
|  |  |  |  | none |  |  |

## Red lines

- No collecting personal or sensitive information.
- No bypassing logins, paywalls, rate limits or bot protection.
- No republishing full copyrighted descriptions as a "dataset release" in this public repo -
  store what you need for analysis and document the source.
- If a source's terms change mid-project, stop using it and record the decision in `meetings/`.
