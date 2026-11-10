import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CSS = Path(__file__).resolve().parents[1] / "app" / "static" / "site.css"


def _html() -> str:
    response = client.get("/projects")
    assert response.status_code == 200
    return response.text


def _cards() -> list[str]:
    cards = re.findall(r'<article class="card".*?</article>', _html(), flags=re.DOTALL)
    assert len(cards) == 2, f"expected 2 project cards, found {len(cards)}"
    return cards


def test_projects_are_shown_as_two_cards() -> None:
    _cards()


def test_each_card_has_a_heading_and_a_status() -> None:
    for card in _cards():
        assert "<h2>" in card
        assert 'class="status"' in card


def test_status_labels_are_accurate() -> None:
    first, second = _cards()
    assert "zerotrustportfolio" in first
    assert ">Live<" in first
    assert "Imara FinTrust" in second
    assert ">In progress<" in second


def test_status_is_a_label_not_part_of_the_heading() -> None:
    assert "(in progress)" not in _html()


def test_each_card_lists_its_topics_as_tags() -> None:
    for card in _cards():
        match = re.search(r'<ul class="tags">(.*?)</ul>', card, flags=re.DOTALL)
        assert match, "card has no tag list"
        assert match.group(1).count("<li>") >= 3


def test_source_link_sits_inside_the_first_card() -> None:
    first, _ = _cards()
    assert "https://github.com/Omo-Dan/zerotrustportfolio" in first


def test_stylesheet_defines_the_card_styles() -> None:
    css = CSS.read_text(encoding="utf-8")
    for selector in (".card", ".status", ".tags"):
        assert f"{selector} {{" in css, f"site.css has no rule for {selector}"
