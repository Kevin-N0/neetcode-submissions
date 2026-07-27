from __future__ import annotations
import shutil
from pathlib import Path
from .reference_scanner import ProblemRecord

def extract(records: list[ProblemRecord], references_root: Path) -> list[Path]:
    written: list[Path] = []
    for record in records:
        if record.solution_reference is None:
            continue
        destination = references_root / "solution" / record.category_slug / f"{record.problem_slug}.py"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(record.solution_reference.path, destination)
        written.append(destination)
    return written
