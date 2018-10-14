from subprocess import run, PIPE


def test_stdout():
    proc = run(['dotenv', 'echo', 'test'], stdout=PIPE)
    assert b'test' in proc.stdout


def test_stderr():
    proc = run(['dotenv',
                'python', '-c', 'import os; os.write(2, b"test")'],
               stderr=PIPE)
    assert b'test' in proc.stderr
