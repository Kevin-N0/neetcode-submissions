CONTRACT: NC250_INTERVIEW_REFERENCE
VERSION: 1

This contract defines the required machine-readable shape of one NC-250 INTERVIEW_REFERENCE.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. REQUIRED STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Python documentation string must contain exactly one complete reference using this marker order:

@NC250_START

TYPE: INTERVIEW_REFERENCE
SCHEMA_VERSION: 1
CATEGORY:
PREFERRED_SOLUTION:

@PROBLEM_DETAILS_START

PROBLEM:
URL:
DIFFICULTY:
PROBLEM DETAILS:

@PROBLEM_DETAILS_END

@CONTENT_START

[STEP_1_UNDERSTAND_THE_PROBLEM]

[STEP_2_RESTATE_THE_PROBLEM]

[STEP_3_CLARIFY_AND_CONFIRM]

[STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]

[STEP_5_BASELINE_APPROACH]

[STEP_6_BASELINE_COMPLEXITY]

[STEP_7_FIND_THE_BOTTLENECK]

[STEP_8_OPTIMIZATION_BRIDGE]

[STEP_9_PREFERRED_APPROACH]

[STEP_10_CORRECTNESS_REASONING]

[STEP_11_EXAMPLE_TRACE]

[STEP_12_CODE_PLAN]

[STEP_13_IMPLEMENTATION]

[STEP_14_TEST_CASES]

[STEP_15_TIME_COMPLEXITY_DERIVATION]

[STEP_16_SPACE_COMPLEXITY_DERIVATION]

[STEP_17_APPROACH_TRADEOFFS]

[STEP_18_INTERVIEW_COMMUNICATION]

[INTERVIEW_SCRIPT]

[PATTERN_RECOGNITION]

[COMMON_PITFALLS]

[FINAL_REVIEW_CHECKLIST]

@CONTENT_END

@NC250_END

Do not:

- rename sections
- remove sections
- duplicate sections
- reorder sections
- merge sections
- split sections
- invent structural sections
- escape structural markers

Every required section must contain meaningful completed content.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. METADATA ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Preserve this metadata order exactly:

TYPE
SCHEMA_VERSION
CATEGORY
PREFERRED_SOLUTION

PROBLEM
URL
DIFFICULTY

Required values:

TYPE: INTERVIEW_REFERENCE
SCHEMA_VERSION: 1

URL is required.

If the canonical SOLUTION_REFERENCE contains:

URL: Unknown

preserve:

URL: Unknown

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. CANONICAL SOURCE INVARIANTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The INTERVIEW_REFERENCE is derived from one accepted SOLUTION_REFERENCE.

The following values must match that accepted source exactly:

- CATEGORY
- PREFERRED_SOLUTION
- PROBLEM
- URL
- DIFFICULTY
- required class name
- required method signature
- preferred executable implementation

Prompt 2 may not change these canonical values.

A mismatch is an artifact-validation failure.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. REQUIRED INTERVIEW SECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Each of the following markers must appear exactly once:

[STEP_1_UNDERSTAND_THE_PROBLEM]
[STEP_2_RESTATE_THE_PROBLEM]
[STEP_3_CLARIFY_AND_CONFIRM]
[STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS]
[STEP_5_BASELINE_APPROACH]
[STEP_6_BASELINE_COMPLEXITY]
[STEP_7_FIND_THE_BOTTLENECK]
[STEP_8_OPTIMIZATION_BRIDGE]
[STEP_9_PREFERRED_APPROACH]
[STEP_10_CORRECTNESS_REASONING]
[STEP_11_EXAMPLE_TRACE]
[STEP_12_CODE_PLAN]
[STEP_13_IMPLEMENTATION]
[STEP_14_TEST_CASES]
[STEP_15_TIME_COMPLEXITY_DERIVATION]
[STEP_16_SPACE_COMPLEXITY_DERIVATION]
[STEP_17_APPROACH_TRADEOFFS]
[STEP_18_INTERVIEW_COMMUNICATION]
[INTERVIEW_SCRIPT]
[PATTERN_RECOGNITION]
[COMMON_PITFALLS]
[FINAL_REVIEW_CHECKLIST]

No required section may be empty.

Do not leave:

- unresolved placeholders
- generic template instructions
- TODO
- O(...)
- empty bullets
- empty numbered entries

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. BASELINE POLICY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The baseline must be supported by the accepted SOLUTION_REFERENCE.

Use the earliest meaningful documented approach.

Prefer a documented brute-force approach when present.

Do not invent a baseline merely because the INTERVIEW_REFERENCE schema contains baseline sections.

If no separate baseline approach is documented:

- use the simplest supported documented approach as the starting point
- state that no separate baseline is documented
- do not fabricate a worse algorithm

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. EXAMPLES AND TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Official examples must remain faithful to the accepted SOLUTION_REFERENCE.

Generated custom traces or tests are allowed for teaching when valid.

Any generated custom example must not be labeled official.

Generated tests must:

- satisfy known constraints
- contain an expected output
- agree with the canonical implementation
- not contradict canonical mutation behavior

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. COMPLEXITY CONSISTENCY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Preferred time and space complexity derivations must analyze the canonical executable implementation.

Their final conclusions must agree with the accepted SOLUTION_REFERENCE.

Do not silently substitute a different complexity conclusion.

Material disagreement indicates source-reference inconsistency or invalid generated content.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. EXECUTABLE CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Exactly one preferred implementation must be active and executable.

It must be the same canonical preferred implementation supplied by the accepted SOLUTION_REFERENCE.

Do not include full alternative implementations.

Do not include multiple active versions of the required method.

Do not include:

- pass used as a placeholder
- raise NotImplementedError
- TODO
- debug prints
- test runners
- example invocations
- unsupported external packages
- pseudocode
- placeholder ellipses
- incomplete branches

Required imports and supporting definitions must be preserved.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. CONSISTENCY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The following must all describe the same canonical preferred implementation:

- preferred approach
- correctness reasoning
- example trace
- code plan
- implementation explanation
- test cases
- time complexity derivation
- space complexity derivation
- mutation statement
- interview script

Canonical metadata and executable code must remain stable across equivalent regeneration.


CANONICAL_COMPLEXITY_CONSISTENCY_V7_1

The accepted SOLUTION_REFERENCE is authoritative for the preferred solution's
final TIME and SPACE headline conclusions.

INTERVIEW_REFERENCE must preserve those conclusions.

The Interview artifact may teach additional distinctions such as:

- auxiliary space excluding required output
- total space including required output
- recursion-stack contribution
- temporary workspace

but those distinctions must not replace or contradict the canonical headline.

Example:

If SOLUTION_REFERENCE says:

    SPACE: O(n)

then INTERVIEW_REFERENCE may teach:

    Canonical space: O(n) including required output.
    Auxiliary space excluding output: O(1).

It must not present O(1) as the final canonical SPACE conclusion.

Likewise, the Interview artifact must not silently alter the canonical TIME
conclusion or complexity convention.

Unsupported speculative claims are invalid quality behavior.

Do not present unsupported statements as facts, including claims about:

- unstated official constraints
- typical input bounds
- standard memory limits
- interviewer expectations
- expected target complexity
- cache friendliness
- practical speed
- platform behavior not supported by the canonical source or established
  language/runtime operation costs

When unsupported, omit the claim or phrase it explicitly as an uncertainty or
clarification question.
