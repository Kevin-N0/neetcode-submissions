from __future__ import annotations
import json
import os
from collections import defaultdict
from pathlib import Path
from .reference_scanner import ProblemRecord

def rel(source_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target, source_file.parent)).as_posix()

def build(records: list[ProblemRecord], references_root: Path, repo_root: Path, combined: bool = True) -> tuple[Path, Path, Path | None]:
    categories = defaultdict(list)
    for record in records:
        categories[record.category_slug].append(record)

    category_root = references_root / "categories"
    data_root = references_root / "data"
    export_root = references_root / "exports"
    category_root.mkdir(parents=True, exist_ok=True)
    data_root.mkdir(parents=True, exist_ok=True)
    export_root.mkdir(parents=True, exist_ok=True)

    for slug, group in categories.items():
        group.sort(key=lambda r: r.problem.lower())
        page = category_root / f"{slug}.md"
        lines = [
            f"# {group[0].category}", "",
            "[Back to the main study index](../README.md)", "",
            "| Problem | Difficulty | Preferred | Solution | Interview |",
            "|---|---|---|---|---|",
        ]
        for record in group:
            chosen = record.interview_reference or record.solution_reference
            difficulty = chosen.difficulty if chosen else "Unknown"
            preferred = chosen.preferred_solution if chosen else "Unknown"
            solution = references_root / "solution" / record.category_slug / f"{record.problem_slug}.py"
            interview = references_root / "interview" / record.category_slug / f"{record.problem_slug}.md"
            solution_link = f"[Open]({rel(page, solution)})" if solution.exists() else "Missing"
            interview_link = f"[Study]({rel(page, interview)})" if interview.exists() else "Missing"
            lines.append(f"| {record.problem} | {difficulty} | {preferred} | {solution_link} | {interview_link} |")
        page.write_text("\n".join(lines) + "\n", encoding="utf-8")

    index = references_root / "README.md"
    complete = sum(r.solution_reference is not None and r.interview_reference is not None for r in records)
    lines = [
        "# NC-250 Study References", "",
        "Generated from the newest submission of each reference type in every problem folder.", "",
        "## Overview", "",
        f"- Problems discovered: **{len(records)}**",
        f"- Solution references: **{sum(r.solution_reference is not None for r in records)}**",
        f"- Interview references: **{sum(r.interview_reference is not None for r in records)}**",
        f"- Problems with both: **{complete}**", "",
        "## Recommended Study Flow", "",
        "1. Open a category.",
        "2. Open the problem's **Interview** page.",
        "3. Use **Solution** for a shorter technical review.",
        "4. Open the source submission only when reviewing history.", "",
        "## Categories", "",
        "| Category | Problems | Complete | Page |",
        "|---|---:|---:|---|",
    ]
    for slug, group in sorted(categories.items(), key=lambda item: item[1][0].category.lower()):
        count = sum(r.solution_reference is not None and r.interview_reference is not None for r in group)
        lines.append(f"| {group[0].category} | {len(group)} | {count} | [Open](categories/{slug}.md) |")
    lines += ["", "## Missing References", "", "| Problem | Category | Missing |", "|---|---|---|"]
    missing = 0
    for record in sorted(records, key=lambda r: (r.category.lower(), r.problem.lower())):
        kinds = []
        if record.solution_reference is None:
            kinds.append("Solution")
        if record.interview_reference is None:
            kinds.append("Interview")
        if kinds:
            missing += 1
            lines.append(f"| {record.problem} | {record.category} | {', '.join(kinds)} |")
    if not missing:
        lines.append("| — | — | None |")
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = data_root / "references.json"
    manifest.write_text(json.dumps({
        "schema_version": 1,
        "problem_count": len(records),
        "problems": [r.manifest(repo_root) for r in records],
    }, indent=2) + "\n", encoding="utf-8")

    export = None
    if combined:
        export = export_root / "ALL_INTERVIEW_REFERENCES.md"
        export_lines = [
            "# All NC-250 Interview References", "",
            "> Generated export. Individual problem pages are the canonical study files.", "",
            "## Table of Contents", "",
        ]
        available = []
        for record in sorted(records, key=lambda r: (r.category.lower(), r.problem.lower())):
            page = references_root / "interview" / record.category_slug / f"{record.problem_slug}.md"
            if page.exists():
                anchor = f"{record.category_slug}-{record.problem_slug}"
                export_lines.append(f"- [{record.category}: {record.problem}](#{anchor})")
                available.append((anchor, page))
        for anchor, page in available:
            export_lines += ["", "---", "", f'<a id="{anchor}"></a>', "", page.read_text(encoding="utf-8")]
        export.write_text("\n".join(export_lines).rstrip() + "\n", encoding="utf-8")

    return index, manifest, export
