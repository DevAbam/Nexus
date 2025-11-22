import uuid
from datetime import datetime, date
from pydantic import BaseModel


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
