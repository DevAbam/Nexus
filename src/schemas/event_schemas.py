import uuid
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional
from src.models.Event import EventCategory
from fastapi import Form


class EventModel(BaseModel):
    event_uid: uuid.UUID
    event_name: str
    event_description: str
    event_location_name: str
    event_longitude: Optional[float] = 0.00
    event_latitude: Optional[float] = 0.00
    event_tag: EventCategory
    event_date: datetime
    event_capacity: int
    created_at: datetime
    updated_at: datetime


class EventCreateModel(BaseModel):
    event_name: str
    event_description: str
    event_location_name: str
    event_longitude: Optional[float] = 0.00
    event_latitude: Optional[float] = 0.00
    event_tag: EventCategory
    event_date: str
    event_capacity: int


class EventUpdateModel(BaseModel):
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_location_name: Optional[str] = None
    event_longitude: Optional[float] = 0.00
    event_latitude: Optional[float] = 0.00
    event_tag: EventCategory = None
    event_date: Optional[str] = None
    event_capacity: Optional[str] = None


class EventCreateForm(EventCreateModel):
    @classmethod
    def as_form(
        cls,
        event_name: str = Form(...),
        event_description: str = Form(...),
        event_location_name: str = Form(...),
        event_longitude: float = Form(0.00),
        event_latitude: float = Form(0.00),
        event_tag: EventCategory = Form(...),
        event_date: str = Form(...),
        event_capacity: int = Form(...),
    ):
        return cls(
            event_name=event_name,
            event_description=event_description,
            event_location_name=event_location_name,
            event_longitude=event_longitude,
            event_latitude=event_latitude,
            event_tag=event_tag,
            event_date=event_date,
            event_capacity=event_capacity,
        )
