from neetcode_references.validation import (
    validate_cross_reference,
    validate_interview_reference,
    validate_solution_reference,
)


def solution_text(url="https://neetcode.io/test"):
    return f"""class Solution:
    def solve(self, nums: list[int]) -> bool:
        \"\"\"
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Example
        URL: {url}
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example details.

        @PROBLEM_DETAILS_END
        @CONTENT_START

        [S1]-[Hash Set]

        INT:
        1. Use a set.

        ALGO:
        1. Scan the input.

        TIME: O(n)
        1. Linear scan.

        SPACE: O(n)
        1. The set can grow to n values.

        [APPROACH_COMPARISON]

        S1:
        - Approach: Hash Set
        - Time: O(n)
        - Time qualification: Expected
        - Space: O(n)
        - Input modified: No
        - Main advantage: Fast lookup.
        - Main disadvantage: Extra memory.

        [COMMON_PITFALLS]

        1. Check before insertion.

        @CONTENT_END
        @NC250_END
        \"\"\"
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
"""


def interview_text(url="https://neetcode.io/test"):
    sections = [
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
    ]

    content = "\n\n".join(
        f"{section}\n\n1. Meaningful content."
        for section in sections
    )

    return f"""class Solution:
    def solve(self, nums: list[int]) -> bool:
        \"\"\"
        @NC250_START
        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Example
        URL: {url}
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example details.

        @PROBLEM_DETAILS_END
        @CONTENT_START

{content}

        @CONTENT_END
        @NC250_END
        \"\"\"
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
"""


def codes(result):
    return {
        issue.code
        for issue in result.errors
    }


def test_valid_solution_reference_passes():
    result = validate_solution_reference(
        solution_text(),
        authoritative_metadata={
            "PROBLEM": "Example",
            "URL": "https://neetcode.io/test",
            "DIFFICULTY": "Easy",
        },
    )

    assert result.valid, result.errors


def test_authoritative_url_mismatch_fails():
    result = validate_solution_reference(
        solution_text(
            "https://leetcode.com/wrong"
        ),
        authoritative_metadata={
            "URL": "https://neetcode.io/test",
        },
    )

    assert not result.valid
    assert "URL_MISMATCH" in codes(result)


def test_escaped_marker_fails():
    text = solution_text().replace(
        "@NC250_START",
        "@NC250\\_START",
    )

    result = validate_solution_reference(text)

    assert not result.valid
    assert "MARKER_ESCAPED" in codes(result)


def test_invalid_python_fails():
    text = solution_text().replace(
        "        seen = set()",
        "seen = set()",
    )

    result = validate_solution_reference(text)

    assert not result.valid
    assert "PYTHON_SYNTAX_ERROR" in codes(result)


def test_valid_interview_reference_passes():
    result = validate_interview_reference(
        interview_text(),
        canonical_metadata={
            "PROBLEM": "Example",
            "URL": "https://neetcode.io/test",
            "DIFFICULTY": "Easy",
            "CATEGORY": "Arrays & Hashing",
            "PREFERRED_SOLUTION": "S1",
        },
    )

    assert result.valid, result.errors


def test_cross_reference_passes_for_same_identity_and_code():
    result = validate_cross_reference(
        solution_text(),
        interview_text(),
    )

    assert result.valid, result.errors


def test_cross_reference_rejects_url_change():
    result = validate_cross_reference(
        solution_text(),
        interview_text(
            "https://wrong.test"
        ),
    )

    assert not result.valid
    assert "CROSS_URL_MISMATCH" in codes(result)


def _semantic_quality_solution_fixture(
    *,
    time: str = "O(n)",
    space: str = "O(n)",
) -> str:
    return f"""
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        \"""
        @NC250_START

        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Example
        URL: https://example.test/problem
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [S1]-[Copy]

        INT:
        Copy the input into the required output.

        ALGO:
        1. Build the output.

        TIME: {time}

        SPACE: {space}

        [APPROACH_COMPARISON]

        - Approach: S1
          Time: {time}
          Time qualification: Canonical
          Space: {space}
          Input modified: No
          Main advantage: Simple
          Main disadvantage: Output allocation

        [COMMON_PITFALLS]

        - Example.

        @CONTENT_END
        @NC250_END
        \"""

        return list(nums)
"""


def _semantic_quality_interview_fixture(
    *,
    time_text: str,
    space_text: str,
) -> str:
    return f"""
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        \"""
        @NC250_START

        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Example
        URL: https://example.test/problem
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example.

        @PROBLEM_DETAILS_END

        @CONTENT_START

        [STEP_15_TIME_COMPLEXITY_DERIVATION]

        {time_text}

        [STEP_16_SPACE_COMPLEXITY_DERIVATION]

        {space_text}

        [STEP_17_APPROACH_TRADEOFFS]

        Example.

        @CONTENT_END
        @NC250_END
        \"""

        return list(nums)
"""


def test_cross_complexity_v7_1_accepts_canonical_space_and_auxiliary_detail():
    solution = _semantic_quality_solution_fixture(
        time="O(n)",
        space="O(n)",
    )

    interview = _semantic_quality_interview_fixture(
        time_text=(
            "Canonical time: O(n)."
        ),
        space_text=(
            "Canonical space: O(n) including required output.\\n"
            "Auxiliary space excluding output: O(1)."
        ),
    )

    result = validate_cross_reference(
        solution,
        interview,
    )

    complexity_errors = [
        issue
        for issue in result.errors
        if issue.code in {
            "CROSS_TIME_COMPLEXITY_MISSING",
            "CROSS_TIME_COMPLEXITY_MISMATCH",
            "CROSS_SPACE_COMPLEXITY_MISSING",
            "CROSS_SPACE_COMPLEXITY_MISMATCH",
        }
    ]

    assert complexity_errors == []


def test_cross_complexity_v7_1_rejects_space_convention_switch():
    solution = _semantic_quality_solution_fixture(
        time="O(n)",
        space="O(n)",
    )

    interview = _semantic_quality_interview_fixture(
        time_text=(
            "Canonical time: O(n)."
        ),
        space_text=(
            "Final space complexity: O(1)."
        ),
    )

    result = validate_cross_reference(
        solution,
        interview,
    )

    assert not result.valid

    assert any(
        issue.code
        == "CROSS_SPACE_COMPLEXITY_MISMATCH"
        for issue in result.errors
    )


def test_cross_complexity_v7_1_rejects_time_mismatch():
    solution = _semantic_quality_solution_fixture(
        time="O(n)",
        space="O(1)",
    )

    interview = _semantic_quality_interview_fixture(
        time_text=(
            "Final time complexity: O(log n)."
        ),
        space_text=(
            "Canonical space: O(1)."
        ),
    )

    result = validate_cross_reference(
        solution,
        interview,
    )

    assert not result.valid

    assert any(
        issue.code
        == "CROSS_TIME_COMPLEXITY_MISMATCH"
        for issue in result.errors
    )


def test_cross_complexity_v7_1_allows_missing_step16_candidate():
    """
    Cross-validation checks disagreement, not completeness.

    Missing required Interview structure/content is owned by the
    INTERVIEW_REFERENCE validator.
    """

    solution = _semantic_quality_solution_fixture(
        time="O(n)",
        space="O(n)",
    )

    interview = _semantic_quality_interview_fixture(
        time_text=(
            "Canonical time: O(n)."
        ),
        space_text=(
            "We use a result list."
        ),
    )

    result = validate_cross_reference(
        solution,
        interview,
    )

    complexity_errors = [
        issue
        for issue in result.errors
        if issue.code in {
            "CROSS_TIME_COMPLEXITY_MISMATCH",
            "CROSS_SPACE_COMPLEXITY_MISMATCH",
        }
    ]

    assert complexity_errors == []


def test_interview_validator_owns_required_complexity_structure():
    """
    Required STEP_15 / STEP_16 completeness belongs to the
    INTERVIEW_REFERENCE validator rather than cross-validation.
    """

    interview = _semantic_quality_interview_fixture(
        time_text=(
            "Canonical time: O(n)."
        ),
        space_text=(
            "We use a result list."
        ),
    )

    result = validate_interview_reference(
        interview
    )

    assert not result.valid
