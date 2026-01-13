"""FastAPI backend application."""

from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="FixFlow API", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "message": "FixFlow API is running"}
