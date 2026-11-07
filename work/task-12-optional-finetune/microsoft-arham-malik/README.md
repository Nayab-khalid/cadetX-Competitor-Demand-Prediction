# Optional Task 12 - Fine-Tune a Skill Extraction Model, Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-11-07

## Result

| Method, 40 held-out postings | Precision | Recall | F1 | Exact rows |
|---|---|---|---|---|
| Keyword matcher, taxonomy as it stands | 0.731 | 0.829 | 0.777 | 3/40 |
| Keyword matcher, Task 4 `drive`/`av` suppression | 0.791 | 0.829 | 0.809 | 7/40 |
| **Keyword matcher + fine-tuned filter** | **0.874** | 0.790 | **0.830** | **12/40** |

The fine-tuned model cuts false positives from 64 to 24, buying 14 points of precision for 4 points
of recall. Against the Task 4 baseline that already suppresses `drive`, the F1 gain is 0.021: modest,
and reported as such. Five-fold cross-validation on the training postings gives 86-91% accuracy
against a 73-81% always-genuine baseline (`data/cv_dev_metrics.csv`). Re-running the script
reproduces every number exactly.

## Why this is feasible for Microsoft when it was not for NVIDIA or Meta

NVIDIA has no description text. Meta and NVIDIA both noted that the only labels available came from
their own regex, so a fine-tune would just learn the rules. Microsoft has full text for all 182
postings, and the task rule - **labels independent of the rule-based extractor** - was met by
labelling directly from the posting text:

- **Training labels** (`data/train_pair_labels_20261107.csv`): all 924 skill candidates the matcher
  proposes in the 142 training postings, each judged genuine or not from its context. The matcher
  only proposes candidates; whether a candidate is genuine is a judgement about the text, not the rule.
  76% are genuine.
- **Gold test set** (`data/eval_set_labelled.csv`): 40 held-out postings, 210 skill labels, written
  from the full text **before** any extractor output for those postings was looked at.

The split (`data/split_20261107.csv`, seed 20261026) was fixed first. Test postings were never used
for training or for choosing settings: epochs, dropout and the 0.5 threshold were fixed in advance and
checked by cross-validation on training postings only.

**Labelling provenance.** The labels were made with AI assistance (Claude) by reading each posting
or candidate against the rules below. They have not yet been checked by a second person. A spot
check of a sample is the next step before these numbers are quoted outside the team.

## Labelling rules

A skill from the shared taxonomy counts only if the posting asks for it, or names it as part of the
role or the team's own technology. These do not count:

- boilerplate - security screening counts as Cybersecurity only if the work itself is security work
- ordinary verbs ("drive results", "on the go")
- company marketing, such as Azure named only as a product customers buy
- adjectives ("an agile team", "a secure, reliable codebase")
- degree fields ("BS in Statistics")

## Method

`finetune_skill_filter.py`

1. Run the shared `skill_matcher` over each posting's `clean_text` to collect candidates (skill,
   matched terms, up to three mentions of context).
2. Fine-tune a pre-trained spaCy pipeline. The `tok2vec` layer of `en_core_web_sm` is kept and
   trained further, with a new text classifier listening to it, so the pre-trained layer is
   fine-tuned and not frozen. It runs 12 epochs with dropout 0.2.
3. Keep a candidate if the model scores it genuine at 0.5 or above. Score against the gold set.

The model is saved in `fine_tuned_skill_filter/` (9.5 MB) and loads with `spacy.load()`.

## What the model learned, and what it did not

It **correctly removed** all 18 `drive` false positives in the test set, security-screening
boilerplate, "on the go", and Azure named only as a product. It **wrongly dropped** 8 genuine skills,
mostly rare aliases it saw too few times to learn: `bringup` for Firmware, `analog`. Most of its
**remaining false positives** are "agile" used as an adjective, which is hard to tell apart even for
a reader.

The filter can only remove candidates, so recall is capped at the matcher's 0.829. The matcher's
misses (`data/matcher_misses.csv`) are a separate problem.

## Two findings about the shared tooling

1. **`C` and `R` can never be extracted, from any text.** `title_match_blocklist` exists to stop
   those letters matching inside job titles, but `build_matchers()` drops blocked terms from **every**
   pattern, including full description text. `C` is the single largest miss in the gold set (7 of 40
   postings). The fix belongs in `scripts/skill_matcher.py`: apply the blocklist to titles only.
2. **Generic aliases dominate the false positives.** `security`, `agile`, `performance`,
   `reliability` and `cloud` produce most of the remaining errors, which backs up the alias review
   raised in Task 4.

## Files

| File | What it is |
|---|---|
| `finetune_skill_filter.py` | Builds candidates, cross-validates, trains, evaluates, saves the model |
| `fine_tuned_skill_filter/` | The fine-tuned spaCy model |
| `data/split_20261107.csv` | Train/test split by posting |
| `data/train_pair_labels_20261107.csv` | 924 training labels |
| `data/eval_set_labelled.csv` | 40-posting gold test set |
| `data/evaluation_metrics.csv` | The result table above |
| `data/evaluation_per_candidate.csv` | Every test candidate with its score, the model's decision, and gold |
| `data/cv_dev_metrics.csv` | Cross-validation accuracy per fold |
| `data/matcher_misses.csv` | Gold skills the keyword matcher never proposes |
| `train_skill_ner.py` | Earlier draft, **not used**: it trains on labels taken from the Task 4 extractor, which breaks the task's label-independence rule |

## To run

    pip install spacy pandas pyyaml
    python -m spacy download en_core_web_sm
    python finetune_skill_filter.py

It takes about five minutes on a laptop CPU.
