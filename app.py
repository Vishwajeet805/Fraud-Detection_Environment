"""
app.py — FastAPI server for the Fraud Detection OpenEnv Environment.

Exposes the standard OpenEnv HTTP API:
  POST /reset          → FraudObservation
  POST /step           → StepResult
  GET  /state          → EnvironmentState
  GET  /tasks          → List of available tasks
  GET  /health         → Health check
  GET  /               → Info

Compatible with Hugging Face Spaces and openenv validate.
"""

from __future__ import annotations

import os
import sys

# Ensure local modules are importable when run from the project root
sys.path.insert(0, os.path.dirname(__file__))

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from env import FraudDetectionEnv
from models import FraudAction, FraudObservation, StepResult, EnvironmentState
from tasks import ALL_TASKS

# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Fraud Detection OpenEnv",
    description=(
        "Adaptive Phishing & Fraud Detection Environment for training and evaluating AI agents. "
        "Implements the full OpenEnv specification with step(), reset(), and state() endpoints."
    ),
    version="0.1.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment registry (one env per task, lazy-initialized)
_envs: Dict[str, FraudDetectionEnv] = {}
_current_task: str = "easy_fraud_detection"


def get_env(task_name: str = None) -> FraudDetectionEnv:
    """Get or create the environment for the given task."""
    global _current_task
    if task_name:
        _current_task = task_name
    if _current_task not in _envs:
        _envs[_current_task] = FraudDetectionEnv(task_name=_current_task)
    return _envs[_current_task]


# ── Request / Response helpers ───────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_name: Optional[str] = "easy_fraud_detection"


class StepRequest(BaseModel):
    action: int
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    task_name: Optional[str] = None


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name": "Fraud Detection OpenEnv",
        "version": "0.1.0",
        "tasks": list(ALL_TASKS.keys()),
        "endpoints": ["/reset", "/step", "/state", "/tasks", "/health"],
        "spec": "openenv>=0.2.0",
    }


@app.get("/health")
async def health():
    return {"status": "ok", "environment": "fraud_detection"}


@app.get("/tasks")
async def list_tasks():
    return {
        task_name: {
            "description": cfg["description"],
            "difficulty": cfg["difficulty"],
            "num_samples": len(cfg["samples"]),
            "passing_threshold": cfg["passing_threshold"],
        }
        for task_name, cfg in ALL_TASKS.items()
    }


@app.post("/reset")
async def reset(request: ResetRequest = None):
    """
    Reset the environment and return the first observation.
    Optionally specify a task_name to switch tasks.
    """
    try:
        task_name = "easy_fraud_detection"
        if request and request.task_name:
            task_name = request.task_name

        if task_name not in ALL_TASKS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown task '{task_name}'. Available: {list(ALL_TASKS.keys())}",
            )

        env = get_env(task_name)
        obs: FraudObservation = env.reset()
        return obs.model_dump()

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/step")
async def step(request: StepRequest):
    """
    Apply an action to the current environment state.
    Returns observation, reward, done flag, and info dict.
    """
    try:
        task_name = request.task_name or _current_task
        env = get_env(task_name)

        if env.done:
            raise HTTPException(
                status_code=400,
                detail="Episode is done. Call POST /reset to start a new episode.",
            )

        if request.action not in (0, 1, 2):
            raise HTTPException(
                status_code=400,
                detail="action must be 0 (Safe), 1 (Fraud), or 2 (Suspicious).",
            )

        action = FraudAction(
            action=request.action,
            confidence=request.confidence,
            reasoning=request.reasoning,
        )
        result: StepResult = env.step(action)
        return result.model_dump()

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/state")
async def state(task_name: Optional[str] = None):
    """Return the full current environment state."""
    try:
        env = get_env(task_name)
        env_state: EnvironmentState = env.state()
        return env_state.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# Serve static assets (JS/CSS)
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

# Root → index.html
@app.get("/")
async def serve_react():
    return FileResponse("dist/index.html")


# ── Exception handler ─────────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
