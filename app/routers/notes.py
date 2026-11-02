from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.security import get_current_member
from app.repositories import notes as notes_repo
from app.schemas.notes import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"], dependencies=[Depends(get_current_member)])
legacy_router = APIRouter(tags=["notes"], dependencies=[Depends(get_current_member)])


async def _get_or_404(note_id: int) -> dict:
    note = await notes_repo.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate) -> dict:
    return await notes_repo.create_note(note.title, note.content)


@router.get("", response_model=list[NoteResponse])
async def list_notes() -> list[dict]:
    return await notes_repo.list_notes()


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int) -> dict:
    return await _get_or_404(note_id)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteCreate) -> dict:
    updated = await notes_repo.update_note(note_id, note.title, note.content)
    if updated is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int) -> Response:
    if not await notes_repo.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@legacy_router.get("/note/{note_id}", response_model=NoteResponse)
async def get_note_legacy(note_id: int) -> dict:
    return await _get_or_404(note_id)
