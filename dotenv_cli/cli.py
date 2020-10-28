import argparse
import logging

from dotenv_cli.core import run_dotenv
from dotenv_cli import __VERSION__


logger = logging.getLogger(__name__)


def parse_args(args=None):
    """Parse arguments.

    Paramters
    ---------
    args : list[str]
        This if for debugging only.

    Returns
    -------
    argparse.Namespace

    """
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

    parser.add_argument(
        '--version',
        action='version',
        version=__VERSION__,
    )

    return parser.parse_args(args)


def main():
    """Run dotenv.

    This function parses sys.argv and runs dotenv.

    Returns
    -------
    int
        the return value

    """
    args = parse_args()
    if not args.command:
        return

    return run_dotenv(args.dotenv, args.command)
