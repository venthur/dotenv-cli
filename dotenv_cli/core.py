"""Core functions."""


# remove when we don't support py38 anymore
from __future__ import annotations

import atexit
import logging
import os
from subprocess import Popen
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
        with open(filename) as fh:
            data = fh.read()
    except FileNotFoundError:
        logger.warning(
            f"{filename} does not exist, continuing without "
            "setting environment variables."
        )
        data = ""

    res = {}
    for line in data.splitlines():
        logger.debug(line)

        line = line.strip()

        # ignore comments
        if line.startswith("#"):
            continue

        # ignore empty lines or lines w/o '='
        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        # allow export
        if key.startswith("export "):
            key = key.split(" ", 1)[-1]

        key = key.strip()
        value = value.strip()

        # remove quotes (not sure if this is standard behaviour)
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
            # escape escape characters
            value = bytes(value, "utf-8").decode("unicode-escape")

        elif len(value) >= 2 and value[0] == value[-1] == "'":
            value = value[1:-1]

        res[key] = value
    logger.debug(res)
    return res


def run_dotenv(
    filename: str, command: list[str], replace: bool = False
) -> NoReturn | int:
    """Run dotenv.

    This function executes the commands with the environment variables
    parsed from filename.

    Parameters
    ----------
    filename
        path to the .env file
    command
        command to execute
    replace_env
        Replace the current environment instead of updating it.

    Returns
    -------
    NoReturn | int
        The exit status code in Windows. In POSIX-compatible systems, the
        function does not return normally.

    """
    # read dotenv
    dotenv = read_dotenv(filename)

    if replace:
        # replace env
        env = dotenv
    else:
        # update env
        env = os.environ.copy()
        env.update(dotenv)

    # in POSIX, we replace the current process with the command, execvpe does
    # not return
    if os.name == "posix":
        os.execvpe(command[0], command, env)

    # in Windows, we spawn a new process
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

    def terminate_proc() -> None:
        """Kill child process.

        All signals should be forwarded to the child processes
        automatically, however child processes are also free to ignore
        some of them. With this we make sure the child processes get
        killed once dotenv exits.

        """
        proc.kill()

    # register
    atexit.register(terminate_proc)

    _, _ = proc.communicate()

    # unregister
    atexit.unregister(terminate_proc)

    return proc.returncode
