from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.routers import post as post_router
from main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI application."""
    yield TestClient(app)


@pytest.fixture(autouse=True)
def clear_tables() -> Generator[None, None, None]:
    """Clear post and comment tables before each test."""
    post_router.post_table.clear()
    post_router.comment_table.clear()
    yield
    post_router.post_table.clear()
    post_router.comment_table.clear()


@pytest.fixture
def sample_post() -> dict[str, str]:
    """Sample post data for testing."""
    return {"body": "This is a test post"}


@pytest.fixture
def sample_comment() -> dict[str, str | int]:
    """Sample comment data for testing."""
    return {"body": "This is a test comment", "post_id": 0}


@pytest.fixture
def created_post(client: TestClient, sample_post: dict[str, str]) -> dict:
    """Create a post and return the response data."""
    response = client.post("/post", json=sample_post)
    return response.json()


@pytest.fixture
def created_comment(
    client: TestClient, created_post: dict, sample_comment: dict[str, str | int]
) -> dict:
    """Create a comment on a post and return the response data."""
    response = client.post("/comment", json=sample_comment)
    return response.json()
