from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from src.services.event_service import EventService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database_config import get_session
from src.schemas.event_schemas import (
    EventModel,
    EventCreateModel,
    EventUpdateModel,
    EventCreateForm,
)
from src.models.Ticket import Ticket
from uuid import UUID
from typing import List
from src.config.images import validate_file_size, validate_image_type

event_router = APIRouter()
event_service = EventService()


@event_router.get("/", status_code=status.HTTP_200_OK, response_model=List[EventModel])
async def get_all_events(session: AsyncSession = Depends(get_session)):
    all_events = await event_service.get_all_events(session)
    return all_events


@event_router.get("/{event_uid}")
async def get_event_by_Id(
    event_uid: UUID, session: AsyncSession = Depends(get_session)
):
    event = await event_service.get_event_by_Id(event_uid, session)
    return (
        event
        if event is not None
        else HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="event not found"
        )
    )


@event_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreateForm = Depends(EventCreateForm.as_form),
    event_poster: UploadFile | None = File(None),
    session: AsyncSession = Depends(get_session),
):
    poster_bytes = None
    poster_filename = None

    if event_poster:
        # Validate image type
        validate_image_type(event_poster)

        # Validate file size
        poster_bytes = await validate_file_size(event_poster)
        poster_filename = event_poster.filename

    try:
        return await event_service.create_event(
            event_data, poster_bytes, poster_filename, session
        )
    except Exception:
        await session.rollback()
        raise


@event_router.patch(
    "/{id}", status_code=status.HTTP_201_CREATED, response_model=EventModel
)
async def update_event(
    event_uid: UUID,
    update_body: EventUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_event = await event_service.update_event(event_uid, update_body, session)
    return updated_event


@event_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_event(event_uid: UUID, session: AsyncSession = Depends(get_session)):
    deleted = await event_service.delete_event(event_uid, session)
    if deleted:
        return f"event with id {event_uid} deleted successfully"


@event_router.get(
    "/alltickets/{event_uid}",
    status_code=status.HTTP_200_OK,
    response_model=List[Ticket],
)
async def get_event_tickets(
    event_uid: UUID, session: AsyncSession = Depends(get_session)
):
    all_event_tickets = await event_service.get_event_tickets(event_uid, session)
    return all_event_tickets
