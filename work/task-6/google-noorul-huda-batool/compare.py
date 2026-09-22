"""
Task 6 - Competitor Comparison
Author: Noor Ul Huda | Company track: Google

Scope note: the full team framework compares 4 companies. This member's raw
data (job_skills.csv, Task 1/2) only covers Google -- which itself contains
two `Company` values, "Google" and "YouTube" (a Google subsidiary). This
script therefore demonstrates the shared comparison framework using
Google vs YouTube as the within-dataset comparison, and is written to also
merge in teammates' companies automatically if they drop their Task 4 output
(`skill_features.csv`, `cleaned_job_postings.csv`) into ./competitor_data/<CompanyName>/.
When no external competitor data is present (the case here), it runs on
Google vs YouTube only and says so in its output.

Inputs:
  ../Task4_Skill_Extraction_Feature_Engineering/skill_features.csv
  ../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv
  ../Task3_NLP_Preprocessing/cleaned_job_postings.csv
  ./competitor_data/<CompanyName>/skill_features.csv        (optional, teammates)
  ./competitor_data/<CompanyName>/extracted_skills.csv       (optional, teammates)
  ./competitor_data/<CompanyName>/cleaned_job_postings.csv   (optional, teammates)

Outputs:
  company_overview.csv          postings, categories, locations per company
  category_mix_by_company.csv   % of postings per Category, per company
  top_skills_by_company.csv     top 15 skills per company with % of postings
  skill_category_mix.csv        skill-category rollup (tech-stack pattern) per company
  hiring_velocity_by_company.csv  monthly postings per company (simulated calendar)
  visuals/*.png
"""

import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("visuals", exist_ok=True)

COMPETITOR_DIR = "competitor_data"


def load_own_data():
    cleaned = pd.read_csv("../Task3_NLP_Preprocessing/cleaned_job_postings.csv", parse_dates=["posting_date"])
    skills = pd.read_csv("../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv")
    return cleaned, skills


def load_competitor_data():
    """Look for teammates' Task 4 output dropped into ./competitor_data/<Company>/."""
    cleaned_frames, skill_frames = [], []
    if os.path.isdir(COMPETITOR_DIR):
        for company_dir in sorted(glob.glob(os.path.join(COMPETITOR_DIR, "*"))):
            if not os.path.isdir(company_dir):
                continue
            cf = os.path.join(company_dir, "cleaned_job_postings.csv")
            sf = os.path.join(company_dir, "extracted_skills.csv")
            if os.path.exists(cf) and os.path.exists(sf):
                cleaned_frames.append(pd.read_csv(cf, parse_dates=["posting_date"]))
                skill_frames.append(pd.read_csv(sf))
    return cleaned_frames, skill_frames


def main():
    cleaned, skills = load_own_data()
    comp_cleaned, comp_skills = load_competitor_data()

    all_cleaned = pd.concat([cleaned] + comp_cleaned, ignore_index=True)
    all_skills = pd.concat([skills] + comp_skills, ignore_index=True)
    companies = sorted(all_cleaned["Company"].unique())

    if comp_cleaned:
        print(f"Loaded competitor_data for extra companies -> comparing: {companies}")
    else:
        print(f"No ./competitor_data found -> demonstrating framework on within-dataset companies: {companies}")

    # 1) company overview
    overview = all_cleaned.groupby("Company").agg(
        postings=("job_id", "count"),
        categories=("Category", "nunique"),
        locations=("Location", "nunique"),
    ).reset_index()
    overview.to_csv("company_overview.csv", index=False)

    # 2) category mix (%) by company
    cat_mix = pd.crosstab(all_cleaned["Company"], all_cleaned["Category"], normalize="index").mul(100).round(2)
    cat_mix.to_csv("category_mix_by_company.csv")

    # 3) top skills by company
    top_rows = []
    for company in companies:
        sub = all_skills[all_skills["job_id"].isin(all_cleaned.loc[all_cleaned["Company"] == company, "job_id"])]
        n = (all_cleaned["Company"] == company).sum()
        counts = sub["skill"].value_counts().head(15)
        for skill, cnt in counts.items():
            top_rows.append({"Company": company, "skill": skill, "postings_mentioning": cnt, "pct_of_postings": round(cnt / n * 100, 2)})
    top_skills_df = pd.DataFrame(top_rows)
    top_skills_df.to_csv("top_skills_by_company.csv", index=False)

    # 4) skill-category (tech-stack) mix by company
    skills_with_company = all_skills.merge(all_cleaned[["job_id", "Company"]], on="job_id", how="left")
    stack_mix = pd.crosstab(skills_with_company["Company"], skills_with_company["skill_category"], normalize="index").mul(100).round(2)
    stack_mix.to_csv("skill_category_mix.csv")

    # 5) hiring velocity by company (monthly, simulated calendar)
    all_cleaned["year_month"] = all_cleaned["posting_date"].dt.to_period("M").astype(str)
    velocity = all_cleaned.groupby(["year_month", "Company"]).size().rename("postings").reset_index()
    velocity_pivot = velocity.pivot(index="year_month", columns="Company", values="postings").fillna(0)
    velocity_pivot.to_csv("hiring_velocity_by_company.csv")

    # visuals
    plt.figure(figsize=(8, 5))
    cat_mix.T.plot(kind="bar", ax=plt.gca())
    plt.ylabel("% of postings")
    plt.title("Category Mix by Company")
    plt.xticks(rotation=75, fontsize=7)
    plt.tight_layout()
    plt.savefig("visuals/category_mix_by_company.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    stack_mix.T.plot(kind="bar", ax=plt.gca())
    plt.ylabel("% of skill mentions")
    plt.title("Tech-Stack / Skill-Category Mix by Company")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()
    plt.savefig("visuals/skill_category_mix.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 5))
    for company in companies:
        if company in velocity_pivot.columns:
            plt.plot(velocity_pivot.index, velocity_pivot[company], marker=".", label=company)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel("Postings/month")
    plt.title("Hiring Velocity by Company (simulated calendar)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("visuals/hiring_velocity_by_company.png", dpi=150)
    plt.close()

    print("\n=== Company Overview ===")
    print(overview.to_string(index=False))
    print("\n=== Skill-category mix (%) ===")
    print(stack_mix.to_string())


if __name__ == "__main__":
    main()
