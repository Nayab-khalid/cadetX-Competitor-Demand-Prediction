#!/usr/bin/env python3
"""Task 9 - insight generation, Microsoft.

Pulls the numbers from Tasks 4, 5, 6 and 8 and writes the tables and figure
behind the insight note. Re-running it regenerates every figure quoted in the
note, so the note cannot drift from the data.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).parent; W=HERE/".."/".."
FEAT=W/"task-4"/"microsoft-arham-malik"/"data"/"features"
OUT=HERE/"data"; FIG=HERE/"figures"; STAMP="20261026"

def sset(v):
    try: return set(json.loads(v))
    except Exception: return set()

def main():
    OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
    f=pd.read_csv(FEAT/f"microsoft_skill_features_{STAMP}.csv",keep_default_na=False)
    freq=pd.read_csv(FEAT/f"microsoft_skill_frequency_{STAMP}.csv")
    swe=pd.read_csv(W/"task-5"/"microsoft-arham-malik"/"data"/f"microsoft_cohort_trends_swe_{STAMP}.csv")
    basis=pd.read_csv(W/"task-6"/"microsoft-arham-malik"/"data"/"comparison"/f"basis_comparison_{STAMP}.csv")
    n=len(f)

    # co-occurrence lift against Azure
    az=f["extracted_skills"].apply(lambda v:"Azure" in sset(v))
    rows=[]
    for sk in freq["skill"]:
        if sk=="Azure": continue
        h=f["extracted_skills"].apply(lambda v,s=sk: s in sset(v))
        if h.sum()<15: continue
        both=int((az&h).sum())
        rows.append({"skill":sk,"with_azure":both,"skill_total":int(h.sum()),
                     "lift":round((both/az.sum())/(h.sum()/n),2)})
    lift=pd.DataFrame(rows).sort_values("lift",ascending=False)
    lift.to_csv(OUT/f"microsoft_azure_cooccurrence_{STAMP}.csv",index=False)

    # seniority gradient
    g=[]
    for sk in freq.head(25)["skill"]:
        h=f["extracted_skills"].apply(lambda v,s=sk: s in sset(v))
        rec={"skill":sk}
        for lvl in ["Mid","Senior","Principal"]:
            m=f["seniority_level"]==lvl
            rec[lvl]=round(h[m].sum()/m.sum()*100,1) if m.sum() else 0.0
        rec["gradient"]=round(rec["Principal"]-rec["Mid"],1); g.append(rec)
    grad=pd.DataFrame(g).sort_values("gradient",ascending=False)
    grad.to_csv(OUT/f"microsoft_seniority_gradient_{STAMP}.csv",index=False)

    head={"postings":n,
          "azure_pct":float(freq.loc[freq.skill=="Azure","pct_of_postings"].iloc[0]),
          "titles_coverage_pct":float(basis.loc[basis.company=="Microsoft","titles_coverage_pct"].iloc[0]),
          "fulltext_coverage_pct":float(basis.loc[basis.company=="Microsoft","fulltext_coverage_pct"].iloc[0]),
          "mean_skills_fulltext":round(float(f["skill_count"].mean()),2),
          "swe_rising":swe.head(3)[["skill","change"]].to_dict("records"),
          "swe_falling":swe.tail(3)[["skill","change"]].to_dict("records")}
    (OUT/f"microsoft_headline_{STAMP}.json").write_text(json.dumps(head,indent=2))
    for k,v in head.items():
        if not isinstance(v,list): print(f"  {k:24} {v}")
    print("\nAzure co-occurrence, top:"); print(lift.head(6).to_string(index=False))
    print("\nSeniority gradient, top:"); print(grad.head(5).to_string(index=False))

    fig,axes=plt.subplots(1,3,figsize=(16,5))
    t=freq.head(10).iloc[::-1]
    axes[0].barh(t["skill"],t["pct_of_postings"],color="#1F3864")
    axes[0].set_xlabel("% of postings"); axes[0].set_title("Skills in demand (full text)",fontsize=10)
    axes[0].grid(axis="x",alpha=.3)
    gg=grad.head(6).iloc[::-1]; y=np.arange(len(gg))
    axes[1].barh(y-.2,gg["Mid"],height=.4,label="Mid",color="#9DC3E6")
    axes[1].barh(y+.2,gg["Principal"],height=.4,label="Principal",color="#1F3864")
    axes[1].set_yticks(y); axes[1].set_yticklabels(gg["skill"],fontsize=8)
    axes[1].set_title("What seniority buys",fontsize=10); axes[1].legend(fontsize=8)
    axes[1].grid(axis="x",alpha=.3)
    b=basis.set_index("company")
    x=np.arange(len(b))
    axes[2].bar(x-.2,b["titles_coverage_pct"],width=.4,label="titles",color="#1F3864")
    axes[2].bar(x+.2,b["fulltext_coverage_pct"].fillna(0),width=.4,label="full text",color="#9DC3E6")
    axes[2].set_xticks(x); axes[2].set_xticklabels(b.index,fontsize=8)
    axes[2].set_title("Microsoft is invisible on the\ncomparable basis",fontsize=10)
    axes[2].legend(fontsize=8); axes[2].grid(axis="y",alpha=.3)
    fig.suptitle(f"Microsoft hiring intelligence — {n} engineering postings",fontsize=12)
    fig.tight_layout(); fig.savefig(FIG/"microsoft_insight_summary.png",dpi=140,bbox_inches="tight")
    print(f"\nwritten to {OUT}")

if __name__=="__main__": main()
