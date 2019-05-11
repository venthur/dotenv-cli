import tempfile

import pytest

from dotenv_cli import core


def test_full():
    f = tempfile.NamedTemporaryFile('w')
    TEST = r"""
BASIC=basic basic
export EXPORT=foo
EMPTY=
INNER_QUOTES=this 'is' a test
INNER_QUOTES2=this "is" a test
TRIM_WHITESPACE= foo
KEEP_WHITESPACE="  foo  "
MULTILINE="multi\nline"
# some comment
should be ignored
"""

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['BASIC'] == 'basic basic'
    assert env['EXPORT'] == 'foo'
    assert env['EMPTY'] == ''
    assert env['INNER_QUOTES'] == "this 'is' a test"
    assert env['INNER_QUOTES2'] == 'this "is" a test'
    assert env['TRIM_WHITESPACE'] == "foo"
    assert env['KEEP_WHITESPACE'] == "  foo  "
    assert env['MULTILINE'] == "multi\nline"

    assert len(env) == 8


def test_basic():
    """Basic unquoted strings"""
    f = tempfile.NamedTemporaryFile('w')
    TEST = "FOO=BAR"

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == 'BAR'


def test_empty():
    """Empty values become empty strings."""
    f = tempfile.NamedTemporaryFile('w')
    TEST = "FOO="

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == ''


def test_inner_quotes():
    """Inner quotes are mainained."""
    f = tempfile.NamedTemporaryFile('w')
    TEST = "FOO=this 'is' a test"

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == "this 'is' a test"

    TEST = 'FOO=this "is" a test'

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == 'this "is" a test'


def test_trim_whitespaces():
    """Whitespaces are stripped from unquoted values."""
    f = tempfile.NamedTemporaryFile('w')
    TEST = "FOO=  test  "

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == "test"


def test_keep_whitespaces():
    """Whitespaces are mainteined from quoted values."""
    f = tempfile.NamedTemporaryFile('w')
    TEST = "FOO='  test  '"

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == "  test  "


def test_multiline():
    """Quoted values can contain newlines."""
    f = tempfile.NamedTemporaryFile('w')
    TEST = r"FOO='This is\nbar'"

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == 'This is\nbar'


@pytest.mark.parametrize('input_, expected', [
    ('FOO="Test"', 'Test'),
    ("FOO='Test'", 'Test'),
    ("FOO='\"Test\"'", '"Test"'),
    ('FOO="\'Test\'"', "'Test'"),
])
def test_quotes(input_, expected):
    f = tempfile.NamedTemporaryFile('w')

    with open(f.name, 'w') as fh:
        fh.write(input_)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == expected


def test_comments():
    """Lines starting with # are ignored."""
    f = tempfile.NamedTemporaryFile('w')

    TEST = """
    FOO=BAR
    # comment
    BAR=BAZ
    """

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert len(env) == 2
    assert env['FOO'] == 'BAR'
    assert env['BAR'] == 'BAZ'


def test_emtpy_lines():
    """Empty lines are skipped."""
    f = tempfile.NamedTemporaryFile('w')

    TEST = """
    FOO=BAR

    BAR=BAZ
    """

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert len(env) == 2
    assert env['FOO'] == 'BAR'
    assert env['BAR'] == 'BAZ'


def test_export():
    """Exports are allowed."""
    f = tempfile.NamedTemporaryFile('w')

    TEST = "export FOO=BAR"

    with open(f.name, 'w') as fh:
        fh.write(TEST)

    env = core.read_dotenv(f.name)
    assert env['FOO'] == 'BAR'
