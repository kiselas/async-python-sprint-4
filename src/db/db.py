from core.config import app_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_async_engine(app_settings.database_dsn, echo=app_settings.db_engine_echo, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
