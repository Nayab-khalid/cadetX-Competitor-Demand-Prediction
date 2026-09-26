"""
Task 3: NLP Preprocessing - Meta
Member: Abdal Farid

Cleans `job_description` into a new `cleaned_description` column.
Runs top to bottom from a clean checkout - only dependency is pandas.

Usage:
    python preprocess.py <input_csv> <output_csv> <log_csv>

Library versions used (see also preprocessing_note.md):
    pandas 3.0.2
    Python 3.12.3
"""

import sys
import re
import pandas as pd

# ---------------------------------------------------------------------------
# Cleaning rules, applied in order. Each is a small, named, testable function
# so the pipeline stays auditable rather than one large regex blob.
# ---------------------------------------------------------------------------

BOILERPLATE_PATTERNS = [
    # Meta's standard ADA/accommodation contact line - constant across postings,
    # adds no company-comparable signal, and repeats an internal contact address.
    re.compile(
        r"Meta is committed to providing reasonable accommodations.*?"
        r"accommodations-ext@(?:fb|meta)\.com\.?",
        re.IGNORECASE | re.DOTALL,
    ),
    # Generic EEO / equal-opportunity-employer disclaimer paragraphs.
    re.compile(
        r"(Meta is proud to be an Equal Employment Opportunity.*?)(?=\n\n|\Z)",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"([A-Za-z ]*[Ee]qual [Oo]pportunity [Ee]mployer[^.]*\.)",
    ),
]

# Embedded salary text, e.g. "$177,000/year to $247,000/year + bonus + equity + benefits"
SALARY_IN_TEXT = re.compile(
    r"\$[\d,]+(?:\.\d+)?\s*/\s*year\s*to\s*\$[\d,]+(?:\.\d+)?\s*/\s*year"
    r"(?:\s*\+\s*[A-Za-z ]+)*\.?",
    re.IGNORECASE,
)

URL_PATTERN = re.compile(r"https?://\S+")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")


def strip_boilerplate(text: str) -> tuple[str, list[str]]:
    """Remove known non-informative boilerplate blocks. Returns cleaned text
    and a list naming which patterns actually matched (for the removal log)."""
    hits = []
    for pattern in BOILERPLATE_PATTERNS:
        if pattern.search(text):
            hits.append("boilerplate_block")
        text = pattern.sub(" ", text)
    if SALARY_IN_TEXT.search(text):
        hits.append("embedded_salary_text")
        text = SALARY_IN_TEXT.sub(" ", text)
    return text, hits


def strip_html_and_urls(text: str) -> tuple[str, list[str]]:
    hits = []
    if HTML_TAG_PATTERN.search(text):
        hits.append("html_tags")
        text = HTML_TAG_PATTERN.sub(" ", text)
    if URL_PATTERN.search(text):
        hits.append("urls")
        text = URL_PATTERN.sub(" ", text)
    return text, hits


def normalise_whitespace(text: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def clean_description(raw: object) -> tuple[str | None, list[str], str]:
    """
    Returns (cleaned_text_or_None, reasons, status)
    status is one of: 'cleaned', 'empty_after_cleaning', 'missing_source'
    """
    if pd.isna(raw) or str(raw).strip() == "":
        return None, ["no_source_description"], "missing_source"

    text = str(raw)
    reasons = []

    text, r1 = strip_html_and_urls(text)
    reasons += r1

    text, r2 = strip_boilerplate(text)
    reasons += r2

    text = normalise_whitespace(text)

    if text == "":
        return None, reasons + ["empty_after_cleaning"], "empty_after_cleaning"

    return text, reasons, "cleaned"


def run(input_path: str, output_path: str, log_path: str) -> None:
    df = pd.read_csv(input_path)
    rows_in = len(df)

    cleaned_col = []
    status_col = []
    reasons_col = []

    for raw in df["job_description"]:
        cleaned, reasons, status = clean_description(raw)
        cleaned_col.append(cleaned)
        status_col.append(status)
        reasons_col.append(";".join(reasons) if reasons else "")

    df["cleaned_description"] = cleaned_col

    # Log every row's outcome - required by the task ("do not drop rows
    # silently; log what was removed and why; rows in and rows out both
    # get reported"). No rows are ever dropped from the dataset itself.
    log = pd.DataFrame({
        "job_id": df["job_id"],
        "status": status_col,
        "reasons_applied": reasons_col,
        "raw_length": df["job_description"].astype(str).str.len(),
        "cleaned_length": df["cleaned_description"].astype(str).str.len(),
    })

    df.to_csv(output_path, index=False, encoding="utf-8")
    log.to_csv(log_path, index=False, encoding="utf-8")

    rows_out = len(df)
    status_counts = log["status"].value_counts().to_dict()

    print(f"Rows in:  {rows_in}")
    print(f"Rows out: {rows_out}  (no rows dropped - all rows retained per task rule)")
    print("Status breakdown:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python preprocess.py <input_csv> <output_csv> <log_csv>")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
