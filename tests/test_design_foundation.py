from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
CSS = Path("app/static/site.css").read_text(encoding="utf-8")

TOKENS = (
    "--bg",
    "--ink",
    "--muted",
    "--line",
    "--panel",
    "--accent",
    "--on-accent",
)


def test_palette_tokens_defined():
    for token in TOKENS:
        assert f"{token}:" in CSS, f"missing {token}"


def test_light_palette_follows_the_device_setting():
    assert "prefers-color-scheme: light" in CSS


def test_links_and_controls_have_a_visible_focus_ring():
    assert "\n:focus-visible" in CSS


def test_reduced_motion_respected():
    assert "prefers-reduced-motion" in CSS


def test_skip_link_comes_before_the_navigation():
    html = client.get("/").text
    before_nav = html.split("<nav", 1)[0]
    assert 'class="skip-link"' in before_nav
    assert 'href="#main"' in before_nav
    assert 'id="main"' in html
