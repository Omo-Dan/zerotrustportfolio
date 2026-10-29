from fastapi.testclient import TestClient

from app.main import SECURITY_HEADERS, app

client = TestClient(app)


def test_projects_page_is_served_as_html():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_projects_page_has_a_title_and_a_heading():
    html = client.get("/projects").text
    assert "<title>" in html
    assert "<h1>Projects</h1>" in html


def test_projects_page_lists_this_project_with_its_source_code():
    html = client.get("/projects").text
    assert "zerotrustportfolio" in html
    assert "https://github.com/Omo-Dan/zerotrustportfolio" in html


def test_projects_page_uses_the_stylesheet_file():
    html = client.get("/projects").text
    assert 'href="/static/site.css"' in html


def test_projects_page_has_no_inline_scripts_or_styles():
    response = client.get("/projects")
    assert response.status_code == 200
    html = response.text
    assert "<script" not in html
    assert "<style" not in html
    assert "style=" not in html


def test_projects_page_sends_the_security_headers():
    response = client.get("/projects")
    assert response.status_code == 200
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value


def test_projects_page_has_no_placeholders_left():
    response = client.get("/projects")
    assert response.status_code == 200
    html = response.text
    assert "[" not in html
    assert "]" not in html


def test_every_page_links_to_the_projects_page():
    for path in ("/", "/about", "/skills"):
        html = client.get(path).text
        assert 'href="/projects"' in html
