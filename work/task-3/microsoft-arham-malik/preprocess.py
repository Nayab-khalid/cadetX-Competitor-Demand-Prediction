#!/usr/bin/env python3
"""Task 3 - preprocessing, Microsoft.

Input : ../task-2/microsoft-arham-malik/microsoft_postings_raw_20261026.csv
Output: data/microsoft_postings_clean_20261026.csv
        data/microsoft_token_frequency_20261026.csv
        data/microsoft_cleaning_log_20261026.csv

Two cleaned columns, deliberately:

  clean_text  - case, punctuation and technology tokens preserved. Task 4
                matches skills against THIS, because the shared taxonomy
                contains "C#", ".NET" and "CI/CD" and any step that strips
                punctuation before matching loses them entirely.
  token_text  - lowercased, punctuation and stopwords removed. Used for
                TF-IDF and similarity in Task 8.

Stemming is not applied. The vocabulary here is dominated by proper nouns
where the surface form carries the meaning; "kubernetes" stemming to
"kubernet" and "azure" to "azur" would break matching against the taxonomy.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
SRC = HERE / ".." / ".." / "task-2" / "microsoft-arham-malik" / "microsoft_postings_raw_20261026.csv"
OUT = HERE / "data"
STAMP = "20261026"

# Boilerplate blocks. Every pattern is BOUNDED - it ends on a known closing
# phrase, never on end-of-string.
#
# An earlier draft used ".*?(?=$)" for the security-screening block. When the
# terminating phrase did not appear, the pattern ran to the end of the document
# and deleted real job content: one 3,897-character posting collapsed to 14
# tokens. verify_no_overdeletion() below exists because of that, and fails loud.
BOILERPLATE = [
    r"Microsoft is an equal opportunity employer\.\s*(Microsoft is an equal opportunity employer\.\s*)?All qualified applicants.*$",
    r"Benefits/perks listed below may vary.*$",
    r"Microsoft Cloud Background Check:\s*This position will be required to pass.*?thereafter\.",
    r"Citizenship Verification:\s*This position requires verification of US Citizenship.*?requirements\.",
    r"Ability to meet Microsoft, customer and/or government security screening requirements are required for this role\.",
    r"Security Clearance Requirements:\s*Candidates must be able to meet Microsoft,.*?for this role\.",
    r"These requirements include, but are not limited to the following specialized security screenings:",
    r"Candidates must be willing to obtain and maintain a[^.]{0,40}clearance\.",
    r"If you need assistance and/or a reasonable accommodation due to a disability.*?form\.",
]

SECTION_HEADERS = ["Responsibilities", "Qualifications", "Required Qualifications",
                   "Preferred Qualifications", "Basic Qualifications",
                   "Additional Qualifications", "Minimum Qualifications",
                   "Other Requirements"]

# Role words are not skills - docs say so and Task 4 relies on it.
ROLE_WORDS = {"engineer", "manager", "architect", "scientist", "developer",
              "analyst", "lead", "director", "specialist", "consultant"}

STOPWORDS = set("""
a an the and or but if then else when while of to in on at by for with about against
between into through during before after above below from up down out off over under
again further once here there all any both each few more most other some such no nor
not only own same so than too very s t can will just don should now i me my myself we
our ours you your yours he him his she her it its they them their what which who whom
this that these those am is are was were be been being have has had having do does did
doing would could ought also may must us your you our we will can
""".split())


def normalise(text: str) -> str:
    t = unicodedata.normalize("NFKD", str(text))
    for a, b in [("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'),
                 ("\u201d", '"'), ("\u2022", " "), ("\u2013", "-"),
                 ("\u2014", "-"), ("\xa0", " ")]:
        t = t.replace(a, b)
    return t


def clean_text(text: str) -> str:
    t = normalise(text)
    for pat in BOILERPLATE:
        t = re.sub(pat, " ", t, flags=re.IGNORECASE | re.DOTALL)
    t = re.sub(r"\b[A-Za-z]{4}\b(?=\s*$)", " ", t)      # trailing req codes
    return re.sub(r"\s+", " ", t).strip()


def token_text(text: str) -> str:
    """Lowercased tokens for TF-IDF. Tech tokens are protected BEFORE
    punctuation stripping or c#, .net and ci/cd vanish."""
    t = clean_text(text).lower()
    for pat, rep in {
        r"\bc\+\+": " cplusplus ", r"\bc#": " csharp ", r"\bf#": " fsharp ",
        r"\.net\b": " dotnet ", r"\bci/cd\b": " cicd ",
        r"\bnode\.js\b": " nodejs ", r"\basp\.net\b": " aspdotnet ",
        r"\bobjective-c\b": " objectivec ", r"\ba/b\b": " abtest ",
    }.items():
        t = re.sub(pat, rep, t)
    for h in SECTION_HEADERS:
        t = t.replace(h.lower(), " ")
    t = re.sub(r"http\S+|www\.\S+", " ", t)
    t = re.sub(r"\S+@\S+", " ", t)
    t = re.sub(r"[^a-z0-9\s+]", " ", t)
    t = re.sub(r"\b\d+\b", " ", t)
    toks = [w for w in t.split()
            if w not in STOPWORDS and w not in ROLE_WORDS and len(w) > 1]
    return " ".join(toks)


def verify_no_overdeletion(df: pd.DataFrame, threshold: float = 0.45) -> float:
    """Raise if any posting kept less than `threshold` of its characters.

    Boilerplate is roughly 30% of this corpus, so anything retaining under 45%
    means a pattern over-matched. Raising rather than warning: silently
    corrupted text would propagate into Tasks 4, 5, 6, 8 and 9 and would be
    very hard to trace back from there.
    """
    ratio = df["clean_text"].str.len() / df["job_description"].str.len()
    bad = df.loc[ratio < threshold, ["job_id", "job_title"]]
    if len(bad):
        raise ValueError(f"over-deletion in {len(bad)} posting(s):\n{bad}")
    return float(ratio.min())


def main() -> None:
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(SRC, keep_default_na=False)
    raw_len = df["job_description"].str.len()

    df["clean_text"] = df["job_description"].apply(clean_text)
    min_ret = verify_no_overdeletion(df)
    df["token_text"] = df["job_description"].apply(token_text)
    df["token_count"] = df["token_text"].str.split().str.len()

    # schema asks for cleaned_description; keep both names so downstream
    # code and the team validator agree
    df["cleaned_description"] = df["clean_text"]

    df.to_csv(OUT / f"microsoft_postings_clean_{STAMP}.csv", index=False)

    from collections import Counter
    counts = Counter(" ".join(df["token_text"]).split())
    (pd.DataFrame(counts.most_common(), columns=["token", "count"])
       .assign(pct_of_postings=lambda d: d["token"].map(
           lambda t: round(df["token_text"].str.contains(
               rf"\b{re.escape(t)}\b", regex=True).sum() / len(df) * 100, 1)))
       .head(300)
       .to_csv(OUT / f"microsoft_token_frequency_{STAMP}.csv", index=False))

    log = pd.DataFrame([
        {"step": "normalise unicode", "detail": "smart quotes, bullets, nbsp folded to ASCII"},
        {"step": "strip boilerplate", "detail": f"{len(BOILERPLATE)} bounded patterns (EEO, benefits, screening)"},
        {"step": "over-deletion guard", "detail": f"min retention {min_ret*100:.1f}%, threshold 45%"},
        {"step": "clean_text", "detail": "case and punctuation preserved for taxonomy matching"},
        {"step": "token_text", "detail": "lowercased, stopwords and role words removed, tech tokens protected"},
        {"step": "stemming", "detail": "NOT applied - breaks proper-noun skill names"},
    ])
    log.to_csv(OUT / f"microsoft_cleaning_log_{STAMP}.csv", index=False)

    print(f"rows                  {len(df)}")
    print(f"raw chars             {raw_len.sum():,} (mean {raw_len.mean():.0f})")
    print(f"clean_text chars      {df['clean_text'].str.len().sum():,}")
    print(f"boilerplate removed   {raw_len.sum()-df['clean_text'].str.len().sum():,} "
          f"({(1-df['clean_text'].str.len().sum()/raw_len.sum())*100:.1f}%)")
    print(f"guard                 min retention {min_ret*100:.1f}%")
    print(f"tokens                {df['token_count'].sum():,} (mean {df['token_count'].mean():.0f})")
    print(f"vocabulary            {len(counts):,}")


if __name__ == "__main__":
    main()
