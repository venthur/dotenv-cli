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
            # un-escape escape characters
            control_chars = {
                r'\a': '\a',
                r'\b': '\b',
                r'\f': '\f',
                r'\n': '\n',
                r'\r': '\r',
                r'\t': '\t',
                r'\v': '\v',
                r'\\': '\\',
            }
            for char, repl in control_chars.items():
                value = value.replace(char, repl)

        elif len(value) >= 2 and value[0] == value[-1] == "'":
            value = value[1:-1]

        res[key] = value
    logger.debug(res)
    return res


def run_dotenv(
    filenames: list[str], command: list[str], replace: bool = False
) -> NoReturn | int:
    """Run dotenv.

    This function executes the commands with the environment variables
    parsed from filename.

    Parameters
    ----------
    filenames
        paths to the .env files
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
    # read dotenv files
    dotenv = {}
    for filename in filenames:
        dotenv.update(read_dotenv(filename))

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
