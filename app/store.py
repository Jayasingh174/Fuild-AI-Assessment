"""In-memory note storage. Encapsulates ID generation and persistence."""

from datetime import datetime, timezone
from typing import Dict, Optional

from app.models import NoteResponse


class NoteStore:
    """Thread-unsafe, process-local, in-memory note store.

    Intentionally simple: a dict keyed by ID plus an incrementing counter.
    Data is lost on process restart — this is a requirement of the
    assignment, not an oversight.
    """

    def __init__(self) -> None:
        self._notes: Dict[int, NoteResponse] = {}
        self._next_id: int = 1

    def create(self, title: str, content: str) -> NoteResponse:
        note = NoteResponse(
            id=self._next_id,
            title=title,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        self._notes[note.id] = note
        self._next_id += 1
        return note

    def get(self, note_id: int) -> Optional[NoteResponse]:
        return self._notes.get(note_id)


# Single shared instance used by the application.
note_store = NoteStore()