"""Generate validated SOLUTION_REFERENCE and INTERVIEW_REFERENCE artifacts with Gemini."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SUBMISSION_RE = re.compile(r"^submission-(\d+)\.py$", re.IGNORECASE)
TYPE_RE = re.compile(
    r"^\s*TYPE\s*:\s*(SOLUTION_REFERENCE|INTERVIEW_REFERENCE)\s*$",
    re.MULTILINE,
)
FIELD_PATTERNS = {
    name: re.compile(rf"^\s*{name}\s*:\s*(.+?)\s*$", re.MULTILINE)
    for name in ["CATEGORY", "PREFERRED_SOLUTION", "PROBLEM", "DIFFICULTY", "URL"]
}

STATE_SCHEMA_VERSION = 1
DEFAULT_MODEL = "gemini-3.5-flash"


@dataclass(frozen=True)
class RawSubmission:
    path: Path
    number: int


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    normalized = value.strip().lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-") or "unknown"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def load_dotenv(root: Path) -> None:
    path = root / ".env"
    if not path.exists():
        return

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


def reference_metadata(text: str) -> dict[str, str]:
    return {
        key.lower(): (match.group(1).strip() if (match := pattern.search(text)) else "")
        for key, pattern in FIELD_PATTERNS.items()
    }


def reference_type(text: str) -> str | None:
    match = TYPE_RE.search(text)
    return match.group(1) if match else None


def raw_submission(path: Path) -> RawSubmission | None:
    match = SUBMISSION_RE.match(path.name)
    if not match or not path.is_file():
        return None
    text = read_text(path)
    if reference_type(text) in {"SOLUTION_REFERENCE", "INTERVIEW_REFERENCE"}:
        return None
    return RawSubmission(path=path, number=int(match.group(1)))


def latest_raw_submission(directory: Path) -> RawSubmission | None:
    found = [
        item
        for path in directory.iterdir()
        if (item := raw_submission(path)) is not None
    ]
    if not found:
        return None
    return max(found, key=lambda item: (item.number, item.path.name.casefold()))


def problem_directories(source_root: Path) -> list[Path]:
    return sorted(
        {
            path.parent
            for path in source_root.rglob("submission-*.py")
            if path.is_file() and SUBMISSION_RE.match(path.name)
        },
        key=lambda path: path.as_posix().casefold(),
    )


def strip_code_fence(text: str) -> str:
    """Remove one outer Markdown code fence."""
    value = text.strip()
    lines = value.splitlines()

    if len(lines) >= 2:
        first = lines[0].strip().lower()
        last = lines[-1].strip()

        if first in {"```", "```python", "```py"} and last == "```":
            return "\n".join(lines[1:-1]).strip()

    return value
def validate_reference(text: str, expected_type: str) -> dict[str, str]:
    errors: list[str] = []

    for marker in ("@NC250_START", "@NC250_END", "@CONTENT_START", "@CONTENT_END"):
        if marker not in text:
            errors.append(f"missing {marker}")

    actual_type = reference_type(text)
    if actual_type != expected_type:
        errors.append(f"expected TYPE: {expected_type}, found {actual_type!r}")

    metadata = reference_metadata(text)
    for field in ("problem", "category", "difficulty", "url"):
        if not metadata.get(field):
            errors.append(f"missing {field.upper()}")

    try:
        ast.parse(text)
    except SyntaxError as exc:
        errors.append(f"not valid Python: line {exc.lineno}: {exc.msg}")

    if errors:
        raise ValueError("; ".join(errors))

    return metadata


def load_state(root: Path) -> dict:
    path = root / "references" / "data" / "ai-generation.json"
    if not path.exists():
        return {"schema_version": STATE_SCHEMA_VERSION, "problems": {}}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"schema_version": STATE_SCHEMA_VERSION, "problems": {}}

    if not isinstance(data, dict):
        data = {}

    data.setdefault("schema_version", STATE_SCHEMA_VERSION)
    data.setdefault("problems", {})
    return data


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(text)
        if not text.endswith("\n"):
            handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)


def save_state(root: Path, state: dict) -> None:
    path = root / "references" / "data" / "ai-generation.json"
    atomic_write(
        path,
        json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    )


def prompt_text(path: Path) -> str:
    if not path.exists():
        raise RuntimeError(f"Missing prompt file: {path}")

    text = read_text(path).strip()
    if not text:
        raise RuntimeError(f"Prompt is empty: {path}")

    placeholder_markers = (
        "Paste your complete SOLUTION_REFERENCE prompt below this line.",
        "Paste your complete INTERVIEW_REFERENCE prompt below this line.",
    )
    if any(marker in text for marker in placeholder_markers):
        raise RuntimeError(f"Prompt placeholder has not been replaced: {path}")

    return text


def gemini_generate(prompt: str, *, api_key: str, model: str) -> str:
    model_name = model.removeprefix("models/")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model_name}:generateContent"
    )

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {"temperature": 0.0},
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gemini API HTTP {exc.code}: {body_text[:2000]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Gemini API request failed: {exc}") from exc

    candidates = payload.get("candidates") or []
    if not candidates:
        raise RuntimeError(
            "Gemini returned no candidates. "
            f"Response: {json.dumps(payload)[:2000]}"
        )

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(
        part.get("text", "")
        for part in parts
        if isinstance(part, dict)
    ).strip()

    if not text:
        raise RuntimeError("Gemini returned a candidate without text content.")

    return strip_code_fence(text)


def _reference_path(
    root: Path,
    *,
    reference_kind: str,
    metadata: dict[str, str],
) -> Path:
    category_slug = slugify(metadata["category"])
    problem_slug = slugify(metadata["problem"])
    return root / "references" / reference_kind / category_slug / f"{problem_slug}.py"


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _remove_old_reference(
    root: Path,
    old_relative: str | None,
    new_path: Path,
) -> None:
    if not old_relative:
        return
    old_path = root / old_relative
    if old_path == new_path or not old_path.exists():
        return
    try:
        old_path.relative_to(root / "references")
    except ValueError:
        return
    old_path.unlink()


def generate_references(
    root: Path,
    *,
    force: bool = False,
    selected_problem_dirs: Iterable[str] | None = None,
) -> dict:
    root = root.resolve()
    load_dotenv(root)

    api_key = (
        os.environ.get("GEMINI_API_KEY", "").strip()
        or os.environ.get("GOOGLE_API_KEY", "").strip()
    )
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Put it in .env for local runs or "
            "GitHub Actions repository secrets for automated runs."
        )

    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL

    solution_prompt = prompt_text(root / "prompts" / "solution_reference.md")
    interview_prompt = prompt_text(root / "prompts" / "interview_reference.md")

    solution_prompt_hash = stable_hash(solution_prompt)
    interview_prompt_hash = stable_hash(interview_prompt)

    source_root = root / "Data Structures & Algorithms"
    state = load_state(root)

    selected = None
    if selected_problem_dirs:
        selected = {
            str(Path(value).as_posix()).rstrip("/")
            for value in selected_problem_dirs
        }

    report = {
        "model": model,
        "generated_solution": [],
        "generated_interview": [],
        "reused_solution": [],
        "reused_interview": [],
        "skipped_no_raw_submission": [],
        "processed": [],
    }

    for directory in problem_directories(source_root):
        problem_dir = _relative(root, directory)

        if selected is not None and problem_dir not in selected:
            continue

        raw = latest_raw_submission(directory)
        if raw is None:
            report["skipped_no_raw_submission"].append(problem_dir)
            continue

        source_text = read_text(raw.path)
        source_hash = stable_hash(source_text)
        entry = dict(state["problems"].get(problem_dir, {}))

        solution_path = (
            root / entry["solution_reference"]
            if entry.get("solution_reference")
            else None
        )

        solution_valid = False
        if solution_path and solution_path.exists():
            try:
                validate_reference(read_text(solution_path), "SOLUTION_REFERENCE")
                solution_valid = True
            except ValueError:
                solution_valid = False

        solution_stale = (
            force
            or not solution_valid
            or entry.get("source_hash") != source_hash
            or entry.get("solution_prompt_hash") != solution_prompt_hash
        )

        if solution_stale:
            combined = (
                solution_prompt.rstrip()
                + "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                + "SOURCE SUBMISSION\n"
                + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                + source_text
            )
            solution_text = gemini_generate(
                combined,
                api_key=api_key,
                model=model,
            )
            solution_metadata = validate_reference(
                solution_text,
                "SOLUTION_REFERENCE",
            )
            new_solution_path = _reference_path(
                root,
                reference_kind="solution",
                metadata=solution_metadata,
            )
            old_solution_relative = entry.get("solution_reference")
            atomic_write(new_solution_path, solution_text)
            _remove_old_reference(root, old_solution_relative, new_solution_path)

            solution_path = new_solution_path
            solution_content_hash = stable_hash(solution_text)
            report["generated_solution"].append(problem_dir)
        else:
            assert solution_path is not None
            solution_text = read_text(solution_path)
            solution_metadata = validate_reference(
                solution_text,
                "SOLUTION_REFERENCE",
            )
            solution_content_hash = stable_hash(solution_text)
            report["reused_solution"].append(problem_dir)

        interview_path = (
            root / entry["interview_reference"]
            if entry.get("interview_reference")
            else None
        )

        interview_valid = False
        if interview_path and interview_path.exists():
            try:
                validate_reference(read_text(interview_path), "INTERVIEW_REFERENCE")
                interview_valid = True
            except ValueError:
                interview_valid = False

        interview_stale = (
            force
            or not interview_valid
            or entry.get("solution_content_hash") != solution_content_hash
            or entry.get("interview_prompt_hash") != interview_prompt_hash
        )

        if interview_stale:
            combined = (
                interview_prompt.rstrip()
                + "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                + "SOURCE SOLUTION_REFERENCE\n"
                + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                + solution_text
            )
            interview_text = gemini_generate(
                combined,
                api_key=api_key,
                model=model,
            )
            interview_metadata = validate_reference(
                interview_text,
                "INTERVIEW_REFERENCE",
            )
            new_interview_path = _reference_path(
                root,
                reference_kind="interview",
                metadata=interview_metadata,
            )
            old_interview_relative = entry.get("interview_reference")
            atomic_write(new_interview_path, interview_text)
            _remove_old_reference(root, old_interview_relative, new_interview_path)

            interview_path = new_interview_path
            interview_content_hash = stable_hash(interview_text)
            report["generated_interview"].append(problem_dir)
        else:
            assert interview_path is not None
            interview_text = read_text(interview_path)
            interview_metadata = validate_reference(
                interview_text,
                "INTERVIEW_REFERENCE",
            )
            interview_content_hash = stable_hash(interview_text)
            report["reused_interview"].append(problem_dir)

        if slugify(interview_metadata["problem"]) != slugify(solution_metadata["problem"]):
            raise RuntimeError(
                f"{problem_dir}: generated INTERVIEW_REFERENCE problem identity "
                "does not match SOLUTION_REFERENCE"
            )

        state["problems"][problem_dir] = {
            "problem_dir": problem_dir,
            "source_submission": _relative(root, raw.path),
            "source_number": raw.number,
            "source_hash": source_hash,
            "solution_prompt_hash": solution_prompt_hash,
            "interview_prompt_hash": interview_prompt_hash,
            "solution_reference": _relative(root, solution_path),
            "interview_reference": _relative(root, interview_path),
            "solution_content_hash": solution_content_hash,
            "interview_content_hash": interview_content_hash,
            "model": model,
        }
        report["processed"].append(problem_dir)

    save_state(root, state)
    return report
