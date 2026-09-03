"""KelvraSpace — Umbrella Dashboard & Unified Platform Hub.

Scaffold service running on port 8090.
Aggregates status, health, and telemetry across:
- Kelvra Voice (Port 8765)
- Kelvra Bench (Port 8099)
- Kelvra Security (Port 8100)
"""
import os
from pathlib import Path
from typing import Any, Dict
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Kelvra Space Hub",
    version="1.0.0",
    description="Umbrella control hub and platform orchestrator dashboard.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static asset mounts
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

VOICE_URL = os.getenv("KELVRA_VOICE_URL", "http://127.0.0.1:8765")
BENCH_URL = os.getenv("KELVRA_BENCH_URL", "http://127.0.0.1:8099")
SECURITY_URL = os.getenv("KELVRA_SECURITY_URL", "http://127.0.0.1:8100")


@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "kelvra-space",
        "port": 8090,
        "version": "1.0.0",
    }


@app.get("/api/overview")
async def get_ecosystem_overview() -> Dict[str, Any]:
    """Polls all three Kelvra products and aggregates their live operational status."""
    async with httpx.AsyncClient(timeout=1.5) as client:
        # 1. Voice
        voice_status = {"online": False, "detail": "Voice service unreachable"}
        try:
            r = await client.get(f"{VOICE_URL}/api/status")
            if r.status_code == 200:
                voice_status = {"online": True, **r.json()}
        except Exception:
            pass

        # 2. Bench
        bench_status = {"online": False, "detail": "Bench service unreachable"}
        try:
            r = await client.get(f"{BENCH_URL}/api/security/audit")
            if r.status_code == 200:
                bench_status = {"online": True, **r.json()}
        except Exception:
            pass

        # 3. Security
        sec_status = {"online": False, "detail": "Security service unreachable"}
        try:
            r = await client.get(f"{SECURITY_URL}/health")
            if r.status_code == 200:
                sec_status = {"online": True, **r.json()}
        except Exception:
            pass

    return {
        "hub": {
            "name": "Kelvra Space",
            "port": 8090,
            "status": "active",
        },
        "services": {
            "voice": {
                "name": "Kelvra Voice",
                "port": 8765,
                "url": VOICE_URL,
                **voice_status,
            },
            "bench": {
                "name": "Kelvra Bench",
                "port": 8099,
                "url": BENCH_URL,
                **bench_status,
            },
            "security": {
                "name": "Kelvra Security",
                "port": 8100,
                "url": SECURITY_URL,
                **sec_status,
            },
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)
