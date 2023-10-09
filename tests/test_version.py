"""Tests for version module."""


def test_version() -> None:
    """Test version."""
    from dotenv_cli import __VERSION__

    assert isinstance(__VERSION__, str)
