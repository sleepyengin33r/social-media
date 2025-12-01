from fastapi.testclient import TestClient


class TestCreatePost:
    """Tests for POST /post endpoint."""

    def test_create_post(self, client: TestClient, sample_post: dict[str, str]):
        """Test creating a new post."""
        response = client.post("/post", json=sample_post)

        assert response.status_code == 200

        data = response.json()
        assert data["body"] == sample_post["body"]
        assert "id" in data

    def test_create_post_returns_id(
        self, client: TestClient, sample_post: dict[str, str]
    ):
        """Test that created post has an id starting from 0."""
        response = client.post("/post", json=sample_post)

        data = response.json()
        assert data["id"] == 0

    def test_create_multiple_posts_increments_id(
        self, client: TestClient, sample_post: dict[str, str]
    ):
        """Test that each new post gets an incremented id."""
        # Create first post
        response1 = client.post("/post", json=sample_post)
        assert response1.json()["id"] == 0

        # Create second post
        response2 = client.post("/post", json={"body": "Second post"})
        assert response2.json()["id"] == 1

        # Create third post
        response3 = client.post("/post", json={"body": "Third post"})
        assert response3.json()["id"] == 2

    def test_create_post_without_body_fails(self, client: TestClient):
        """Test that creating a post without body returns validation error."""
        response = client.post("/post", json={})

        assert response.status_code == 422  # Validation error


class TestGetPosts:
    """Tests for GET /post endpoint."""

    def test_get_all_posts_empty(self, client: TestClient):
        """Test getting posts when none exist."""
        response = client.get("/post")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_posts(self, client: TestClient, created_post: dict):
        """Test getting all posts."""
        response = client.get("/post")

        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["body"] == created_post["body"]

    def test_get_all_posts_multiple(self, client: TestClient):
        """Test getting multiple posts."""
        # Create multiple posts
        client.post("/post", json={"body": "First post"})
        client.post("/post", json={"body": "Second post"})
        client.post("/post", json={"body": "Third post"})

        response = client.get("/post")

        assert response.status_code == 200
        assert len(response.json()) == 3
