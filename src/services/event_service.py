from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.models.Event import Event
from src.schemas.event_schemas import EventCreateModel, EventUpdateModel
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from typing import List
from src.models.Ticket import Ticket
from src.config.images import imagekit
from src.config.images import upload_event_poster, delete_event_poster
from src.models.Event import EventCategory


class EventService:
    async def get_all_events(self, session: AsyncSession):
        statement = select(Event).order_by(desc(Event.created_at))
        result = await session.exec(statement)
        data = result.all()
        return data

    async def get_event_by_Id(self, event_uid: UUID, session: AsyncSession):
        statement = select(Event).where(Event.event_uid == event_uid)
        result = await session.exec(statement)
        data = result.first()
        if data is not None:
            return data
        else:
            return None

    async def create_event(
        self,
        event_data: EventCreateModel,
        poster_bytes: bytes | None,
        poster_filename: str | None,
        session: AsyncSession,
    ):
        data = event_data.model_dump()
        data["event_date"] = datetime.strptime(data["event_date"], "%Y-%m-%d")

        if poster_bytes and poster_filename:
            upload_result = upload_event_poster(poster_bytes, poster_filename)
            data["event_poster_url"] = upload_result["url"]
            data["event_poster_file_id"] = upload_result["fileId"]

        new_event = Event(**data)
        session.add(new_event)

        try:
            await session.commit()
            await session.refresh(new_event)
        except Exception:
            await session.rollback()
            raise

        return new_event

    async def update_event(
        self, event_uid: UUID, update_body: EventUpdateModel, session: AsyncSession
    ):
        update_body_dict = update_body.model_dump()
        statement = select(Event).where(Event.event_uid == event_uid)
        result = await session.exec(statement)
        to_update = result.first()

        if to_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="event with the given id not found",
            )
        for key, value in update_body_dict.items():
            if value is not None:
                setattr(to_update, key, value)
        to_update.updated_at = datetime.now()
        await session.commit()
        await session.refresh(to_update)
        return to_update

    async def delete_event(self, event_uid: UUID, session: AsyncSession):
        statement = select(Event).where(Event.event_uid == event_uid)
        result = await session.exec(statement)
        to_delete = result.first()

        if to_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event with the given id not found",
            )

        if to_delete.event_poster_file_id:
            delete_event_poster(to_delete.event_poster_file_id)

        await session.delete(to_delete)
        await session.commit()

        return True

    async def get_event_tickets(self, event_uid: UUID, session: AsyncSession):
        event = await self.get_event_by_Id(event_uid=event_uid, session=session)
        return event.tickets

    async def get_event_by_category(
        self, event_tag: EventCategory, session: AsyncSession
    ):
        statement = (
            select(Event)
            .where(Event.event_tag == event_tag)
            .order_by(desc(Event.created_at))
        )
        result = await session.exec(statement)
        data = result.all()
        return data
