#!/usr/bin/env python3
"""Task 8 company similarity scoring - NVIDIA against Google, Microsoft and Meta.

Method, per the shared analysis config: canonical skill share vectors, TF-IDF weighted, compared
with cosine similarity.

Why there are three matrices and not one
----------------------------------------
Task 6 measured a bias that Task 8 cannot ignore. The 34 skills added to the taxonomy in Task 4
were chosen by reading NVIDIA job titles, and they lift NVIDIA's coverage from 21% to 72% while
lifting the other three by 2 to 6 points. A similarity matrix built on that taxonomy would report
that NVIDIA is unlike everyone else, when part of what it is really reporting is that the taxonomy
was written by NVIDIA's analyst.

So the same calculation is run three ways and the disagreement between them is the result:

  M1  extended taxonomy, titles      - what a naive run produces
  M2  pre-extension taxonomy, titles - the unbiased but sparse control
  M3  extended taxonomy, full text   - Google, Meta and Microsoft only; NVIDIA has no text

Usage:  python similarity.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "work/task-3/nvidia-nayab-khalid"))
sys.path.insert(0, str(ROOT / "work/task-6/nvidia-nayab-khalid"))
from skill_matcher import build_matchers, extract, load_taxonomy      # noqa: E402
from compare_companies import load_members                            # noqa: E402

SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdcd8"
ORDER = ["NVIDIA", "Google", "Microsoft", "Meta"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "text.color": INK, "xtick.color": INK_2, "ytick.color": INK_2,
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
})


def skill_share_matrix(df, column, entries) -> pd.DataFrame:
    """companies x skills, each cell = share of that company's postings mentioning the skill."""
    rows = []
    for company, text in zip(df.company, df[column].astype(str)):
        for name, _cat, _term in extract(text, entries):
            rows.append((company, name))
    long = pd.DataFrame(rows, columns=["company", "skill"])
    if long.empty:
        return pd.DataFrame()
    counts = long.groupby(["company", "skill"]).size().unstack(fill_value=0)
    postings = df.company.value_counts()
    return counts.div(postings.reindex(counts.index), axis=0).fillna(0)


def tfidf(mat: pd.DataFrame) -> pd.DataFrame:
    """Weight each skill by how few companies use it - a skill everyone has carries no signal."""
    n = len(mat)
    dfreq = (mat > 0).sum(axis=0)
    idf = np.log((1 + n) / (1 + dfreq)) + 1
    return mat.mul(idf, axis=1)


def cosine(mat: pd.DataFrame) -> pd.DataFrame:
    v = mat.values.astype(float)
    norm = np.linalg.norm(v, axis=1, keepdims=True)
    norm[norm == 0] = 1
    unit = v / norm
    return pd.DataFrame((unit @ unit.T).round(4), index=mat.index, columns=mat.index)


def heatmap(sim: pd.DataFrame, title, path, subtitle=""):
    labels = [c for c in ORDER if c in sim.index] or list(sim.index)
    sim = sim.loc[labels, labels]
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    # Sequential ramp, one hue light to dark - never a rainbow.
    im = ax.imshow(sim.values, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(length=0)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = sim.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=11,
                    fontweight="bold", color="white" if v > 0.55 else INK)
    ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=14)
    if subtitle:
        ax.annotate(subtitle, xy=(0, -0.16), xycoords="axes fraction", fontsize=8, color=INK_2)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.04)
    cb.set_label("cosine similarity", fontsize=8, color=INK_2)
    cb.ax.tick_params(labelsize=8, length=0)
    cb.outline.set_visible(False)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def main() -> int:
    out = Path("data/similarity"); out.mkdir(parents=True, exist_ok=True)
    figs = Path("figures"); figs.mkdir(parents=True, exist_ok=True)

    print("1. loading the four datasets and both taxonomies")
    df = load_members()
    ext = load_taxonomy(ROOT / "shared/taxonomy/skills.yaml")
    orig_p = ROOT / "work/task-6/nvidia-nayab-khalid/taxonomy_original_reference.yaml"
    e_ext, _ = build_matchers(ext)
    e_orig, _ = build_matchers(load_taxonomy(orig_p))
    print(f"   extended {len(ext['skills'])} skills | pre-extension "
          f"{len(load_taxonomy(orig_p)['skills'])} skills")

    results = {}

    print("\n2. M1 - extended taxonomy, titles")
    m1 = skill_share_matrix(df, "title_clean", e_ext)
    s1 = cosine(tfidf(m1)); results["M1_extended_titles"] = s1
    print(s1.reindex(ORDER)[ORDER].to_string())

    print("\n3. M2 - pre-extension taxonomy, titles (unbiased control)")
    m2 = skill_share_matrix(df, "title_clean", e_orig)
    s2 = cosine(tfidf(m2)); results["M2_original_titles"] = s2
    print(s2.reindex([c for c in ORDER if c in s2.index])[
        [c for c in ORDER if c in s2.index]].to_string())

    print("\n4. M3 - extended taxonomy, full text (NVIDIA has none)")
    txt = df[df.full_clean.str.len() > 200]
    m3 = skill_share_matrix(txt, "full_clean", e_ext)
    s3 = cosine(tfidf(m3)); results["M3_extended_fulltext"] = s3
    print(s3.to_string())

    for name, sim in results.items():
        sim.to_csv(out / f"similarity_{name}.csv", encoding="utf-8")

    # ---- what drives it: shared and distinguishing skills, on the unbiased basis
    print("\n5. what drives the scores")
    pairs = []
    cols = [c for c in ORDER if c in m1.index]
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            va, vb = m1.loc[a], m1.loc[b]
            both = ((va > 0) & (vb > 0))
            shared = (va[both] + vb[both]).sort_values(ascending=False)
            gap = (va - vb).abs().sort_values(ascending=False)
            pairs.append({
                "pair": f"{a} - {b}",
                "cosine_M1": s1.loc[a, b],
                "cosine_M2": s2.loc[a, b] if (a in s2.index and b in s2.index) else np.nan,
                "skills_in_common": int(both.sum()),
                "top_shared": ", ".join(shared.head(3).index),
                "top_divider": ", ".join(gap.head(3).index),
            })
    drivers = pd.DataFrame(pairs).sort_values("cosine_M1", ascending=False)
    drivers.to_csv(out / "pair_drivers.csv", index=False, encoding="utf-8")
    print(drivers.to_string(index=False))

    print("\n6. drawing heatmaps")
    heatmap(s1, "Company similarity: extended taxonomy, titles",
            figs / "fig1_similarity_extended.png",
            "Biased toward NVIDIA - see the control below")
    heatmap(s2, "Company similarity: pre-extension taxonomy, titles (control)",
            figs / "fig2_similarity_control.png",
            "The taxonomy the team actually agreed")
    heatmap(s3, "Company similarity: full description text",
            figs / "fig3_similarity_fulltext.png",
            "NVIDIA absent - its source carries no description text")

    comp = pd.DataFrame({
        "pair": drivers.pair,
        "extended_taxonomy": drivers.cosine_M1.values,
        "original_taxonomy": drivers.cosine_M2.values,
    })
    comp["shift"] = (comp.extended_taxonomy - comp.original_taxonomy).round(3)
    comp.to_csv(out / "matrix_comparison.csv", index=False, encoding="utf-8")
    print("\n--- how much the taxonomy choice moves each pair ---")
    print(comp.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
