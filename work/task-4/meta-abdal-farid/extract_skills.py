"""
Task 4: Skill Extraction and Feature Engineering - Meta
Member: Abdal Farid

Extracts canonical skills (from shared/taxonomy/skills.yaml) out of job_title
and cleaned_description. Every extracted skill maps to a canonical name in
the taxonomy - nothing is invented locally. Terms that appear often but match
nothing are written to a candidates file for team review, not silently kept
or silently discarded.

Usage:
    python extract_skills.py <cleaned_csv> <taxonomy_yaml> <outdir>

Library versions:
    pandas 3.0.2, PyYAML 6.0.3, Python 3.12.3
"""

import sys
import re
import json
import yaml
import pandas as pd
from collections import Counter

# ---------------------------------------------------------------------------
# Taxonomy loading
# ---------------------------------------------------------------------------

def load_taxonomy(path):
    with open(path) as f:
        tax = yaml.safe_load(f)
    blocklist = set(t.lower() for t in tax.get("title_match_blocklist", []))
    skills = []
    for entry in tax["skills"]:
        name = entry["name"]
        category = entry["category"]
        aliases = entry.get("aliases", []) or []
        terms = [name] + list(aliases)
        skills.append({"name": name, "category": category, "terms": terms})
    return skills, blocklist


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------
# Every alias is compiled into a regex. Two boundary styles are used:
#
#  - Standard \b...\b for multi-character terms (safe: a real word boundary
#    either side is enough to avoid absorbing part of another word).
#  - A stricter whitespace-or-string-edge boundary for single-character
#    terms (currently only ever the case for the blocklisted "r" / "c"
#    canonical skills), because \b alone still matches the "c" inside
#    "c++" or the "r" inside "r&d" - punctuation counts as a boundary too.
#    This is the exact false-positive the shared taxonomy's
#    title_match_blocklist comment documents.
#
# Per the taxonomy rule, blocklisted skills are never matched against
# job_title at all, regardless of boundary style. The strict boundary above
# is an extra safeguard applied to job_description too, since the same
# substring risk exists there and was not restricted to titles.

# A small number of aliases need a negative-context check beyond a plain word-boundary
# match. This is matching *logic*, not a taxonomy change - the alias itself stays in
# shared/taxonomy/skills.yaml; this only tells the matcher when NOT to count a hit.
# Found during Task 4 hand validation (Abdal Farid / Meta, 2026-09-26):
#   "network" (Networking) matched 8 times; 3 were "neural network" (an ML term, not
#   infra/networking) and 5 were genuine (tcp/ip, compute/network/storage, "network
#   engineer"). Removing the alias entirely would have thrown away the 5 real hits, so
#   only the specific "neural network" bigram is excluded here.
NEGATIVE_CONTEXT = {
    ("Networking", "network"): [re.compile(r"neural\s+network")],
}


def has_excluded_context(skill_name, term, text, match_start):
    key = (skill_name, term.lower())
    if key not in NEGATIVE_CONTEXT:
        return False
    window = text[max(0, match_start - 15):match_start + len(term) + 5]
    return any(p.search(window) for p in NEGATIVE_CONTEXT[key])


def compile_term(term):
    escaped = re.escape(term.lower())
    if len(term) == 1:
        # strict: only whitespace or string start/end either side
        pattern = r"(?:(?<=^)|(?<=\s))" + escaped + r"(?:(?=\s)|(?=$))"
    else:
        pattern = r"\b" + escaped + r"\b"
    return re.compile(pattern)


def build_matchers(skills):
    matchers = []
    for skill in skills:
        for term in skill["terms"]:
            matchers.append({
                "name": skill["name"],
                "category": skill["category"],
                "term": term,
                "regex": compile_term(term),
                "is_short": len(term) == 1,
            })
    return matchers


def normalise_text(text):
    if pd.isna(text):
        return ""
    return str(text).lower()


def extract_for_row(title, description, matchers, blocklist):
    title_n = normalise_text(title)
    desc_n = normalise_text(description)

    hits = []  # (canonical_name, category, matched_term, matched_field)
    matched_names = set()

    for m in matchers:
        skill_key = m["name"].lower()
        # never match blocklisted skills from title at all
        if skill_key not in blocklist:
            title_match = m["regex"].search(title_n)
            if title_match and not has_excluded_context(m["name"], m["term"], title_n, title_match.start()):
                hits.append((m["name"], m["category"], m["term"], "title"))
                matched_names.add(m["name"])
        desc_match = m["regex"].search(desc_n)
        if desc_match and m["name"] not in matched_names:
            if not has_excluded_context(m["name"], m["term"], desc_n, desc_match.start()):
                hits.append((m["name"], m["category"], m["term"], "description"))
                matched_names.add(m["name"])

    return hits


# ---------------------------------------------------------------------------
# Candidate term mining (frequent-but-unmatched terms for team review)
# ---------------------------------------------------------------------------

STOPWORDS = set("""
the a an and or of to in for with on at from by is are be will you your our
we team this that as it its into across including experience years work
working role join build building strong new most one more also who what
skills ability etc opportunity part
meta product data people help teams research beyond technical business risk
like qualifications systems connect experiences development screens
facebook technology technologies reality products world instagram
cross-functional around understanding businesses billions future their
operations other user language program computer minimum around them they
company companies employees global candidates candidate position positions
apply application applicants employment equal without regard status
benefits compensation base salary bonus equity total pay
looking seeking join us today tomorrow every day everyday
family applications world's largest across all app growth
""".split())

# role_function words are explicitly excluded per the task rule
# ("Role words are not skills.")
ROLE_WORDS = set("""
engineer engineering manager management architect architecture director lead
leadership scientist analyst specialist consultant intern associate senior
staff principal head vp president officer coordinator administrator
""".split())


def mine_candidates(df, matchers, blocklist, top_n=60):
    all_matched_terms = set()
    for m in matchers:
        all_matched_terms.add(m["term"].lower())

    counter = Counter()
    contexts = {}

    for _, row in df.iterrows():
        text = normalise_text(row["job_title"]) + " " + normalise_text(row["cleaned_description"])
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+/\-]{2,}", text)
        # unigrams and bigrams
        grams = list(tokens)
        grams += [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)]
        for g in grams:
            g_clean = g.strip()
            if g_clean in all_matched_terms:
                continue
            words = g_clean.split()
            if any(w in STOPWORDS or w in ROLE_WORDS for w in words):
                continue
            if len(g_clean) < 3:
                continue
            counter[g_clean] += 1
            if g_clean not in contexts:
                contexts[g_clean] = row["job_id"]

    candidates = counter.most_common(top_n)
    rows = [{"candidate_term": term, "frequency": freq, "example_job_id": contexts[term]}
            for term, freq in candidates]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(cleaned_csv, taxonomy_yaml, outdir):
    df = pd.read_csv(cleaned_csv)
    skills, blocklist = load_taxonomy(taxonomy_yaml)
    matchers = build_matchers(skills)

    long_rows = []
    per_posting_counts = []

    for _, row in df.iterrows():
        hits = extract_for_row(row["job_title"], row["cleaned_description"], matchers, blocklist)
        for name, category, term, field in hits:
            long_rows.append({
                "job_id": row["job_id"],
                "company_name": row["company_name"],
                "skill_canonical": name,
                "category": category,
                "matched_term": term,
                "matched_field": field,
                "posting_month": row.get("posting_month"),
            })
        per_posting_counts.append({
            "job_id": row["job_id"],
            "num_skills_matched": len(set(h[0] for h in hits)),
        })

    extracted = pd.DataFrame(long_rows)
    counts = pd.DataFrame(per_posting_counts)

    # --- feature table 1: skill frequency across postings ---
    total_postings = len(df)
    skill_freq = (
        extracted.drop_duplicates(subset=["job_id", "skill_canonical"])
        .groupby(["skill_canonical", "category"])
        .size()
        .reset_index(name="postings_matched")
    )
    skill_freq["pct_of_postings"] = (skill_freq["postings_matched"] / total_postings * 100).round(1)
    skill_freq = skill_freq.sort_values("postings_matched", ascending=False)

    # --- feature table 2: category-level rollup ---
    category_freq = (
        extracted.drop_duplicates(subset=["job_id", "category"])
        .groupby("category")
        .size()
        .reset_index(name="postings_with_category")
    )
    category_freq["pct_of_postings"] = (category_freq["postings_with_category"] / total_postings * 100).round(1)
    category_freq = category_freq.sort_values("postings_with_category", ascending=False)

    # --- feature table 3: monthly trend for top 10 skills ---
    top_skills = skill_freq.head(10)["skill_canonical"].tolist()
    trend = (
        extracted[extracted["skill_canonical"].isin(top_skills)]
        .drop_duplicates(subset=["job_id", "skill_canonical"])
        .groupby(["posting_month", "skill_canonical"])
        .size()
        .reset_index(name="count")
    )
    trend_pivot = trend.pivot(index="posting_month", columns="skill_canonical", values="count").fillna(0).astype(int)

    # --- coverage stats ---
    postings_with_any_skill = counts[counts["num_skills_matched"] > 0].shape[0]
    coverage_pct = round(postings_with_any_skill / total_postings * 100, 1)
    avg_skills_per_posting = round(counts["num_skills_matched"].mean(), 2)

    # --- candidate terms ---
    candidates = mine_candidates(df, matchers, blocklist)

    # --- save everything ---
    extracted.to_csv(f"{outdir}/meta_extracted_skills_20260926.csv", index=False)
    counts.to_csv(f"{outdir}/meta_skill_counts_per_posting_20260926.csv", index=False)
    skill_freq.to_csv(f"{outdir}/meta_feature_skill_frequency_20260926.csv", index=False)
    category_freq.to_csv(f"{outdir}/meta_feature_category_frequency_20260926.csv", index=False)
    trend_pivot.to_csv(f"{outdir}/meta_feature_monthly_skill_trend_20260926.csv")
    candidates.to_csv(f"{outdir}/meta_taxonomy_candidates_20260926.csv", index=False)

    print(f"Total postings: {total_postings}")
    print(f"Postings with >=1 matched skill: {postings_with_any_skill} ({coverage_pct}%)")
    print(f"Average skills per posting: {avg_skills_per_posting}")
    print(f"Distinct canonical skills matched at least once: {skill_freq.shape[0]} of {len(skills)}")
    print(f"Candidate (unmatched, frequent) terms logged: {len(candidates)}")

    return {
        "total_postings": total_postings,
        "coverage_pct": coverage_pct,
        "avg_skills_per_posting": avg_skills_per_posting,
        "distinct_skills_matched": int(skill_freq.shape[0]),
        "taxonomy_size": len(skills),
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_skills.py <cleaned_csv> <taxonomy_yaml> <outdir>")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
