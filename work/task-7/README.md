# Task 7: Demand Forecasting

## Objective

Predict future hiring demand from the time-series signals, aligning on a shared forecast horizon.

## What is submitted

**Each member (in their own folder)**

1. Forecasting outputs and visual plots
2. A brief explanation of the chosen model and why

## Rules for this task

- Always report a naive baseline. A model that cannot beat last-value-carried-forward is not a result.
- Report a prediction interval, not just a point forecast.
- Backtest on a holdout. Fit quality on training data proves nothing.

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

## Open team decisions raised by this task

1. **Only NVIDIA can currently do this task.** Google and Microsoft have no usable posting dates
   and Meta's window is 2024.
2. **Denser collection is the highest-value fix.** NVIDIA's 12 observations against a 12-week
   horizon is the binding constraint; re-running collection at `--every 2` would give about 60.
3. **Task 5's upward trend does not forecast.** The trend-extrapolating models came last in
   backtesting. Worth knowing before anyone plans against a trend line.

See [Nayab's forecast note](nvidia-nayab-khalid/forecast-note.md).

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
