"""
Task 3 - NLP Preprocessing & Method Selection
Author: Noor ul Huda | Company track: Google
Input:  ../job_skills.csv  (raw Google/YouTube job postings)
Output: cleaned_job_postings.csv

Pipeline:
  1. Load raw data, assign a stable job_id.
  2. Handle missing values in Responsibilities / Min Qualifications / Preferred Qualifications.
  3. Concatenate text fields into one document per posting.
  4. Clean text: lowercase, strip HTML/urls, remove punctuation/digits, normalise whitespace.
  5. Tokenize, remove stopwords, lemmatize (NLTK WordNet lemmatizer).
  6. Add a SIMULATED posting_date column.
     NOTE (limitation, also logged in README.md): the public job_skills.csv dataset
     (a static Kaggle snapshot) does not include a real posting-date field, and no
     legally-approved live source with dates was available for this task (see Task 1/2
     reports). Tasks 5 and 7 require a time series, so a synthetic posting_date is
     generated here (seeded, reproducible) by sampling a date in a 24-month window with
     mild category-level seasonality, purely to demonstrate the trend/forecasting
     methodology. This is clearly flagged everywhere the date field is used downstream
     and must not be read as real hiring-velocity data.
"""

import re
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

RANDOM_SEED = 42
DATE_START = pd.Timestamp("2023-01-01")
DATE_END = pd.Timestamp("2024-12-31")

STOPWORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

# Keep a few tokens that look like stopwords but matter for tech/skill context
KEEP_TOKENS = {"c", "r", "go"}
STOPWORDS -= KEEP_TOKENS


def basic_clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^a-z0-9+#./\- ]", " ", text)  # keep +,#,.,/,- for tech terms (c++, c#, node.js)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_lemmatize(text: str) -> list:
    tokens = word_tokenize(text)
    out = []
    for tok in tokens:
        if tok in STOPWORDS:
            continue
        if len(tok) <= 1 and tok not in KEEP_TOKENS:
            continue
        if tok.isdigit():
            continue
        out.append(LEMMATIZER.lemmatize(tok))
    return out


GROWTH_CATEGORIES = {
    "Software Engineering", "Data Center & Network", "Technical Infrastructure",
    "IT & Data Management", "Network Engineering", "Technical Solutions",
    "Developer Relations",
}


def _sample_trapezoidal(rng: np.random.Generator, end_to_start_ratio: float) -> float:
    """Sample t in [0,1] from a linear (trapezoidal) density with f(1)/f(0) = ratio.
    Unlike a Beta(a,b) with a,b>1 (which forces density to 0 at BOTH ends and creates
    an artificial mid-window hump / near-zero tails), this keeps density positive at
    both endpoints, so no month is artificially collapsed toward zero postings."""
    r = end_to_start_ratio
    a = 2.0 / (r + 1.0)   # density at t=0
    b = a * (r - 1.0)     # slope, so density at t=1 is a+b = a*r
    u = rng.uniform(0.0, 1.0)
    if abs(b) < 1e-9:
        return u
    t = (-a + (a ** 2 + 2 * b * u) ** 0.5) / b
    return min(max(t, 0.0), 1.0)


def simulate_posting_date(rng: np.random.Generator, category: str) -> pd.Timestamp:
    total_days = (DATE_END - DATE_START).days
    # mild category-level trend: engineering/data/infra categories trend up over the
    # window (end density 2.5x start), other categories trend gently down (end density
    # 0.6x start) -- a linear trend, not a hump, so no window-edge collapses to zero.
    ratio = 2.5 if category in GROWTH_CATEGORIES else 0.6
    frac = _sample_trapezoidal(rng, ratio)
    offset = int(frac * total_days)
    return DATE_START + pd.Timedelta(days=offset)


def main():
    df = pd.read_csv("../job_skills.csv")

    # Task 2 flagged 123 exact full-row duplicates in the raw dataset but kept the raw
    # file untouched. This is the right stage to drop them: they'd otherwise double-count
    # postings in every downstream trend/forecast/comparison table.
    n_before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    n_dupes_dropped = n_before - len(df)

    df.insert(0, "job_id", [f"JOB{idx:05d}" for idx in df.index])

    for col in ["Responsibilities", "Minimum Qualifications", "Preferred Qualifications"]:
        df[col] = df[col].fillna("")

    df["clean_title"] = df["Title"].apply(basic_clean)

    df["raw_text"] = (
        df["Title"].fillna("") + ". "
        + df["Responsibilities"] + " "
        + df["Minimum Qualifications"] + " "
        + df["Preferred Qualifications"]
    )
    df["clean_text"] = df["raw_text"].apply(basic_clean)

    tokens = df["clean_text"].apply(tokenize_and_lemmatize)
    df["tokens"] = tokens.apply(lambda t: " ".join(t))
    df["token_count"] = tokens.apply(len)

    rng = np.random.default_rng(RANDOM_SEED)
    df["posting_date"] = df["Category"].apply(lambda c: simulate_posting_date(rng, c))
    df["posting_year_month"] = df["posting_date"].dt.to_period("M").astype(str)
    df["posting_date_is_simulated"] = True

    out_cols = [
        "job_id", "Company", "Title", "clean_title", "Category", "Location",
        "posting_date", "posting_year_month", "posting_date_is_simulated",
        "Responsibilities", "Minimum Qualifications", "Preferred Qualifications",
        "raw_text", "clean_text", "tokens", "token_count",
    ]
    df = df[out_cols]
    df.to_csv("cleaned_job_postings.csv", index=False)

    print(f"Exact duplicate rows dropped: {n_dupes_dropped}")
    print(f"Rows processed: {len(df)}")
    print(f"Avg tokens/posting: {df['token_count'].mean():.1f}")
    print(f"Empty clean_text rows: {(df['clean_text'].str.len() == 0).sum()}")
    print("Saved -> cleaned_job_postings.csv")


if __name__ == "__main__":
    main()
