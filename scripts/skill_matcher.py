#!/usr/bin/env python3
"""Shared skill matcher - the one implementation every task and every member should use.

Factored out of work/task-4/nvidia-nayab-khalid/extract_skills.py so that Task 4 (extraction),
Task 6 (comparison) and Task 8 (similarity) cannot drift apart. If two members match the taxonomy
with different code, any cross-company number is a comparison of implementations.

    from skill_matcher import load_taxonomy, build_matchers, extract

    tax = load_taxonomy("shared/taxonomy/skills.yaml")
    entries, blocked = build_matchers(tax)
    hits = extract("senior physical design engineer", entries)   # [(skill, category, term)]

Three rules, all of which exist because job titles are short:

1. Longest alias wins. "gpu architecture" must not also register as a bare "gpu"; a matched span
   is consumed so no shorter term can claim it.
2. The taxonomy's `title_match_blocklist` is honoured. "r" matches "R&D" once punctuation is
   stripped; "c" matches the c inside "c++".
3. Nothing is inferred. A title with no technical term gets no skill.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml


def load_taxonomy(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def build_matchers(tax: dict) -> tuple[list[tuple[re.Pattern, str, str, int]], set[str]]:
    """One compiled pattern per alias, sorted longest-first so specific terms win."""
    blocked = {str(b).lower() for b in (tax.get("title_match_blocklist") or [])}
    entries = []
    for skill in tax["skills"]:
        name, category = skill["name"], skill["category"]
        for term in [str(name)] + [str(a) for a in (skill.get("aliases") or [])]:
            t = term.lower().strip()
            if not t or t in blocked:
                continue
            # \b fails at a "+" boundary, so guard with explicit non-word lookarounds.
            entries.append((re.compile(r"(?<![\w+#])" + re.escape(t) + r"(?![\w+#])"),
                            name, category, len(t)))
    entries.sort(key=lambda e: -e[3])
    return entries, blocked


def extract(text: str, entries) -> list[tuple[str, str, str]]:
    """Return [(canonical_skill, category, matched_term)] for one piece of text."""
    found, spans, seen = [], [], set()
    for pattern, name, category, _ in entries:
        for m in pattern.finditer(text):
            if any(m.start() < e and m.end() > s for s, e in spans):
                continue                                  # inside an already-matched span
            spans.append((m.start(), m.end()))
            if name not in seen:
                seen.add(name)
                found.append((name, category, m.group(0)))
    return found
