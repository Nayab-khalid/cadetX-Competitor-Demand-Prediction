# Task 5: Hiring Trend Analysis Method Note — Meta

Member: Abdal Farid
Date: 2026-09-26

## Executive summary

Meta's trend data shows a **single massive spike in February 2026** (74 of 128 postings, 57.8% of the total), followed by scattered activity through June 2026, then nothing. **This is not a hiring trend. It is a data collection artifact.** The spike is a single Kaggle dataset snapshot downloaded on or around that date, not 74 independent job arrivals in the labor market.

This directly parallels Nayab's NVIDIA case: a censored observation that distorts flow analysis. Like NVIDIA, Meta's data is sourced from multiple Kaggle snapshots (5 sources), not a continuous stream. Per the team's open decisions (section 8 of Nayab's note), stock and flow need to be distinguished, and raw counts are not comparable across members who have different collection cadences.

**Recommendation for Task 6:** Treat Meta's series the same way NVIDIA's is treated — flag it as having limited data collection window (primarily Feb 2026 snapshot) and do not directly compare raw velocity or month-over-month trends against NVIDIA/Google/Microsoft without that caveat.

## Data within the analysis window

Config window: **Sept 1, 2025 — Aug 31, 2026** (as per `shared/config/analysis_config.yaml`, version 0.1.0 proposed).

Meta data coverage within this window:
- **Total rows in window:** 128 of 209 (61.2%)
- **Total rows outside window:** 81 (mostly Jan–Aug 2024, plus some from May–June 2025)
- **Active posting dates within window:** Sept 23, 2025 — June 21, 2026 (9 months)
- **Full-month data:** Dec 2025, Jan 2026, Feb 2026, Apr–Jun 2026
- **Empty months:** Mar 2026, July–Aug 2026 (zero-filled per config)
- **Sparse months:** Sept–Nov 2025 (1 posting each)

## The "spike" explained — data collection structure, not hiring behavior

February 2026 shows 74 postings (57.8% of Meta's total within the window). This week-by-week breakdown:

| Week | Postings |
|---|---|
| 2026-W06 (Feb 9–15) | 45 |
| 2026-W07 (Feb 16–22) | 2 |
| 2026-W08 (Feb 23–Mar 1) | 27 |

This is a **two-week surge, 72 of 74 postings**, concentrated in a single calendar month.

**Why this is a snapshot, not a hiring surge:** All 128 Meta postings within the config window come from 5 Kaggle datasets (per Task 2 source review):
1. `arshkon/linkedin-job-postings` — 3 rows in window
2. `asaniczka/1-3m-linkedin-jobs-and-skills-2024` — dataset primarily covers 2024, minimal contribution
3. `atharvasoundankar/ai-job-market-global-2026` — 91 rows, weekly-updated via GitHub Actions; primary contributor
4. `ankit0017/ai-and-ml-job-postings-linkedin-and-indeed-2025` — 37 rows
5. `sweetymahale/job-listing-dataset` — 4 rows

Each dataset is a **snapshot** (historical Kaggle upload capturing a moment in time), not a live stream. The Feb 2026 spike is concentrated because one of the datasets' collection dates fell in mid-February — it's not 74 separate hiring decisions over two weeks.

**Comparison to NVIDIA:** Nayab's NVIDIA data had one censored first observation (395 existing postings at collection start, treated as stock, not flow). Meta's case is similar in principle but spans the whole series: what appears as "hiring velocity" is actually "when each Kaggle dataset was downloaded and published."

## Method: weekly bucketing, zero-filling, rolling average

Per `shared/config/analysis_config.yaml`:

- **Weekly bucketing:** ISO-8601 (2026-W34 format, weeks start Monday)
- **Empty period treatment:** Zero-filled (not NaN)
- **Velocity definition:** Count of new postings per week
- **Smoothing:** 4-week rolling average (center=False, min_periods=1 per config)
- **Normalisation:** Share of company total (for cross-company comparison in Task 6)

Weekly trend table: `meta_trend_weekly_20260926.csv` (53 weeks, 128 total postings, 45 weeks with zero velocity)

Monthly trend table: `meta_trend_monthly_20260926.csv` (12 months, cumulative + share-of-total)

Visualization: `meta_trend_analysis_20260926.png`
- Top panel: raw weekly velocity + 4-week rolling average, with annotations for the Feb spike and March gap
- Bottom panel: cumulative postings + monthly share of total (%)
- Both axes labeled with units; spike and gap flagged explicitly per config rules

## Patterns observed (with caveats)

1. **Pre-data phase (Sept–Nov 2025):** 1 posting per month, likely straggler/edge-case listings from an older snapshot. Not representative of Meta hiring.

2. **Ramp phase (Dec 2025–Feb 2026):** 5 → 9 → 74 postings. The spike in Feb is the primary snapshot; Dec–Jan are slow ramp-up from other sources. **No hiring acceleration signal here — this is data arrival, not labor-market signal.**

3. **Post-snapshot phase (April–June 2026):** 9 → 6 → 22 postings from secondary Kaggle sources. **These are real observations, but each represents a different collection date, not a continuous stream.**

4. **End of window (July–Aug 2026):** Zero postings. **This is data cutoff, not hiring decline.** Meta's most recent data is June 21, 2026.

## What NOT to conclude

- "Meta's hiring surged in February" — wrong. A Kaggle dataset was released/downloaded in February.
- "Meta's hiring declined after June" — wrong. Data collection stopped in June.
- "Meta hired 74 people in Feb, then 9 in April" — wrong. These are snapshots at different times, not separate hiring cycles.
- Raw weekly or monthly counts are directly comparable to NVIDIA/Google/Microsoft — no. Those companies may have different collection cadences.

## Deviation from config (justified per rules)

No deviations. The config window is used as-is (Sept 2025–Aug 2026). The data is zero-filled for empty weeks/months as specified. Velocity is defined as postings per bucket. The spike is **not smoothed away or hidden** — it's shown raw and explicitly flagged as an artifact.

## Censored/gapped periods (per config rule: "Do not quietly drop them")

- **March 2026:** zero postings between source 3 (ends ~Feb 22) and source 4/5 (start ~April). This 38-day gap is included as zero weeks/month (no NaN).
- **July–Aug 2026:** zero postings after June 21 through end of analysis window. Included as zero, not dropped.
- **Outside-window data (81 rows):** Not included in any table, but not silently omitted — mentioned explicitly above.

## Implications for Task 6 (Cross-company comparison)

Per the open team decisions raised by Task 5 (Nayab's note, sections 1 and 8):

1. **Raw counts are not comparable.** Meta's series is stock+flow (mixed snapshots). NVIDIA's series may have different collection rhythms. Google/Microsoft may be different again. Task 6 must use normalised share-of-total, not raw velocity.

2. **Per-day normalisation.** NVIDIA noted that gapped series turn multi-day gaps into artificial spikes. Meta's case is more extreme: a 38-day gap (March 2026) followed by scattered data (April–June) means a week-by-week velocity chart is meaningless. Task 6 should consider per-day normalisation or an explicit "only compare within collection periods" caveat.

3. **Stock vs. flow distinction.** Meta's series is fundamentally **stock** (snapshots of open postings at collection date), not **flow** (arrivals over time). NVIDIA has the same issue. Task 6 cannot compare flows across companies without knowing that all four are actually stocks. The brief warns: "Task 6 has to compare like with like."

4. **Recommendation:** Treat Meta and NVIDIA data similarly — flag both as censored/gapped collection, use only the normalised share-of-total for cross-company comparison, and in the Task 6 report state explicitly that "velocity comparison is limited by data collection differences" or exclude velocity from the comparison entirely.

## Limitations

- Meta's hiring trends within the Feb–June 2026 window cannot be reliably extracted from this data — each collection point is a snapshot, not a continuous stream.
- The 4-week rolling average smooths noisy data, but the underlying data is so gapped that trend signals are unreliable.
- Any forecasting (Task 7) based on this series would be forecasting "when the next Kaggle dataset will be published," not "when Meta will post new jobs."

## Library versions

Python 3.12.3, pandas 3.0.2, matplotlib 3.8.4.

## Deliverables

- `meta_trend_weekly_20260926.csv` — 53 ISO weeks, zero-filled, velocity + cumulative + 4-week rolling average
- `meta_trend_monthly_20260926.csv` — 12 calendar months, zero-filled, velocity + cumulative + share of total (%)
- `meta_trend_analysis_20260926.png` — 2-panel visualization (raw + rolling avg, cumulative + monthly share), spike and gap annotated, readable in greyscale, axes labelled with units
