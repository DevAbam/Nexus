from pydantic import BaseModel
import uuid
from datetime import datetime
from src.models.Ticket import TicketStatus
from src.models.Event import Event


class TicketCreateModel(BaseModel):
    event_uid: uuid.UUID


class TicketModel(BaseModel):
    ticket_uid: uuid.UUID
    ticket_code: str
    ticket_status: TicketStatus
    created_at: datetime
    event_uid: uuid.UUID
    # event: Event


class TicketScanModel(BaseModel):
    ticket_code: uuid.UUID
    event_uid: uuid.UUID


class TicketScanResponse(BaseModel):
    success: bool
    ticket_uid: uuid.UUID
    status: TicketStatus
    message: str
