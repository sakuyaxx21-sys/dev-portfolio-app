"""Pytest configuration and shared test fixtures."""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.db import models  # noqa: F401


# Resolve project root and define test database path
BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DB_PATH = BASE_DIR / "test_test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"


# Create a SQLite engine for testing
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
)

# Create a dedicated session factory for tests
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
)


def override_get_db():
    # Override dependency to use the test database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    # Inject the test database dependency into the FastAPI app
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clear dependency overrides after each test
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def reset_test_database():
    # Reset the schema before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    # Clean up after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db_file():
    # Remove the SQLite file after all tests finish
    yield

    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()