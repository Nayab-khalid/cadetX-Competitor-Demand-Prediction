#!/usr/bin/env python3
"""Task 4 - skill extraction and feature engineering, Microsoft.

Uses scripts/skill_matcher.py and shared/taxonomy/skills.yaml. No local skill
list: the task README forbids one, and a four-way comparison where two members
matched with different code is a comparison of implementations.

Outputs (data/features/):
    microsoft_skills_long_20261026.csv       one row per posting-skill hit
    microsoft_skill_features_20261026.csv    one row per posting, wide
    microsoft_skill_frequency_20261026.csv   corpus totals
    taxonomy_candidates_20261026.csv         frequent terms matching nothing
    basis_comparison_20261026.csv            titles vs full text
    drive_false_positive_evidence_20261026.csv

TWO BASES, following the convention Nayab set in Task 6:
  Basis A, titles only  - every company has titles, so this is like-for-like
                          and is what any cross-company claim must use.
  Basis B, full text    - richer, but NVIDIA has no description text, so it
                          cannot carry a four-way comparison.

A DEFECT FOUND IN THE SHARED TAXONOMY
`Autonomous Vehicles` lists "drive" and "av" as aliases. "drive" matches the
ordinary verb, in phrases such as "drive features to closure". Measured:

    Microsoft  74/182 postings (40.7%) falsely tagged
    Meta       70/209 postings (33.5%) falsely tagged

Google reads 0% only because its Task 6 run matched on titles; the error is
latent there, not absent. This script reports BOTH numbers - as the taxonomy
currently stands, so figures are comparable with teammates' existing work, and
with the alias suppressed, so the size of the error is visible. The fix needs
a PR and two approvals per CONTRIBUTING.md; it is proposed separately, not
applied here unilaterally.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
ROOT = HERE / ".." / ".." / ".."          # repo root
sys.path.insert(0, str((ROOT / "scripts").resolve()))
from skill_matcher import load_taxonomy, build_matchers, extract  # noqa: E402

SRC = HERE / ".." / ".." / "task-3" / "microsoft-arham-malik" / "data" / "microsoft_postings_clean_20261026.csv"
TAX = ROOT / "shared" / "taxonomy" / "skills.yaml"
OUT = HERE / "data" / "features"
STAMP = "20261026"
COMPANY = "Microsoft"

# Alias known to produce false positives; see the module docstring.
SUPPRESS = {("Autonomous Vehicles", "drive"), ("Autonomous Vehicles", "av")}


def hits(text, entries, suppress=False):
    """Lowercase BEFORE matching.

    build_matchers() compiles each pattern from term.lower() with no re.I
    flag, so the patterns are case-sensitive and Title Case input matches
    nothing. A first run here passed case-preserved text and produced 0.0%
    title coverage for Microsoft, which looked like a finding about generic
    Microsoft job titles and was in fact this bug. NVIDIA's Task 4 calls
    .str.lower() for the same reason.
    """
    out = []
    for skill, category, term in extract(str(text).lower(), entries):
        if suppress and (skill, term.lower()) in SUPPRESS:
            continue
        out.append((skill, category, term))
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SRC, keep_default_na=False)
    tax = load_taxonomy(TAX)
    entries, blocked = build_matchers(tax)
    canonical = {s["name"] for s in tax["skills"]}
    print(f"{len(df)} postings | taxonomy {len(canonical)} skills | "
          f"title blocklist {sorted(blocked)}")

    # ---- long form, both bases ------------------------------------------
    rows = []
    for _, r in df.iterrows():
        for basis, col in [("titles", "job_title"), ("fulltext", "clean_text")]:
            for skill, cat, term in hits(r[col], entries, suppress=True):
                rows.append({"job_id": r["job_id"], "company_name": COMPANY,
                             "basis": basis, "skill": skill,
                             "skill_category": cat, "matched_term": term})
    long = pd.DataFrame(rows).drop_duplicates()
    long.to_csv(OUT / f"microsoft_skills_long_{STAMP}.csv", index=False)

    # ---- wide features, full text, corrected -----------------------------
    per = {r["job_id"]: hits(r["clean_text"], entries, suppress=True)
           for _, r in df.iterrows()}
    feat = df.copy()
    feat["extracted_skills"] = feat["job_id"].map(
        lambda j: json.dumps(sorted({s for s, _, _ in per[j]})))
    feat["skill_categories"] = feat["job_id"].map(
        lambda j: json.dumps(sorted({c for _, c, _ in per[j]})))
    feat["skill_count"] = feat["job_id"].map(lambda j: len({s for s, _, _ in per[j]}))
    tech_cats = {"languages", "ml_frameworks", "data_engineering", "cloud_infra",
                 "hardware_systems", "silicon_design"}
    feat["tech_stack_tags"] = feat["job_id"].map(
        lambda j: json.dumps(sorted({s for s, c, _ in per[j] if c in tech_cats})))
    for cat in sorted({s["category"] for s in tax["skills"]}):
        feat[f"cat_{cat}"] = feat["job_id"].map(
            lambda j, c=cat: sum(1 for _, cc, _ in per[j] if cc == c))
    feat.to_csv(OUT / f"microsoft_skill_features_{STAMP}.csv", index=False)

    # ---- frequency --------------------------------------------------------
    cnt = Counter(s for j in per for s, _, _ in set(per[j]))
    cat_of = {s["name"]: s["category"] for s in tax["skills"]}
    freq = (pd.DataFrame([(s, cat_of.get(s, ""), n, round(n / len(df) * 100, 1))
                          for s, n in cnt.items()],
                         columns=["skill", "category", "postings", "pct_of_postings"])
            .sort_values("postings", ascending=False))
    freq.to_csv(OUT / f"microsoft_skill_frequency_{STAMP}.csv", index=False)

    # ---- basis comparison -------------------------------------------------
    def basis_stats(col, suppress):
        tot = cov = 0
        for t in df[col]:
            h = {s for s, _, _ in hits(t, entries, suppress=suppress)}
            tot += len(h)
            cov += bool(h)
        return round(tot / len(df), 2), round(cov / len(df) * 100, 1)

    bc = []
    for basis, col in [("titles", "job_title"), ("fulltext", "clean_text")]:
        for label, sup in [("as_taxonomy_stands", False), ("drive_alias_suppressed", True)]:
            spp, cov = basis_stats(col, sup)
            bc.append({"company": COMPANY, "basis": basis, "variant": label,
                       "skills_per_posting": spp, "coverage_pct": cov})
    bcdf = pd.DataFrame(bc)
    bcdf.to_csv(OUT / f"basis_comparison_{STAMP}.csv", index=False)
    print("\nBasis comparison:")
    print(bcdf.to_string(index=False))

    # ---- evidence for the taxonomy PR -------------------------------------
    ev = []
    for _, r in df.iterrows():
        for skill, cat, term in hits(r["clean_text"], entries, suppress=False):
            if (skill, term.lower()) in SUPPRESS:
                txt = str(r["clean_text"])
                i = txt.lower().find(term.lower())
                ev.append({"job_id": r["job_id"], "job_title": r["job_title"],
                           "skill": skill, "matched_term": term,
                           "context": txt[max(0, i - 60):i + 40].replace("\n", " ")})
                break
    evdf = pd.DataFrame(ev)
    evdf.to_csv(OUT / f"drive_false_positive_evidence_{STAMP}.csv", index=False)
    print(f"\n'drive' false positives: {len(evdf)}/{len(df)} postings "
          f"({len(evdf)/len(df)*100:.1f}%)")

    # ---- taxonomy candidates ---------------------------------------------
    known = {t.lower() for s in tax["skills"]
             for t in [s["name"]] + list(s.get("aliases") or [])}
    terms = Counter()
    for t in df["token_text"]:
        for w in set(str(t).split()):
            if w not in known and len(w) > 3:
                terms[w] += 1
    cand = [(w, n, round(n / len(df) * 100, 1)) for w, n in terms.most_common(400)
            if n >= 18]
    pd.DataFrame(cand, columns=["term", "postings", "pct_of_postings"]).to_csv(
        OUT / f"taxonomy_candidates_{STAMP}.csv", index=False)

    print(f"\nTop skills (full text, corrected):")
    print(freq.head(12).to_string(index=False))
    print(f"\ncandidates for team review: {len(cand)}")


if __name__ == "__main__":
    main()
