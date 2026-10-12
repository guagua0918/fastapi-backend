from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.security import get_current_member
from app.repositories import notes as notes_repo
from app.schemas.notes import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"], dependencies=[Depends(get_current_member)])
legacy_router = APIRouter(tags=["notes"], dependencies=[Depends(get_current_member)])


def _get_or_404(note_id: int) -> dict:
    note = notes_repo.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> dict:
    return notes_repo.create_note(note.title, note.content)


@router.get("", response_model=list[NoteResponse])
def list_notes() -> list[dict]:
    return notes_repo.list_notes()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int) -> dict:
    return _get_or_404(note_id)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteCreate) -> dict:
    updated = notes_repo.update_note(note_id, note.title, note.content)
    if updated is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int) -> Response:
    if not notes_repo.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@legacy_router.get("/note/{note_id}", response_model=NoteResponse)
def get_note_legacy(note_id: int) -> dict:
    return _get_or_404(note_id)
