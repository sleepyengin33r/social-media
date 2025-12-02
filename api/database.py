"""
Database configuration and table definitions.

This module sets up the database connection and defines the schema
for posts and comments tables using SQLAlchemy Core.
"""

import sqlalchemy
from databases import Database

from api.config import settings

# =============================================================================
# 1. METADATA REGISTRY
# =============================================================================
# MetaData is a container that holds all table definitions.
# Tables register themselves with this object when defined.
metadata = sqlalchemy.MetaData()

# =============================================================================
# 2. TABLE DEFINITIONS
# =============================================================================
# Define table schemas. These are registered with the metadata object above.
# At this point, tables only exist as Python objects, not in the database.

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id")),
)

# =============================================================================
# 3. CREATE DATABASE ENGINE
# =============================================================================
# Engine is a synchronous connection factory used for DDL operations
# (creating/dropping tables). It manages the connection pool.
engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.DATABASE_URL
    else {},
)

# =============================================================================
# 4. CREATE TABLES
# =============================================================================
# Execute CREATE TABLE statements for all tables registered in metadata.
# This is idempotent - tables are only created if they don't exist.
metadata.create_all(engine)

# =============================================================================
# 5. ASYNC DATABASE CONNECTION
# =============================================================================
# The `databases` library provides async database access for FastAPI.
# Use this for all CRUD operations in your routes.
database = Database(settings.DATABASE_URL)
