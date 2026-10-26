"""
Conform the Microsoft dataset to the team's shared schema and scrub personal data.

WHY THIS EXISTS
The dataset originally committed to work/task-2/microsoft-arham-malik/ fails the
team's own validator (scripts/validate_dataset.py) on two counts:

  1. PERSONAL DATA. Three job descriptions contain askstaff@microsoft.com.
     docs/data-schema.md forbids collecting an email "not even in a spare
     column - it fails the ethics criterion outright." The Task 2 report
     claimed no contact information was present. That claim was wrong.

  2. posting_date empty in all 182 rows. Unfixable from this source; the
     column stays, per the schema rule that missing fields keep their column.

It also brings the file onto the shared conventions it did not follow:
  - job_id prefixed with the company, microsoft_00001, per docs/data-schema.md
  - extracted_skills / skill_categories / tech_stack_tags as JSON list strings
    rather than semicolon-separated
  - required columns first, in the documented order

Output: microsoft_postings_raw_20261026.csv  (CONTRIBUTING.md naming)
"""

import pandas as pd
import re
import json

SRC = "/mnt/user-data/outputs/CadetX/_shared/raw_source/microsoft_jobs_dataset.csv"
OUT = "/mnt/user-data/outputs/CadetX/Task2_Data_Collection/microsoft_postings_raw_20261026.csv"

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\+?\d[\d\s().\-]{8,}\d")

REQUIRED = ["job_id", "company_name", "job_title", "job_description",
            "posting_date", "location", "job_url"]


def scrub(text):
    """Replace contact details with a marker rather than deleting silently.

    A marker keeps the sentence readable and makes the redaction auditable -
    a reviewer can see that something was removed and why, which a silent
    deletion would hide.
    """
    t = EMAIL.sub("[EMAIL REDACTED]", str(text))
    t = PHONE.sub("[PHONE REDACTED]", t)
    return t


def main():
    df = pd.read_csv(SRC, keep_default_na=False)
    before = sum(len(EMAIL.findall(str(t))) for t in df["job_description"])

    for col in ["job_description", "job_title", "location"]:
        if col in df.columns:
            df[col] = df[col].apply(scrub)

    after = sum(len(EMAIL.findall(str(t))) for t in df["job_description"])
    print(f"Emails: {before} before, {after} after")

    # company-prefixed ids, per docs/data-schema.md
    df["source_job_id"] = df["job_id"]
    df["job_id"] = [f"microsoft_{i:05d}" for i in range(1, len(df) + 1)]

    # semicolon lists -> JSON list strings, per the schema's Recommended table
    for col in ["extracted_skills", "skill_categories", "tech_stack_tags"]:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda v: json.dumps([x for x in str(v).split(";") if x]))

    cols = REQUIRED + [c for c in df.columns if c not in REQUIRED]
    df = df[cols]
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Wrote {len(df)} rows, {len(df.columns)} columns -> {OUT}")
    print(f"job_id now: {df['job_id'].iloc[0]} .. {df['job_id'].iloc[-1]}")


if __name__ == "__main__":
    main()
