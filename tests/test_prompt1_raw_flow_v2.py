"""Prompt 1 v2 raw-template flow regression tests."""

from pathlib import Path

from neetcode_references.ai import (
    authoritative_metadata_for_source,
    classify_submission_text,
    extract_source_metadata,
    latest_raw_submission,
    raw_submission,
)


def test_plain_submission_is_raw():
    text = """
class Solution:
    def solve(self, nums):
        return nums
"""

    result = classify_submission_text(text)

    assert result.kind == "RAW"


def test_new_raw_schema_is_raw():
    text = """
class Solution:
    def solve(self, nums):
        \"""
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy

        PREFERRED_SOLUTION: [OPTIONAL]

        @NC250_RAW_END
        \"""
        return nums
"""

    result = classify_submission_text(text)

    assert result.kind == "RAW"
    assert "raw template" in result.reason


def test_legacy_typed_template_with_placeholders_is_still_raw():
    text = """
class Solution:
    def solve(self, nums):
        \"""
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: [S1 | S2 | S3 | S4]

        @PROBLEM_DETAILS_START

        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example.

        @PROBLEM_DETAILS_END
        @CONTENT_START

        [S1]-[APPROACH NAME]

        TIME: O(...)
        SPACE: O(...)

        @CONTENT_END
        @NC250_END
        \"""
        return nums
"""

    result = classify_submission_text(text)

    assert result.kind == "RAW"
    assert result.reference_type == "SOLUTION_REFERENCE"


def test_completed_solution_reference_is_not_raw():
    text = """
class Solution:
    def solve(self, nums):
        \"""
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example.

        @PROBLEM_DETAILS_END
        @CONTENT_START

        [S1]-[Hash Set]

        INT:
        1. Use a set.

        ALGO:
        1. Scan.

        TIME: O(n)

        SPACE: O(n)

        [APPROACH_COMPARISON]

        S1:
        - Approach: Hash Set

        [COMMON_PITFALLS]

        1. Example.

        @CONTENT_END
        @NC250_END
        \"""
        return nums
"""

    result = classify_submission_text(text)

    assert result.kind == "SOLUTION_REFERENCE"


def test_completed_interview_reference_is_not_raw():
    text = """
class Solution:
    def solve(self, nums):
        \"""
        @NC250_START
        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START
        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        PROBLEM DETAILS:
        Example.
        @PROBLEM_DETAILS_END

        @CONTENT_START
        [STEP_1_UNDERSTAND_THE_PROBLEM]
        Complete.
        @CONTENT_END
        @NC250_END
        \"""
        return nums
"""

    result = classify_submission_text(text)

    assert result.kind == "INTERVIEW_REFERENCE"


def test_latest_raw_submission_prefers_highest_numeric_raw(tmp_path: Path):
    (tmp_path / "submission-1.py").write_text(
        "class Solution:\n    pass\n",
        encoding="utf-8",
    )

    (tmp_path / "submission-2.py").write_text(
        """
class Solution:
    def solve(self):
        \"""
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays
        PREFERRED_SOLUTION: S1
        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        \"""
        return None
""",
        encoding="utf-8",
    )

    (tmp_path / "submission-3.py").write_text(
        """
class Solution:
    def solve(self):
        \"""
        TYPE: INTERVIEW_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays
        PREFERRED_SOLUTION: S1
        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        \"""
        return None
""",
        encoding="utf-8",
    )

    (tmp_path / "submission-4.py").write_text(
        """
class Solution:
    def solve(self):
        \"""
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1
        PROBLEM: Example
        PREFERRED_SOLUTION: [OPTIONAL]
        TIME: O(...)
        @NC250_RAW_END
        \"""
        return None
""",
        encoding="utf-8",
    )

    found = latest_raw_submission(tmp_path)

    assert found is not None
    assert found.number == 4
    assert found.path.name == "submission-4.py"


def test_completed_reference_after_latest_raw_is_still_skipped(tmp_path: Path):
    (tmp_path / "submission-4.py").write_text(
        """
class Solution:
    def solve(self):
        \"""
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1
        PREFERRED_SOLUTION: [OPTIONAL]
        @NC250_RAW_END
        \"""
        return None
""",
        encoding="utf-8",
    )

    (tmp_path / "submission-5.py").write_text(
        """
class Solution:
    def solve(self):
        \"""
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1
        CATEGORY: Arrays
        PREFERRED_SOLUTION: S1
        PROBLEM: Example
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        \"""
        return None
""",
        encoding="utf-8",
    )

    found = latest_raw_submission(tmp_path)

    assert found is not None
    assert found.number == 4


def test_preferred_placeholder_is_not_authoritative():
    text = """
PROBLEM: Concatenation of Array
URL: https://neetcode.io/problems/concatenation-of-array/solution
DIFFICULTY: Easy
CATEGORY: Arrays & Hashing
PREFERRED_SOLUTION: [S1 | S2 | S3 | S4]
"""

    metadata = extract_source_metadata(text)

    assert metadata["PROBLEM"] == "Concatenation of Array"
    assert metadata["URL"] == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )
    assert metadata["DIFFICULTY"] == "Easy"
    assert metadata["CATEGORY"] == "Arrays & Hashing"
    assert "PREFERRED_SOLUTION" not in metadata


def test_markdown_url_is_extracted_as_authoritative_target():
    text = """
PROBLEM: Concatenation of Array
URL: [https://neetcode.io/problems/concatenation-of-array/solution](https://neetcode.io/problems/concatenation-of-array/solution)
DIFFICULTY: [Easy]
CATEGORY: Arrays & Hashing
"""

    metadata = extract_source_metadata(text)

    assert metadata["URL"] == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )

    assert metadata["DIFFICULTY"] == "Easy"


def test_authoritative_metadata_from_raw_template(tmp_path: Path):
    root = tmp_path

    directory = (
        root
        / "Data Structures & Algorithms"
        / "concatenation-of-array"
    )

    directory.mkdir(parents=True)

    path = directory / "submission-7.py"

    text = """
class Solution:
    def solve(self):
        \"""
        @NC250_RAW_START
        RAW_SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: [OPTIONAL]

        PROBLEM: Concatenation of Array
        URL: https://neetcode.io/problems/concatenation-of-array/solution
        DIFFICULTY: Easy

        TIME: O(...)

        @NC250_RAW_END
        \"""
        return None
"""

    path.write_text(
        text,
        encoding="utf-8",
    )

    raw = raw_submission(path)

    assert raw is not None

    metadata = authoritative_metadata_for_source(
        root,
        directory,
        raw,
        text,
    )

    assert metadata["SOURCE_SUBMISSION"] == "submission-7.py"
    assert metadata["PROBLEM"] == "Concatenation of Array"
    assert metadata["URL"] == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )
    assert metadata["DIFFICULTY"] == "Easy"
    assert metadata["CATEGORY"] == "Arrays & Hashing"

    assert "PREFERRED_SOLUTION" not in metadata


def test_real_world_markdown_url_field_is_normalized():
    text = """
CATEGORY: Arrays & Hashing
PREFERRED_SOLUTION: [S1 | S2 | S3 | S4]

PROBLEM: Concatenation of Array
URL: [https://neetcode.io/problems/concatenation-of-array/solution](https://neetcode.io/problems/concatenation-of-array/solution)
DIFFICULTY: [Easy]
"""

    metadata = extract_source_metadata(text)

    assert metadata["PROBLEM"] == "Concatenation of Array"
    assert metadata["URL"] == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )
    assert metadata["DIFFICULTY"] == "Easy"
    assert metadata["CATEGORY"] == "Arrays & Hashing"
    assert "PREFERRED_SOLUTION" not in metadata


def test_escaped_markdown_url_field_is_normalized():
    text = r"""
PROBLEM: Concatenation of Array
URL: \[https://neetcode.io/problems/concatenation-of-array/solution\]\(https://neetcode.io/problems/concatenation-of-array/solution\)
DIFFICULTY: [Easy]
"""

    metadata = extract_source_metadata(text)

    assert metadata["URL"] == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )


def test_untouched_raw_template_metadata_is_not_authoritative():
    text = """
@NC250_RAW_START
RAW_SCHEMA_VERSION: 1

CATEGORY: [OPTIONAL]
PREFERRED_SOLUTION: [OPTIONAL]

PROBLEM: [PASTE PROBLEM NAME]

URL: [PASTE ORIGINAL PROBLEM URL]

DIFFICULTY: [Easy | Medium | Hard | Unknown]

@NC250_RAW_END
"""

    metadata = extract_source_metadata(text)

    assert metadata == {}


def test_unbracketed_raw_template_instructions_are_not_authoritative():
    text = """
CATEGORY: OPTIONAL
PREFERRED_SOLUTION: OPTIONAL
PROBLEM: PASTE PROBLEM NAME
URL: PASTE ORIGINAL PROBLEM URL
DIFFICULTY: Easy | Medium | Hard | Unknown
"""

    metadata = extract_source_metadata(text)

    assert metadata == {}


def test_filled_raw_template_metadata_is_authoritative():
    text = """
@NC250_RAW_START
RAW_SCHEMA_VERSION: 1

CATEGORY: Arrays & Hashing
PREFERRED_SOLUTION: [OPTIONAL]

PROBLEM: Concatenation of Array

URL: https://neetcode.io/problems/concatenation-of-array/solution

DIFFICULTY: Easy

@NC250_RAW_END
"""

    metadata = extract_source_metadata(text)

    assert metadata == {
        "CATEGORY": "Arrays & Hashing",
        "PROBLEM": "Concatenation of Array",
        "URL": (
            "https://neetcode.io/problems/"
            "concatenation-of-array/solution"
        ),
        "DIFFICULTY": "Easy",
    }


def test_filled_markdown_url_is_normalized():
    text = """
PROBLEM: Concatenation of Array
URL: [https://neetcode.io/problems/concatenation-of-array/solution](https://neetcode.io/problems/concatenation-of-array/solution)
DIFFICULTY: [Easy]
CATEGORY: Arrays & Hashing
"""

    metadata = extract_source_metadata(text)

    assert metadata["URL"] == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )

    assert metadata["DIFFICULTY"] == "Easy"


def test_literal_unknown_metadata_is_not_promoted_to_authoritative():
    text = """
PROBLEM: Example
URL: Unknown
DIFFICULTY: Unknown
CATEGORY: Unknown
PREFERRED_SOLUTION: Unknown
"""

    metadata = extract_source_metadata(text)

    assert metadata == {
        "PROBLEM": "Example",
    }


def test_markdown_url_cleaner_directly_returns_target():
    from neetcode_references.ai import _clean_source_value

    value = (
        "[https://neetcode.io/problems/"
        "concatenation-of-array/solution]"
        "(https://neetcode.io/problems/"
        "concatenation-of-array/solution)"
    )

    assert _clean_source_value(value) == (
        "https://neetcode.io/problems/"
        "concatenation-of-array/solution"
    )


def test_real_submission_style_markdown_url_metadata_is_clean():
    text = """
        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: [OPTIONAL]

        PROBLEM: Concatenation of Array

        URL: [https://neetcode.io/problems/concatenation-of-array/solution](https://neetcode.io/problems/concatenation-of-array/solution)

        DIFFICULTY: Easy
    """

    metadata = extract_source_metadata(text)

    assert metadata == {
        "CATEGORY": "Arrays & Hashing",
        "PROBLEM": "Concatenation of Array",
        "URL": (
            "https://neetcode.io/problems/"
            "concatenation-of-array/solution"
        ),
        "DIFFICULTY": "Easy",
    }
