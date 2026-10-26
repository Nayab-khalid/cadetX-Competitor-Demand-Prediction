# Task 5 Method Note - Microsoft

Member: Arham Malik (Microsoft) | Date: 2026-10-26

## The constraint

The Microsoft source has no `posting_date`. Nayab's Task 6 note already records
that no cross-company time series is possible: NVIDIA has dates but no text,
Google has no real dates, Meta has both.

## Two bases, not equal

**Basis 1, ordinal cohorts. Real, and the basis for every claim.** Microsoft
issues requisition IDs sequentially, so `source_job_id` orders postings even
without dates. Four equal cohorts, cut on ID rank rather than value - gaps run
from 191 to 46,037, so cutting on value would give cohorts of 2 and 150.

This supports direction of change. It does not support velocity or seasonality,
because no elapsed time is known. The four cohorts could span four months or
four years.

**Basis 2, simulated calendar. Synthetic, methodology demonstration only.**
Google's Task 3 seeds a reproducible `posting_date` for all 1,127 rows and flags
it with `posting_date_is_simulated`, then demonstrates monthly velocity on it.
That precedent is followed so the Microsoft deliverable has the same shape, with
the same warning: every number on Basis 2 describes the simulation.

Dates are assigned in requisition-ID order, so the synthetic calendar preserves
the real ordering. Only the spacing is invented.

Where the two disagree, Basis 1 wins.

## The confound that changed the headline

The first pass found Program Management rising 17 points and Stakeholder
Management 13. Before writing it up, the cohorts were checked for composition.

| Job family share | C1 oldest | C4 newest |
|---|---|---|
| Software Engineering | 78.3% | 58.7% |
| Program Management | 2.2% | 17.4% |

The cohorts do not contain the same kind of role. "Program Management skills
rising" was the role mix moving, not Microsoft changing what it asks of a given
role.

Re-run holding role family constant, using Software Engineering alone - the only
family present in every cohort in usable numbers (36, 28, 29, 27):

| Skill | C1 oldest | C4 newest | Change |
|---|---|---|---|
| C++ | 38.9 | 63.0 | +24.1 |
| Cybersecurity | 27.8 | 51.9 | +24.1 |
| Apache Spark | 2.8 | 14.8 | +12.0 |
| Cloud Infrastructure | 66.7 | 77.8 | +11.1 |
| JavaScript | 30.6 | 18.5 | -12.1 |
| Agile | 52.8 | 22.2 | -30.6 |

Program Management disappears, confirming it was composition. What survives is
a coherent cluster: C++, Cybersecurity and Cloud Infrastructure rising together
describes a shift toward systems and reliability work.

Both tables are committed. `..._raw_...csv` is the confounded version, kept so
the correction is visible rather than hidden; `..._swe_...csv` is the one to
quote.

## Caution on the largest movement

Agile falling 30.6 points is the biggest single number here. It may be a change
in how postings are written rather than how teams work - methodology language
going out of fashion in job copy is not the same as methodology being abandoned.
Flagged as a question for the mentor, not asserted.

## Standing assumption

That requisition IDs increase monotonically with time. Standard applicant-
tracking behaviour, unverified for Microsoft. If it is wrong, the cohort
ordering is wrong and every Basis 1 finding falls with it.
