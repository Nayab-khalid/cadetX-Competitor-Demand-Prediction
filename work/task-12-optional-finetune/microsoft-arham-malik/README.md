# Optional Task 12 - Fine-Tune a Skill Extraction Model, Microsoft

## Status: script written, not run here

The fine-tuning itself needs model weights downloaded from Hugging Face, which
the environment this was prepared in cannot reach. `train_skill_ner.py` is
complete and runs locally in roughly ten minutes on CPU.

Noorul's Google submission uses spaCy and is the reference to follow; this
mirrors that approach rather than inventing a second one.

## Why this is the optional task worth taking

Task 4 matches keywords against a fixed taxonomy, so by construction it finds
only skills already listed. Microsoft's case makes the cost visible: 5.5% title
coverage against 96.7% on full text. A trained model generalises past the alias
list, and the gain is measurable against the keyword baseline on held-out
postings.

## To run it

    pip install spacy && python -m spacy download en_core_web_sm
    python train_skill_ner.py

1. Labels are bootstrapped from the Task 4 output, then corrected by hand. That
   is faster than labelling from scratch and the corrections are where the value
   is - the model learns from what Task 4 got wrong.
2. Train on 70%, evaluate on 30% held out.
3. Report precision, recall and F1 for both the keyword baseline and the model,
   on the same held-out set.

## Expect a modest gain, and say so

182 postings is a small training set. An honest small improvement reads better
than an inflated one, and the comparison against the baseline is the deliverable
rather than the model itself.
