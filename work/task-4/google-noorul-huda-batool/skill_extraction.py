"""
Task 4 - Skill Extraction & Feature Engineering
Author: Noor Ul Huda | Company track: Google

Method: regex/keyword-based skill extraction against a shared skill taxonomy
(skill_taxonomy.json), applied to Task 3's cleaned text. This taxonomy format
(category -> skill_name -> [regex variants]) is designed to be reused as-is
against the other three companies' cleaned datasets in the team, so skill
counts stay comparable in Task 6/8.

Inputs:
  ../Task3_NLP_Preprocessing/cleaned_job_postings.csv
  skill_taxonomy.json

Outputs:
  extracted_skills.csv   (long format: job_id, skill, skill_category)
  skill_features.csv     (wide format: job_id x one binary column per skill + summary counts)
  skill_frequency.csv    (skill, skill_category, postings_mentioning, pct_of_postings)
  category_skill_counts.csv (job Category x skill_category mention counts)
"""

import json
import re

import pandas as pd

with open("skill_taxonomy.json", encoding="utf-8") as f:
    TAXONOMY = json.load(f)

# flatten to skill -> (category, compiled_pattern)
COMPILED = {}
for cat, skills in TAXONOMY.items():
    for skill, patterns in skills.items():
        combined = "|".join(patterns)
        COMPILED[skill] = (cat, re.compile(combined, flags=re.IGNORECASE))


def extract_skills_for_text(text: str) -> list:
    if not isinstance(text, str) or not text:
        return []
    found = []
    for skill, (cat, pattern) in COMPILED.items():
        if pattern.search(text):
            found.append((skill, cat))
    return found


def main():
    df = pd.read_csv("../Task3_NLP_Preprocessing/cleaned_job_postings.csv")

    records = []
    for job_id, text, category in zip(df["job_id"], df["clean_text"], df["Category"]):
        for skill, cat in extract_skills_for_text(text):
            records.append({"job_id": job_id, "skill": skill, "skill_category": cat, "job_category": category})

    extracted = pd.DataFrame(records)
    extracted.to_csv("extracted_skills.csv", index=False)

    # wide binary feature matrix
    all_skills = sorted(COMPILED.keys())
    wide = pd.DataFrame({"job_id": df["job_id"]})
    presence = extracted.pivot_table(index="job_id", columns="skill", aggfunc="size", fill_value=0)
    presence = (presence > 0).astype(int)
    wide = wide.merge(presence, on="job_id", how="left")
    for s in all_skills:
        if s not in wide.columns:
            wide[s] = 0
    wide[all_skills] = wide[all_skills].fillna(0).astype(int)

    wide["total_skills_matched"] = wide[all_skills].sum(axis=1)
    skill_to_cat = {s: c for s, (c, _) in COMPILED.items()}
    cat_count_cols = {}
    for cat in TAXONOMY.keys():
        cat_skills = [s for s in all_skills if skill_to_cat[s] == cat]
        col = "cat_" + re.sub(r"[^a-z0-9]+", "_", cat.lower()).strip("_") + "_count"
        cat_count_cols[col] = wide[cat_skills].sum(axis=1)
    wide = pd.concat([wide, pd.DataFrame(cat_count_cols)], axis=1)

    wide = wide.merge(df[["job_id", "Company", "Category", "Location", "posting_date", "posting_year_month"]], on="job_id", how="left")
    wide.to_csv("skill_features.csv", index=False)

    n_postings = len(df)
    freq = (
        extracted.groupby(["skill", "skill_category"])["job_id"].nunique().reset_index(name="postings_mentioning")
    )
    freq["pct_of_postings"] = (freq["postings_mentioning"] / n_postings * 100).round(2)
    freq = freq.sort_values("postings_mentioning", ascending=False)
    freq.to_csv("skill_frequency.csv", index=False)

    cat_counts = extracted.groupby(["job_category", "skill_category"])["job_id"].count().reset_index(name="mentions")
    cat_counts.to_csv("category_skill_counts.csv", index=False)

    print(f"Postings processed: {n_postings}")
    print(f"Total skill taxonomy size: {len(all_skills)} skills across {len(TAXONOMY)} categories")
    print(f"Postings with >=1 skill matched: {(wide['total_skills_matched'] > 0).sum()} ({(wide['total_skills_matched'] > 0).mean()*100:.1f}%)")
    print(f"Avg skills matched per posting: {wide['total_skills_matched'].mean():.2f}")
    print("Top 10 skills:")
    print(freq.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
