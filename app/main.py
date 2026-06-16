"""60's Pulse FastAPI server.

Rung 0: serve the broadsheet dashboard (static) + the baked golden run.
The dashboard is a pure render of /api/golden, so nothing here calls a sponsor API.
Run:  uvicorn app.main:app --reload  (from the repo root, with the venv active)
"""
import json
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(ROOT, "app", "static")
GOLDEN_PATH = os.path.join(ROOT, "demo", "golden_run.json")

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))  # so live /api/analyze has the API keys
except Exception:
    pass

app = FastAPI(title="60's Pulse", version="0.1.0")


@app.get("/healthz")
def healthz():
    return {"ok": True, "mode": "fixture"}


@app.get("/api/golden")
def api_golden():
    """The single object the dashboard renders. Rung 0 = baked fixture."""
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        return JSONResponse(json.load(f))


@app.post("/api/analyze")
async def api_analyze(payload: dict):
    """Live 'paste your own campaign' path: regenerate the 60-agent panel for the typed input."""
    campaign = (payload.get("campaign") or "").strip()
    if not campaign:
        return JSONResponse({"detail": "campaign text required"}, status_code=400)
    brand = (payload.get("brand") or "").strip() or "the brand"
    provider = payload.get("provider") or "kimi"
    from app.analyze import analyze
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        golden = json.load(f)
    try:
        result = await analyze(campaign, brand, golden, provider=provider, mode="live")
    except Exception as e:
        return JSONResponse({"detail": f"{type(e).__name__}: {e}"}, status_code=502)
    return JSONResponse(result)


# Mount the dashboard last so the explicit /api routes win.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
