from sqlalchemy.ext.asyncio import create_async_engine
from src.config.settings import settings
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
