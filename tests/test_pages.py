from fastapi.testclient import TestClient

from app.main import SECURITY_HEADERS, app

client = TestClient(app)


def test_landing_page_is_served_as_html():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_landing_page_has_a_title_and_a_heading():
    html = client.get("/").text
    assert "<title>" in html
    assert "<h1>" in html


def test_landing_page_links_to_the_source_code():
    html = client.get("/").text
    assert "https://github.com/Omo-Dan/zerotrustportfolio" in html


def test_landing_page_uses_the_stylesheet_file():
    html = client.get("/").text
    assert 'href="/static/site.css"' in html


def test_landing_page_has_no_inline_scripts_or_styles():
    # The content security policy only allows files served by this site.
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "<script" not in html
    assert "<style" not in html
    assert "style=" not in html


def test_landing_page_sends_the_security_headers():
    response = client.get("/")
    assert response.status_code == 200
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value


def test_stylesheet_is_served():
    response = client.get("/static/site.css")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/css")