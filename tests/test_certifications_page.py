import re

from fastapi.testclient import TestClient

from app.main import SECURITY_HEADERS, app

client = TestClient(app)

BADGE = "https://www.credly.com/badges/925cf89c-cedb-4097-b995-9173e79a6bd6/public_url"


def main_html() -> str:
    response = client.get("/certifications")
    assert response.status_code == 200
    match = re.search(r"<main[^>]*>.*?</main>", response.text, re.S)
    assert match is not None
    return match.group(0)


def test_certifications_page_is_served_as_html():
    response = client.get("/certifications")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_certifications_page_has_a_title_and_a_heading():
    html = client.get("/certifications").text
    assert "<title>" in html
    assert "<h1>Certifications</h1>" in html


def test_certifications_page_lists_the_badge_with_its_issuer():
    main = main_html()
    assert "Amazon Web Services (AWS) Training Workshops" in main
    assert "Queensborough Community College" in main


def test_certification_links_to_its_public_verification_page():
    main = main_html()
    assert f'<a href="{BADGE}">verify</a>' in main


def test_certifications_page_has_no_placeholders():
    response = client.get("/certifications")
    assert response.status_code == 200
    html = response.text
    assert "YOUR-" not in html
    assert "[" not in html
    assert "]" not in html


def test_certifications_page_has_no_inline_scripts_or_styles():
    response = client.get("/certifications")
    assert response.status_code == 200
    html = response.text
    assert "<script" not in html
    assert "<style" not in html
    assert "style=" not in html


def test_certifications_page_sends_the_security_headers():
    response = client.get("/certifications")
    assert response.status_code == 200
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value
