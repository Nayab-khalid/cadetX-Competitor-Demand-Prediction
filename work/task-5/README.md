# Task 5: Hiring Trend Analysis

## Objective

Aggregate postings by week or month, calculate hiring velocity, and identify growth, decline or
seasonal spikes. Align on a shared time-series structure so all four companies compare consistently.

## What is submitted

**Each member (in their own folder)**

1. Trend-analysis tables and visual summaries
2. A short note on the key hiring patterns observed

## Rules for this task

- The shared time-series structure is in
  [`shared/config/analysis_config.yaml`](../../shared/config/analysis_config.yaml): ISO weekly
  buckets, empty periods zero-filled, velocity = new postings per bucket.
- Every chart states its units, including any normalisation.
- Any figure showing a spike must be explained or explicitly flagged as unexplained.
- Say what you did with censored periods. Do not quietly drop them.

## Definition of done

- [ ] Trend tables committed
- [ ] Figures committed, readable in greyscale with labelled axes
- [ ] Note committed, covering method, patterns and limitations
- [ ] Any deviation from the shared config stated and justified

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

## Open team decisions raised by this task

1. **Per-day normalisation for gapped series.** NVIDIA's observation gaps run 6 to 21 days because
   partial scrapes were excluded in Task 2. Raw per-observation counts turn the two 21-day gaps
   into fake spikes: 266 and 297 arrivals against a typical 100 to 120, which normalise to 12.7 and
   14.1 per day. Anyone whose collection missed days has the same distortion, and raw counts are
   not comparable across members with different cadences.

2. **How to treat a censored first observation.** NVIDIA's first observation carries 395 postings
   that were already open, so its "arrivals" are not arrivals. That period is dropped from all flow
   analysis here. Task 6 must not compare a de-censored series against a raw one.

3. **Stock versus flow needs one definition.** A member collecting only current openings has a
   stock series and no flows at all. Task 6 has to compare like with like.

See [Nayab's trend note](nvidia-nayab-khalid/trend-note.md), sections 1 and 8.

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
