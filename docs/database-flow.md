# Database Configuration Flow

Visual guide to how `api/database.py` initializes the database.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         database.py EXECUTION FLOW                          │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │    IMPORTS      │
                              │  sqlalchemy     │
                              │  databases      │
                              │  settings       │
                              └────────┬────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: METADATA                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  metadata = sqlalchemy.MetaData()                                    │   │
│  │                                                                      │   │
│  │  Empty container waiting for table definitions                       │   │
│  │  ┌──────────────────────────────────────────────────┐               │   │
│  │  │  MetaData { tables: [] }                         │               │   │
│  │  └──────────────────────────────────────────────────┘               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: TABLE DEFINITIONS                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  post_table = Table("posts", metadata, ...)                          │   │
│  │  comments_table = Table("comments", metadata, ...)                   │   │
│  │                                                                      │   │
│  │  Tables register themselves with metadata                            │   │
│  │  ┌──────────────────────────────────────────────────┐               │   │
│  │  │  MetaData {                                      │               │   │
│  │  │    tables: [                                     │               │   │
│  │  │      "posts"    → {id, body}                     │               │   │
│  │  │      "comments" → {id, body, post_id}            │               │   │
│  │  │    ]                                             │               │   │
│  │  │  }                                               │               │   │
│  │  └──────────────────────────────────────────────────┘               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: CREATE ENGINE                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  engine = create_engine(DATABASE_URL)                                │   │
│  │                                                                      │   │
│  │  ┌──────────────┐         ┌─────────────────────────────┐           │   │
│  │  │   Engine     │ ──────► │  sqlite:///./dev.db         │           │   │
│  │  │  (sync)      │         │  (or PostgreSQL, etc.)      │           │   │
│  │  └──────────────┘         └─────────────────────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4: CREATE TABLES                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  metadata.create_all(engine)                                         │   │
│  │                                                                      │   │
│  │  ┌──────────────┐                     ┌─────────────────────────┐   │   │
│  │  │  MetaData    │ ───── SQL ────────► │     DATABASE FILE       │   │   │
│  │  │  + Engine    │                     │                         │   │   │
│  │  └──────────────┘                     │  CREATE TABLE posts     │   │   │
│  │        │                              │  CREATE TABLE comments  │   │   │
│  │        │                              └─────────────────────────┘   │   │
│  │        ▼                                                            │   │
│  │  CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, body)    │   │
│  │  CREATE TABLE IF NOT EXISTS comments (id, body, post_id → posts.id) │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 5: ASYNC DATABASE CONNECTION                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  database = Database(DATABASE_URL)                                   │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐                                               │   │
│  │  │  Async Database  │ ◄──── Used by FastAPI routes                  │   │
│  │  │  Connection      │                                               │   │
│  │  │                  │       await database.fetch_all(query)         │   │
│  │  │  • fetch_one()   │       await database.execute(query)           │   │
│  │  │  • fetch_all()   │                                               │   │
│  │  │  • execute()     │                                               │   │
│  │  └──────────────────┘                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Why Two Connections?

```
         ┌─────────────────────────────────────────────────┐
         │                                                 │
         │   ENGINE (sync)          DATABASE (async)       │
         │   ─────────────          ────────────────       │
         │   • Create tables        • CRUD operations      │
         │   • Migrations           • Used in routes       │
         │   • Schema changes       • Non-blocking I/O     │
         │   • One-time setup       • Concurrent requests  │
         │                                                 │
         └─────────────────────────────────────────────────┘
```

| Component    | Type         | Purpose                                                          |
| ------------ | ------------ | ---------------------------------------------------------------- |
| **Engine**   | Synchronous  | DDL operations (CREATE TABLE, migrations) - runs once at startup |
| **Database** | Asynchronous | CRUD operations in FastAPI routes - handles concurrent requests  |

## Summary

1. **Metadata** - Empty container for table schemas
2. **Table Definitions** - Register schemas with metadata
3. **Engine** - Sync connection to execute DDL
4. **Create Tables** - Run CREATE TABLE statements
5. **Async Database** - Ready for CRUD in routes
