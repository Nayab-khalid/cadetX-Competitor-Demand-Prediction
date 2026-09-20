#!/usr/bin/env python3
"""Task 3 preprocessing - NVIDIA job postings.

Input :  work/task-2/nvidia-nayab-khalid/data/raw/nvidia_postings_raw_<stamp>.csv
Output:  data/processed/nvidia_postings_clean_<stamp>.csv
         data/processed/nvidia_token_frequency_<stamp>.csv

Method selection, in short
--------------------------
The NVIDIA dataset carries no description text (see the Task 2 report, section 7). The NLP input
is therefore the job title: median 6 words, maximum 13. That changes what "preprocessing" should
mean, and the pipeline is built around three decisions:

1. No aggressive stopword removal or stemming. On a 500-word description, dropping function words
   and stemming costs nothing. On a 6-word title it destroys signal: "Solutions Architect - AI
   Factory Deployment" has no words to spare, and stemming turns "Systems" and "System" into the
   same token while also mangling "Analysis" to "Analysi". Only unambiguous noise is removed.

2. Structural parsing instead of bag-of-words. NVIDIA titles follow a grammar:
   [seniority] [role] [, or - or en dash] [team / product / domain qualifier]
   1,201 of 1,745 titles carry a separator, and the head noun of the first segment is one of a
   small set (Engineer 942, Manager 307, Architect 306). Parsing that structure yields far more
   than counting words does.

3. Fill the gaps the source left. The raw feed populated seniority_level on 662 of 1,745 rows and
   job_category on 878. Both are recoverable from the title text, which is the single largest
   quality gain available in this task.

Deliberately out of scope: skill and technology extraction, which is Task 4. This script produces
cleaned text and structural fields only, so the boundary between the two tasks stays clean.

Usage:  python preprocess_nvidia.py [--in <raw csv>] [--out-dir data/processed]
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------- normalisation
# The feed carries typographic characters that would otherwise split identical titles into
# different tokens: 91 en dashes, 19 em dashes, 3 non-breaking spaces, 1 non-breaking hyphen.
DASHES = {"–": "-", "—": "-", "‒": "-", "‑": "-", "−": "-"}
SPACES = {" ": " ", " ": " ", " ": " ", "﻿": ""}

SEPARATOR_RE = re.compile(r"\s*(?:,|\s-\s|\s–\s|\s—\s|\||/(?=\s))\s*")

# --------------------------------------------------------------------------- seniority
# Ordered: the first pattern that matches wins, so "Senior Principal" resolves to Principal and
# "Senior Director" to Director. The team schema lists Junior/Mid/Senior/Lead/Principal; the four
# extra values below are flagged in the preprocessing note for ratification.
SENIORITY_RULES = [
    ("Intern",        r"\b(intern|internship|co-?op|placement)\b"),
    ("Executive",     r"\b(vice\s+president|vp|chief|head\s+of)\b"),
    ("Director",      r"\bdirector\b"),
    ("Distinguished", r"\bdistinguished\b"),
    ("Principal",     r"\bprincipal\b"),
    ("Staff",         r"\bstaff\b"),
    ("Lead",          r"\b(lead|leader)\b"),
    ("Senior",        r"\b(senior|sr\.?|snr)\b"),
    ("Junior",        r"\b(junior|jr\.?|associate|entry[-\s]level|"
                      r"new\s+(college\s+)?grad(uate)?|college\s+grad(uate)?|graduate)\b"),
]

# Words that denote rank rather than function, stripped from the cleaned title so that
# "Senior Software Engineer" and "Software Engineer" share a surface form.
# "lead" and "leader" are deliberately absent: at NVIDIA they are as often the head noun of a
# role (sales lead, account leader, engagement lead) as they are a rank, so stripping them would
# delete the only content word in those titles. Found by manual validation.
SENIORITY_TOKENS = re.compile(
    r"\b(senior|sr\.?|snr|junior|jr\.?|principal|staff|distinguished|"
    r"director|vice\s+president|vp|chief|head\s+of|intern|internship|associate|"
    r"entry[-\s]level|graduate|new\s+grad)\b", re.I)

# --------------------------------------------------------------------------- role function
# Matched against the head noun of the first segment, then against the whole title as a fallback.
ROLE_FUNCTION_RULES = [
    ("Engineer",    r"\bengineer(ing)?\b"),
    ("Architect",   r"\barchitect(ure)?\b"),
    ("Scientist",   r"\bscientist\b"),
    ("Researcher",  r"\b(researcher|research|post-?doc)\b"),
    ("Developer",   r"\bdeveloper\b"),
    ("Designer",    r"\bdesigner\b"),
    ("Manager",     r"\bmanager\b"),
    ("Director",    r"\bdirector\b"),
    ("Analyst",     r"\banalyst\b"),
    ("Specialist",  r"\bspecialist\b"),
    ("Consultant",  r"\bconsultant\b"),
    ("Technician",  r"\btechnician\b"),
    ("Recruiter",   r"\b(recruiter|recruiting|talent)\b"),
    ("Counsel",     r"\b(counsel|attorney|paralegal)\b"),
    ("Accountant",  r"\b(accountant|accounting|controller)\b"),
    ("Intern",      r"\b(intern|internship)\b"),
    # Added after manual validation of a 12-row sample and a full review of the "Other" bucket.
    # These head nouns were all falling through to Other.
    ("Lead",          r"\b(lead|leader)\b"),
    ("Administrator", r"\b(administrator|admin)\b"),
    ("Assistant",     r"\bassistant\b"),
    ("Planner",       r"\bplanner\b"),
    ("Buyer",         r"\b(buyer|procurement)\b"),
    ("Auditor",       r"\bauditor\b"),
    ("Reviewer",      r"\breviewer\b"),
    ("Generalist",    r"\bgeneralist\b"),
]

# --------------------------------------------------------------------------- tokenisation
# Only unambiguous noise. Everything else in a six-word title is signal.
TITLE_STOPWORDS = {"and", "or", "of", "the", "for", "to", "in", "with", "a", "an", "&"}
YEAR_RE = re.compile(r"^(19|20)\d{2}$")

# Minimal, controlled singularisation. A general stemmer is not used: on this vocabulary it
# produces "analysi", "architectur" and "seri", which are worse than the plurals they replace.
SINGULARISE = {
    "tools": "tool", "systems": "system", "models": "model", "services": "service",
    "solutions": "solution", "platforms": "platform", "operations": "operation",
    "applications": "application", "products": "product", "programs": "program",
    "networks": "network", "drivers": "driver", "compilers": "compiler", "clusters": "cluster",
    "partners": "partner", "markets": "market", "graphics": "graphics", "analytics": "analytics",
    "communications": "communication", "sales": "sales", "devices": "device",
    "technologies": "technology", "libraries": "library", "frameworks": "framework",
    "architectures": "architecture", "engineers": "engineer", "managers": "manager",
}


def normalise_unicode(text: str) -> str:
    """NFKC, then map typographic dashes and exotic spaces onto plain ASCII equivalents."""
    text = unicodedata.normalize("NFKC", str(text))
    for src, dst in {**DASHES, **SPACES}.items():
        text = text.replace(src, dst)
    return re.sub(r"\s+", " ", text).strip()


def split_segments(title: str) -> tuple[str, list[str]]:
    """Split a title into its core role and any trailing team / product qualifiers."""
    parts = [p.strip(" -–—,") for p in SEPARATOR_RE.split(title) if p and p.strip(" -–—,")]
    if not parts:
        return title, []
    return parts[0], parts[1:]


def derive_seniority(title: str, is_lead_role: bool = False) -> str:
    """Rank from the title. When "Lead" is the role's head noun it is a function, not a rank,
    so the Lead rule is skipped for those rows - found by manual validation of 12 samples."""
    for label, pattern in SENIORITY_RULES:
        if label == "Lead" and is_lead_role:
            continue
        if re.search(pattern, title, re.I):
            return label
    return "Unspecified"


def derive_role_function(core: str, full: str) -> str:
    head = core.split()[-1] if core.split() else ""
    for label, pattern in ROLE_FUNCTION_RULES:
        if re.search(pattern, head, re.I):
            return label
    for label, pattern in ROLE_FUNCTION_RULES:
        if re.search(pattern, full, re.I):
            return label
    return "Other"


def clean_text(title: str) -> str:
    """Lowercase surface form with rank words and punctuation removed."""
    text = SENIORITY_TOKENS.sub(" ", title)
    text = re.sub(r"[^\w\s+#-]", " ", text)          # keep + # - for c++, c#, multi-gpu
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def tokenise(cleaned: str) -> list[str]:
    tokens = []
    for raw in cleaned.split():
        tok = raw.strip("-")
        if not tok or YEAR_RE.match(tok) or tok in TITLE_STOPWORDS or len(tok) == 1 and tok.isalpha():
            continue
        tokens.append(SINGULARISE.get(tok, tok))
    return tokens


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=None, help="raw CSV from Task 2")
    ap.add_argument("--out-dir", default="data/processed")
    args = ap.parse_args()

    if args.src:
        src = Path(args.src)
    else:
        candidates = sorted(Path("../../task-2/nvidia-nayab-khalid/data/raw").glob(
            "nvidia_postings_raw_*.csv"))
        if not candidates:
            print("ERROR  no raw dataset found; pass --in explicitly")
            return 1
        src = candidates[-1]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = re.search(r"(\d{8})", src.name).group(1)

    print(f"1. reading {src}")
    df = pd.read_csv(src)
    rows_in = len(df)
    print(f"   {rows_in} rows")

    print("2. normalising unicode and whitespace")
    df["job_title"] = df["job_title"].map(normalise_unicode)
    changed = int((df["job_title"] != pd.read_csv(src)["job_title"].astype(str).str.strip()).sum())
    print(f"   {changed} titles altered by normalisation")

    print("3. parsing title structure")
    parsed = df["job_title"].map(split_segments)
    df["title_core"] = [c for c, _ in parsed]
    df["title_qualifiers"] = [json.dumps(q) for _, q in parsed]
    df["n_qualifiers"] = [len(q) for _, q in parsed]

    print("4. deriving role function, then seniority")
    df["role_function"] = [derive_role_function(c, t)
                           for c, t in zip(df["title_core"], df["job_title"])]
    df["seniority_derived"] = [derive_seniority(t, f == "Lead")
                               for t, f in zip(df["job_title"], df["role_function"])]

    print("5. cleaning text and tokenising")
    df["cleaned_description"] = df["job_title"].map(clean_text)   # team schema field name
    df["cleaned_title_core"] = df["title_core"].map(clean_text)
    toks = df["cleaned_description"].map(tokenise)
    df["title_tokens"] = toks.map(json.dumps)
    df["n_tokens"] = toks.map(len)

    print("6. flagging repeated titles")
    counts = df["job_title"].value_counts()
    df["title_repeat_count"] = df["job_title"].map(counts)

    # ------------------------------------------------------------------ coverage gains
    def filled(col):
        return int(df[col].astype(str).str.strip().replace("nan", "").ne("").sum())

    before_sen = filled("seniority_level")
    after_sen = int((df["seniority_derived"] != "Unspecified").sum())
    before_cat = filled("job_category")
    after_fun = int((df["role_function"] != "Other").sum())

    cols = list(df.columns)
    keep = [c for c in cols if c not in {"title_core"}]
    out = df[keep]
    dest = out_dir / f"nvidia_postings_clean_{stamp}.csv"
    out.to_csv(dest, index=False, encoding="utf-8")
    print(f"7. wrote {dest}  ({len(out)} rows, {len(out.columns)} columns)")

    freq = Counter(t for lst in toks for t in lst)
    fr = pd.DataFrame(freq.most_common(), columns=["token", "count"])
    fr["share_of_postings"] = (fr["count"] / len(df)).round(4)
    fpath = out_dir / f"nvidia_token_frequency_{stamp}.csv"
    fr.to_csv(fpath, index=False, encoding="utf-8")
    print(f"8. wrote {fpath}  ({len(fr)} distinct tokens)")

    print("\n--- summary for the preprocessing note ---")
    print(f"rows in / rows out          {rows_in} / {len(out)}  (no rows dropped)")
    print(f"titles altered by unicode   {changed}")
    print(f"titles with a qualifier     {int((df['n_qualifiers'] > 0).sum())} of {rows_in}")
    print(f"tokens per title            min {df.n_tokens.min()} median "
          f"{int(df.n_tokens.median())} max {df.n_tokens.max()}")
    print(f"distinct tokens             {len(fr)}")
    print(f"seniority coverage          {before_sen} -> {after_sen} of {rows_in}")
    print(f"role function coverage      {before_cat} (source job_category) -> {after_fun} of {rows_in}")
    print(f"\nseniority distribution:\n{df.seniority_derived.value_counts().to_string()}")
    print(f"\nrole function distribution:\n{df.role_function.value_counts().to_string()}")
    print(f"\ntop 20 tokens:\n{fr.head(20).to_string(index=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
