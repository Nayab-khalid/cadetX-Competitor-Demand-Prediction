# Task 4: Skill Extraction Method Note — Meta

Member: Abdal Farid
Date: 2026-09-26

## Method

Rules-based matching (regex over canonical names + aliases) against `job_title` and
`cleaned_description`, using the shared taxonomy at `shared/taxonomy/skills.yaml`
(version 0.1.0, 93 skills, including Nayab's silicon_design/specialisation extension —
used as-is since it is already merged into the file this team has access to; **still
pending formal ratification per the Task 4 brief, flagged below**).

No embeddings/ML classifier was used — with 209 postings and a taxonomy this size, a
transparent, auditable regex pass is easier for the team to check and re-verify than a
model would be, and matches what Nayab's NVIDIA method note used.

**Blocklist rule applied exactly as specified:** the taxonomy's `title_match_blocklist`
(`r`, `c`) is never matched against `job_title`, in either direction.

**Extra safeguard added beyond the minimum:** single-character skill terms use a strict
whitespace-or-string-edge boundary, not just regex `\b`, because `\b` alone still matches
`c` inside `c++` or `r` inside `r&d` (punctuation counts as a word boundary too — this is
the exact bug the blocklist comment describes, and it isn't limited to titles). Verified:
all "R" matches in the Meta dataset are genuine ("Python or R", "software such as R"), zero
came from a corrupted `R&D` split.

## Coverage

| | |
|---|---|
| Total postings | 209 |
| Postings with ≥1 matched skill | 191 (**91.4%**) |
| Average skills matched per posting | 3.41 |
| Distinct canonical skills matched at least once | 66 of 93 |

For comparison, NVIDIA's coverage was 72.0% against the same taxonomy (per Nayab's note),
because NVIDIA's dataset is title-only. Meta's higher coverage here reflects full
description text being present for 206/209 postings (per the Task 3 note), not a
difference in extraction quality — **this is the exact "input richness" asymmetry flagged
in the Task 2 open team decisions**, and it means raw coverage % is not directly
comparable across companies without accounting for source text length.

## Validation — three real taxonomy issues found and handled differently

Beyond the required 20-posting hand check (below), the top of the frequency table was
inspected directly, because an implausible result (Meta showing 34.4% "Autonomous
Vehicles" coverage) surfaced immediately and was worth chasing before trusting anything
downstream.

### 1. "drive" (Autonomous Vehicles alias) — false positive, fixed by taxonomy edit
71 of 72 matches were the generic corporate verb ("drive impact", "drive innovation"),
not automotive content. **Removed from the taxonomy** with a dated comment, mirroring the
existing "automation" → "Design Automation" precedent already in the file. Flagged for
team ratification alongside the rest of the taxonomy changes.

### 2. "driver" (Kernel and Drivers alias) — false positive, fixed by taxonomy edit
All 49 matches were the *identical* boilerplate sentence ("a key driver of Meta's app
growth"), repeated across duplicate/reposted postings — zero were about device drivers.
**Removed from the taxonomy** the same way. `device driver` and `linux kernel` aliases
were kept; they did not show this pattern.

### 3. "network" (Networking alias) — false positive, fixed at the matching-logic level, not the taxonomy
8 matches, but only 3 were the generic ML term "neural network"; the other 5 were genuine
(`tcp/ip network fundamentals`, `compute, network and storage`, `network engineer`).
Removing the alias entirely would have thrown away real signal, so instead a narrow
negative-context rule was added in the extraction script itself (excludes only the
"neural network" bigram) — **this is a change to my local matching logic, not to the
shared taxonomy file**, since the alias itself is fine and other members' descriptions
may use "network" differently.

### 4. "alignment" (AI Safety alias) — genuinely ambiguous, NOT edited, flagged for team discussion
16 matches, and unlike the three above this one is a real mixed bag: 10 are genuine AI
alignment/research content (Meta's FAIR team language — "reasoning, memory and alignment
methods", "safety alignment team"), 6 are generic corporate usage ("stakeholder
alignment", "drives alignment between business unit objectives"). Because it's ~62%
genuine rather than clearly wrong, this was **left as-is rather than unilaterally
removed** — flagging it for team discussion (possible fix: require "alignment" to
co-occur with "AI"/"safety"/"research" within a short window, which the current taxonomy
format can't express but a future context-rule extension could).

## Hand validation — 20 postings, random sample (seed=7)

| job_id | title | matched skills | assessment |
|---|---|---|---|
| meta_00083 | AI Research Engineer, Media | (none) | **Miss** — description mentions "image and video understanding, generation" but doesn't use an exact taxonomy phrase; a real false-negative, not a bug, just a coverage gap |
| meta_00039 | AI Research Scientist – Language | LLMs, Recommender Systems, Generative AI | Correct |
| meta_00102 | Data Scientist, Product Analytics | Python, SQL, A/B Testing | Correct |
| meta_00167 | Research Scientist, AI for Science | Python, PyTorch, TensorFlow, JAX, Statistics, ML, Deep Learning, NLP, RL, Research Publication, Networking, Performance Engineering | Correct — dense, plausible for a research role; "Networking" here is the genuine `tcp/ip`-style match, not neural-network noise |
| meta_00013 | AI Research Scientist, Robotics | Robotics | Correct |
| meta_00019 | AI Research Scientist, MRS AI (PhD) | Machine Learning, LLMs, Recommender Systems | Correct |
| meta_00138 | ISSO GRC Risk Management Intelligence Lead | AI Safety, Cybersecurity | **Borderline** — "AI Safety" came from generic "alignment" usage (see finding #4 above); "Cybersecurity" from "Security" in the ISSO department name, which is defensibly correct for a security-governance role |
| meta_00025 | AI Research Scientist – Language | LLMs, Recommender Systems, Generative AI | Correct (duplicate posting, same as meta_00039) |
| meta_00094 | Data Scientist, Product Analytics | Python, SQL, R, A/B Testing | Correct |
| meta_00150 | Associate General Counsel, Product (Youth) | Cybersecurity | **Borderline** — matched on "data security" mentioned in a legal/policy context, not a technical security skill; defensible as domain-relevant but not a strong signal |
| meta_00015 | AI Research Scientist, Robotics | Robotics | Correct |
| meta_00130 | Central Investigations Analyst | Python, SQL, Cybersecurity | Correct |
| meta_00055 | AI Research Scientist – Language | LLMs, Recommender Systems, Generative AI | Correct (duplicate posting) |
| meta_00010 | Fundamental AI Researcher – FAIR | AI Safety | Correct — genuine alignment-research context |
| meta_00023 | AI Research Scientist – Language | LLMs, Recommender Systems, Generative AI | Correct (duplicate posting) |
| meta_00112 | Research Scientist, AI, Formal and Informal Reasoning | PyTorch, ML, LLMs, RL, Research Publication, Agentic AI | Correct |
| meta_00108 | AI Research Scientist, Computer Vision | Python, PyTorch, ML, Deep Learning, Computer Vision, Robotics, Research Publication, Networking | Correct |
| meta_00018 | Contextual AI Research Scientist | Reinforcement Learning, Agentic AI | Correct |
| meta_00062 | AI Research Scientist – Language | LLMs, Recommender Systems, Generative AI | Correct (duplicate posting) |
| meta_00024 | AI Research Scientist – Language | LLMs, Recommender Systems, Generative AI | Correct (duplicate posting) |

**Result: 18/20 clearly correct, 1 false negative (miss, not a bug), 1 borderline
(defensible but weak signal).** No clear false positives in this random sample — the
three confirmed false-positive patterns (drive, driver, neural network) were found by
inspecting the frequency table directly, not by this random sample, which is a useful
reminder that a random spot-check alone would have missed them; the frequency-table sanity
check was necessary too.

**Note on duplicates:** 7 of the 20 sampled postings are the identical "AI Research
Scientist – Language" duplicate/repost, consistent with the ~63% duplicate-flag rate
found in Task 2. Skill counts in the feature tables are computed per-row (not
deduplicated), so this repost inflates raw counts for LLMs/Recommender Systems/Generative
AI; anyone using these feature tables for cross-company comparison in Task 8 should
consider deduplicating first.

## Taxonomy changes made (for team ratification)

1. Removed `drive` from `Autonomous Vehicles` aliases (100% false positive in this dataset)
2. Removed `driver` from `Kernel and Drivers` aliases (100% false positive, single
   repeated boilerplate sentence)
3. Left `alignment` (AI Safety) as-is — flagged as ambiguous, not edited
4. Recommend the team consider a new taxonomy entry for **AR/VR / Reality Labs** work —
   candidate mining surfaced `augmented`/`virtual`/`immersive` at high frequency
   (103–115 occurrences), and no existing category covers this cleanly (closest is
   `Digital Twin and Simulation`, which is Omniverse/simulation-specific, not AR/VR)

Updated taxonomy file: `skills_updated_20260926.yaml`. Diff is limited to the two alias
removals above, each with a dated comment in the same style as the existing precedent.

## Feature tables produced

- `meta_extracted_skills_20260926.csv` — long format, one row per (posting, matched skill), with matched term and field (title/description)
- `meta_skill_counts_per_posting_20260926.csv` — skills-per-posting count
- `meta_feature_skill_frequency_20260926.csv` — skill × postings-matched × % of postings
- `meta_feature_category_frequency_20260926.csv` — category-level rollup
- `meta_feature_monthly_skill_trend_20260926.csv` — top-10 skills by posting month (subject to the Task 2 date-gap limitation — Sept 2024–Aug 2025 has almost no data)
- `meta_taxonomy_candidates_20260926.csv` — 60 frequent-but-unmatched terms for team review; most are generic corporate boilerplate (expected — that's what review is for), but `analytics` and the AR/VR cluster are worth the team's attention specifically

## Limitations

- Coverage is not directly comparable to NVIDIA's without adjusting for input-text richness (Task 2 open decision #1).
- High duplicate-repost rate inflates raw counts for a handful of skills (LLMs, Recommender Systems, Generative AI) tied to one repeated "MRS AI" posting; Task 8 similarity work should decide whether to deduplicate before comparing companies.
- The "alignment" ambiguity is unresolved by design — flagged, not fixed, pending team input.
- Candidate mining is frequency-based unigrams/bigrams only; it will not surface multi-word technical phrases longer than two words, or skills that only appear as part of a longer descriptive sentence.

## Library versions

Python 3.12.3, pandas 3.0.2, PyYAML 6.0.3.

## Code

`extract_skills.py`, re-verified from a clean checkout:

```
python extract_skills.py meta_cleaned_20260906.csv skills.yaml <outdir>
```

Dependencies: pandas, PyYAML (both already used by earlier tasks).
