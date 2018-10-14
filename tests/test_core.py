import tempfile

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
