from fastapi import FastAPI

app = FastAPI(title="zerotrustportfolio")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}