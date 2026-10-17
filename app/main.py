import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

logger = logging.getLogger("app")

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


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception) -> JSONResponse:
    # Details go to the log only. The visitor gets a plain message.
    logger.error(
        "Unhandled error on %s %s", request.method, request.url.path, exc_info=exc
    )
    # This handler runs outside the middleware above, so it sets the
    # security headers itself.
    return JSONResponse(
        {"detail": "Internal Server Error"},
        status_code=500,
        headers=SECURITY_HEADERS,
    )


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}