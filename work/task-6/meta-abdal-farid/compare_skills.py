"""
Task 6 — Competitor Comparison: META skill profile
Member: Abdal Farid

Reads Task 4's feature tables (skill frequency + category frequency)
and produces Meta's Task 6 deliverables:

  - meta_comparison_skill_tiers_<stamp>.csv
  - meta_comparison_category_deep_dive_<stamp>.csv
  - meta_comparison_skill_profile_<stamp>.png

Run:
    python compare_skills.py
    python compare_skills.py --stamp 20260926
"""
import argparse
from datetime import date
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------
# Config: tier thresholds and category colours
# ------------------------------------------------------------------
TIER_CORE       = 20.0     # >= 20% of postings
TIER_SPECIALIST = 10.0     # 10–20%
TIER_NICHE      =  5.0     #  5–10%
#                             < 5%  -> Rare

TIER_ORDER  = ["Core", "Specialist", "Niche", "Rare"]
TIER_COLORS = {
    "Core":       "#4A90E2",   # blue
    "Specialist": "#ED7D31",   # orange
    "Niche":      "#7CB342",   # green
    "Rare":       "#BFBFBF",   # grey
}

CATEGORY_COLORS = {
    "research_domains":  "#4A90E2",   # blue      (Research)
    "languages":         "#E74C3C",   # red       (Languages)
    "hardware_systems":  "#7CB342",   # green     (Hardware)
    "analytics_bi":      "#F39C12",
    "product_process":   "#9B59B6",
    "mlops_devops":      "#1ABC9C",
    "ml_frameworks":     "#E67E22",
    "cloud_infra":       "#3498DB",
    "data_engineering":  "#95A5A6",
    "silicon_design":    "#34495E",
}

# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Task 6 — META skill profile")
    p.add_argument("--skill-freq",    type=Path, default=None)
    p.add_argument("--category-freq", type=Path, default=None)
    p.add_argument("--outdir",        type=Path, default=HERE)
    p.add_argument("--stamp", default=date.today().strftime("%Y%m%d"))
    return p.parse_args()


def resolve_inputs(args):
    """Find Task 4 outputs if not supplied on the CLI."""
    t4 = HERE.parents[1] / "task-4" / "meta-abdal-farid"
    if args.skill_freq is None:
        for pat in ("meta_feature_skill_frequency_*.csv",
                    "*skill_frequency*.csv",
                    "*skill_freq*.csv"):
            cands = sorted(t4.glob(pat), reverse=True)
            if cands:
                args.skill_freq = cands[0]
                break
        if args.skill_freq is None:
            raise SystemExit(f"Could not locate Task 4 skill-frequency CSV under {t4}")
    if args.category_freq is None:
        for pat in ("meta_feature_category_frequency_*.csv",
                    "*category_frequency*.csv",
                    "*category_freq*.csv"):
            cands = sorted(t4.glob(pat), reverse=True)
            if cands:
                args.category_freq = cands[0]
                break
        if args.category_freq is None:
            raise SystemExit(f"Could not locate Task 4 category-frequency CSV under {t4}")
    return args


# ------------------------------------------------------------------
# Normalise column names (tolerate minor differences in Task 4 output)
# ------------------------------------------------------------------
SKILL_ALIASES = {
    "skill_canonical": ["skill_canonical", "skill", "name", "canonical"],
    "category":        ["category", "skill_category", "cat"],
    "postings_matched": ["postings_matched", "count", "postings", "n_postings", "mentions"],
    "pct_of_postings": ["pct_of_postings", "percentage", "pct", "share", "pct_postings"],
}

def normalise_skill_df(df):
    rename = {}
    for canon, alts in SKILL_ALIASES.items():
        if canon in df.columns:
            continue
        for a in alts:
            if a in df.columns:
                rename[a] = canon
                break
    df = df.rename(columns=rename)
    required = {"skill_canonical", "category", "postings_matched", "pct_of_postings"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(
            f"Skill-frequency file is missing columns: {sorted(missing)}. "
            f"Got: {list(df.columns)}"
        )
    return df


# ------------------------------------------------------------------
# Core transformations
# ------------------------------------------------------------------
def assign_tier(pct):
    if pct >= TIER_CORE:       return "Core"
    if pct >= TIER_SPECIALIST: return "Specialist"
    if pct >= TIER_NICHE:      return "Niche"
    return "Rare"


def build_skill_tiers(skill_df):
    df = skill_df.copy()
    df["tier"] = df["pct_of_postings"].apply(assign_tier)
    df = df.sort_values("pct_of_postings", ascending=False).reset_index(drop=True)
    return df[["skill_canonical", "category", "postings_matched",
               "pct_of_postings", "tier"]]


def build_category_deep_dive(cat_df):
    """Pass-through of Task 4's category table, lightly tidied."""
    return cat_df.copy()


# ------------------------------------------------------------------
# Plot
# ------------------------------------------------------------------
def plot_profile(tiers_df, cats_df, outpath):
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    ax_top,  ax_cat   = axes[0]
    ax_pie,  ax_ment  = axes[1]

    # ---- Panel 1: Top 20 skills, coloured by category -----------
    top20 = tiers_df.head(20).iloc[::-1]        # reverse for hbar (largest on top)
    colors = [CATEGORY_COLORS.get(c, "#999999") for c in top20["category"]]
    bars = ax_top.barh(top20["skill_canonical"], top20["pct_of_postings"],
                       color=colors)
    for b, v in zip(bars, top20["pct_of_postings"]):
        ax_top.text(v + 0.4, b.get_y() + b.get_height() / 2,
                    f"{v:.1f}%", va="center", fontsize=9)
    ax_top.set_xlabel("% of postings")
    ax_top.set_title(
        "Meta Top 20 Skills\n"
        "(Blue=Research, Red=Languages, Green=Hardware)",
        fontsize=12, fontweight="bold",
    )
    ax_top.grid(axis="x", alpha=0.3)

    # ---- Panel 2: Category distribution -------------------------
    cats = cats_df.sort_values("pct_of_postings", ascending=False)
    cat_colors = [CATEGORY_COLORS.get(c, "#999999") for c in cats["category"]]
    bars2 = ax_cat.bar(cats["category"], cats["pct_of_postings"], color=cat_colors)
    for b, v in zip(bars2, cats["pct_of_postings"]):
        ax_cat.text(b.get_x() + b.get_width() / 2, v + 0.8,
                    f"{v:.1f}%", ha="center", fontsize=9)
    ax_cat.set_ylabel("% of postings")
    ax_cat.set_title(
        "Meta Skill Categories\n(% of postings mentioning category)",
        fontsize=12, fontweight="bold",
    )
    ax_cat.tick_params(axis="x", rotation=45)
    for lbl in ax_cat.get_xticklabels():
        lbl.set_ha("right")
    ax_cat.grid(axis="y", alpha=0.3)

    # ---- Panel 3: Tier pie --------------------------------------
    tier_counts = (tiers_df.groupby("tier")
                     .size()
                     .reindex(TIER_ORDER, fill_value=0))
    pie_labels = [f"{t} ({int(n)} skills)" for t, n in tier_counts.items()]
    pie_colors = [TIER_COLORS[t] for t in tier_counts.index]
    wedges, texts, autotexts = ax_pie.pie(
        tier_counts.values,
        labels=pie_labels,
        colors=pie_colors,
        autopct="%d",
        startangle=90,
        counterclock=False,
        textprops={"fontsize": 10},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    ax_pie.set_title(
        f"Skill Tier Distribution\n({len(tiers_df)} total distinct skills matched)",
        fontsize=12, fontweight="bold",
    )

    # ---- Panel 4: Total mentions by tier ------------------------
    tier_mentions = (tiers_df.groupby("tier")["postings_matched"]
                       .sum()
                       .reindex(TIER_ORDER, fill_value=0))
    bar_colors = [TIER_COLORS[t] for t in tier_mentions.index]
    bars4 = ax_ment.bar(tier_mentions.index, tier_mentions.values, color=bar_colors)
    for b, v in zip(bars4, tier_mentions.values):
        ax_ment.text(b.get_x() + b.get_width() / 2, v + 3,
                     f"{int(v)}", ha="center", fontsize=10, fontweight="bold")
    ax_ment.set_ylabel("Total skill mentions")
    ax_ment.set_title(
        "Where Meta's Hiring Signal Concentrates\n(Total mentions by tier)",
        fontsize=12, fontweight="bold",
    )
    # relabel xticks with skill counts
    ax_ment.set_xticks(range(len(tier_mentions)))
    ax_ment.set_xticklabels(
        [f"{t}\n({int(tier_counts[t])} skills)" for t in tier_mentions.index],
        fontsize=10,
    )
    ax_ment.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    args = parse_args()
    args = resolve_inputs(args)

    print(f"Reading skills:     {args.skill_freq}")
    print(f"Reading categories: {args.category_freq}")

    skill_df = normalise_skill_df(pd.read_csv(args.skill_freq))
    cat_df   = pd.read_csv(args.category_freq)

    tiers  = build_skill_tiers(skill_df)
    cats   = build_category_deep_dive(cat_df)

    tiers_path = args.outdir / f"meta_comparison_skill_tiers_{args.stamp}.csv"
    cats_path  = args.outdir / f"meta_comparison_category_deep_dive_{args.stamp}.csv"
    png_path   = args.outdir / f"meta_comparison_skill_profile_{args.stamp}.png"

    tiers.to_csv(tiers_path, index=False)
    cats.to_csv(cats_path, index=False)
    plot_profile(tiers, cats, png_path)

    # summary
    tier_summary = tiers.groupby("tier").agg(
        skills=("skill_canonical", "count"),
        mentions=("postings_matched", "sum"),
    ).reindex(TIER_ORDER)
    print(f"\n✅ {tiers_path.name}  ({len(tiers)} skills)")
    print(tier_summary.to_string())
    print(f"✅ {cats_path.name}")
    print(f"✅ {png_path.name}")


if __name__ == "__main__":
    main()
