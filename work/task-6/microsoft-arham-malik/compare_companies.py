#!/usr/bin/env python3
"""Task 6 - competitor comparison, Microsoft's view.

Reads the other three members' committed datasets from the repo and compares
all four through scripts/skill_matcher.py, so no number here is a comparison
of implementations.

BASIS. Nayab established in the NVIDIA Task 6 note that titles are the only
like-for-like basis, because NVIDIA's collection was ToS-blocked from taking
description text. That convention is followed: every cross-company claim below
is on titles. Full text is reported separately and only to quantify what the
title basis cannot see.

THE TAXONOMY CAVEAT, RESTATED. NVIDIA extended the shared taxonomy by 34
skills during Task 4, built by reading NVIDIA titles. NVIDIA's title coverage
is 72%; Microsoft's is 5.5%. Until every member extends the taxonomy for their
own company, a four-way skill comparison still partly measures the taxonomy.
Microsoft's proposed extension is in _shared/PROPOSED_taxonomy_patch.yaml and
is deliberately NOT applied here - applying it unilaterally would make
Microsoft look better for the same reason NVIDIA currently does.

Outputs (data/comparison/): skill_share_by_company_titles, category_mix,
microsoft_vs_others, basis_comparison, all dated.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
ROOT = HERE / ".." / ".." / ".."
sys.path.insert(0, str((ROOT / "scripts").resolve()))
from skill_matcher import load_taxonomy, build_matchers, extract  # noqa: E402

OUT = HERE / "data" / "comparison"
FIG = HERE / "figures"
STAMP = "20261026"
SUPPRESS = {("Autonomous Vehicles", "drive"), ("Autonomous Vehicles", "av")}

# Each entry: path relative to repo root, title column, full-text column or None
SOURCES = {
    "Microsoft": ("work/task-3/microsoft-arham-malik/data/microsoft_postings_clean_20261026.csv",
                  "job_title", "clean_text"),
    "NVIDIA": ("work/task-3/nvidia-nayab-khalid/data/processed/nvidia_postings_clean_20260902.csv",
               None, None),
    "Google": ("work/task-3/google-noorul-huda-batool/cleaned_job_postings.csv",
               None, None),
    "Meta": ("work/task-3/meta-abdal-farid/meta_cleaned_20260906.csv",
             None, None),
}


def pick(cols, *cands):
    for c in cands:
        if c in cols:
            return c
    return None


def load_company(name, spec):
    rel, tcol, fcol = spec
    path = (ROOT / rel).resolve()
    if not path.exists():
        print(f"  {name}: MISSING {rel}")
        return None
    df = pd.read_csv(path, keep_default_na=False, low_memory=False)
    tcol = tcol or pick(df.columns, "clean_title", "job_title", "Title", "title")
    fcol = fcol or pick(df.columns, "clean_text", "cleaned_description",
                        "job_description", "raw_text")
    # a text column that is really the title is not full text
    if fcol and tcol and fcol == tcol:
        fcol = None
    print(f"  {name}: {len(df):>5} rows | title={tcol} | fulltext={fcol or 'NONE'}")
    return df, tcol, fcol


def hits(text, entries):
    return {s for s, _, term in extract(str(text).lower(), entries)
            if (s, term.lower()) not in SUPPRESS}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(exist_ok=True)
    tax = load_taxonomy(ROOT / "shared" / "taxonomy" / "skills.yaml")
    entries, _ = build_matchers(tax)
    cat_of = {s["name"]: s["category"] for s in tax["skills"]}

    print("Loading committed datasets:")
    loaded = {}
    for name, spec in SOURCES.items():
        r = load_company(name, spec)
        if r:
            loaded[name] = r

    if len(loaded) < 2:
        print("\nfewer than two companies available - nothing written")
        return

    # ---- basis comparison -------------------------------------------------
    basis_rows, title_share, cat_share = [], {}, {}
    for name, (df, tcol, fcol) in loaded.items():
        tc = Counter(); cov = 0; tot = 0
        for t in df[tcol]:
            h = hits(t, entries)
            tc.update(h); tot += len(h); cov += bool(h)
        title_share[name] = {s: round(n / len(df) * 100, 2) for s, n in tc.items()}
        cc = Counter()
        for s, n in tc.items():
            cc[cat_of.get(s, "other")] += n
        tot_cat = sum(cc.values()) or 1
        cat_share[name] = {k: round(v / tot_cat * 100, 1) for k, v in cc.items()}

        row = {"company": name, "postings": len(df),
               "titles_skills_per_posting": round(tot / len(df), 2),
               "titles_coverage_pct": round(cov / len(df) * 100, 1)}
        if fcol:
            ft = fc = 0
            for t in df[fcol]:
                h = hits(t, entries)
                ft += len(h); fc += bool(h)
            row["fulltext_skills_per_posting"] = round(ft / len(df), 2)
            row["fulltext_coverage_pct"] = round(fc / len(df) * 100, 1)
        else:
            row["fulltext_skills_per_posting"] = None
            row["fulltext_coverage_pct"] = None
        basis_rows.append(row)

    basis = pd.DataFrame(basis_rows)
    basis.to_csv(OUT / f"basis_comparison_{STAMP}.csv", index=False)
    print("\nBasis comparison:")
    print(basis.to_string(index=False))

    # ---- skill share matrix, titles --------------------------------------
    allsk = sorted({s for d in title_share.values() for s in d})
    mat = pd.DataFrame({c: {s: title_share[c].get(s, 0.0) for s in allsk}
                        for c in title_share})
    mat["max_gap"] = mat.max(axis=1) - mat.min(axis=1)
    mat = mat.sort_values("max_gap", ascending=False)
    mat.to_csv(OUT / f"skill_share_by_company_titles_{STAMP}.csv")

    cm = pd.DataFrame(cat_share).fillna(0).round(1)
    cm.to_csv(OUT / f"category_mix_by_company_titles_{STAMP}.csv")
    print("\nCategory mix by company (% of title skill hits):")
    print(cm.to_string())

    # ---- Microsoft vs the field -------------------------------------------
    others = [c for c in mat.columns if c not in ("Microsoft", "max_gap")]
    sk = mat.drop(columns="max_gap")
    gaps = pd.DataFrame({
        "skill": sk.index,
        "microsoft": sk["Microsoft"].values,
        "others_mean": sk[others].mean(axis=1).round(2).values,
    })
    gaps["gap"] = (gaps["microsoft"] - gaps["others_mean"]).round(2)
    gaps = gaps.sort_values("gap", ascending=False)
    gaps.to_csv(OUT / f"microsoft_vs_others_titles_{STAMP}.csv", index=False)
    print("\nMicrosoft ahead of the field (titles):")
    print(gaps.head(5).to_string(index=False))
    print("\nMicrosoft behind the field (titles):")
    print(gaps.tail(5).to_string(index=False))

    # ---- figures ----------------------------------------------------------
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(15, 6))
    b = basis.set_index("company")
    x = range(len(b))
    a1.bar([i - .2 for i in x], b["titles_coverage_pct"], width=.4,
           label="titles", color="#1F3864")
    a1.bar([i + .2 for i in x], b["fulltext_coverage_pct"].fillna(0), width=.4,
           label="full text", color="#9DC3E6")
    a1.set_xticks(list(x)); a1.set_xticklabels(b.index)
    a1.set_ylabel("% of postings with >=1 skill matched")
    a1.set_title("What each source can see\n"
                 "NVIDIA and Google have no usable description text", fontsize=10)
    a1.legend(fontsize=8); a1.grid(axis="y", alpha=.3)

    top = sk.loc[mat.head(18).index]
    im = a2.imshow(top.values, cmap="YlGnBu", aspect="auto")
    a2.set_xticks(range(len(top.columns)))
    a2.set_xticklabels(top.columns, rotation=30, ha="right")
    a2.set_yticks(range(len(top))); a2.set_yticklabels(top.index, fontsize=7)
    for i in range(len(top)):
        for j in range(len(top.columns)):
            v = top.values[i, j]
            a2.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=6,
                    color="white" if v > top.values.max() * .6 else "black")
    a2.set_title("Skill share by company, titles basis (%)\n"
                 "18 widest-spread skills", fontsize=10)
    fig.colorbar(im, ax=a2, shrink=.7)
    fig.tight_layout()
    fig.savefig(FIG / "microsoft_comparison.png", dpi=140, bbox_inches="tight")
    print(f"\nwritten to {OUT}")


if __name__ == "__main__":
    main()
