"""
Optional Task 12 - Fine-Tune a Skill Extraction Model
Author: Noor Ul Huda | Company track: Google

Approach: fine-tune spaCy's pretrained en_core_web_sm NER component to add a
new "SKILL" entity label, so the model can recognize skill mentions as spans
in running text -- not just via exact keyword/regex match (Task 4's method).

Training labels come from Task 4's regex taxonomy applied to Task 3's cleaned
text (distant/weak supervision: the regex model is the "teacher", spaCy NER
is the "student"). This is a standard, honest way to bootstrap NER training
data without hand-labeling, but it means the held-out test-set metrics below
mostly measure how well the student reproduced the teacher's regex labels,
not true ground truth. A small, hand-written "generalization set" (unseen
paraphrases the regex CANNOT match) is used separately to measure the actual
value a trained model adds over static keyword matching -- that comparison
is the real point of this task.

Steps:
  1. Build weakly-labeled NER training examples from Task 3 + Task 4 output.
  2. Split postings 80/20 (train/test) at the job level.
  3. Fine-tune en_core_web_sm's NER: add the SKILL label, resume training on
     the new data with the pretrained weights as the starting point.
  4. Evaluate on the held-out weak-label test set (precision/recall/F1).
  5. Evaluate regex baseline vs fine-tuned model on a hand-written
     generalization set of paraphrased skill mentions.
  6. Save the fine-tuned model to ./fine_tuned_skill_ner/ and metrics to
     evaluation_metrics.csv.
"""

import json
import random
import re
import time
from pathlib import Path

import pandas as pd
import spacy
from spacy.training import Example
from spacy.util import filter_spans, minibatch

random.seed(42)

TAXONOMY_PATH = Path("../Task4_Skill_Extraction_Feature_Engineering/skill_taxonomy.json")
CLEANED_PATH = Path("../Task3_NLP_Preprocessing/cleaned_job_postings.csv")

MAX_TRAIN_DOCS = 550
MAX_TEST_DOCS = 150
N_EPOCHS = 12


def load_taxonomy_patterns():
    with open(TAXONOMY_PATH, encoding="utf-8") as f:
        taxonomy = json.load(f)
    compiled = []
    for cat, skills in taxonomy.items():
        for skill, patterns in skills.items():
            compiled.append(re.compile("|".join(patterns), flags=re.IGNORECASE))
    return compiled


def label_text(text: str, patterns) -> list:
    """Return non-overlapping (start, end, 'SKILL') spans for all taxonomy matches in text."""
    spans = []
    for pattern in patterns:
        for m in pattern.finditer(text):
            if m.start() != m.end():
                spans.append((m.start(), m.end(), "SKILL"))
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    non_overlapping = []
    last_end = -1
    for start, end, label in spans:
        if start >= last_end:
            non_overlapping.append((start, end, label))
            last_end = end
    return non_overlapping


def build_examples(nlp, df: pd.DataFrame, patterns) -> list:
    examples = []
    for text in df["clean_text"].astype(str):
        if not text.strip():
            continue
        entities = label_text(text, patterns)
        if not entities:
            continue
        doc = nlp.make_doc(text)
        spans = [doc.char_span(s, e, label=lbl, alignment_mode="contract") for s, e, lbl in entities]
        spans = [s for s in spans if s is not None]
        spans = filter_spans(spans)
        if not spans:
            continue
        example = Example.from_dict(doc, {"entities": [(s.start_char, s.end_char, s.label_) for s in spans]})
        examples.append(example)
    return examples


def evaluate(nlp, examples) -> dict:
    tp = fp = fn = 0
    for ex in examples:
        pred_doc = nlp(ex.reference.text)
        pred_spans = {(e.start_char, e.end_char) for e in pred_doc.ents if e.label_ == "SKILL"}
        gold_spans = {(e.start_char, e.end_char) for e in ex.reference.ents if e.label_ == "SKILL"}
        tp += len(pred_spans & gold_spans)
        fp += len(pred_spans - gold_spans)
        fn += len(gold_spans - pred_spans)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3), "tp": tp, "fp": fp, "fn": fn}


def regex_baseline_predict(text: str, patterns) -> set:
    return {(s, e) for s, e, _ in label_text(text, patterns)}


def main():
    patterns = load_taxonomy_patterns()
    df = pd.read_csv(CLEANED_PATH)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)  # shuffle at job level

    n_train = min(MAX_TRAIN_DOCS, int(len(df) * 0.8))
    n_test = min(MAX_TEST_DOCS, len(df) - n_train)
    train_df = df.iloc[:n_train]
    test_df = df.iloc[n_train:n_train + n_test]

    print(f"Loading base model en_core_web_sm ...")
    nlp = spacy.load("en_core_web_sm")

    print("Building weakly-labeled training/test examples from Task 4 regex taxonomy ...")
    train_examples = build_examples(nlp, train_df, patterns)
    test_examples = build_examples(nlp, test_df, patterns)
    print(f"Train examples: {len(train_examples)} (from {len(train_df)} postings)")
    print(f"Test examples: {len(test_examples)} (from {len(test_df)} postings)")

    # --- baseline: pretrained model with NO fine-tuning has no SKILL label at all ---
    baseline_metrics = {"precision": 0.0, "recall": 0.0, "f1": 0.0, "tp": 0, "fp": 0,
                         "fn": sum(len([e for e in ex.reference.ents if e.label_ == "SKILL"]) for ex in test_examples)}

    ner = nlp.get_pipe("ner")
    ner.add_label("SKILL")

    other_pipes = [p for p in nlp.pipe_names if p != "ner"]
    print(f"Fine-tuning NER (disabling other pipes: {other_pipes}) for {N_EPOCHS} epochs ...")

    start = time.time()
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.resume_training()
        for epoch in range(1, N_EPOCHS + 1):
            random.shuffle(train_examples)
            losses = {}
            for batch in minibatch(train_examples, size=16):
                nlp.update(batch, drop=0.3, losses=losses, sgd=optimizer)
            print(f"  epoch {epoch:2d}/{N_EPOCHS}  ner_loss={losses.get('ner', 0):.2f}")
    elapsed = time.time() - start
    print(f"Training finished in {elapsed:.1f}s")

    print("\nEvaluating fine-tuned model on held-out weak-label test set ...")
    finetuned_metrics = evaluate(nlp, test_examples)
    print(finetuned_metrics)

    # --- generalization set: paraphrases the regex taxonomy CANNOT match verbatim ---
    # (text, [gold skill substring(s)]) -- offsets are computed via str.index() below,
    # rather than hand-counted, so a miscounted character can't silently corrupt the gold labels.
    generalization_raw = [
        ("Comfortable coding in Python for backend services.", ["Python"]),
        ("Experience building large scale distributed systems in production.", ["distributed systems"]),
        ("A background in machine-learning research is a plus.", ["machine-learning"]),
        ("Fluency in cloud infrastructure on GCP is expected.", ["GCP"]),
        ("Has led cross functional teams across engineering and sales.", ["cross functional"]),
        ("Skilled at managing stakeholders across the org.", ["stakeholders"]),
        ("Proficient in SQL and relational databases.", ["SQL"]),
        ("Strong grasp of Kubernetes and container orchestration.", ["Kubernetes"]),
        ("Bachelor of Science degree required for this role.", ["Bachelor of Science degree"]),
        ("Excellent written and verbal communication skills needed.", ["communication skills"]),
    ]
    generalization_set = []
    for text, substrings in generalization_raw:
        ents = []
        for sub in substrings:
            idx = text.index(sub)
            ents.append((idx, idx + len(sub), "SKILL"))
        generalization_set.append((text, ents))

    def score_predictions(pred_sets, gold_sets):
        tp = sum(len(p & g) for p, g in zip(pred_sets, gold_sets))
        fp = sum(len(p - g) for p, g in zip(pred_sets, gold_sets))
        fn = sum(len(g - p) for p, g in zip(pred_sets, gold_sets))
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        return {"precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3), "tp": tp, "fp": fp, "fn": fn}

    gold_sets = [{(s, e) for s, e, _ in ents} for _, ents in generalization_set]
    regex_pred_sets = [regex_baseline_predict(text, patterns) for text, _ in generalization_set]
    nlp_pred_sets = [{(e.start_char, e.end_char) for e in nlp(text).ents if e.label_ == "SKILL"} for text, _ in generalization_set]

    regex_gen_metrics = score_predictions(regex_pred_sets, gold_sets)
    finetuned_gen_metrics = score_predictions(nlp_pred_sets, gold_sets)

    print("\nGeneralization set (paraphrased, unseen-by-regex mentions):")
    print(f"  Regex baseline : {regex_gen_metrics}")
    print(f"  Fine-tuned NER : {finetuned_gen_metrics}")

    out_dir = Path("fine_tuned_skill_ner")
    nlp.to_disk(out_dir)
    print(f"\nSaved fine-tuned model -> {out_dir}/")

    metrics_rows = [
        {"eval_set": "held_out_weak_labels", "model": "pretrained_no_finetune (no SKILL label)", **baseline_metrics},
        {"eval_set": "held_out_weak_labels", "model": "fine_tuned_skill_ner", **finetuned_metrics},
        {"eval_set": "generalization_paraphrases", "model": "regex_taxonomy_baseline", **regex_gen_metrics},
        {"eval_set": "generalization_paraphrases", "model": "fine_tuned_skill_ner", **finetuned_gen_metrics},
    ]
    pd.DataFrame(metrics_rows).to_csv("evaluation_metrics.csv", index=False)
    print("Saved -> evaluation_metrics.csv")


if __name__ == "__main__":
    main()
