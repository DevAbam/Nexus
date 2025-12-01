from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.models.Event import Event
from src.schemas.event_schemas import EventCreateModel, EventUpdateModel
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status


# TODO -> remember to update the updated_at field after updating an event


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

    async def create_event(self, event_data: EventCreateModel, session: AsyncSession):
        event_data_dict = event_data.model_dump()
        event_data_dict["event_date"] = datetime.strptime(
            event_data_dict["event_date"], "%Y-%m-%d"
        )
        new_event = Event(**event_data_dict)
        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)
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

        await session.delete(to_delete)
        await session.commit()

        return True
