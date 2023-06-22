import tempfile
from pathlib import Path
from subprocess import PIPE, run
from typing import Iterator

import pytest

DOTENV_FILE = """
# comment=foo
TEST=foo
TWOLINES='foo\nbar'
TEST_COMMENT=foo # bar
LINE_WITH_EQUAL='foo=bar'
"""


@pytest.fixture
def dotenvfile() -> Iterator[Path]:
    _file = Path.cwd() / ".env"
    with _file.open("w") as fh:
        fh.write(DOTENV_FILE)
    yield _file
    _file.unlink()


def test_stdout(dotenvfile: Path) -> None:
    proc = run(["dotenv", "echo", "test"], stdout=PIPE)
    assert b"test" in proc.stdout


def test_stderr(dotenvfile: Path) -> None:
    proc = run(["dotenv echo test 1>&2"], stderr=PIPE, shell=True)
    assert b"test" in proc.stderr


def test_returncode(dotenvfile: Path) -> None:
    proc = run(["dotenv", "false"])
    assert proc.returncode == 1

    proc = run(["dotenv", "true"])
    assert proc.returncode == 0


def test_alternative_dotenv() -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("foo=bar")

    proc = run(["dotenv", "-e", f.name, "env"], stdout=PIPE)
    assert b"foo=bar" in proc.stdout

    proc = run(["dotenv", "--dotenv", f.name, "env"], stdout=PIPE)
    assert b"foo=bar" in proc.stdout


def test_nonexisting_dotenv() -> None:
    proc = run(["dotenv", "-e", "/tmp/i.dont.exist", "true"], stderr=PIPE)
    assert proc.returncode == 0
    assert b"does not exist" in proc.stderr


def test_no_command() -> None:
    proc = run(["dotenv"])
    assert proc.returncode == 0
