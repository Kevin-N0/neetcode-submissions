CONTRACT: NC250_SOLUTION_REFERENCE
VERSION: 1

This contract defines the required machine-readable shape of one NC-250 SOLUTION_REFERENCE.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. REQUIRED STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Python documentation string must contain exactly one complete reference using this marker order:

@NC250_START

TYPE: SOLUTION_REFERENCE
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

[S#]-[APPROACH NAME]

INT:
ALGO:
TIME:
SPACE:

[APPROACH_COMPARISON]

[COMMON_PITFALLS]

@CONTENT_END

@NC250_END

Do not:

- rename structural markers
- remove structural markers
- duplicate structural markers
- reorder structural markers
- escape structural markers
- invent new structural markers

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

TYPE: SOLUTION_REFERENCE
SCHEMA_VERSION: 1

URL is required.

If no authoritative or reliable URL is available, use:

URL: Unknown

Do not omit the URL field.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. SOLUTION SECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Each surviving solution must use a contiguous label:

S1
S2
S3
S4

Do not leave gaps.

Every surviving solution must include:

[S#]-[APPROACH NAME]

INT:
ALGO:
TIME:
SPACE:

INT, ALGO, TIME, and SPACE must contain completed meaningful content.

Do not leave:

- O(...)
- placeholder instructions
- empty sections
- TODO
- unresolved template values

PREFERRED_SOLUTION must exactly equal one surviving solution label.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. APPROACH COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[APPROACH_COMPARISON] must exist exactly once.

It must contain exactly one entry for every surviving solution and no entry for a removed solution.

Each entry must include:

- Approach
- Time
- Time qualification
- Space
- Input modified
- Main advantage
- Main disadvantage

Input modified must be exactly:

Yes

or:

No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. COMMON PITFALLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[COMMON_PITFALLS] must exist exactly once.

It must contain meaningful problem-specific content.

Do not include unresolved placeholder pitfalls.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. EXECUTABLE CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Python file must preserve the required class name and official method signature.

Every surviving documented approach must have a complete corresponding implementation.

Exactly one approach may be active and executable.

The active implementation must correspond to PREFERRED_SOLUTION.

Every non-preferred implementation must be fully inactive/commented.

Do not include:

- multiple active implementations
- pass used as a placeholder
- raise NotImplementedError
- TODO
- placeholder ellipses
- pseudocode instead of implementation
- debug prints
- example invocations
- test runners
- unsupported external packages
- incomplete branches

Required supporting definitions and platform-appropriate imports must be preserved.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. CONSISTENCY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For every surviving approach:

- INT must describe the same approach as the code.
- ALGO must describe the code in execution order.
- TIME must match the implementation.
- SPACE must match the implementation.
- comparison values must match the detailed section.
- mutation claims must match actual behavior.

The active preferred implementation must correctly solve the stated problem.
