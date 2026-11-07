# Optional Task: Fine-Tune a Skill Extraction Model

## Objective

Fine-tune a pre-trained NLP model on job descriptions and verified skill labels to improve precision and recall in skill detection.

## What is submitted

**Each member (in their own folder)**

1. The fine-tuned model and evaluation metrics
2. A short note on the training process and gains

## Rules for this task

- Labels must be independent of the rule-based extractor, or the model just learns the rules.
- A held-out test set, never used during development.

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [x] | |
| Abdal Farid | Meta | [x] | |

## Outcome: not feasible for NVIDIA, with the nearest useful work done instead

NVIDIA's dataset has **no description text**, which is the Task 1 legal finding again. Beyond that,
the only labels available come from my own regex, so a fine-tune would distil the rules into a
slower, less inspectable copy of themselves.

**What was done instead:** a hand-labelled 40-title evaluation set, and a proper measurement of the
extractor that Tasks 4 to 9 all depend on.

| | Precision | Recall | F1 | Exact rows |
|---|---|---|---|---|
| Current shared taxonomy | 0.857 | 0.818 | 0.837 | 30/40 |
| With proposed fixes | 0.978 | 1.000 | 0.989 | 39/40 |

It found four taxonomy defects, including two aliases attached to **two different canonical
skills** (`firmware`, `generative ai`), which meant `Firmware` and `Generative AI` could never match
anything at all.

The fixes are in `taxonomy_proposed_fixes.yaml` **for ratification**, not applied, because they
would change every number in Tasks 4 to 9.

See [Nayab's note](nvidia-nayab-khalid/finetune-note.md).

## Outcome: not feasible for Meta, with an independent hand-labelled evaluation done instead

Every skill label in the project comes from my own Task 4 regex, so a
fine-tune would just distil the rules into a slower, less inspectable
copy of themselves — not a genuine improvement. Building a proper
fine-tune would need ~500+ hand-labelled postings, which is beyond a
single member's scope.

**What was done instead:** a hand-labelled 39-posting gold set, and a
systematic measurement of the Task 4 extractor against it.

| | Precision | Recall | F1 | Exact rows |

| Task 4 rule-based extractor | 0.438 | 0.778 | 0.560 | 1/39 |

The extractor is recall-oriented but precision-poor: it catches ~78% of
real skills, but for every real one it invents ~1.3 fake ones. Only 1
of 39 postings had no false positives or misses. The dominant failure
is whole-document scanning — the regex matches any skill name anywhere
in the text, including cross-references and "nice-to-have" lists.

Four defect patterns found: over-matching from full-text scanning,
false positives from the title field, missed abbreviations (`RL`,
`LLM`), and non-technical postings matching boilerplate.

The full evaluation is in `evaluate_extractor.py`,
`evaluation_metrics.csv`, `evaluation_per_row.csv`, and
`eval_set_labelled.csv`, all in this folder.

## Outcome: feasible for Microsoft, fine-tuned on independent labels

Microsoft is the one company with full description text, so a fine-tune with labels independent of
the extractor was possible. All 924 matcher candidates in 142 training postings were judged genuine
or not from their context. A 40-posting gold test set (210 skills) was labelled from the full text
before any extractor output for it was seen. A pre-trained spaCy pipeline (`en_core_web_sm`) was
fine-tuned to keep or reject each candidate.

| 40 held-out postings | Precision | Recall | F1 | Exact rows |
|---|---|---|---|---|
| Keyword matcher, taxonomy as it stands | 0.731 | 0.829 | 0.777 | 3/40 |
| Keyword matcher, `drive` suppressed (Task 4) | 0.791 | 0.829 | 0.809 | 7/40 |
| Keyword matcher + fine-tuned filter | 0.874 | 0.790 | 0.830 | 12/40 |

A modest, reproducible gain: false positives fall from 64 to 24 for 4 points of recall. The labels
were made with AI assistance and have not yet been checked by a second person.

It also found that **`C` and `R` can never be extracted from any text**: `title_match_blocklist`
is applied to full descriptions as well as titles, and `C` is the largest single miss in the gold set.

See [Arham's note](microsoft-arham-malik/README.md).

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
