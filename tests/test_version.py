import pytest
from fastapi.testclient import TestClient

from app.main import SECURITY_HEADERS, app

client = TestClient(app)


def test_version_reports_the_deployed_commit(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("RENDER_GIT_COMMIT", "0123456789abcdef0123456789abcdef01234567")
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"commit": "0123456789abcdef0123456789abcdef01234567"}


def test_version_says_unknown_when_no_commit_is_set(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"commit": "unknown"}


def test_version_sends_the_security_headers():
    response = client.get("/version")
    assert response.status_code == 200
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value
