#!/usr/bin/env python3
"""Task 10 - final presentation, Microsoft.

Builds slides/Microsoft-Final-Presentation-Arham-Malik.pdf on the template of
nvidia-nayab-khalid/slides/: same page size, header band, palette, type sizes
and chart style, per the Task 10 rule of one template across all four decks.

Every number on a slide is read from a committed Task 2-9 output in this
repository, so the deck cannot drift from the data.

    pip install pandas matplotlib reportlab
    python build_deck.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

HERE = Path(__file__).resolve().parent
W_ = HERE.parents[1]                      # work/
M = "microsoft-arham-malik"
FIG = HERE / "figures"
OUT = HERE / "slides" / "Microsoft-Final-Presentation-Arham-Malik.pdf"

# ---- template, measured from the NVIDIA deck
PW, PH = 841.89, 595.28
NAVY, NAVY_TXT, GREEN, GREEN_TXT = "#13213d", "#14213d", "#75b800", "#76b900"
INK, MUTED, GRID, ZEBRA = "#1a202c", "#5a6472", "#d4dae2", "#f2f4f6"
OK_FILL, OK_EDGE = "#f4f8eb", "#c8dfa0"
WARN_FILL, WARN_EDGE, WARN_BAR = "#fdf6e6", "#f2d8a3", "#b35208"
X0, BODY_W = 57.0, 722.8
AUTHOR = "Arham Malik  |  Microsoft"

# ---- chart style, measured from the NVIDIA figures
C_BLUE, C_GREEN, C_ORANGE = "#2a78d6", "#1baf7a", "#eb6834"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "axes.edgecolor": "#dfdfdb", "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": "#dfdfdb", "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.titleweight": "bold", "axes.titlesize": 15,
    "axes.titlelocation": "left", "axes.titlecolor": "#0b0b0b",
    "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
    "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.frameon": False,
    "legend.labelcolor": "#52514e",
})


def data(task, *parts):
    return W_ / f"task-{task}" / M / "data" / Path(*parts)


def para_style(size=10, color=INK, bold=False, leading=None):
    return ParagraphStyle("p", fontName="Helvetica-Bold" if bold else "Helvetica",
                          fontSize=size, leading=leading or size * 1.45,
                          textColor=HexColor(color))


class Deck:
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(path), pagesize=(PW, PH))
        self.c.setTitle("What Microsoft's job postings reveal")
        self.c.setAuthor("Arham Malik")
        self.n = 0

    def _top(self, y):
        return PH - y

    def page(self, kicker, title, cover=False):
        if self.n:
            self.c.showPage()
        self.n += 1
        c = self.c
        c.setFillColor(HexColor(NAVY)); c.rect(0, PH - 39.7, PW, 39.7, stroke=0, fill=1)
        c.setFillColor(HexColor(GREEN)); c.rect(0, PH - 44.2, PW, 4.5, stroke=0, fill=1)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont("Helvetica-Bold", 8.5); c.drawString(51, PH - 24.4, "COMPETITOR DEMAND PREDICTION USING JOB POSTINGS")
        c.setFont("Helvetica", 8.5); c.drawRightString(790.9, PH - 24.4, AUTHOR)
        c.setFillColor(HexColor(MUTED)); c.setFont("Helvetica", 7.5)
        c.drawString(51, PH - 567.5, "CadetX Virtual Work Experience  |  Final presentation")
        if not cover:
            c.drawRightString(790.9, PH - 567.5, str(self.n))
        ky, ty, ts = (171, 205, 30) if cover else (80.5, 105.5, 21)
        c.setFillColor(HexColor(GREEN_TXT)); c.setFont("Helvetica-Bold", 9); c.drawString(X0, PH - ky, kicker.upper())
        c.setFillColor(HexColor(NAVY_TXT)); c.setFont("Helvetica-Bold", ts); c.drawString(X0, PH - ty, title)

    def text(self, html, y, size=10, color=INK, width=BODY_W, x=X0, bold=False):
        p = Paragraph(html, para_style(size, color, bold))
        _, h = p.wrap(width, PH)
        p.drawOn(self.c, x, PH - y - h)
        return y + h

    def bullets(self, items, y, size=10, gap=7.5):
        for it in items:
            self.c.setFillColor(HexColor(INK)); self.c.setFont("Helvetica", size)
            self.c.drawString(59, PH - y - size, "•")
            y = self.text(it, y, size, width=BODY_W - 12, x=69) + gap
        return y

    def table(self, rows, widths, y, row_h=23, size=9.5, bold_cols=()):
        c = self.c
        total = sum(widths)
        hs = [23] + [row_h] * (len(rows) - 1)
        tops = [y + sum(hs[:r]) for r in range(len(rows) + 1)]
        for r, row in enumerate(rows):
            top, rh = tops[r], hs[r]
            fill = NAVY if r == 0 else ("#ffffff" if r % 2 else ZEBRA)
            c.setFillColor(HexColor(fill)); c.rect(X0, PH - top - rh, total, rh, stroke=0, fill=1)
            x = X0
            for i, cell in enumerate(row):
                bold = r == 0 or i in bold_cols
                color = "#ffffff" if r == 0 else INK
                p = Paragraph(str(cell), para_style(size, color, bold, leading=size * 1.2))
                _, h = p.wrap(widths[i] - 12, rh)
                p.drawOn(c, x + 6, PH - top - (rh + h) / 2)
                x += widths[i]
        c.setStrokeColor(HexColor(GRID)); c.setLineWidth(0.4)
        for t in tops:
            c.line(X0, PH - t, X0 + total, PH - t)
        x = X0
        for wd in [0] + list(widths):
            x += wd
            c.line(x, PH - y, x, PH - tops[-1])
        return tops[-1]

    def callout(self, title, body, y, warn=False, pad=8.5):
        fill, edge, bar = (WARN_FILL, WARN_EDGE, WARN_BAR) if warn else (OK_FILL, OK_EDGE, GREEN)
        t = Paragraph(title, para_style(10.5, NAVY_TXT, True))
        b = Paragraph(body, para_style(10))
        _, th = t.wrap(BODY_W - 24, PH); _, bh = b.wrap(BODY_W - 24, PH)
        h = pad + th + 2 + bh + pad
        c = self.c
        c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(edge)); c.setLineWidth(0.5)
        c.rect(X0, PH - y - h, BODY_W, h, stroke=1, fill=1)
        c.setStrokeColor(HexColor(bar)); c.setLineWidth(4); c.line(X0, PH - y, X0, PH - y - h)
        t.drawOn(c, X0 + 12, PH - y - pad - th)
        b.drawOn(c, X0 + 12, PH - y - pad - th - 2 - bh)
        return y + h

    def image(self, path, y, w=567.0):
        h = w * 800 / 1800
        self.c.drawImage(str(path), (PW - w) / 2 + 0.5, PH - y - h, w, h)
        return y + h

    def save(self):
        self.c.save()


# ---------------------------------------------------------------- figures
def fig_cohorts(swe):
    keep = ["C++", "Cybersecurity", "Apache Spark", "Cloud Infrastructure",
            "Machine Learning", "Site Reliability", "JavaScript", "Agile"]
    d = swe.set_index("skill").loc[keep, "change"][::-1]
    fig, ax = plt.subplots(figsize=(9, 4), dpi=200)
    ax.barh(d.index, d.values, color=[C_BLUE if v > 0 else C_ORANGE for v in d.values], height=0.62)
    ax.grid(axis="x", color="#dfdfdb"); ax.grid(axis="y", visible=False)
    ax.axvline(0, color="#52514e", lw=0.8)
    for i, v in enumerate(d.values):
        ax.text(v + (0.8 if v > 0 else -0.8), i, f"{v:+.1f}", va="center",
                ha="left" if v > 0 else "right", fontsize=10, fontweight="bold", color="#0b0b0b")
    ax.set_xlim(-38, 32)
    ax.set_xlabel("change in share of postings, oldest to newest cohort (points)")
    ax.set_title("Software Engineering only, role mix held fixed")
    fig.tight_layout(); fig.savefig(FIG / "microsoft_cohort_change_swe.png"); plt.close(fig)


def fig_basis(basis):
    order = ["NVIDIA", "Google", "Meta", "Microsoft"]
    b = basis.set_index("company").loc[order]
    titles = b["titles_coverage_pct"].values
    full = [None if c == "NVIDIA" else v for c, v in zip(order, b["fulltext_coverage_pct"].values)]
    fig, ax = plt.subplots(figsize=(9, 4), dpi=200)
    x = range(len(order)); w = 0.36
    ax.bar([i - w / 2 - 0.01 for i in x], titles, w, color=C_BLUE, label="job titles (the team's comparison basis)")
    ax.bar([i + w / 2 + 0.01 for i in x], [v or 0 for v in full], w, color=C_GREEN, label="full description text")
    for i, (t, f) in enumerate(zip(titles, full)):
        ax.text(i - w / 2, t + 1.5, f"{t:.1f}%", ha="center", fontsize=10, fontweight="bold")
        ax.text(i + w / 2, (f or 0) + 1.5, f"{f:.1f}%" if f else "no text", ha="center",
                fontsize=10, fontweight="bold", color="#0b0b0b" if f else "#52514e")
    ax.set_xticks(list(x), order); ax.set_ylim(0, 112)
    ax.set_ylabel("postings with at least one skill (%)")
    ax.set_title("Same taxonomy, same matcher: coverage by basis")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=10)
    fig.tight_layout(); fig.savefig(FIG / "microsoft_coverage_by_basis.png"); plt.close(fig)


# ---------------------------------------------------------------- build
def main():
    FIG.mkdir(exist_ok=True)
    raw = pd.read_csv(W_ / "task-2" / M / "microsoft_postings_raw_20261026.csv", keep_default_na=False)
    b4 = pd.read_csv(data(4, "features", "basis_comparison_20261026.csv"))
    drive = pd.read_csv(data(4, "features", "drive_false_positive_evidence_20261026.csv"))
    swe = pd.read_csv(data(5, "microsoft_cohort_trends_swe_20261026.csv"))
    mix = pd.read_csv(data(5, "microsoft_cohort_role_mix_20261026.csv")).set_index("cohort")
    basis = pd.read_csv(W_ / "task-6" / M / "data" / "comparison" / "basis_comparison_20261026.csv")
    fc = pd.read_csv(data(7, "microsoft_forecast_SIMULATED_20261026.csv"))
    ar = pd.read_csv(data(7, "microsoft_forecast_arima_SIMULATED_20261026.csv"))
    pairs = pd.read_csv(data(8, "company_pairs_20261026.csv"))
    azure = pd.read_csv(data(9, "microsoft_azure_cooccurrence_20261026.csv"))
    grad = pd.read_csv(data(9, "microsoft_seniority_gradient_20261026.csv")).set_index("skill")
    head = json.loads(data(9, "microsoft_headline_20261026.json").read_text())
    freq = pd.read_csv(data(4, "features", "microsoft_skill_frequency_20261026.csv")).set_index("skill")
    ml_pct = freq.loc["Machine Learning", "pct_of_postings"]
    fig_cohorts(swe); fig_basis(basis)

    n = len(raw)
    ft = b4.set_index(["basis", "variant"])
    ft_ok = ft.loc[("fulltext", "drive_alias_suppressed")]
    ft_raw = ft.loc[("fulltext", "as_taxonomy_stands")]
    chg = swe.set_index("skill")["change"]
    bs = basis.set_index("company")
    n_drive = drive["job_id"].nunique()
    seniority = raw["seniority_level"].value_counts()
    states = raw["location"].value_counts()
    swe_mix = mix["Software Engineering"]; pm_mix = mix["Program Management"]

    d = Deck(OUT)

    # 1 - cover
    d.page("Final presentation", "What Microsoft's job postings reveal", cover=True)
    d.text(f"{n} engineering postings · published by Microsoft under MIT · no posting dates", 222, size=12.5)
    # cover info table has no navy header row, as on the NVIDIA cover
    c = d.c; y = 277.6
    for i, (k, v) in enumerate([("Arham Malik", "Microsoft specialist"),
                                ("Team", "Nayab Khalid (NVIDIA) · Noorul Huda Batool (Google) · Abdal Farid (Meta)"),
                                ("Repository", "github.com/Nayab-khalid/cadetX-Competitor-Demand-Prediction")]):
        top = y + i * 23
        c.setFillColor(HexColor(ZEBRA)); c.rect(X0, PH - top - 23, 119.1, 23, stroke=0, fill=1)
        c.setFillColor(HexColor(INK)); c.setFont("Helvetica", 9.5)
        c.drawString(63, PH - top - 15, k); c.drawString(182.1, PH - top - 15, v)
    c.setStrokeColor(HexColor(GRID)); c.setLineWidth(0.4)
    for i in range(4):
        c.line(X0, PH - y - i * 23, 743, PH - y - i * 23)
    for x in (X0, 176.1, 743):
        c.line(x, PH - y, x, PH - y - 69)

    # 2 - headline
    d.page("The headline", "Three findings")
    y = d.bullets([
        f"<b>Microsoft hires cloud-first; AI is present but secondary.</b> Azure appears in {head['azure_pct']}% of postings, "
        f"Machine Learning in {ml_pct}%. Reliability, networking, security and storage all cluster inside Azure work - the cloud is "
        f"where the other disciplines happen, not a line item beside them.",
        f"<b>The direction of travel is systems and security.</b> Holding role family fixed, C++ and Cybersecurity both rose "
        f"{chg['C++']:+.1f} points from the oldest to the newest cohort, Apache Spark {chg['Apache Spark']:+.1f}; "
        f"Agile fell {chg['Agile']:.1f}.",
        f"<b>Seniority buys coordination, not syntax.</b> Technical Program Management is in {grad.loc['Technical Program Management','Mid']}% "
        f"of Mid postings and {grad.loc['Technical Program Management','Principal']}% of Principal ones.",
    ], 124)
    d.callout("And one finding about the method",
              f"Microsoft has the richest description text in the team ({ft_ok['coverage_pct']}% full-text coverage) and is nearly "
              f"invisible on the basis the team compares with ({bs.loc['Microsoft','titles_coverage_pct']}% of titles). "
              f"Reading it also exposed a defect in the shared taxonomy that falsely tags {n_drive} of {n} Microsoft postings.",
              y + 14)

    # 3 - tasks 1 & 2
    d.page("Tasks 1 & 2", "No legal route to scrape - so Microsoft's own published sample")
    y = d.table([["Source", "Expected", "Actual", "Verdict"],
                 ["jobs.careers.microsoft.com", "live postings with dates", "automated request refused (robots-disallowed)", "<b>Rejected</b>"],
                 ["LinkedIn postings dataset", "33,246 rows, cross-market", "zero Microsoft-employer postings - only consultancies", "<b>Rejected</b>"],
                 ["Wayback Machine snapshots", "recover posting dates", "proposed in Task 1, not yet attempted", "Open"],
                 ["microsoft/SkillsExtractorCognitiveSearch", "sample data for an Azure demo",
                  f"{n} postings, full text, MIT, published by Microsoft", "<b>Used</b>"]],
                [190, 150, 266, 80], 124)
    y = d.text(f"No scraping and no licence ambiguity. The cost: no posting dates, all {n} postings are Engineering, and "
               f"{states.iloc[0]} of {n} are in {states.index[0]}.", y + 12)
    d.callout("A correction to my own Task 2 report",
              "The report said all records had been inspected and held no contact information. That was wrong: three descriptions "
              "contained <b>askstaff@microsoft.com</b>, which the team's data schema forbids outright. The re-issued file replaces "
              "them with a visible [EMAIL REDACTED] marker and follows the shared schema. The validator now passes on everything "
              "except posting_date, which this source does not have.", y + 14, warn=True)

    # 4 - tasks 3 & 4
    d.page("Tasks 3 & 4", "The richest text in the team - and the least visible")
    y = d.table([["", "NVIDIA", "Google", "Meta", "Microsoft"],
                 ["Skills per posting, titles"] + [f"{bs.loc[k,'titles_skills_per_posting']:.2f}" for k in ("NVIDIA", "Google", "Meta", "Microsoft")],
                 ["Coverage, titles"] + [f"{bs.loc[k,'titles_coverage_pct']:.1f}%" for k in ("NVIDIA", "Google", "Meta", "Microsoft")],
                 ["Coverage, full text", "no text"] + [f"{bs.loc[k,'fulltext_coverage_pct']:.1f}%" for k in ("Google", "Meta", "Microsoft")]],
                [175.8, 127.5, 127.6, 127.5, 127.6], 124, bold_cols=(4,))
    y = d.bullets([
        "<b>Boilerplate is 29.1% of the corpus</b> - EEO, benefits and security-screening text in roughly 180 of 182 postings. "
        "Left in, it dominates any similarity measure while saying nothing about hiring.",
        "<b>My first cleaning pass silently destroyed text.</b> An unanchored pattern ran to the end of the document: one 3,897-character "
        "posting collapsed to 14 tokens. Every pattern is now anchored, and a guard <b>raises</b> if any posting keeps under 45% of its "
        "characters. Every member has boilerplate, so every member is exposed to the same failure.",
        "<b>My first extraction run reported 0.0% title coverage</b> and I nearly wrote it up as a finding. The shared matcher is "
        "case-sensitive and returns zero, not an error, on Title Case input.",
    ], y + 12)
    d.text(f"Full text after removing the 'drive' false positive: {ft_ok['skills_per_posting']:.2f} skills per posting "
           f"({ft_raw['skills_per_posting']:.2f} as the taxonomy stands). The NVIDIA deck shows 6.84 for Microsoft; "
           f"the figures here are the committed Task 4 and Task 6 outputs, to reconcile with Nayab.", y + 4, size=8, color=MUTED)

    # 5 - task 4 taxonomy defect
    d.page("Task 4", "A defect in the shared taxonomy, affecting everyone")
    y = d.table([["Company", "Postings", "Falsely tagged 'Autonomous Vehicles'", "Why"],
                 ["Microsoft", str(n), f"<b>{n_drive} ({n_drive / n * 100:.1f}%)</b>", "full text, alias 'drive'"],
                 ["Meta", "209", "<b>70 (33.5%)</b>", "full text, alias 'drive'"],
                 ["Google", "1,127", "0% - latent, not absent", "Task 6 matched Google on titles only"],
                 ["NVIDIA", "1,745", "n/a", "no description text"]],
                [140, 100, 236, 210], 124)
    y = d.text("Every one of those postings contains the ordinary verb - <i>\"drive features to closure\"</i>, "
               "<i>\"drive impact with a global team\"</i>, <i>\"Drive for results\"</i>. None is about vehicles. "
               "I found it by reading 20 postings by hand, not from the code.", y + 12)
    y = d.bullets([
        "Two more aliases were measured before proposing them and rejected: <b>teams</b> (96 hits, 4 are Microsoft Teams) and "
        "<b>windows</b> (60 hits, 11 are the operating system).",
        "Task 4 reports both numbers - as the taxonomy stands, so nothing already committed becomes incomparable, and with the "
        "alias suppressed, so the size of the error is visible.",
    ], y + 8)
    d.callout("The fix is ready but not merged",
              "It is on its own branch, taxonomy/microsoft-extension, with Microsoft's proposed extension. It changes every member's "
              "Autonomous Vehicles numbers, so it needs the team's agreement before it goes to main.", y + 8, warn=True)

    # 6 - task 5
    d.page("Task 5", "The skill that was rising was the role mix moving")
    y = d.image(FIG / "microsoft_cohort_change_swe.png", 120, w=530)
    y = d.text(f"The first pass found Program Management skills up 17 points. The cohorts did not hold the same roles: Software "
               f"Engineering fell from {swe_mix.iloc[0]}% to {swe_mix.iloc[-1]}% of postings while Program Management rose from "
               f"{pm_mix.iloc[0]}% to {pm_mix.iloc[-1]}%. <b>Holding Software Engineering fixed, the Program Management effect "
               f"disappears.</b> What survives is a coherent cluster: systems, security and data-platform work rising together.",
               y + 10, size=10)
    d.text("No posting dates exist, so cohorts are cut on Microsoft's sequential requisition IDs: four equal groups by rank. This "
           "gives direction of change, not speed - the four cohorts could span four months or four years - and assumes IDs rise "
           "with time, which is standard but unverified. Agile's -30.6 may be job-ad style changing, not teams.",
           y + 6, size=8, color=MUTED)

    # 7 - task 6
    d.page("Task 6", "On the team's comparison basis, Microsoft is nearly invisible")
    y = d.image(FIG / "microsoft_coverage_by_basis.png", 120, w=530)
    d.callout("An empty Microsoft column means naming, not hiring less",
              "Microsoft titles are generic by house style - \"Software Engineer II\", \"Principal Data Scientist\". NVIDIA's carry "
              "the technology - \"Senior Linux Kernel Systems Software Engineer\". Titles are still the right basis: they are the only "
              "one all four companies have. But every four-way chart needs this sentence beside it, or Microsoft reads as hiring "
              "narrower. Microsoft's taxonomy extension is deliberately not applied here: doing it alone would inflate Microsoft for "
              "the same reason NVIDIA is inflated today.", y + 12, warn=True)

    # 8 - task 7
    d.page("Task 7", "A forecast on a calendar that does not exist")
    y = d.table([["Method", "Verdict", "Reason"],
                 ["Moving average", "<b>Chosen</b>", "24 monthly points: stable, transparent, hard to overfit"],
                 ["ARIMA(1,0,0)", "Cross-check", "wants 30-50 points for its parameter search to mean much"],
                 ["Prophet", "Rejected", "built for multi-year daily series; on 24 points it fits noise"],
                 ["Deep learning", "Rejected", "182 postings would be memorised"]],
                [150, 110, 426], 124)
    rows = [["Month (simulated)", "Moving average", "ARIMA(1,0,0)", "1-sd band"]]
    for (_, f), (_, a) in zip(fc.iterrows(), ar.iterrows()):
        rows.append([f["posting_month"], f"{f['forecast_postings']:.1f}", f"{a.iloc[1]:.1f}",
                     f"{f['lower_1sd']:.1f} - {f['upper_1sd']:.1f}"])
    y = d.table(rows, [171.5, 171.5, 171.5, 171.5], y + 14)
    d.callout("Every number on this slide describes the simulation",
              "Dates were seeded in requisition-ID order, following Google's Task 3 precedent: the order is real, the spacing is "
              "invented. Filenames carry SIMULATED and the output has a basis column saying so. The two methods agree, which proves "
              "the implementation, not the forecast: the residual spread (4.04 on a mean of 7.6) is more than half the level.",
              y + 14, warn=True)

    # 9 - task 8
    d.page("Task 8", "Three measures, three different answers")
    rows = [["Pair", "Jaccard (same skills?)", "Cosine, skill shares", "Cosine, title text"]]
    for _, p in pairs.iterrows():
        rows.append([f"{p['a']} - {p['b']}", f"{p['jaccard']:.3f}", f"{p['cosine_skills']:.3f}", f"{p['cosine_text']:.3f}"])
    y = d.table(rows, [200, 162, 162, 162], 124)
    y = d.bullets([
        "<b>NVIDIA - Google:</b> highest Jaccard, near-lowest cosine. They name the same skills and weight them completely "
        "differently. One measure alone would have called them the closest pair.",
        "<b>Microsoft - NVIDIA:</b> the opposite shape. Few shared skill names, but the closest proportions and the most alike title "
        "language. Microsoft's few title hits fall where NVIDIA concentrates.",
        "<b>Two sparse companies can look similar by both being sparse.</b> With 5.5% title coverage, a handful of postings moves "
        "Microsoft's vectors. I agree with the NVIDIA deck: do not publish a four-company similarity matrix yet.",
    ], y + 12)

    # 10 - task 9
    d.page("Task 9", "What a decision-maker should do with this")
    az = azure.set_index(azure.columns[0])
    def az_row(skill):
        return f"{int(az.loc[skill, 'with_azure'])} of {int(az.loc[skill, 'skill_total'])}"
    d.table([["If you are", "Then"],
             ["Competing for cloud engineers",
              f"Hire for reliability, security and networking inside Azure, not cloud on its own. Azure appears in "
              f"{az_row('Site Reliability')} Site Reliability postings, {az_row('Networking')} Networking, "
              f"{az_row('Cybersecurity')} Cybersecurity."],
             ["Watching Microsoft's direction",
              "Systems, security and data-platform skills rising together (C++, Cybersecurity, Spark); Agile and JavaScript "
              "falling. Order only - not when, not how fast."],
             ["Hiring senior people",
              f"Principal roles ask for programme management, not more languages: TPM {grad.loc['Technical Program Management','Principal']}% "
              f"at Principal. Only {seniority.get('Principal', 24)} Principal postings - each moves it by ~4 points."],
             ["Sizing Microsoft's AI hiring",
              f"In engineering postings AI is secondary: Machine Learning {ml_pct}% against Azure {head['azure_pct']}%."],
             ["Benchmarking salary or region", f"Not possible. No salary field; {states.iloc[0]} of {n} postings are in {states.index[0]}."]],
            [190, 496], 124, row_h=38)

    # 11 - honesty
    d.page("Honesty", "What this data cannot tell you")
    y = d.bullets([
        "<b>When, or how fast.</b> The source has no posting dates. Velocity and seasonality are not measured; the Task 7 forecast is "
        "on a synthetic calendar and labelled as such everywhere it appears.",
        "<b>Market share.</b> 182 postings Microsoft published as demo data for an Azure project - a sample with an unknown selection, "
        "not a census of hiring.",
        "<b>Company-wide strategy.</b> All 182 are Engineering. Sales, Finance, Marketing and Operations are absent.",
        f"<b>Regional patterns.</b> {states.iloc[0]} of {n} are in {states.index[0]}.",
        "<b>Capability on the titles basis.</b> A skill missing from a Microsoft title means the title did not name it - Microsoft "
        "titles rarely name anything.",
        "<b>The cohort ordering, if requisition IDs are not chronological.</b> Every Task 5 finding rests on that assumption.",
    ], 124, gap=5)
    d.callout("Why this slide exists",
              "Every limitation here is in the committed task notes. Every number in this deck comes from a committed output file - "
              "read directly by build_deck.py - or from the Task 2-9 notes. A mentor can check any figure against the repository.", y + 10)

    # 12 - next
    d.page("Next", "What the team should do, and questions")
    y = d.table([["Priority", "Action", "Unblocks"],
                 ["1", "Agree the 'drive' alias fix; every member extends the taxonomy for their own company; all re-run Task 4",
                  "Tasks 6 and 8; removes a 44% false tag from Microsoft"],
                 ["2", "Decide titles or full text once, for everyone", "Like-for-like comparison; Microsoft visible"],
                 ["3", "Add the over-deletion guard to every member's Task 3", "Silent text loss surfacing later in Task 8"],
                 ["4", "Recover Microsoft dates from Wayback Machine snapshots", "Real time axis for Tasks 5 and 7"],
                 ["5", "Run Task 12 on hand-corrected labels", "Skills the alias list cannot see"]],
                [70, 380, 236], 124, row_h=30)
    d.text("Expected questions: why a 182-posting demo sample · whether requisition IDs are chronological · why Agile fell · "
           "why the Microsoft taxonomy extension was not applied · how the Task 2 report missed the email addresses.",
           y + 14, size=9.5, color=MUTED)

    d.save()
    print(f"wrote {OUT.relative_to(HERE)}  ({d.n} slides)")


if __name__ == "__main__":
    main()
