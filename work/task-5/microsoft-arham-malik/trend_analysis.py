#!/usr/bin/env python3
"""Task 5 - hiring trend analysis, Microsoft.

The Microsoft source has no posting_date. Two bases are produced, and they are
not equal in standing.

BASIS 1 - ORDINAL COHORTS (real, and the basis for every claim).
Microsoft issues requisition IDs sequentially, so a higher source_job_id was
opened later than a lower one. Postings are ordered by it and split into four
equal cohorts. This supports "skill X rose across cohorts". It does not
support velocity or seasonality, because no elapsed time is known: the four
cohorts could span four months or four years.

BASIS 2 - SIMULATED CALENDAR (synthetic, methodology demonstration only).
Google's Task 3 seeds a reproducible synthetic posting_date for all 1,127 of
its rows and flags it with posting_date_is_simulated, then demonstrates
monthly velocity and seasonality on it. That precedent is followed here so the
Microsoft deliverable has the same shape, and it carries the same warning:
every number on this basis describes the simulation, not Microsoft.

Where the two disagree, Basis 1 wins. Basis 2 exists so the velocity and
forecasting machinery is built and reviewable, not to make a claim.

THE CONFOUND THAT CHANGED THE HEADLINE
A first pass found Program Management rising 17 points across cohorts. It was
composition, not strategy: the oldest cohort is 78% Software Engineering with
2% Program Management, the newest 59% and 17%. Holding role family constant
removes it. The controlled table is the one to read.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
SRC = HERE / ".." / ".." / "task-4" / "microsoft-arham-malik" / "data" / "features" / "microsoft_skill_features_20261026.csv"
OUT = HERE / "data"
FIG = HERE / "figures"
STAMP = "20261026"
N_COHORTS = 4
SEED = 20261026          # fixed so the synthetic calendar is reproducible
MIN_PCT = 10             # reporting floor; ~45 postings per cohort


def load():
    df = pd.read_csv(SRC, keep_default_na=False)
    df["source_job_id"] = df["source_job_id"].astype(int)
    return df.sort_values("source_job_id").reset_index(drop=True)


def skill_set(v):
    import json
    try:
        return set(json.loads(v))
    except Exception:
        return set()


def cohort_trends(df, labels, universe, subset=None, min_hits=0):
    d = df if subset is None else subset
    rows = []
    for sk in universe:
        has = d["extracted_skills"].apply(lambda v: sk in skill_set(v))
        if has.sum() < min_hits:
            continue
        rec = {"skill": sk}
        for name in labels.values():
            m = d["cohort"] == name
            rec[name] = round(has[m].sum() / m.sum() * 100, 1) if m.sum() else 0.0
        rec["change"] = round(rec["C4 newest"] - rec["C1 oldest"], 1)
        rec["overall_pct"] = round(has.sum() / len(d) * 100, 1)
        rows.append(rec)
    return pd.DataFrame(rows).sort_values("change", ascending=False)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)
    df = load()
    labels = {0: "C1 oldest", 1: "C2", 2: "C3", 3: "C4 newest"}

    # rank-based cut: ID gaps run from 191 to 46,037, so cutting on value
    # would give cohorts of 2 and 150
    df["cohort"] = pd.qcut(df["source_job_id"].rank(method="first"),
                           N_COHORTS, labels=False).map(labels)

    universe = sorted({s for v in df["extracted_skills"] for s in skill_set(v)})
    print(f"{len(df)} postings | {len(universe)} distinct skills")

    # ---- BASIS 1a: raw cohort trends (confounded, kept for transparency) --
    raw = cohort_trends(df, labels, universe)
    raw = raw[raw["overall_pct"] >= MIN_PCT]
    raw.to_csv(OUT / f"microsoft_cohort_trends_raw_{STAMP}.csv", index=False)

    # ---- the confound check ----------------------------------------------
    mix = pd.crosstab(df["cohort"], df["job_family_subcategory"],
                      normalize="index").mul(100).round(1)
    mix.to_csv(OUT / f"microsoft_cohort_role_mix_{STAMP}.csv")
    swe_spread = mix["Software Engineering"].max() - mix["Software Engineering"].min()
    print(f"\nconfound check: Software Engineering share spans "
          f"{mix['Software Engineering'].min():.1f}-{mix['Software Engineering'].max():.1f}% "
          f"({swe_spread:.1f} pts) across cohorts")
    if swe_spread > 10:
        print("  cohorts differ in role composition -> raw trends are confounded")

    # ---- BASIS 1b: controlled, Software Engineering only ------------------
    swe = df[df["job_family_subcategory"] == "Software Engineering"]
    ctrl = cohort_trends(df, labels, universe, subset=swe, min_hits=8)
    ctrl.to_csv(OUT / f"microsoft_cohort_trends_swe_{STAMP}.csv", index=False)
    print(f"\ncontrolled (Software Engineering, n={len(swe)}, per cohort "
          f"{swe.groupby('cohort').size().tolist()}):")
    print(ctrl.head(6)[["skill", "C1 oldest", "C4 newest", "change"]].to_string(index=False))
    print("  ...")
    print(ctrl.tail(4)[["skill", "C1 oldest", "C4 newest", "change"]].to_string(index=False))

    # ---- BASIS 2: simulated calendar -------------------------------------
    # Seeded and reproducible. Dates are assigned in requisition-ID order so
    # the synthetic calendar at least preserves the real ordering; the spacing
    # between them is invented.
    rng = np.random.default_rng(SEED)
    start, end = pd.Timestamp("2024-01-01"), pd.Timestamp("2025-12-31")
    span = (end - start).days
    offs = np.sort(rng.integers(0, span, len(df)))
    sim = df.copy()
    sim["posting_date"] = [start + pd.Timedelta(days=int(o)) for o in offs]
    sim["posting_date_is_simulated"] = True
    sim["posting_month"] = sim["posting_date"].dt.to_period("M").astype(str)
    sim["posting_week"] = sim["posting_date"].dt.strftime("%G-W%V")
    sim[["job_id", "source_job_id", "posting_date", "posting_date_is_simulated",
         "posting_month", "posting_week", "cohort"]].to_csv(
        OUT / f"microsoft_simulated_calendar_{STAMP}.csv", index=False)

    monthly = (sim.groupby("posting_month").size()
                 .rename("postings").reset_index())
    monthly["rolling_3mo_avg"] = monthly["postings"].rolling(3).mean().round(2)
    monthly["mom_growth_pct"] = (monthly["postings"].pct_change() * 100).round(1)
    monthly.to_csv(OUT / f"microsoft_monthly_postings_SIMULATED_{STAMP}.csv",
                   index=False)
    print(f"\nBasis 2 (SIMULATED): {len(monthly)} months, "
          f"mean {monthly['postings'].mean():.1f} postings/month")
    print("  these numbers describe the simulation, not Microsoft")

    # ---- figure -----------------------------------------------------------
    top = ctrl.reindex(ctrl["change"].abs().sort_values(ascending=False).index).head(8)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5))
    for _, r in top.iterrows():
        a1.plot(range(N_COHORTS), [r[c] for c in labels.values()],
                marker="o", linewidth=1.8, label=r["skill"])
    a1.set_xticks(range(N_COHORTS)); a1.set_xticklabels(labels.values())
    a1.set_ylabel("% of Software Engineering postings in cohort")
    a1.set_title("Basis 1 (REAL): skill share by requisition-ID cohort\n"
                 "role family held constant", fontsize=10)
    a1.legend(fontsize=7, ncol=2); a1.grid(alpha=.3)

    a2.plot(monthly["posting_month"], monthly["postings"], marker="o",
            linewidth=1.5, color="#999999", label="postings")
    a2.plot(monthly["posting_month"], monthly["rolling_3mo_avg"],
            linewidth=2.2, color="#B71C1C", label="3-month rolling")
    a2.set_xticks(range(0, len(monthly), 3))
    a2.set_xticklabels(monthly["posting_month"][::3], rotation=45, ha="right", fontsize=7)
    a2.set_title("Basis 2 (SIMULATED DATES): monthly velocity\n"
                 "methodology demonstration - not real Microsoft activity",
                 fontsize=10, color="#B71C1C")
    a2.legend(fontsize=8); a2.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(FIG / "microsoft_trend_dual_basis.png", dpi=140, bbox_inches="tight")
    print(f"\nwritten to {OUT} and {FIG}")


if __name__ == "__main__":
    main()
