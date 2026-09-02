#!/usr/bin/env python3
"""Validate a job-posting dataset against the team's shared schema.

Run this before committing any dataset. Standard library only - no installs needed.

    python scripts/validate_dataset.py work/task-2/nvidia-nayab-khalid/data/raw/nvidia_postings_raw_20260901.csv

Checks the required columns from docs/data-schema.md, the ISO date format, job_id uniqueness,
and scans every cell for personal data (emails, phone numbers). Exits 1 if anything fails, so it
can be wired into CI later.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

REQUIRED = [
    "job_id",
    "company_name",
    "job_title",
    "job_description",
    "posting_date",
    "location",
    "job_url",
]

# Personal data must never appear in the dataset - see docs/legal-checklist.md.
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+\d{1,3}[\s-]?)?(?:\(\d{2,4}\)[\s-]?)?\d{3,4}[\s-]?\d{3,4}(?!\d)")
# Ordinary text is full of number groups; only flag phone-shaped strings near a phone-ish word.
# Word boundaries matter: a bare "tel" also matches "Tel Aviv", "Intel" and "hotel".
PHONE_CONTEXT_RE = re.compile(r"\b(phone|tel|telephone|mobile|whatsapp|call us)\b", re.I)
# URLs carry structured identifiers (requisition numbers, ids) that look like phone numbers but
# never are, so they are excluded from the phone scan.
PHONE_SKIP_COLUMNS = {"job_url", "job_id", "application_url"}

MIN_DESCRIPTION_CHARS = 20
SHORT_DESCRIPTION_CHARS = 200


def widen_csv_field_limit() -> None:
    """Job descriptions are long; raise the field limit as far as this platform allows."""
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit = limit // 10


def parse_iso_date(value: str) -> date | None:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a job-posting dataset against the shared schema.")
    ap.add_argument("csv_path", type=Path, help="path to the dataset CSV")
    ap.add_argument("--max-report", type=int, default=5, help="example rows to print per problem")
    args = ap.parse_args()

    path: Path = args.csv_path
    if not path.exists():
        print(f"ERROR  file not found: {path}")
        return 1

    widen_csv_field_limit()
    errors: list[str] = []
    warnings: list[str] = []

    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        missing = [c for c in REQUIRED if c not in header]
        if missing:
            print(f"ERROR  missing required columns: {', '.join(missing)}")
            print("       required order is: " + ", ".join(REQUIRED))
            return 1
        if header[: len(REQUIRED)] != REQUIRED:
            warnings.append(
                "required columns are present but not in the documented order - "
                "reorder them to match docs/data-schema.md"
            )

        rows = 0
        ids = Counter()
        companies = Counter()
        dates: list[date] = []
        bad_dates: list[str] = []
        empty_required: Counter = Counter()
        short_desc = 0
        tiny_desc: list[str] = []
        bad_urls: list[str] = []
        emails_found: list[str] = []
        phones_found: list[str] = []

        for row in reader:
            rows += 1
            jid = (row.get("job_id") or "").strip()
            ids[jid] += 1

            for col in REQUIRED:
                if not (row.get(col) or "").strip():
                    empty_required[col] += 1

            companies[(row.get("company_name") or "").strip()] += 1

            raw_date = (row.get("posting_date") or "").strip()
            parsed = parse_iso_date(raw_date)
            if parsed is None:
                if raw_date and len(bad_dates) < args.max_report:
                    bad_dates.append(f"row {rows}: {raw_date!r}")
            else:
                dates.append(parsed)

            desc = row.get("job_description") or ""
            if len(desc) < MIN_DESCRIPTION_CHARS:
                if len(tiny_desc) < args.max_report:
                    tiny_desc.append(f"row {rows}: {len(desc)} chars")
            elif len(desc) < SHORT_DESCRIPTION_CHARS:
                short_desc += 1

            url = (row.get("job_url") or "").strip()
            if url and not url.startswith(("http://", "https://")):
                if len(bad_urls) < args.max_report:
                    bad_urls.append(f"row {rows}: {url[:60]!r}")

            for col, value in row.items():
                if not value:
                    continue
                hit = EMAIL_RE.search(value)
                if hit and len(emails_found) < args.max_report:
                    emails_found.append(f"row {rows}, column {col}: {hit.group()[:40]}")
                if col not in PHONE_SKIP_COLUMNS and PHONE_CONTEXT_RE.search(value):
                    phit = PHONE_RE.search(value)
                    if phit and len(phones_found) < args.max_report:
                        phones_found.append(f"row {rows}, column {col}: {phit.group()[:30]}")

    # ---------------------------------------------------------------- verdict
    if rows == 0:
        errors.append("the file has no data rows")

    dupes = [k for k, v in ids.items() if v > 1 and k]
    if dupes:
        errors.append(f"{len(dupes)} duplicate job_id values, e.g. {dupes[: args.max_report]}")
    if ids.get("", 0):
        errors.append(f"{ids['']} rows have an empty job_id")

    for col, n in empty_required.items():
        if col == "job_id":
            continue
        (errors if col in {"job_description", "posting_date"} else warnings).append(
            f"{n} rows have an empty required field: {col}"
        )

    if bad_dates:
        errors.append("posting_date must be ISO-8601 YYYY-MM-DD; bad values: " + "; ".join(bad_dates))
    if tiny_desc:
        errors.append(f"job_description shorter than {MIN_DESCRIPTION_CHARS} chars: " + "; ".join(tiny_desc))
    if emails_found:
        errors.append("PERSONAL DATA - email addresses found: " + "; ".join(emails_found))
    if phones_found:
        errors.append("PERSONAL DATA - possible phone numbers found: " + "; ".join(phones_found))

    real_companies = [c for c in companies if c]
    if len(real_companies) > 1:
        warnings.append(
            "more than one company_name in this file "
            f"({', '.join(sorted(real_companies)[:5])}) - one file per company is expected"
        )
    if short_desc:
        warnings.append(f"{short_desc} descriptions are under {SHORT_DESCRIPTION_CHARS} chars - check for truncation")
    if bad_urls:
        warnings.append("job_url should be an absolute http(s) URL: " + "; ".join(bad_urls))

    print(f"file            {path}")
    print(f"rows            {rows}")
    print(f"unique job_ids  {len([k for k in ids if k])}")
    print(f"company_name    {', '.join(sorted(real_companies)) or '(empty)'}")
    if dates:
        months = sorted({d.strftime('%Y-%m') for d in dates})
        unit = "month" if len(months) == 1 else "months"
        print(f"date range      {min(dates)} to {max(dates)}  ({len(months)} {unit})")
    print()

    for wmsg in warnings:
        print(f"WARN   {wmsg}")
    for emsg in errors:
        print(f"ERROR  {emsg}")

    print()
    if errors:
        print(f"FAILED - {len(errors)} error(s), {len(warnings)} warning(s). Fix the errors before committing.")
        return 1
    print(f"PASSED - 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
