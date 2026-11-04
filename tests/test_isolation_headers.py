import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ISOLATION_HEADERS = {
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cross-Origin-Resource-Policy": "same-origin",
}


@pytest.mark.parametrize("path", ["/", "/about", "/healthz", "/does-not-exist"])
def test_responses_isolate_the_site_from_other_origins(path: str):
    response = client.get(path)
    for name, value in ISOLATION_HEADERS.items():
        assert response.headers[name] == value
