"""Command line interface for dotenv-cli."""


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
    parser = argparse.ArgumentParser(
        description=(
            "dotenv executes a given command with environment variables "
            "loaded from a .env file."
        ),
    )

    parser.add_argument(
        "-e",
        "--dotenv",
        help="alternative .env file",
        default=".env",
    )

    parser.add_argument(
        "command",
        help="shell command to execute",
        nargs=argparse.REMAINDER,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=__VERSION__,
    )

    parser.add_argument(
        "-r",
        "--replace",
        action="store_true",
        help=(
            "completely replace all existing environment variables with the "
            "ones loaded from the .env file"
            )
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

    return run_dotenv(args.dotenv, args.command, args.replace)
