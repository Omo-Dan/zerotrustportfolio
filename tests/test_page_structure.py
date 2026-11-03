import re

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PAGES = ["/", "/about", "/skills", "/projects", "/certifications"]

NAV_ORDER = ["/", "/about", "/projects", "/skills", "/certifications"]


@pytest.mark.parametrize("path", PAGES)
def test_nothing_sits_between_the_navigation_and_the_main_content(path: str):
    html = client.get(path).text
    assert re.search(r"</nav>\s*<main[^>]*>", html)


@pytest.mark.parametrize("path", PAGES)
def test_page_closes_html_exactly_once(path: str):
    assert client.get(path).text.count("</html>") == 1


@pytest.mark.parametrize("path", PAGES)
def test_navigation_lists_pages_in_the_agreed_order(path: str):
    match = re.search(r"<nav>.*?</nav>", client.get(path).text, re.S)
    assert match is not None
    assert re.findall(r'<a href="([^"]+)"', match.group(0)) == NAV_ORDER
