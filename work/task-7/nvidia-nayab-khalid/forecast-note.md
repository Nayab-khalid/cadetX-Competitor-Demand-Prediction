# Forecast Note - NVIDIA

Member: Nayab Khalid | Company: NVIDIA | Task 7 | Date: 2026-09-20

Full write-up with figures: [Task-7-Demand-Forecasting-NVIDIA-Nayab-Khalid.pdf](Task-7-Demand-Forecasting-NVIDIA-Nayab-Khalid.pdf)

## The constraint, stated first

The shared config sets a **12-week horizon**. The NVIDIA series has **12 observations**. Forecasting
a horizon as long as the entire history is a data problem, not a modelling problem, and no choice
of model fixes it.

So this task fits five simple models and backtests them properly, rather than fitting one complex
model that cannot be evaluated. With 12 points, ARIMA order selection or Prophet's seasonality
terms would be fitting noise.

## Results

Expanding-origin, one-step-ahead backtest over the last 4 observations.

### Open roles (stock, 12 observations)

| Model | MAE | MAPE | Bias |
|---|---|---|---|
| **Simple exponential smoothing** | **5.91** | **1.38%** | -3.14 |
| Mean of last 3 | 6.33 | 1.50% | -0.67 |
| Holt linear trend | 8.45 | 2.01% | +3.49 |
| Naive (last value) | 9.00 | 2.14% | +2.00 |
| Drift | 10.96 | 2.61% | +5.30 |

SES beats the naive baseline by 34%. That is a real result, not a formality.

### New postings per day (flow, 11 intervals)

| Model | MAE | MAPE | Bias |
|---|---|---|---|
| **Mean of last 3** | **1.99** | **10.40%** | -1.74 |
| Holt linear trend | 2.42 | 12.97% | -1.17 |
| Simple exponential smoothing | 2.78 | 15.12% | -0.74 |
| Naive (last value) | 3.02 | 16.51% | -0.50 |
| Drift | 3.23 | 17.77% | -0.36 |

### Forecasts

| Series | Model | 12 weeks ahead | 80% interval | Useful? |
|---|---|---|---|---|
| Open roles | SES | **416** | 377 to 455 | Marginally |
| New per day | Mean of last 3 | **17.7** | 7.6 to 27.8 | **No** |

At 4 weeks the open-roles forecast is 416 with an interval of 394 to 439, which is usable. At 12
weeks the flow interval spans a factor of 3.6 and carries no information.

## The finding worth reporting

**Task 5's upward trend does not forecast.** Task 5 measured new-per-day rising at +0.60 per
observation, and that is real in the sample. But in the backtest the two models that extrapolate a
trend — Drift and Holt — come **last and second-last** on the flow series. The models that win
assume no trend at all.

The trend is real and it is not projectable. A hiring plan built on extrapolating it would be built
on noise. This is the sort of thing a backtest exists to catch, and it is why the naive baseline is
reported next to every model rather than omitted.

Both series forecast essentially flat, which agrees with Task 5: NVIDIA holds roughly 416 open
roles and replaces them rather than growing.

## Method

- **Models:** naive, mean of last 3, drift, simple exponential smoothing, Holt linear trend.
- **Backtest:** expanding origin, one step ahead, last 4 observations held out.
- **Metrics:** MAE and MAPE, both reported, plus bias and residual spread.
- **Intervals:** 80%, from backtest residual standard deviation widened by the square root of the
  horizon. They are empirical, not model-assumed, so they inherit the backtest's small sample.
- **Seasonality:** not modelled. Four months of data cannot identify an annual cycle, and pretending
  otherwise would manufacture structure.

## Limitations

1. **Twelve observations.** Every number here rests on that. The backtest itself has four points.
2. **The 12-week horizon is not supportable** on this data. The 4-week view is the defensible one.
3. **Intervals are empirical** and inherit the same small sample.
4. **Left-censoring** in the underlying data (Task 2) means the first observation is not a true
   arrival count; the flow series starts from the second.
5. **No seasonality, no external drivers.** Product launches, earnings and hiring freezes are not
   in the model.
6. **This forecasts postings, not headcount.** Closed does not mean filled (Task 5, section 4).

## For the team

1. **Denser collection is the only real fix.** The source has 126 daily snapshots; re-running Task
   2 collection at `--every 2` would give roughly 60 observations instead of 12 and would improve
   this task more than any modelling change.
2. **Report the naive baseline.** Any member whose model does not beat last-value-carried-forward
   should say so.
3. **Three of four companies cannot do this task at all** as their data stands: Google and
   Microsoft have no usable posting dates and Meta's window is 2024. Task 7 is currently NVIDIA-only.

## Files

`data/forecasts/` — open_roles_backtest, open_roles_forecast, new_per_day_backtest,
new_per_day_forecast, forecast_summary · `figures/` — open_roles_forecast, new_per_day_forecast,
backtest_open_roles · `forecast_demand.py`

```bash
cd work/task-7/nvidia-nayab-khalid
python forecast_demand.py
```
