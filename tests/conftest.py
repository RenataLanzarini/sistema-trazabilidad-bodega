import pytest


@pytest.fixture(scope="session")
def test_environment() -> str:
    return "testing"
