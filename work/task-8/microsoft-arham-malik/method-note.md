# Task 8 Method Note - Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-10-26

## Basis and measures

Titles, for the same reason as Task 6. Three measures, because they disagree in
ways that carry information.

- Jaccard on skill sets - do they want the same skills at all
- Cosine on skill-share vectors - do they want them in the same proportions
- Cosine on title TF-IDF - does the hiring language itself look alike

## Results

Cosine on skill-share weighting:

| | Microsoft | NVIDIA | Google | Meta |
|---|---|---|---|---|
| Microsoft | 1.000 | 0.324 | 0.092 | 0.170 |
| NVIDIA | 0.324 | 1.000 | 0.116 | 0.173 |
| Google | 0.092 | 0.116 | 1.000 | 0.029 |
| Meta | 0.170 | 0.173 | 0.029 | 1.000 |

## Where the measures disagree, which is the point

**NVIDIA and Google: Jaccard 0.400, cosine 0.116.** The widest gap in the
matrix. They name many of the same skills but weight them completely
differently. One measure alone would have reported them as the most similar
pair; they are nearly the least.

**Microsoft and NVIDIA: Jaccard 0.083, cosine 0.324, text cosine 0.622.** The
opposite shape. Few shared skill names, but the proportions line up and the
title language is the most alike of any pair. Microsoft's titles are sparse, so
the little that does match is concentrated in the same places NVIDIA
concentrates.

Reporting one number here would have been actively misleading in both
directions.

## Inherited caveat

The taxonomy is still NVIDIA-extended. Microsoft matches 5.5% of its titles
against it, so Microsoft's vectors are built from very few hits and are
correspondingly unstable - a handful of postings moves them. Two low-coverage
companies can also look similar simply by both being sparse, which is a property
of the taxonomy rather than a finding about the companies. This is on the figure
as well as here.
