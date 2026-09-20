# Similarity Note - NVIDIA

Member: Nayab Khalid | Company: NVIDIA | Task 8 | Date: 2026-09-20

Full write-up with heatmaps: [Task-8-Company-Similarity-NVIDIA-Nayab-Khalid.pdf](Task-8-Company-Similarity-NVIDIA-Nayab-Khalid.pdf)

## Headline

**Similarity cannot be measured from job titles.** Title-based skill vectors carry about one skill
per posting, which is too sparse for cosine similarity to mean anything: every pair scores between
0.02 and 0.22, and the ranking flips depending on which taxonomy is used. The full-text matrix,
available for three companies, gives scores between 0.38 and 0.57 and is stable.

## Method

Per the shared config: canonical skill share vectors, TF-IDF weighted, cosine similarity. Run three
ways, because Task 6 established a taxonomy bias that Task 8 cannot ignore.

| Matrix | Taxonomy | Text | Companies |
|---|---|---|---|
| M1 | extended (93) | titles | all four |
| M2 | pre-extension (59) | titles | all four — the unbiased control |
| M3 | extended (93) | full descriptions | Google, Meta, Microsoft — NVIDIA has no text |

## M1 — extended taxonomy, titles

| | NVIDIA | Google | Microsoft | Meta |
|---|---|---|---|---|
| **NVIDIA** | 1.00 | 0.08 | 0.22 | 0.15 |
| **Google** | 0.08 | 1.00 | 0.05 | 0.02 |
| **Microsoft** | 0.22 | 0.05 | 1.00 | 0.10 |
| **Meta** | 0.15 | 0.02 | 0.10 | 1.00 |

## M2 — pre-extension taxonomy, titles (control)

| | NVIDIA | Google | Microsoft | Meta |
|---|---|---|---|---|
| **NVIDIA** | 1.00 | 0.01 | 0.09 | 0.19 |
| **Google** | 0.01 | 1.00 | 0.00 | 0.01 |
| **Microsoft** | 0.09 | 0.00 | 1.00 | 0.13 |
| **Meta** | 0.19 | 0.01 | 0.13 | 1.00 |

**The ranking flips.** On M1 NVIDIA's closest peer is Microsoft (0.22); on M2 it is Meta (0.19) and
Microsoft drops to 0.09. Changing the taxonomy moves the NVIDIA-Microsoft pair by 0.123 — larger
than most of the scores themselves. A measurement whose ordering depends on that choice is not yet
a measurement.

## M3 — full description text (the one that works)

| | Google | Microsoft | Meta |
|---|---|---|---|
| **Google** | 1.00 | **0.57** | 0.42 |
| **Microsoft** | 0.57 | 1.00 | 0.38 |
| **Meta** | 0.42 | 0.38 | 1.00 |

Scores are an order of magnitude higher and the ordering is sensible: Google and Microsoft are the
most alike, two large cloud-and-platform employers hiring similar profiles. Meta sits apart from
both. **NVIDIA cannot appear in this matrix at all**, because its source carries no description
text.

## What drives the pairs

| Pair | Skills in common | Top shared | Top divider |
|---|---|---|---|
| NVIDIA – Microsoft | 5 | Cloud Infrastructure, Cybersecurity, Embedded Systems | Solutions Architecture, Networking, Datacenter Systems |
| NVIDIA – Meta | 12 | Datacenter Systems, Machine Learning, Robotics | Solutions Architecture, Networking, Cloud Infrastructure |
| NVIDIA – Google | 24 | Solutions Architecture, Cloud Infrastructure, Networking | GCP, Solutions Architecture, Networking |
| Google – Microsoft | 5 | Cloud Infrastructure, Cybersecurity, Machine Learning | GCP, Azure, Business Development |

Note the pattern: NVIDIA and Google share the *most* skills (24) yet score the *lowest* similarity
(0.08 on M1). Cosine similarity is driven by the weighted profile, not overlap count — the two
companies touch many of the same skills at very different intensities, and GCP dominates Google's
vector while Solutions Architecture and Networking dominate NVIDIA's.

## What can be concluded

| Conclusion | Confidence |
|---|---|
| Google and Microsoft are the most similar pair with usable data (0.57) | **High** — full text, stable |
| NVIDIA is unlike the other three | **Medium** — true on every matrix, but NVIDIA's vector is built from titles while the others' best data is text |
| NVIDIA's closest peer | **Not determined.** M1 says Microsoft, M2 says Meta |
| Any precise similarity value involving NVIDIA | **Low.** Sparse vectors, and a taxonomy bias worth up to 0.12 |

## Limitations

1. **Title vectors are too sparse.** One skill per posting produces near-orthogonal vectors; the
   low scores are a property of the data, not evidence that the companies are unrelated.
2. **The taxonomy bias from Task 6 propagates here** and is worth up to 0.123 on a pair.
3. **NVIDIA is absent from the only trustworthy matrix.**
4. **Sample sizes are unequal**: 1,745 and 1,227 against 209 and 182.
5. **No temporal dimension.** The shared config lists trends as a similarity input; three of four
   datasets have no usable dates, so this is a snapshot comparison only.

## For the team

1. **Do not publish a four-company similarity matrix yet.** It would be presented as a finding and
   it is not stable. This is the single most important thing I can say about Task 8.
2. **Every member extends the taxonomy for their own company** — the same ask as Task 6, and the
   precondition for this task.
3. **Settle titles versus descriptions.** M3 works and M1 does not; the difference is entirely the
   input text.

## Files

`data/similarity/` — similarity_M1_extended_titles, similarity_M2_original_titles,
similarity_M3_extended_fulltext, pair_drivers, matrix_comparison · `figures/` fig1–fig3 ·
`similarity.py`

```bash
cd work/task-8/nvidia-nayab-khalid
python similarity.py
```
