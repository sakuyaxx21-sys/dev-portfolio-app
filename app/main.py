"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.db import models  # noqa: F401
from app.core.exceptions import AppServiceError
from app.api.error_handlers import app_service_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup and shutdown lifecycle management
    # Create tables at startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Register the global handler for service-layer exceptions
app.add_exception_handler(AppServiceError, app_service_exception_handler)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "debug": settings.debug,
    }


# Mount all API v1 routes under the configured prefix
app.include_router(api_router, prefix=settings.api_v1_prefix)