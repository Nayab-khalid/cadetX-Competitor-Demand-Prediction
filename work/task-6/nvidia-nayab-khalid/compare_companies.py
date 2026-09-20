#!/usr/bin/env python3
"""Task 6 competitor comparison - NVIDIA against the team's other three companies.

Reads each member's committed dataset, extracts skills from all four with the same shared
taxonomy and the same matcher, and compares them.

The comparability problem, and what is done about it
----------------------------------------------------
The four datasets are not alike. NVIDIA carries job titles only, because NVIDIA's Terms of Service
rule out collecting from its own careers site (Task 1). Meta and Microsoft carry full descriptions
of around 3,200 and 3,700 characters. Google carries responsibilities and qualifications text but
no dates at all. Extracting skills from a description finds ten to twenty per posting; from a title
it finds about one. Comparing those numbers directly would measure the data sources, not the
companies.

So everything is computed on two bases and reported separately:

  Basis A - TITLES ONLY, all four companies. Every member's data has a job title, so this is
            like-for-like and it is the basis for every comparison claim in the note.
  Basis B - FULL TEXT where it exists (Google, Meta, Microsoft). Not comparable with NVIDIA;
            included only to quantify what the NVIDIA data cannot see.

Outputs: data/comparison/*.csv and figures/*.png

Usage:  python compare_companies.py
"""
from __future__ import annotations

import json
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
from skill_matcher import build_matchers, extract, load_taxonomy      # noqa: E402
from preprocess_nvidia import clean_text, normalise_unicode           # noqa: E402

SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdcd8"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
# Colour follows the entity, fixed for the whole project so a chart never repaints a company.
COMPANY_COLOUR = {"NVIDIA": SERIES[0], "Google": SERIES[1],
                  "Microsoft": SERIES[2], "Meta": SERIES[3]}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_2, "text.color": INK,
    "xtick.color": INK_2, "ytick.color": INK_2, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
})


def style(ax, title, ylabel=""):
    ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(axis="y", alpha=0.9)
    ax.tick_params(length=0)
    return ax


def load_members() -> pd.DataFrame:
    """Normalise four differently-shaped datasets into company / title / full_text."""
    frames = []

    nv = pd.read_csv(sorted((ROOT / "work/task-3/nvidia-nayab-khalid/data/processed")
                            .glob("nvidia_postings_clean_*.csv"))[-1])
    frames.append(pd.DataFrame({"company": "NVIDIA", "title": nv.job_title.astype(str),
                                "full_text": ""}))

    g = pd.read_csv(ROOT / "work/task-2/google-noorul-huda-batool/job_skills.csv")
    # 23 of 1,250 rows are YouTube postings; this comparison is company-level, so they are dropped.
    g = g[g.Company.astype(str).str.strip() == "Google"]
    gtext = (g["Responsibilities"].fillna("") + " " + g["Minimum Qualifications"].fillna("")
             + " " + g["Preferred Qualifications"].fillna(""))
    frames.append(pd.DataFrame({"company": "Google", "title": g.Title.astype(str),
                                "full_text": gtext.astype(str)}))

    mt = pd.read_csv(ROOT / "work/task-2/meta-abdal-farid/meta_postings_raw_20260906.csv")
    frames.append(pd.DataFrame({"company": "Meta", "title": mt.job_title.astype(str),
                                "full_text": mt.job_description.fillna("").astype(str)}))

    ms = pd.read_csv(ROOT / "work/task-2/microsoft-arham-malik/microsoft_jobs_dataset.csv",
                     low_memory=False)
    frames.append(pd.DataFrame({"company": "Microsoft", "title": ms.job_title.astype(str),
                                "full_text": ms.job_description.fillna("").astype(str)}))

    df = pd.concat(frames, ignore_index=True)
    df["title_clean"] = df.title.map(lambda t: clean_text(normalise_unicode(t)))
    df["full_clean"] = df.full_text.str.lower()
    return df


def extract_basis(df: pd.DataFrame, column: str, entries) -> pd.DataFrame:
    rows = []
    for company, text in zip(df.company, df[column].astype(str)):
        for name, category, term in extract(text, entries):
            rows.append({"company": company, "skill": name, "skill_category": category})
    return pd.DataFrame(rows)


def main() -> int:
    out = Path("data/comparison"); out.mkdir(parents=True, exist_ok=True)
    figs = Path("figures"); figs.mkdir(parents=True, exist_ok=True)

    print("1. loading the four members' datasets")
    df = load_members()
    tax = load_taxonomy(ROOT / "shared/taxonomy/skills.yaml")
    entries, _ = build_matchers(tax)
    counts = df.company.value_counts()
    print(df.groupby("company").agg(postings=("title", "size"),
                                    with_full_text=("full_text", lambda s: int((s.str.len() > 200).sum()))
                                    ).to_string())

    print("\n2. Basis A - titles only, all four companies (like-for-like)")
    a = extract_basis(df, "title_clean", entries)
    per_post_a = (df.assign(n=[len(extract(t, entries)) for t in df.title_clean])
                  .groupby("company").n.agg(["mean", lambda s: (s > 0).mean()]))
    per_post_a.columns = ["skills_per_posting", "coverage"]
    print(per_post_a.round(3).to_string())

    # ---- the validity control. The Task 4 extension added 34 skills chosen to describe NVIDIA's
    # vocabulary. If NVIDIA's coverage advantage disappears under the pre-extension taxonomy, the
    # advantage is a property of my taxonomy work and not of NVIDIA's hiring.
    print("\n2b. control: the same titles against the pre-extension taxonomy")
    orig_path = Path(__file__).with_name("taxonomy_original_reference.yaml")
    control = None
    if orig_path.exists():
        otax = load_taxonomy(orig_path)
        oentries, _ = build_matchers(otax)
        n_orig = [len(extract(t, oentries)) for t in df.title_clean]
        control = (df.assign(n=n_orig).groupby("company").n
                   .agg(orig_skills_per_posting="mean",
                        orig_coverage=lambda s: (s > 0).mean()))
        control["orig_coverage"] = (control.orig_coverage * 100).round(1)
        control["orig_skills_per_posting"] = control.orig_skills_per_posting.round(2)
        print(f"   pre-extension taxonomy: {len(otax['skills'])} skills")
        print(control.to_string())
    else:
        print(f"   SKIPPED - {orig_path.name} not present")

    print("\n3. Basis B - full text where it exists")
    has_text = df[df.full_clean.str.len() > 200]
    b = extract_basis(has_text, "full_clean", entries)
    per_post_b = (has_text.assign(n=[len(extract(t, entries)) for t in has_text.full_clean])
                  .groupby("company").n.agg(["mean", lambda s: (s > 0).mean()]))
    per_post_b.columns = ["skills_per_posting", "coverage"]
    print(per_post_b.round(3).to_string())

    # ---------------------------------------------------------------- tables
    print("\n4. building comparison tables")
    share_a = (a.groupby(["skill", "company"]).size().unstack(fill_value=0)
               .div(counts, axis=1).fillna(0) * 100).round(2)
    share_a["max_gap"] = (share_a.max(axis=1) - share_a.min(axis=1)).round(2)
    share_a = share_a.sort_values("max_gap", ascending=False)
    share_a.to_csv(out / "skill_share_by_company_titles.csv", encoding="utf-8")

    cat_a = (a.groupby(["company", "skill_category"]).size().unstack(fill_value=0))
    cat_share = (cat_a.div(cat_a.sum(axis=1), axis=0) * 100).round(1)
    cat_share.to_csv(out / "category_mix_by_company_titles.csv", encoding="utf-8")

    basis = pd.DataFrame({
        "postings": counts,
        "titles_skills_per_posting": per_post_a.skills_per_posting.round(2),
        "titles_coverage_pct": (per_post_a.coverage * 100).round(1),
        "fulltext_skills_per_posting": per_post_b.skills_per_posting.round(2),
        "fulltext_coverage_pct": (per_post_b.coverage * 100).round(1),
    })
    if control is not None:
        basis = basis.join(control)
    basis.to_csv(out / "basis_comparison.csv", encoding="utf-8")
    print(basis.to_string())

    # fig 0: the validity control, drawn first because it governs how the rest may be read
    if control is not None:
        order0 = [c for c in ["NVIDIA", "Google", "Microsoft", "Meta"] if c in control.index]
        fig, ax = plt.subplots(figsize=(9, 3.8))
        x0 = np.arange(len(order0))
        o = [control.orig_coverage.get(c, 0) for c in order0]
        n = [round(per_post_a.coverage.get(c, 0) * 100, 1) for c in order0]
        ax.bar(x0 - 0.19, o, width=0.36, color=SERIES[2], label="pre-extension taxonomy (59 skills)")
        ax.bar(x0 + 0.19, n, width=0.36, color=SERIES[0], label="extended taxonomy (93 skills)")
        for xi, (a_, b_) in enumerate(zip(o, n)):
            ax.text(xi - 0.19, a_ + 1.5, f"{a_:.0f}%", ha="center", fontsize=8.5, color=INK,
                    fontweight="bold")
            ax.text(xi + 0.19, b_ + 1.5, f"{b_:.0f}%", ha="center", fontsize=8.5, color=INK,
                    fontweight="bold")
        style(ax, "Validity control: whose taxonomy is being measured?",
              "postings with at least one skill (%)")
        ax.set_xticks(x0); ax.set_xticklabels(order0)
        ax.legend(frameon=False, fontsize=8.5, labelcolor=INK_2)
        ax.set_ylim(0, 88)
        fig.tight_layout(); fig.savefig(figs / "fig0_validity_control.png", dpi=200); plt.close(fig)

    # NVIDIA versus the mean of the other three, on titles
    others = [c for c in counts.index if c != "NVIDIA"]
    diff = pd.DataFrame({
        "NVIDIA": share_a.get("NVIDIA", pd.Series(dtype=float)),
        "others_mean": share_a[others].mean(axis=1).round(2),
    })
    diff["gap"] = (diff.NVIDIA - diff.others_mean).round(2)
    diff = diff.sort_values("gap", ascending=False)
    diff.to_csv(out / "nvidia_vs_others_titles.csv", encoding="utf-8")
    print("\nNVIDIA most distinctive (titles):")
    print(diff.head(8).to_string())
    print("\nNVIDIA most absent (titles):")
    print(diff.tail(6).to_string())

    # ---------------------------------------------------------------- figures
    print("\n5. drawing figures")
    order = ["NVIDIA", "Google", "Microsoft", "Meta"]
    order = [c for c in order if c in counts.index]

    # fig 1: the comparability problem itself
    fig, ax = plt.subplots(figsize=(9, 3.8))
    x = np.arange(len(order))
    t_vals = [per_post_a.skills_per_posting.get(c, 0) for c in order]
    f_vals = [per_post_b.skills_per_posting.get(c, np.nan) for c in order]
    ax.bar(x - 0.19, t_vals, width=0.36, color=SERIES[0], label="from job titles")
    ax.bar(x + 0.19, [0 if np.isnan(v) else v for v in f_vals], width=0.36,
           color=SERIES[1], label="from full description text")
    for xi, (t, f) in enumerate(zip(t_vals, f_vals)):
        ax.text(xi - 0.19, t + 0.25, f"{t:.2f}", ha="center", fontsize=8.5, color=INK,
                fontweight="bold")
        ax.text(xi + 0.19, (0 if np.isnan(f) else f) + 0.25,
                "no text" if np.isnan(f) else f"{f:.1f}", ha="center", fontsize=8.5,
                color=INK, fontweight="bold")
    style(ax, "Skills found per posting, by what the source actually contains",
          "skills per posting")
    ax.set_xticks(x); ax.set_xticklabels(order)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK_2)
    ax.set_ylim(0, max([v for v in f_vals if not np.isnan(v)] + t_vals) * 1.2)
    fig.tight_layout(); fig.savefig(figs / "fig1_basis_gap.png", dpi=200); plt.close(fig)

    # fig 2: category mix, titles basis, 100% stacked
    fig, ax = plt.subplots(figsize=(9, 4.2))
    cats = cat_share.columns.tolist()
    bottom = np.zeros(len(order))
    for i, c in enumerate(cats):
        vals = np.array([cat_share.loc[co, c] if co in cat_share.index else 0 for co in order])
        ax.bar(np.arange(len(order)), vals, bottom=bottom, width=0.6,
               color=SERIES[i % len(SERIES)], edgecolor=SURFACE, linewidth=2, label=c)
        for xi, (v, bt) in enumerate(zip(vals, bottom)):
            if v >= 7:
                ax.text(xi, bt + v / 2, f"{v:.0f}", ha="center", va="center", fontsize=7.5,
                        color="white", fontweight="bold")
        bottom += vals
    style(ax, "Skill mix by category, titles basis (like-for-like)", "share of mentions (%)")
    ax.set_xticks(np.arange(len(order))); ax.set_xticklabels(order)
    ax.set_ylim(0, 100); ax.set_yticks([0, 25, 50, 75, 100])
    ax.legend(frameon=False, ncol=4, fontsize=8, loc="upper center",
              bbox_to_anchor=(0.5, -0.10), labelcolor=INK_2, handlelength=1.4)
    fig.tight_layout(); fig.savefig(figs / "fig2_category_mix.png", dpi=200); plt.close(fig)

    # fig 3: where NVIDIA differs most
    top = pd.concat([diff.head(7), diff.tail(5)]).sort_values("gap")
    fig, ax = plt.subplots(figsize=(9, 5.0))
    y = np.arange(len(top))
    colours = [SERIES[0] if g > 0 else SERIES[1] for g in top.gap]
    ax.barh(y, top.gap, color=colours, height=0.62)
    ax.set_yticks(y); ax.set_yticklabels(top.index, fontsize=8.5)
    ax.axvline(0, color=INK_2, linewidth=1)
    for yi, g in enumerate(top.gap):
        ax.text(g + (0.25 if g > 0 else -0.25), yi, f"{g:+.1f}", va="center",
                ha="left" if g > 0 else "right", fontsize=8, color=INK, fontweight="bold")
    style(ax, "Where NVIDIA differs from the other three, titles basis", "")
    ax.set_xlabel("percentage points of postings, NVIDIA minus the mean of the other three",
                  fontsize=8.5)
    ax.grid(axis="x", alpha=0.9); ax.grid(axis="y", visible=False)
    ax.set_xlim(top.gap.min() * 1.35, top.gap.max() * 1.35)
    fig.tight_layout(); fig.savefig(figs / "fig3_nvidia_vs_others.png", dpi=200); plt.close(fig)
    print(f"   wrote 3 figures to {figs}/")

    print("\n--- summary for the comparison note ---")
    print(f"companies compared     {', '.join(order)}")
    print(f"postings               {dict(counts[order])}")
    print(f"\ncategory mix (titles basis, % of mentions):\n{cat_share.reindex(order).to_string()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
