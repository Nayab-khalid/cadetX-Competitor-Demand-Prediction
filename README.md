# Competitor Demand Prediction Using Job Postings

CadetX Virtual Work Experience. A team of four data scientists analysing job-posting data from four
technology companies to predict competitor demand, skill trends and market direction.

## Objective

Job postings show what a company is planning, not what it has already done. This project collects
public job-posting data for four companies, applies NLP to extract skills and roles, analyses hiring
trends, forecasts future demand, and compares the four companies within one shared framework.

Each member is the specialist for one company. All four datasets follow the same schema and the same
analysis standards so the results can be compared directly.

## Team

| Member | Company | Folder |
|---|---|---|
| Nayab Khalid | NVIDIA | `nvidia-nayab-khalid` |
| Noorul Huda Batool | Google | `google-noorul-huda-batool` |
| Arham Malik | Microsoft | `microsoft-arham-malik` |
| Abdal Farid | Anthropic | `anthropic-abdal-farid` |

## Tasks

| # | Task | Folder | Status |
|---|---|---|---|
| 1 | Understanding Data Sources and Legal | [work/task-1](work/task-1) | In progress |
| 2 | Data Collection | - | Not started |
| 3 | NLP Preprocessing and Method Selection | - | Not started |
| 4 | Skill Extraction and Feature Engineering | - | Not started |
| 5 | Hiring Trend Analysis | - | Not started |
| 6 | Competitor Comparison | - | Not started |
| 7 | Demand Forecasting | - | Not started |
| 8 | Company Similarity Scoring | - | Not started |
| 9 | Insight Generation and Reporting | - | Not started |
| 10 | Final Presentation and Mentor Review | - | Not started |
| 11 | Optional: Automated Pipeline | - | Optional |
| 12 | Optional: Fine-Tune a Skill Extraction Model | - | Optional |

Tasks 11 and 12 are optional and will be attempted only if the team has time after Task 10.

## Repository structure

```
work/                  one folder per task; inside it one folder per member
minutes-of-meeting/    weekly meeting minutes, one folder per sprint (1 to 12)
docs/                  programme brief, dataset schema, legal checklist, analysis conventions
shared/                standards all four members must follow (schema, skill taxonomy, config)
scripts/               dataset validator
```

Each member submits their work inside their own folder within the relevant task folder. Nobody edits
another member's folder.

## Requirements the team must fulfil

- Each member collects and analyses job-posting data for their own company.
- All four datasets use the same fields and formats, defined in [docs/data-schema.md](docs/data-schema.md).
- All four members use the same skill taxonomy, time period and forecast horizon, so the companies
  can be compared fairly.
- A weekly meeting is held on Microsoft Teams. The Scrum Leader of the week uploads the minutes.
- The four roles (Scrum Leader, Data Quality Lead, Documentation Lead, Technical Lead) rotate every
  week. The rota is in [minutes-of-meeting/role-rota.md](minutes-of-meeting/role-rota.md).
- Every task ends with the work uploaded to this repository.

## Ground rules

- Only legally approved data sources are used. Terms of Service and robots.txt are checked and
  recorded before any data is collected. See [docs/legal-checklist.md](docs/legal-checklist.md).
- No personal or sensitive data is collected at any point. This includes names, email addresses,
  phone numbers and recruiter details.
- Copyright is respected. Licences and attribution requirements are documented for every source.
- All work is committed to this repository, so each member's contribution is visible.

## Submission

The URL of this repository is submitted in the CadetX portal at the end of each task.

The full programme brief is in [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md).
Working conventions are in [CONTRIBUTING.md](CONTRIBUTING.md).
