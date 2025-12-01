from fastapi import FastAPI
from src.controller.event_router import event_router
from src.controller.ticket_router import ticket_router
from contextlib import asynccontextmanager
from src.db.database_config import init_db

version = "v1"


@asynccontextmanager
async def life_span(app: FastAPI):
    print("starting...")
    await init_db()
    yield
    print("shutting down...")


app = FastAPI(
    title="Nexus",
    description="An Event Management and Ticketing purchase api",
    version=version,
    lifespan=life_span,
)

app.include_router(event_router, prefix="/events", tags=["Events"])
app.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])
