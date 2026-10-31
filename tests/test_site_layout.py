import re

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PAGES = ["/", "/about", "/skills", "/projects"]


def footer_of(path: str) -> str:
    match = re.search(r"<footer>.*?</footer>", client.get(path).text, re.S)
    assert match is not None
    return match.group(0)


@pytest.mark.parametrize("path", PAGES)
def test_page_has_exactly_one_footer(path: str):
    assert client.get(path).text.count("<footer>") == 1


@pytest.mark.parametrize("path", PAGES)
def test_footer_comes_after_the_main_content(path: str):
    assert re.search(r"</main>\s*<footer>", client.get(path).text)


@pytest.mark.parametrize("path", PAGES)
def test_footer_links_to_github_and_linkedin(path: str):
    footer = footer_of(path)
    assert "https://github.com/Omo-Dan/zerotrustportfolio" in footer
    assert "https://www.linkedin.com/in/daniel-omondi-ojiambo-852021180/" in footer


def test_every_page_shows_the_same_footer():
    footers = {footer_of(path) for path in PAGES}
    assert len(footers) == 1


@pytest.mark.parametrize("path", PAGES)
def test_page_has_exactly_one_navigation(path: str):
    assert client.get(path).text.count("<nav>") == 1
