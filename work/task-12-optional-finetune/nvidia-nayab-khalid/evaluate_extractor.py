#!/usr/bin/env python3
"""Optional Task 12 - evaluation of the rule-based skill extractor.

Fine-tuning a model was not possible for NVIDIA; the reasoning is in finetune-note.md. This is the
work that a fine-tune would have needed first and that has value on its own: a hand-labelled
evaluation set, and precision/recall/F1 for the extractor that Tasks 4 to 8 all depend on.

The gold labels below were assigned by reading each of 40 randomly sampled NVIDIA job titles and
deciding which canonical skills in shared/taxonomy/skills.yaml genuinely apply. They are a human
judgement, recorded here so anyone can disagree with a specific row rather than with a number.

Sample: 40 titles, random_state=2026, from the Task 3 cleaned corpus.

Usage:  python evaluate_extractor.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_matcher import build_matchers, extract, load_taxonomy      # noqa: E402

# job title -> the canonical skills that should be extracted. Empty set means "no skill in this
# title", which is a correct answer, not a failure.
GOLD: dict[str, set[str]] = {
    "Senior System Software Engineer - DevOps and Infrastructure Automation": {"Site Reliability"},
    "Senior Solutions Architect, CSP System": {"Solutions Architecture", "Cloud Infrastructure"},
    "Senior Firmware Engineer": {"Firmware"},
    "Product Marketing Manager, Quantum Computing Platform": set(),
    "Senior DL Compiler Engineer -CUDA Tile": {"Compilers", "CUDA", "Deep Learning"},
    "Senior Software Release Manager - Networking Verification Engineer": {"Networking"},
    "Senior Verification Engineer - Scalable Coherency Fabric": {"Silicon Verification"},
    "Senior Machine Learning Engineer, Perception - Autonomous Driving":
        {"Machine Learning", "Autonomous Vehicles"},
    "Senior System Software Engineer, Client Embedded Controller": {"Embedded Systems"},
    "Insider Threat Detection Engineer": {"Cybersecurity"},
    "Senior Solutions Architect, NVIDIA Cloud Partners - Telco":
        {"Solutions Architecture", "Cloud Infrastructure"},
    "Senior Firmware Micro-Architect": {"Firmware"},
    "Solutions Architect, AI Factory Infrastructure": {"Solutions Architecture"},
    "Senior Software Engineer, CUDA Python Core Libraries": {"Python", "CUDA"},
    "Principal Software Engineer - Infrastructure": set(),
    "SOC Clock Distribution Engineer": {"SoC Design"},
    "DPU Performance Validation Engineer": {"Performance Engineering", "DPU and Offload"},
    "Senior Power Integrity Engineer - LPU Packaging": {"Signal and Power Integrity"},
    "Solutions Architect, AI and ML": {"Solutions Architecture", "Machine Learning"},
    "Senior SRAM Engineer": set(),
    "SOC IP Methodology Engineer - Custom SOC": {"SoC Design"},
    "Physical Design Backend STA Engineer": {"Physical Design"},
    "Senior Technical Program Manager, Data Center - Engineering Operations":
        {"Datacenter Systems", "Technical Program Management"},
    # "ASIC" is an alias of Computer Architecture (original taxonomy) and "asic design" of SoC
    # Design (added in Task 4). Either is defensible, so both are accepted.
    "ASIC Verification Engineer - New College Grad 2026":
        {"Silicon Verification", "SoC Design", "Computer Architecture"},
    "Senior Solution Engineer, Networking": {"Networking"},
    "Senior Solutions Architect, Higher Education and Research, Multimodal and Physical AI":
        {"Solutions Architecture"},
    "Senior Solutions Architect, Generative AI": {"Solutions Architecture", "Generative AI"},
    "Applied AI Engineer": set(),
    "Senior Software Architect, RISC-V Networking Accelerator": {"Networking"},
    "Senior Software Technical Program Manager": {"Technical Program Management"},
    "SAI Software Design Engineer": set(),
    "Senior Corporate Counsel": set(),
    "Senior Customer Success Operations Manager - Technology": set(),
    "Senior Deep Learning Engineer, Accuracy Evaluation": {"Deep Learning"},
    "Applied Machine Learning Engineer, Circuit Design - New College Grad 2026":
        {"Machine Learning", "Analog and Mixed Signal"},
    "Senior Field Application Engineer - AI Factory Deployment": set(),
    "System Software Engineer, UEFI Firmware": {"Firmware"},
    "Senior Customer Program Manager - OEM": set(),
    "Senior Solutions Architect, AI Infrastructure": {"Solutions Architecture"},
    "Senior ASIC Verification Engineer, Coherent High Speed Interconnect":
        {"Silicon Verification", "SoC Design", "Computer Architecture"},
}
# Skills accepted as alternatives rather than required, so a correct-but-different mapping is not
# counted as a miss.
OPTIONAL = {"Computer Architecture", "SoC Design"}


def main() -> int:
    tax_path = ROOT / "shared/taxonomy/skills.yaml"
    entries, _ = build_matchers(load_taxonomy(tax_path))
    clean = pd.read_csv(sorted((ROOT / "work/task-3/nvidia-nayab-khalid/data/processed")
                               .glob("nvidia_postings_clean_*.csv"))[-1])
    lookup = dict(zip(clean.job_title.astype(str), clean.cleaned_description.astype(str)))

    rows, tp = [], 0
    fp = fn = 0
    for title, gold in GOLD.items():
        text = lookup.get(title)
        if text is None:
            print(f"WARN  title not found in the corpus: {title[:60]}")
            continue
        pred = {n for n, _c, _t in extract(text, entries)}
        required = {g for g in gold if g not in OPTIONAL} | (
            {g for g in gold if g in OPTIONAL} and set())
        # A row is satisfied on the optional group if it predicts at least one member of it.
        opt_in_gold = gold & OPTIONAL
        opt_ok = (not opt_in_gold) or bool(pred & opt_in_gold)
        hits = pred & gold
        misses = required - pred
        if opt_in_gold and not opt_ok:
            misses = misses | {"/".join(sorted(opt_in_gold))}
        extras = pred - gold
        tp += len(hits)
        fp += len(extras)
        fn += len(misses)
        rows.append({"title": title[:64], "gold": ", ".join(sorted(gold)) or "-",
                     "predicted": ", ".join(sorted(pred)) or "-",
                     "missed": ", ".join(sorted(misses)) or "",
                     "spurious": ", ".join(sorted(extras)) or ""})

    res = pd.DataFrame(rows)
    out = Path("data"); out.mkdir(exist_ok=True)
    res.to_csv(out / "extractor_evaluation.csv", index=False, encoding="utf-8")

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    exact = int((res.missed.eq("") & res.spurious.eq("")).sum())

    print(f"evaluated titles      {len(res)}")
    print(f"true positives        {tp}")
    print(f"false positives       {fp}")
    print(f"false negatives       {fn}")
    print(f"precision             {precision:.3f}")
    print(f"recall                {recall:.3f}")
    print(f"F1                    {f1:.3f}")
    print(f"exactly correct rows  {exact} of {len(res)} ({exact / len(res) * 100:.0f}%)")
    print("\nrows with a miss or a spurious label:")
    bad = res[(res.missed != "") | (res.spurious != "")]
    print(bad[["title", "missed", "spurious"]].to_string(index=False))
    pd.DataFrame([{"precision": round(precision, 3), "recall": round(recall, 3),
                   "f1": round(f1, 3), "tp": tp, "fp": fp, "fn": fn,
                   "titles": len(res), "exact_rows": exact}]
                 ).to_csv(out / "extractor_metrics.csv", index=False, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
