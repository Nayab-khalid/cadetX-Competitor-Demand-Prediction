# Task 4: Skill Extraction and Feature Engineering

## Objective

Extract skills from the preprocessed postings and turn them into features: counts, categories,
frequency trends. Align a shared skill taxonomy across the four datasets.

## What is submitted

**Each member (in their own folder)**

1. Extracted-skills dataset and feature tables
2. A short note on the methods used

## Rules for this task

- **Every extracted skill must map to a canonical name in
  [`shared/taxonomy/skills.yaml`](../../shared/taxonomy/skills.yaml).** No local skill lists.
- New skills are added by editing the shared taxonomy with a dated comment explaining why, not by
  inventing them inside your own script.
- Terms that appear often but match nothing go into a candidates file for team review.
- Role words are not skills. `engineer`, `manager`, `architect` are `role_function`, from Task 3.
- Spot-check at least 20 postings by hand and write up what it found.

## Definition of done

- [ ] Extracted-skills dataset committed
- [ ] Feature tables committed
- [ ] Method note committed, including validation results and coverage
- [ ] Zero skills in the output that are absent from the taxonomy
- [ ] Taxonomy additions raised for team ratification

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

## Open team decisions raised by this task

1. **34 skills and a new `silicon_design` category were added to the shared taxonomy and need
   ratifying.** The taxonomy as written covered only 21.2% of NVIDIA's postings, because it lists
   tools that belong in a description while a title names the specialisation. 32 of the original 59
   skills never matched once. The extension raised coverage to 72.0%.

   **This is the alignment risk for Task 8.** If the other three extract against the original 59
   and NVIDIA extracts against 93, the similarity score measures the taxonomy rather than the
   companies.

2. **Adopt a title match blocklist.** Any member matching short tokens against titles will hit the
   same false positives: `r` matches "R&D" once punctuation is stripped, `c` matches the `c` inside
   `c++`.

3. **164 candidate terms await promotion or rejection**, in
   [taxonomy_candidates](nvidia-nayab-khalid/data/features/taxonomy_candidates_20260902.csv).

See [Nayab's method note](nvidia-nayab-khalid/method-note.md), sections 1 and 8.

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
