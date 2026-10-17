from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

REQUIRED_HEADERS = [
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
    "permissions-policy",
]


def test_security_headers_on_normal_response():
    response = client.get("/healthz")
    for name in REQUIRED_HEADERS:
        assert name in response.headers, f"missing header: {name}"


def test_security_headers_on_error_response():
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    for name in REQUIRED_HEADERS:
        assert name in response.headers, f"missing header: {name}"


def test_csp_blocks_framing_and_unlisted_sources():
    csp = client.get("/healthz").headers.get("content-security-policy", "")
    assert "default-src" in csp
    assert "frame-ancestors 'none'" in csp


def test_hsts_and_nosniff_values():
    headers = client.get("/healthz").headers
    assert headers.get("strict-transport-security", "").startswith("max-age=")
    assert headers.get("x-content-type-options") == "nosniff"


def test_api_docs_are_not_exposed():
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert client.get(path).status_code == 404, f"{path} is exposed"