from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime


class Event(SQLModel, table=True):
    __tablename__ = "tbl_events"
    event_uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_name: str = Field(nullable=False, min_length=3, max_length=200)
    event_description: str = Field(nullable=False, min_length=3)
    event_location_name: str = Field(nullable=False)
    event_date: datetime
    event_capacity: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
