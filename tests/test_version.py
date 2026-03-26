"""Test version is accessible."""

from miappe_api import __version__


def test_version_exists() -> None:
    """Version string should be defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)
