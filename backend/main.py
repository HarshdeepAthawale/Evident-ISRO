"""
EVIDENT Main Application

This module initializes the FastAPI application and sets up all routes,
middleware, and configuration.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.core.config import settings
from backend.core.middleware import setup_middleware
from backend.core.database import init_db
from backend.utils.logger import StructuredLogger
from backend.auth.routes import router as auth_router

# Initialize logger
logger = StructuredLogger.get_logger()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Evidence-Grounded Intelligence for Document-Enabled Knowledge Systems",
    debug=settings.debug
)

# Set up middleware (CORS, error handling, logging)
setup_middleware(app)

# Include routers
app.include_router(auth_router)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(
        f"Starting {settings.app_name} v{settings.app_version}",
        extra={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
            "event": "application_startup"
        }
    )
    
    # Database tables are created via Alembic migrations
    # Uncomment below if you need to create tables programmatically:
    # init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info(
        f"Shutting down {settings.app_name}",
        extra={"event": "application_shutdown"}
    )


@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
