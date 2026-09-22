"""
Task 8 - Company Similarity Scoring
Author: Noor Ul Huda | Company track: Google

Same scope note as Task 6: this member's data only covers Google/YouTube.
The script auto-merges teammates' companies from ./competitor_data/<Company>/
(same layout as Task 6) if present; otherwise it demonstrates the similarity
framework on Google vs YouTube.

Method: three complementary similarity views, computed pairwise across
companies and combined into one heatmap-ready framework:
  1. Skill-overlap similarity  - Jaccard index over each company's taxonomy-skill set
  2. Skill-profile cosine similarity - cosine similarity over each company's
     skill-category mention-share vector (the "tech-stack" fingerprint)
  3. Text (TF-IDF) similarity  - cosine similarity over TF-IDF vectors built
     from each company's concatenated cleaned job-posting text (captures
     phrasing/role-mix similarity beyond the fixed taxonomy)

Inputs:
  ../Task3_NLP_Preprocessing/cleaned_job_postings.csv
  ../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv
  ./competitor_data/<Company>/{cleaned_job_postings.csv, extracted_skills.csv}  (optional)

Outputs:
  similarity_jaccard_skills.csv
  similarity_cosine_skill_profile.csv
  similarity_cosine_tfidf_text.csv
  company_skill_profile.csv   (the skill-category share vectors used above)
  visuals/*.png (heatmaps)
"""

import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

os.makedirs("visuals", exist_ok=True)
COMPETITOR_DIR = "competitor_data"


def load_all():
    cleaned = pd.read_csv("../Task3_NLP_Preprocessing/cleaned_job_postings.csv")
    skills = pd.read_csv("../Task4_Skill_Extraction_Feature_Engineering/extracted_skills.csv")
    cleaned_frames, skill_frames = [cleaned], [skills]
    if os.path.isdir(COMPETITOR_DIR):
        for company_dir in sorted(glob.glob(os.path.join(COMPETITOR_DIR, "*"))):
            cf = os.path.join(company_dir, "cleaned_job_postings.csv")
            sf = os.path.join(company_dir, "extracted_skills.csv")
            if os.path.exists(cf) and os.path.exists(sf):
                cleaned_frames.append(pd.read_csv(cf))
                skill_frames.append(pd.read_csv(sf))
    return pd.concat(cleaned_frames, ignore_index=True), pd.concat(skill_frames, ignore_index=True)


def plot_heatmap(matrix: pd.DataFrame, title: str, path: str):
    plt.figure(figsize=(5 + 0.4 * len(matrix), 5 + 0.4 * len(matrix)))
    plt.imshow(matrix.values, cmap="viridis", vmin=0, vmax=1)
    plt.colorbar(label="Similarity")
    plt.xticks(range(len(matrix.columns)), matrix.columns, rotation=45, ha="right")
    plt.yticks(range(len(matrix.index)), matrix.index)
    for i in range(len(matrix.index)):
        for j in range(len(matrix.columns)):
            plt.text(j, i, f"{matrix.values[i, j]:.2f}", ha="center", va="center", color="white", fontsize=9)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main():
    cleaned, skills = load_all()
    companies = sorted(cleaned["Company"].unique())
    skills = skills.merge(cleaned[["job_id", "Company"]], on="job_id", how="left")

    if os.path.isdir(COMPETITOR_DIR) and glob.glob(os.path.join(COMPETITOR_DIR, "*")):
        print(f"Loaded competitor_data -> comparing: {companies}")
    else:
        print(f"No ./competitor_data found -> demonstrating framework on within-dataset companies: {companies}")

    # 1) Jaccard similarity of skill sets
    company_skillsets = {c: set(skills.loc[skills["Company"] == c, "skill"].unique()) for c in companies}
    jaccard = pd.DataFrame(index=companies, columns=companies, dtype=float)
    for a in companies:
        for b in companies:
            union = company_skillsets[a] | company_skillsets[b]
            inter = company_skillsets[a] & company_skillsets[b]
            jaccard.loc[a, b] = len(inter) / len(union) if union else 0.0
    jaccard.to_csv("similarity_jaccard_skills.csv")

    # 2) cosine similarity of skill-category profile (tech-stack fingerprint)
    profile = pd.crosstab(skills["Company"], skills["skill_category"], normalize="index")
    profile = profile.reindex(companies).fillna(0)
    profile.to_csv("company_skill_profile.csv")
    cos_profile = pd.DataFrame(cosine_similarity(profile.values), index=companies, columns=companies)
    cos_profile.to_csv("similarity_cosine_skill_profile.csv")

    # 3) TF-IDF text similarity over each company's concatenated posting text
    docs = [" ".join(cleaned.loc[cleaned["Company"] == c, "clean_text"].dropna().astype(str)) for c in companies]
    vec = TfidfVectorizer(max_features=3000, stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vec.fit_transform(docs)
    cos_tfidf = pd.DataFrame(cosine_similarity(tfidf_matrix), index=companies, columns=companies)
    cos_tfidf.to_csv("similarity_cosine_tfidf_text.csv")

    plot_heatmap(jaccard.astype(float), "Skill-Set Overlap (Jaccard)", "visuals/heatmap_jaccard_skills.png")
    plot_heatmap(cos_profile, "Tech-Stack Profile Similarity (Cosine)", "visuals/heatmap_cosine_skill_profile.png")
    plot_heatmap(cos_tfidf, "Job-Description Text Similarity (TF-IDF Cosine)", "visuals/heatmap_cosine_tfidf.png")

    print("\n=== Jaccard skill overlap ===")
    print(jaccard.round(3).to_string())
    print("\n=== Cosine skill-profile similarity ===")
    print(cos_profile.round(3).to_string())
    print("\n=== Cosine TF-IDF text similarity ===")
    print(cos_tfidf.round(3).to_string())

    if len(companies) >= 2:
        a, b = companies[0], companies[1]
        common = company_skillsets[a] & company_skillsets[b]
        only_a = company_skillsets[a] - company_skillsets[b]
        only_b = company_skillsets[b] - company_skillsets[a]
        print(f"\n{a} vs {b}: {len(common)} shared skills, {len(only_a)} unique to {a}, {len(only_b)} unique to {b}")


if __name__ == "__main__":
    main()
