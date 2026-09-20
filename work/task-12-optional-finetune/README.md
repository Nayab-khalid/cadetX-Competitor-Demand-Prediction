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
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

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

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
