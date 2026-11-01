import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
CSS = Path("app/static/site.css").read_text(encoding="utf-8")

CHECKS = ("secret-scan", "quality", "semgrep", "dependency-audit", "container")


def main_html() -> str:
    match = re.search(r"<main[^>]*>.*?</main>", client.get("/").text, re.S)
    assert match is not None
    return match.group(0)


def panel_html() -> str:
    match = re.search(r'<section class="checks".*?</section>', main_html(), re.S)
    assert match is not None
    return match.group(0)


def test_view_projects_is_the_single_primary_button():
    main = main_html()
    assert main.count("button--primary") == 1
    assert (
        '<a class="button button--primary" href="/projects">View projects</a>' in main
    )


def test_primary_button_comes_before_the_secondary_buttons():
    main = main_html()
    assert (
        main.index("View projects")
        < main.index("View on GitHub")
        < main.index("Connect on LinkedIn")
    )


def test_checks_panel_lists_the_required_checks():
    panel = panel_html()
    for name in CHECKS:
        assert f"<li>{name}</li>" in panel


def test_checks_panel_has_a_heading():
    assert "<h2" in panel_html()


def test_checks_panel_makes_no_live_status_claims():
    assert "pass" not in panel_html().lower()


def test_hero_styles_exist():
    assert ".button--primary" in CSS
    assert ".checks" in CSS
