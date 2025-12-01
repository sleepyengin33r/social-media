from fastapi.testclient import TestClient


class TestCreateComment:
    """Tests for POST /comment endpoint."""

    def test_create_comment(
        self,
        client: TestClient,
        created_post: dict,
        sample_comment: dict[str, str | int],
    ):
        """Test creating a comment on an existing post."""
        response = client.post("/comment", json=sample_comment)

        assert response.status_code == 200

        data = response.json()
        assert data["body"] == sample_comment["body"]
        assert data["post_id"] == sample_comment["post_id"]
        assert "id" in data

    def test_create_comment_returns_id(
        self,
        client: TestClient,
        created_post: dict,
        sample_comment: dict[str, str | int],
    ):
        """Test that created comment has an id starting from 0."""
        response = client.post("/comment", json=sample_comment)

        data = response.json()
        assert data["id"] == 0

    def test_create_comment_on_nonexistent_post_fails(self, client: TestClient):
        """Test that creating a comment on non-existent post returns 404."""
        comment = {"body": "This should fail", "post_id": 999}
        response = client.post("/comment", json=comment)

        assert response.status_code == 404
        assert response.json()["detail"] == "Post not found"

    def test_create_comment_without_body_fails(
        self, client: TestClient, created_post: dict
    ):
        """Test that creating a comment without body returns validation error."""
        response = client.post("/comment", json={"post_id": 0})

        assert response.status_code == 422

    def test_create_multiple_comments_increments_id(
        self, client: TestClient, created_post: dict
    ):
        """Test that each new comment gets an incremented id."""
        comment1 = client.post("/comment", json={"body": "First", "post_id": 0})
        assert comment1.json()["id"] == 0

        comment2 = client.post("/comment", json={"body": "Second", "post_id": 0})
        assert comment2.json()["id"] == 1

        comment3 = client.post("/comment", json={"body": "Third", "post_id": 0})
        assert comment3.json()["id"] == 2


class TestGetComments:
    """Tests for GET /post/{post_id}/comment endpoint."""

    def test_get_comments_on_post(
        self,
        client: TestClient,
        created_post: dict,
        created_comment: dict,
    ):
        """Test getting comments on a post."""
        response = client.get(f"/post/{created_post['id']}/comment")

        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["body"] == created_comment["body"]

    def test_get_comments_on_post_with_no_comments(
        self, client: TestClient, created_post: dict
    ):
        """Test getting comments on a post with no comments."""
        response = client.get(f"/post/{created_post['id']}/comment")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_comments_returns_only_comments_for_specific_post(
        self, client: TestClient
    ):
        """Test that comments are filtered by post_id."""
        # Create two posts
        post1 = client.post("/post", json={"body": "Post 1"}).json()
        post2 = client.post("/post", json={"body": "Post 2"}).json()

        # Add comments to each post
        client.post(
            "/comment", json={"body": "Comment on post 1", "post_id": post1["id"]}
        )
        client.post(
            "/comment", json={"body": "Comment on post 2", "post_id": post2["id"]}
        )
        client.post(
            "/comment", json={"body": "Another on post 1", "post_id": post1["id"]}
        )

        # Get comments for post 1
        response = client.get(f"/post/{post1['id']}/comment")
        comments = response.json()

        assert len(comments) == 2
        assert all(c["post_id"] == post1["id"] for c in comments)


class TestGetPostWithComments:
    """Tests for GET /post/{post_id} endpoint."""

    def test_get_post_with_comments(
        self,
        client: TestClient,
        created_post: dict,
        created_comment: dict,
    ):
        """Test getting a post with its comments."""
        response = client.get(f"/post/{created_post['id']}")

        assert response.status_code == 200

        data = response.json()
        assert data["post"]["id"] == created_post["id"]
        assert data["post"]["body"] == created_post["body"]
        assert len(data["comments"]) == 1
        assert data["comments"][0]["body"] == created_comment["body"]

    def test_get_post_with_no_comments(self, client: TestClient, created_post: dict):
        """Test getting a post that has no comments."""
        response = client.get(f"/post/{created_post['id']}")

        assert response.status_code == 200

        data = response.json()
        assert data["post"]["id"] == created_post["id"]
        assert data["comments"] == []

    def test_get_nonexistent_post_fails(self, client: TestClient):
        """Test that getting a non-existent post returns 404."""
        response = client.get("/post/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Post not found"
