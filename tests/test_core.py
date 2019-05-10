import tempfile

import pytest

from dotenv_cli import core

TEST_NORMAL = """
foo=bar
# some=comment
should be ignored
"""


def test_read_dotenv():
    f = tempfile.NamedTemporaryFile('w')

    with open(f.name, 'w') as fh:
        fh.write(TEST_NORMAL)

    env = core.read_dotenv(f.name)
    assert env['foo'] == 'bar'
    assert len(env) == 1


def test_multiline():
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
