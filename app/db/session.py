"""Database session and engine configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Create DB engine (supports both SQLite and PostgreSQL)
engine = create_engine(
    settings.database_url,

    # Required only for SQLite (multi-thread handling)
    connect_args=(
        {"check_same_thread": False} 
        if "sqlite" in settings.database_url 
        else {}
    ),

    # Automatically checks connection before use
    pool_pre_ping=True,
)

# Factory for DB sessions (used per request)
SessionLocal = sessionmaker(
    autocommit=False,   # Explicit commit control
    autoflush=False,    # Avoid unintended flush before commit
    bind=engine,
)


def get_db():
    """Provide a database session (FastAPI dependency)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session after the request
        db.close()