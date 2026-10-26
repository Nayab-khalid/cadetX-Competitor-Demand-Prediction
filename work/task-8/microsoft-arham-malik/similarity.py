#!/usr/bin/env python3
"""Task 8 - company similarity scoring, Microsoft's view.

Scores all four companies on the titles basis, for the same reason Task 6
uses it: NVIDIA has no description text, so full text cannot carry a
four-way comparison.

THREE MEASURES, because they disagree in useful ways.
  Jaccard on skill sets        - do they want the same skills at all
  Cosine on skill-share vectors- do they want them in the same proportions
  Cosine on title TF-IDF       - does the hiring language itself look alike
Two companies can share a skill list and weight it completely differently.
Jaccard hides that; cosine shows it.

INHERITED CAVEAT. The shared taxonomy is still NVIDIA-extended (Task 6 note),
so similarity partly measures whose vocabulary the taxonomy speaks. Microsoft
matches 5.5% of its titles against it. Low-coverage companies will look
similar to each other simply by both being sparse, which is a property of the
taxonomy and not a finding about the companies. Stated on the figure too.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).parent; ROOT=HERE/".."/".."/".."
sys.path.insert(0,str((ROOT/"scripts").resolve()))
from skill_matcher import load_taxonomy, build_matchers, extract

OUT=HERE/"data"; FIG=HERE/"figures"; STAMP="20261026"
SUPPRESS={("Autonomous Vehicles","drive"),("Autonomous Vehicles","av")}
SOURCES={
 "Microsoft":("work/task-3/microsoft-arham-malik/data/microsoft_postings_clean_20261026.csv","job_title"),
 "NVIDIA":("work/task-3/nvidia-nayab-khalid/data/processed/nvidia_postings_clean_20260902.csv",None),
 "Google":("work/task-3/google-noorul-huda-batool/cleaned_job_postings.csv",None),
 "Meta":("work/task-3/meta-abdal-farid/meta_cleaned_20260906.csv",None),
}
def pick(cols,*c):
    for x in c:
        if x in cols: return x
def hits(t,e):
    return {s for s,_,term in extract(str(t).lower(),e) if (s,term.lower()) not in SUPPRESS}

def main():
    OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
    tax=load_taxonomy(ROOT/"shared"/"taxonomy"/"skills.yaml"); entries,_=build_matchers(tax)
    allsk=[s["name"] for s in tax["skills"]]
    vecs,sets,corp,ns={},{},{},{}
    for name,(rel,tcol) in SOURCES.items():
        p=(ROOT/rel).resolve()
        if not p.exists(): print(f"  {name}: missing"); continue
        d=pd.read_csv(p,keep_default_na=False,low_memory=False)
        tcol=tcol or pick(d.columns,"clean_title","job_title","Title","title")
        per=[hits(t,entries) for t in d[tcol]]
        n=len(d); ns[name]=n
        vecs[name]=np.array([sum(sk in h for h in per)/n for sk in allsk])
        sets[name]={s for h in per for s in h}
        corp[name]=" ".join(str(t).lower() for t in d[tcol])
        print(f"  {name}: {n} postings, {len(sets[name])} distinct skills in titles")

    comps=list(vecs)
    if len(comps)<2: print("need two companies"); return
    jac=pd.DataFrame(index=comps,columns=comps,dtype=float)
    cos=pd.DataFrame(index=comps,columns=comps,dtype=float)
    for a in comps:
        for b in comps:
            u,v=sets[a],sets[b]
            jac.loc[a,b]=round(len(u&v)/len(u|v),3) if (u|v) else 0.0
            cos.loc[a,b]=round(float(cosine_similarity(vecs[a].reshape(1,-1),
                                                       vecs[b].reshape(1,-1))[0,0]),3)
    M=TfidfVectorizer(max_features=4000,ngram_range=(1,2)).fit_transform([corp[c] for c in comps])
    txt=pd.DataFrame(np.round(cosine_similarity(M),3),index=comps,columns=comps)

    jac.to_csv(OUT/f"company_jaccard_titles_{STAMP}.csv")
    cos.to_csv(OUT/f"company_cosine_skillshare_{STAMP}.csv")
    txt.to_csv(OUT/f"company_cosine_titletfidf_{STAMP}.csv")
    print("\nJaccard (shared skill sets):\n",jac.to_string())
    print("\nCosine (skill-share weighting):\n",cos.to_string())
    print("\nCosine (title TF-IDF):\n",txt.to_string())

    rows=[]
    for i,a in enumerate(comps):
        for j,b in enumerate(comps):
            if i<j: rows.append({"a":a,"b":b,"jaccard":jac.loc[a,b],
                                 "cosine_skills":cos.loc[a,b],"cosine_text":txt.loc[a,b],
                                 "jaccard_minus_cosine":round(jac.loc[a,b]-cos.loc[a,b],3)})
    pairs=pd.DataFrame(rows).sort_values("cosine_skills",ascending=False)
    pairs.to_csv(OUT/f"company_pairs_{STAMP}.csv",index=False)
    print("\nPairs, most to least similar on skill weighting:")
    print(pairs.to_string(index=False))

    fig,axes=plt.subplots(1,3,figsize=(16,5))
    for ax,(m,t) in zip(axes,[(jac,"Jaccard\nshared skill sets"),
                              (cos,"Cosine\nskill-share weighting"),
                              (txt,"Cosine\ntitle TF-IDF")]):
        im=ax.imshow(m.values.astype(float),cmap="YlGnBu",vmin=0,vmax=1)
        ax.set_xticks(range(len(comps))); ax.set_yticks(range(len(comps)))
        ax.set_xticklabels(comps,rotation=30,ha="right",fontsize=8); ax.set_yticklabels(comps,fontsize=8)
        for i in range(len(comps)):
            for j in range(len(comps)):
                v=float(m.values[i,j])
                ax.text(j,i,f"{v:.2f}",ha="center",va="center",fontsize=7,
                        color="white" if v>.6 else "black")
        ax.set_title(t,fontsize=10)
    fig.suptitle("Company similarity, titles basis — taxonomy is NVIDIA-extended, "
                 "so low-coverage companies may look alike through sparsity",fontsize=10)
    fig.tight_layout(); fig.savefig(FIG/"microsoft_similarity.png",dpi=140,bbox_inches="tight")
    print(f"\nwritten to {OUT}")

if __name__=="__main__": main()
