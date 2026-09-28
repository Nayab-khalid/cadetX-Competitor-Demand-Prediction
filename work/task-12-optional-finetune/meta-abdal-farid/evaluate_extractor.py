"""
Task 12 — Fine-Tune a Skill Extraction Model (META)
Nearest useful work: measure the Task 4 rule-based extractor against a
hand-labelled gold set, since fine-tuning is not feasible on this dataset.

Reads:
  - eval_set_labelled.csv   (hand labels, independent of Task 4)
  - ../task-4/.../meta_extracted_skills_*.csv   (Task 4 output)

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
    p.add_argument("--extracted", type=Path, default=None,
                   help="Task 4 meta_extracted_skills_*.csv")
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


def parse_skills(cell):
    if pd.isna(cell):
        return set()
    s = str(cell).strip()
    if s.lower() in ("", "none", "[]"):
        return set()
    # Handle list-like strings too
    s = s.strip("[]").replace('"', "").replace("'", "")
    return {x.strip() for x in s.replace("|", ",").split(",") if x.strip()}


def main():
    args = parse_args()
    gold_path = args.gold
    ext_path = resolve_extracted(args.extracted)
    print(f"Gold:      {gold_path}")
    print(f"Extracted: {ext_path}")

    gold = pd.read_csv(gold_path)
    ext = pd.read_csv(ext_path)

    if "job_id" not in ext.columns:
        raise SystemExit(f"extracted CSV needs 'job_id'. Got: {list(ext.columns)}")

    ext_col = None
    for c in ("extracted_skills", "skills", "skill_list"):
        if c in ext.columns:
            ext_col = c
            break
    if ext_col is None:
        raise SystemExit(f"No skills column in extracted CSV. Got: {list(ext.columns)}")

    joined = gold.merge(ext[["job_id", ext_col]], on="job_id", how="left")

    tp = fp = fn = 0
    rows = []
    for _, r in joined.iterrows():
        g = parse_skills(r["hand_labelled_skills"])
        e = parse_skills(r[ext_col])
        tp += len(g & e)
        fp += len(e - g)
        fn += len(g - e)
        rows.append({
            "job_id": r["job_id"],
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
