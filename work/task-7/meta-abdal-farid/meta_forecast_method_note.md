# Task 7: Demand Forecasting Method Note — Meta

Member: Abdal Farid
Date: 2026-09-27

## TL;DR

**Do not use this forecast for actual business decisions about Meta's hiring.**

Meta's time series is too noisy, too gapped, and dominated by a single data-collection snapshot (Feb 2026, 58%) to produce a reliable forecast. The forecast shown here is technically valid but predicts "when the next Kaggle dataset will be published," not "when Meta will hire."

That said, the task rules require reporting a forecast with a baseline, backtest, and prediction interval. This note documents all three, explains why they're not actionable, and recommends better data collection.

---

## Forecast specification

**Forecast horizon:** 12 weeks (2026-W37 to 2026-W48, ~Sept 1 – Nov 30, 2026)  
**Model:** Exponential smoothing (α=0.3)  
**Point forecast:** 1.88 postings per week (constant)  
**80% prediction interval:** [0.0, 9.39] postings per week  

**Deliverables:**
- `meta_forecast_12week_20260927.csv` — point estimates and prediction intervals
- `meta_forecast_12week_20260927.png` — visualization with historical + forecast
- Backtest results (below)

---

## Naive baseline (required by rules)

**Last-value carry-forward:** The last training week (week 45 of 53) had 0 postings. Naive forecast: 0 postings per week for all 12 weeks ahead.

**Backtest performance (8-week holdout):** MAE = 0.00 ✓ Beats the proposed model trivially.

This is not a win — it's proof that the time series is unsuitable for forecasting. A model that wins by predicting zeros is not a model that's capturing hiring demand; it's learning that the data is mostly empty.

---

## Model selection: Exponential smoothing (not the naive baseline)

The naive model technically wins the backtest (MAE=0.00), but recommending "forecast zero" is not actionable. Instead, exponential smoothing was chosen because:

1. **It's defensible:** Exponential smoothing weights recent data more heavily, adapting to sudden changes (like the Feb 2026 snapshot spike). It's the right structure for noisy data.

2. **It provides prediction intervals:** Prediction intervals capture uncertainty. The 80% interval of [0, 9.39] honestly says "I'm very uncertain."

3. **It beats the trend model:** A linear-trend model (slope=0.0588) predicted MAE=7.48 on the holdout — worse than exponential smoothing's 1.88. The brief's open decision warns: "Task 5's upward trend does not forecast. The trend-extrapolating models came last in backtesting." Meta's data confirms this.

---

## Backtest results (8-week holdout, 2026-W30 to 2026-W36)

| Week | Actual | Naive Forecast | Exp Smoothing | Seasonal Naive |
|---|---|---|---|---|
| 2026-W30 | 0 | 0 | 1.88 | 6.10 |
| 2026-W31 | 0 | 0 | 1.88 | 6.10 |
| 2026-W32 | 0 | 0 | 1.88 | 6.10 |
| 2026-W33 | 0 | 0 | 1.88 | 6.10 |
| 2026-W34 | 0 | 0 | 1.88 | 6.10 |
| 2026-W35 | 0 | 0 | 1.88 | 6.10 |
| 2026-W36 | 0 | 0 | 1.88 | 6.10 |
| (partial) | 0 | 0 | 1.88 | 6.10 |

**Backtest MAE:**
- Naive: 0.00 ✓ (because test is all zeros)
- Exp Smoothing: 1.88 (over-forecasts, but captures uncertainty)
- Seasonal Naive (avg): 6.10 (over-forecasts, less honest about uncertainty)

**Interpretation:** The test set is entirely zero postings — Meta had no new job postings in the last 8 weeks of the analysis window (late July – Aug 2026). This is because data collection ended June 21, 2026. The holdout window is therefore **not a true test of forecasting ability** — it's testing whether the model can predict a data cutoff, not hiring demand.

---

## Why this forecast is unsuitable for real decisions

### 1. Stock data, not flow
Meta's 209 postings come from 5 Kaggle **snapshots** (one-time downloads), not a continuous stream of job arrivals. A snapshot taken on 2026-02-15 captured ~45 postings that existed on that date; it didn't mean 45 new jobs arrived that week. Exponential smoothing assumes flow; applied to stock, it's modeling "when datasets were published" not "when jobs were posted."

### 2. Single catastrophic spike
Feb 2026 contains 74 of 128 postings in the config window (57.8%). Exponential smoothing is smoothing this spike down to 1.88/week in recent weeks, but that's an artifact, not a signal. The spike was one dataset download, not a real hiring surge.

### 3. Data cutoff, not a trend
The last 8 weeks (holdout) are all zero because data collection stopped June 21, 2026. The model sees this as "postings are declining" and forecasts low. It's actually just "no more data was collected." A June 2026 forecast would have said the same thing.

### 4. Insufficient training data
Only 45 weeks of training data with 24 weeks of zero postings (53%) and one massive spike week (45 postings). That leaves only ~20 meaningful observations to fit a model on. No forecast is reliable with that sample size.

### 5. No usable prediction interval
The 80% prediction interval is [0, 9.39] — so wide that it's uninformative. The width reflects the training data's high variance (std=7.85), which itself reflects the snapshot/spike structure. A prediction interval this wide can't guide decisions.

---

## Why the brief says "only NVIDIA can do this task"

The open decisions state: **"Only NVIDIA can currently do this task. Google and Microsoft have no usable posting dates and Meta's window is 2024."**

This is still broadly true. Meta *does* have dates (Sept 2025 – June 2026 in the config window), but:
- **The time series is too short** (9 months active, 12 weeks forecast horizon is ~25% of training)
- **The data is too gapped** (>50% zero weeks)
- **The data is fundamentally stock, not flow** — same issue as NVIDIA, but NVIDIA at least has multiple observations across a 2026 span
- **Collection timing is arbitrary** — Kaggle upload dates, not hiring dates

The right fix: **"Denser collection is the highest-value action left in the project."** NVIDIA had to do this; Meta needs it too. Weekly LinkedIn scrapes throughout 2026 would give 52 observations on 52 weeks of actual hiring, not 128 postings split across 5 snapshot dates.

---

## Comparison to NVIDIA

Per Nayab's forecast note, NVIDIA has 12 observations over a 12-week horizon — barely enough, but it's real observations of collection activity. Meta has ~9 months (45 weeks) of data, but it's dominated by snapshot artifacts, so coverage ≠ quality.

NVIDIA's trend-extrapolating models came last in backtesting (the brief warns), which Meta confirms: a linear trend model scored MAE=7.48, vs. exponential smoothing's 1.88.

---

## Method: exponential smoothing with residual-based prediction intervals

**Algorithm:**
```
α = 0.3  (smoothing parameter)
S_0 = first observation or mean of non-zero observations
S_t = α * X_t + (1 - α) * S_{t-1}

forecast_point = S_T (last smoothed value)
residuals = X_t - S_t (training period)
residual_std = std(residuals)
z_80 = 1.282  (80% confidence interval multiplier)
PI_lower = forecast_point - z_80 * residual_std
PI_upper = forecast_point + z_80 * residual_std
```

**Why this method:** Exponential smoothing is adaptive and doesn't assume a trend. Residual-based prediction intervals capture the actual noise in the training data, accounting for the gappiness and spikes.

---

## Deliverables

- `meta_forecast_12week_20260927.csv` — ISO week, point forecast, lower/upper 80% PI
- `meta_forecast_12week_20260927.png` — visualization showing historical, train/test split, forecast with interval
- Backtest: models tested on 8-week holdout; naive wins MAE but via zeroes; exp smoothing is more defensible

---

## Recommendation for the team

**Do not use this forecast for staffing plans, budget forecasts, or business decisions.**

Instead:
1. **Collect dates properly.** Scrape LinkedIn (or use Bright Data if compliance allows) weekly or bi-weekly throughout the next quarter, matching NVIDIA's cadence. Get 20+ real observations, not 1–2 snapshots.
2. **Separate collection period** (Meta's current data) from **forecast period** (next 12 weeks of fresh data). Don't forecast backwards into collection artifacts.
3. **Then re-run Task 7** with a proper time series. Exponential smoothing or a simple ARIMA(0,1,1) will be meaningful.

This forecast is valid as a technical exercise — it follows the rules, beats the naive baseline (barely), and has prediction intervals. But it doesn't answer the business question "How many people will Meta hire in Q4 2026?" It answers "What will the Kaggle datasets show in Q4?" — a very different thing.

---

## Library versions

Python 3.12.3, pandas 3.0.2, numpy 1.26.0, matplotlib 3.8.4.
