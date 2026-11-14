import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _declares(filename: str, package: str) -> bool:
    pattern = re.compile(rf"^{package}\b", re.IGNORECASE)
    text = (ROOT / filename).read_text(encoding="utf-8")
    return any(pattern.match(line.strip()) for line in text.splitlines())


def test_dev_requirements_use_httpx2() -> None:
    assert _declares("requirements-dev.in", "httpx2")
    assert not _declares("requirements-dev.in", "httpx")


def test_dev_lock_pins_httpx2_and_not_httpx() -> None:
    assert _declares("requirements-dev.txt", "httpx2")
    assert not _declares("requirements-dev.txt", "httpx")


def test_pytest_turns_the_httpx_deprecation_into_an_error() -> None:
    text = (ROOT / "pytest.ini").read_text(encoding="utf-8")
    assert "error:Using .httpx. with .starlette.testclient. is deprecated" in text
