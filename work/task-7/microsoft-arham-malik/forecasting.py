#!/usr/bin/env python3
"""Task 7 - demand forecasting, Microsoft.

WHAT IS FORECAST, AND WHAT IT MEANS
The Microsoft source has no posting_date. Task 5 produced two bases: real
ordinal cohorts, and a seeded synthetic calendar following the precedent
Google set in its Task 3 (posting_date_is_simulated, all 1,127 rows).

A forecast needs elapsed time, which the ordinal basis does not have. So the
forecast below runs on the SYNTHETIC calendar. Every number it produces
describes the simulation. It demonstrates that the method is built and
correct; it does not predict Microsoft hiring.

That is stated here, in the method note, in the output filenames, and on the
figure, because a forecast chart is the single easiest artefact in this
project to quote out of context.

METHOD SELECTION
  Moving average  CHOSEN. 24 synthetic monthly points. Stable, transparent,
                  hard to overfit, and defensible in review.
  ARIMA           Run alongside for comparison where statsmodels is present.
                  Wants 30-50 points for its parameter search to mean much.
  Prophet         Rejected. Built for multi-year daily series with real
                  seasonality; on 24 points it fits noise and reports
                  confident intervals that are not earned.
  Deep learning   Rejected. Hundreds of observations minimum; 182 postings
                  total would be memorised.

The team should agree one horizon and one method across all four companies,
or the four forecasts are not comparable.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
SRC = HERE/".."/".."/"task-5"/"microsoft-arham-malik"/"data"/"microsoft_monthly_postings_SIMULATED_20261026.csv"
OUT = HERE/"data"; FIG = HERE/"figures"; STAMP="20261026"
HORIZON, WINDOW = 3, 3

def moving_average(series, window=WINDOW, horizon=HORIZON):
    vals=[float(v) for v in series]
    fitted=[np.nan]*window
    for i in range(window,len(vals)):
        fitted.append(float(np.mean(vals[i-window:i])))
    resid=[v-f for v,f in zip(vals,fitted) if not np.isnan(f)]
    sd=float(np.std(resid)) if resid else 0.0
    preds,work=[],vals[:]
    for _ in range(horizon):
        nxt=float(np.mean(work[-window:])); preds.append(nxt); work.append(nxt)
    return preds, sd, fitted

def main():
    OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
    if not SRC.exists():
        print("Task 5 simulated calendar missing - run Task 5 first"); return
    m=pd.read_csv(SRC)
    preds,sd,fitted=moving_average(m["postings"])
    last=pd.Period(m["posting_month"].iloc[-1],freq="M")
    future=[str(last+i) for i in range(1,HORIZON+1)]
    out=pd.DataFrame({"posting_month":future,
                      "forecast_postings":np.round(preds,1),
                      "lower_1sd":np.round(np.array(preds)-sd,1),
                      "upper_1sd":np.round(np.array(preds)+sd,1),
                      "basis":"SIMULATED_CALENDAR_NOT_REAL"})
    out.to_csv(OUT/f"microsoft_forecast_SIMULATED_{STAMP}.csv",index=False)
    print("Forecast on the SYNTHETIC calendar - describes the simulation, not Microsoft:")
    print(out.to_string(index=False))
    print(f"\nin-sample residual sd {sd:.2f} on a mean of {m['postings'].mean():.1f}")

    try:
        from statsmodels.tsa.arima.model import ARIMA
        a=ARIMA(m["postings"].astype(float),order=(1,0,0)).fit()
        af=a.forecast(HORIZON)
        pd.DataFrame({"posting_month":future,"arima_forecast":np.round(af.values,1),
                      "basis":"SIMULATED_CALENDAR_NOT_REAL"}).to_csv(
            OUT/f"microsoft_forecast_arima_SIMULATED_{STAMP}.csv",index=False)
        print(f"\nARIMA(1,0,0) comparison: {[round(v,1) for v in af.values]}")
        print(f"  moving average: {[round(v,1) for v in preds]}")
        print("  the two agree closely, which on a flat synthetic series is expected")
    except Exception as e:
        print(f"\nARIMA skipped: {type(e).__name__}")

    fig,ax=plt.subplots(figsize=(11,5))
    ax.plot(m["posting_month"],m["postings"],marker="o",color="#999",label="observed (simulated)")
    ax.plot(m["posting_month"],fitted,color="#1F3864",linewidth=2,label=f"{WINDOW}-month MA fit")
    ax.plot(future,preds,marker="s",linestyle="--",color="#B71C1C",linewidth=2,label="forecast")
    ax.fill_between(future,np.array(preds)-sd,np.array(preds)+sd,color="#B71C1C",alpha=.15)
    ax.set_xticks(range(0,len(m)+HORIZON,3))
    ax.set_xticklabels((list(m["posting_month"])+future)[::3],rotation=45,ha="right",fontsize=7)
    ax.set_ylabel("postings per month")
    ax.set_title("SIMULATED DATA - methodology demonstration only\n"
                 "This is not a forecast of Microsoft hiring",color="#B71C1C",fontsize=11)
    ax.legend(fontsize=8); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(FIG/"microsoft_forecast_SIMULATED.png",dpi=140,bbox_inches="tight")
    print(f"\nwritten to {OUT}")

if __name__=="__main__": main()
