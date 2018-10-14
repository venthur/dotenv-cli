from subprocess import run, PIPE
import tempfile


def test_stdout():
    proc = run(['dotenv', 'echo', 'test'], stdout=PIPE)
    assert b'test' in proc.stdout


def test_stderr():
    proc = run(['dotenv',
                'python', '-c', 'import os; os.write(2, b"test")'],
               stderr=PIPE)
    assert b'test' in proc.stderr


def test_returncode():
    proc = run(['dotenv', 'false'])
    assert proc.returncode == 1

    proc = run(['dotenv', 'true'])
    assert proc.returncode == 0


def test_alternative_dotenv():
    f = tempfile.NamedTemporaryFile('w')
    with open(f.name, 'w') as fh:
        fh.write('foo=bar')

    proc = run(['dotenv', '-e', f.name, 'env'], stdout=PIPE)
    assert b'foo=bar' in proc.stdout

    proc = run(['dotenv', '--dotenv', f.name, 'env'], stdout=PIPE)
    assert b'foo=bar' in proc.stdout
