# Shared skill taxonomy

**Alignment lock #2.** Task 4 is where this project quietly succeeds or fails. If one person writes
`pytorch`, another `PyTorch`, another `Py Torch` and the fourth `torch`, then Tasks 6, 8 and 9 are
comparing noise.

## The rule

Every skill in every member's output must be a **canonical name** from
`shared/taxonomy/skills.yaml`. Anything else is an alias and must be mapped to a canonical name.

## Canonicalisation

1. Match case-insensitively, ignoring punctuation and whitespace.
2. Map the match to its canonical name via the `aliases` list in the YAML.
3. If there is no match, it is a **candidate skill** - collect it, do not invent a canonical name
   locally.
4. Candidates are proposed in the weekly meeting and added to the YAML by PR. Two approvals to merge.

## Categories

`languages`, `ml_frameworks`, `data_engineering`, `cloud_infra`, `mlops_devops`, `analytics_bi`,
`hardware_systems`, `research_domains`, `product_process`.

A skill belongs to exactly one category. Argue about it once, in the meeting, then move on.

## What counts as a skill

- Yes: technologies, languages, frameworks, platforms, named methods (`RAG`, `RLHF`, `CUDA`).
- No: soft-skill filler ("team player", "fast-paced environment"), degree requirements, years of
  experience, benefits, EEO boilerplate.
- Borderline: job-family words like "machine learning". Keep them, but in `research_domains`, and
  never mix them with concrete tools in the same chart.

## Maintenance

The Data Quality Lead of the week owns the taxonomy: reviewing candidates, merging PRs, and
checking that nobody's output contains an off-taxonomy skill.
