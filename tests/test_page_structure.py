import re

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PAGES = ["/", "/about", "/skills", "/projects"]


@pytest.mark.parametrize("path", PAGES)
def test_nothing_sits_between_the_navigation_and_the_main_content(path: str):
    html = client.get(path).text
    assert re.search(r"</nav>\s*<main>", html)
