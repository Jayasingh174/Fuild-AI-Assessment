"""Pydantic models for request/response validation and typing."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    """Request body for creating a note."""

    title: str = Field(..., min_length=1, description="Note title. Cannot be empty or whitespace-only.")
    content: str = Field(..., min_length=1, description="Note content. Cannot be empty or whitespace-only.")

    model_config = {"extra": "forbid"}

    @field_validator("title", "content")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty or whitespace only")
        return value


class NoteResponse(BaseModel):
    """Response body representing a stored note."""

    id: int
    title: str
    content: str
    created_at: datetime


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    detail: str