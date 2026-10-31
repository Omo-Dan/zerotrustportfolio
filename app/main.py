import logging
import os
from collections.abc import Awaitable, Callable
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import load_settings

logger = logging.getLogger("app")
settings = load_settings()

# The API docs pages describe every route to anyone who asks, so they are off.
app = FastAPI(
    title="zerotrustportfolio",
    debug=settings.debug,
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


BASE_DIR = Path(__file__).parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def page(request: Request, name: str) -> Response:
    return templates.TemplateResponse(request, name)


@app.get("/")
def landing(request: Request) -> Response:
    return page(request, "pages/index.html")


@app.get("/about")
def about(request: Request) -> Response:
    return page(request, "pages/about.html")


@app.get("/skills")
def skills(request: Request) -> Response:
    return page(request, "pages/skills.html")


@app.get("/projects")
def projects(request: Request) -> Response:
    return page(request, "pages/projects.html")


@app.get("/version")
def version() -> dict[str, str]:
    return {"commit": os.environ.get("RENDER_GIT_COMMIT", "unknown")}
