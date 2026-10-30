import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SITE = "https://zerotrustportfolio.onrender.com"
PAGES = ["/", "/about", "/skills", "/projects"]


@pytest.mark.parametrize("path", PAGES)
def test_page_has_link_preview_tags(path: str):
    html = client.get(path).text
    for tag in (
        'property="og:title"',
        'property="og:description"',
        'property="og:type"',
        'property="og:site_name"',
    ):
        assert tag in html


@pytest.mark.parametrize("path", PAGES)
def test_page_declares_its_canonical_address(path: str):
    html = client.get(path).text
    address = f"{SITE}{path}"
    assert f'<link rel="canonical" href="{address}">' in html
    assert f'<meta property="og:url" content="{address}">' in html


@pytest.mark.parametrize("path", PAGES)
def test_page_links_the_favicon(path: str):
    html = client.get(path).text
    assert '<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">' in html


def test_favicon_is_served():
    response = client.get("/static/favicon.svg")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")