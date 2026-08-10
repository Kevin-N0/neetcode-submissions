from pathlib import Path

from neetcode_references.ai import (
    authoritative_metadata_for_source,
    extract_source_metadata,
    latest_raw_submission,
    raw_submission,
)


def test_source_metadata_extracts_markdown_url_target():
    text = """
    PROBLEM: Concatenation of Array
    URL: [https://neetcode.io/test](https://neetcode.io/test)
    DIFFICULTY: [Easy]
    CATEGORY: Arrays & Hashing
    """

    metadata = extract_source_metadata(text)

    assert metadata["PROBLEM"] == "Concatenation of Array"
    assert metadata["URL"] == "https://neetcode.io/test"
    assert metadata["DIFFICULTY"] == "Easy"
    assert metadata["CATEGORY"] == "Arrays & Hashing"


def test_typed_submission_is_not_raw(tmp_path: Path):
    path = tmp_path / "submission-3.py"

    path.write_text(
        'class Solution:\n'
        '    """\n'
        '    TYPE: SOLUTION_REFERENCE\n'
        '    """\n',
        encoding="utf-8",
    )

    assert raw_submission(path) is None


def test_latest_raw_submission_skips_typed_reference(tmp_path: Path):
    raw = tmp_path / "submission-4.py"
    typed = tmp_path / "submission-5.py"

    raw.write_text(
        "class Solution:\n    pass\n",
        encoding="utf-8",
    )

    typed.write_text(
        'class Solution:\n'
        '    """\n'
        '    TYPE: INTERVIEW_REFERENCE\n'
        '    """\n',
        encoding="utf-8",
    )

    found = latest_raw_submission(tmp_path)

    assert found is not None
    assert found.number == 4


def test_authoritative_metadata_contains_source_identity(tmp_path: Path):
    root = tmp_path
    directory = (
        root
        / "Data Structures & Algorithms"
        / "example"
    )

    directory.mkdir(parents=True)

    path = directory / "submission-1.py"

    text = """
PROBLEM: Example
URL: https://neetcode.io/example
DIFFICULTY: Easy
CATEGORY: Arrays & Hashing
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

    assert metadata["PROBLEM"] == "Example"
    assert metadata["URL"] == "https://neetcode.io/example"
    assert metadata["SOURCE_SUBMISSION"] == "submission-1.py"


def test_persisted_content_hash_matches_atomic_write_output_v7_2(
    tmp_path,
):
    """
    State hashes must describe the representation actually persisted by
    atomic_write(), not the pre-write model response.
    """

    from neetcode_references.state import (
        atomic_write,
        read_text,
        stable_hash,
    )

    path = tmp_path / "reference.py"

    model_response = (
        "print('hello')\n\n\n"
    )

    pre_write_hash = stable_hash(
        model_response
    )

    atomic_write(
        path,
        model_response,
    )

    persisted = read_text(
        path
    )

    persisted_hash = stable_hash(
        persisted
    )

    assert persisted == "print('hello')\n"

    assert (
        persisted_hash
        != pre_write_hash
    )

    # This is the representation ai.py must store after acceptance.
    assert persisted_hash == stable_hash(
        read_text(path)
    )
