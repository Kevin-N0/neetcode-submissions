"""Persistent state and filesystem helpers for NC-250 AI generation."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


STATE_SCHEMA_VERSION = 2
VALIDATOR_SCHEMA_VERSION = 2


def stable_hash(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    )


def atomic_write(
    path: Path,
    text: str,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    value = text.rstrip() + "\n"

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(value)
        temporary = Path(handle.name)

    temporary.replace(path)


def state_path(root: Path) -> Path:
    return (
        root
        / "references"
        / "data"
        / "ai-generation.json"
    )


def empty_state() -> dict[str, Any]:
    return {
        "schema_version":
            STATE_SCHEMA_VERSION,
        "validator_schema_version":
            VALIDATOR_SCHEMA_VERSION,
        "problems": {},
    }


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)

    if not path.exists():
        return empty_state()

    try:
        value = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        json.JSONDecodeError,
    ):
        return empty_state()

    if not isinstance(value, dict):
        return empty_state()

    value.setdefault(
        "schema_version",
        STATE_SCHEMA_VERSION,
    )

    value.setdefault(
        "validator_schema_version",
        VALIDATOR_SCHEMA_VERSION,
    )

    value.setdefault(
        "problems",
        {},
    )

    if not isinstance(
        value["problems"],
        dict,
    ):
        value["problems"] = {}

    return value


def save_state(
    root: Path,
    state: dict[str, Any],
) -> None:
    state["schema_version"] = (
        STATE_SCHEMA_VERSION
    )

    state["validator_schema_version"] = (
        VALIDATOR_SCHEMA_VERSION
    )

    atomic_write(
        state_path(root),
        json.dumps(
            state,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        ),
    )


def load_dotenv_chain(root: Path) -> list[Path]:
    """
    Load .env files without overriding existing environment variables.

    The child repository is checked first, then ancestors.

    This allows either:

        neetcode-submissions/.env

    or:

        InterviewForge/.env

    without requiring the secret to be duplicated.
    """

    candidates: list[Path] = []

    current = root.resolve()

    while True:
        candidate = current / ".env"

        if candidate.exists():
            candidates.append(candidate)

        if current.parent == current:
            break

        current = current.parent

    for path in candidates:
        for raw in path.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines():
            line = raw.strip()

            if (
                not line
                or line.startswith("#")
                or "=" not in line
            ):
                continue

            key, value = line.split(
                "=",
                1,
            )

            key = key.strip()
            value = value.strip()

            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in {"'", '"'}
            ):
                value = value[1:-1]

            if (
                key
                and key not in os.environ
            ):
                os.environ[key] = value

    return candidates
