CONTRACT: NC250_REPAIR
VERSION: 1

This contract is used only when a previously generated NC-250 artifact failed deterministic validation.

The goal is repair, not regeneration or redesign.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. REPAIR OBJECTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repair the supplied FAILED_ARTIFACT so that it satisfies:

1. the NC-250 generation contract
2. the applicable artifact-specific contract
3. AUTHORITATIVE_METADATA
4. the supplied VALIDATION_ERRORS

Return the entire repaired artifact.

Make the smallest changes necessary.

Preserve all correct content.

Do not rewrite correct sections merely for stylistic improvement.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. VALIDATION ERRORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VALIDATION_ERRORS identify concrete defects in the failed artifact.

Correct every listed error.

Examples may include:

- PYTHON_SYNTAX_ERROR
- MARKER_ESCAPED
- TYPE_MISMATCH
- URL_MISMATCH
- SECTION_MISSING
- UNRESOLVED_PLACEHOLDER
- MULTIPLE_ACTIVE_IMPLEMENTATIONS

Do not ignore listed errors.

Do not invent unrelated changes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. AUTHORITATIVE METADATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTHORITATIVE_METADATA is immutable.

When an error reports a mismatch, copy the supplied expected authoritative value exactly.

For example, when validation reports:

URL_MISMATCH

use the authoritative URL supplied by the pipeline.

Do not search memory for another URL.

Do not substitute another website.

Do not reinterpret the authoritative value.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. SOURCE AND CONTENT PRESERVATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Preserve correct:

- problem details
- approaches
- explanations
- complexity derivations
- implementation logic
- variable names
- approach order
- preferred solution

Do not add a new approach unless the applicable transformation policy explicitly permits it.

Do not change PREFERRED_SOLUTION merely because repair is being performed.

Do not change correct algorithm logic to make formatting easier.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The NC-250 generation contract still applies during repair.

Return raw Python source only.

Do not use Markdown code fences.

Do not include explanations before or after the repaired artifact.

Do not escape NC-250 markers.

Preserve Python indentation.

Return the complete repaired file, not a patch or diff.
