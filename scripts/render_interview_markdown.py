from __future__ import annotations
import ast
import inspect
import re
from pathlib import Path
from .reference_scanner import ProblemRecord, read_text

SECTIONS = {
    "STEP_1_UNDERSTAND_THE_PROBLEM": "1. Understand the Problem",
    "STEP_2_RESTATE_THE_PROBLEM": "2. Restate the Problem",
    "STEP_3_CLARIFY_AND_CONFIRM": "3. Clarify and Confirm",
    "STEP_4_IDENTIFY_INPUTS_OUTPUTS_AND_CONSTRAINTS": "4. Inputs, Outputs, and Constraints",
    "STEP_5_BASELINE_APPROACH": "5. Baseline Approach",
    "STEP_6_BASELINE_COMPLEXITY": "6. Baseline Complexity",
    "STEP_7_FIND_THE_BOTTLENECK": "7. Find the Bottleneck",
    "STEP_8_OPTIMIZATION_BRIDGE": "8. Optimization Bridge",
    "STEP_9_PREFERRED_APPROACH": "9. Preferred Approach",
    "STEP_10_CORRECTNESS_REASONING": "10. Correctness Reasoning",
    "STEP_11_EXAMPLE_TRACE": "11. Example Trace",
    "STEP_12_CODE_PLAN": "12. Code Plan",
    "STEP_13_IMPLEMENTATION": "13. Implementation",
    "STEP_14_TEST_CASES": "14. Test Cases",
    "STEP_15_TIME_COMPLEXITY_DERIVATION": "15. Time Complexity Derivation",
    "STEP_16_SPACE_COMPLEXITY_DERIVATION": "16. Space Complexity Derivation",
    "STEP_17_APPROACH_TRADEOFFS": "17. Approach Tradeoffs",
    "STEP_18_INTERVIEW_COMMUNICATION": "18. Interview Communication",
    "INTERVIEW_SCRIPT": "Interview Script",
    "PATTERN_RECOGNITION": "Pattern Recognition",
    "COMMON_PITFALLS": "Common Pitfalls",
    "FINAL_REVIEW_CHECKLIST": "Final Review Checklist",
}

def reference_docstring(source: str) -> str:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and "TYPE: INTERVIEW_REFERENCE" in doc:
                return inspect.cleandoc(doc)
    raise ValueError("INTERVIEW_REFERENCE docstring not found")

class RemoveDocstrings(ast.NodeTransformer):
    def _clean(self, node):
        self.generic_visit(node)
        body = getattr(node, "body", None)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            node.body = body[1:]
        return node
    visit_Module = _clean
    visit_ClassDef = _clean
    visit_FunctionDef = _clean
    visit_AsyncFunctionDef = _clean

def executable_code(source: str) -> str:
    tree = RemoveDocstrings().visit(ast.parse(source))
    ast.fix_missing_locations(tree)
    return ast.unparse(tree).strip()

def markdown_body(doc: str) -> str:
    output: list[str] = []
    active = False
    content = False
    problem_details = False

    for raw in doc.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped == "@NC250_START":
            active = True
            continue
        if stripped == "@NC250_END":
            break
        if not active:
            continue
        if stripped == "@PROBLEM_DETAILS_START":
            problem_details = True
            output += ["## Problem Details", ""]
            continue
        if stripped == "@PROBLEM_DETAILS_END":
            problem_details = False
            continue
        if stripped == "@CONTENT_START":
            content = True
            continue
        if stripped == "@CONTENT_END":
            content = False
            continue
        if re.match(r"^(TYPE|SCHEMA_VERSION|CATEGORY|PREFERRED_SOLUTION|PROBLEM|DIFFICULTY)\s*:", stripped):
            continue
        if problem_details and stripped == "PROBLEM DETAILS:":
            continue
        marker = re.fullmatch(r"\[(.+)]", stripped)
        if marker and content:
            key = marker.group(1)
            output += [f"## {SECTIONS.get(key, key.replace('_', ' ').title())}", ""]
            continue
        output.append(line)

    compact: list[str] = []
    blanks = 0
    for line in output:
        if line.strip():
            blanks = 0
            compact.append(line)
        else:
            blanks += 1
            if blanks <= 2:
                compact.append("")
    return "\n".join(compact).strip()

def render(records: list[ProblemRecord], references_root: Path, repo_root: Path) -> list[Path]:
    written: list[Path] = []
    for record in records:
        candidate = record.interview_reference
        if candidate is None:
            continue

        source = read_text(candidate.path)
        destination = references_root / "interview" / record.category_slug / f"{record.problem_slug}.md"
        destination.parent.mkdir(parents=True, exist_ok=True)

        source_rel = Path(*([".."] * len(destination.parent.relative_to(repo_root).parts))) / candidate.path.relative_to(repo_root)
        solution = references_root / "solution" / record.category_slug / f"{record.problem_slug}.py"
        solution_line = f"- **Solution reference:** [Open](../../solution/{record.category_slug}/{record.problem_slug}.py)\n" if solution.exists() else ""

        page = (
            f"# {record.problem}\n\n"
            f"- **Category:** {record.category}\n"
            f"- **Difficulty:** {candidate.difficulty}\n"
            f"- **Preferred solution:** {candidate.preferred_solution}\n"
            f"- **Source submission:** [`{candidate.path.name}`]({source_rel.as_posix()})\n"
            f"{solution_line}"
            f"- **Study index:** [Back to index](../../README.md)\n\n"
            f"{markdown_body(reference_docstring(source))}\n\n"
            "## Executable Preferred Implementation\n\n"
            f"```python\n{executable_code(source)}\n```\n"
        )
        destination.write_text(page, encoding="utf-8")
        written.append(destination)
    return written
