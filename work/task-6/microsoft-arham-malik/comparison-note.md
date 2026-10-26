# Task 6 Comparison Note - Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-10-26

## Basis

Titles, following the NVIDIA Task 6 note. NVIDIA's collection was ToS-blocked
from taking description text, so titles are the only like-for-like basis across
all four. All four datasets are read from the repo and matched through
`scripts/skill_matcher.py`.

| Company | Postings | Titles, skills/posting | Titles coverage | Full text coverage |
|---|---|---|---|---|
| Microsoft | 182 | 0.08 | 5.5% | 96.7% |
| NVIDIA | 1,745 | 1.03 | 71.7% | none |
| Google | 1,127 | 0.36 | 30.3% | 73.6% |
| Meta | 209 | 0.17 | 16.3% | 88.5% |

These reproduce NVIDIA's committed figures (Meta 0.17/16.3 exactly, NVIDIA
1.03/71.7 against their 72.0), which is the check that this is wired the same
way as the rest of the team's work.

## The result that governs Microsoft's participation

**On the agreed comparison basis, Microsoft is very nearly invisible.** 5.5%
title coverage means roughly ten of 182 postings contribute anything at all, and
almost all of that is Azure. On full text Microsoft has the richest signal in
the team at 96.7% coverage and 5.95 skills per posting.

So Microsoft has the most to say and the least room to say it. That is not a
complaint about the convention - titles are genuinely the only common
denominator. It is the cost of the convention, and it should be stated in Task
10 rather than left for a reader to notice that the Microsoft column is empty.

Microsoft job titles are generic by house style: "Software Engineer II",
"Principal Data Scientist", "Senior Software Engineer". NVIDIA's carry the
technology: "Senior Linux Kernel Systems Software Engineer", "Solutions
Architect, Generative AI". The difference is real, and it is a fact about naming
conventions rather than about what the two companies build.

## Where Microsoft sits, titles basis

Ahead: Azure, 2.2% against a field mean of 0.0 - the only skill where Microsoft
leads, and it leads because no other company's titles mention a cloud by name.

Behind: GCP (-7.3), Solutions Architecture (-4.1), Networking (-3.0),
Datacenter Systems (-2.8), Performance Engineering (-2.4). Every one of these is
zero for Microsoft on titles and non-zero on full text, so these gaps measure
title style, not capability.

## Category mix, titles basis

| Category | Microsoft | NVIDIA | Google | Meta |
|---|---|---|---|---|
| cloud_infra | 60.0 | 8.2 | 67.8 | 0.0 |
| hardware_systems | 13.3 | 35.2 | 7.2 | 8.6 |
| research_domains | 13.3 | 18.4 | 3.5 | 80.0 |
| silicon_design | 0.0 | 14.3 | 1.5 | 5.7 |

Microsoft and Google both skew cloud; NVIDIA to hardware and silicon; Meta
almost entirely to research domains. Read these as proportions of a very small
number of Microsoft hits.

## The taxonomy caveat, restated

NVIDIA extended the taxonomy by 34 skills built from NVIDIA titles, which is why
NVIDIA's coverage is 72% and Microsoft's is 5.5%. Microsoft's proposed extension
is in `_shared/PROPOSED_taxonomy_patch.yaml` and is deliberately **not** applied
here. Applying it unilaterally would inflate Microsoft for exactly the reason
NVIDIA is currently inflated, and the comparison would still measure the
taxonomy rather than the companies.

The fix is for all four members to extend, then re-run. Until then every number
above carries that caveat.
