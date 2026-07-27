from __future__ import annotations
import shutil
from pathlib import Path
from .build_indexes import build as build_indexes
from .extract_solution_references import extract
from .reference_scanner import scan
from .render_interview_markdown import render

def clean(references_root: Path) -> None:
    for name in ("solution", "interview", "categories", "data", "exports", "README.md"):
        path = references_root / name
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

def build(repo_root: Path, source_root: Path, references_root: Path, clean_first: bool = False, combined: bool = True) -> dict:
    if clean_first:
        clean(references_root)
    references_root.mkdir(parents=True, exist_ok=True)
    records = scan(source_root)
    solutions = extract(records, references_root)
    interviews = render(records, references_root, repo_root)
    index, manifest, export = build_indexes(records, references_root, repo_root, combined)
    return {
        "records": records,
        "solutions": solutions,
        "interviews": interviews,
        "index": index,
        "manifest": manifest,
        "export": export,
    }
