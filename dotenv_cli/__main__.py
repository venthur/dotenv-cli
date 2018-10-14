import sys
import os
import argparse
from subprocess import Popen, PIPE, STDOUT
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument(
    '-e',
    '--dotenv',
    help='Alternative .env file',
    default='.env',
)
parser.add_argument(
    'command',
    help='Shell command to execute',
    nargs=argparse.REMAINDER,
)

def read_dotenv(dotenv):
    with open(dotenv, 'r') as fh:
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


def main():
    args = parser.parse_args()
    if not args.command:
        return

    # read dotenv
    dotenv = read_dotenv(args.dotenv)

    # update env
    env = os.environ.copy()
    env.update(dotenv)


    # execute
    proc = Popen(
        args.command,
        #stdin=PIPE,
        #stdout=PIPE,
        #stderr=STDOUT,
        universal_newlines=True,
        bufsize=0,
        shell=False,
        env=env,
    )
    _, _ = proc.communicate()
    return proc.returncode


if __name__ == '__main__':
    main()
