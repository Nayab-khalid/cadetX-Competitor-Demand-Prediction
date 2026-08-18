# Shared dataset schema

**Alignment lock #1.** One row = one job posting. Every member's dataset uses these column names,
in this order, with these dtypes. If a source does not provide a field, keep the column and leave it
empty - do not drop or rename it.

## Required

| Column | Type | Format / rule | Why |
|---|---|---|---|
| `job_id` | string | unique within your file; prefix with company, e.g. `nvidia_00123` | unique identifier |
| `company_name` | string | exactly one value per file, title case: `NVIDIA` | competitor comparison |
| `job_title` | string | as posted, whitespace trimmed | role classification, seniority |
| `job_description` | string | full text, newlines preserved | the NLP input |
| `posting_date` | date | ISO-8601 `YYYY-MM-DD` | velocity, trends, forecasting |
| `location` | string | as posted; `Remote` when stated | regional patterns |
| `job_url` | string | absolute URL | traceability and validation |

## Recommended

Add these when the source supports it - they make Tasks 4 to 8 much stronger.

| Column | Type | Notes |
|---|---|---|
| `employment_type` | string | full-time / part-time / contract / internship |
| `department` / `job_category` | string | Engineering, AI, Data, Product, ... |
| `seniority_level` | string | Junior / Mid / Senior / Lead / Principal |
| `extracted_skills` | JSON list as string | `["Python","CUDA","PyTorch"]` - canonical names only |
| `skill_categories` | JSON list as string | from `shared/taxonomy/skills.yaml` |
| `tech_stack_tags` | JSON list as string | AWS, Kubernetes, Triton, ... |
| `cleaned_description` | string | Task 3 output |
| `posting_week` | string | ISO week `2026-W34` |
| `posting_month` | string | `2026-08` |
| `scraped_date` / `updated_at` | date | freshness, reposting detection |
| `job_status` | string | active / closed |
| `salary_range` | string | only when publicly posted |
| `company_industry` / `sector` | string | grouping and benchmarking |
| `role_cluster_id` | int | Task 8 clustering |
| `embedding_vector` | JSON list as string | store separately if large |
| `skill_frequency_vector` | JSON list as string | vectorised skills |
| `emerging_skill_flag` | bool | new or fast-rising skill present |
| `hiring_velocity_bucket` | string | low / medium / high |

## Rules that bite later

- **Never** collect a person's name, email, phone number or any recruiter identity - not even in a
  spare column. It fails the ethics criterion outright.
- Encoding is UTF-8. Files are CSV with a header row, comma separated, quoted where needed.
- Keep raw untouched. Cleaning happens in Task 3 into a new file, never in place.
- Duplicates: reposts are real signal. Keep them, but flag them - do not silently deduplicate.

## Example

| job_id | company_name | job_title | posting_date | location | job_url |
|---|---|---|---|---|---|
| nvidia_00001 | NVIDIA | Senior Deep Learning Engineer | 2026-05-12 | Santa Clara, CA | https://... |
