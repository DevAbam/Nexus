import uuid
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional
from src.models.Event import EventCategory


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
