from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT = ROOT / "prompts" / "interview_reference.md"
CONTRACT = (
    ROOT
    / "prompts"
    / "contracts"
    / "interview_reference_contract.md"
)

GENERATION = (
    ROOT
    / "prompts"
    / "contracts"
    / "generation_contract.md"
)

SOLUTION_CONTRACT = (
    ROOT
    / "prompts"
    / "contracts"
    / "solution_reference_contract.md"
)

REPAIR = (
    ROOT
    / "prompts"
    / "contracts"
    / "repair_contract.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_prompt2_files_exist():
    for path in (
        PROMPT,
        CONTRACT,
        GENERATION,
        SOLUTION_CONTRACT,
        REPAIR,
    ):
        assert path.exists(), path


def test_prompt2_uses_explicit_source_material_language():
    text = read(PROMPT)

    assert "SOURCE_MATERIAL" in text
    assert "CANONICAL_METADATA" in text

    lowered = text.lower()

    assert "immediately above this prompt" not in lowered
    assert "preceding submission" not in lowered


def test_prompt2_preserves_canonical_preferred_solution():
    text = read(PROMPT)

    assert "Do not change PREFERRED_SOLUTION." in text
    assert "Do not invent a new preferred approach." in text


def test_prompt2_preserves_canonical_code():
    text = read(PROMPT)

    assert "Prompt 2 does not own algorithm redesign." in text
    assert (
        "Do not change the preferred executable implementation merely for style."
        in text
    )


def test_interview_contract_contains_shared_identity_schema():
    text = read(CONTRACT)

    required = (
        "TYPE: INTERVIEW_REFERENCE",
        "SCHEMA_VERSION: 1",
        "CATEGORY:",
        "PREFERRED_SOLUTION:",
        "PROBLEM:",
        "URL:",
        "DIFFICULTY:",
        "@PROBLEM_DETAILS_START",
        "@PROBLEM_DETAILS_END",
        "@CONTENT_START",
        "@CONTENT_END",
        "@NC250_END",
    )

    for value in required:
        assert value in text


def test_interview_contract_contains_all_required_sections():
    text = read(CONTRACT)

    sections = (
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

    for value in sections:
        assert value in text


def test_interview_contract_preserves_solution_identity():
    text = read(CONTRACT)

    required = (
        "CATEGORY",
        "PREFERRED_SOLUTION",
        "PROBLEM",
        "URL",
        "DIFFICULTY",
        "required class name",
        "required method signature",
        "preferred executable implementation",
    )

    for value in required:
        assert value in text

    assert "Prompt 2 may not change these canonical values." in text


def test_baseline_policy_forbids_invented_baseline():
    prompt = read(PROMPT)
    contract = read(CONTRACT)

    assert "Do not invent a baseline merely to satisfy the interview flow." in prompt
    assert "Do not invent a baseline merely because" in contract
    assert "do not fabricate a worse algorithm" in contract


def test_custom_examples_must_not_be_mislabeled_official():
    prompt = read(PROMPT)
    contract = read(CONTRACT)

    assert "Custom teaching example" in prompt
    assert "Never label a generated custom example as official." in prompt
    assert "must not be labeled official" in contract


def test_prompt2_retains_learning_flow():
    text = read(PROMPT)

    required = (
        "ROLE, OBJECTIVE, AND LEARNING FLOW",
        "DERIVATION AUTHORITY AND CANONICAL SOURCE POLICY",
        "GLOBAL WRITING AND TEACHING RULES",
        "COMPLEXITY TEACHING FRAMEWORK",
        "[STEP_1_UNDERSTAND_THE_PROBLEM]",
        "[STEP_18_INTERVIEW_COMMUNICATION]",
        "[INTERVIEW_SCRIPT]",
        "[PATTERN_RECOGNITION]",
        "[COMMON_PITFALLS]",
        "[FINAL_REVIEW_CHECKLIST]",
        "CODE PRESERVATION RULES",
        "UNCERTAINTY POLICY",
        "CONTENT QUALITY AND CONSISTENCY",
        "FINAL TASK",
    )

    for value in required:
        assert value in text


def test_both_artifact_contracts_use_url():
    solution = read(SOLUTION_CONTRACT)
    interview = read(CONTRACT)

    assert "URL:" in solution
    assert "URL:" in interview


def test_shared_generation_and_repair_contracts_remain_present():
    generation = read(GENERATION)
    repair = read(REPAIR)

    assert "CONTRACT: NC250_GENERATION" in generation
    assert "CONTRACT: NC250_REPAIR" in repair
