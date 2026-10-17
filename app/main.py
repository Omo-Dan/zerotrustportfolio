from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

# The API docs pages describe every route to anyone who asks, so they are off.
app = FastAPI(
    title="zerotrustportfolio",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; frame-ancestors 'none'; "
        "base-uri 'none'; form-action 'self'; object-src 'none'"
    ),
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}


@app.middleware("http")
async def add_security_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    for name, value in SECURITY_HEADERS.items():
        response.headers[name] = value
    return response


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}