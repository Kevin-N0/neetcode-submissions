from pathlib import Path

from neetcode_references.prompting import (
    build_interview_prompt,
    build_repair_prompt,
    build_solution_prompt,
    load_prompt_bundle,
)
from neetcode_references.validation import (
    ValidationIssue,
)


ROOT = Path(__file__).resolve().parents[1]


def test_v7_prompt_bundle_loads():
    bundle = load_prompt_bundle(ROOT)

    assert bundle.generation_contract_version == 1
    assert bundle.solution_contract_version == 1
    assert bundle.interview_contract_version == 1
    assert bundle.repair_contract_version == 1


def test_solution_prompt_composes_all_layers():
    bundle = load_prompt_bundle(ROOT)

    text = build_solution_prompt(
        bundle,
        authoritative_metadata={
            "PROBLEM": "Example",
            "URL": "https://example.test/problem",
        },
        source_material="class Solution:\n    pass",
    )

    assert "CONTRACT: NC250_GENERATION" in text
    assert "CONTRACT: NC250_SOLUTION_REFERENCE" in text
    assert "TRANSFORMATION INSTRUCTIONS" in text
    assert "AUTHORITATIVE_METADATA" in text
    assert "<SOURCE_MATERIAL>" in text
    assert "https://example.test/problem" in text


def test_interview_prompt_composes_all_layers():
    bundle = load_prompt_bundle(ROOT)

    text = build_interview_prompt(
        bundle,
        canonical_metadata={
            "PROBLEM": "Example",
            "PREFERRED_SOLUTION": "S1",
        },
        solution_reference="example solution",
    )

    assert "CONTRACT: NC250_GENERATION" in text
    assert "CONTRACT: NC250_INTERVIEW_REFERENCE" in text
    assert "CANONICAL_METADATA" in text
    assert "<SOURCE_MATERIAL>" in text


def test_repair_prompt_contains_only_repair_inputs():
    bundle = load_prompt_bundle(ROOT)

    issue = ValidationIssue(
        code="URL_MISMATCH",
        message="URL changed",
        expected="https://expected.test",
        actual="https://wrong.test",
    )

    text = build_repair_prompt(
        bundle,
        artifact_type="SOLUTION_REFERENCE",
        authoritative_metadata={
            "URL": "https://expected.test",
        },
        errors=[issue],
        failed_artifact="bad output",
    )

    assert "CONTRACT: NC250_REPAIR" in text
    assert "VALIDATION_ERRORS" in text
    assert "URL_MISMATCH" in text
    assert "https://expected.test" in text
    assert "<FAILED_ARTIFACT>" in text
