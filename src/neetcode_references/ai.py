"""NC-250 v7 Gemini generation pipeline."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .prompting import (
    PromptBundle,
    build_interview_prompt,
    build_repair_prompt,
    build_solution_prompt,
    load_prompt_bundle,
)
from .state import (
    VALIDATOR_SCHEMA_VERSION,
    atomic_write,
    load_dotenv_chain,
    load_state,
    read_text,
    save_state,
    stable_hash,
)
from .validation import (
    ValidationResult,
    extract_metadata,
    format_validation_errors,
    validate_cross_reference,
    validate_interview_reference,
    validate_solution_reference,
)


SUBMISSION_RE = re.compile(
    r"^submission-(\d+)\.py$",
    re.IGNORECASE,
)

REFERENCE_TYPE_RE = re.compile(
    r"^\s*(?:#\s*)?"
    r"TYPE\s*:\s*"
    r"(SOLUTION_REFERENCE|INTERVIEW_REFERENCE)"
    r"\s*$",
    re.MULTILINE,
)

SOURCE_FIELD_PATTERNS = {
    field:
        re.compile(
            rf"^\s*(?:#\s*)?"
            rf"{field}\s*:\s*(.*?)\s*$",
            re.MULTILINE,
        )
    for field in (
        "CATEGORY",
        "PREFERRED_SOLUTION",
        "PROBLEM",
        "URL",
        "DIFFICULTY",
    )
}

DEFAULT_MODEL = "gemini-3.5-flash"


# =============================================================================
# Configuration
# =============================================================================


def _env_bool(
    name: str,
    default: bool,
) -> bool:
    raw = os.environ.get(name)

    if raw is None:
        return default

    value = raw.strip().lower()

    if value in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True

    if value in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False

    raise RuntimeError(
        f"Invalid boolean for {name}: "
        f"{raw!r}"
    )


def _env_int(
    name: str,
    default: int,
    *,
    minimum: int = 0,
) -> int:
    raw = os.environ.get(name)

    if raw is None or not raw.strip():
        return default

    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(
            f"Invalid integer for {name}: "
            f"{raw!r}"
        ) from exc

    if value < minimum:
        raise RuntimeError(
            f"{name} must be >= {minimum}"
        )

    return value


def _env_float(
    name: str,
    default: float,
) -> float:
    raw = os.environ.get(name)

    if raw is None or not raw.strip():
        return default

    try:
        return float(raw)
    except ValueError as exc:
        raise RuntimeError(
            f"Invalid float for {name}: "
            f"{raw!r}"
        ) from exc


@dataclass(frozen=True)
class AIConfig:
    enabled: bool
    api_key: str
    model: str

    max_repair_attempts: int
    max_calls_per_problem: int
    max_calls_per_run: int

    transport_retries: int
    retry_base_delay_seconds: float

    temperature: float
    max_output_tokens: int | None

    save_failed_responses: bool


def load_config(
    root: Path,
) -> AIConfig:
    load_dotenv_chain(root)

    enabled = _env_bool(
        "AI_GENERATION_ENABLED",
        True,
    )

    api_key = (
        os.environ.get(
            "GEMINI_API_KEY",
            "",
        ).strip()
        or
        os.environ.get(
            "GOOGLE_API_KEY",
            "",
        ).strip()
    )

    if enabled and not api_key:
        raise RuntimeError(
            "AUTH_FAILED: Missing "
            "GEMINI_API_KEY or "
            "GOOGLE_API_KEY."
        )

    model = (
        os.environ.get(
            "GEMINI_MODEL",
            DEFAULT_MODEL,
        ).strip()
        or DEFAULT_MODEL
    )

    output_raw = os.environ.get(
        "AI_MAX_OUTPUT_TOKENS",
        "",
    ).strip()

    max_output_tokens = (
        int(output_raw)
        if output_raw
        else None
    )

    if (
        max_output_tokens is not None
        and max_output_tokens <= 0
    ):
        raise RuntimeError(
            "AI_MAX_OUTPUT_TOKENS must "
            "be positive."
        )

    return AIConfig(
        enabled=enabled,
        api_key=api_key,
        model=model,

        max_repair_attempts=
            _env_int(
                "AI_MAX_REPAIR_ATTEMPTS",
                1,
            ),

        max_calls_per_problem=
            _env_int(
                "AI_MAX_CALLS_PER_PROBLEM",
                4,
            ),

        max_calls_per_run=
            _env_int(
                "AI_MAX_CALLS_PER_RUN",
                4,
            ),

        transport_retries=
            _env_int(
                "AI_TRANSPORT_RETRIES",
                2,
            ),

        retry_base_delay_seconds=
            _env_float(
                "AI_RETRY_BASE_DELAY_SECONDS",
                2.0,
            ),

        temperature=
            _env_float(
                "AI_TEMPERATURE",
                0.0,
            ),

        max_output_tokens=
            max_output_tokens,

        save_failed_responses=
            _env_bool(
                "AI_SAVE_FAILED_RESPONSES",
                True,
            ),
    )


# =============================================================================
# Budgeting
# =============================================================================


class CallBudgetExceeded(RuntimeError):
    pass


@dataclass
class CallBudget:
    run_limit: int
    problem_limit: int

    run_calls: int = 0
    problem_calls: int = 0

    def begin_problem(self) -> None:
        self.problem_calls = 0

    def consume(self) -> None:
        if (
            self.run_calls
            >= self.run_limit
        ):
            raise CallBudgetExceeded(
                "CALL_BUDGET_EXHAUSTED: "
                "run call budget exhausted."
            )

        if (
            self.problem_calls
            >= self.problem_limit
        ):
            raise CallBudgetExceeded(
                "CALL_BUDGET_EXHAUSTED: "
                "problem call budget exhausted."
            )

        self.run_calls += 1
        self.problem_calls += 1


# =============================================================================
# Builder compatibility API
# =============================================================================


def reference_metadata(
    text: str,
) -> dict[str, str]:
    """
    Return reference metadata using the legacy builder-facing shape.

    builder.py historically imports:

        reference_metadata as ai_reference_metadata

    from this module and expects lower-case field names.

    v7 moved canonical metadata parsing into validation.extract_metadata().
    This adapter preserves the existing builder API while keeping the new
    parser as the single implementation of metadata extraction.
    """

    metadata = extract_metadata(text)

    return {
        key.lower(): metadata.get(
            key,
            "",
        )
        for key in (
            "CATEGORY",
            "PREFERRED_SOLUTION",
            "PROBLEM",
            "DIFFICULTY",
            "URL",
        )
    }

# =============================================================================
# Raw-submission classification
# =============================================================================


RAW_START_MARKER = "@NC250_RAW_START"
RAW_END_MARKER = "@NC250_RAW_END"

RAW_SCHEMA_RE = re.compile(
    r"^\s*RAW_SCHEMA_VERSION\s*:\s*(\d+)\s*$",
    re.MULTILINE,
)

RAW_PLACEHOLDER_PATTERNS = (
    re.compile(
        r"PREFERRED_SOLUTION\s*:\s*"
        r"\[(?:OPTIONAL|S1\s*\|\s*S2\s*\|\s*S3\s*\|\s*S4)\]",
        re.IGNORECASE,
    ),
    re.compile(
        r"CATEGORY\s*:\s*\[OPTIONAL\]",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bTIME\s*:\s*(?:\[)?O\(\.\.\.\)(?:\])?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bSPACE\s*:\s*(?:\[)?O\(\.\.\.\)(?:\])?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:TIME|SPACE)\s*:\s*(?:\[)?UNKNOWN(?:\])?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\[APPROACH NAME\]",
        re.IGNORECASE,
    ),
    re.compile(
        r"\[(?:DEFINE|IDENTIFY|STATE|EXPLAIN)\b[^\]]*\]",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True)
class SubmissionClassification:
    kind: str
    reason: str
    reference_type: str | None = None


def has_raw_template_markers(
    text: str,
) -> bool:
    return (
        RAW_START_MARKER in text
        or RAW_END_MARKER in text
        or RAW_SCHEMA_RE.search(text) is not None
    )


def has_unresolved_raw_placeholders(
    text: str,
) -> bool:
    return any(
        pattern.search(text) is not None
        for pattern in RAW_PLACEHOLDER_PATTERNS
    )


def classify_submission_text(
    text: str,
) -> SubmissionClassification:
    """
    Classify one submission-N.py file.

    RAW means the file is eligible as Prompt 1 SOURCE_MATERIAL.

    A template-backed source remains RAW even when legacy/template text
    contains TYPE: SOLUTION_REFERENCE.

    Completed typed references remain excluded from raw-source selection.
    """

    reference_type = _reference_type_from_source(text)

    if has_raw_template_markers(text):
        return SubmissionClassification(
            kind="RAW",
            reason="raw template marker/schema present",
            reference_type=reference_type,
        )

    if has_unresolved_raw_placeholders(text):
        return SubmissionClassification(
            kind="RAW",
            reason="unresolved raw template placeholders present",
            reference_type=reference_type,
        )

    if reference_type == "SOLUTION_REFERENCE":
        return SubmissionClassification(
            kind="SOLUTION_REFERENCE",
            reason="completed typed solution reference",
            reference_type=reference_type,
        )

    if reference_type == "INTERVIEW_REFERENCE":
        return SubmissionClassification(
            kind="INTERVIEW_REFERENCE",
            reason="completed typed interview reference",
            reference_type=reference_type,
        )

    return SubmissionClassification(
        kind="RAW",
        reason="untyped submission source",
        reference_type=None,
    )

# =============================================================================
# Source discovery
# =============================================================================


@dataclass(frozen=True)
class RawSubmission:
    path: Path
    number: int


def _reference_type_from_source(
    text: str,
) -> str | None:
    match = REFERENCE_TYPE_RE.search(
        text
    )

    return (
        match.group(1)
        if match
        else None
    )


def raw_submission(
    path: Path,
) -> RawSubmission | None:
    match = SUBMISSION_RE.match(
        path.name
    )

    if (
        not match
        or not path.is_file()
    ):
        return None

    text = read_text(path)

    classification = (
        classify_submission_text(text)
    )

    if classification.kind != "RAW":
        return None

    return RawSubmission(
        path=path,
        number=int(match.group(1)),
    )

def latest_raw_submission(
    directory: Path,
) -> RawSubmission | None:
    candidates = [
        item
        for path in directory.iterdir()
        if (
            item := raw_submission(path)
        ) is not None
    ]

    if not candidates:
        return None

    return max(
        candidates,
        key=lambda item: (
            item.number,
            item.path.name.casefold(),
        ),
    )


def problem_directories(
    source_root: Path,
) -> list[Path]:
    return sorted(
        {
            path.parent
            for path in source_root.rglob(
                "submission-*.py"
            )
            if (
                path.is_file()
                and SUBMISSION_RE.match(
                    path.name
                )
            )
        },
        key=lambda value:
            value.as_posix().casefold(),
    )


def _relative(
    root: Path,
    path: Path,
) -> str:
    return (
        path
        .resolve()
        .relative_to(
            root.resolve()
        )
        .as_posix()
    )


# =============================================================================
# Source metadata
# =============================================================================


def _clean_source_value(
    value: str,
) -> str:
    """
    Perform deterministic formatting cleanup on one RAW metadata value.

    This function may remove source-formatting wrappers, but it must never
    invent or semantically rewrite metadata.
    """

    value = value.strip()

    # Copied Markdown may escape delimiters.
    value = (
        value
        .replace(r"\[", "[")
        .replace(r"\]", "]")
        .replace(r"\(", "(")
        .replace(r"\)", ")")
    )

    # ---------------------------------------------------------------
    # Markdown link
    #
    #     [label](https://example.com/path)
    #
    # RAW submissions are intentionally allowed to contain Markdown.
    # Prefer deterministic structural parsing here rather than relying
    # on the model to normalize authoritative metadata.
    # ---------------------------------------------------------------

    if (
        value.startswith("[")
        and "](" in value
        and value.endswith(")")
    ):
        _, separator, remainder = value.partition("](")

        if separator:
            target = remainder[:-1].strip()

            if target.startswith(
                ("http://", "https://")
            ):
                return target

    # Defensive fallback when copied formatting surrounds a Markdown link.
    marker = "]("

    marker_index = value.find(marker)

    if marker_index >= 0:
        remainder = value[
            marker_index + len(marker):
        ]

        close_index = remainder.find(")")

        if close_index >= 0:
            target = remainder[
                :close_index
            ].strip()

            if target.startswith(
                ("http://", "https://")
            ):
                return target

    # ---------------------------------------------------------------
    # Simple template wrapper
    #
    #     [Easy]
    #
    # Do not unwrap option lists such as:
    #
    #     [Easy | Medium | Hard | Unknown]
    # ---------------------------------------------------------------

    if (
        value.startswith("[")
        and value.endswith("]")
        and "|" not in value
    ):
        value = value[1:-1].strip()

    return value

def _source_value_is_placeholder(
    key: str,
    value: str,
) -> bool:
    """
    Return True when a raw-template field is not real source metadata.

    Raw submissions are intentionally allowed to contain instructional
    placeholder values. These must never become AUTHORITATIVE_METADATA.
    """

    normalized = " ".join(
        value.strip().split()
    )

    upper = normalized.upper()

    if not normalized:
        return True

    universal_placeholders = {
        "OPTIONAL",
        "UNKNOWN",
        "TBD",
        "TODO",
        "N/A",
        "NONE",
        "...",
        "O(...)",
    }

    if upper in universal_placeholders:
        return True

    # Anything still expressed as a choice/list is unresolved.
    if "|" in normalized:
        return True

    # Generic bracket/template remnants.
    if (
        normalized.startswith("[")
        and normalized.endswith("]")
    ):
        return True

    if "..." in normalized:
        return True

    instructional_prefixes = (
        "PASTE ",
        "ENTER ",
        "ADD ",
        "INSERT ",
        "WRITE ",
        "FILL ",
        "CHOOSE ",
        "SELECT ",
        "DEFINE ",
        "IDENTIFY ",
        "STATE ",
        "EXPLAIN ",
        "COPY ",
    )

    if upper.startswith(
        instructional_prefixes
    ):
        return True

    key = key.upper()

    if key == "URL":
        # An authoritative URL must actually be a URL.
        #
        # Unknown or placeholder values are simply omitted from authoritative
        # metadata so Prompt 1 can preserve uncertainty.
        if not normalized.startswith(
            ("http://", "https://")
        ):
            return True

    elif key == "DIFFICULTY":
        if normalized not in {
            "Easy",
            "Medium",
            "Hard",
        }:
            return True

    elif key == "PREFERRED_SOLUTION":
        if not re.fullmatch(
            r"S[1-4]",
            normalized,
        ):
            return True

    elif key in {
        "PROBLEM",
        "CATEGORY",
    }:
        placeholder_phrases = (
            "PROBLEM NAME",
            "PASTE PROBLEM",
            "CATEGORY NAME",
            "PASTE CATEGORY",
        )

        if any(
            phrase in upper
            for phrase in placeholder_phrases
        ):
            return True

    return False


def extract_source_metadata(
    text: str,
) -> dict[str, str]:
    """
    Extract only concrete metadata supplied by the raw submission.

    Raw-template placeholders are intentionally ignored.
    """

    values: dict[str, str] = {}

    for key, pattern in SOURCE_FIELD_PATTERNS.items():
        match = pattern.search(text)

        if not match:
            continue

        value = _clean_source_value(
            match.group(1)
        )

        if _source_value_is_placeholder(
            key,
            value,
        ):
            continue

        values[key] = value

    return values

def authoritative_metadata_for_source(
    root: Path,
    directory: Path,
    raw: RawSubmission,
    text: str,
) -> dict[str, str]:
    source = extract_source_metadata(
        text
    )

    result = {
        "SOURCE_PATH":
            _relative(
                root,
                directory,
            ),
        "SOURCE_SUBMISSION":
            raw.path.name,
    }

    for key in (
        "PROBLEM",
        "URL",
        "DIFFICULTY",
        "CATEGORY",
        "PREFERRED_SOLUTION",
    ):
        if key in source:
            result[key] = source[key]

    return result


# =============================================================================
# Gemini transport
# =============================================================================


@dataclass(frozen=True)
class GeminiResponse:
    text: str
    finish_reason: str | None


class GeminiTransportError(
    RuntimeError
):
    pass


def strip_outer_code_fence(
    text: str,
) -> str:
    """
    One safe normalization is retained.

    We still reject fences at validation time if
    they survive this exact outer-wrapper removal.
    """

    value = text.strip()
    lines = value.splitlines()

    if len(lines) < 2:
        return value

    first = lines[0].strip().lower()
    last = lines[-1].strip()

    if (
        first in {
            "```",
            "```python",
            "```py",
        }
        and last == "```"
    ):
        return "\n".join(
            lines[1:-1]
        ).strip()

    return value


def _http_error_body(
    exc: urllib.error.HTTPError,
) -> str:
    try:
        return (
            exc.read()
            .decode(
                "utf-8",
                errors="replace",
            )
        )
    except Exception:
        return ""


def gemini_generate(
    prompt: str,
    *,
    config: AIConfig,
    budget: CallBudget,
) -> GeminiResponse:
    model_name = (
        config.model
        .removeprefix("models/")
    )

    endpoint = (
        "https://generativelanguage."
        "googleapis.com/v1beta/"
        f"models/{model_name}:"
        "generateContent"
    )

    generation_config: dict[
        str,
        object,
    ] = {
        "temperature":
            config.temperature,
    }

    if (
        config.max_output_tokens
        is not None
    ):
        generation_config[
            "maxOutputTokens"
        ] = (
            config.max_output_tokens
        )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],
        "generationConfig":
            generation_config,
    }

    encoded = json.dumps(
        payload
    ).encode("utf-8")

    attempts = (
        config.transport_retries
        + 1
    )

    last_error: Exception | None = None

    for transport_attempt in range(
        attempts
    ):
        budget.consume()

        request = urllib.request.Request(
            endpoint,
            data=encoded,
            method="POST",
            headers={
                "Content-Type":
                    "application/json",
                "x-goog-api-key":
                    config.api_key,
            },
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=300,
            ) as response:
                body = json.loads(
                    response.read().decode(
                        "utf-8"
                    )
                )

        except urllib.error.HTTPError as exc:
            body_text = (
                _http_error_body(exc)
            )

            if exc.code in {
                400,
                401,
                403,
                404,
            }:
                if exc.code in {
                    401,
                    403,
                }:
                    status = "AUTH_FAILED"
                elif exc.code == 404:
                    status = (
                        "MODEL_UNAVAILABLE"
                    )
                else:
                    status = (
                        "API_BAD_REQUEST"
                    )

                raise GeminiTransportError(
                    f"{status}: HTTP "
                    f"{exc.code}: "
                    f"{body_text[:1200]}"
                ) from exc

            if (
                exc.code == 429
                or 500 <= exc.code < 600
            ):
                last_error = exc

                if (
                    transport_attempt
                    + 1
                    < attempts
                ):
                    delay = (
                        config
                        .retry_base_delay_seconds
                        * (
                            2
                            ** transport_attempt
                        )
                    )

                    time.sleep(delay)
                    continue

                status = (
                    "RATE_LIMITED"
                    if exc.code == 429
                    else "API_UNAVAILABLE"
                )

                raise GeminiTransportError(
                    f"{status}: HTTP "
                    f"{exc.code}: "
                    f"{body_text[:1200]}"
                ) from exc

            raise GeminiTransportError(
                f"API_UNAVAILABLE: HTTP "
                f"{exc.code}: "
                f"{body_text[:1200]}"
            ) from exc

        except urllib.error.URLError as exc:
            last_error = exc

            if (
                transport_attempt
                + 1
                < attempts
            ):
                delay = (
                    config
                    .retry_base_delay_seconds
                    * (
                        2
                        ** transport_attempt
                    )
                )

                time.sleep(delay)
                continue

            raise GeminiTransportError(
                "API_UNAVAILABLE: "
                f"{exc}"
            ) from exc

        candidates = (
            body.get("candidates")
            or []
        )

        if not candidates:
            raise GeminiTransportError(
                "API_UNAVAILABLE: Gemini "
                "returned no candidates."
            )

        candidate = candidates[0]

        finish_reason = (
            candidate.get(
                "finishReason"
            )
        )

        parts = (
            candidate
            .get(
                "content",
                {},
            )
            .get(
                "parts",
                [],
            )
        )

        text = "".join(
            part.get(
                "text",
                "",
            )
            for part in parts
            if isinstance(
                part,
                dict,
            )
        ).strip()

        if not text:
            raise GeminiTransportError(
                "EMPTY_RESPONSE: Gemini "
                "candidate contained no text."
            )

        return GeminiResponse(
            text=strip_outer_code_fence(
                text
            ),
            finish_reason=
                finish_reason,
        )

    raise GeminiTransportError(
        "API_UNAVAILABLE: "
        f"{last_error}"
    )


# =============================================================================
# Failed output diagnostics
# =============================================================================


def _failure_root(
    root: Path,
    directory: Path,
) -> Path:
    return (
        root
        / "references"
        / "data"
        / "ai-failures"
        / directory.name
    )


def save_failed_response(
    root: Path,
    directory: Path,
    *,
    name: str,
    response_text: str,
    validation:
        ValidationResult | None,
    config: AIConfig,
) -> None:
    if not config.save_failed_responses:
        return

    base = _failure_root(
        root,
        directory,
    )

    base.mkdir(
        parents=True,
        exist_ok=True,
    )

    artifact_path = (
        base / f"{name}.txt"
    )

    artifact_path.write_text(
        response_text,
        encoding="utf-8",
    )

    metadata = {
        "name": name,
        "validation_errors": (
            [
                {
                    "code": issue.code,
                    "message":
                        issue.message,
                    "expected":
                        issue.expected,
                    "actual":
                        issue.actual,
                }
                for issue
                in validation.errors
            ]
            if validation
            else []
        ),
    }

    (
        base
        / f"{name}.json"
    ).write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


# =============================================================================
# Accepted-reference paths / lookup
# =============================================================================


def slugify(
    value: str,
) -> str:
    normalized = (
        value.strip().lower()
        .replace("&", " and ")
    )

    normalized = re.sub(
        r"[^a-z0-9]+",
        "-",
        normalized,
    )

    return (
        normalized.strip("-")
        or "unknown"
    )


def reference_path(
    root: Path,
    kind: str,
    metadata: dict[str, str],
) -> Path:
    return (
        root
        / "references"
        / kind
        / slugify(
            metadata["CATEGORY"]
        )
        / (
            slugify(
                metadata["PROBLEM"]
            )
            + ".py"
        )
    )


def find_existing_reference(
    root: Path,
    *,
    kind: str,
    problem_name: str | None,
) -> Path | None:
    if not problem_name:
        return None

    base = root / "references" / kind

    if not base.exists():
        return None

    slug = slugify(problem_name)

    matches = list(
        base.rglob(
            f"{slug}.py"
        )
    )

    if len(matches) == 1:
        return matches[0]

    return None


# =============================================================================
# Validation + repair
# =============================================================================


@dataclass
class ArtifactGeneration:
    text: str
    validation: ValidationResult
    generation_calls_before: int
    generation_calls_after: int
    repair_attempts: int


def _log_validation(
    result: ValidationResult,
) -> None:
    if result.valid:
        print("[VALIDATION] passed")
        return

    print("[VALIDATION] failed:")

    for issue in result.errors:
        print(
            f"  - {issue.code}: "
            f"{issue.message}"
        )


def generate_with_repair(
    *,
    root: Path,
    directory: Path,
    artifact_type: str,
    initial_prompt: str,
    authoritative_metadata:
        dict[str, str],
    bundle: PromptBundle,
    config: AIConfig,
    budget: CallBudget,
) -> ArtifactGeneration:
    calls_before = budget.run_calls

    print(
        f"[AI] {artifact_type} "
        "generation attempt 1"
    )

    response = gemini_generate(
        initial_prompt,
        config=config,
        budget=budget,
    )

    if artifact_type == "SOLUTION_REFERENCE":
        validation = (
            validate_solution_reference(
                response.text,
                authoritative_metadata=
                    authoritative_metadata,
            )
        )
    else:
        validation = (
            validate_interview_reference(
                response.text,
                canonical_metadata=
                    authoritative_metadata,
            )
        )

    _log_validation(validation)

    if validation.valid:
        return ArtifactGeneration(
            text=response.text,
            validation=validation,
            generation_calls_before=
                calls_before,
            generation_calls_after=
                budget.run_calls,
            repair_attempts=0,
        )

    save_failed_response(
        root,
        directory,
        name=(
            artifact_type.lower()
            + "-generation-1"
        ),
        response_text=response.text,
        validation=validation,
        config=config,
    )

    failed_text = response.text

    for repair_index in range(
        1,
        config.max_repair_attempts + 1,
    ):
        print(
            f"[AI] {artifact_type} "
            f"repair attempt "
            f"{repair_index}/"
            f"{config.max_repair_attempts}"
        )

        repair_prompt = (
            build_repair_prompt(
                bundle,
                artifact_type=
                    artifact_type,
                authoritative_metadata=
                    authoritative_metadata,
                errors=
                    validation.errors,
                failed_artifact=
                    failed_text,
            )
        )

        response = gemini_generate(
            repair_prompt,
            config=config,
            budget=budget,
        )

        if artifact_type == (
            "SOLUTION_REFERENCE"
        ):
            validation = (
                validate_solution_reference(
                    response.text,
                    authoritative_metadata=
                        authoritative_metadata,
                )
            )
        else:
            validation = (
                validate_interview_reference(
                    response.text,
                    canonical_metadata=
                        authoritative_metadata,
                )
            )

        _log_validation(
            validation
        )

        if validation.valid:
            return ArtifactGeneration(
                text=response.text,
                validation=validation,
                generation_calls_before=
                    calls_before,
                generation_calls_after=
                    budget.run_calls,
                repair_attempts=
                    repair_index,
            )

        failed_text = response.text

        save_failed_response(
            root,
            directory,
            name=(
                artifact_type.lower()
                + f"-repair-{repair_index}"
            ),
            response_text=
                response.text,
            validation=validation,
            config=config,
        )

    raise RuntimeError(
        "REPAIR_EXHAUSTED: "
        f"{artifact_type}: "
        f"{format_validation_errors(validation)}"
    )


# =============================================================================
# State / staleness helpers
# =============================================================================


def _entry_path(
    root: Path,
    entry: dict,
    key: str,
) -> Path | None:
    raw = entry.get(key)

    if not raw:
        return None

    path = root / raw

    return (
        path
        if path.exists()
        else None
    )


def _valid_existing_solution(
    root: Path,
    entry: dict,
    *,
    authoritative_metadata:
        dict[str, str],
) -> tuple[
    Path | None,
    str | None,
    ValidationResult | None,
]:
    path = _entry_path(
        root,
        entry,
        "solution_reference",
    )

    if path is None:
        problem = (
            authoritative_metadata
            .get("PROBLEM")
        )

        path = find_existing_reference(
            root,
            kind="solution",
            problem_name=problem,
        )

    if (
        path is None
        or not path.exists()
    ):
        return None, None, None

    text = read_text(path)

    validation = (
        validate_solution_reference(
            text,
            authoritative_metadata=
                authoritative_metadata,
        )
    )

    if not validation.valid:
        return path, text, validation

    return path, text, validation


def _valid_existing_interview(
    root: Path,
    entry: dict,
    *,
    canonical_metadata:
        dict[str, str],
) -> tuple[
    Path | None,
    str | None,
    ValidationResult | None,
]:
    path = _entry_path(
        root,
        entry,
        "interview_reference",
    )

    if path is None:
        problem = (
            canonical_metadata
            .get("PROBLEM")
        )

        path = find_existing_reference(
            root,
            kind="interview",
            problem_name=problem,
        )

    if (
        path is None
        or not path.exists()
    ):
        return None, None, None

    text = read_text(path)

    validation = (
        validate_interview_reference(
            text,
            canonical_metadata=
                canonical_metadata,
        )
    )

    if not validation.valid:
        return path, text, validation

    return path, text, validation


def solution_is_stale(
    *,
    force: bool,
    entry: dict,
    source_hash: str,
    bundle: PromptBundle,
    existing_text: str | None,
    existing_validation:
        ValidationResult | None,
) -> bool:
    if force:
        return True

    if (
        existing_text is None
        or existing_validation is None
        or not existing_validation.valid
    ):
        return True

    if (
        entry.get("source_hash")
        != source_hash
    ):
        return True

    if (
        entry.get(
            "solution_prompt_hash"
        )
        != bundle.solution_prompt_hash
    ):
        return True

    if (
        entry.get(
            "generation_contract_version"
        )
        != bundle
        .generation_contract_version
    ):
        return True

    if (
        entry.get(
            "solution_contract_version"
        )
        != bundle
        .solution_contract_version
    ):
        return True

    if (
        entry.get(
            "validator_schema_version"
        )
        != VALIDATOR_SCHEMA_VERSION
    ):
        return True

    stored_hash = entry.get(
        "solution_content_hash"
    )

    if (
        stored_hash
        and stored_hash
        != stable_hash(existing_text)
    ):
        return True

    return False


def interview_is_stale(
    *,
    force: bool,
    entry: dict,
    solution_hash: str,
    bundle: PromptBundle,
    existing_text: str | None,
    existing_validation:
        ValidationResult | None,
) -> bool:
    if force:
        return True

    if (
        existing_text is None
        or existing_validation is None
        or not existing_validation.valid
    ):
        return True

    if (
        entry.get(
            "solution_content_hash"
        )
        != solution_hash
    ):
        return True

    if (
        entry.get(
            "interview_prompt_hash"
        )
        != bundle.interview_prompt_hash
    ):
        return True

    if (
        entry.get(
            "generation_contract_version"
        )
        != bundle
        .generation_contract_version
    ):
        return True

    if (
        entry.get(
            "interview_contract_version"
        )
        != bundle
        .interview_contract_version
    ):
        return True

    if (
        entry.get(
            "validator_schema_version"
        )
        != VALIDATOR_SCHEMA_VERSION
    ):
        return True

    stored_hash = entry.get(
        "interview_content_hash"
    )

    if (
        stored_hash
        and stored_hash
        != stable_hash(existing_text)
    ):
        return True

    return False


# =============================================================================
# Main generation pipeline
# =============================================================================


def generate_references(
    root: Path,
    *,
    force: bool = False,
    selected_problem_dirs:
        Iterable[str] | None = None,
) -> dict:
    root = root.resolve()

    config = load_config(root)

    report = {
        "schema_version": 7,
        "model": config.model,
        "generated_solution": [],
        "generated_interview": [],
        "reused_solution": [],
        "reused_interview": [],
        "skipped_no_raw_submission": [],
        "processed": [],
        "failures": [],
        "calls": {
            "total_model_requests": 0,
            "run_limit":
                config.max_calls_per_run,
        },
    }

    if not config.enabled:
        report["status"] = (
            "AI_GENERATION_DISABLED"
        )
        return report

    bundle = load_prompt_bundle(root)
    state = load_state(root)

    budget = CallBudget(
        run_limit=
            config.max_calls_per_run,
        problem_limit=
            config.max_calls_per_problem,
    )

    selected: set[str] | None = None

    if selected_problem_dirs:
        selected = {
            str(
                Path(value)
                .as_posix()
            ).rstrip("/")
            for value
            in selected_problem_dirs
        }

    source_root = (
        root
        / "Data Structures & Algorithms"
    )

    for directory in problem_directories(
        source_root
    ):
        problem_dir = _relative(
            root,
            directory,
        )

        if (
            selected is not None
            and problem_dir
            not in selected
        ):
            continue

        raw = latest_raw_submission(
            directory
        )

        if raw is None:
            report[
                "skipped_no_raw_submission"
            ].append(problem_dir)
            continue

        budget.begin_problem()

        print()
        print(
            f"[AI] {directory.name}"
        )
        print(
            f"[AI] Source: "
            f"{raw.path.name}"
        )

        source_text = read_text(
            raw.path
        )

        source_hash = stable_hash(
            source_text
        )

        authoritative = (
            authoritative_metadata_for_source(
                root,
                directory,
                raw,
                source_text,
            )
        )

        entry = dict(
            state[
                "problems"
            ].get(
                problem_dir,
                {},
            )
        )

        (
            existing_solution_path,
            existing_solution_text,
            existing_solution_validation,
        ) = _valid_existing_solution(
            root,
            entry,
            authoritative_metadata=
                authoritative,
        )

        solution_stale = (
            solution_is_stale(
                force=force,
                entry=entry,
                source_hash=source_hash,
                bundle=bundle,
                existing_text=
                    existing_solution_text,
                existing_validation=
                    existing_solution_validation,
            )
        )

        print(
            "[AI] Solution: "
            + (
                "stale"
                if solution_stale
                else "fresh"
            )
        )

        new_solution = False
        new_interview = False

        try:
            # ============================================================
            # Stage 1
            # ============================================================

            if solution_stale:
                solution_prompt = (
                    build_solution_prompt(
                        bundle,
                        authoritative_metadata=
                            authoritative,
                        source_material=
                            source_text,
                    )
                )

                generated_solution = (
                    generate_with_repair(
                        root=root,
                        directory=
                            directory,
                        artifact_type=
                            "SOLUTION_REFERENCE",
                        initial_prompt=
                            solution_prompt,
                        authoritative_metadata=
                            authoritative,
                        bundle=bundle,
                        config=config,
                        budget=budget,
                    )
                )

                solution_text = (
                    generated_solution.text
                )

                solution_validation = (
                    generated_solution
                    .validation
                )

                new_solution = True

            else:
                assert (
                    existing_solution_text
                    is not None
                )

                assert (
                    existing_solution_validation
                    is not None
                )

                solution_text = (
                    existing_solution_text
                )

                solution_validation = (
                    existing_solution_validation
                )

                report[
                    "reused_solution"
                ].append(problem_dir)

            canonical_metadata = dict(
                solution_validation.metadata
            )

            solution_hash = stable_hash(
                solution_text
            )

            # ============================================================
            # Existing interview lookup
            # ============================================================

            (
                existing_interview_path,
                existing_interview_text,
                existing_interview_validation,
            ) = _valid_existing_interview(
                root,
                entry,
                canonical_metadata=
                    canonical_metadata,
            )

            interview_stale = (
                interview_is_stale(
                    force=force,
                    entry=entry,
                    solution_hash=
                        solution_hash,
                    bundle=bundle,
                    existing_text=
                        existing_interview_text,
                    existing_validation=
                        existing_interview_validation,
                )
            )

            if new_solution:
                interview_stale = True

            print(
                "[AI] Interview: "
                + (
                    "stale"
                    if interview_stale
                    else "fresh"
                )
            )

            # ============================================================
            # Stage 2
            # ============================================================

            if interview_stale:
                interview_prompt = (
                    build_interview_prompt(
                        bundle,
                        canonical_metadata=
                            canonical_metadata,
                        solution_reference=
                            solution_text,
                    )
                )

                generated_interview = (
                    generate_with_repair(
                        root=root,
                        directory=
                            directory,
                        artifact_type=
                            "INTERVIEW_REFERENCE",
                        initial_prompt=
                            interview_prompt,
                        authoritative_metadata=
                            canonical_metadata,
                        bundle=bundle,
                        config=config,
                        budget=budget,
                    )
                )

                interview_text = (
                    generated_interview.text
                )

                interview_validation = (
                    generated_interview
                    .validation
                )

                new_interview = True

            else:
                assert (
                    existing_interview_text
                    is not None
                )

                assert (
                    existing_interview_validation
                    is not None
                )

                interview_text = (
                    existing_interview_text
                )

                interview_validation = (
                    existing_interview_validation
                )

                report[
                    "reused_interview"
                ].append(problem_dir)

            # ============================================================
            # Cross validation
            # ============================================================

            cross = (
                validate_cross_reference(
                    solution_text,
                    interview_text,
                )
            )

            if not cross.valid:
                _log_validation(cross)

                raise RuntimeError(
                    "CROSS_REFERENCE_VALIDATION_FAILED: "
                    + format_validation_errors(
                        cross
                    )
                )

            print(
                "[CROSS-VALIDATION] passed"
            )

            # ============================================================
            # Stale-run guard
            # ============================================================

            current_raw = (
                latest_raw_submission(
                    directory
                )
            )

            if current_raw is None:
                raise RuntimeError(
                    "STALE_RUN: raw submission "
                    "disappeared during generation."
                )

            current_text = read_text(
                current_raw.path
            )

            if (
                current_raw.number
                != raw.number
                or stable_hash(
                    current_text
                )
                != source_hash
            ):
                raise RuntimeError(
                    "STALE_RUN: source changed "
                    "during generation."
                )

            # ============================================================
            # Determine final paths
            # ============================================================

            solution_path = (
                reference_path(
                    root,
                    "solution",
                    canonical_metadata,
                )
            )

            interview_path = (
                reference_path(
                    root,
                    "interview",
                    canonical_metadata,
                )
            )

            # ============================================================
            # Atomic acceptance
            #
            # Both artifacts have already passed:
            #
            #   individual validation
            #   cross validation
            #   stale-source guard
            #
            # before either generated artifact is promoted.
            # ============================================================

            if new_solution:
                atomic_write(
                    solution_path,
                    solution_text,
                )

                report[
                    "generated_solution"
                ].append(problem_dir)

            elif (
                existing_solution_path
                is not None
            ):
                solution_path = (
                    existing_solution_path
                )

            if new_interview:
                atomic_write(
                    interview_path,
                    interview_text,
                )

                report[
                    "generated_interview"
                ].append(problem_dir)

            elif (
                existing_interview_path
                is not None
            ):
                interview_path = (
                    existing_interview_path
                )

            # Remove old generated paths only AFTER new pair is accepted.
            old_solution = entry.get(
                "solution_reference"
            )

            old_interview = entry.get(
                "interview_reference"
            )

            for old_relative, accepted in (
                (
                    old_solution,
                    solution_path,
                ),
                (
                    old_interview,
                    interview_path,
                ),
            ):
                if not old_relative:
                    continue

                old_path = root / old_relative

                if (
                    old_path == accepted
                    or not old_path.exists()
                ):
                    continue

                try:
                    old_path.relative_to(
                        root / "references"
                    )
                except ValueError:
                    continue

                old_path.unlink()

            # ============================================================
            # State
            # ============================================================

            state[
                "problems"
            ][problem_dir] = {
                "problem_dir":
                    problem_dir,

                "source_submission":
                    _relative(
                        root,
                        raw.path,
                    ),

                "source_number":
                    raw.number,

                "source_hash":
                    source_hash,

                "solution_prompt_hash":
                    bundle
                    .solution_prompt_hash,

                "interview_prompt_hash":
                    bundle
                    .interview_prompt_hash,

                "generation_contract_version":
                    bundle
                    .generation_contract_version,

                "solution_contract_version":
                    bundle
                    .solution_contract_version,

                "interview_contract_version":
                    bundle
                    .interview_contract_version,

                "validator_schema_version":
                    VALIDATOR_SCHEMA_VERSION,

                "solution_reference":
                    _relative(
                        root,
                        solution_path,
                    ),

                "interview_reference":
                    _relative(
                        root,
                        interview_path,
                    ),

                # Hash the accepted persisted artifacts, not the
                # pre-write Gemini strings. atomic_write() normalizes
                # trailing whitespace/newlines, so state must describe
                # the exact representation that will be read next run.
                "solution_content_hash":
                    stable_hash(
                        read_text(
                            solution_path
                        )
                    ),

                "interview_content_hash":
                    stable_hash(
                        read_text(
                            interview_path
                        )
                    ),

                "model":
                    config.model,

                "last_problem_model_calls":
                    budget.problem_calls,

                "status":
                    "SUCCESS",
            }

            save_state(
                root,
                state,
            )

            report[
                "processed"
            ].append(problem_dir)

            print(
                "[AI] Accepted pair"
            )

            print(
                "[AI] Problem model calls: "
                f"{budget.problem_calls}/"
                f"{config.max_calls_per_problem}"
            )

            print(
                "[AI] Run model calls: "
                f"{budget.run_calls}/"
                f"{config.max_calls_per_run}"
            )

        except Exception as exc:
            failure = {
                "problem_dir":
                    problem_dir,
                "error":
                    str(exc),
                "problem_model_calls":
                    budget.problem_calls,
            }

            report[
                "failures"
            ].append(failure)

            previous = dict(
                state[
                    "problems"
                ].get(
                    problem_dir,
                    {},
                )
            )

            previous[
                "last_failure"
            ] = failure

            state[
                "problems"
            ][problem_dir] = (
                previous
            )

            save_state(
                root,
                state,
            )

            report[
                "calls"
            ][
                "total_model_requests"
            ] = budget.run_calls

            print()
            print(
                "[AI] Generation failed."
            )
            print(
                "[AI] Accepted references "
                "were not replaced."
            )
            print(
                f"[AI] Error: {exc}"
            )

            raise

    report[
        "calls"
    ][
        "total_model_requests"
    ] = budget.run_calls

    return report
