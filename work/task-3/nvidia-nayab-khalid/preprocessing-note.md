# Preprocessing Note - NVIDIA

Member: Nayab Khalid
Company: NVIDIA
Task 3: NLP Preprocessing and Method Selection
Date: 2026-09-20

## Summary

1,745 NVIDIA postings were normalised, structurally parsed and tokenised. No rows were dropped.
The largest gain is coverage: seniority rose from 662 to 1,229 of 1,745 rows, and role function
from 878 to 1,743, both recovered from the title text that the source feed left unparsed.

| Measure | Result |
|---|---|
| Rows in / rows out | 1,745 / 1,745, none dropped |
| Titles altered by unicode normalisation | 121 |
| Titles carrying a qualifier segment | 1,201 of 1,745 |
| Tokens per title | min 2, median 5, max 9 |
| Distinct tokens in the vocabulary | 809 |
| Seniority coverage | 662 → **1,229** (+86%) |
| Role function coverage | 878 → **1,743** (99.9% of rows) |

## 1. The input, and the constraint that shapes everything

The Task 2 dataset carries **no job description text**. NVIDIA publishes through Workday, whose
Terms of Service prohibit automated collection (Task 1, section 3.1), and the openly licensed
source that does carry NVIDIA rows stores only title, location, URL and dates.

So the NLP input for this task is the **job title**: median 6 words, maximum 13. That single fact
determines the method.

## 2. Method selection

The task brief says to choose your own methods and libraries. Three decisions, each made because
titles are short:

### 2.1  No stemming, and almost no stopword removal

On a 500-word description, dropping function words and stemming costs nothing. On a six-word title
it destroys the signal. `Solutions Architect - AI Factory Deployment` has no words to spare.

A standard stemmer on this vocabulary produces `analysi`, `architectur` and `seri`, which are worse
than the plurals they replace. Instead there is a **controlled singularisation map** of 26 entries
covering the plurals that actually occur (`tools → tool`, `systems → system`, `libraries →
library`), and a stopword list of 11 genuine function words plus bare years such as `2027`.

### 2.2  Structural parsing rather than bag-of-words

NVIDIA titles follow a consistent grammar:

```
[seniority]  [role]  ,|-|–  [team / product / domain qualifier]
```

1,201 of 1,745 titles carry a separator, and the head noun of the first segment is drawn from a
small set: Engineer 964, Architect 314, Manager 313. Parsing that structure yields far more than
counting words does, so the pipeline splits each title into a core role and its qualifiers and
derives fields from each part.

### 2.3  Fill the gaps the source left

The raw feed populated `seniority_level` on 662 rows and `job_category` on 878. Both are largely
recoverable from the title, and doing so is the single largest quality gain available in this task.

### 2.4  Libraries

`pandas`, plus `re` and `unicodedata` from the standard library. spaCy and NLTK are not used, and
not merely because they were unavailable in the environment: both are built for sentence-level text,
their taggers and lemmatisers are trained on prose, and a six-word noun phrase gives them almost
nothing to work with. A rule set that is readable, auditable and reviewable by a teammate is worth
more here than a dependency that adds no accuracy. Every rule lives in a named constant at the top
of [`preprocess_nvidia.py`](preprocess_nvidia.py).

**Out of scope by design:** skill and technology extraction is Task 4. This task produces cleaned
text and structural fields only, so the boundary between the two stays clean.

## 3. The pipeline

| # | Stage | What it does |
|---|---|---|
| 1 | Read | Loads the Task 2 raw dataset |
| 2 | Unicode normalisation | NFKC, then maps typographic characters to ASCII: 91 en dashes, 19 em dashes, 3 non-breaking spaces, 1 non-breaking hyphen. Without this, `Engineer – Cloud` and `Engineer - Cloud` tokenise differently |
| 3 | Segment | Splits on `,`, ` - `, ` – `, ` — `, `\|` into a core role and its qualifiers |
| 4 | Role function | Matches the head noun of the core against 24 patterns, falling back to the full title |
| 5 | Seniority | Matches 9 ordered rank patterns; most specific wins, so `Senior Director` resolves to Director |
| 6 | Clean text | Strips rank words and punctuation, lowercases, collapses whitespace. `+ # -` are preserved for `C++`, `C#`, `multi-gpu` |
| 7 | Tokenise | Splits, drops stopwords and bare years, applies controlled singularisation |
| 8 | Flag repeats | Counts identical titles; 1,463 of 1,745 titles are unique |

Stage 4 runs **before** stage 5 on purpose: seniority needs to know whether `Lead` is this row's
head noun. See section 6.

## 4. Fields produced

Added to the 25 columns carried through from Task 2:

| Field | Description |
|---|---|
| `cleaned_description` | The cleaned title text. **Team schema field name**, used so cross-company joins in Task 6 work unchanged. For NVIDIA it derives from the title, not a description |
| `cleaned_title_core` | The cleaned core role, with qualifiers removed |
| `title_qualifiers` | JSON list of the team / product / domain segments |
| `n_qualifiers` | How many qualifier segments the title carried |
| `role_function` | Engineer, Architect, Manager, Lead, Scientist, … |
| `seniority_derived` | Intern, Junior, Senior, Staff, Lead, Principal, Distinguished, Director, Executive, Unspecified |
| `title_tokens` | JSON list of cleaned tokens, the NLP input for Task 4 |
| `n_tokens` | Token count |
| `title_repeat_count` | How many postings share this exact title |

## 5. Results

### Seniority

| Level | Postings |
|---|---|
| Senior | 1,081 |
| Unspecified | 516 |
| Principal | 57 |
| Junior | 38 |
| Director | 19 |
| Intern | 15 |
| Distinguished | 10 |
| Lead | 6 |
| Staff | 3 |

62% of NVIDIA's open roles are explicitly Senior or above. The 516 unspecified are titles that
genuinely carry no rank word, such as `Solutions Architect, Supercomputing`; they are left
unspecified rather than guessed at.

### Role function

| Function | Postings |
|---|---|
| Engineer | 964 |
| Architect | 314 |
| Manager | 313 |
| Lead | 24 |
| Scientist | 23 |
| Developer | 20 |
| Director | 18 |
| Researcher | 15 |
| Intern | 14 |
| Analyst | 12 |
| Specialist | 9 |
| Other | 2 |
| Designer, Counsel, Administrator, Technician, Planner | 11 combined |

### Most frequent tokens

| Token | Count | Share of postings |
|---|---|---|
| engineer | 971 | 55.6% |
| software | 486 | 27.9% |
| ai | 330 | 18.9% |
| manager | 319 | 18.3% |
| architect | 317 | 18.2% |
| solution | 211 | 12.1% |
| system | 197 | 11.3% |
| design | 129 | 7.4% |
| cloud | 118 | 6.8% |
| developer | 116 | 6.7% |
| infrastructure | 98 | 5.6% |
| learning | 90 | 5.2% |
| networking | 88 | 5.0% |

The full table of all 809 tokens is in `data/processed/nvidia_token_frequency_20260902.csv`.

## 6. Validation, and two bugs it caught

A 12-row random sample and a full review of the `Other` bucket were checked by hand. That found two
real errors, both now fixed.

**`Lead` was being read as a rank when it is a function.** NVIDIA has a family of roles whose head
noun is Lead or Leader: `Global Account Leader, Automotive`, `Segment Sales Leader`, `Business
Development Lead`. The rank stripper removed the word, leaving those titles with no role noun, so
24 postings fell into `Other` and their seniority was inflated to Lead. Fixed by matching role
function first and suppressing the Lead rank rule when Lead is the head noun, and by removing
`lead|leader` from the words stripped out of the cleaned text.

**New-graduate postings were not detected as junior.** The pattern required `new grad` adjacently,
so `New College Grad 2027` and `NVIDIA 2027 New College Graduate` were missed. Junior rose from 11
to 38 once fixed.

After both fixes, `Other` fell from 30 rows to 2. Those 2 are genuine graduate-programme postings
with no role noun at all (`Physical Design, VLSI - New College Grad 2027`), and are left as Other
rather than forced into a category.

## 7. Limitations

1. **A title is not a description.** This is the ceiling on everything downstream. Five tokens per
   title cannot carry what 500 words would.
2. **516 rows have no seniority signal.** Not an error, just absent from the source text. They are
   marked Unspecified, and any analysis that splits by seniority must say what it does with them.
3. **Rules are tuned to NVIDIA's title conventions.** Another company's titles would need their own
   review. This is a per-company pipeline, not a general one.
4. **`role_function` is not a job family.** It is the head noun. A Solutions Architect in sales and
   a Silicon Architect both read as Architect. Grouping into families belongs in Task 4.
5. **Qualifier segments are kept as raw text.** Normalising `AI Infra`, `AI Infrastructure` and
   `AI Factory` onto shared concepts is Task 4's job, not this one's.

## 8. Two points for the team

1. **The seniority vocabulary needs extending.** `docs/data-schema.md` lists Junior, Mid, Senior,
   Lead and Principal. NVIDIA's titles also carry Intern, Staff, Distinguished, Director and
   Executive. I have used the extended set and flagged it here rather than forcing real values into
   five buckets. It needs ratifying so all four members use the same list.
2. **`cleaned_description` means different things per member.** For members with description text it
   is preprocessed prose; for NVIDIA it is a preprocessed title. The column name is shared so the
   Task 6 joins work, but anything comparing text length, vocabulary size or token counts across
   companies will be comparing incomparable things unless it accounts for this.

## Files

| File | Rows | Contents |
|---|---|---|
| `data/processed/nvidia_postings_clean_20260902.csv` | 1,745 | Cleaned dataset, 34 columns |
| `data/processed/nvidia_token_frequency_20260902.csv` | 809 | Token frequency across the corpus |
| `preprocess_nvidia.py` | - | The pipeline, re-runnable from a clean checkout |

Reproduce with:

```bash
cd work/task-3/nvidia-nayab-khalid
python preprocess_nvidia.py
```
