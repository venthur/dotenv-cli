"""Test read_dotenv with unreadable dotenv paths."""

from pathlib import Path

from dotenv_cli import core


def test_directory_dotenv_returns_empty(tmp_path: Path) -> None:
    """A directory passed as dotenv file warns, returns empty dict."""
    env = core.read_dotenv(str(tmp_path))
    assert env == {}


def test_missing_dotenv_still_returns_empty(tmp_path: Path) -> None:
    """Missing dotenv file behavior is unchanged (regression guard)."""
    env = core.read_dotenv(str(tmp_path / "i.dont.exist"))
    assert env == {}
