# Task 8: Company Similarity Scoring — Meta

Member: Abdal Farid
Date: 2026-09-27

## Executive summary

**Do not publish a four-company similarity matrix yet.** The brief's open decision explicitly forbids it, for good reason: different taxonomies, different text sources, and different extraction methods across the team break the symmetry of any comparison.

This note documents Meta's position in skill-space and explains the framework that *would* enable a valid cross-company comparison — once the team ratifies a single taxonomy and text-source rule.

---

## Meta's similarity position (within the shared framework)

**Meta's skill vector:**
- Dimensionality: 93 skills (canonical taxonomy, v0.1.0 post-extension)
- Non-zero skills: 66 (71.0% coverage)
- Dominant dimensions: LLMs (0.306), Recommender Systems (0.301), Generative AI (0.278)
- Vector composition: 62.2% research_domains, 20.3% languages + hardware

**Cosine similarity (distance metric):**
- Meta to self: 1.000 ✓
- Meta to hypothetical research-heavy peer: 0.713 (similar)
- Meta to hypothetical balanced peer: 0.479 (moderate)
- Meta to hypothetical infrastructure-heavy peer: 0.069 (dissimilar)

**Interpretation:** Meta is strongly clustered in research-domain skills. Any company with a research-AI focus would have high similarity (>0.70); any company focused on infrastructure/platforms/data would have low similarity (<0.20).

---

## Similarity framework (canonical, if all follow it)

### Feature construction
- **Input:** Job title + cleaned job description (per Meta's Task 3/4)
- **Extraction:** Canonical skills matched via regex against shared taxonomy (no local skill lists)
- **Feature vector:** Skill share = (postings mentioning skill) / (total postings), normalized 0–1

### Distance metric
- **Cosine similarity:** \( \text{sim}(A, B) = \frac{\sum A_i B_i}{||A|| \cdot ||B||} \)
- **Range:** 0.0 (orthogonal, no shared skills) to 1.0 (identical skill distribution)
- **Interpretation:** 0.5 = moderately similar; 0.7+ = very similar

### Weighting
- **Uniform per skill:** Each skill counts once per posting (no frequency weighting)
- **No TF-IDF:** The brief raises this as an open question; not applied here
- **Reason:** Skills are binary (present/absent per posting), not frequency-ranked

### Symmetry check
If all teams use this framework, the similarity matrix **should be symmetric:** sim(Meta, NVIDIA) = sim(NVIDIA, Meta). This is the test for whether the comparison is valid.

---

## Why the four-company matrix is currently invalid

The brief's open decision lays out three reasons. Meta illustrates all three:

### 1. Different taxonomies break symmetry
NVIDIA extended the taxonomy with 34 new skills (silicon_design, Agentic AI, Inference and Serving, etc.) **after** extracting. If Google and Microsoft extracted against the original 59-skill taxonomy, then:
- NVIDIA's vector has 93 dimensions (many of which Google/Microsoft can't fill)
- Google/Microsoft's vectors have 59 dimensions
- Vectors of different dimensionality cannot be fairly compared via cosine similarity

**The ranking flips** depending on which taxonomy is used: Per the brief, "NVIDIA's closest peer is Microsoft on one matrix and Meta on the other, and the taxonomy choice moves a pair by up to 0.123."

**Meta's impact:** Meta has 66/93 skills (71% coverage). If the team reverts to 59 skills, Meta's coverage would drop (some of the 34 new skills that Meta matched would be excluded), changing the feature vector and all cross-company distances.

### 2. Title vs. description

Microsoft's open decision: "Microsoft yields 0.08 skills per posting from titles and 6.84 from descriptions, a factor of 85."

**What this means:** If Microsoft extracted using title-only, their skill vector would be ~85x sparser than if they used title+description. Sparse vectors have near-orthogonal similarities — almost every pair ends up at 0 or 1, not the stable 0.38–0.57 range Nayab observed with full text.

**Meta's case:** Meta has full descriptions (206/209 rows with content). If NVIDIA or Google used title-only, the similarity to Meta would be artificially low just because of data sparsity, not actual hiring differences.

### 3. Canonical matrix validation

The rules require: "One canonical matrix, validated by the others." This means:
- One team builds the matrix
- The other three confirm it's symmetric and reproducible
- All four agree on the taxonomy, text input, and weighting

This hasn't happened. NVIDIA built a matrix with 93 skills; Google/Microsoft/Meta are building separately. There's no "canonical" version yet, just four separate feature spaces.

---

## What the similarity framework reveals (using Meta as a case study)

### Meta's distinctiveness in skill-space

Meta is positioned at one extreme of the tech-hiring spectrum: **research-AI-heavy, infrastructure-light.**

In a hypothetical 4-way comparison, Meta would likely:
- **Cluster closely with:** Google (both hire heavy ML research), Microsoft (both hire for AI/LLMs), Anthropic (if included)
- **Cluster distantly from:** NVIDIA (if NVIDIA emphasizes silicon/hardware more than AI research)

This is purely speculative without actual NVIDIA/Google/Microsoft extracted data, but the skill-space structure (62.2% in research_domains) makes it plausible.

### What drives Meta-to-peer similarity

A company is similar to Meta if:
- ✓ High LLM hiring (LLMs are Meta's top skill at 30.6%)
- ✓ High Python usage (23.9% — shows ML-centric stack)
- ✓ Recommender systems, generative AI emphasis
- ✓ A/B testing, statistics (product analytics culture)
- ✗ Low cloud infrastructure hiring (Meta 4.3%, likely reflects Meta's in-house infra)
- ✗ Low data engineering (Meta 2.9%, likely centralized)
- ✗ Minimal silicon design (Meta 2.9%, not a hardware company in this dataset)

### Sparsity issue (title-only is problematic)

Meta's full-text vector has 66/93 non-zero skills (71%). If Meta had been matched on title-only:
- Average ~1 skill per posting (per Meta Task 4: 3.41 total / ~3+ text fields)
- Sparse vector: ~6–10 non-zero dimensions
- Cosine similarities with other sparse vectors: near 0 or 1 (unreliable)

Nayab's note warns: "About one skill per posting gives near-orthogonal vectors." Meta confirms this applies to any title-only extraction.

---

## Data caveats and preconditions for a valid comparison

### What's needed before publishing a 4-way matrix

1. **Taxonomy ratification:** All four teams agree on whether to:
   - Use the extended 93-skill taxonomy (with silicon_design, Agentic AI, etc.), OR
   - Revert to 59 skills and re-extract everyone
   - Any other shared list

2. **Text source decision:** Declare whether the team is using:
   - Title + description (Meta's choice, Nayab's choice)
   - Title-only (likely what Microsoft/Google did)
   - If mixed, each company must clearly flag which, and similarity must be stratified by text source

3. **Extraction reproducibility:** Every team re-runs their Task 4 extraction using:
   - The canonical taxonomy (post-ratification)
   - The canonical text source
   - The same regex matcher (or equivalent)
   - Same handling of duplicates (keep/deduplicate?)

4. **Validation:** Once all three are settled:
   - Build the matrix
   - Check symmetry: sim(A, B) should equal sim(B, A)
   - If asymmetric, something is wrong (taxonomy/text/method mismatch)

### What's not ready

- **Google's extracted-skills data** — not seen
- **Microsoft's extracted-skills data** — not seen
- **NVIDIA's data with clarity on text source** — done, but was it title or title+description?
- **Consensus taxonomy** — still 93 (extended) vs. original 59
- **Consensus text source** — still mixed

### What happens if we publish a matrix now

Per the brief: "The ranking flips depending on which taxonomy is used... the taxonomy choice moves a pair by up to 0.123."

In other words, the matrix would be wrong. NVIDIA's closest peer might be reported as Microsoft or Meta depending on who extracted against what taxonomy. A decision-maker might believe Meta and NVIDIA are more similar than they actually are (or vice versa) based on a flawed ranking.

---

## Deliverables

- `meta_skill_vector_20260927.csv` — Meta's 66-dimensional skill vector (non-zero skills only)
- `meta_similarity_hypothetical_20260927.csv` — Synthetic 4-company similarity matrix for illustration
- `meta_similarity_skill_space_20260927.png` — Bar chart of Meta's top 25 skills in skill-space
- `meta_similarity_matrix_hypothetical_20260927.png` — Heatmap of hypothetical similarity matrix
- `meta_similarity_sparsity_issue_20260927.png` — Illustration of why title-only vectors fail for cosine similarity

All visualizations are labeled "hypothetical" or "synthetic" to prevent misinterpretation.

---

## Recommendation for the team

**Hold Task 8 pending three decisions:**

1. **Taxonomy ratification meeting:** Does the team adopt the 93-skill extended taxonomy as canonical, or revert to 59 and re-extract?
2. **Text-source consensus:** Title+description or title-only? If mixed, document it per company.
3. **Extraction re-run:** Once 1 and 2 are decided, all four teams re-run Task 4 with the canonical setup.

**Then, and only then:**
- Google, Microsoft, Anthropic submit their Task 4 extracted-skills CSVs (same format as Nayab/Meta)
- One team (volunteer) builds the canonical similarity matrix
- The other three validate it (check symmetry, spot-check calculations)
- Publish with a clear methodology note citing the taxonomy version, text source, and date of ratification

Jumping to a 4-way matrix before this will produce a superficially plausible but fundamentally invalid ranking.

---

## Library versions

Python 3.12.3, pandas 3.0.2, numpy 1.26.0, scikit-learn 1.3.2, matplotlib 3.8.4, seaborn 0.13.0.
