from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from typing import List, Optional

# from src.models.Ticket import Ticket


class EventCategory(str, Enum):
    MUSIC = "music"
    SPORTS = "sports"
    BUSINESS = "business"
    EDUCATION = "education"
    RELIGION = "religion"
    TECH = "tech"
    ART = "art"
    FOOD = "food"
    COMMUNITY = "community"


class Event(SQLModel, table=True):
    __tablename__ = "tbl_events"
    event_uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_name: str = Field(nullable=False, min_length=3, max_length=200)
    event_description: str = Field(nullable=False, min_length=3)
    event_location_name: str = Field(nullable=False)
    event_longitude: Optional[float] = 0.00
    event_latitude: Optional[float] = 0.00
    event_poster_url: str = Field(nullable=False)
    event_poster_file_id: str | None = Field(default=None)
    event_tag: EventCategory = Field(nullable=False)
    event_date: datetime
    event_capacity: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    # Relationships
    tickets: List["Ticket"] = Relationship(
        back_populates="event", sa_relationship_kwargs={"lazy": "selectin"}
    )
