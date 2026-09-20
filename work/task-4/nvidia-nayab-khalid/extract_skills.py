#!/usr/bin/env python3
"""Task 4 skill extraction and feature engineering - NVIDIA job postings.

Input :  work/task-3/nvidia-nayab-khalid/data/processed/nvidia_postings_clean_<stamp>.csv
         shared/taxonomy/skills.yaml          (ALIGNMENT LOCK #2 - the shared taxonomy)
Output:  data/features/nvidia_skills_long_<stamp>.csv        the extracted-skills dataset
         data/features/nvidia_skill_features_<stamp>.csv     per-skill feature table
         data/features/nvidia_skill_by_week_<stamp>.csv      skill x observation week
         data/features/taxonomy_candidates_<stamp>.csv       unmatched terms, for the team

Method
------
Dictionary matching of the shared taxonomy against the cleaned title text, with three rules that
exist because the input is a job title rather than a job description:

1. Longest alias wins. "computer vision" must not also register as a separate "vision" hit, and
   "gpu architecture" must not double-count as "gpu". Aliases are sorted by length and a matched
   span is consumed so no shorter term can claim it.

2. Blocked single letters. The taxonomy's `title_match_blocklist` holds terms that are real skills
   in a description but false positives in a title: "r" matches "R&D" once punctuation is
   stripped, and "c" matches the c inside "c++". Both were measured, not assumed.

3. No inference. If a title says "Senior Software Engineer" and nothing else, it gets no skill.
   Guessing that a software engineer at NVIDIA "probably knows C++" would manufacture data.

Everything matched maps to a canonical taxonomy name, so the four companies stay comparable. Terms
that appear often but match nothing are written to the candidates file for the team's taxonomy
review rather than being invented locally.

Usage:  python extract_skills.py [--in <clean csv>] [--taxonomy <yaml>] [--out-dir data/features]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from skill_matcher import build_matchers, extract, load_taxonomy   # noqa: E402

# Words that are roles, not skills. role_function already captures these (Task 3), and letting
# them into the skill space would make every posting look identical.
ROLE_WORDS = {
    "engineer", "engineering", "manager", "architect", "director", "developer", "scientist",
    "researcher", "analyst", "specialist", "lead", "leader", "intern", "designer", "consultant",
    "administrator", "assistant", "planner", "buyer", "auditor", "reviewer", "generalist",
    "technician", "counsel", "recruiter", "accountant", "senior", "principal", "staff", "junior",
}
# Generic nouns that carry no technical signal on their own.
GENERIC_WORDS = {
    "new", "college", "grad", "graduate", "team", "global", "regional", "technical", "technology",
    "solution", "solutions", "service", "services", "product", "products", "program", "programs",
    "project", "projects", "business", "customer", "account", "partner", "partners", "sales",
    "marketing", "operation", "operations", "development", "relations", "experience", "platform",
    "platforms", "system", "systems", "software", "hardware", "data", "center", "core", "advanced",
    "applied", "field", "group", "internal", "external", "support", "management", "strategy",
    "planning", "quality", "process", "design", "research", "science", "tools", "tool", "stack",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=None)
    ap.add_argument("--taxonomy", default="../../../shared/taxonomy/skills.yaml")
    ap.add_argument("--out-dir", default="data/features")
    args = ap.parse_args()

    if args.src:
        src = Path(args.src)
    else:
        found = sorted(Path("../../task-3/nvidia-nayab-khalid/data/processed").glob(
            "nvidia_postings_clean_*.csv"))
        if not found:
            print("ERROR  no cleaned dataset found; pass --in")
            return 1
        src = found[-1]
    stamp = re.search(r"(\d{8})", src.name).group(1)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"1. reading {src}")
    df = pd.read_csv(src)
    tax = load_taxonomy(args.taxonomy)
    entries, blocked = build_matchers(tax)
    print(f"   {len(df)} postings | {len(tax['skills'])} canonical skills, "
          f"{len(entries)} alias patterns | blocklist: {sorted(blocked)}")

    print("2. matching the taxonomy against cleaned titles")
    rows = []
    per_posting = []
    for jid, text, week, sen, fun, status in zip(
            df.job_id, df.cleaned_description.astype(str).str.lower(), df.posting_date,
            df.seniority_derived, df.role_function, df.job_status):
        hits = extract(text, entries)
        per_posting.append(len(hits))
        for name, category, term in hits:
            rows.append({"job_id": jid, "skill": name, "skill_category": category,
                         "matched_term": term, "posting_date": week,
                         "seniority_level": sen, "role_function": fun, "job_status": status})
    long = pd.DataFrame(rows)
    df["n_skills"] = per_posting
    covered = int((df.n_skills > 0).sum())
    print(f"   {len(long)} skill mentions | {covered} of {len(df)} postings matched "
          f"({covered / len(df) * 100:.1f}%) | mean {df.n_skills.mean():.2f} per posting")

    long_path = out_dir / f"nvidia_skills_long_{stamp}.csv"
    long.to_csv(long_path, index=False, encoding="utf-8")
    print(f"   wrote {long_path}")

    # ---------------------------------------------------------------- per-skill features
    print("3. building the per-skill feature table")
    # The first observation is left-censored: every posting already open on that date is stamped
    # with it, 395 of 1,745 (23%). Leaving it in loads the first half and makes almost everything
    # look like it is declining. It is excluded from the trend comparison, and only from that.
    weeks = sorted(df.posting_date.dropna().unique())
    censored_week = weeks[0]
    trend_weeks = weeks[1:]
    midpoint = trend_weeks[len(trend_weeks) // 2]
    in_trend = df.posting_date.isin(trend_weeks)
    long_trend = long[long.posting_date.isin(trend_weeks)]
    first_half = long_trend[long_trend.posting_date < midpoint]
    second_half = long_trend[long_trend.posting_date >= midpoint]
    n_first = max(int((in_trend & (df.posting_date < midpoint)).sum()), 1)
    n_second = max(int((in_trend & (df.posting_date >= midpoint)).sum()), 1)
    print(f"   trend basis excludes the left-censored week {censored_week} "
          f"({int((df.posting_date == censored_week).sum())} postings); "
          f"{n_first} vs {n_second} postings compared")

    feats = []
    for skill, grp in long.groupby("skill"):
        early = int((first_half.skill == skill).sum())
        late = int((second_half.skill == skill).sum())
        early_rate, late_rate = early / n_first, late / n_second
        feats.append({
            "skill": skill,
            "skill_category": grp.skill_category.iloc[0],
            "postings": len(grp),
            "share_of_postings": round(len(grp) / len(df), 4),
            "first_seen": grp.posting_date.min(),
            "last_seen": grp.posting_date.max(),
            "weeks_present": grp.posting_date.nunique(),
            "top_role_function": grp.role_function.mode().iloc[0] if len(grp) else "",
            "senior_share": round((grp.seniority_level.isin(
                ["Senior", "Principal", "Distinguished", "Director", "Executive", "Staff"])
            ).mean(), 3),
            "postings_first_half": early,
            "postings_second_half": late,
            "rate_change": round(late_rate - early_rate, 4),
            "emerging_skill_flag": bool(late_rate > early_rate * 1.5 and late >= 5),
        })
    features = pd.DataFrame(feats).sort_values("postings", ascending=False)
    features["rank"] = range(1, len(features) + 1)
    fpath = out_dir / f"nvidia_skill_features_{stamp}.csv"
    features.to_csv(fpath, index=False, encoding="utf-8")
    print(f"   wrote {fpath}  ({len(features)} skills)")

    # ---------------------------------------------------------------- skill x week
    print("4. building the skill-by-week table")
    by_week = (long.groupby(["skill", "posting_date"]).size()
               .rename("postings").reset_index()
               .pivot(index="skill", columns="posting_date", values="postings")
               .fillna(0).astype(int))
    wpath = out_dir / f"nvidia_skill_by_week_{stamp}.csv"
    by_week.to_csv(wpath, encoding="utf-8")
    print(f"   wrote {wpath}  ({by_week.shape[0]} skills x {by_week.shape[1]} weeks)")

    # ---------------------------------------------------------------- candidates
    print("5. collecting candidate terms for the team taxonomy review")
    matched_words = {w for term in long.matched_term.astype(str) for w in term.split()}
    freq = Counter()
    for toks in df.title_tokens.map(json.loads):
        for t in toks:
            if t in matched_words or t in ROLE_WORDS or t in GENERIC_WORDS or len(t) < 3:
                continue
            freq[t] += 1
    cand = pd.DataFrame(freq.most_common(), columns=["term", "postings"])
    cand["share_of_postings"] = (cand.postings / len(df)).round(4)
    cand = cand[cand.postings >= 3]
    cpath = out_dir / f"taxonomy_candidates_{stamp}.csv"
    cand.to_csv(cpath, index=False, encoding="utf-8")
    print(f"   wrote {cpath}  ({len(cand)} candidate terms seen 3+ times)")

    # ---------------------------------------------------------------- summary
    print("\n--- summary for the method note ---")
    print(f"postings                    {len(df)}")
    print(f"postings with >=1 skill     {covered} ({covered / len(df) * 100:.1f}%)")
    print(f"skill mentions              {len(long)}")
    print(f"mean skills per posting     {df.n_skills.mean():.2f}")
    print(f"distinct skills matched     {long.skill.nunique()} of {len(tax['skills'])} in taxonomy")
    print(f"\nby category:\n{long.skill_category.value_counts().to_string()}")
    print(f"\ntop 20 skills:\n"
          f"{features.head(20)[['skill','skill_category','postings','share_of_postings']].to_string(index=False)}")
    em = features[features.emerging_skill_flag]
    print(f"\nemerging skills ({len(em)}):\n"
          f"{em[['skill','postings_first_half','postings_second_half','rate_change']].to_string(index=False)}")
    print(f"\ntop 15 unmatched candidate terms:\n{cand.head(15).to_string(index=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
