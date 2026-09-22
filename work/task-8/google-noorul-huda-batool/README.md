# Task 8 – Company Similarity Scoring By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

> Same scope note as Task 6: this member's raw data only covers Google/YouTube. `similarity_scoring.py` reuses Task 6's `competitor_data/<Company>/` auto-merge pattern, so dropping in teammates' Task 4 outputs immediately extends every table/heatmap below to all four companies with no code changes.

## 1. Method — three complementary similarity views
| View | Metric | What it captures |
|---|---|---|
| `similarity_jaccard_skills.csv` | Jaccard index over each company's distinct taxonomy-skill set | raw skill-vocabulary overlap — "do they ask for the same skills at all" |
| `similarity_cosine_skill_profile.csv` | Cosine similarity over each company's skill-*category* mention-share vector | "tech-stack fingerprint" — similar mix of Programming/Cloud/Data-ML/Business-Soft-Skills etc., even if the exact skills differ |
| `similarity_cosine_tfidf_text.csv` | Cosine similarity over TF-IDF vectors (unigrams+bigrams) of each company's concatenated cleaned posting text | phrasing/role-mix similarity beyond the fixed taxonomy — catches things the taxonomy doesn't have a keyword for |

Three views rather than one, because each answers a different question: Jaccard is strict (same exact skills), cosine-on-profile is about *shape* of the tech stack, and TF-IDF is taxonomy-agnostic — a company could score low on Jaccard (different named skills) but high on TF-IDF (similar underlying role descriptions), and that gap is itself informative.

## 2. Results — Google vs YouTube (within-dataset demonstration)
- **Jaccard skill overlap: 0.398** — only ~40% of the combined skill vocabulary is shared; YouTube's 20 postings use a narrower set (all 37 of YouTube's skills are also used by Google — 0 unique to YouTube — while Google's much larger 1,107-posting set surfaces 56 skills YouTube's postings never happen to mention).
- **Cosine skill-profile similarity: 0.987** — despite the low exact-skill overlap, their *tech-stack shape* is nearly identical (both lean Business & Soft Skills, similar Programming/Education shares — see Task 6's `skill_category_mix.csv`). This is the expected pattern for a subsidiary run inside its parent's hiring pipeline.
- **Cosine TF-IDF text similarity: 0.788** — moderately high; postings read similarly in style/content but not as close as the profile similarity, likely due to YouTube's smaller, more content/product-specific role set.
- **Interpretation**: the gap between Jaccard (0.40) and profile-cosine (0.99) is the interesting signal here — it shows YouTube isn't a *different* kind of employer from Google, it's a *smaller-vocabulary* one. A team-wide comparison across four separate competitor companies would be expected to show low scores on all three metrics where a genuine strategic divergence exists.

## 3. What a real 4-company run would add
With `competitor_data/` populated by teammates, the same script produces N×N similarity matrices and heatmaps (`visuals/heatmap_*.png`) across all four companies — letting Strategy/HR readers see at a glance which competitor's hiring pattern is closest to Google's, and on which axis (raw skills vs tech-stack shape vs role phrasing) they diverge. Flagged again in Task 9.

## Task 8 Outcome
Three-metric, auto-merging similarity framework built and validated on Google vs YouTube — Jaccard skill overlap (0.40), tech-stack cosine similarity (0.99), and TF-IDF text similarity (0.79) — with heatmap visuals in `visuals/`, ready to extend to the full four-company comparison.
