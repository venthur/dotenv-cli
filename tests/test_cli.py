"""Test the CLI interface."""

import tempfile
from pathlib import Path
from subprocess import PIPE, run
from typing import Iterator

import pytest

from dotenv_cli import __VERSION__

DOTENV_FILE = """
# comment=foo
TEST=foo
TWOLINES='foo\nbar'
TEST_COMMENT=foo # bar
LINE_WITH_EQUAL='foo=bar'
"""


@pytest.fixture
def dotenvfile() -> Iterator[Path]:
    """Provide temporary dotenv file."""
    _file = Path.cwd() / ".env"
    with _file.open("w") as fh:
        fh.write(DOTENV_FILE)
    yield _file
    _file.unlink()


def test_this_dotenv() -> None:
    """Simple test for CI to assert we're running *our* dotenv."""
    proc = run(["dotenv", "--version"], stdout=PIPE)
    assert __VERSION__.encode() in proc.stdout


def test_stdout(dotenvfile: Path) -> None:
    """Test stdout."""
    proc = run(["dotenv", "echo", "test"], stdout=PIPE)
    assert b"test" in proc.stdout


def test_stderr(dotenvfile: Path) -> None:
    """Test stderr."""
    proc = run(["dotenv echo test 1>&2"], stderr=PIPE, shell=True)
    assert b"test" in proc.stderr


def test_returncode(dotenvfile: Path) -> None:
    """Test returncode."""
    proc = run(["dotenv", "false"])
    assert proc.returncode == 1

    proc = run(["dotenv", "true"])
    assert proc.returncode == 0


def test_alternative_dotenv() -> None:
    """Test alternative dotenv file."""
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("foo=bar")

    proc = run(["dotenv", "-e", f.name, "env"], stdout=PIPE)
    assert b"foo=bar" in proc.stdout

    proc = run(["dotenv", "--dotenv", f.name, "env"], stdout=PIPE)
    assert b"foo=bar" in proc.stdout


def test_nonexisting_dotenv() -> None:
    """Test non-existing dotenv file."""
    proc = run(["dotenv", "-e", "/tmp/i.dont.exist", "true"], stderr=PIPE)
    assert proc.returncode == 0
    assert b"does not exist" in proc.stderr


def test_no_command() -> None:
    """Test no command."""
    proc = run(["dotenv"])
    assert proc.returncode == 0


def test_replace_environment(dotenvfile: Path) -> None:
    """Test replace environment."""
    # we're putting the venv/bin explicitly in the command as dotenv -r removes
    # all environment variables, including the PATH
    proc = run(
        ["dotenv", "-r", "venv/bin/python", "-m", "tests.env"], stdout=PIPE
    )
    # the above .env file has exactly 4 lines
    assert len(proc.stdout.splitlines()) == 4

    proc = run(
        ["dotenv", "--replace", "venv/bin/python", "-m", "tests.env"],
        stdout=PIPE,
    )
    # the above .env file has exactly 4 lines
    assert len(proc.stdout.splitlines()) == 4
