# Social Media API

A lightweight social media REST API built with FastAPI. Features posts and comments CRUD operations with cloud-native configuration.

## Features

- Create, read posts
- Create, read comments on posts
- Get posts with their comments
- Multi-environment configuration (development, staging, production)

## Tech Stack

- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation
- **pydantic-settings** - Environment configuration
- **SQLite** - Database (default)
- **pytest** - Testing

## Quick Start

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/social-media.git
cd social-media

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```bash
ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your-secret-key
```

### Run the Server

```bash
# With uv
uv run uvicorn main:app --reload

# Or directly
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

| Method | Endpoint                  | Description            |
| ------ | ------------------------- | ---------------------- |
| `POST` | `/post`                   | Create a new post      |
| `GET`  | `/post`                   | Get all posts          |
| `GET`  | `/post/{post_id}`         | Get post with comments |
| `POST` | `/comment`                | Create a comment       |
| `GET`  | `/post/{post_id}/comment` | Get comments on a post |

## Running Tests

```bash
# With uv
uv run pytest

# Or directly
pytest
```

## Project Structure

```
social-media/
├── main.py              # FastAPI application entry point
├── api/
│   ├── config.py        # Environment configuration
│   ├── models/
│   │   └── post.py      # Pydantic models
│   ├── routers/
│   │   └── post.py      # API routes
│   └── tests/
│       ├── conftest.py  # Test fixtures
│       ├── test_post.py
│       └── test_comment.py
├── pyproject.toml
└── .env                 # Environment variables (not committed)
```

## License

MIT
