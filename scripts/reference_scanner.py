from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

SUBMISSION_RE = re.compile(r"^submission-(\d+)\.py$", re.IGNORECASE)
TYPE_RE = re.compile(r"^\s*TYPE\s*:\s*(SOLUTION_REFERENCE|INTERVIEW_REFERENCE)\s*$", re.MULTILINE)

def slugify(value: str) -> str:
    value = value.strip().lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "unknown"

def field(text: str, name: str, default: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else default

@dataclass(frozen=True)
class Candidate:
    path: Path
    number: int
    reference_type: str
    category: str
    preferred_solution: str
    problem: str
    difficulty: str

@dataclass
class ProblemRecord:
    problem_dir: Path
    category: str
    problem: str
    category_slug: str
    problem_slug: str
    solution_reference: Candidate | None
    interview_reference: Candidate | None

    def manifest(self, repo_root: Path) -> dict:
        def pack(candidate: Candidate | None):
            if candidate is None:
                return None
            data = asdict(candidate)
            data["path"] = candidate.path.relative_to(repo_root).as_posix()
            return data
        return {
            "problem_dir": self.problem_dir.relative_to(repo_root).as_posix(),
            "category": self.category,
            "problem": self.problem,
            "category_slug": self.category_slug,
            "problem_slug": self.problem_slug,
            "solution_reference": pack(self.solution_reference),
            "interview_reference": pack(self.interview_reference),
        }

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
    return Candidate(
        path=path,
        number=int(match.group(1)),
        reference_type=type_match.group(1),
        category=field(text, "CATEGORY", "Unknown"),
        preferred_solution=field(text, "PREFERRED_SOLUTION", "Unknown"),
        problem=field(text, "PROBLEM", path.parent.name),
        difficulty=field(text, "DIFFICULTY", "Unknown"),
    )

def newest(items: list[Candidate], kind: str) -> Candidate | None:
    matches = [item for item in items if item.reference_type == kind]
    return max(matches, key=lambda item: (item.number, item.path.stat().st_mtime_ns)) if matches else None

def scan(source_root: Path) -> list[ProblemRecord]:
    if not source_root.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source_root}")

    records: list[ProblemRecord] = []
    for problem_dir in sorted((p for p in source_root.rglob("*") if p.is_dir()), key=lambda p: p.as_posix().lower()):
        files = [p for p in problem_dir.iterdir() if p.is_file() and SUBMISSION_RE.match(p.name)]
        if not files:
            continue
        items = [item for p in files if (item := candidate(p)) is not None]
        solution = newest(items, "SOLUTION_REFERENCE")
        interview = newest(items, "INTERVIEW_REFERENCE")
        selected = interview or solution
        category = selected.category if selected and selected.category != "Unknown" else problem_dir.parent.name
        problem = selected.problem if selected and selected.problem != "Unknown" else problem_dir.name
        records.append(ProblemRecord(
            problem_dir=problem_dir,
            category=category,
            problem=problem,
            category_slug=slugify(category),
            problem_slug=slugify(problem),
            solution_reference=solution,
            interview_reference=interview,
        ))
    return records
