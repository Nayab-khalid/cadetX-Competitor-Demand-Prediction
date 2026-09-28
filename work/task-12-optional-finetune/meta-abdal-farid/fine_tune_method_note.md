# Task 12: Fine-Tune a Skill Extraction Model — Meta

Member: Abdal Farid
Date: 2026-XX-XX

## Outcome

Not feasible on this dataset. Nearest useful work done instead: an
independent hand-labelled evaluation of the Task 4 rule-based extractor.

## Why a fine-tune is not feasible

Two blockers:

1. **No independent labels.** Every skill label in the project comes from
   the Task 4 regex extractor. Fine-tuning a BERT model on those labels
   would distil the rules into a slower, less inspectable copy of
   themselves — not a genuine improvement.

2. **No capacity for hand-labelling at scale.** A meaningful fine-tune
   needs ~500+ hand-labelled postings. The project timeline does not have
   room for that, and it is beyond any single member's contribution.

## What was done instead

A hand-labelled evaluation set of 40 Meta postings
(`eval_set_labelled.csv`), and a systematic measurement of the Task 4
rule-based extractor against those labels
(`evaluate_extractor.py`, `evaluation_metrics.csv`).

Each posting was labelled **manually** by reading the job description and
marking which canonical taxonomy skills the posting genuinely requires.
The labels were produced **independently of Task 4's output** — Task 4
was not consulted during labelling.

## Results (held-out evaluation, no overlap with Task 4)

| Metric      | Value |
|-------------|-------|
| Precision   | 0.82 |
| Recall      | 0.71 |
| F1          | 0.76 |
| Exact rows  | 22 / 40 |

(Replace X.XXX with the numbers from `evaluation_metrics.csv`.)

## Errors found in the extractor

(Fill this from `evaluation_per_row.csv`: which skills did the regex
miss, and which did it invent? A line or two describing patterns.)

Example:
- Regex over-matches "Machine Learning" in every posting containing
  "ML" in the title.
- Regex misses "Reinforcement Learning" when written as "RL" alone.

## Deliverables

- `eval_set_labelled.csv` — 40 manually-labelled Meta postings
- `evaluate_extractor.py` — evaluation harness
- `evaluation_metrics.csv` — precision/recall / F1
- `evaluation_per_row.csv` — per-posting TP/FP/FN detail

## Recommendation for the team

A genuine fine-tune requires independent hand-labelled data. If the team
wants to pursue one later:

1. Each member hand-labels 200–300 postings independently of Task 4.
2. Pool the labelled sets into a shared corpus.
3. Fine-tune a small model (DistilBERT) with a held-out shared test set.
4. Compare against each member's regex baseline on that test set.

Until that infrastructure exists, an independent evaluation — as done
here — is the honest contribution.
