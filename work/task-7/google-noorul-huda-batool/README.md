# Task 7 – Demand Forecasting By Noor Ul Huda

**Company track:** Google (Google Job Skills dataset)

> Built on the simulated `posting_date` calendar from Task 3 — demonstrates the forecasting methodology, not a real prediction of Google's future hiring.

## 1. Method & why
**Holt's linear exponential smoothing** (level + damped trend, no seasonal component), via `statsmodels.tsa.holtwinters.ExponentialSmoothing`.

- **Why not ARIMA**: the series is only 24 monthly points; ARIMA's (p,d,q) order selection is unstable and prone to overfitting at that length, and getting a clean fit typically needs careful manual order search per series (impractical across 1 overall + 3 category + 3 skill series).
- **Why not Prophet**: Prophet's strength is multi-year seasonality/holiday modelling, which a 24-point series can't support meaningfully — it would add a heavy dependency for no real benefit here.
- **Damped trend**: without damping, a linear trend model can extrapolate a short recent run indefinitely (e.g. runaway growth or negative postings). Damping lets the trend flatten out over the horizon, which is the safer default for a 6-month-ahead HR/hiring forecast.
- **Shared forecast horizon**: 6 months, the mid-point of the programme's "3–12 months" ask, agreed as the team's common horizon so all four companies' forecasts line up for later comparison.

## 2. What's forecasted
| Output | Series |
|---|---|
| `forecast_overall.csv` | total monthly postings, all Google/YouTube postings |
| `forecast_by_category.csv` | the categories flagged as growing in Task 5's `growth_summary.csv` (Technical Solutions, Partnerships, People Operations) with enough volume to fit |
| `forecast_by_skill.csv` | the fastest-growing taxonomy skills from Task 5 (`data_mining`, `virtualization`, `ruby`) with ≥10 total mentions |

Skill/category series with too few observations (<8 total mentions across the window) are skipped rather than forecast on noise — a fit on 3 non-zero months isn't a real forecast, it's curve-fitting on noise.

## 3. Results
- **Overall demand**: forecast holds roughly flat-to-mildly-declining, ~40 → ~37 postings/month over Jan–Jun 2025, consistent with the gentle downward trend visible in H2 2024 actuals (see `visuals/forecast_overall.png`).
- **Technical Solutions** (the strongest growth category in Task 5) is forecast to keep climbing slowly, ~6.1 → 6.8 postings/month.
- **Partnerships** and **People Operations** forecast roughly flat (~3/month each) — Task 5 showed Partnerships growing and People Operations roughly flat, and the damped-trend model correctly avoids extrapolating Partnerships' one-window growth indefinitely.
- **Skill-level forecasts** (`data_mining`, `virtualization`, `ruby`) stay low-single-digit mentions/month — expected, since these are lower-volume skills; the value here is the *direction* (mildly increasing) rather than the absolute count.

## 4. Note on a modeling bug caught during this task
An earlier version of the Task 3 date-simulation used a Beta distribution to place postings across the 24-month window. Beta(a,b) with a,b>1 has **zero density at both window edges**, which silently collapsed the last simulated month (Dec 2024) to almost no postings — an artifact, not a real trend. Left uncorrected, Holt's trend model picked up that artificial cliff and forecast the series crashing to negative postings within 2 months. This was caught by inspecting the raw monthly series before trusting the forecast, and fixed in Task 3 by switching to a linear (trapezoidal) sampler, which keeps density positive at both endpoints. Worth flagging as a general lesson: **always eyeball the raw series before fitting a forecast model** — a smooth-looking model output does not mean the input was clean.

## Task 7 Outcome
6-month-ahead demand forecasts produced for overall postings, the top growing categories, and the top growing skills, using a damped Holt's-linear-trend model chosen for its stability on a short series — with the method, horizon, and a caught data-generation bug documented above.
