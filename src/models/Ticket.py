from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

# from src.models.Event import Event


class TicketStatus(str, Enum):
    USED = "used"
    UNUSED = "unused"


class Ticket(SQLModel, table=True):
    __tablename__ = "tbl_tickets"
    ticket_uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ticket_code: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    ticket_status: TicketStatus = Field(default=TicketStatus.UNUSED)
    created_at: datetime = Field(default_factory=datetime.now)
    scanned_at: Optional[datetime] = None
    # relationsgipis
    event_uid: uuid.UUID = Field(foreign_key="tbl_events.event_uid")
    event: Optional["Event"] = Relationship(back_populates="tickets")
