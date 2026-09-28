"""
Task 12 — Fine-Tune a Skill Extraction Model (META)
Nearest useful work: measure the Task 4 rule-based extractor against a
hand-labelled gold set, since fine-tuning is not feasible on this dataset.

Handles Task 4's long format:
    job_id, company_name, skill_canonical, category, matched_term, ...
    (one row per job-skill pair)

Reads:
  - eval_set_labelled.csv                    (hand labels)
  - ../task-4/.../meta_extracted_skills_*.csv (long format)

Writes:
  - evaluation_metrics.csv
  - evaluation_per_row.csv
"""
import argparse
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--gold", type=Path, default=HERE / "eval_set_labelled.csv")
    p.add_argument("--extracted", type=Path, default=None)
    p.add_argument("--out", type=Path, default=HERE / "evaluation_metrics.csv")
    return p.parse_args()


def resolve_extracted(cli_path):
    if cli_path and Path(cli_path).exists():
        return Path(cli_path)
    t4 = HERE.parents[1] / "task-4" / "meta-abdal-farid"
    for pat in ("meta_extracted_skills_*.csv", "*extracted_skills*.csv"):
        for c in sorted(t4.glob(pat), reverse=True):
            return c
    raise SystemExit(f"Task 4 extracted-skills CSV not found under {t4}")


def parse_hand(cell):
    if pd.isna(cell):
        return set()
    s = str(cell).strip()
    if s.lower() in ("", "none", "[]"):
        return set()
    s = s.strip("[]").replace('"', "").replace("'", "")
    return {x.strip() for x in s.split("|") if x.strip()}


def pivot_extracted(df):
    """Turn the long (one-row-per-job-skill) format into {job_id: set(skills)}."""
    # Find the skill column
    skill_col = None
    for c in ("skill_canonical", "skill", "canonical"):
        if c in df.columns:
            skill_col = c
            break
    if skill_col is None:
        raise SystemExit(
            f"No skill column found. Columns: {list(df.columns)}"
        )
    if "job_id" not in df.columns:
        raise SystemExit(f"No job_id column. Columns: {list(df.columns)}")

    grouped = (
        df.dropna(subset=[skill_col])
          .groupby("job_id")[skill_col]
          .apply(lambda s: {str(x).strip() for x in s if str(x).strip()})
          .to_dict()
    )
    return grouped


def main():
    args = parse_args()
    gold_path = args.gold
    ext_path = resolve_extracted(args.extracted)
    print(f"Gold:      {gold_path}")
    print(f"Extracted: {ext_path}")

    gold = pd.read_csv(gold_path)
    ext = pd.read_csv(ext_path)

    extracted_map = pivot_extracted(ext)
    print(f"Pivoted extracted skills for {len(extracted_map)} jobs")

    tp = fp = fn = 0
    rows = []
    for _, r in gold.iterrows():
        jid = r["job_id"]
        g = parse_hand(r.get("hand_labelled_skills"))
        e = extracted_map.get(jid, set())

        tp += len(g & e)
        fp += len(e - g)
        fn += len(g - e)

        rows.append({
            "job_id": jid,
            "hand_skills": "|".join(sorted(g)),
            "extracted_skills": "|".join(sorted(e)),
            "true_positives": "|".join(sorted(g & e)),
            "false_positives": "|".join(sorted(e - g)),
            "false_negatives": "|".join(sorted(g - e)),
            "tp": len(g & e), "fp": len(e - g), "fn": len(g - e),
        })

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    exact_rows = sum(1 for r in rows if r["fp"] == 0 and r["fn"] == 0)

    print(f"\nTP={tp}  FP={fp}  FN={fn}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1:        {f1:.3f}")
    print(f"Exact rows: {exact_rows}/{len(rows)}")

    pd.DataFrame([{
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "tp": tp, "fp": fp, "fn": fn,
        "exact_rows": exact_rows,
        "total_rows": len(rows),
    }]).to_csv(args.out, index=False)
    print(f"\n✅ {args.out.name}")

    detail = args.out.with_name("evaluation_per_row.csv")
    pd.DataFrame(rows).to_csv(detail, index=False)
    print(f"✅ {detail.name}")


if __name__ == "__main__":
    main()
