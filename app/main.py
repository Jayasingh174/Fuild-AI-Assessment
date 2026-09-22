"""FastAPI application: routes, status codes, and error handling."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import NoteNotFoundError
from app.models import ErrorResponse, NoteCreate, NoteResponse
from app.store import note_store

app = FastAPI(
    title="Notes API",
    description=(
        "A minimal, production-quality API for creating and retrieving notes. "
        "Storage is intentionally in-memory for this assignment; data does not "
        "persist across process restarts."
    ),
    version="1.0.0",
)


@app.exception_handler(NoteNotFoundError)
async def note_not_found_handler(request: Request, exc: NoteNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(detail=str(exc)).model_dump(),
    )


@app.post(
    "/notes",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Creates a note with a title and content. Returns the note with its generated ID and UTC timestamp.",
)
async def create_note(payload: NoteCreate) -> NoteResponse:
    return note_store.create(title=payload.title, content=payload.content)


@app.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse, "description": "Note not found"}},
    summary="Retrieve a note by ID",
    description="Returns the note with the given integer ID, or 404 if it does not exist.",
)
async def get_note(note_id: int) -> NoteResponse:
    note = note_store.get(note_id)
    if note is None:
        raise NoteNotFoundError(note_id)
    return note