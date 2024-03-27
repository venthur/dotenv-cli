"""Test core module."""


import tempfile

import pytest

from dotenv_cli import core


def test_full() -> None:
    """Test full dotenv file."""
    TEST = r"""
BASIC=basic basic
export EXPORT=foo
EMPTY=
INNER_QUOTES=this 'is' a test
INNER_QUOTES2=this "is" a test
TRIM_WHITESPACE= foo
KEEP_WHITESPACE="  foo  "
MULTILINE_DQ="multi\nline"
MULTILINE_SQ='multi\nline'
MULTILINE_NQ=multi\nline
# some comment
should be ignored
"""

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["BASIC"] == "basic basic"
    assert env["EXPORT"] == "foo"
    assert env["EMPTY"] == ""
    assert env["INNER_QUOTES"] == "this 'is' a test"
    assert env["INNER_QUOTES2"] == 'this "is" a test'
    assert env["TRIM_WHITESPACE"] == "foo"
    assert env["KEEP_WHITESPACE"] == "  foo  "
    assert env["MULTILINE_DQ"] == "multi\nline"
    assert env["MULTILINE_SQ"] == "multi\\nline"
    assert env["MULTILINE_NQ"] == "multi\\nline"

    assert len(env) == 10


def test_basic() -> None:
    """Basic unquoted strings."""
    TEST = "FOO=BAR"

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == "BAR"


def test_empty() -> None:
    """Empty values become empty strings."""
    TEST = "FOO="

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == ""


def test_inner_quotes() -> None:
    """Inner quotes are mainained."""
    TEST = "\n".join(["FOO1=this 'is' a test", 'FOO2=this "is" a test'])

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO1"] == "this 'is' a test"
    assert env["FOO2"] == 'this "is" a test'


def test_trim_whitespaces() -> None:
    """Whitespaces are stripped from unquoted values."""
    TEST = "FOO=  test  "

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == "test"


def test_keep_whitespaces() -> None:
    """Whitespaces are mainteined from quoted values."""
    TEST = "FOO='  test  '"

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == "  test  "


def test_multiline() -> None:
    """Quoted values can contain newlines."""
    TEST = r'FOO="This is\nbar"'

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == "This is\nbar"


@pytest.mark.parametrize(
    "input_, expected",
    [
        ('FOO="Test"', "Test"),
        ("FOO='Test'", "Test"),
        ("FOO='\"Test\"'", '"Test"'),
        ("FOO=\"'Test'\"", "'Test'"),
    ],
)
def test_quotes(input_: str, expected: str) -> None:
    """Test different quotes."""
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(input_)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == expected


def test_comments() -> None:
    """Test comments."""
    """Lines starting with # are ignored."""
    TEST = """
    FOO=BAR
    # comment
    BAR=BAZ
    """

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert len(env) == 2
    assert env["FOO"] == "BAR"
    assert env["BAR"] == "BAZ"


def test_emtpy_lines() -> None:
    """Empty lines are skipped."""
    TEST = """
    FOO=BAR

    BAR=BAZ
    """

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert len(env) == 2
    assert env["FOO"] == "BAR"
    assert env["BAR"] == "BAZ"


def test_export() -> None:
    """Exports are allowed."""
    TEST = "export FOO=BAR"

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(TEST)

    env = core.read_dotenv(f.name)
    assert env["FOO"] == "BAR"


def test_non_existing_dotenv() -> None:
    """Non-existing dotenv file."""
    env = core.read_dotenv("/tmp/i.dont.exist")
    assert len(env) == 0
