"""Prompt loading and deterministic prompt assembly for NC-250."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .state import read_text, stable_hash


CONTRACT_VERSION_RE = re.compile(
    r"^\s*VERSION\s*:\s*(\d+)\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class PromptBundle:
    solution_prompt: str
    interview_prompt: str
    generation_contract: str
    solution_contract: str
    interview_contract: str
    repair_contract: str

    solution_prompt_hash: str
    interview_prompt_hash: str

    generation_contract_version: int
    solution_contract_version: int
    interview_contract_version: int
    repair_contract_version: int


def _required_text(
    path: Path,
) -> str:
    if not path.exists():
        raise RuntimeError(
            f"PROMPT_MISSING: {path}"
        )

    text = read_text(path).strip()

    if not text:
        raise RuntimeError(
            f"PROMPT_EMPTY: {path}"
        )

    return text


def contract_version(
    text: str,
    *,
    name: str,
) -> int:
    match = CONTRACT_VERSION_RE.search(text)

    if not match:
        raise RuntimeError(
            f"CONTRACT_INVALID: "
            f"{name} has no VERSION"
        )

    return int(match.group(1))


def load_prompt_bundle(
    root: Path,
) -> PromptBundle:
    prompts = root / "prompts"
    contracts = prompts / "contracts"

    solution_prompt = _required_text(
        prompts / "solution_reference.md"
    )

    interview_prompt = _required_text(
        prompts / "interview_reference.md"
    )

    generation = _required_text(
        contracts / "generation_contract.md"
    )

    solution_contract = _required_text(
        contracts
        / "solution_reference_contract.md"
    )

    interview_contract = _required_text(
        contracts
        / "interview_reference_contract.md"
    )

    repair = _required_text(
        contracts / "repair_contract.md"
    )

    return PromptBundle(
        solution_prompt=
            solution_prompt,
        interview_prompt=
            interview_prompt,
        generation_contract=
            generation,
        solution_contract=
            solution_contract,
        interview_contract=
            interview_contract,
        repair_contract=
            repair,
        solution_prompt_hash=
            stable_hash(solution_prompt),
        interview_prompt_hash=
            stable_hash(interview_prompt),
        generation_contract_version=
            contract_version(
                generation,
                name="generation_contract",
            ),
        solution_contract_version=
            contract_version(
                solution_contract,
                name="solution_reference_contract",
            ),
        interview_contract_version=
            contract_version(
                interview_contract,
                name="interview_reference_contract",
            ),
        repair_contract_version=
            contract_version(
                repair,
                name="repair_contract",
            ),
    )


def render_metadata(
    metadata: dict[str, str],
    *,
    title: str,
) -> str:
    lines = [
        title,
        "",
    ]

    preferred_order = (
        "SOURCE_PATH",
        "SOURCE_SUBMISSION",
        "PROBLEM",
        "URL",
        "DIFFICULTY",
        "CATEGORY",
        "PREFERRED_SOLUTION",
    )

    used: set[str] = set()

    for key in preferred_order:
        if key in metadata:
            lines.append(
                f"{key}: {metadata[key]}"
            )
            used.add(key)

    for key in sorted(metadata):
        if key in used:
            continue

        lines.append(
            f"{key}: {metadata[key]}"
        )

    return "\n".join(lines)


def _section(
    name: str,
    value: str,
) -> str:
    return (
        f"\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{name}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{value.strip()}"
    )


def build_solution_prompt(
    bundle: PromptBundle,
    *,
    authoritative_metadata:
        dict[str, str],
    source_material: str,
) -> str:
    return (
        bundle.generation_contract.strip()
        + _section(
            "SOLUTION_REFERENCE CONTRACT",
            bundle.solution_contract,
        )
        + _section(
            "TRANSFORMATION INSTRUCTIONS",
            bundle.solution_prompt,
        )
        + _section(
            "AUTHORITATIVE_METADATA",
            render_metadata(
                authoritative_metadata,
                title="AUTHORITATIVE_METADATA",
            ),
        )
        + _section(
            "SOURCE_MATERIAL",
            (
                "<SOURCE_MATERIAL>\n"
                + source_material.rstrip()
                + "\n</SOURCE_MATERIAL>"
            ),
        )
    )


def build_interview_prompt(
    bundle: PromptBundle,
    *,
    canonical_metadata:
        dict[str, str],
    solution_reference: str,
) -> str:
    return (
        bundle.generation_contract.strip()
        + _section(
            "INTERVIEW_REFERENCE CONTRACT",
            bundle.interview_contract,
        )
        + _section(
            "TRANSFORMATION INSTRUCTIONS",
            bundle.interview_prompt,
        )
        + _section(
            "CANONICAL_METADATA",
            render_metadata(
                canonical_metadata,
                title="CANONICAL_METADATA",
            ),
        )
        + _section(
            "SOURCE_MATERIAL",
            (
                "<SOURCE_MATERIAL>\n"
                + solution_reference.rstrip()
                + "\n</SOURCE_MATERIAL>"
            ),
        )
    )


def render_validation_errors(
    errors: list[object],
) -> str:
    lines: list[str] = []

    for index, error in enumerate(
        errors,
        start=1,
    ):
        code = getattr(
            error,
            "code",
            "VALIDATION_ERROR",
        )

        message = getattr(
            error,
            "message",
            str(error),
        )

        expected = getattr(
            error,
            "expected",
            None,
        )

        actual = getattr(
            error,
            "actual",
            None,
        )

        lines.append(
            f"{index}. {code}: {message}"
        )

        if expected is not None:
            lines.append(
                f"   Expected: {expected}"
            )

        if actual is not None:
            lines.append(
                f"   Actual: {actual}"
            )

    return "\n".join(lines)


def build_repair_prompt(
    bundle: PromptBundle,
    *,
    artifact_type: str,
    authoritative_metadata:
        dict[str, str],
    errors: list[object],
    failed_artifact: str,
) -> str:
    if artifact_type == "SOLUTION_REFERENCE":
        artifact_contract = (
            bundle.solution_contract
        )
    elif artifact_type == "INTERVIEW_REFERENCE":
        artifact_contract = (
            bundle.interview_contract
        )
    else:
        raise ValueError(
            f"Unknown artifact type: "
            f"{artifact_type}"
        )

    return (
        bundle.generation_contract.strip()
        + _section(
            "ARTIFACT CONTRACT",
            artifact_contract,
        )
        + _section(
            "REPAIR CONTRACT",
            bundle.repair_contract,
        )
        + _section(
            "EXPECTED ARTIFACT",
            artifact_type,
        )
        + _section(
            "AUTHORITATIVE_METADATA",
            render_metadata(
                authoritative_metadata,
                title="AUTHORITATIVE_METADATA",
            ),
        )
        + _section(
            "VALIDATION_ERRORS",
            render_validation_errors(
                errors
            ),
        )
        + _section(
            "FAILED_ARTIFACT",
            (
                "<FAILED_ARTIFACT>\n"
                + failed_artifact.rstrip()
                + "\n</FAILED_ARTIFACT>"
            ),
        )
    )
