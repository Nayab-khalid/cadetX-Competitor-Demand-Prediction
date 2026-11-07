#!/usr/bin/env python3
"""Optional Task 12 - fine-tune a skill extraction model, Microsoft.

The Task 4 keyword matcher finds candidate skill mentions with high recall but
cannot tell "drive features to closure" from a driving system, or a security
screening from security engineering. This script fine-tunes a pre-trained spaCy
pipeline (en_core_web_sm) to judge each candidate in context, then scores
keyword-only extraction against keyword + model on a held-out test set.

Labels are independent of the extractor, per the task rule:
  - data/train_pair_labels_20261107.csv: every candidate the matcher proposes in
    the 142 training postings, labelled genuine (1) or not (0) by reading its
    context. The matcher proposes; the label is a judgement, not the rule.
  - data/eval_set_labelled.csv: 40 held-out postings, labelled with the skills
    each posting genuinely asks for, by reading the full text, before any
    extractor output for them was looked at.

The test postings are never used in training or in choosing settings: settings
are fixed by 5-fold cross-validation on the training postings only.

    pip install spacy pandas pyyaml && python -m spacy download en_core_web_sm
    python finetune_skill_filter.py
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_matcher import build_matchers  # noqa: E402

DATA = HERE / "data"
SRC = ROOT / "work" / "task-3" / "microsoft-arham-malik" / "data" / "microsoft_postings_clean_20261026.csv"
TAX = ROOT / "shared" / "taxonomy" / "skills.yaml"
MODEL_DIR = HERE / "fine_tuned_skill_filter"
SEED, EPOCHS, DROPOUT, THRESHOLD = 20261107, 12, 0.2, 0.5
# Task 4 suppresses these two aliases; reported as a second baseline.
SUPPRESS = {("Autonomous Vehicles", "drive"), ("Autonomous Vehicles", "av")}


def candidates(df, entries):
    """Every skill the matcher finds in a posting, with up to three mentions of
    context. Same longest-first, no-overlap logic as skill_matcher.extract(),
    which does not return positions."""
    rows = []
    for r in df.itertuples():
        text = str(r.clean_text); low = text.lower(); spans = []; per = {}
        for pat, name, _, _ in entries:
            for m in pat.finditer(low):
                if any(m.start() < e and m.end() > s for s, e in spans):
                    continue
                spans.append((m.start(), m.end()))
                per.setdefault(name, []).append((m.start(), m.end(), m.group(0)))
        for name, ms in per.items():
            ms.sort()
            ctx = " ... ".join(text[max(0, s - 90):e + 90] for s, e, _ in ms[:3])
            terms = sorted({t for *_, t in ms})
            rows.append({"job_id": r.job_id, "skill": name, "terms": "|".join(terms),
                         "model_text": f"{name}. Matched: {', '.join(terms)}. Context: {ctx}"})
    return pd.DataFrame(rows)


def build_nlp(spacy):
    """Pre-trained tok2vec from en_core_web_sm plus a new text classifier that
    listens to it, so training fine-tunes the pre-trained layer too."""
    nlp = spacy.load("en_core_web_sm", exclude=["tagger", "parser", "attribute_ruler", "lemmatizer", "ner", "senter"])
    nlp.add_pipe("textcat", config={"model": {
        "@architectures": "spacy.TextCatEnsemble.v2",
        "tok2vec": {"@architectures": "spacy.Tok2VecListener.v1", "width": 96, "upstream": "*"},
        "linear_model": {"@architectures": "spacy.TextCatBOW.v3", "exclusive_classes": True,
                         "ngram_size": 2, "no_output_layer": False}}})
    return nlp


def train(spacy, texts, labels):
    from spacy.training import Example
    from spacy.util import minibatch
    random.seed(SEED); spacy.util.fix_random_seed(SEED)
    nlp = build_nlp(spacy)
    tc = nlp.get_pipe("textcat")
    for lab in ("GENUINE", "NOT"):
        tc.add_label(lab)
    ex = [Example.from_dict(nlp.make_doc(t), {"cats": {"GENUINE": float(y), "NOT": 1.0 - y}})
          for t, y in zip(texts, labels)]
    tc.initialize(lambda: ex, nlp=nlp)
    opt = nlp.resume_training()
    for epoch in range(EPOCHS):
        random.shuffle(ex)
        for batch in minibatch(ex, size=16):
            nlp.update(batch, sgd=opt, drop=DROPOUT)
    return nlp


def prob(nlp, texts):
    return [d.cats["GENUINE"] for d in nlp.pipe(texts)]


def score(pred: dict, gold: dict):
    tp = fp = fn = exact = 0
    for j, g in gold.items():
        p = pred.get(j, set())
        tp += len(g & p); fp += len(p - g); fn += len(g - p); exact += (g == p)
    pr = tp / (tp + fp) if tp + fp else 0; rc = tp / (tp + fn) if tp + fn else 0
    return {"precision": round(pr, 3), "recall": round(rc, 3),
            "f1": round(2 * pr * rc / (pr + rc), 3) if pr + rc else 0,
            "exact_rows": f"{exact}/{len(gold)}", "tp": tp, "fp": fp, "fn": fn}


def main() -> int:
    try:
        import spacy
    except ImportError:
        print("pip install spacy && python -m spacy download en_core_web_sm"); return 1

    df = pd.read_csv(SRC, keep_default_na=False)
    entries, _ = build_matchers(yaml.safe_load(TAX.read_text(encoding="utf-8")))
    cand = candidates(df, entries)
    split = pd.read_csv(DATA / "split_20261107.csv").set_index("job_id")["split"]
    cand["split"] = cand["job_id"].map(split)

    lab = pd.read_csv(DATA / "train_pair_labels_20261107.csv")
    tr = cand[cand.split == "train"].merge(lab, on=["job_id", "skill"], how="left")
    assert tr["genuine"].notna().all(), "unlabelled training candidate - labels out of date"
    te = cand[cand.split == "test"].copy()
    gold = {r.job_id: set(json.loads(r.gold_skills)) for r in pd.read_csv(DATA / "eval_set_labelled.csv").itertuples()}
    assert set(gold) == set(split[split == "test"].index), "gold set and test split disagree"
    print(f"candidates: {len(tr)} train ({tr.genuine.mean():.0%} genuine), {len(te)} test")

    # ---- development: 5-fold cross-validation on training postings only
    jobs = sorted(tr.job_id.unique()); random.Random(SEED).shuffle(jobs)
    folds = [set(jobs[i::5]) for i in range(5)]; cv = []
    for k, held in enumerate(folds):
        a, b = tr[~tr.job_id.isin(held)], tr[tr.job_id.isin(held)]
        m = train(spacy, a.model_text.tolist(), a.genuine.tolist())
        p = [x >= THRESHOLD for x in prob(m, b.model_text.tolist())]
        acc = sum(int(x) == y for x, y in zip(p, b.genuine)) / len(b)
        cv.append({"fold": k + 1, "pairs": len(b), "accuracy": round(acc, 3),
                   "majority_baseline": round(max(b.genuine.mean(), 1 - b.genuine.mean()), 3)})
        print(f"  fold {k+1}: accuracy {acc:.3f} (always-genuine {b.genuine.mean():.3f})")
    pd.DataFrame(cv).to_csv(DATA / "cv_dev_metrics.csv", index=False)

    # ---- final model on all training postings, scored once on the test set
    model = train(spacy, tr.model_text.tolist(), tr.genuine.tolist())
    te["p_genuine"] = prob(model, te.model_text.tolist())
    keep_all = te.groupby("job_id").skill.apply(set).to_dict()
    # a candidate survives suppression unless every term it matched is suppressed
    sup = te[~te.apply(lambda r: all((r.skill, t) in SUPPRESS for t in r.terms.split("|")), axis=1)]
    keep_sup = sup.groupby("job_id").skill.apply(set).to_dict()
    keep_model = te[te.p_genuine >= THRESHOLD].groupby("job_id").skill.apply(set).to_dict()

    rows = [{"method": "keyword matcher, taxonomy as it stands", **score(keep_all, gold)},
            {"method": "keyword matcher, Task 4 'drive'/'av' suppression", **score(keep_sup, gold)},
            {"method": "keyword matcher + fine-tuned filter", **score(keep_model, gold)}]
    met = pd.DataFrame(rows); met["labels"] = "independent, read from posting text"
    met.to_csv(DATA / "evaluation_metrics.csv", index=False)
    print("\n" + met.drop(columns="labels").to_string(index=False))

    te["in_gold"] = te.apply(lambda r: r.skill in gold[r.job_id], axis=1)
    te["kept_by_model"] = te.p_genuine >= THRESHOLD
    te[["job_id", "skill", "terms", "p_genuine", "kept_by_model", "in_gold"]].round(3).to_csv(
        DATA / "evaluation_per_candidate.csv", index=False)
    missed = sorted((s for j, g in gold.items() for s in g - keep_all.get(j, set())))
    pd.Series(missed).value_counts().rename_axis("skill").reset_index(name="missed_by_matcher").to_csv(
        DATA / "matcher_misses.csv", index=False)

    model.to_disk(MODEL_DIR)
    print(f"\nmodel saved to {MODEL_DIR.name}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
