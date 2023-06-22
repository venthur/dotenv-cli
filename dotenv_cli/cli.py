# remove when we don't support py38 anymore
from __future__ import annotations

import argparse
import logging
from typing import NoReturn

from dotenv_cli import __VERSION__
from dotenv_cli.core import run_dotenv

logger = logging.getLogger(__name__)


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse arguments.

    Paramters
    ---------
    args
        This if for debugging only.

    Returns
    -------
    argparse.Namespace

    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-e",
        "--dotenv",
        help="Alternative .env file",
        default=".env",
    )

    parser.add_argument(
        "command",
        help="Shell command to execute",
        nargs=argparse.REMAINDER,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=__VERSION__,
    )

    return parser.parse_args(args)


def main() -> NoReturn | int:
    """Run dotenv.

    This function parses sys.argv and runs dotenv.

    Returns
    -------
    int
        the return value

    """
    args = parse_args()
    if not args.command:
        return 0

    return run_dotenv(args.dotenv, args.command)
