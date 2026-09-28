# Task 12: Fine-Tune a Skill Extraction Model — Meta

Member: Abdal Farid
Date: 2026-09-28

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
   needs ~500+ hand-labelled postings. The project timeline does not
   have room for that, and it is beyond any single member's
   contribution.

## What was done instead

A hand-labelled evaluation set of 39 Meta postings
(`eval_set_labelled.csv`), and a systematic measurement of the Task 4
rule-based extractor against those labels (`evaluate_extractor.py`,
`evaluation_metrics.csv`).

Each posting was labelled **manually** by reading the job description and
marking which canonical taxonomy skills the posting genuinely requires.
The labels were produced **independently of Task 4's output** — Task 4
was not consulted during labelling.

## Results (held-out evaluation, no overlap with Task 4)

| Metric      | Value |
|-------------|-------|
| Precision   | 0.438 |
| Recall      | 0.778 |
| F1          | 0.560 |
| TP / FP / FN | 119 / 153 / 34 |
| Exact rows  | 1 / 39 |

## Interpretation

**The extractor is over-matching heavily.** For every real skill it
finds (119 true positives), it invents roughly 1.3 fake ones (153 false
positives). Recall is acceptable at 0.778 — the regex catches most of
the skills that are actually required — but precision at 0.438 means
most rows contain at least one skill the posting does not really
require.

Only 1 of 39 postings has an exact match between hand labels and
extracted skills. This is the strongest signal in the evaluation: the
regex is usable as a *recall-oriented first pass*, but not as a
production-quality extractor.

## Errors found in the extractor

Three recurring defect patterns, drawn from `evaluation_per_row.csv`:

1. **Over-matching from whole-document scanning.** The worst case is
   `meta_00125` (Research Scientist, AI & Systems Co-design): 6 real
   skills but 16 false positives. The description lists related
   technologies (CUDA, Compilers, Kernel and Drivers, Storage Systems,
   Triton Inference Server, Networking) as examples of the systems
   area, not as skills the candidate must have. The regex cannot
   distinguish "must have X" from "our team works on X".

2. **False positives on title-only signal.** Postings titled
   "Machine Learning Engineer" (`meta_00119`, `meta_00120`, `meta_00121`)
   trigger `Machine Learning` regardless of whether the description
   lists it as a requirement — the title alone is treated as a match.

3. **Missed abbreviations and synonyms.** `Reinforcement Learning` is
   not caught when written as `RL` alone; `Large Language Models`
   misses the `LLM` form. These show up as false negatives
   (`meta_00109`: RL not captured; `meta_00125`: `PyTorch` missed even
   though the description mentions it).

4. **Non-technical postings match cross-functional boilerplate.**
   Legal (`meta_00147`) and Creative Director (`meta_00166`) postings
   returned a single technical skill (`Cybersecurity`, `Go`
   respectively) because the phrase appeared in general Meta
   boilerplate text, not as an actual requirement.

The exact per-posting breakdown is in `evaluation_per_row.csv`.

## Deliverables

- `eval_set_labelled.csv` — 39 manually-labelled Meta postings
- `evaluate_extractor.py` — evaluation harness
- `evaluation_metrics.csv` — precision / recall / F1
- `evaluation_per_row.csv` — per-posting TP / FP / FN detail

## Recommendation for the team

A genuine fine-tune requires independent hand-labelled data. If the
team wants to pursue one later:

1. Each member hand-labels 200–300 postings independently of Task 4.
2. Pool the labelled sets into a shared corpus.
3. Fine-tune a small model (DistilBERT) with a held-out shared test set.
4. Compare against each member's regex baseline on that test set.

**Priority for the current regex pipeline:** the biggest wins are on
precision, not recall. Simple fixes — requiring the skill name to appear
inside a "Requirements" or "Qualifications" section, or ignoring
matches in the title field — would likely cut the false-positive rate
substantially without hurting recall.

Until that infrastructure exists, an independent evaluation — as done
here — is the honest contribution.

Until that infrastructure exists, an independent evaluation — as done
here — is the honest contribution.
