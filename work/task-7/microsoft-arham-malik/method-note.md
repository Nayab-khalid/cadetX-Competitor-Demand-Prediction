# Task 7 Method Note - Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-10-26

## What is forecast

The synthetic calendar from Task 5, not real Microsoft dates. A forecast needs
elapsed time; the real ordinal basis has ordering but no elapsed time.

Every number in `data/` and on the figure describes the simulation. The
filenames carry `SIMULATED`, the output column `basis` carries
`SIMULATED_CALENDAR_NOT_REAL`, and the figure title says so in red, because a
forecast chart is the easiest artefact in this project to quote out of context.

## Method selection

| Method | Verdict | Reason |
|---|---|---|
| Moving average | **Chosen** | 24 monthly points. Stable, transparent, hard to overfit, defensible in review. |
| ARIMA(1,0,0) | Run alongside | Wants 30-50 points for its parameter search to mean much. Included as a cross-check. |
| Prophet | Rejected | Built for multi-year daily series with real seasonality. On 24 points it fits noise and reports intervals that are not earned. |
| Deep learning | Rejected | Hundreds of observations minimum. 182 postings would be memorised. |

## Result

3-month horizon, 3-month window.

| Month | Moving average | ARIMA(1,0,0) |
|---|---|---|
| 2026-01 | 7.3 | 6.7 |
| 2026-02 | 8.1 | 7.7 |
| 2026-03 | 8.8 | 7.5 |

In-sample residual standard deviation is 4.04 on a mean of 7.6 - the band is
more than half the level. On a flat synthetic series that is expected, and it is
a useful demonstration of why a short series does not support a confident
forecast.

The two methods agree closely, which on a series with no real trend is what
should happen. Agreement here is evidence the implementation is correct, not
evidence the forecast is good.

## For the team

One horizon and one method across all four companies, or the forecasts are not
comparable. Moving average is proposed: Google's and Meta's series are short
too, and the one with genuinely real dates (Meta) is the only one where a
heavier method could be justified.
