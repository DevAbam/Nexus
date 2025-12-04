from fastapi import status, APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database_config import get_session
from src.services.ticket_service import TicketService
from typing import List
from src.schemas.ticket_schemas import (
    TicketCreateModel,
    TicketModel,
    TicketScanModel,
    TicketScanResponse,
)

ticket_router = APIRouter()
ticket_service = TicketService()


@ticket_router.post(
    "/buy", status_code=status.HTTP_201_CREATED, response_model=List[TicketModel]
)
async def buy_ticket(
    ticket_data: TicketCreateModel,
    session: AsyncSession = Depends(get_session),
):
    created_tickets = await ticket_service.create_ticket(ticket_data, session)
    return created_tickets


@ticket_router.patch("/scan", response_model=TicketScanResponse)
async def scan_ticket(
    scan_data: TicketScanModel, session: AsyncSession = Depends(get_session)
):
    ticket = await ticket_service.scan_ticket(scan_data, session)
    return TicketScanResponse(
        message="Ticket scan success",
        status=ticket.ticket_status,
        success=True,
        ticket_uid=ticket.ticket_uid,
    )
