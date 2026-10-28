# Task 10 - Final Presentation, Microsoft

Member: Arham Malik (Microsoft)

## Contents

| File | What it is |
|---|---|
| `slides/Microsoft-Final-Presentation-Arham-Malik.pdf` | 12-slide final deck |
| `build_deck.py` | Builds the deck and both figures |
| `figures/microsoft_cohort_change_swe.png` | Task 5 cohort change, Software Engineering only |
| `figures/microsoft_coverage_by_basis.png` | Task 6 skill coverage, titles against full text |

## Template

The deck uses the template of `../nvidia-nayab-khalid/slides/`, following the Task 10 rule of one
template, one palette and one chart style across all four decks. That means the same A4 landscape
page, header band, colours, type sizes, table and callout styles, and chart colours, all measured
from the NVIDIA PDF.

## Slide flow

It follows the same structure as the NVIDIA deck, so the four decks can be read side by side.

1. Title
2. The headline - three findings and one about the method
3. Tasks 1 and 2 - sources, and the correction to the Task 2 report
4. Tasks 3 and 4 - richest text in the team, least visible on titles
5. Task 4 - the `drive` defect in the shared taxonomy
6. Task 5 - the rise that was role mix, not skills
7. Task 6 - Microsoft on the titles basis
8. Task 7 - forecast on a simulated calendar, labelled as such
9. Task 8 - three similarity measures that disagree
10. Task 9 - what a decision-maker should do with this
11. What this data cannot tell you
12. What the team should do, and expected questions

## To rebuild

    pip install pandas matplotlib reportlab
    python build_deck.py

The script reads the committed Task 2-9 outputs under `work/task-N/microsoft-arham-malik/`, so
re-running it after any upstream change keeps the deck in step with the data. The rest of the figures
are quoted from the Task 2-9 notes: 29.1% boilerplate, the over-deletion example, the Program
Management +17 first pass, the rejected aliases, the Meta `drive` count and the Task 7 residual
spread.

## Known discrepancy

Slide 4 uses Microsoft full text at 5.95 skills per posting (6.38 before the `drive` false positive
is removed), which are the committed Task 4 and Task 6 figures. The NVIDIA deck shows 6.84 for
Microsoft. This needs reconciling in the sprint meeting.
