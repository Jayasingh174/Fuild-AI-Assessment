"""Automated tests for the Notes API."""

from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.store import note_store

client = TestClient(app)


def setup_function() -> None:
    """Reset in-memory state before each test so tests stay independent."""
    note_store._notes.clear()
    note_store._next_id = 1


def test_create_note_returns_201() -> None:
    response = client.post("/notes", json={"title": "Groceries", "content": "Milk, eggs, bread"})
    assert response.status_code == 201


def test_create_note_response_contains_core_fields() -> None:
    response = client.post("/notes", json={"title": "Groceries", "content": "Milk"})
    body = response.json()
    assert set(body.keys()) == {"id", "title", "content", "created_at"}
    assert body["title"] == "Groceries"
    assert body["content"] == "Milk"


def test_created_id_is_integer() -> None:
    response = client.post("/notes", json={"title": "A", "content": "B"})
    assert isinstance(response.json()["id"], int)


def test_created_at_is_present_and_valid_iso_datetime() -> None:
    response = client.post("/notes", json={"title": "A", "content": "B"})
    created_at = response.json()["created_at"]
    # Raises ValueError if not a valid ISO datetime string.
    datetime.fromisoformat(created_at)


def test_get_existing_note_returns_200_and_matches_created_data() -> None:
    create_response = client.post("/notes", json={"title": "Trip plan", "content": "Pack early"})
    created = create_response.json()

    get_response = client.get(f"/notes/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created


def test_get_missing_note_returns_404() -> None:
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note with ID 999 was not found."}


def test_empty_title_is_rejected() -> None:
    response = client.post("/notes", json={"title": "", "content": "Some content"})
    assert response.status_code == 422


def test_whitespace_only_title_is_rejected() -> None:
    response = client.post("/notes", json={"title": "   ", "content": "Some content"})
    assert response.status_code == 422


def test_empty_content_is_rejected() -> None:
    response = client.post("/notes", json={"title": "Some title", "content": ""})
    assert response.status_code == 422


def test_missing_title_is_rejected() -> None:
    response = client.post("/notes", json={"content": "Some content"})
    assert response.status_code == 422


def test_missing_content_is_rejected() -> None:
    response = client.post("/notes", json={"title": "Some title"})
    assert response.status_code == 422


def test_wrong_type_for_title_is_rejected() -> None:
    response = client.post("/notes", json={"title": 123, "content": "Some content"})
    assert response.status_code == 422


def test_invalid_note_id_type_is_rejected() -> None:
    response = client.get("/notes/not-a-number")
    assert response.status_code == 422


def test_multiple_notes_receive_unique_ids() -> None:
    first = client.post("/notes", json={"title": "One", "content": "First"}).json()
    second = client.post("/notes", json={"title": "Two", "content": "Second"}).json()
    assert first["id"] != second["id"]


def test_unexpected_field_is_rejected() -> None:
    response = client.post(
        "/notes",
        json={"title": "A", "content": "B", "extra_field": "not allowed"},
    )
    assert response.status_code == 422