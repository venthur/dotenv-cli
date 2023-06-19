# remove when we don't support py38 anymore
from __future__ import annotations
import logging
import os
from typing import NoReturn


logger = logging.getLogger(__name__)


def read_dotenv(filename: str) -> dict[str, str]:
    """Read dotenv file.

    Parameters
    ----------
    filename
        path to the filename

    Returns
    -------
    dict

    """
    try:
        with open(filename, 'r') as fh:
            data = fh.read()
    except FileNotFoundError:
        logger.warning(f"{filename} does not exist, continuing without "
                       "setting environment variables.")
        data = ""

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

        # allow export
        if key.startswith('export '):
            key = key.split(' ', 1)[-1]

        key = key.strip()
        value = value.strip()

        # remove quotes (not sure if this is standard behaviour)
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
            # escape escape characters
            value = bytes(value, 'utf-8').decode('unicode-escape')

        elif len(value) >= 2 and value[0] == value[-1] == "'":
            value = value[1:-1]

        res[key] = value
    logger.debug(res)
    return res


def run_dotenv(filename: str, command: list[str]) -> NoReturn:
    """Run dotenv.

    This function executes the commands with the environment variables
    parsed from filename.

    Parameters
    ----------
    filename
        path to the .env file
    command
        command to execute

    """
    # read dotenv
    dotenv = read_dotenv(filename)

    # update env
    env = os.environ.copy()
    env.update(dotenv)

    # execute
    # this function replaces this process with the command and does not return
    os.execvpe(command[0], command, env)
