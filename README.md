# Notes API

A small, production-quality FastAPI service for creating and retrieving notes.

## Overview

This API implements exactly two endpoints:

- `POST /notes` — create a note
- `GET /notes/{id}` — retrieve a note by ID

Storage is **intentionally in-memory** — this is an explicit requirement of
the assignment, not an oversight. Data does not persist across restarts, and
there is no database, authentication, or other infrastructure. The goal is a
small, correct, well-tested service, not a fully productionized system.

## Project structure

```text
notes-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routes, HTTP status codes, error handling
│   ├── models.py        # Pydantic request/response models and validation
│   ├── store.py         # In-memory storage and ID generation
│   └── exceptions.py    # Custom exception (NoteNotFoundError)
├── tests/
│   ├── __init__.py
│   └── test_notes.py
├── requirements.txt
└── README.md


## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.
Interactive docs: `http://127.0.0.1:8000/docs`.

## Running tests

```bash
pytest
```

## API endpoints

### `POST /notes`

Create a new note.

**Request body:**

```json
{
  "title": "Groceries",
  "content": "Milk, eggs, bread"
}
```

**Success response — `201 Created`:**

```json
{
  "id": 1,
  "title": "Groceries",
  "content": "Milk, eggs, bread",
  "created_at": "2026-09-22T10:15:30.123456+00:00"
}
```

**Validation error — `422 Unprocessable Entity`:**

Returned when `title` or `content` is missing, empty, whitespace-only, the
wrong type, or when an unexpected field is included in the request body.

### `GET /notes/{id}`

Retrieve a note by its integer ID.

**Success response — `200 OK`:**

```json
{
  "id": 1,
  "title": "Groceries",
  "content": "Milk, eggs, bread",
  "created_at": "2026-09-22T10:15:30.123456+00:00"
}
```

**Not found — `404 Not Found`:**

```json
{
  "detail": "Note with ID 999 was not found."
}
```

**Invalid ID type — `422 Unprocessable Entity`:**

Returned when the path segment cannot be parsed as an integer (e.g.
`GET /notes/abc`).

## Key design decisions

- **In-memory storage is deliberate.** `app/store.py` holds a single
  `NoteStore` instance with a dict keyed by ID and an incrementing counter.
  It's the assignment requirement, documented rather than "solved."
- **Explicit response models everywhere.** No endpoint returns a raw dict;
  everything goes through `NoteResponse`, so the OpenAPI schema is accurate
  and consumers get typed, predictable payloads.
- **Validation lives in Pydantic, not in route logic.** `NoteCreate` rejects
  missing fields, empty strings, whitespace-only strings, wrong types, and
  unexpected extra fields (`extra: "forbid"`) — routes stay free of manual
  `if` checks.
- **Timezone-aware timestamps.** `created_at` is generated with
  `datetime.now(timezone.utc)`, never a naive datetime.
- **A custom exception, not inline `HTTPException`.** `NoteNotFoundError` is
  raised in the route and translated to a 404 by a single exception handler,
  keeping the "not found" message in one place instead of duplicated.
- **No unrequested endpoints or infrastructure.** No `DELETE`/`PUT`, no
  pagination, no auth, no database — only what the specification asks for.

## Limitations (by design)

- Data is lost when the process restarts (in-memory only).
- Not thread-safe for concurrent writes (acceptable for this scope; a real
  deployment behind a database or a lock would address this).
- No authentication/authorization (explicitly out of scope)."# Fuild-AI-Assessment" 
