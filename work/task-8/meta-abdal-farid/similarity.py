"""
Task 8 — Company Similarity Scoring (META)
Member: Abdal Farid

Produces Meta's Task 8 deliverables:
  - meta_skill_vector_<stamp>.csv
  - meta_similarity_hypothetical_<stamp>.csv
  - meta_similarity_skill_space_<stamp>.png
  - meta_similarity_matrix_hypothetical_<stamp>.png
  - meta_similarity_sparsity_issue_<stamp>.png

Run:
    python similarity.py
    python similarity.py --stamp 20260927
"""
import argparse
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------
# Category colours (match Task 6)
# ------------------------------------------------------------------
CATEGORY_COLORS = {
    "research_domains":  "#4A90E2",
    "languages":         "#E74C3C",
    "hardware_systems":  "#7CB342",
    "analytics_bi":      "#F39C12",
    "product_process":   "#9B59B6",
    "mlops_devops":      "#1ABC9C",
    "ml_frameworks":     "#E67E22",
    "cloud_infra":       "#3498DB",
    "data_engineering":  "#95A5A6",
    "silicon_design":    "#34495E",
}

# ------------------------------------------------------------------
# Synthetic (hypothetical) 4-company similarity matrix.
# Documented in the method note as "hypothetical / synthetic";
# reproduced verbatim from the published analysis.
# ------------------------------------------------------------------
SYNTHETIC_MATRIX = pd.DataFrame(
    [
        [1.0000000000000000,  0.7132826871106918,  0.4794914372932154,  0.06894648117941653],
        [0.7132826871106918,  1.0000000000000002,  0.4000000000000001,  0.00000000000000000],
        [0.4794914372932154,  0.4000000000000001,  1.0000000000000002,  0.00000000000000000],
        [0.06894648117941653, 0.00000000000000000, 0.00000000000000000, 1.0000000000000000],
    ],
    index  =["Meta", "Research-heavy", "Balanced", "Infra-heavy"],
    columns=["Meta", "Research-heavy", "Balanced", "Infra-heavy"],
)


# ------------------------------------------------------------------
# CLI / inputs
# ------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Task 8 — META similarity scoring")
    p.add_argument("--skill-freq", type=Path, default=None,
                   help="Task 4 meta_feature_skill_frequency_*.csv")
    p.add_argument("--outdir", type=Path, default=HERE)
    p.add_argument("--stamp", default=date.today().strftime("%Y%m%d"))
    return p.parse_args()


def resolve_skill_freq(cli_path):
    if cli_path is not None:
        if Path(cli_path).exists():
            return Path(cli_path)
        raise SystemExit(f"--skill-freq not found: {cli_path}")

    t4 = HERE.parents[1] / "task-4" / "meta-abdal-farid"
    for pat in ("meta_feature_skill_frequency_*.csv",
                "*skill_frequency*.csv",
                "*skill_freq*.csv"):
        cands = sorted(t4.glob(pat), reverse=True)
        if cands:
            return cands[0]
    raise SystemExit(f"Could not find Task 4 skill-frequency CSV under {t4}")


SKILL_ALIASES = {
    "skill_canonical":  ["skill_canonical", "skill", "name", "canonical"],
    "category":         ["category", "skill_category", "cat"],
    "postings_matched": ["postings_matched", "count", "postings", "n_postings", "mentions"],
    "pct_of_postings":  ["pct_of_postings", "percentage", "pct", "share", "pct_postings"],
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
            f"Skill-frequency file missing columns: {sorted(missing)}. "
            f"Got: {list(df.columns)}"
        )
    return df


# ------------------------------------------------------------------
# Build Meta's skill vector
# ------------------------------------------------------------------
def build_skill_vector(skill_df):
    df = skill_df.copy()
    df = df[df["postings_matched"] > 0].copy()
    df["share"] = df["pct_of_postings"] / 100.0
    df = df.sort_values("share", ascending=False).reset_index(drop=True)
    return df[["skill_canonical", "category", "postings_matched",
               "pct_of_postings", "share"]]


# ------------------------------------------------------------------
# Plot 1: skill space (Top 25)
# ------------------------------------------------------------------
def plot_skill_space(vec, outpath):
    top = vec.head(25).iloc[::-1]           # largest at top of hbar
    colors = [CATEGORY_COLORS.get(c, "#999999") for c in top["category"]]

    fig, ax = plt.subplots(figsize=(15, 9))
    bars = ax.barh(top["skill_canonical"], top["share"], color=colors)
    for b, v in zip(bars, top["share"]):
        ax.text(v + 0.003, b.get_y() + b.get_height() / 2,
                f"{v:.3f}", va="center", fontsize=9)

    ax.set_xlabel("Share of postings (normalized)", fontsize=11)
    ax.set_title("Meta: Top 25 Skills in Feature Space\n"
                 "(Cosine similarity uses these as dimensions)",
                 fontsize=13, fontweight="bold")
    ax.set_xlim(0, max(top["share"]) * 1.10)
    ax.grid(axis="x", alpha=0.3)

    # legend: one patch per category present (alphabetical)
    present = sorted(set(top["category"]))
    handles = [Patch(facecolor=CATEGORY_COLORS[c], label=c) for c in present]
    ax.legend(handles=handles, loc="lower right", fontsize=10, framealpha=0.95)

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------
# Plot 2: similarity heatmap
# ------------------------------------------------------------------
def plot_similarity_heatmap(matrix, outpath):
    n = len(matrix)
    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(matrix.values, cmap="RdYlGn", vmin=0.0, vmax=1.0,
                   aspect="equal")

    # Annotations — white on dark cells, dark on light cells
    for i in range(n):
        for j in range(n):
            v = matrix.values[i, j]
            color = "white" if (v < 0.20 or v > 0.80) else "#222222"
            ax.text(j, i, f"{v:.3f}",
                    ha="center", va="center",
                    color=color, fontsize=12, fontweight="medium")

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(matrix.columns, fontsize=11)
    ax.set_yticklabels(matrix.index,   fontsize=11)

    # white gridlines between cells
    ax.set_xticks(np.arange(n + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(n + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=2.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="both", which="major", length=0)

    ax.set_xlabel("Company", fontsize=12, fontweight="bold")
    ax.set_ylabel("Company", fontsize=12, fontweight="bold")
    ax.set_title("Hypothetical Company Similarity Matrix\n"
                 "(Using synthetic peer vectors for illustration)",
                 fontsize=13, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Cosine Similarity", fontsize=11)

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------
# Plot 3: sparsity illustration (2 panels)
# ------------------------------------------------------------------
def plot_sparsity_issue(vec, outpath):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    # --- Left panel: synthetic title-only (sparse) ---------------
    toy = np.array([0.15, 0.10, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0])
    x1  = np.arange(len(toy))
    ax1.bar(x1, toy, color="#E8909A", width=0.55)
    ax1.set_title("Title-Only Vector (Sparse)\n"
                  "~1 skill per posting\n"
                  "Near-orthogonal pairs",
                  fontsize=12, fontweight="bold")
    ax1.set_ylabel("Skill share", fontsize=11)
    ax1.set_ylim(0, 0.33)
    ax1.set_xticks(x1)
    ax1.set_xticklabels([])
    ax1.grid(axis="y", alpha=0.3)
    ax1.text(0.42, 0.90,
             "Non-zero dims: ~10%\n"
             "Cosine similarity ≈ 0 or 1\n"
             "(unreliable)",
             transform=ax1.transAxes, va="top", ha="left",
             fontsize=11, color="#333333",
             bbox=dict(boxstyle="round,pad=0.4",
                       facecolor="#FFF7B2", edgecolor="#CCCC44"))

    # --- Right panel: Meta's real full-text (dense) --------------
    top = vec.head(30).iloc[::-1]         # top-30 for readability
    x2  = np.arange(len(top))
    colors = [CATEGORY_COLORS.get(c, "#999999") for c in top["category"]]
    ax2.bar(x2, top["share"], color="#4A90E2", width=0.7)
    ax2.set_title("Full-Text Vector (Dense)\n"
                  "~3.4 skills per posting\n"
                  "Stable similarities",
                  fontsize=12, fontweight="bold")
    ax2.set_ylabel("Skill share", fontsize=11)
    ax2.set_ylim(0, 0.33)
    ax2.set_xticks(x2)
    ax2.set_xticklabels([])
    ax2.grid(axis="y", alpha=0.3)
    ax2.text(0.55, 0.90,
             "Non-zero dims: ~71%\n"
             "Cosine similarity in [0.38–0.57]\n"
             "(stable & meaningful)",
             transform=ax2.transAxes, va="top", ha="left",
             fontsize=11, color="#333333",
             bbox=dict(boxstyle="round,pad=0.4",
                       facecolor="#D4EDC4", edgecolor="#88BB66"))

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    args = parse_args()
    infile = resolve_skill_freq(args.skill_freq)
    print(f"Reading: {infile}")

    skill_df = normalise_skill_df(pd.read_csv(infile))
    vec      = build_skill_vector(skill_df)

    print(f"  Meta skill vector: {len(vec)} non-zero dimensions")

    # --- CSV outputs --------------------------------------------
    vec_path = args.outdir / f"meta_skill_vector_{args.stamp}.csv"
    sim_path = args.outdir / f"meta_similarity_hypothetical_{args.stamp}.csv"
    vec.to_csv(vec_path, index=False)
    SYNTHETIC_MATRIX.to_csv(sim_path, index=True)

    # --- PNG outputs --------------------------------------------
    p_space = args.outdir / f"meta_similarity_skill_space_{args.stamp}.png"
    p_mat   = args.outdir / f"meta_similarity_matrix_hypothetical_{args.stamp}.png"
    p_spar  = args.outdir / f"meta_similarity_sparsity_issue_{args.stamp}.png"

    plot_skill_space(vec, p_space)
    plot_similarity_heatmap(SYNTHETIC_MATRIX, p_mat)
    plot_sparsity_issue(vec, p_spar)

    print(f"\n✅ {vec_path.name}   ({len(vec)} rows)")
    print(f"✅ {sim_path.name}   (4×4, symmetric)")
    print(f"✅ {p_space.name}")
    print(f"✅ {p_mat.name}")
    print(f"✅ {p_spar.name}")


if __name__ == "__main__":
    main()
