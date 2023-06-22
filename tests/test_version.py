def test_version() -> None:
    from dotenv_cli import __VERSION__

    assert isinstance(__VERSION__, str)
