# Task 3 Method Note - Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-10-26

## Input

`../../task-2/microsoft-arham-malik/microsoft_postings_raw_20261026.csv`, 182 postings.
This is the re-issued Task 2 file. The original failed `scripts/validate_dataset.py`
on personal data - three descriptions contained an email address, which
`docs/data-schema.md` forbids outright. See the Task 2 note.

## Two cleaned columns

`clean_text` keeps case and punctuation. Task 4 matches against this because the
shared taxonomy contains `C#`, `.NET` and `CI/CD`, and any step that strips
punctuation first loses them.

`token_text` is lowercased with stopwords and role words removed, for TF-IDF in
Task 8. Technology tokens are substituted before punctuation stripping so `c#`
becomes `csharp` rather than disappearing.

Role words (`engineer`, `manager`, `architect`...) are removed per the Task 4
rule that they are `role_function`, not skills.

## Stemming: not applied

The vocabulary is dominated by proper nouns. `kubernetes` stems to `kubernet`
and `azure` to `azur`, neither of which matches the taxonomy.

## Boilerplate

29.1% of the corpus (209,037 of 717,298 characters) is EEO, benefits and
security-screening text, present in roughly 180 of 182 postings. Left in, it
dominates any similarity measure while saying nothing about hiring.

## A bug worth recording

The first version used unbounded patterns ending `.*?(?=$)`. Where the closing
phrase never appeared, the pattern ran to the end of the document and deleted
real content: one 3,897-character posting collapsed to 14 tokens.

Every pattern is now anchored at both ends, and `verify_no_overdeletion()`
raises if any posting keeps under 45% of its characters. Minimum retention is
now 45.9%, shortest posting 87 tokens.

Recommended for the other three members. Every company has boilerplate, so
every member is exposed to the same failure mode, and silent text corruption
would surface as a confusing result in Task 8 rather than as an error here.

## Numbers

| | |
|---|---|
| Postings | 182 |
| Raw characters | 717,298 (mean 3,941) |
| After cleaning | 508,261 |
| Boilerplate removed | 209,037 (29.1%) |
| Tokens | 47,299 (mean 260) |
| Vocabulary | 4,885 |
