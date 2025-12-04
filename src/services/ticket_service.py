from src.schemas.ticket_schemas import TicketCreateModel, TicketScanModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.Ticket import Ticket
from sqlmodel import select
from fastapi import HTTPException, status
from src.models.Ticket import TicketStatus
from src.services.event_service import EventService
from datetime import datetime

event_service = EventService()


class TicketService:
    async def create_ticket(
        self, ticket_data: TicketCreateModel, session: AsyncSession
    ):
        ticket_data_dict = ticket_data.model_dump()
        tickets_bought = []
        purchase_quantity = ticket_data.quantity
        event_uid = ticket_data.event_uid

        if purchase_quantity == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="quantity should be at least 1",
            )

        event_exists = await event_service.get_event_by_Id(event_uid, session)

        if event_exists is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="event with specified id not found",
            )
        else:
            for _ in range(purchase_quantity):
                new_ticket = Ticket(**ticket_data_dict)
                session.add(new_ticket)
                await session.commit()
                await session.refresh(new_ticket)
                tickets_bought.append(new_ticket)

            return tickets_bought

    async def scan_ticket(self, scan_data: TicketScanModel, session: AsyncSession):
        result = await session.exec(
            select(Ticket).where(
                Ticket.ticket_code == str(scan_data.ticket_code),
                Ticket.event_uid == scan_data.event_uid,
            )
        )
        ticket = result.first()

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
            )

        if ticket.ticket_status == TicketStatus.USED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Ticket already used"
            )

        ticket.ticket_status = TicketStatus.USED
        ticket.scanned_at = datetime.now()
        await session.commit()
        await session.refresh(ticket)
        return ticket
