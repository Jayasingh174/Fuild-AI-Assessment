"""Custom exceptions used to keep route handlers declarative."""


class NoteNotFoundError(Exception):
    """Raised when a note lookup fails. Caught by a FastAPI exception handler."""

    def __init__(self, note_id: int) -> None:
        self.note_id = note_id
        super().__init__(f"Note with ID {note_id} was not found.")