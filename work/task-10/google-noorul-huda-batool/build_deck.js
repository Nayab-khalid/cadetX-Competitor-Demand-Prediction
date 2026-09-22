const pptxgen = require("pptxgenjs");

const NAVY = "1E2761";
const ICE = "CADCFC";
const WHITE = "FFFFFF";
const GBLUE = "4285F4";
const GGREEN = "34A853";
const GYELLOW = "FBBC05";
const GRED = "EA4335";
const INK = "212121";
const MUTED = "5F6368";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
const W = 13.33, H = 7.5;

function darkTitle(title, kicker) {
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText(kicker.toUpperCase(), { x: 0.7, y: 2.55, w: 11.9, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, color: ICE, charSpacing: 2 });
  s.addText(title, { x: 0.7, y: 2.95, w: 11.9, h: 1.8, isTextBox: true, margin: 0, fontFace: "Cambria", fontSize: 40, bold: true, color: WHITE });
  return s;
}

function contentSlide(title) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText(title, { x: 0.6, y: 0.4, w: 12.1, h: 0.8, isTextBox: true, margin: 0, fontFace: "Cambria", fontSize: 30, bold: true, color: NAVY });
  return s;
}

function statCircle(s, x, y, d, num, label, color) {
  s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color }, line: { type: "none" } });
  s.addText(num, { x, y: y + d * 0.18, w: d, h: d * 0.5, isTextBox: true, margin: 0, align: "center", fontFace: "Calibri", fontSize: d > 1.5 ? 26 : 20, bold: true, color: WHITE });
  s.addText(label, { x: x - 0.3, y: y + d + 0.08, w: d + 0.6, h: 0.5, isTextBox: true, margin: 0, align: "center", fontFace: "Calibri", fontSize: 11, color: INK });
}

// ---------- Slide 1: Title ----------
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 0.35, h: H, fill: { color: GBLUE }, line: { type: "none" } });
  s.addText("GOOGLE HIRING INTELLIGENCE", { x: 0.9, y: 2.05, w: 11.5, h: 0.5, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, color: ICE, charSpacing: 3 });
  s.addText("Forecasting Competitor Demand from Job Postings", { x: 0.9, y: 2.55, w: 11.5, h: 1.6, isTextBox: true, margin: 0, fontFace: "Cambria", fontSize: 38, bold: true, color: WHITE });
  s.addText("Company track: Google  |  Job-Posting Intelligence Internship Programme", { x: 0.9, y: 4.1, w: 11.5, h: 0.5, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 16, color: ICE });
  s.addText("Noor Ul Huda", { x: 0.9, y: 6.4, w: 6, h: 0.5, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 18, bold: true, color: WHITE });
  s.addText("Tasks 3 - 12  |  Final Presentation & Mentor Review", { x: 0.9, y: 6.85, w: 8, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12, color: ICE });
}

// ---------- Slide 2: Problem & Business Value ----------
{
  const s = contentSlide("The Problem & Why It Matters");
  s.addText("Companies read the market backward-looking - news, financials, assumptions. Job postings show what a company plans to do next.", {
    x: 0.6, y: 1.25, w: 6.2, h: 1.5, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, color: INK,
  });
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 2.9, w: 6.2, h: 3.7, rectRadius: 0.08, fill: { color: "F4F6FB" }, line: { type: "none" } });
  s.addText("This project turns Google's own job postings into a forecast of:", { x: 0.9, y: 3.15, w: 5.6, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13, bold: true, color: NAVY });
  const bullets = [
    "Skill & technology demand trends",
    "Hiring velocity, growth and slowdown signals",
    "Competitor / subsidiary positioning",
    "6-month-ahead hiring demand forecasts",
  ];
  s.addText(bullets.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < bullets.length - 1, paraSpaceAfter: 10 } })),
    { x: 0.9, y: 3.65, w: 5.6, h: 2.7, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14 });

  statCircle(s, 7.6, 1.3, 1.7, "4", "Business functions\nusing this: Strategy,\nHR, PM, CEO/CTO", GBLUE);
  statCircle(s, 9.9, 1.3, 1.7, "1,127", "Unique Google/\nYouTube postings\nanalyzed", GGREEN);
  statCircle(s, 7.6, 3.9, 1.7, "97", "Skills in the\nshared taxonomy", GYELLOW);
  statCircle(s, 9.9, 3.9, 1.7, "6mo", "Forecast horizon\n(team-aligned)", GRED);
}

// ---------- Slide 3: Pipeline overview ----------
{
  const s = contentSlide("End-to-End Pipeline (Tasks 1 - 9)");
  const steps = [
    ["1-2", "Sources &\nCollection", GBLUE],
    ["3", "NLP\nPreprocessing", GGREEN],
    ["4", "Skill\nExtraction", GYELLOW],
    ["5", "Trend\nAnalysis", GRED],
    ["6", "Competitor\nComparison", GBLUE],
    ["7", "Demand\nForecasting", GGREEN],
    ["8", "Similarity\nScoring", GYELLOW],
    ["9", "Insight\nReport", GRED],
  ];
  const startX = 0.6, gap = 1.52, boxW = 1.3, boxH = 1.3, y = 2.6;
  steps.forEach((st, i) => {
    const x = startX + i * gap;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: boxW, h: boxH, rectRadius: 0.12, fill: { color: st[2] }, line: { type: "none" } });
    s.addText(st[0], { x, y: y + 0.12, w: boxW, h: 0.4, isTextBox: true, margin: 0, align: "center", fontFace: "Calibri", fontSize: 16, bold: true, color: WHITE });
    s.addText(st[1], { x, y: y + 0.5, w: boxW, h: 0.7, isTextBox: true, margin: 0, align: "center", fontFace: "Calibri", fontSize: 10.5, color: WHITE });
    if (i < steps.length - 1) {
      s.addText("→", { x: x + boxW, y: y + 0.35, w: gap - boxW, h: 0.6, isTextBox: true, margin: 0, align: "center", fontFace: "Calibri", fontSize: 20, bold: true, color: MUTED });
    }
  });
  s.addText("Each stage's output is a versioned CSV/JSON that the next stage reads - fully reproducible end to end, and the same code runs against any of the team's four companies.", {
    x: 0.6, y: 4.4, w: 11.5, h: 1.0, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, color: MUTED, italic: true,
  });
  s.addText("Folder layout: Task3_NLP_Preprocessing / Task4_Skill_Extraction... / Task5_Hiring_Trend_Analysis / Task6_Competitor_Comparison / Task7_Demand_Forecasting / Task8_Company_Similarity_Scoring / Task9_Insight_Generation_Reporting", {
    x: 0.6, y: 5.9, w: 11.9, h: 1.0, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 11, color: MUTED,
  });
}

// ---------- Slide 4: Data & Legal foundation ----------
{
  const s = contentSlide("Data Source & Legal Foundation (Tasks 1-2)");
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 1.3, w: 5.9, h: 5.4, rectRadius: 0.08, fill: { color: "F4F6FB" }, line: { type: "none" } });
  s.addText("Dataset", { x: 0.95, y: 1.55, w: 5.2, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, bold: true, color: NAVY });
  const dataBullets = [
    "Kaggle “Google Job Skills” dataset",
    "Originally scraped from Google Careers (by dataset creator), license CC BY-NC-SA 4.0",
    "1,250 raw postings → 1,127 after removing 123 exact duplicates",
    "Fields: Company, Title, Category, Location, Responsibilities, Min/Preferred Qualifications",
  ];
  s.addText(dataBullets.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < dataBullets.length - 1, paraSpaceAfter: 8 } })),
    { x: 0.95, y: 2.05, w: 5.2, h: 2.2, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12.5 });
  s.addText("Legal / Ethical Checks", { x: 0.95, y: 4.35, w: 5.2, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, bold: true, color: NAVY });
  const legalBullets = [
    "Academic / non-commercial use only, source attributed",
    "No independent scraping of Google Careers performed",
    "No personal or sensitive data collected",
  ];
  s.addText(legalBullets.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < legalBullets.length - 1, paraSpaceAfter: 8 } })),
    { x: 0.95, y: 4.85, w: 5.2, h: 1.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12.5 });

  s.addShape(pres.ShapeType.roundRect, { x: 6.85, y: 1.3, w: 5.9, h: 5.4, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("Known Limitation", { x: 7.2, y: 1.6, w: 5.2, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, bold: true, color: GYELLOW });
  s.addText("The dataset has no real posting-date field. This was not caught in Tasks 1-2.", {
    x: 7.2, y: 2.1, w: 5.2, h: 0.9, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13, color: WHITE,
  });
  s.addText("Tasks 5 & 7 need a time series, so Task 3 adds a seeded, reproducible SIMULATED posting_date (2023-2024), flagged in every downstream file with posting_date_is_simulated = True.", {
    x: 7.2, y: 3.1, w: 5.2, h: 1.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13, color: ICE,
  });
  s.addText("Trend & forecast results below demonstrate the methodology; absolute values are not real Google hiring activity.", {
    x: 7.2, y: 5.9, w: 5.2, h: 0.7, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 11.5, italic: true, color: ICE,
  });
}

// ---------- Slide 5: NLP + Skill Extraction ----------
{
  const s = contentSlide("NLP Preprocessing & Skill Extraction (Tasks 3-4)");
  s.addText("Method", { x: 0.6, y: 1.25, w: 5.7, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, bold: true, color: NAVY });
  const m1 = [
    "Clean → tokenize → remove stopwords → lemmatize (NLTK)",
    "Symbol-aware cleaning keeps c++, c#, node.js intact",
    "97-skill shared taxonomy across 9 categories (regex-based)",
    "Taxonomy format reusable as-is by all 4 companies on the team",
  ];
  s.addText(m1.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < m1.length - 1, paraSpaceAfter: 9 } })),
    { x: 0.6, y: 1.7, w: 5.7, h: 2.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13.5 });

  statCircle(s, 0.6, 4.6, 1.5, "99.2%", "Postings with\n>=1 skill matched", GGREEN);
  statCircle(s, 2.5, 4.6, 1.5, "7.2", "Avg skills\nmatched/posting", GBLUE);
  statCircle(s, 4.4, 4.6, 1.5, "139", "Avg tokens\nper posting", GYELLOW);

  s.addText("Top Skills by Coverage", { x: 6.9, y: 1.25, w: 5.8, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, bold: true, color: NAVY });
  const skillLabels = ["bachelors_degree", "sales", "cross_functional_collab.", "marketing", "strategic_planning", "stakeholder_mgmt", "google_cloud", "cs_degree"];
  const skillVals = [74.45, 42.32, 37.62, 34.61, 30.43, 29.81, 24.13, 23.6];
  s.addChart(pres.ChartType.bar, [{ name: "% of postings", labels: skillLabels, values: skillVals }], {
    x: 6.9, y: 1.7, w: 5.8, h: 5.2,
    barDir: "bar", chartColors: [GBLUE], showTitle: false, showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: INK, dataLabelFontSize: 10,
    catAxisLabelColor: INK, catAxisLabelFontSize: 10, valAxisLabelColor: MUTED, valAxisLabelFontSize: 9,
    valAxisTitle: "% of postings", showValAxisTitle: true, valGridLine: { color: "E0E0E0", size: 0.75 }, catGridLine: { style: "none" },
  });
}

// ---------- Slide 6: Hiring Trend Analysis ----------
{
  const s = contentSlide("Hiring Trend Analysis (Task 5)");
  const monthly = [["2023-01",57],["2023-02",36],["2023-03",70],["2023-04",52],["2023-05",50],["2023-06",46],["2023-07",64],["2023-08",39],["2023-09",49],["2023-10",57],["2023-11",44],["2023-12",40],["2024-01",46],["2024-02",47],["2024-03",46],["2024-04",39],["2024-05",45],["2024-06",53],["2024-07",34],["2024-08",47],["2024-09",43],["2024-10",53],["2024-11",31],["2024-12",39]];
  s.addChart(pres.ChartType.line, [{ name: "Postings/month", labels: monthly.map(m => m[0]), values: monthly.map(m => m[1]) }], {
    x: 0.6, y: 1.25, w: 8.3, h: 4.6,
    chartColors: [GBLUE], showTitle: true, title: "Monthly Postings (simulated calendar)", titleFontSize: 13, titleColor: NAVY,
    showLegend: false, lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 5,
    catAxisLabelColor: MUTED, catAxisLabelFontSize: 8, catAxisLabelRotate: 90,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 9, valGridLine: { color: "E0E0E0", size: 0.75 }, catGridLine: { style: "none" },
  });
  s.addShape(pres.ShapeType.roundRect, { x: 9.15, y: 1.25, w: 3.55, h: 5.7, rectRadius: 0.08, fill: { color: "F4F6FB" }, line: { type: "none" } });
  s.addText("Signals", { x: 9.45, y: 1.5, w: 3, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, bold: true, color: NAVY });
  const signals = [
    "Avg 47 postings/month",
    "Growing: Technical Solutions (+73%), Partnerships (+35%)",
    "Growing skills: data_mining, virtualization, ruby, rest_api",
    "Declining: Manufacturing & Supply Chain, Administrative, Legal & Gov't Relations",
  ];
  s.addText(signals.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < signals.length - 1, paraSpaceAfter: 10 } })),
    { x: 9.45, y: 2.0, w: 3.0, h: 4.7, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 11.5 });
  s.addNotes("Seasonal heatmap and category-level trend charts are in Task5_Hiring_Trend_Analysis/visuals/.");
}

// ---------- Slide 7: Competitor Comparison ----------
{
  const s = contentSlide("Competitor Comparison: Google vs YouTube (Task 6)");
  s.addText("Scope note: this member's data covers Google/YouTube only. The framework auto-merges other companies from competitor_data/ the moment teammates share their Task 4 output.", {
    x: 0.6, y: 1.2, w: 11.9, h: 0.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12, italic: true, color: MUTED,
  });

  const overviewRows = [
    [{ text: "Company", options: { bold: true, color: WHITE, fill: { color: NAVY } } }, { text: "Postings", options: { bold: true, color: WHITE, fill: { color: NAVY } } }, { text: "Categories", options: { bold: true, color: WHITE, fill: { color: NAVY } } }, { text: "Locations", options: { bold: true, color: WHITE, fill: { color: NAVY } } }],
    ["Google", "1,107", "23", "92"],
    ["YouTube", "20", "10", "8"],
  ];
  s.addTable(overviewRows, { x: 0.6, y: 2.0, w: 5.2, h: 1.4, fontFace: "Calibri", fontSize: 12, color: INK, border: { type: "solid", color: "E0E0E0", pt: 0.75}, autoPage: false, valign: "middle", align: "center" });

  s.addText("Tech-Stack Mix (% of skill mentions)", { x: 0.6, y: 3.7, w: 5.2, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13, bold: true, color: NAVY });
  s.addChart(pres.ChartType.bar, [
    { name: "Google", labels: ["Business/Soft", "Cloud/Infra", "Data/ML", "Programming"], values: [47.37, 7.17, 4.31, 14.22] },
    { name: "YouTube", labels: ["Business/Soft", "Cloud/Infra", "Data/ML", "Programming"], values: [51.94, 0.0, 8.53, 15.50] },
  ], {
    x: 0.6, y: 4.1, w: 5.5, h: 2.85, barDir: "col", barGrouping: "clustered",
    chartColors: [GBLUE, GYELLOW], showLegend: true, legendPos: "b", legendFontSize: 9,
    catAxisLabelColor: MUTED, catAxisLabelFontSize: 8, valAxisLabelColor: MUTED, valAxisLabelFontSize: 8,
    valGridLine: { color: "E0E0E0", size: 0.75 }, catGridLine: { style: "none" }, showTitle: false,
  });

  s.addShape(pres.ShapeType.roundRect, { x: 6.5, y: 2.0, w: 6.2, h: 4.9, rectRadius: 0.08, fill: { color: "F4F6FB" }, line: { type: "none" } });
  s.addText("Reading the gap", { x: 6.8, y: 2.25, w: 5.6, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, bold: true, color: NAVY });
  const compBullets = [
    "Skill-vocabulary overlap (Jaccard): 0.40 - only ~40% of skills shared",
    "Tech-stack shape (cosine): 0.99 - almost identical profile",
    "YouTube: 0 Cloud & Infra mentions vs Google's 7.2% - directional signal, small sample (n=20)",
    "Interpretation: YouTube isn't hiring differently from Google - it's hiring with a smaller vocabulary inside the same shape",
  ];
  s.addText(compBullets.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < compBullets.length - 1, paraSpaceAfter: 12 } })),
    { x: 6.8, y: 2.75, w: 5.6, h: 4.2, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13 });
}

// ---------- Slide 8: Demand Forecasting ----------
{
  const s = contentSlide("Demand Forecasting: Next 6 Months (Task 7)");
  const hist = [["2024-07",34],["2024-08",47],["2024-09",43],["2024-10",53],["2024-11",31],["2024-12",39]];
  const fc = [["2025-01",39.7],["2025-02",39.1],["2025-03",38.6],["2025-04",38.0],["2025-05",37.5],["2025-06",36.9]];
  const allLabels = hist.map(h => h[0]).concat(fc.map(f => f[0]));
  const actualVals = hist.map(h => h[1]).concat(fc.map(() => null));
  const forecastVals = hist.map(() => null).slice(0, -1).concat([hist[hist.length - 1][1]]).concat(fc.map(f => f[1]));
  s.addChart(pres.ChartType.line, [
    { name: "Actual", labels: allLabels, values: actualVals },
    { name: "Forecast", labels: allLabels, values: forecastVals },
  ], {
    x: 0.6, y: 1.3, w: 7.6, h: 4.8,
    chartColors: [GBLUE, GRED], showLegend: true, legendPos: "b", legendFontSize: 10,
    lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 5,
    catAxisLabelColor: MUTED, catAxisLabelFontSize: 9, valAxisLabelColor: MUTED, valAxisLabelFontSize: 9,
    valGridLine: { color: "E0E0E0", size: 0.75 }, catGridLine: { style: "none" }, showTitle: false,
  });
  s.addShape(pres.ShapeType.roundRect, { x: 8.5, y: 1.3, w: 4.2, h: 5.6, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("Method: Holt's Linear\n(damped trend)", { x: 8.8, y: 1.55, w: 3.6, h: 0.7, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, bold: true, color: GYELLOW });
  const fcBullets = [
    "24 monthly points → too short for stable ARIMA order selection",
    "Damping avoids unrealistic runaway extrapolation",
    "Shared 6-month horizon across the team's 4 companies",
    "Overall demand: ~40 → ~37 postings/month, flat-to-mild decline",
  ];
  s.addText(fcBullets.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: WHITE, breakLine: i < fcBullets.length - 1, paraSpaceAfter: 12 } })),
    { x: 8.8, y: 2.35, w: 3.6, h: 4.3, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12.5 });
}

// ---------- Slide 9: Company Similarity ----------
{
  const s = contentSlide("Company Similarity Scoring (Task 8)");
  s.addText("Three complementary similarity views", { x: 0.6, y: 1.25, w: 12, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, bold: true, color: NAVY });

  const cards = [
    ["Jaccard\nSkill Overlap", "0.40", "Exact skill-vocabulary overlap", GBLUE],
    ["Cosine\nSkill Profile", "0.99", "Tech-stack “shape” similarity", GGREEN],
    ["Cosine\nTF-IDF Text", "0.79", "Posting-language similarity", GYELLOW],
  ];
  const cw = 3.7, gap2 = 0.35, x0 = 0.6, y0 = 1.85;
  cards.forEach((c, i) => {
    const x = x0 + i * (cw + gap2);
    s.addShape(pres.ShapeType.roundRect, { x, y: y0, w: cw, h: 2.5, rectRadius: 0.1, fill: { color: "F4F6FB" }, line: { type: "none" } });
    s.addText(c[0], { x: x + 0.25, y: y0 + 0.2, w: cw - 0.5, h: 0.7, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 14, bold: true, color: NAVY });
    s.addText(c[1], { x: x + 0.25, y: y0 + 0.85, w: cw - 0.5, h: 0.9, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 36, bold: true, color: c[3] });
    s.addText(c[2], { x: x + 0.25, y: y0 + 1.8, w: cw - 0.5, h: 0.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 11.5, color: MUTED });
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.65, w: 12.1, h: 2.15, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("Key read: the gap between a low Jaccard score and a near-1.0 profile-cosine score is itself the insight - YouTube isn't a differently-postured employer than Google, it's a smaller-vocabulary one operating inside the same tech-stack shape. Ready to extend to all 4 companies via competitor_data/.", {
    x: 0.95, y: 4.95, w: 11.4, h: 1.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, color: WHITE,
  });
}

// ---------- Slide 10: Insights & Strategy ----------
{
  const s = contentSlide("Google's Hiring Strategy & Position (Task 9)");
  const rows = [
    ["Cloud-first technical identity", "Google Cloud dominates named platform skills; no competing cloud platform appears in the taxonomy matches.", GBLUE],
    ["Go-to-market weight", "Sales, Marketing & Partnerships are among the largest and fastest-growing categories - commercial expansion alongside product work.", GGREEN],
    ["Reliability/infra tilt in growth", "virtualization, rest_api and Technical Solutions growing fastest - a maturing cloud/infra business, not early-stage feature-building.", GYELLOW],
    ["Centralized subsidiary hiring", "YouTube tracks Google's tech-stack shape almost exactly despite a much smaller, narrower posting set.", GRED],
  ];
  let y = 1.35;
  rows.forEach(r => {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 0.12, h: 1.15, fill: { color: r[2] }, line: { type: "none" } });
    s.addText(r[0], { x: 1.0, y: y - 0.02, w: 11.6, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 15, bold: true, color: NAVY });
    s.addText(r[1], { x: 1.0, y: y + 0.4, w: 11.6, h: 0.7, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12.5, color: INK });
    y += 1.4;
  });
}

// ---------- Slide 11: Limitations & Next Steps ----------
{
  const s = contentSlide("Limitations & Next Steps");
  s.addText("Limitations", { x: 0.6, y: 1.25, w: 5.9, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 16, bold: true, color: NAVY });
  const lims = [
    "No real posting-date field → trend/forecast use a documented, seeded synthetic calendar",
    "Single-source dataset → competitor comparison validated on Google/YouTube only so far",
    "Regex/keyword skill extraction can miss unanticipated phrasing",
    "YouTube's small sample (n=20) makes its metrics directional, not confirmatory",
  ];
  s.addText(lims.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < lims.length - 1, paraSpaceAfter: 12 } })),
    { x: 0.6, y: 1.75, w: 5.9, h: 4.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13.5 });

  s.addText("Next Steps (Tasks 11-12, optional)", { x: 6.85, y: 1.25, w: 5.9, h: 0.4, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 16, bold: true, color: NAVY });
  const next = [
    "Automated pipeline: scheduled end-to-end run, Tasks 3-9 chained",
    "Fine-tuned skill-extraction model (spaCy NER) to raise recall beyond the regex taxonomy",
    "Merge in the other 3 companies' data via competitor_data/ for the full team comparison",
    "Replace simulated dates with real collection timestamps once a live source is approved",
  ];
  s.addText(next.map((b, i) => ({ text: b, options: { bullet: { code: "25AA" }, color: INK, breakLine: i < next.length - 1, paraSpaceAfter: 12 } })),
    { x: 6.85, y: 1.75, w: 5.9, h: 4.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 13.5 });
}

// ---------- Slide 12: Thank you ----------
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 0.35, h: H, fill: { color: GBLUE }, line: { type: "none" } });
  s.addText("Thank You", { x: 0.9, y: 2.7, w: 11.5, h: 1.2, isTextBox: true, margin: 0, fontFace: "Cambria", fontSize: 44, bold: true, color: WHITE });
  s.addText("Questions & Discussion", { x: 0.9, y: 3.7, w: 11.5, h: 0.6, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 18, color: ICE });
  s.addText("Noor Ul Huda  |  Google Hiring Intelligence  |  Full workspace: Task3-Task9 folders, GitHub-ready", {
    x: 0.9, y: 6.6, w: 11.5, h: 0.5, isTextBox: true, margin: 0, fontFace: "Calibri", fontSize: 12, color: ICE,
  });
}

pres.writeFile({ fileName: "Google_Hiring_Intelligence_Final_Presentation.pptx" }).then(() => {
  console.log("Deck written.");
});
