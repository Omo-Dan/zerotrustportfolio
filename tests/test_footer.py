import re
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PAGES = ["/", "/about", "/skills", "/projects", "/certifications"]
REPO = "https://github.com/Omo-Dan/zerotrustportfolio"
CSS = Path(__file__).resolve().parents[1] / "app" / "static" / "site.css"


def _footer(path: str) -> str:
    match = re.search(r"<footer>.*?</footer>", client.get(path).text, re.S)
    assert match is not None
    return match.group(0)


@pytest.mark.parametrize("path", PAGES)
def test_footer_names_the_owner(path: str) -> None:
    assert "Daniel Omondi Ojiambo" in _footer(path)


@pytest.mark.parametrize("path", PAGES)
def test_footer_links_to_the_github_profile(path: str) -> None:
    assert 'href="https://github.com/Omo-Dan"' in _footer(path)


@pytest.mark.parametrize("path", PAGES)
def test_footer_links_to_the_security_documents(path: str) -> None:
    assert f'href="{REPO}/tree/main/docs/security"' in _footer(path)


@pytest.mark.parametrize("path", PAGES)
def test_footer_states_the_security_first_approach(path: str) -> None:
    assert "security first" in _footer(path).lower()


@pytest.mark.parametrize("path", PAGES)
def test_footer_keeps_its_links_in_a_list(path: str) -> None:
    footer = _footer(path)
    assert '<ul class="footer-links">' in footer
    assert footer.count("<li>") == 3


@pytest.mark.parametrize("path", PAGES)
def test_footer_publishes_no_private_contact_details(path: str) -> None:
    footer = _footer(path).lower()
    for forbidden in ("mailto:", "tel:", "wa.me", "whatsapp"):
        assert forbidden not in footer, f"footer contains {forbidden}"


def test_stylesheet_styles_the_footer_links() -> None:
    assert ".footer-links {" in CSS.read_text(encoding="utf-8")


@pytest.mark.parametrize("path", PAGES)
def test_footer_shows_the_current_year(path: str) -> None:
    year = datetime.now(UTC).year
    assert f"&copy; {year}" in _footer(path)
