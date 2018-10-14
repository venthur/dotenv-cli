import logging
import os
from subprocess import Popen  # , PIPE, STDOUT


logger = logging.getLogger(__name__)


def read_dotenv(filename):
    """Read dotenv file.

    Parameters
    ----------
    filename : str
        path to the filename

    Returns
    -------
    dict

    Raises
    ------
    FileNotFoundError

    """
    with open(filename, 'r') as fh:
        data = fh.read()

    res = {}
    for line in data.splitlines():
        logger.debug(line)

        line = line.strip()

        # ignore comments
        if line.startswith('#'):
            continue

        # ignore empty lines or lines w/o '='
        if '=' not in line:
            continue

        key, value = line.split('=', 1)

        key = key.strip()
        value = value.strip()

        # remove quotes (not sure if this is standard behaviour)
        if value[0] == value[-1] in ['"', "'"]:
            value = value[1:-1]

        res[key] = value
    logger.debug(res)
    return res


def run_dotenv(filename, command):

    # read dotenv
    dotenv = read_dotenv(filename)

    # update env
    env = os.environ.copy()
    env.update(dotenv)

    # execute
    proc = Popen(
        command,
        # stdin=PIPE,
        # stdout=PIPE,
        # stderr=STDOUT,
        universal_newlines=True,
        bufsize=0,
        shell=False,
        env=env,
    )
    _, _ = proc.communicate()
    return proc.returncode
