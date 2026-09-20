# Skill Extraction Method Note - NVIDIA

Member: Nayab Khalid
Company: NVIDIA
Task 4: Skill Extraction and Feature Engineering
Date: 2026-09-20

## Summary

Skills were extracted from 1,745 NVIDIA job titles by dictionary matching against the shared
taxonomy. The headline result is not the extraction itself but what it exposed: **the shared
taxonomy as written covered only 21.2% of NVIDIA's postings**, because it was built for job
descriptions and my source carries only titles. Extending it to the specialisation vocabulary that
titles actually use raised coverage to 72.0%.

| Measure | Start | After extension and validation fixes |
|---|---|---|
| Canonical skills in the taxonomy | 59 | **93** |
| Postings matching at least one skill | 370 (21.2%) | **1,256 (72.0%)** |
| Mean skills per posting | 0.24 | **1.03** |
| Total skill mentions | 419 | **1,793** |
| Distinct skills matched | 27 | **59** |

## 1. The problem with the taxonomy

The starter taxonomy lists tools: AWS, Docker, Spark, TensorFlow, Tableau. Those words belong in a
job description. A job title names the **specialisation**, not the tool. NVIDIA advertises
`Senior Physical Design Engineer`, never `Verilog, Synopsys, PrimeTime`.

Measured against the 1,745 NVIDIA titles, 32 of the 59 taxonomy skills never matched once: SQL,
Java, Scala, TensorFlow, scikit-learn, Spark, Kafka, Airflow, dbt, AWS, Azure, GCP, Docker,
Terraform, MLflow, Tableau, Power BI, A/B Testing, Statistics, RAG, RLHF and others. This is not a
statement about NVIDIA's technology; it is a statement about what fits in a job title.

## 2. What I added, and why

34 canonical skills, in a new `silicon_design` category plus additions to existing ones. They are
the specialisation vocabulary titles carry, and they are skills in a hiring-intelligence sense:
they say what the team builds.

| Area | Added |
|---|---|
| `silicon_design` (new) | Physical Design, RTL Design, Silicon Verification, SoC Design, Analog and Mixed Signal, Signal and Power Integrity, Design for Test, Design Automation, CPU Architecture, GPU Architecture |
| Systems | Firmware, Kernel and Drivers, Compilers, Networking, DPU and Offload, Datacenter Systems, Storage Systems, Performance Engineering |
| Applied AI | Generative AI, Agentic AI, Inference and Serving, Autonomous Vehicles, Digital Twin and Simulation, Graphics and Rendering, Healthcare AI, Speech and Audio |
| Practice and go-to-market | Cloud Infrastructure, Site Reliability, Cybersecurity, Test Automation, Solutions Architecture, Developer Relations, Technical Program Management, Business Development |

Role words are deliberately **not** skills. `engineer`, `manager`, `architect` and `director` are
`role_function`, derived in Task 3. Letting them into the skill space would make every posting look
identical.

All additions went into `shared/taxonomy/skills.yaml` with a dated comment block explaining the
reasoning, per the governance rule in `docs/skill-taxonomy.md`. **They need team ratification**, and
that is the main thing I am bringing to the sprint meeting.

## 3. Method

Dictionary matching of canonical names and aliases against the cleaned title text from Task 3, with
three rules that exist because the input is a title:

1. **Longest alias wins.** `gpu architecture` must not also register as a bare `gpu`, and
   `computer vision` must not register as `vision`. Aliases are sorted by length and a matched span
   is consumed, so no shorter term can claim it.
2. **Blocked single letters.** `title_match_blocklist: [r, c]` in the taxonomy. Both were measured,
   not assumed: `r` matched **R&D** in 9 postings once punctuation was stripped, and `c` matched the
   `c` inside `c++` in 11, double-counting C and C++.
3. **No inference.** A title reading `Senior Software Engineer` and nothing else gets no skill.
   Guessing that a software engineer at NVIDIA probably knows C++ would manufacture data.

Libraries: `pandas`, `pyyaml`, and `re` from the standard library. The taxonomy is the single source
of truth; the script contains no skill list of its own.

## 4. Validation

20 postings were checked by hand against their extracted skills. That found one false positive and
one large miss, both fixed.

**False positive.** `Senior Design Automation Engineer, Applied AI` was tagged Test Automation,
because `automation` was an alias of it. Design Automation is EDA tooling, a different thing
entirely. The bare alias was removed and Design Automation added as its own silicon skill. Test
Automation fell from 36 matches to 14, which is the honest number.

**Large miss.** `Senior Solutions Architect, AI Infrastructure` matched nothing, because the
taxonomy had `solutions architecture` but titles say `solutions architect`. That one missing word
form cost **192 postings**, 11% of the corpus, and made it the largest single skill once fixed.

Rare misses were left as candidates rather than fixed: silicon photonics (2 postings), NeMo (3),
OpenBMC (2), linear algebra (1). Adding a canonical skill for a term seen twice would inflate the
taxonomy for no analytical gain.

Coverage across the four passes: 21.2% → 63.5% after the extension → 67.2% after adding Cloud
Infrastructure and Site Reliability → **72.0%** after the validation fixes.

## 5. A bias I had to correct

The emerging-skill flag compares the first half of the window with the second. Run naively it made
almost everything look like it was declining, and the reason is in the Task 2 data:
**`posting_date` is a first-seen proxy, so every posting already open at the first observation is
stamped with that date** - 395 of 1,745 postings, 23% of the corpus, all landing in the first half.

The trend basis therefore excludes the first observation entirely, comparing 641 postings against
709. Nothing else in the task uses that exclusion. Before the fix, Datacenter Systems appeared to
fall 82 → 36; after it, 49 → 36, which is a real but far milder decline.

## 6. Results

### Where NVIDIA's hiring sits

| Category | Skill mentions |
|---|---|
| hardware_systems | 629 |
| research_domains | 334 |
| product_process | 269 |
| silicon_design | 256 |
| cloud_infra | 147 |
| mlops_devops | 119 |
| languages | 25 |
| ml_frameworks | 14 |

Hardware and silicon together account for 885 of 1,793 mentions, just under half. ML frameworks,
the thing most people associate with NVIDIA, account for 14. NVIDIA is hiring the people who build
the machine, not the people who use it.

### Top 12 skills

| Rank | Skill | Category | Postings | Share |
|---|---|---|---|---|
| 1 | Solutions Architecture | product_process | 192 | 11.0% |
| 2 | Networking | hardware_systems | 142 | 8.1% |
| 3 | Cloud Infrastructure | cloud_infra | 133 | 7.6% |
| 4 | Datacenter Systems | hardware_systems | 118 | 6.8% |
| 5 | Performance Engineering | hardware_systems | 113 | 6.5% |
| 6 | Deep Learning | research_domains | 81 | 4.6% |
| 7 | Silicon Verification | silicon_design | 79 | 4.5% |
| 8 | SoC Design | silicon_design | 61 | 3.5% |
| 9 | Developer Relations | product_process | 57 | 3.3% |
| 10 | Agentic AI | research_domains | 56 | 3.2% |
| 11 | Compilers | hardware_systems | 55 | 3.2% |
| 12 | Cybersecurity | mlops_devops | 55 | 3.2% |

### Emerging skills

12 skills flagged, meaning their rate in the second half exceeded 1.5x the first half on at least 5
postings.

| Skill | First half | Second half |
|---|---|---|
| Inference and Serving | 3 | 14 |
| Compilers | 11 | 25 |
| Agentic AI | 17 | 31 |
| AI Safety | 0 | 7 |
| Physical Design | 6 | 13 |
| HPC | 14 | 24 |
| LLMs | 4 | 8 |
| Design Automation | 3 | 9 |

AI Safety going from zero to seven is the cleanest signal in the set, because it cannot be a
sampling artefact of the kind described in section 5.

### Seniority concentration

| Most senior | Share senior+ | Least senior | Share senior+ |
|---|---|---|---|
| Storage Systems | 94% | Business Development | 21% |
| C++ | 91% | Robotics | 46% |
| Analog and Mixed Signal | 90% | Developer Relations | 47% |
| Signal and Power Integrity | 90% | SoC Design | 54% |

The analog and signal-integrity roles being almost entirely senior is consistent with a scarce
talent pool. Nothing in this data proves that, and it is stated as an observation, not a finding.

## 7. Limitations

1. **28% of postings carry no skill.** 489 titles name a role and nothing else. They are not
   skill-free jobs; the title is simply silent.
2. **One skill per posting on average.** A description-based extraction would yield 15 to 25. Any
   comparison against a member who has descriptions is a comparison of sources, not of companies.
3. **Solutions Architecture overlaps `role_function`.** It is a skill that is also a role. The
   overlap is deliberate, so that the kind of architect is distinguishable, but it must not be
   double-counted in Task 6.
4. **Trend flags rest on 11 observation weeks** after the censored one is dropped, with uneven gaps
   where partial scrapes were excluded. They indicate direction, not magnitude.
5. **The taxonomy extension is unratified.** Until the team agrees it, my skill space is wider than
   the others', which would distort a similarity score in Task 8.

## 8. For the team

1. **Ratify the 34 added skills and the `silicon_design` category.** If the others extract against
   the original 59 and I extract against 93, Task 8 similarity measures the taxonomy, not the
   companies.
2. **Add a `title_match_blocklist` habit.** Any member matching short tokens against titles will hit
   the same `r`/`R&D` and `c`/`c++` problems.
3. **164 candidate terms are waiting**, in `data/features/taxonomy_candidates_20260902.csv`, ranked
   by frequency. Highest unmatched: infrastructure (98), factory (21), enterprise (20), compute (20).
   Those are the next candidates for promotion or rejection.

## Files

| File | Rows | Contents |
|---|---|---|
| `data/features/nvidia_skills_long_20260902.csv` | 1,793 | **The extracted-skills dataset.** One row per posting-skill pair, with the matched term |
| `data/features/nvidia_skill_features_20260902.csv` | 59 | Per-skill feature table: counts, share, trend, emerging flag, seniority mix |
| `data/features/nvidia_skill_by_week_20260902.csv` | 59 x 12 | Skill by observation week, the input to Tasks 5 and 7 |
| `data/features/taxonomy_candidates_20260902.csv` | 164 | Unmatched terms for the team's taxonomy review |
| `extract_skills.py` | - | The pipeline, re-runnable from a clean checkout |

Reproduce with:

```bash
cd work/task-4/nvidia-nayab-khalid
python extract_skills.py
```
