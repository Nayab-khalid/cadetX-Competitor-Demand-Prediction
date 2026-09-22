# Optional Task 12 – Fine-Tune a Skill Extraction Model By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

## 1. Approach
Fine-tuned spaCy's pretrained **`en_core_web_sm`** NER component to recognize a new **`SKILL`** entity label, so skill mentions can be found as *spans in running text* rather than only via Task 4's exact keyword/regex match.

**Training labels**: Task 4's regex taxonomy applied to Task 3's cleaned text, used as **distant/weak supervision** — the regex extractor is the "teacher," spaCy NER is the "student." This is a standard way to bootstrap NER training data without hand-labeling, but it has an honest consequence: evaluating the student against held-out *regex* labels mostly measures how well it reproduced the teacher, not true real-world accuracy. See §3 for how this is addressed.

## 2. Training setup
- Base model: `en_core_web_sm` (pretrained English, tok2vec+NER already fit on general text).
- 550 training postings / 150 held-out test postings (job-level split, seeded).
- Added `SKILL` label to the existing NER pipe, disabled all other pipes (`tok2vec` frozen implicitly since only `ner` gradients are applied), `nlp.resume_training()` to continue from pretrained weights rather than reinitializing.
- 12 epochs, batch size 16, dropout 0.3. Loss dropped steadily from 9,817 → 127 over training (see script stdout) — normal convergence pattern, no divergence.
- Training time: **~209 seconds** on CPU.

## 3. Evaluation — two different questions, two different test sets
| Test set | What it measures | Precision | Recall | F1 |
|---|---|---|---|---|
| Held-out weak-label test set (150 postings, regex-derived gold) | Agreement with the teacher labels | **0.991** | **0.991** | **0.991** |
| Pretrained baseline, no fine-tuning (no `SKILL` label exists yet) | Floor — same test set | 0.0 | 0.0 | 0.0 |
| **Generalization set** (10 hand-written paraphrase sentences the regex taxonomy cannot match verbatim, e.g. *"distributed systems"* instead of the taxonomy's `"distributed system"`, *"machine-learning"* with a hyphen) — **regex baseline** | Can static keyword matching handle unseen phrasing? | 0.455 | 0.500 | 0.476 |
| **Generalization set** — **fine-tuned NER** | Can the trained model handle unseen phrasing? | **0.600** | **0.600** | **0.600** |

**Reading these honestly**: the 0.991 F1 on the held-out weak-label set is expected and not very meaningful on its own — it mainly confirms the model learned to imitate its teacher (the regex), which is by construction easy since the labels came from that same regex. The number that actually matters is the **generalization set**: regex scores 0.476 F1 there (it fails whenever phrasing doesn't exactly match a taxonomy pattern), while the fine-tuned model reaches **0.600 F1** — a real, if modest, improvement from *learning the concept* of a skill mention rather than only matching fixed strings. 10 sentences is a small generalization set (chosen for hand-verifiable gold labels), so this gain should be read as a directional proof-of-concept, not a precise, statistically robust estimate — a larger held-out human-annotated set would be needed to quantify the gain with confidence.

## 4. Output
- `fine_tuned_skill_ner/` — the fine-tuned spaCy model (~15MB), loadable via `spacy.load("fine_tuned_skill_ner")`.
- `evaluation_metrics.csv` — all four rows above.
- `finetune_skill_ner.py` — full training + evaluation script (rerunnable end-to-end; ~3.5 minutes on CPU).

## 5. When to use this vs. Task 4's regex extractor
The regex taxonomy (Task 4) stays the production default: it's exact, auditable, and needs no training data or GPU — appropriate for a team that needs the same skill definitions to line up across four companies. This fine-tuned model is the natural next step if/when postings start using phrasing the taxonomy doesn't anticipate (new job titles, competitor terminology, non-English postings) — the generalization-set result above is the evidence that a trained model would help there, once a larger real (not weakly-labeled) evaluation set justifies switching.

## Task 12 Outcome
spaCy NER fine-tuned on Google job postings via distant supervision from the Task 4 taxonomy; evaluated both against held-out weak labels (0.991 F1, expected/teacher-agreement) and a hand-written generalization set (0.600 F1 vs. regex's 0.476 F1), honestly separating "did it learn the teacher" from "does it generalize" — model and metrics saved for reuse.
