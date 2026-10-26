#!/usr/bin/env python3
"""Optional Task 12 - fine-tune a skill NER model, Microsoft.

Bootstraps training labels from the Task 4 keyword output, trains a spaCy NER
component, and scores it against the keyword baseline on a held-out split.

Written to run locally; see README.md for why it was not run in preparation.

    pip install spacy && python -m spacy download en_core_web_sm
    python train_skill_ner.py
"""
from __future__ import annotations
import json, random, sys
from pathlib import Path
import pandas as pd

HERE=Path(__file__).parent; W=HERE/".."/".."
FEAT=W/"task-4"/"microsoft-arham-malik"/"data"/"features"/"microsoft_skill_features_20261026.csv"
OUT=HERE/"data"
SEED=20261026; TRAIN_FRAC=0.7; ITER=30

def spans(text, skills):
    """Character spans for each skill mention. Overlaps are dropped - spaCy
    rejects overlapping entities and silently training on them degrades the
    model rather than erroring."""
    low=text.lower(); out=[]
    for s in skills:
        start=low.find(s.lower())
        while start!=-1:
            end=start+len(s)
            if not any(start<e and end>b for b,e,_ in out):
                out.append((start,end,"SKILL"))
            start=low.find(s.lower(),end)
    return sorted(out)

def main():
    try:
        import spacy
        from spacy.training import Example
    except ImportError:
        print("spaCy not installed. pip install spacy && python -m spacy download en_core_web_sm")
        return 1
    OUT.mkdir(exist_ok=True)
    df=pd.read_csv(FEAT,keep_default_na=False)
    data=[]
    for _,r in df.iterrows():
        try: sk=json.loads(r["extracted_skills"])
        except Exception: sk=[]
        if not sk: continue
        t=str(r["clean_text"])[:2000]
        ents=spans(t,sk)
        if ents: data.append((t,{"entities":ents}))
    random.Random(SEED).shuffle(data)
    cut=int(len(data)*TRAIN_FRAC); train,test=data[:cut],data[cut:]
    print(f"{len(train)} train / {len(test)} test postings")

    nlp=spacy.blank("en"); ner=nlp.add_pipe("ner"); ner.add_label("SKILL")
    opt=nlp.begin_training()
    for i in range(ITER):
        random.Random(SEED+i).shuffle(train); losses={}
        for text,ann in train:
            nlp.update([Example.from_dict(nlp.make_doc(text),ann)],drop=0.3,losses=losses,sgd=opt)
        if (i+1)%10==0: print(f"  iter {i+1:3} loss {losses.get('ner',0):.1f}")

    tp=fp=fn=0
    for text,ann in test:
        gold={(b,e) for b,e,_ in ann["entities"]}
        pred={(e.start_char,e.end_char) for e in nlp(text).ents}
        tp+=len(gold&pred); fp+=len(pred-gold); fn+=len(gold-pred)
    p=tp/(tp+fp) if tp+fp else 0; r=tp/(tp+fn) if tp+fn else 0
    f1=2*p*r/(p+r) if p+r else 0
    print(f"\nmodel      precision {p:.3f}  recall {r:.3f}  F1 {f1:.3f}")
    print("baseline   precision 1.000  recall 1.000  F1 1.000  (labels came FROM it)")
    print("\nThe baseline scores 1.0 by construction because it generated the")
    print("labels. The honest comparison needs hand-corrected labels - correct")
    print("a sample by hand first, then re-run. Until then this measures only")
    print("whether the model reproduces the keyword matcher.")
    pd.DataFrame([{"model":"spacy_ner","precision":round(p,3),"recall":round(r,3),
                   "f1":round(f1,3),"labels":"bootstrapped_uncorrected"}]).to_csv(
        OUT/"evaluation_metrics.csv",index=False)
    nlp.to_disk(OUT/"fine_tuned_skill_ner")
    return 0

if __name__=="__main__": sys.exit(main())
