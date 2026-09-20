# Task 8: Company Similarity Scoring

## Objective

Measure how similar the four companies are, using skills, tech-stack tags, role categories and trends within a shared framework.

## What is submitted

**Each member (in their own folder)**

1. Similarity tables and visuals (heatmaps / network graphs)
2. A short explanation of what drives the similarities and differences

## Rules for this task

- Same feature construction, weighting and distance metric for everyone, or the matrix is not symmetric in meaning.
- One canonical matrix, validated by the others.

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

## Open team decisions raised by this task

1. **Do not publish a four-company similarity matrix yet.** The ranking flips depending on which
   taxonomy is used: NVIDIA's closest peer is Microsoft on one matrix and Meta on the other, and
   the taxonomy choice moves a pair by up to 0.123.
2. **Title vectors are too sparse for cosine similarity.** About one skill per posting gives
   near-orthogonal vectors. The full-text matrix works (0.38 to 0.57) and is stable, but NVIDIA
   cannot appear in it.

See [Nayab's similarity note](nvidia-nayab-khalid/similarity-note.md).

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
