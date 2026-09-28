"""
Task 9 — Insight Generation & Reporting (META)
Member: Abdal Farid

Builds the executive-summary infographic from Task 6's CSVs and verifies
that the (hand-written) insight report exists alongside it.

Outputs:
  - meta_insight_executive_summary_<stamp>.png
  - (checks) meta_insight_report_<stamp>.md

Run:
    python generate_insights.py
    python generate_insights.py --stamp 20260927
"""
import argparse
from datetime import date
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


HERE = Path(__file__).resolve().parent

# Display-name mapping for category labels on the hbar chart
CATEGORY_LABELS = {
    "research_domains": "Research\nDomains",
    "mlops_devops":     "MLOps/\nDevOps",
    "product_process":  "Product\nProcess",
    "analytics_bi":     "Analytics/\nBI",
    "ml_frameworks":    "ML\nFrameworks",
    "languages":        "Languages",
    "hardware_systems": "Hardware",
    "cloud_infra":      "Cloud Infra",
    "data_engineering": "Data Eng",
    "silicon_design":   "Silicon Design",
}


# ------------------------------------------------------------------
# CLI / inputs
# ------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Task 9 — META insights")
    p.add_argument("--tiers",    type=Path, default=None,
                   help="Task 6 meta_comparison_skill_tiers_*.csv")
    p.add_argument("--category", type=Path, default=None,
                   help="Task 6 meta_comparison_category_deep_dive_*.csv")
    p.add_argument("--outdir", type=Path, default=HERE)
    p.add_argument("--stamp", default=date.today().strftime("%Y%m%d"))
    return p.parse_args()


def resolve_inputs(args):
    t6 = HERE.parents[1] / "task-6" / "meta-abdal-farid"
    if args.tiers is None:
        for pat in ("meta_comparison_skill_tiers_*.csv",
                    "*skill_tiers*.csv"):
            cands = sorted(t6.glob(pat), reverse=True)
            if cands:
                args.tiers = cands[0]; break
        if args.tiers is None:
            raise SystemExit(f"Tiers CSV not found under {t6}")
    if args.category is None:
        for pat in ("meta_comparison_category_deep_dive_*.csv",
                    "*category_deep_dive*.csv"):
            cands = sorted(t6.glob(pat), reverse=True)
            if cands:
                args.category = cands[0]; break
        if args.category is None:
            raise SystemExit(f"Category deep-dive CSV not found under {t6}")
    return args


# ------------------------------------------------------------------
# Derived stats
# ------------------------------------------------------------------
def compute_stats(tiers_df, cats_df):
    """Pull the numbers the infographic needs."""
    tiers = tiers_df.sort_values("pct_of_postings", ascending=False)

    # Top 5 skills for the left chart
    top5 = tiers.head(5)[["skill_canonical", "pct_of_postings"]].values.tolist()

    # Top 5 categories for the right chart (already sorted by Task 6)
    cats = cats_df.sort_values("pct_of_postings", ascending=False).head(5)
    top5_cat = list(zip(cats["category"], cats["pct_of_postings"]))

    def pct_of(skill):
        row = tiers[tiers["skill_canonical"] == skill]
        return float(row["pct_of_postings"].iloc[0]) if len(row) else 0.0

    def cat_pct(category):
        row = cats_df[cats_df["category"] == category]
        return float(row["pct_of_postings"].iloc[0]) if len(row) else 0.0

    return {
        "top5_skills":       top5,
        "top5_categories":   top5_cat,
        "research_share":    cat_pct("research_domains"),
        "cloud_share":       cat_pct("cloud_infra"),
        "data_eng_share":    cat_pct("data_engineering"),
        "silicon_share":     cat_pct("silicon_design"),
        "sre_share":         pct_of("Site Reliability"),
        "cpp_share":         pct_of("C++"),
        "rust_share":        pct_of("Rust"),   # may be 0 if not matched
        "python_share":      pct_of("Python"),
    }


# ------------------------------------------------------------------
# Box helper
# ------------------------------------------------------------------
def draw_box(ax, facecolor, edgecolor, rounding=0.04, linewidth=2.0):
    box = FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle=f"round,pad=0.01,rounding_size={rounding}",
        linewidth=linewidth,
        edgecolor=edgecolor, facecolor=facecolor,
        transform=ax.transAxes, clip_on=False,
    )
    ax.add_patch(box)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


# ------------------------------------------------------------------
# Figure
# ------------------------------------------------------------------
def build_infographic(s, outpath):
    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor("white")

    # --- Main title ---
    fig.text(0.5, 0.965,
             "Meta: Hiring Strategy & Market Position",
             ha="center", fontsize=22, fontweight="bold")
    fig.text(0.5, 0.935,
             "Executive Summary (Sept 2026)",
             ha="center", fontsize=18, fontweight="bold")

    # ==================================================================
    # Blue thesis box — full width, top
    # ==================================================================
    ax_top = fig.add_axes([0.05, 0.79, 0.90, 0.12])
    draw_box(ax_top, "#E3F0F7", "#7BA7C4", rounding=0.05)
    ax_top.text(0.02, 0.88,
                "CORE HIRING THESIS: Meta is building an AI-research-first organization",
                fontsize=13, fontweight="bold", family="monospace", va="top")
    bullets = [
        f"• {int(s['research_share'])}% of jobs require ML/AI research skills "
        "(LLMs, Recommendations, Generative AI, Computer Vision, Robotics)",
        f"• Python-dominant tech stack: {int(s['python_share'])}% Python "
        "vs. <5% for any other language (C++, Go, Rust, Java)",
        f"• Infrastructure is minimal: {s['cloud_share']:.0f}% cloud hiring, "
        f"{s['data_eng_share']:.0f}% data engineering — "
        "suggesting outsourced or centralized functions",
    ]
    for i, b in enumerate(bullets):
        ax_top.text(0.025, 0.58 - i * 0.22, b,
                    fontsize=11, family="monospace", va="top")

    # ==================================================================
    # Left bar chart — Top 5 skills
    # ==================================================================
    ax_skills = fig.add_axes([0.05, 0.40, 0.26, 0.30])
    names  = [n for n, _ in s["top5_skills"]]
    values = [v for _, v in s["top5_skills"]]
    bars = ax_skills.bar(range(len(names)), values, color="#4A90E2",
                         edgecolor="#2E5C8A", linewidth=0.8)
    for b, v in zip(bars, values):
        ax_skills.text(b.get_x() + b.get_width() / 2, v + 0.6,
                       f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold")
    ax_skills.set_xticks(range(len(names)))
    ax_skills.set_xticklabels(names, fontsize=9, rotation=0)
    ax_skills.set_ylabel("% of postings", fontsize=11, fontweight="bold")
    ax_skills.set_title("Top 5 Skills\n(% of job postings)",
                        fontsize=13, fontweight="bold")
    ax_skills.set_ylim(0, max(values) * 1.15)
    ax_skills.grid(axis="y", alpha=0.3)

    # ==================================================================
    # Pink box — What Meta is NOT hiring for
    # ==================================================================
    ax_not = fig.add_axes([0.37, 0.40, 0.26, 0.30])
    draw_box(ax_not, "#FADBD8", "#C97B7B", rounding=0.05)
    ax_not.text(0.04, 0.93,
                "WHAT META IS NOT HIRING FOR:",
                fontsize=12, fontweight="bold", va="top")
    ax_not.text(0.05, 0.72,
                f"□  Infrastructure roles\n"
                f"    (Cloud: {s['cloud_share']:.0f}%, "
                f"Data Eng: {s['data_eng_share']:.0f}%)\n\n"
                f"□  DevOps / Reliability\n"
                f"    (Site Reliability: {s['sre_share']:.0f}%, CI/CD: <2%)\n\n"
                f"□  Systems programming\n"
                f"    (C++: {s['cpp_share']:.0f}%, Rust: 0.5%)\n\n"
                f"□  Chip design\n"
                f"    (Silicon design: {s['silicon_share']:.0f}%)",
                fontsize=10.5, va="top")

    # ==================================================================
    # Right hbar chart — Hiring by category (Top 5)
    # ==================================================================
    ax_cat = fig.add_axes([0.69, 0.40, 0.26, 0.30])
    cat_names  = [CATEGORY_LABELS.get(c, c) for c, _ in s["top5_categories"]]
    cat_values = [v for _, v in s["top5_categories"]]
    colors = ["#4A90E2", "#E74C3C", "#7CB342", "#F39C12", "#F4D03F"]
    bars2 = ax_cat.barh(range(len(cat_names)), cat_values,
                        color=colors[:len(cat_names)],
                        edgecolor="#333333", linewidth=0.6)
    ax_cat.invert_yaxis()
    for b, v in zip(bars2, cat_values):
        ax_cat.text(v + 1.5, b.get_y() + b.get_height() / 2,
                    f"{v:.1f}%", va="center", fontsize=11, fontweight="bold")
    ax_cat.set_yticks(range(len(cat_names)))
    ax_cat.set_yticklabels(cat_names, fontsize=10)
    ax_cat.set_xlabel("% of postings", fontsize=11, fontweight="bold")
    ax_cat.set_title("Hiring by Category\n(Top 5)",
                     fontsize=13, fontweight="bold")
    ax_cat.set_xlim(0, max(cat_values) * 1.18)
    ax_cat.grid(axis="x", alpha=0.3)

    # ==================================================================
    # Yellow box — Data quality & caveats
    # ==================================================================
    ax_dq = fig.add_axes([0.05, 0.04, 0.26, 0.28])
    draw_box(ax_dq, "#FCF3CF", "#C9B458", rounding=0.05)
    ax_dq.text(0.04, 0.93, "DATA QUALITY & CAVEATS:",
               fontsize=12, fontweight="bold", va="top")
    ax_dq.text(0.05, 0.76,
               "⚠  209 postings from 5 Kaggle\n"
               "     snapshots (not census)\n\n"
               "⚠  Feb 2026 has 58% of data\n"
               "     (artifact, not signal)\n\n"
               "⚠  63% are duplicates\n"
               "     (true unique count ≈ 112)\n\n"
               "⚠  Kaggle filters for 'AI jobs'\n"
               "     (selection bias)",
               fontsize=10.5, va="top")

    # ==================================================================
    # Green box — Strategic implications
    # ==================================================================
    ax_strat = fig.add_axes([0.37, 0.04, 0.58, 0.28])
    draw_box(ax_strat, "#E4F1DF", "#7BA86E", rounding=0.04)
    ax_strat.text(0.03, 0.94, "STRATEGIC IMPLICATIONS:",
                  fontsize=12, fontweight="bold", va="top")
    ax_strat.text(0.03, 0.79,
                  "✓  WHAT META IS BETTING ON:\n"
                  "      •  Researcher-driven culture: Hire top AI researchers, "
                  "they drive innovation + product\n"
                  "      •  Python + existing infra is enough: Accept technical debt "
                  "in non-AI systems\n"
                  "      •  AI research is defensible advantage: Allocate 84% of "
                  "hiring to research, minimize infrastructure\n",
                  fontsize=10, va="top")
    ax_strat.text(0.03, 0.53,
                  "✓  RISKS IF THIS BET FAILS:\n"
                  "      •  Infrastructure debt accumulates → Performance/reliability "
                  "crises → Hiring firefighters (expensive)\n"
                  "      •  Researcher productivity drops → Project delays → Hiring "
                  "slowdown to save cost\n"
                  "      •  AI market commoditizes → Research hires become less "
                  "valuable → Excess payroll\n",
                  fontsize=10, va="top")
    ax_strat.text(0.03, 0.26,
                  "✓  COMPETITIVE POSITION:\n"
                  "      •  Similar to: Google, Anthropic (if they also hire 80%+ AI research)\n"
                  "      •  Unlike: NVIDIA (hardware), AWS/Azure (cloud/platform), "
                  "traditional Big Tech (polyglot hiring)",
                  fontsize=10, va="top")

    fig.savefig(outpath, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    args = parse_args()
    args = resolve_inputs(args)

    print(f"Reading tiers:    {args.tiers}")
    print(f"Reading category: {args.category}")

    tiers_df = pd.read_csv(args.tiers)
    cats_df  = pd.read_csv(args.category)

    stats = compute_stats(tiers_df, cats_df)

    # Sanity print
    print("Computed stats:")
    print(f"  research_share  = {stats['research_share']:.1f}%")
    print(f"  cloud_share     = {stats['cloud_share']:.1f}%")
    print(f"  data_eng_share  = {stats['data_eng_share']:.1f}%")
    print(f"  python_share    = {stats['python_share']:.1f}%")
    print(f"  top-5 skills:   {[n for n, _ in stats['top5_skills']]}")

    png_path = args.outdir / f"meta_insight_executive_summary_{args.stamp}.png"
    build_infographic(stats, png_path)
    print(f"\n✅ {png_path.name}")

    # Verify the (hand-written) insight report sits next to the PNG
    report = args.outdir / f"meta_insight_report_{args.stamp}.md"
    if report.exists():
        print(f"✅ Report present: {report.name}")
    else:
        print(f"⚠  Report not found at {report} — expected to be hand-written.")


if __name__ == "__main__":
    main()
