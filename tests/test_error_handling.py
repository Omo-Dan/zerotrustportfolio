import pytest
from fastapi.testclient import TestClient

from app.main import app

LEAK_MARKERS = ["Traceback", 'File "', ".py", "internal-detail-should-not-leak"]


@pytest.fixture
def boom_route():
    """Temporarily add a route that always crashes, then remove it."""

    def boom():
        raise RuntimeError("internal-detail-should-not-leak")

    app.add_api_route("/_test_boom", boom)
    yield "/_test_boom"
    app.router.routes[:] = [
        route
        for route in app.router.routes
        if getattr(route, "path", None) != "/_test_boom"
    ]


def test_unhandled_error_returns_generic_500(boom_route):
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get(boom_route)
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    for marker in LEAK_MARKERS:
        assert marker not in response.text


def test_unhandled_error_still_has_security_headers(boom_route):
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get(boom_route)
    assert "content-security-policy" in response.headers
    assert "x-content-type-options" in response.headers


def test_unknown_path_is_generic():
    response = TestClient(app).get("/does-not-exist")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_wrong_method_is_generic():
    response = TestClient(app).post("/healthz")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}