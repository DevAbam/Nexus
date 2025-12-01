from src.schemas.ticket_schemas import TicketCreateModel, TicketScanModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.Ticket import Ticket
from sqlmodel import select
from fastapi import HTTPException, status
from src.models.Ticket import TicketStatus


class TicketService:
    async def create_ticket(
        self, ticket_data: TicketCreateModel, session: AsyncSession
    ):
        ticket_data_dict = ticket_data.model_dump()
        new_ticket = Ticket(**ticket_data_dict)
        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)
        return new_ticket

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
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        return ticket
