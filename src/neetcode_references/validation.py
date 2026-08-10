"""Structured validation for NC-250 generated references."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Iterable


TYPE_RE = re.compile(
    r"^\s*TYPE\s*:\s*"
    r"(SOLUTION_REFERENCE|INTERVIEW_REFERENCE)"
    r"\s*$",
    re.MULTILINE,
)

SCHEMA_RE = re.compile(
    r"^\s*SCHEMA_VERSION\s*:\s*(\d+)\s*$",
    re.MULTILINE,
)

FIELD_NAMES = (
    "CATEGORY",
    "PREFERRED_SOLUTION",
    "PROBLEM",
    "URL",
    "DIFFICULTY",
)

FIELD_PATTERNS = {
    field_name:
        re.compile(
            rf"^\s*{re.escape(field_name)}"
            rf"\s*:\s*(.*?)\s*$",
            re.MULTILINE,
        )
    for field_name in FIELD_NAMES
}

SOLUTION_HEADER_RE = re.compile(
    r"^\s*\[(S[1-4])\]"
    r"-\[(.+?)\]\s*$",
    re.MULTILINE,
)

INTERVIEW_SECTIONS = (
    "[STEP_1_UNDERSTAND_THE_PROBLEM]",
    "[STEP_2_RESTATE_THE_PROBLEM]",
    "[STEP_3_CLARIFY_AND_CONFIRM]",
    "[STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]",
    "[STEP_5_BASELINE_APPROACH]",
    "[STEP_6_BASELINE_COMPLEXITY]",
    "[STEP_7_FIND_THE_BOTTLENECK]",
    "[STEP_8_OPTIMIZATION_BRIDGE]",
    "[STEP_9_PREFERRED_APPROACH]",
    "[STEP_10_CORRECTNESS_REASONING]",
    "[STEP_11_EXAMPLE_TRACE]",
    "[STEP_12_CODE_PLAN]",
    "[STEP_13_IMPLEMENTATION]",
    "[STEP_14_TEST_CASES]",
    "[STEP_15_TIME_COMPLEXITY_DERIVATION]",
    "[STEP_16_SPACE_COMPLEXITY_DERIVATION]",
    "[STEP_17_APPROACH_TRADEOFFS]",
    "[STEP_18_INTERVIEW_COMMUNICATION]",
    "[INTERVIEW_SCRIPT]",
    "[PATTERN_RECOGNITION]",
    "[COMMON_PITFALLS]",
    "[FINAL_REVIEW_CHECKLIST]",
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: str = "ERROR"
    expected: str | None = None
    actual: str | None = None


@dataclass
class ValidationResult:
    artifact_type: str
    valid: bool = True
    errors: list[ValidationIssue] = (
        field(default_factory=list)
    )
    warnings: list[ValidationIssue] = (
        field(default_factory=list)
    )
    metadata: dict[str, str] = (
        field(default_factory=dict)
    )

    def add_error(
        self,
        code: str,
        message: str,
        *,
        expected: str | None = None,
        actual: str | None = None,
    ) -> None:
        self.valid = False

        self.errors.append(
            ValidationIssue(
                code=code,
                message=message,
                severity="ERROR",
                expected=expected,
                actual=actual,
            )
        )

    def add_warning(
        self,
        code: str,
        message: str,
    ) -> None:
        self.warnings.append(
            ValidationIssue(
                code=code,
                message=message,
                severity="WARNING",
            )
        )


def extract_docstring(
    text: str,
) -> str | None:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.Module,
                ast.ClassDef,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            value = ast.get_docstring(
                node,
                clean=False,
            )

            if (
                value
                and "@NC250_START" in value
            ):
                return value

    return None


def extract_metadata(
    text: str,
) -> dict[str, str]:
    source = extract_docstring(text)

    if source is None:
        source = text

    metadata: dict[str, str] = {}

    type_match = TYPE_RE.search(source)

    if type_match:
        metadata["TYPE"] = (
            type_match.group(1).strip()
        )

    schema_match = SCHEMA_RE.search(
        source
    )

    if schema_match:
        metadata["SCHEMA_VERSION"] = (
            schema_match.group(1).strip()
        )

    for field_name, pattern in (
        FIELD_PATTERNS.items()
    ):
        match = pattern.search(source)

        if match:
            metadata[field_name] = (
                match.group(1).strip()
            )

    return metadata


def _marker_count(
    source: str,
    marker: str,
) -> int:
    return source.count(marker)


def _validate_marker(
    result: ValidationResult,
    source: str,
    marker: str,
    *,
    prefix: str,
) -> None:
    count = _marker_count(
        source,
        marker,
    )

    if count == 0:
        result.add_error(
            f"{prefix}_MISSING",
            f"Missing required marker "
            f"{marker}.",
        )

    elif count > 1:
        result.add_error(
            f"{prefix}_DUPLICATE",
            f"Required marker {marker} "
            f"appears {count} times.",
            expected="1",
            actual=str(count),
        )


def _check_order(
    result: ValidationResult,
    source: str,
    markers: Iterable[str],
    *,
    code: str,
) -> None:
    positions: list[int] = []

    for marker in markers:
        position = source.find(marker)

        if position < 0:
            return

        positions.append(position)

    if positions != sorted(positions):
        result.add_error(
            code,
            "Required markers are not in "
            "the expected order.",
        )


def _contains_unresolved_placeholder(
    source: str,
) -> bool:
    obvious = (
        "O(...)",
        "NotImplementedError",
        "TODO",
        "[APPROACH NAME]",
        "[PROBLEM_NAME]",
        "[CATEGORY_OR_UNKNOWN]",
        "[DEFINE ",
        "[IDENTIFY ",
        "[STATE ",
        "[EXPLAIN ",
        "[COPY AND PASTE",
    )

    return any(
        item in source
        for item in obvious
    )


def _normalized_metadata_key(
    key: str,
) -> str:
    return key.strip().upper()


def validate_common(
    text: str,
    expected_type: str,
    *,
    authoritative_metadata:
        dict[str, str] | None = None,
) -> ValidationResult:
    result = ValidationResult(
        artifact_type=expected_type
    )

    if not text.strip():
        result.add_error(
            "EMPTY_RESPONSE",
            "Generated response is empty.",
        )
        return result

    stripped = text.strip()

    if (
        stripped.startswith("```")
        or stripped.endswith("```")
    ):
        result.add_error(
            "MARKDOWN_FENCE_PRESENT",
            "Automation output contains "
            "Markdown code fences.",
        )

    if (
        "@NC250\\_START" in text
        or "@NC250\\_END" in text
        or "SOLUTION\\_REFERENCE" in text
        or "INTERVIEW\\_REFERENCE" in text
    ):
        result.add_error(
            "MARKER_ESCAPED",
            "NC-250 marker or reference type "
            "contains escaped underscores.",
        )

    try:
        ast.parse(text)
    except SyntaxError as exc:
        result.add_error(
            "PYTHON_SYNTAX_ERROR",
            (
                f"Python syntax error at "
                f"line {exc.lineno}: "
                f"{exc.msg}"
            ),
        )

    source = extract_docstring(text)

    if source is None:
        source = text

    _validate_marker(
        result,
        source,
        "@NC250_START",
        prefix="NC250_START",
    )

    _validate_marker(
        result,
        source,
        "@NC250_END",
        prefix="NC250_END",
    )

    _validate_marker(
        result,
        source,
        "@PROBLEM_DETAILS_START",
        prefix="PROBLEM_DETAILS_START",
    )

    _validate_marker(
        result,
        source,
        "@PROBLEM_DETAILS_END",
        prefix="PROBLEM_DETAILS_END",
    )

    _validate_marker(
        result,
        source,
        "@CONTENT_START",
        prefix="CONTENT_START",
    )

    _validate_marker(
        result,
        source,
        "@CONTENT_END",
        prefix="CONTENT_END",
    )

    _check_order(
        result,
        source,
        (
            "@NC250_START",
            "@PROBLEM_DETAILS_START",
            "@PROBLEM_DETAILS_END",
            "@CONTENT_START",
            "@CONTENT_END",
            "@NC250_END",
        ),
        code="MARKER_ORDER_INVALID",
    )

    metadata = extract_metadata(text)
    result.metadata = metadata

    actual_type = metadata.get("TYPE")

    if actual_type is None:
        result.add_error(
            "TYPE_MISSING",
            "TYPE metadata is missing.",
            expected=expected_type,
        )

    elif actual_type != expected_type:
        result.add_error(
            "TYPE_MISMATCH",
            "TYPE metadata does not match "
            "the expected artifact.",
            expected=expected_type,
            actual=actual_type,
        )

    schema = metadata.get(
        "SCHEMA_VERSION"
    )

    if schema is None:
        result.add_error(
            "SCHEMA_VERSION_MISSING",
            "SCHEMA_VERSION is missing.",
            expected="1",
        )

    elif schema != "1":
        result.add_error(
            "SCHEMA_VERSION_MISMATCH",
            "SCHEMA_VERSION must be 1.",
            expected="1",
            actual=schema,
        )

    for field_name in (
        "CATEGORY",
        "PREFERRED_SOLUTION",
        "PROBLEM",
        "URL",
        "DIFFICULTY",
    ):
        value = metadata.get(field_name)

        if not value:
            result.add_error(
                f"{field_name}_MISSING",
                f"{field_name} metadata "
                f"is missing.",
            )

    if authoritative_metadata:
        for raw_key, expected in (
            authoritative_metadata.items()
        ):
            key = _normalized_metadata_key(
                raw_key
            )

            if key not in {
                "PROBLEM",
                "URL",
                "DIFFICULTY",
                "CATEGORY",
                "PREFERRED_SOLUTION",
            }:
                continue

            if (
                not expected
                or expected in {
                    "INFER_ALLOWED",
                    "Unknown",
                }
            ):
                continue

            actual = metadata.get(key)

            if (
                actual is not None
                and actual != expected
            ):
                result.add_error(
                    f"{key}_MISMATCH",
                    (
                        f"{key} changed from "
                        "authoritative metadata."
                    ),
                    expected=expected,
                    actual=actual,
                )

    if _contains_unresolved_placeholder(
        source
    ):
        result.add_error(
            "UNRESOLVED_PLACEHOLDER",
            "Generated artifact contains "
            "an unresolved template value.",
        )

    if (
        "@NC250_START" in source
        and "@NC250_END" not in source
    ):
        result.add_error(
            "OUTPUT_TRUNCATED",
            "Artifact begins an NC-250 "
            "reference but does not finish it.",
        )

    return result


def _solution_blocks(
    source: str,
) -> list[tuple[str, str, int, int]]:
    matches = list(
        SOLUTION_HEADER_RE.finditer(
            source
        )
    )

    blocks: list[
        tuple[str, str, int, int]
    ] = []

    for index, match in enumerate(
        matches
    ):
        start = match.end()

        if index + 1 < len(matches):
            end = matches[
                index + 1
            ].start()
        else:
            comparison = source.find(
                "[APPROACH_COMPARISON]",
                start,
            )

            end = (
                comparison
                if comparison >= 0
                else len(source)
            )

        blocks.append(
            (
                match.group(1),
                match.group(2).strip(),
                start,
                end,
            )
        )

    return blocks


def _find_reference_function(
    text: str,
) -> tuple[
    str | None,
    ast.FunctionDef | ast.AsyncFunctionDef | None,
]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None, None

    for node in tree.body:
        if not isinstance(
            node,
            ast.ClassDef,
        ):
            continue

        for child in node.body:
            if not isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                continue

            doc = ast.get_docstring(
                child,
                clean=False,
            )

            if (
                doc
                and "@NC250_START" in doc
            ):
                return node.name, child

    return None, None


def canonical_signature(
    text: str,
) -> str | None:
    class_name, function = (
        _find_reference_function(text)
    )

    if (
        class_name is None
        or function is None
    ):
        return None

    args = function.args

    payload = ast.dump(
        ast.arguments(
            posonlyargs=args.posonlyargs,
            args=args.args,
            vararg=args.vararg,
            kwonlyargs=args.kwonlyargs,
            kw_defaults=args.kw_defaults,
            kwarg=args.kwarg,
            defaults=args.defaults,
        ),
        include_attributes=False,
    )

    returns = (
        ast.dump(
            function.returns,
            include_attributes=False,
        )
        if function.returns
        else "None"
    )

    return (
        f"{class_name}."
        f"{function.name}:"
        f"{payload}:"
        f"{returns}"
    )


def canonical_implementation(
    text: str,
) -> str | None:
    _, function = (
        _find_reference_function(text)
    )

    if function is None:
        return None

    body = list(function.body)

    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(
            body[0].value,
            ast.Constant,
        )
        and isinstance(
            body[0].value.value,
            str,
        )
    ):
        body = body[1:]

    synthetic = ast.Module(
        body=body,
        type_ignores=[],
    )

    return ast.dump(
        synthetic,
        include_attributes=False,
    )


def validate_solution_reference(
    text: str,
    *,
    authoritative_metadata:
        dict[str, str] | None = None,
) -> ValidationResult:
    result = validate_common(
        text,
        "SOLUTION_REFERENCE",
        authoritative_metadata=
            authoritative_metadata,
    )

    source = (
        extract_docstring(text)
        or text
    )

    blocks = _solution_blocks(source)

    if not blocks:
        result.add_error(
            "SOLUTION_SECTION_MISSING",
            "No [S#]-[APPROACH NAME] "
            "section was found.",
        )
        return result

    labels = [
        item[0]
        for item in blocks
    ]

    if len(labels) != len(set(labels)):
        result.add_error(
            "SOLUTION_LABEL_DUPLICATE",
            "Solution labels are duplicated.",
        )

    expected_labels = [
        f"S{i}"
        for i in range(
            1,
            len(labels) + 1,
        )
    ]

    if labels != expected_labels:
        result.add_error(
            "SOLUTION_LABEL_GAP",
            "Solution labels must be "
            "contiguous and ordered.",
            expected=", ".join(
                expected_labels
            ),
            actual=", ".join(labels),
        )

    preferred = result.metadata.get(
        "PREFERRED_SOLUTION"
    )

    if preferred not in labels:
        result.add_error(
            "PREFERRED_SOLUTION_INVALID",
            "PREFERRED_SOLUTION does not "
            "reference a surviving solution.",
            expected=", ".join(labels),
            actual=preferred,
        )

    for (
        label,
        _name,
        start,
        end,
    ) in blocks:
        block = source[start:end]

        for section_name in (
            "INT:",
            "ALGO:",
            "TIME:",
            "SPACE:",
        ):
            if section_name not in block:
                result.add_error(
                    (
                        f"{section_name[:-1]}"
                        "_MISSING"
                    ),
                    (
                        f"{label} is missing "
                        f"{section_name}"
                    ),
                )

    if (
        source.count(
            "[APPROACH_COMPARISON]"
        )
        != 1
    ):
        result.add_error(
            "APPROACH_COMPARISON_MISSING",
            "[APPROACH_COMPARISON] must "
            "appear exactly once.",
        )

    if (
        source.count(
            "[COMMON_PITFALLS]"
        )
        != 1
    ):
        result.add_error(
            "COMMON_PITFALLS_MISSING",
            "[COMMON_PITFALLS] must appear "
            "exactly once.",
        )

    class_name, function = (
        _find_reference_function(text)
    )

    if (
        class_name is None
        or function is None
    ):
        result.add_error(
            "PREFERRED_IMPLEMENTATION_MISSING",
            "Could not locate the active "
            "reference class/method.",
        )

    else:
        implementation = (
            canonical_implementation(text)
        )

        if (
            implementation is None
            or implementation.endswith(
                "body=[]"
            )
        ):
            result.add_error(
                "INCOMPLETE_IMPLEMENTATION",
                "Preferred implementation "
                "contains no executable body.",
            )

    return result


def _section_content(
    source: str,
    marker: str,
    markers: tuple[str, ...],
) -> str:
    start = source.find(marker)

    if start < 0:
        return ""

    start += len(marker)

    later = [
        source.find(
            other,
            start,
        )
        for other in markers
        if other != marker
    ]

    later = [
        value
        for value in later
        if value >= 0
    ]

    content_end = source.find(
        "@CONTENT_END",
        start,
    )

    if content_end >= 0:
        later.append(content_end)

    end = (
        min(later)
        if later
        else len(source)
    )

    return source[start:end].strip()


def validate_interview_reference(
    text: str,
    *,
    canonical_metadata:
        dict[str, str] | None = None,
) -> ValidationResult:
    result = validate_common(
        text,
        "INTERVIEW_REFERENCE",
        authoritative_metadata=
            canonical_metadata,
    )

    source = (
        extract_docstring(text)
        or text
    )

    for marker in INTERVIEW_SECTIONS:
        count = source.count(marker)

        if count == 0:
            result.add_error(
                "INTERVIEW_SECTION_MISSING",
                f"Missing required section "
                f"{marker}.",
            )

        elif count > 1:
            result.add_error(
                "INTERVIEW_SECTION_DUPLICATE",
                f"Section {marker} appears "
                f"{count} times.",
            )

    _check_order(
        result,
        source,
        INTERVIEW_SECTIONS,
        code=
            "INTERVIEW_SECTION_ORDER_INVALID",
    )

    for marker in INTERVIEW_SECTIONS:
        if source.count(marker) != 1:
            continue

        content = _section_content(
            source,
            marker,
            INTERVIEW_SECTIONS,
        )

        if not content:
            result.add_error(
                "INTERVIEW_SECTION_EMPTY",
                f"Section {marker} is empty.",
            )

    _, function = (
        _find_reference_function(text)
    )

    if function is None:
        result.add_error(
            "PREFERRED_IMPLEMENTATION_MISSING",
            "Could not locate canonical "
            "preferred implementation.",
        )

    # NC250_V7_3B_INTERVIEW_SEMANTIC_CALL
    _validate_interview_semantic_safety(
        result,
        source,
    )

    return result


def _normalize_complexity_headline(
    value: str,
) -> str:
    """
    Normalize whitespace only for deterministic Big-O comparison.

    This deliberately does not attempt algebraic equivalence.

    Examples:

        O(n)       -> O(n)
        O( n )     -> O(n)
        O(n + m)   -> O(n+m)
    """

    return re.sub(
        r"\s+",
        "",
        value.strip(),
    )


def _solution_approach_blocks(
    text: str,
) -> dict[str, str]:
    """
    Extract [S1]...[S4] documentation blocks from a SOLUTION_REFERENCE.

    Only the preferred block is later used for canonical TIME/SPACE.
    """

    docstring = extract_docstring(
        text
    )

    source = (
        docstring
        if docstring is not None
        else text
    )

    headers = list(
        re.finditer(
            r"(?m)^\s*\[(S[1-4])\]-\[[^\]]+\]\s*$",
            source,
        )
    )

    blocks: dict[str, str] = {}

    for index, match in enumerate(
        headers
    ):
        label = match.group(1)

        start = match.end()

        if index + 1 < len(headers):
            end = headers[
                index + 1
            ].start()
        else:
            comparison = re.search(
                r"(?m)^\s*\[APPROACH_COMPARISON\]\s*$",
                source[start:],
            )

            if comparison:
                end = (
                    start
                    + comparison.start()
                )
            else:
                end = len(source)

        blocks[label] = source[
            start:end
        ]

    return blocks


def preferred_solution_complexities(
    solution_text: str,
) -> tuple[str | None, str | None]:
    """
    Return canonical preferred (TIME, SPACE) headlines from Solution.
    """

    metadata = extract_metadata(
        solution_text
    )

    preferred = metadata.get(
        "PREFERRED_SOLUTION"
    )

    if preferred not in {
        "S1",
        "S2",
        "S3",
        "S4",
    }:
        return None, None

    block = _solution_approach_blocks(
        solution_text
    ).get(
        preferred
    )

    if not block:
        return None, None

    time_match = re.search(
        r"(?m)^\s*TIME\s*:\s*(O\([^\n]+\))\s*$",
        block,
    )

    space_match = re.search(
        r"(?m)^\s*SPACE\s*:\s*(O\([^\n]+\))\s*$",
        block,
    )

    canonical_time = (
        _normalize_complexity_headline(
            time_match.group(1)
        )
        if time_match
        else None
    )

    canonical_space = (
        _normalize_complexity_headline(
            space_match.group(1)
        )
        if space_match
        else None
    )

    return (
        canonical_time,
        canonical_space,
    )


def _interview_complexity_section(
    interview_text: str,
    *,
    start_marker: str,
    end_marker: str,
) -> str:
    docstring = extract_docstring(
        interview_text
    )

    source = (
        docstring
        if docstring is not None
        else interview_text
    )

    start = source.find(
        start_marker
    )

    if start < 0:
        return ""

    start += len(
        start_marker
    )

    end = source.find(
        end_marker,
        start,
    )

    if end < 0:
        end = len(source)

    return source[
        start:end
    ]


def _interview_complexity_candidates(
    interview_text: str,
    *,
    kind: str,
) -> list[str]:
    """
    Extract Big-O values only from STEP_15 or STEP_16.

    This avoids confusing baseline complexities in earlier sections with
    preferred/canonical complexity conclusions.
    """

    if kind == "TIME":
        block = _interview_complexity_section(
            interview_text,
            start_marker=(
                "[STEP_15_TIME_COMPLEXITY_DERIVATION]"
            ),
            end_marker=(
                "[STEP_16_SPACE_COMPLEXITY_DERIVATION]"
            ),
        )

    elif kind == "SPACE":
        block = _interview_complexity_section(
            interview_text,
            start_marker=(
                "[STEP_16_SPACE_COMPLEXITY_DERIVATION]"
            ),
            end_marker=(
                "[STEP_17_APPROACH_TRADEOFFS]"
            ),
        )

    else:
        raise ValueError(
            f"Unsupported complexity kind: {kind}"
        )

    candidates: list[str] = []

    for value in re.findall(
        r"O\([^)\n]+\)",
        block,
    ):
        normalized = (
            _normalize_complexity_headline(
                value
            )
        )

        if normalized not in candidates:
            candidates.append(
                normalized
            )

    return candidates


def validate_cross_reference(
    solution_text: str,
    interview_text: str,
) -> ValidationResult:
    result = ValidationResult(
        artifact_type="CROSS_REFERENCE"
    )

    solution = extract_metadata(
        solution_text
    )

    interview = extract_metadata(
        interview_text
    )

    mapping = (
        ("PROBLEM", "CROSS_PROBLEM_MISMATCH"),
        ("URL", "CROSS_URL_MISMATCH"),
        (
            "DIFFICULTY",
            "CROSS_DIFFICULTY_MISMATCH",
        ),
        (
            "CATEGORY",
            "CROSS_CATEGORY_MISMATCH",
        ),
        (
            "PREFERRED_SOLUTION",
            "CROSS_PREFERRED_SOLUTION_MISMATCH",
        ),
    )

    for key, code in mapping:
        expected = solution.get(key)
        actual = interview.get(key)

        if expected != actual:
            result.add_error(
                code,
                f"{key} differs between "
                "SOLUTION_REFERENCE and "
                "INTERVIEW_REFERENCE.",
                expected=expected,
                actual=actual,
            )

    solution_signature = (
        canonical_signature(solution_text)
    )

    interview_signature = (
        canonical_signature(
            interview_text
        )
    )

    if (
        solution_signature
        != interview_signature
    ):
        result.add_error(
            "CROSS_SIGNATURE_MISMATCH",
            "Class/method signature differs "
            "between references.",
            expected=solution_signature,
            actual=interview_signature,
        )

    solution_impl = (
        canonical_implementation(
            solution_text
        )
    )

    interview_impl = (
        canonical_implementation(
            interview_text
        )
    )

    if solution_impl != interview_impl:
        result.add_error(
            "CROSS_IMPLEMENTATION_MISMATCH",
            "Preferred executable "
            "implementation changed in "
            "INTERVIEW_REFERENCE.",
        )


    # CROSS_COMPLEXITY_CONSISTENCY_V7_1
    canonical_time, canonical_space = (
        preferred_solution_complexities(
            solution_text
        )
    )

    if canonical_time:
        interview_time = (
            _interview_complexity_candidates(
                interview_text,
                kind="TIME",
            )
        )

        if (
            interview_time
            and canonical_time not in interview_time
        ):
            result.add_error(
                "CROSS_TIME_COMPLEXITY_MISMATCH",
                (
                    "Preferred TIME complexity differs "
                    "between SOLUTION_REFERENCE and "
                    "INTERVIEW_REFERENCE."
                ),
                expected=canonical_time,
                actual=", ".join(
                    interview_time
                ),
            )

    if canonical_space:
        interview_space = (
            _interview_complexity_candidates(
                interview_text,
                kind="SPACE",
            )
        )

        if (
            interview_space
            and canonical_space not in interview_space
        ):
            result.add_error(
                "CROSS_SPACE_COMPLEXITY_MISMATCH",
                (
                    "Preferred SPACE complexity differs "
                    "between SOLUTION_REFERENCE and "
                    "INTERVIEW_REFERENCE."
                ),
                expected=canonical_space,
                actual=", ".join(
                    interview_space
                ),
            )

    return result


def format_validation_errors(
    result: ValidationResult,
) -> str:
    return "; ".join(
        issue.code
        for issue in result.errors
    )

# NC250_V7_3B_INTERVIEW_SEMANTIC_HELPERS

_UNSAFE_DOCSTRING_LATEX_RE = re.compile(
    r"""\\(?:le|ge|frac|text|times|cdot|sqrt|log|sum|begin|end)\b"""
)

_UNSUPPORTED_INTERVIEW_PHRASES = (
    "standard memory limits",
    "standard memory limit",
    "in most interview scenarios",
    "in most interviews",
    "time is prioritized over space",
    "time complexity is prioritized over space",
    "highly acceptable",
    "highly favorable",
    "the optimal solution",
    "optimal solution",
    "optimal time complexity",
    "the most efficient approach",
    "fastest expected runtime",
)


def _validate_interview_semantic_safety(
    result: ValidationResult,
    source: str,
) -> None:
    """
    Validate deterministic semantic-safety rules for INTERVIEW_REFERENCE.

    This is intentionally narrow.

    It does not attempt general semantic correctness. It only rejects
    known unsafe Python-docstring notation and unsupported interview /
    optimization claims that Prompt 2 is explicitly forbidden to emit.
    """

    unsafe_latex = sorted(
        set(
            _UNSAFE_DOCSTRING_LATEX_RE.findall(
                source
            )
        )
    )

    if unsafe_latex:
        result.add_error(
            "UNSAFE_DOCSTRING_LATEX",
            (
                "INTERVIEW_REFERENCE contains backslash-based "
                "LaTeX commands inside the generated Python "
                "docstring. Use Python-safe plain-text mathematical "
                "notation instead."
            ),
            expected=(
                "Plain text such as O(n), 0 <= i < n, "
                "or n(n - 1) / 2"
            ),
            actual=", ".join(
                unsafe_latex
            ),
        )

    lowered = source.lower()

    found_phrases = [
        phrase
        for phrase in _UNSUPPORTED_INTERVIEW_PHRASES
        if phrase in lowered
    ]

    if found_phrases:
        result.add_error(
            "UNSUPPORTED_INTERVIEW_ASSUMPTION",
            (
                "INTERVIEW_REFERENCE contains unsupported "
                "interview, memory-limit, efficiency, or "
                "optimality language. Claims must remain grounded "
                "in the accepted Solution and authoritative "
                "problem metadata."
            ),
            expected=(
                "Evidence-bound wording with no invented "
                "interviewer preference, memory assumption, "
                "or global optimality claim"
            ),
            actual=", ".join(
                found_phrases
            ),
        )

