from __future__ import annotations

from pathlib import Path

import pytest

from neetcode_references.ai import (
    latest_raw_submission,
    strip_code_fence,
    validate_reference,
)


VALID_SOLUTION = '''from typing import List


class Solution:
    def example(self, nums: List[int]) -> bool:
        """
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S1

        @PROBLEM_DETAILS_START

        PROBLEM: Example Problem
        URL: https://example.test/problem
        DIFFICULTY: Easy

        @PROBLEM_DETAILS_END
        @CONTENT_START

        Content.

        @CONTENT_END
        @NC250_END
        """
        return True
'''


def test_strip_python_code_fence():
    wrapped = '''```python
print("hello")
```'''

    assert strip_code_fence(wrapped) == 'print("hello")'


def test_strip_plain_code_fence():
    wrapped = '''```
print("hello")
```'''

    assert strip_code_fence(wrapped) == 'print("hello")'


def test_validate_reference_accepts_valid_python():
    metadata = validate_reference(
        VALID_SOLUTION,
        "SOLUTION_REFERENCE",
    )

    assert metadata["problem"] == "Example Problem"
    assert metadata["category"] == "Arrays & Hashing"


def test_validate_reference_rejects_wrong_type():
    with pytest.raises(ValueError):
        validate_reference(
            VALID_SOLUTION,
            "INTERVIEW_REFERENCE",
        )


def test_validate_reference_rejects_invalid_python():
    broken = VALID_SOLUTION.replace(
        "        return True",
        "        return True !!!",
    )

    with pytest.raises(ValueError):
        validate_reference(
            broken,
            "SOLUTION_REFERENCE",
        )


def test_latest_raw_submission_ignores_old_typed_refs(
    tmp_path: Path,
):
    (tmp_path / "submission-1.py").write_text(
        "print('raw')\n",
        encoding="utf-8",
    )

    (tmp_path / "submission-2.py").write_text(
        VALID_SOLUTION,
        encoding="utf-8",
    )

    (tmp_path / "submission-3.py").write_text(
        "print('new raw')\n",
        encoding="utf-8",
    )

    latest = latest_raw_submission(tmp_path)

    assert latest is not None
    assert latest.number == 3