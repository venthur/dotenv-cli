import argparse
import logging
import sys

from dotenv_cli.core import run_dotenv


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


def main():
    args = parser.parse_args()
    if not args.command:
        return

    return run_dotenv(args.dotenv, args.command)


if __name__ == '__main__':
    # sys exit?
    main()
