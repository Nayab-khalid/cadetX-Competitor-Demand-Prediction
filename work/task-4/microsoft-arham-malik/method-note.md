# Task 4 Method Note - Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-10-26

## Method

`scripts/skill_matcher.py` against `shared/taxonomy/skills.yaml`, 93 canonical
skills. No local skill list, per the task rules.

Two bases, following the convention Nayab set in the NVIDIA Task 6 note:
titles for anything that will be compared across companies, full text to
quantify what titles cannot see.

| Basis | Skills/posting | Coverage |
|---|---|---|
| Titles | 0.08 | 5.5% |
| Full text | 5.95 | 96.7% |

The 5.5% title figure reproduces the number in NVIDIA's committed
`basis_comparison.csv` exactly, which is the check that this pipeline is wired
the same way as the rest of the team's.

## A bug in my own first run

The first run reported 0.0% title coverage and I nearly wrote it up as a
finding about Microsoft using generic job titles. It was not. `build_matchers()`
compiles patterns from `term.lower()` with no `re.I` flag, so the patterns are
case-sensitive and Title Case input matches nothing. NVIDIA's Task 4 calls
`.str.lower()` for this reason.

Worth adding to `scripts/README.md`: the matcher requires lowercased input, and
failing to do so returns zero rather than an error.

## A defect in the shared taxonomy

`Autonomous Vehicles` lists `drive` and `av` as aliases. `drive` matches the
ordinary verb.

| Company | Postings | Falsely tagged |
|---|---|---|
| Microsoft | 182 | 80 (44.0%) |
| Meta | 209 | 70 (33.5%) |

Every one contains the bare word in phrases such as "drive features to closure"
and "drive impact with a global team". None concerns vehicles. Google reads 0%
only because its Task 6 run matched on titles; the error is latent there, not
absent.

Evidence with context lines is in
`data/features/drive_false_positive_evidence_20261026.csv`.

This file reports both numbers - as the taxonomy stands, so figures stay
comparable with work already committed, and with the alias suppressed, so the
size of the error is visible. The fix needs a PR and two approvals, so it is
proposed in `_shared/PROPOSED_taxonomy_patch.yaml` rather than applied here.

## Taxonomy extension

Nayab's note asks each member to extend the taxonomy for their own company,
since NVIDIA's 34 additions are why NVIDIA looks skill-rich. Microsoft's
proposed additions are in the same patch file: C#, .NET, PowerShell, Windows
Platform, Debugging, Distributed Systems, Algorithms and Data Structures,
Telemetry, Microsoft 365, Bing, Xbox.

Two candidates were tested and rejected, recorded so nobody re-proposes them:

- `teams` matched 96 postings, but only 4 are Microsoft Teams. The other 92 are
  the ordinary plural noun.
- `windows` matched 60, of which 11 are the operating system. Qualified forms
  (`windows server`, `windows kernel`) are proposed instead.

Those two are the same failure mode as `drive`, which is why they were measured
before being proposed rather than after.

## Hand spot-check

20 postings read by hand against their extracted skills. The `drive` false
positive was found this way, not by the code. Two further observations: `cloud`
as an alias for Cloud Infrastructure is doing heavy lifting at 64.8%, and
`security` for Cybersecurity at 30.8% has the same breadth. Both are arguably
correct for Microsoft but neither has been measured. Raised in the patch file
as a question, not a proposed change.
