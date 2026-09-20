# Optional Task: Fine-Tune a Skill Extraction Model — NVIDIA

Member: Nayab Khalid | Company: NVIDIA | Optional Task | Date: 2026-09-20

## Verdict: not feasible for NVIDIA, and here is why

The task asks for a pre-trained NLP model fine-tuned on job descriptions and verified skill labels.
**NVIDIA's dataset contains no job descriptions.** NVIDIA publishes through Workday, whose Terms of
Service prohibit automated collection (Task 1), and the openly licensed source that does carry
NVIDIA rows stores title, location, URL and dates only. There is nothing to fine-tune on.

Three further objections, each of which would independently block a useful result:

1. **The labels would come from my own regex.** The only skill labels I have were produced by the
   rule-based matcher in Task 4. Training a transformer on them would distil my regex into a neural
   network — slower, less inspectable, and incapable of exceeding its teacher. That is not an
   improvement in precision or recall; it is the same decision function in a more expensive form.
2. **Six-word titles are the wrong input.** Token classification models earn their keep on context.
   `Senior Firmware Micro-Architect` offers almost none.
3. **The environment cannot run it.** `transformers` and `datasets` are not installed and torch is
   CPU-only.

Objection 1 is the one that matters. Even with the libraries and a GPU, fine-tuning on
self-generated labels would produce a confident-looking model with no new information in it.

## What I did instead

A fine-tune needs a **hand-labelled evaluation set** before it can be claimed to improve anything.
That set is valuable on its own, because Tasks 4 to 9 all depend on the extractor and Task 4 only
ever spot-checked it qualitatively. So I built one and measured the extractor properly.

**Method.** 40 job titles sampled at random (`random_state=2026`) from the Task 3 corpus. For each,
I read the title and recorded which canonical skills genuinely apply. The gold labels are in
`evaluate_extractor.py` as data, so anyone can disagree with a specific row rather than with a
number. Rows where two canonical skills are equally defensible — `ASIC` maps to both Computer
Architecture and SoC Design — accept either.

## Results

| | Precision | Recall | F1 | Exactly correct rows |
|---|---|---|---|---|
| **Current shared taxonomy** | 0.857 | 0.818 | **0.837** | 30 / 40 |
| **With the proposed fixes below** | 0.978 | 1.000 | **0.989** | 39 / 40 |

The evaluation found four defects, all in the taxonomy rather than the matching code.

### 1. `firmware` is an alias of two different skills

It appears on both `Firmware` and `Embedded Systems`. Because ties are broken by ordering,
**`Firmware` never matches anything** — three of 40 titles were affected. The canonical name
`Embedded Systems` also never matched `Embedded Controller`, because `embedded` was not an alias
at all.

*Fix: `firmware` stays on `Firmware`; `Embedded Systems` takes `embedded`.*

### 2. `generative ai` is an alias of two different skills

It appears on both `Generative AI` and `LLMs`, so `Senior Solutions Architect, Generative AI` was
labelled LLMs and **`Generative AI` never matched**.

*Fix: `generative ai` stays on `Generative AI`; `LLMs` takes `llm`.*

### 3. Missing word forms — the same class of bug as Task 4's

`Technical Program Management` had `technical program management` but not `technical program
manager`, which is what titles actually say. Two of 40 titles missed. `Autonomous Vehicles` had
`self-driving` and `av` but not `autonomous driving`.

*Fix: add the title word forms.* This is the third time this pattern has cost real coverage; in
Task 4 the equivalent bug was worth 192 postings.

### 4. An over-broad alias

`physical ai` was an alias of `Digital Twin and Simulation`, which tagged a multimodal-AI
architect role as simulation work.

*Fix: remove it. Physical AI is not digital twin work.*

### One error left, and it is a genuine ambiguity

`Senior Software Release Manager - Networking Verification Engineer` is still tagged
`Silicon Verification`, because `verification` is that skill's main alias. Here it means software
verification. Removing the alias would cost far more true positives than it saves, so the error is
documented rather than fixed.

## Why the shared taxonomy was not edited

The fixes are in `taxonomy_proposed_fixes.yaml`, **not** in `shared/taxonomy/skills.yaml`.

Applying them would change every number in Tasks 4 through 9, which are already committed and whose
documents quote specific figures. Under the governance rule in `docs/skill-taxonomy.md`, taxonomy
changes need team agreement. The right sequence is: team ratifies, then the pipeline re-runs every
downstream task at once, then the documents are regenerated from the new numbers.

The pipeline from the other optional task exists precisely for this. One command re-runs Tasks 3
through 8 in 245 seconds.

## What an actual fine-tune would need

1. **Description text.** Either the team decides NVIDIA works from another company's descriptions,
   which defeats the point, or NVIDIA is out of scope for this task.
2. **Human labels independent of the rules** — at minimum several hundred labelled postings, not 40,
   and labelled without seeing the rule-based output.
3. **A held-out test set** never used during development, which the 40 rows here are not: they were
   used to diagnose the fixes, so 0.989 is an optimistic in-sample number.
4. `transformers`, `datasets`, and a GPU.

Members with description text — Meta and Microsoft, at ~3,200 and ~3,700 characters per posting —
could attempt this. For NVIDIA it is blocked by the Task 1 legal finding, like most of the
constraints in this project.

## Files

| File | Contents |
|---|---|
| `evaluate_extractor.py` | The evaluation, with the 40 gold labels as inspectable data |
| `data/extractor_evaluation.csv` | Row-by-row: gold, predicted, missed, spurious |
| `data/extractor_metrics.csv` | Precision, recall, F1, counts |
| `taxonomy_proposed_fixes.yaml` | The four fixes, for team ratification — **not** applied to the shared taxonomy |

```bash
cd work/task-12-optional-finetune/nvidia-nayab-khalid
python evaluate_extractor.py
```
