"""Select reference artifacts and create a stable reference manifest."""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from neetcode_references.ai import (
    generate_references,
    load_state as load_ai_state,
    reference_metadata as ai_reference_metadata,
)

SUBMISSION_RE = re.compile(r"^submission-(\d+)\.py$", re.IGNORECASE)
TYPE_RE = re.compile(
    r"^\s*TYPE\s*:\s*(SOLUTION_REFERENCE|INTERVIEW_REFERENCE)\s*$",
    re.MULTILINE,
)
FIELD_PATTERNS = {
    name: re.compile(rf"^\s*{name}\s*:\s*(.+?)\s*$", re.MULTILINE)
    for name in ["CATEGORY", "PREFERRED_SOLUTION", "PROBLEM", "DIFFICULTY", "URL"]
}


@dataclass(frozen=True)
class Candidate:
    path: Path
    number: int
    reference_type: str
    metadata: dict[str, str]


def slugify(value: str) -> str:
    normalized = value.strip().lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-") or "unknown"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def candidate(path: Path) -> Candidate | None:
    match = SUBMISSION_RE.match(path.name)
    if not match:
        return None
    text = read_text(path)
    type_match = TYPE_RE.search(text)
    if not type_match:
        return None
    metadata = {
        key.lower(): (pattern.search(text).group(1).strip() if pattern.search(text) else "")
        for key, pattern in FIELD_PATTERNS.items()
    }
    return Candidate(path, int(match.group(1)), type_match.group(1), metadata)


def newest(candidates: Iterable[Candidate], reference_type: str) -> Candidate | None:
    matches = [item for item in candidates if item.reference_type == reference_type]
    return max(matches, key=lambda item: (item.number, item.path.name.lower())) if matches else None


def problem_directories(source_root: Path) -> list[Path]:
    return sorted(
        {
            path.parent
            for path in source_root.rglob("submission-*.py")
            if path.is_file() and SUBMISSION_RE.match(path.name)
        },
        key=lambda path: path.as_posix().lower(),
    )


def extract_docstring(source: str) -> str:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node, clean=False)
            if docstring and "@NC250_START" in docstring:
                return docstring.strip()
    return source


def _existing_ai_reference(root: Path, entry: dict, key: str) -> Path | None:
    relative = entry.get(key)
    if not relative:
        return None
    path = root / relative
    return path if path.is_file() else None


def _metadata_from_reference(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    return ai_reference_metadata(read_text(path))


def build(root: Path, *, clean: bool) -> dict:
    source_root = root / "Data Structures & Algorithms"
    references_root = root / "references"
    solution_root = references_root / "solution"
    interview_root = references_root / "interview"
    data_root = references_root / "data"

    # v6 keeps accepted reference artifacts in their existing locations.
    # --clean only rebuilds derived index/manifest files.
    if clean:
        for derived in (
            references_root / "README.md",
            data_root / "references.json",
        ):
            if derived.exists():
                derived.unlink()

    data_root.mkdir(parents=True, exist_ok=True)
    ai_state = load_ai_state(root)

    records: list[dict] = []

    for directory in problem_directories(source_root):
        problem_dir = directory.relative_to(root).as_posix()

        candidates = [
            item
            for path in directory.iterdir()
            if path.is_file()
            if (item := candidate(path))
        ]
        typed_solution = newest(candidates, "SOLUTION_REFERENCE")
        typed_interview = newest(candidates, "INTERVIEW_REFERENCE")

        ai_entry = ai_state.get("problems", {}).get(problem_dir, {})
        ai_solution_path = _existing_ai_reference(
            root,
            ai_entry,
            "solution_reference",
        )
        ai_interview_path = _existing_ai_reference(
            root,
            ai_entry,
            "interview_reference",
        )

        ai_solution_meta = _metadata_from_reference(ai_solution_path)
        ai_interview_meta = _metadata_from_reference(ai_interview_path)

        metadata: dict[str, str] = {}
        for key in ["category", "preferred_solution", "problem", "difficulty", "url"]:
            metadata[key] = (
                ai_interview_meta.get(key, "")
                or ai_solution_meta.get(key, "")
                or (typed_interview.metadata.get(key) if typed_interview else "")
                or (typed_solution.metadata.get(key) if typed_solution else "")
                or ""
            )

        problem = metadata.get("problem") or directory.name
        category = metadata.get("category") or directory.parent.name
        problem_slug = slugify(problem)
        category_slug = slugify(category)

        solution_relative = None
        interview_relative = None
        solution_source = None
        interview_source = None

        if ai_solution_path:
            solution_relative = ai_solution_path.relative_to(root).as_posix()
            solution_source = ai_entry.get("source_submission")
        elif typed_solution:
            destination = solution_root / category_slug / f"{problem_slug}.py"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(typed_solution.path, destination)
            solution_relative = destination.relative_to(root).as_posix()
            solution_source = typed_solution.path.relative_to(root).as_posix()

        if ai_interview_path:
            interview_relative = ai_interview_path.relative_to(root).as_posix()
            interview_source = ai_entry.get("source_submission")
        elif typed_interview:
            destination = interview_root / category_slug / f"{problem_slug}.py"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(typed_interview.path, destination)
            interview_relative = destination.relative_to(root).as_posix()
            interview_source = typed_interview.path.relative_to(root).as_posix()

        records.append(
            {
                "problem_dir": problem_dir,
                "problem": problem,
                "problem_slug": problem_slug,
                "category": category,
                "category_slug": category_slug,
                "difficulty": metadata.get("difficulty") or "Unknown",
                "preferred_solution": metadata.get("preferred_solution") or "Unknown",
                "url": metadata.get("url") or "",
                "solution_reference": solution_relative,
                "interview_reference": interview_relative,
                "solution_source": solution_source,
                "interview_source": interview_source,
            }
        )

    payload = {"schema_version": 1, "problem_count": len(records), "problems": records}
    manifest = data_root / "references.json"
    manifest.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    index_lines = [
        "# NeetCode References",
        "",
        "Generated from accepted AI references when available, with typed submissions retained as a fallback.",
        "",
        "| Problem | Category | Solution | Interview | URL |",
        "|---|---|---|---|---|",
    ]

    for item in sorted(records, key=lambda value: (value["category"], value["problem"])):
        solution_link = (
            f"[Open]({item['solution_reference'].removeprefix('references/')})"
            if item["solution_reference"] else "Missing"
        )
        interview_link = (
            f"[Open]({item['interview_reference'].removeprefix('references/')})"
            if item["interview_reference"] else "Missing"
        )
        url_link = (
            f"[Problem]({item['url']})"
            if item["url"].startswith(("http://", "https://")) else "Missing"
        )
        index_lines.append(
            f"| {item['problem']} | {item['category']} | {solution_link} | {interview_link} | {url_link} |"
        )

    (references_root / "README.md").write_text(
        "\n".join(index_lines) + "\n",
        encoding="utf-8",
    )
    return payload


def main(root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build typed and AI-generated NeetCode references."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Rebuild derived reference index/manifest files.",
    )
    parser.add_argument(
        "--ai",
        action="store_true",
        help="Generate stale references with Gemini.",
    )
    parser.add_argument(
        "--force-ai",
        action="store_true",
        help="Force AI regeneration for selected problems.",
    )
    parser.add_argument(
        "--problem-dir",
        action="append",
        default=[],
        help="Limit AI generation to a repository-relative problem directory. May be repeated.",
    )

    args = parser.parse_args()
    repository_root = (root or Path.cwd()).resolve()

    if args.force_ai and not args.ai:
        parser.error("--force-ai requires --ai")

    if args.ai:
        report = generate_references(
            repository_root,
            force=args.force_ai,
            selected_problem_dirs=args.problem_dir or None,
        )
        print(json.dumps({"ai_generation": report}, indent=2))

    payload = build(repository_root, clean=args.clean)
    complete = sum(
        bool(item["solution_reference"] and item["interview_reference"])
        for item in payload["problems"]
    )
    print(f"Discovered {payload['problem_count']} problems; {complete} have both references.")
    return 0
