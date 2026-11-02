import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
CSS = Path("app/static/site.css").read_text(encoding="utf-8")


def rule(selector: str) -> str:
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", CSS)
    assert match is not None, f"no rule for {selector}"
    return match.group(1)


def test_skills_render_as_wrapping_tags():
    body = rule(".skills")
    assert "display: flex" in body
    assert "flex-wrap: wrap" in body
    assert "list-style: none" in body


def test_each_skill_tag_has_a_visible_boundary():
    body = rule(".skills li")
    assert "border:" in body
    assert "background: var(--panel)" in body


def test_certifications_list_is_marked():
    html = client.get("/skills").text
    assert re.search(r'<h2>Certifications</h2>\s*<ul class="skills certs">', html)


def test_skills_page_has_no_placeholder_links():
    html = client.get("/skills").text
    assert "YOUR-" not in html
    assert "example.com" not in html
