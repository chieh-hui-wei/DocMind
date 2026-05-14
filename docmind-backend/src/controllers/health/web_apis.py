"""
src/controllers/health/web_apis.py
Health check endpoints for liveness and readiness probes.
"""
from fastapi import APIRouter
from pydantic import BaseModel

from src.configs.settings import settings

router = APIRouter(prefix="/health")


class HealthResponse(BaseModel):
    status: str
    env: str
    version: str


@router.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", env=settings.ENV, version="1.0.0")
