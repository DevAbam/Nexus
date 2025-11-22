from fastapi import APIRouter, Depends, status
from src.services.event_service import EventService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database_config import get_session
from src.schemas.event_schemas import EventModel, EventCreateModel
from typing import List

event_router = APIRouter()
event_service = EventService()


@event_router.get("/", status_code=status.HTTP_200_OK, response_model=List[EventModel])
async def get_all_events(session: AsyncSession = Depends(get_session)):
    all_events = await event_service.get_all_events(session)
    return all_events


@event_router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventModel)
async def create_event(
    event_data: EventCreateModel, session: AsyncSession = Depends(get_session)
):
    created_event = await event_service.create_event(event_data, session)
    return created_event
