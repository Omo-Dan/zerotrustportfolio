from fastapi.testclient import TestClient

from app.main import SECURITY_HEADERS, app

client = TestClient(app)


def test_about_page_is_served_as_html():
    response = client.get("/about")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_about_page_has_a_title_and_a_heading():
    html = client.get("/about").text
    assert "<title>" in html
    assert "<h1>About</h1>" in html


def test_about_page_uses_the_stylesheet_file():
    html = client.get("/about").text
    assert 'href="/static/site.css"' in html


def test_about_page_has_no_inline_scripts_or_styles():
    response = client.get("/about")
    assert response.status_code == 200
    html = response.text
    assert "<script" not in html
    assert "<style" not in html
    assert "style=" not in html


def test_about_page_sends_the_security_headers():
    response = client.get("/about")
    assert response.status_code == 200
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value


def test_about_page_has_no_placeholders_left():
    response = client.get("/about")
    assert response.status_code == 200
    html = response.text
    assert "[" not in html
    assert "]" not in html


def test_landing_page_links_to_the_about_page():
    html = client.get("/").text
    assert 'href="/about"' in html


def test_skills_page_links_to_the_about_page():
    html = client.get("/skills").text
    assert 'href="/about"' in html
