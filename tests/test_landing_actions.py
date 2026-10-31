import re

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

GITHUB = "https://github.com/Omo-Dan/zerotrustportfolio"
LINKEDIN = "https://www.linkedin.com/in/daniel-omondi-ojiambo-852021180/"


def main_of(path: str) -> str:
    match = re.search(r"<main>.*?</main>", client.get(path).text, re.S)
    assert match is not None
    return match.group(0)


def test_landing_page_has_a_github_button():
    assert f'<a class="button" href="{GITHUB}">' in main_of("/")


def test_landing_page_has_a_linkedin_button():
    assert f'<a class="button" href="{LINKEDIN}">' in main_of("/")
