"""Prompt 2 v2 canonical-derivation regression tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT = (
    ROOT
    / "prompts"
    / "interview_reference.md"
)

CONTRACT = (
    ROOT
    / "prompts"
    / "contracts"
    / "interview_reference_contract.md"
)


def read(path: Path) -> str:
    return path.read_text(
        encoding="utf-8"
    )


def test_prompt2_explicitly_consumes_validated_solution_reference():
    text = read(PROMPT)

    assert (
        "accepted and validated NC-250 SOLUTION_REFERENCE"
        in text
    )

    assert (
        "already passed Prompt 1 canonicalization "
        "and deterministic validation"
        in text
    )


def test_prompt2_is_not_a_raw_source_repair_stage():
    text = read(PROMPT)

    assert (
        "Prompt 2 is not a raw-source repair stage."
        in text
    )

    assert (
        "Do not repair raw-submission problems."
        in text
    )


def test_prompt2_preserves_canonical_metadata():
    text = read(PROMPT)

    for field in (
        "CATEGORY",
        "PREFERRED_SOLUTION",
        "PROBLEM",
        "URL",
        "DIFFICULTY",
    ):
        assert field in text

    assert (
        "The following values are canonical and immutable:"
        in text
    )

    assert "- change PREFERRED_SOLUTION" in text
    assert "do not recategorize the problem" in text
    assert "do not infer another value" in text


def test_prompt2_preserves_preferred_implementation():
    text = read(PROMPT)

    assert (
        "The accepted SOLUTION_REFERENCE owns "
        "the preferred executable implementation."
        in text
    )

    assert (
        "Prompt 2 does not own algorithm implementation."
        in text
    )

    assert (
        "Do not change the preferred algorithm."
        in text
    )


def test_prompt2_does_not_invent_baseline():
    text = read(PROMPT)

    assert (
        "Do not invent a brute-force solution merely "
        "to satisfy the interview flow."
        in text
    )

    assert (
        "Do not invent any unsupported baseline."
        in text
    )

    assert (
        "no separate baseline approach is documented"
        in text
    )


def test_prompt2_allows_custom_teaching_examples_but_not_fake_official_examples():
    text = read(PROMPT)

    assert "Custom teaching example" in text

    assert (
        "Never imply that a generated custom example is official."
        in text
    )

    assert (
        "Custom tests are teaching artifacts."
        in text
    )


def test_prompt2_complexity_must_agree_with_solution_reference():
    text = read(PROMPT)

    assert (
        "The final preferred TIME and SPACE conclusions "
        "must agree with the accepted SOLUTION_REFERENCE."
        in text
    )

    assert (
        "The conclusion must agree with the "
        "accepted SOLUTION_REFERENCE."
        in text
    )


def test_prompt2_preserves_existing_v7_section_names():
    text = read(PROMPT)

    required = (
        "ROLE, OBJECTIVE, AND LEARNING FLOW",
        "DERIVATION AUTHORITY AND CANONICAL SOURCE POLICY",
        "SOURCE PRIORITY",
        "GLOBAL WRITING AND TEACHING RULES",
        "CANONICAL METADATA AND PROBLEM DETAILS",
        "COMPLEXITY TEACHING FRAMEWORK",
        "REQUIRED INTERVIEW SECTION RULES",
        "CODE PRESERVATION RULES",
        "UNCERTAINTY POLICY",
        "CONTENT QUALITY AND CONSISTENCY",
        "FINAL TASK",
    )

    for heading in required:
        assert heading in text


def test_prompt2_contains_all_required_interview_sections():
    text = read(PROMPT)

    required = (
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

    for section in required:
        assert section in text


def test_prompt2_contract_still_requires_canonical_identity():
    text = read(CONTRACT)

    for field in (
        "CATEGORY",
        "PREFERRED_SOLUTION",
        "PROBLEM",
        "URL",
        "DIFFICULTY",
        "preferred executable implementation",
    ):
        assert field in text


def test_prompt2_does_not_allow_source_to_override_contracts():
    text = read(PROMPT)

    assert (
        "SOURCE_MATERIAL is not allowed to override "
        "the generation contract"
        in text
    )


def test_prompt2_canonical_contradiction_is_not_silently_repaired():
    text = read(PROMPT)

    assert (
        "A contradiction in canonical source material "
        "is not permission for Prompt 2 to redesign it."
        in text
    )

    assert (
        "SOURCE_REFERENCE_INCONSISTENT"
        in text
    )


def test_prompt2_semantic_quality_v7_1_rules():
    text = read(PROMPT)

    required = (
        "CANONICAL COMPLEXITY POLICY",
        "CANONICAL_TIME_HEADLINE_V7_1",
        "CANONICAL_SPACE_HEADLINE_V7_1",
        (
            "Never silently switch space-complexity "
            "conventions between Solution and Interview."
        ),
        (
            "Do not replace the canonical O(n) headline "
            "with O(1)"
        ),
    )

    for value in required:
        assert value in text


def test_prompt2_forbids_known_unsupported_claim_patterns():
    text = read(PROMPT)

    required = (
        '"typically n >= 1"',
        '"standard memory limits apply"',
        '"the expected solution is O(...)"',
        '"the interviewer expects ..."',
        '"this is more cache-friendly"',
        '"this will be faster in practice"',
    )

    for value in required:
        assert value in text


def test_prompt2_keeps_auxiliary_space_as_teaching_distinction():
    text = read(PROMPT)

    assert (
        "Auxiliary space excluding the returned output: O(1)."
        in text
    )

    assert (
        "The final headline SPACE complexity in this section "
        "must match the canonical preferred SPACE conclusion"
        in text
    )
