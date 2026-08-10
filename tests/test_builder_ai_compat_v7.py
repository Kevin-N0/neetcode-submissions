"""Regression tests for builder ↔ v7 AI compatibility."""

from neetcode_references.ai import (
    generate_references,
    load_state,
    reference_metadata,
)


def test_legacy_reference_metadata_shape():
    source = """
class Solution:
    def solve(self):
        \"""
        @NC250_START
        TYPE: SOLUTION_REFERENCE
        SCHEMA_VERSION: 1

        CATEGORY: Arrays & Hashing
        PREFERRED_SOLUTION: S2

        @PROBLEM_DETAILS_START

        PROBLEM: Example Problem
        URL: https://neetcode.io/example
        DIFFICULTY: Easy
        PROBLEM DETAILS:

        Example.

        @PROBLEM_DETAILS_END
        @CONTENT_START
        @CONTENT_END
        @NC250_END
        \"""
        return None
"""

    metadata = reference_metadata(source)

    assert metadata == {
        "category": "Arrays & Hashing",
        "preferred_solution": "S2",
        "problem": "Example Problem",
        "difficulty": "Easy",
        "url": "https://neetcode.io/example",
    }


def test_ai_public_builder_api_exists():
    assert callable(generate_references)
    assert callable(load_state)
    assert callable(reference_metadata)


def test_real_builder_imports_successfully():
    from neetcode_references import builder

    assert callable(builder.main)


def test_build_references_entrypoint_imports_successfully():
    # The original v7 tests imported pieces of the AI layer but did not import
    # the actual builder integration path. This protects that boundary.
    import neetcode_references.builder as builder

    assert hasattr(builder, "main")
    assert callable(builder.main)
