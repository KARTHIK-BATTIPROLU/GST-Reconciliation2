"""
FastAPI application entry point.

- Enables CORS for Streamlit (localhost:8501)
- Registers all route modules
- Manages database connections on startup / shutdown
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import close_connections
from backend.routes import health, test_mongo, test_neo4j, ingest, graph, dashboard

from backend.config import get_settings

settings = get_settings()

# ── Lifespan (startup + shutdown) ─────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: connections are lazily created on first use.
    Shutdown: close all database connections cleanly."""
    yield
    await close_connections()


# ── App instance ──────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# ── CORS ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────
app.include_router(health.router)
app.include_router(test_mongo.router)
app.include_router(test_neo4j.router)
app.include_router(ingest.router)
app.include_router(graph.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Root"])
async def root():
    """Minimal root endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Backend is running."}
