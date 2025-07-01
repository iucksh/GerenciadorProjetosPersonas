"""FastAPI adapter exposing safe endpoints to WindSurf agents.

Endpoints:
- GET /monitor  → run monitor.py and return stdout
- POST /rotate  → rotate personas if needed or forced
- POST /report  → generate progress reports

Usage (dev):
    uvicorn scripts.windsurf_adapter:app --reload --port 8080
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from .adapter_utils import run_script, rotation_needed

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)  # ensure scripts run relative to project root

app = FastAPI(title="GPP WindSurf Adapter", version="0.1")


class ScriptResponse(BaseModel):
    returncode: int
    stdout: str
    stderr: str


@app.get("/monitor", response_model=ScriptResponse)
async def monitor():
    rc, out, err = await _async_run("monitor")
    return ScriptResponse(returncode=rc, stdout=out, stderr=err)


class RotateRequest(BaseModel):
    force: bool = False


@app.post("/rotate", response_model=ScriptResponse)
async def rotate(req: RotateRequest):
    if not req.force and not rotation_needed():
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                            detail="Rotation not needed according to monitor output.")
    rc, out, err = await _async_run("rotate")
    return ScriptResponse(returncode=rc, stdout=out, stderr=err)


@app.post("/report", response_model=ScriptResponse)
async def report():
    rc, out, err = await _async_run("report")
    return ScriptResponse(returncode=rc, stdout=out, stderr=err)


async def _async_run(key: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: run_script(key, check=False))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("scripts.windsurf_adapter:app", host="0.0.0.0", port=8080, reload=True)
