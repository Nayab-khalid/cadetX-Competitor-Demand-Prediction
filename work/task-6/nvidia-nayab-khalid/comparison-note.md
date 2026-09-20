# Competitor Comparison Note - NVIDIA

Member: Nayab Khalid | Company: NVIDIA | Task 6 | Date: 2026-09-20

Full write-up with figures: [Task-6-Competitor-Comparison-NVIDIA-Nayab-Khalid.pdf](Task-6-Competitor-Comparison-NVIDIA-Nayab-Khalid.pdf)

## The result that governs everything else

Run against the shared taxonomy as it stands, NVIDIA looks far more skill-rich than the other
three. **That result is an artefact of my own Task 4 work.**

| Company | Pre-extension taxonomy (59 skills) | Extended taxonomy (93) | Change |
|---|---|---|---|
| NVIDIA | 21.2% | 72.0% | **+50.8 pts** |
| Google | 22.3% | 28.7% | +6.4 pts |
| Meta | 12.4% | 16.3% | +3.9 pts |
| Microsoft | 3.8% | 5.5% | +1.7 pts |

Under the taxonomy the team actually agreed, NVIDIA and Google are level and NVIDIA is marginally
behind. The 34 skills I added in Task 4 were built by reading NVIDIA titles, so they find NVIDIA
vocabulary. **Until each member extends the taxonomy for their own company, a four-way skill
comparison measures the taxonomy, not the companies.**

The fix is not to discard the extension. It is for everyone to do the same work and re-run.

## What the four datasets are

| Company | Postings | Titles | Description text | Posting dates |
|---|---|---|---|---|
| NVIDIA | 1,745 | yes | **none** (ToS blocked collection) | yes, 12 weekly observations |
| Google | 1,227 | yes | responsibilities + qualifications | **none** |
| Meta | 209 | yes | yes, median 3,239 chars | yes, 2024 |
| Microsoft | 182 | yes | yes, median 3,715 chars | **empty column** |

Two consequences: **no cross-company time series is possible**, and raw skill counts are not
comparable.

## Method: two bases

- **Basis A, titles only, all four.** Every dataset has a job title, so this is like-for-like. It
  is the basis for every comparison claim.
- **Basis B, full text where it exists.** Not comparable with NVIDIA; included only to quantify
  what NVIDIA's data cannot see.

Both use the same shared taxonomy through `scripts/skill_matcher.py`, which was factored out in
this task so Tasks 4, 6 and 8 cannot drift apart. Task 4 was refactored onto it and re-run to
confirm byte-identical output.

## What the sources can see

| Company | Skills/posting, titles | Skills/posting, full text | Ratio |
|---|---|---|---|
| NVIDIA | 1.03 | no text | - |
| Google | 0.34 | 2.43 | 7x |
| Meta | 0.17 | 4.13 | 24x |
| Microsoft | 0.08 | 6.84 | **85x** |

Microsoft's factor of 85 is the strongest argument in this project for the decision flagged since
Task 2: either everyone runs on titles, or the members with text are solving a different problem.

## Findings, with confidence

| Conclusion | Confidence |
|---|---|
| NVIDIA hires for hardware, silicon and systems; the others do not. 49.4% of NVIDIA's mentions against 8.1% for Google | **High** - survives both taxonomies |
| Each company's own cloud appears in its own postings: GCP for Google, Azure for Microsoft | **High** |
| NVIDIA's titles carry more technical content than the others' | Medium - partly a taxonomy effect |
| The four-way category mix | **Low** - Meta and Microsoft rest on 15-35 mentions |
| Any hiring-velocity or growth comparison | **Not possible** - three of four datasets lack usable dates |

NVIDIA's largest positive gaps on the titles basis: Solutions Architecture +10.7 points,
Networking +7.8, Performance Engineering +6.3, Datacenter Systems +6.2, Silicon Verification +4.5.
Largest negative: GCP -7.0.

## For the team

1. **Every member extends the taxonomy for their own company**, then everyone re-runs Task 4. The
   highest-value action left in the project.
2. **Decide titles or descriptions once, for everyone.**
3. **Google and Microsoft need posting dates**; Meta's 2024 window needs aligning.
4. **Sample sizes**: 182 and 209 against 1,745 and 1,227 makes Meta and Microsoft percentages fragile.

## Files

`data/comparison/` - basis_comparison, skill_share_by_company_titles, category_mix_by_company_titles,
nvidia_vs_others_titles · `figures/` fig0-fig3 · `compare_companies.py` ·
`taxonomy_original_reference.yaml` (kept so the control is reproducible)

```bash
cd work/task-6/nvidia-nayab-khalid
python compare_companies.py
```
