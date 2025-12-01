import uuid
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class EventModel(BaseModel):
    event_uid: uuid.UUID
    event_name: str
    event_description: str
    event_location_name: str
    event_date: datetime
    event_capacity: int
    created_at: datetime
    updated_at: datetime


class EventCreateModel(BaseModel):
    event_name: str
    event_description: str
    event_location_name: str
    event_date: str
    event_capacity: int


class EventUpdateModel(BaseModel):
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_location_name: Optional[str] = None
    event_date: Optional[str] = None
    event_capacity: Optional[str] = None
